#!/usr/bin/env python3
"""Velvet Authority - daily new-in collector.

Collects *verifiable* new-in candidates from the seven retailers using only
public, crawler-friendly routes (the public new-in pages, product pages and
robots.txt-listed sitemaps). It never solves bot challenges, never logs in and
never touches carts. Retailers that answer with a bot challenge or a block are
recorded as such in the status output.

Output: scan/out/candidates-YYYY-MM-DD.json  (input for the daily curated report)
State : scan/state/*.txt.gz                   (sitemap snapshots, to prove "new")

Usage: python3 -I scan/scan.py [--date YYYY-MM-DD]
"""
import gzip, html, json, os, re, sys, time, urllib.request, urllib.error, datetime

HERE = os.path.dirname(os.path.abspath(__file__))
STATE = os.path.join(HERE, "state")
OUT = os.path.join(HERE, "out")
UA = "Mozilla/5.0 (compatible; VelvetScan/1.0; personal shopping digest)"
PAUSE = 1.0

OFFICIAL = {
    "Gina Tricot": "https://www.ginatricot.com/nl/nieuws",
    "H&M": "https://www2.hm.com/content/hmonline/nl_nl/dames/new-arrivals/kleding.html",
    "Zara": "https://www.zara.com/be/nl/dames-nieuw-in-l1180.html",
    "Stradivarius": "https://www.stradivarius.com/nl/dames/nieuw-n1906",
    "NA-KD": "https://www.na-kd.com/nl/nieuw-binnen",
    "Mango": "https://shop.mango.com/nl/nl/c/dames/nieuw_8c5a3c5f",
    "Pull&Bear": "https://www.pullandbear.com/nl/",
}
FALLBACK = {"Gina Tricot": "https://www.zalando.nl/gina-tricot/", "Stradivarius": "https://www.asos.com/nl/stradivarius/cat/?cid=27012",
            "Pull&Bear": "https://www.zalando.nl/pull-bear/"}

# NA-KD new-in filters (links taken from the new-in page's own navigation)
NAKD_CATS = {"jassen": ["32893", "317966", "32895"], "tassen": ["32944"], "tops": ["32884", "32877", "90356", "385550", "32880"],
             "broeken": ["32897", "469504", "33043"], "schoenen": ["32961"]}


def get(url, tries=2):
    last = None
    for i in range(tries):
        try:
            req = urllib.request.Request(url, headers={"User-Agent": UA, "Accept-Language": "nl-NL,nl;q=0.9"})
            with urllib.request.urlopen(req, timeout=40) as r:
                data = r.read()
                if url.endswith(".gz") or data[:2] == b"\x1f\x8b":
                    data = gzip.decompress(data)
                return r.status, data.decode("utf-8", "ignore")
        except urllib.error.HTTPError as e:
            return e.code, ""
        except Exception as e:  # network / proxy
            last = str(e)
            time.sleep(2)
    return 0, last or ""


def classify(status, body):
    if status == 0:
        return "geen verbinding (" + (body[:80] or "netwerk") + ")"
    if status in (403, 429):
        return f"geblokkeerd door de webshop (HTTP {status}, botbescherming)"
    if "bm-verify" in body or "/_sec/verify" in body or "interstitial" in body[:4000]:
        return "botcontrole (Akamai-interstitial); productgrid niet bereikbaar zonder browserverificatie"
    if status >= 400:
        return f"HTTP {status}"
    return None


def ld_blocks(h):
    out = []
    for m in re.finditer(r'<script[^>]*ld\+json[^>]*>(.*?)</script>', h, re.S):
        try:
            out.append(json.loads(m.group(1)))
        except Exception:
            pass
    return out


def page_text(h):
    body = re.sub(r"<script.*?</script>|<style.*?</style>", " ", h, flags=re.S)
    return re.sub(r"\s+", " ", html.unescape(re.sub(r"<[^>]+>", " ", body)))


