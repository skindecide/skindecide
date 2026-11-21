# Dagelijkse Velvet Authority-scan — werkinstructie

Deze instructie wordt elke dag uitgevoerd. Het resultaat is één JSON-bestand in
`velvet-authority/reports/JJJJ-MM-DD.json` plus een bijgewerkte `reports/index.json`.
De app (`velvet-authority/index.html`) toont dat rapport.

**Koop niets, plaats niets in winkelmandjes, voer geen bestellingen uit.**
**Verzin nooit producten, prijzen, maten, voorraad, kleuren of links.**

## 0. Werkwijze

1. Draai `python3 -I velvet-authority/scan/scan.py`. Dit verzamelt via openbare routes (nieuw-in-pagina's, productpagina's, sitemaps uit robots.txt) de verifieerbare kandidaten in `scan/out/candidates-JJJJ-MM-DD.json`, met de status van alle zeven retailers. Het werkt de sitemap-momentopname in `scan/state/` bij; die moet je meecommitten, want alleen zo is "nieuw sinds gisteren" aantoonbaar voor Gina Tricot.
2. Kies uit de kandidaten de beste matches per categorie volgens de regels hieronder. Bekijk van elke kandidaat de productfoto (download de `image` en bekijk hem) voordat je kleur en silhouet beoordeelt.
3. Schrijf het rapport-JSON en werk `reports/index.json` bij.
4. **Nooit** botcontroles omzeilen, browserverificatie oplossen of interne API's van de shops aanroepen. Blokkeert een shop, dan staat dat eerlijk in de scanstatus.

## 1. Retailers (alle zeven, elke dag)

| Retailer | Primaire bron | Fallback |
|---|---|---|
| Gina Tricot | https://www.ginatricot.com/nl/nieuws | Zalando (+ officiële Engelstalige site) |
| H&M | https://www2.hm.com/content/hmonline/nl_nl/dames/new-arrivals/kleding.html | geen |
| Zara | https://www.zara.com/be/nl/dames-nieuw-in-l1180.html | geen |
| Stradivarius | https://www.stradivarius.com/nl/dames/nieuw-n1906 | ASOS (+ officiële Engelstalige site) |
| NA-KD | https://www.na-kd.com/nl/nieuw-binnen | geen |
| Mango | https://shop.mango.com/nl/nl/c/dames/nieuw_8c5a3c5f | geen |
| Pull&Bear | https://www.pullandbear.com/nl/ (nieuw-in via navigatie) | Zalando |

- Altijd eerst de officiële nieuw-in-pagina. Als die niet werkt: directe URL opnieuw, navigatie van dezelfde shop, officiële Engelstalige route (alleen Gina Tricot en Stradivarius), andere openbare route binnen dezelfde retailer, gekoppelde productpagina's, en pas dan de afgesproken fallback.
- Een fallback is alleen voor producten van díe retailer, en alleen als het product aantoonbaar nieuw is (nieuw-in-filter, "nieuw"-label of vergelijkbaar). Vermeld altijd dat een fallback is gebruikt en waarom.
- Sla nooit een retailer over.
- Bepaal bij een probleem wat er speelt: dynamisch geladen grid, cookie-, regio- of sessieprobleem, botbescherming, foutieve of geblokkeerde pagina, of een niet-toegankelijke productpagina.

## 2. Stijl: Velvet Authority

Quiet luxury: chic, vrouwelijk, volwassen, zelfverzekerd, verzorgd.
Kleuren: espresso, chocoladebruin, zwart, ivoor, crème, taupe, camel, oxblood, bordeaux, gedempt olijfgroen.
Materialen en details: satijn, wol, fijn breiwerk, suède- en leerlook, elegante tailoring, taille-accenten, cleane lijnen, subtiele details.
Referentie: espresso satijnen slipdress met subtiele split, minimalistische gouden sieraden, nude hakken, sleek donker haar, warme bronzen make-up, oxblood accenten.
Vermijden: grote logo's, drukke prints, goedkope afwerking, trends die niet passen.

## 3. Figuur en petite-fit

