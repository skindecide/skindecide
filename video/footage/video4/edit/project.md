## Session 1 — 2026-11-27

**Bron:** 8:52 4K60 HEVC (staand, rotatie 90) via Google Drive, 4.3 GB. Heatless curls (sjaal + roze rollers + pins), voorkantjes te heftig → bijgewerkt met Airwrap.
**Strategy:** ~20s, zonder geluid (muziek in app), huisstijl v2-titel "another day / another blowout" (typewriter + roze glitch) 0–2.4s op borsthoogte. Snelle cuts 1–1.5s: sjaal af → rollers/pins eruit → haarzwiep/volume → volume → airwrap voorkantjes → achterkant → eindresultaat.
**Decisions:** zie `edl.json`/`cut.py` (13 shots, 19.5s). Beeld onaangetast: alleen knippen + verkleinen 4K→1080×1920 (lanczos), 60fps behouden, bt709-tags. Gemiddelde RGB frame bron 96.7/94.6/87.3 vs export 96.6/93.6/87.2. CRF 20 om bestand klein te houden.
**Outstanding:** feedback op v1.

## Session 1b — 2026-11-27 (v2)

**Feedback:** krullen die uit de pins vallen zichtbaarder (satisfying); titelregels "another/blowout" te ver uit elkaar; eerste airwrap-shot (400s) ongemakkelijk.
**Decisions:** 4 drop-shots van 1.6–2.4s die de hele beweging tonen: 24.4–26.2 (pin, krul valt), 52.4–54.2 (pin, lange krul), 117.4–119.8 (roller afgerold), 130.2–131.8 (roller, haar vliegt los). Airwrap nu 405.0–406.3 + 478.5–479.8. Volume-shot 255s eruit, eindshot 2.8s. Titel: grote regels als losse events, TITLE_LINE_STEP 105 (vaste huisstijl). 20.9s.
**Outstanding:** feedback op v2.