def nakd_product(url):
    st, h = get(url)
    if st != 200:
        return {"url": url, "error": f"HTTP {st}"}
    prod = next((b for b in ld_blocks(h) if isinstance(b.get("offers"), list)), None)
    if not prod:  # ProductGroup variant
        grp = next((b for b in ld_blocks(h) if b.get("@type") == "ProductGroup"), None)
        sku = url.rsplit("-", 3)[-3:]
        if grp:
            vs = [v for v in grp.get("hasVariant", []) if v.get("url") == url] or grp.get("hasVariant", [])
            prod = {"name": grp.get("name"), "description": grp.get("description"), "image": vs[0].get("image") if vs else None,
                    "color": vs[0].get("color") if vs else None, "offers": [v["offers"] for v in vs if "offers" in v], "url": url}
    if not prod:
        return {"url": url, "error": "geen productdata"}
    offers = prod["offers"] if isinstance(prod["offers"], list) else [prod["offers"]]
    txt = page_text(h)
    colour = re.search(r"Kleur : ([^ ]+(?: [a-z]+)?)", txt)
    model = re.search(r"Dit model is ([^.]{3,70}?)\s+Omrekentabel", txt)
    i, j = txt.find("Precies op maat Groot"), txt.find("Artikelnummer")
    desc = txt[i + 22:j].strip() if 0 < i < j else (prod.get("description") or "")
    was = (offers[0].get("priceSpecification") or {}).get("price")
    sizes, seen = [], set()
    for o in offers:
        s = o.get("size")
        if s and s not in seen:
            seen.add(s)
            sizes.append(s + ("" if o.get("availability", "").endswith("InStock") else " (uitverkocht)"))
    return {"retailer": "NA-KD", "name": prod.get("name"), "url": url, "image": prod.get("image"),
            "colour_page": colour.group(1) if colour else prod.get("color"), "price": offers[0].get("price"),
            "was": was, "currency": offers[0].get("priceCurrency"), "sizes": sizes,
            "model": model.group(1) if model else None, "description": desc[:900]}


def scan_nakd():
    status = {"retailer": "NA-KD", "officialAccessible": False, "gridReadable": False, "fallbackUsed": None,
              "fallbackReason": None, "verified": False, "limitation": None}
    st, h = get(OFFICIAL["NA-KD"])
    lim = classify(st, h)
    if lim:
        status["limitation"] = lim
        return status, {}
    status["officialAccessible"] = True
    cands = {}
    for cat, ids in NAKD_CATS.items():
        urls = []
        for cid in ids:
            for attempt in range(3):  # the server-rendered list is occasionally missing; retry politely
                time.sleep(PAUSE * (1 + 2 * attempt))
                st, h = get(f"{OFFICIAL['NA-KD']}?p_categories_nl-nl=c_1-{cid}")
                lists = [b for b in ld_blocks(h) if b.get("@type") == "ItemList"]
                if lists:
                    for b in lists:
                        urls += [i["url"] for i in b.get("itemListElement", [])]
                    break
        urls = list(dict.fromkeys(urls))
        cands[cat] = [{"url": u, "name_list": None} for u in urls]
    status["gridReadable"] = any(cands.values())
    status["limitation"] = "Productgrid via de server-gerenderde productlijst (eerste ~36 per filter); materiaalsamenstelling laadt dynamisch en is niet altijd uitleesbaar."
    return status, cands


def sitemap_diff(name, sitemap_url, product_re, today):
    """Return (new_urls, baseline_created) by comparing with yesterday's snapshot."""
    os.makedirs(STATE, exist_ok=True)
    st, x = get(sitemap_url)
    if st != 200:
        return None, f"sitemap HTTP {st}"
    urls = sorted(set(u for u in re.findall(r"<loc>([^<]+)</loc>", x) if re.search(product_re, u)))
    path = os.path.join(STATE, f"{name}.txt.gz")
    prev = None
    if os.path.exists(path):
        with gzip.open(path, "rt") as f:
            prev = set(f.read().split())
    with gzip.open(path, "wt") as f:
        f.write("\n".join(urls))
    if prev is None:
        return [], "eerste momentopname opgeslagen; vanaf de volgende scan zijn nieuwe producten aantoonbaar"
    return [u for u in urls if u not in prev], None


