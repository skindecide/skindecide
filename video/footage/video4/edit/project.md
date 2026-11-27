## Session 1 — 2026-11-27

**Bron:** 8:52 4K60 HEVC (staand, rotatie 90) via Google Drive, 4.3 GB. Heatless curls (sjaal + roze rollers + pins), voorkantjes te heftig → bijgewerkt met Airwrap.
**Strategy:** ~20s, zonder geluid (muziek in app), huisstijl v2-titel "another day / another blowout" (typewriter + roze glitch) 0–2.4s op borsthoogte. Snelle cuts 1–1.5s: sjaal af → rollers/pins eruit → haarzwiep/volume → volume → airwrap voorkantjes → achterkant → eindresultaat.
**Decisions:** zie `edl.json`/`cut.py` (13 shots, 19.5s). Beeld onaangetast: alleen knippen + verkleinen 4K→1080×1920 (lanczos), 60fps behouden, bt709-tags. Gemiddelde RGB frame bron 96.7/94.6/87.3 vs export 96.6/93.6/87.2. CRF 20 om bestand klein te houden.
**Outstanding:** feedback op v1.

## Session 1b — 2026-11-27 (v2)

**Feedback:** krullen die uit de pins vallen zichtbaarder (satisfying); titelregels "another/blowout" te ver uit elkaar; eerste airwrap-shot (400s) ongemakkelijk.
**Decisions:** 4 drop-shots van 1.6–2.4s die de hele beweging tonen: 24.4–26.2 (pin, krul valt), 52.4–54.2 (pin, lange krul), 117.4–119.8 (roller afgerold), 130.2–131.8 (roller, haar vliegt los). Airwrap nu 405.0–406.3 + 478.5–479.8. Volume-shot 255s eruit, eindshot 2.8s. Titel: grote regels als losse events, TITLE_LINE_STEP 105 (vaste huisstijl). 20.9s.
**Outstanding:** feedback op v2.

## Session 1c — 2026-11-27 (v3)

**Feedback:** achterkant-shot langer; drop-shots hadden niet de mooiste krullen, alleen mooie krullen kiezen.
**Decisions:** drops vervangen door gedefinieerde spiraalkrullen: 36.4–38.4, 46.8–48.4, 64.6–66.4, plus glorie-shot alle krullen 123.7–125.0. Afgewezen: 24s/53s (pluizig/gedraaid), roller-shots 117s/130s (steil haar). Achterkant 512.6–516.2 (over schouder → achterkant, 3.6s i.p.v. 1.5s). Losschud-shot 162s eruit. 20.9s.
**Les:** bij reveals op krulkwaliteit selecteren (strak, spiraal, veerkrachtig), niet alleen op beweging.
**Outstanding:** feedback op v3.

## Session 1d — 2026-11-27 (v4)

**Feedback:** bovenkant loslaten mist; shot op 0:06 (pin zijkant 64.6s) ongemakkelijk, niets gebeurt; achterkant-shot mag een knip.
**Decisions:** + bovenkant: 111.2–112.6 (roller afgerold) en 140.8–142.2 (laatste roller eruit). − 64.6–66.4. Achterkant gesplitst: 512.6–513.8 (over schouder) | 514.3–515.9 (zwiepen), omdraaien eruit. 21.1s.
**Outstanding:** feedback op v4.
