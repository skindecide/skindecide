## Session 1 — 2026-11-28

**Bron:** 6:58 4K30 HEVC (staand) via Google Drive, 2.1 GB. Zelfde verhaal als video4: heatless pincurls onder sjaal, Airwrap voor de voorkant. Titel "another day / another blowout".
**Strategy:** recept van video4 v5: ~20s zonder geluid, alleen mooie krullen (strakke spiralen), bovenkant los, achterkant met knip, airwrap, eindresultaat.
**Decisions:** zie `edl.json`/`cut.py` (13 shots, 21.7s). Nieuwe titel-witruimte (gebruiker: "aesthetically pleasing kwa witruimte"): kleine regel 58px met letterspatiëring 5, 120px tot eerste grote regel, grote regels 105px; blok hangt onder de kin (--title-y 1095, kin op ~1020 in openingsshot). Kleurcheck: clip/export = bron via dezelfde yuv420p-route (56.4/54.5/52.3 vs 56.5/54.5/52.4); het eerdere ~1 punt verschil zat in de meetroute.
**Outstanding:** feedback op v1.

## Session 1b — 2026-11-28 (v2)

**Feedback/idee gebruiker:** het shot waarin ze ronddraait met de pins snel tonen met stops: voorkant, zijkant, achterkant, zijkant.
**Decisions:** "rondje" als 4 freeze-frames van 0.37s direct na sjaal af: 25.5 (voor), 24.5 (zijkant links, pins), 27.9 (achter), 28.8 (zijkant rechts, gouden pin). Volume-shot 166s eruit. 21.7s. Freeze = timing-effect op verzoek gebruiker; beeld zelf (kleur/uitsnede) ongewijzigd.
**Outstanding:** feedback op v2.

## Session 1c — 2026-11-28 (v3)

**Feedback:** titel "blowout of the day", waarbij "of the day" de bewegende tekst is; butter yellow i.p.v. roze.
**Decisions:** "blowout" stilstaand in Instrument Serif Italic crème 150px (--small-serif --static-small), "of the day" groot Nunito Black butter yellow (#F7E3A1) met pixel-glitch. 2 varianten vergeleken (klein sans vs. serif); serif gekozen: geeft het hoofdwoord gewicht en sluit aan bij de captions. --title-y 1100 --title-gap 135.
**Outstanding:** feedback op v3.

## Session 1d — 2026-11-28 (v4)

**Feedback:** rondje niet als stilstaande beelden maar bewegend en sneller; betere krul-val-shots; eindshot is ze nog haar aan het goedzetten; beginshot met de doek te lang.
**Decisions:** sjaal 17.8–19.4 (1.6s, was 2.6). Rondje = 4 bewegende clips van 0.3s in draairichting: 20.0 voor, 22.1 zij, 23.0 achter, 24.3 zij. Krul-val via OpenCV-bewegingspieken in haarzones + visuele check: 108.1–109.4 (lok valt), 118.6–119.8 en 122.6–124.0 (bovenkant los, krullen vallen naar voren), glorie 126.0–127.2. Eindshot 393–396 (haar zit, lacht, handen vrij). 19.5s.
**Outstanding:** feedback op v4.

## Session 1e — 2026-11-28 (v5)

**Feedback:** "of the day" langer glitchen; eindshot korter; sjaal sneller af; achterkant-shot waarin ze mooi in het midden staat (stond rechts); minder afstand tussen blowout en of the day.
**Decisions:** --glitch-cycles 5 (≈0.55s flikkeren, was ≈0.22s); --title-gap 115 (was 135); sjaal 18.4–19.4 (1.0s); achterkant vervangen door 245.0–247.4 (gecentreerd, haar recht); eindshot 393.5–395.7 (2.2s). Titel 0–2.2s. 17.5s.
**Outstanding:** feedback op v5.