def gina_product(url):
    st, h = get(url)
    if st != 200:
        return {"url": url, "error": f"HTTP {st}"}
    p = next((b for b in ld_blocks(h) if b.get("@type") == "Product"), None)
    if not p:
        return {"url": url, "error": "geen productdata"}
    offers = p.get("offers") or []
    offers = offers if isinstance(offers, list) else [offers]
    sizes = []
    for o in offers:
        s = o.get("size") or (o.get("itemOffered") or {}).get("size") or o.get("name")
        if isinstance(s, dict):
            s = s.get("name")
        sizes.append(f"{s}{'' if str(o.get('availability','')).endswith('InStock') else ' (uitverkocht)'}")
    img = p.get("image")
    return {"retailer": "Gina Tricot", "name": p.get("name"), "url": url, "image": img[0] if isinstance(img, list) else img,
            "colour_page": p.get("color"), "price": offers[0].get("price") if offers else None,
            "currency": offers[0].get("priceCurrency") if offers else None, "sizes": sizes,
            "description": (p.get("description") or "")[:900]}


def main():
    today = datetime.date.today().isoformat()
    if "--date" in sys.argv:
        today = sys.argv[sys.argv.index("--date") + 1]
    os.makedirs(OUT, exist_ok=True)
    result = {"date": today, "status": [], "candidates": {}}

    # NA-KD
    st_nakd, cands = scan_nakd()
    for cat, items in cands.items():
        for it in items:
            time.sleep(PAUSE)
            it.update(nakd_product(it["url"]))
        result["candidates"].setdefault(cat, []).extend(cands[cat])
    st_nakd["verified"] = any(not i.get("error") for v in cands.values() for i in v)
    result["status"].append(st_nakd)

    # Gina Tricot: new-in grid is rendered client-side -> sitemap diff + product pages
    st, h = get(OFFICIAL["Gina Tricot"])
    gs = {"retailer": "Gina Tricot", "officialAccessible": st == 200 and not classify(st, h), "gridReadable": False,
          "fallbackUsed": None, "fallbackReason": None, "verified": False, "limitation": None}
    new, note = sitemap_diff("ginatricot-nl", "https://www.ginatricot.com/market_sitemaps/nl/sitemap.xml", r"-\d{9}$", today)
    fst, fh = get(FALLBACK["Gina Tricot"])
    flim = classify(fst, fh)
    gs["limitation"] = ("Nieuw-in-grid laadt pas in de browser (niet in de HTML). Nieuw = verschenen in de officiële sitemap sinds de vorige scan. "
                        + (note or f"{len(new or [])} nieuwe product-URL's gevonden.") + (f" Fallback Zalando: {flim}." if flim else ""))
    gs["fallbackReason"] = f"Zalando geprobeerd: {flim}" if flim else None
    gina = []
    for u in (new or [])[:80]:
        time.sleep(PAUSE)
        gina.append(gina_product(u))
    if gina:
        gs["gridReadable"] = True
        gs["verified"] = any(not g.get("error") for g in gina)
        result["candidates"]["gina_tricot_nieuw"] = gina
    result["status"].append(gs)

    # Retailers without a readable public route from this environment
    for r in ["H&M", "Zara", "Stradivarius", "Mango", "Pull&Bear"]:
        time.sleep(PAUSE)
        st, h = get(OFFICIAL[r])
        lim = classify(st, h)
        row = {"retailer": r, "officialAccessible": not lim, "gridReadable": False, "fallbackUsed": None,
               "fallbackReason": None, "verified": False, "limitation": lim or "pagina geladen, maar productgrid laadt pas in de browser"}
        if r in FALLBACK:
            fst, fh = get(FALLBACK[r])
            flim = classify(fst, fh)
            row["fallbackReason"] = f"{'ASOS' if r == 'Stradivarius' else 'Zalando'} geprobeerd: {flim or 'bereikbaar, maar nieuw-zijn niet aantoonbaar'}"
        result["status"].append(row)

    order = list(OFFICIAL)
    result["status"].sort(key=lambda s: order.index(s["retailer"]))
    path = os.path.join(OUT, f"candidates-{today}.json")
    with open(path, "w") as f:
        json.dump(result, f, ensure_ascii=False, indent=1)
    print(path)
    for s in result["status"]:
        print(f"- {s['retailer']}: bereikbaar={s['officialAccessible']} grid={s['gridReadable']} geverifieerd={s['verified']} | {s['limitation']}")
    print({k: len(v) for k, v in result["candidates"].items()})


if __name__ == "__main__":
    main()