153 cm, circa 58 kg, zachte zandloper, taille 66, heup 100, borst 92 cm.
Voorrang voor: hoge tailles, duidelijke taille-accenten, proportionele lengtes, verticale lijnen, aansluitende of mooi gevormde silhouetten. Niet vormloos of overdreven oversized.
Beoordeel per item: lengte, taillehoogte, schouderlijn, mouwlengte, totale proporties. Controleer maatinformatie op de productpagina; geen aannames.
**Als de maattabel een lengte vermeldt** (jas/top: lengte vanaf schouder; broek: binnenbeenlengte en rise; rok: lengte), neem die op in `lengthCm` / `riseCm` en noem bij welke maat (`lengthSize`). De paskamer in de app gebruikt dit om op haar foto te tonen waar de zoom valt.

## 4. Categorieën (altijd alle vijf, in deze volgorde)

`jassen`, `tassen`, `tops` (Shirts & tops), `broeken`, `schoenen`.
Maximaal 3 per categorie, gerangschikt op stijlmatch en draagbaarheid. Nooit forceren. Geen match: lege lijst en een korte reden in `noMatch`; de app toont dan "Geen sterke match vandaag."

## 5. Verificatie per product

1. Controleer de actuele nieuw-in-pagina. 2. Open de directe productpagina. 3. Bekijk de productafbeeldingen. 4. Controleer de exacte variant en kleur. 5. Controleer de actuele prijs. 6. Controleer beschikbaarheid en maten indien mogelijk. 7. Gebruik de directe product-URL.
Niet op zoekresultaat-snippets of categoriepagina's alleen baseren. Wat niet te verifiëren is: weglaten of expliciet als "niet verifieerbaar" markeren.

## 6. Eerdere rapporten

Lees de bestaande rapporten in `reports/`. Herhaal niet onnodig dezelfde producten. Meld het wel (veld `change`) als een eerder gezien product nieuw beschikbaar is, van prijs veranderd is, terugkomt in een relevante kleur, of weer in een relevante maat beschikbaar is. Zijn er weinig sterke nieuwe matches: zeg dat in `summary`.

## 7. JSON-formaat

```json
{
  "date": "2026-11-22",
  "summary": "Korte samenvatting van de dag in het Nederlands.",
  "categories": {
    "jassen": [
      {
        "name": "Exacte productnaam",
        "brand": "Mango",
        "retailer": "Mango",
        "source": "officieel",
        "fallbackSite": null,
        "fallbackReason": null,
        "price": "79,99",
        "currency": "EUR",
        "color": "Exacte kleur/variant",
        "sizes": "Beschikbaar in XS–L (gecontroleerd op productpagina) — of 'Niet verifieerbaar'",
        "url": "https://directe-productpagina",
        "image": "https://directe-afbeelding-url-van-de-productpagina (alleen als betrouwbaar)",
        "label": "sterk | eventueel | overslaan",
        "why": "Waarom het bij Velvet Authority past.",
        "petite": "Petite-fit aandachtspunt.",
        "outfit": "Concrete outfitcombinatie.",
        "lengthCm": 92,
        "lengthSize": "S",
        "riseCm": null,
        "garmentType": "jas | top | jurk | rok | broek",
        "change": "Optioneel: 'Prijs verlaagd van 89,99' / 'Nieuwe kleur' / 'Weer in maat S'"
      }
    ],
    "tassen": [], "tops": [], "broeken": [], "schoenen": []
  },
  "noMatch": { "tassen": "Korte reden waarom er vandaag geen sterke match is." },
  "topPicks": ["Twee of drie beste vondsten van de dag, met korte reden."],
  "scanStatus": [
    {
      "retailer": "Zara",
      "officialAccessible": true,
      "gridReadable": true,
      "fallbackUsed": null,
      "fallbackReason": null,
      "verified": true,
      "limitation": "Welke technische beperking optrad, of null"
    }
  ]
}
```

`scanStatus` bevat altijd precies zeven regels, één per retailer. Voeg daarna de bestandsnaam toe aan `reports/index.json` (`{"reports": ["2026-11-22.json", ...]}`), commit en push.
