## Session 1 — 2026-11-25

**Bron:** ruwe opname 8:39 via Google Drive (HEVC 1080x1920 30fps, 457 MB). Pincurl reveal na 12 uur; resultaat valt tegen (duim omlaag = clou, gebruiker wil die erin).
**Strategy:** ~25s Reel in ref2-stijl (snelle cuts 1.5–3s), chronologisch: hook (handen gevouwen, sjaal om) → sjaal af → pins eruit/krullen vallen → losschudden → uitborstelen → redden (haarzwiep) → duim omlaag (4.5s hold). Geen captions (gebruikerswens), wel titel "pincurl reveal na 12 uur" (Liberation Serif 84, wit, y=360, hele video). Geen geluid: muziek voegt gebruiker toe in de app.
**Decisions:** zie `edl.json` / `cut.py` (12 shots, 25.1s). Weglopen (3:56–4:22, 7:46–7:58) en herhalingen eruit.
**Reasoning log:** Niet openen met eindresultaat omdat het resultaat tegenvalt: spanning opbouwen naar de duim. Shots per stuk geëxtraheerd (één filtergraph met 12 trims liep OOM op de 8.6 min HEVC).
**Outstanding:** feedback op v1 (tempo, shotkeuze, titel aan/uit, lengte).

## Session 1b — 2026-11-25 (v2)

**Feedback:** titel niet de hele tijd in beeld.
**Decisions:** titel alleen 0–4.6s (hook + sjaal af), fade-out 0.3s. Verder gelijk aan v1.
**Outstanding:** verdere feedback op v2.

## Session 1c — 2026-11-25 (v3)

**Feedback:** eindshot te lang; pins eruithalen sneller; netter sjaal-af-shot.
**Decisions:** sjaal af nu 29.2–31.6 (sjaal als gordijn opgetild, dan gezicht met pins) i.p.v. 26–29 (fladderig). Pin-shots ingekort naar 1.0–1.3s. Eindshot 4.5s → 2.8s (509.8–512.6). Titel 0–4.0s. Totaal 25.1s → 20.2s.
**Outstanding:** feedback op v3.

## Session 1d — 2026-11-25 (v4)

**Vraag gebruiker:** titel hoog, midden of weg?
**Decisions:** titel naar borsthoogte (y=1180), zelfde plek als huis-captions. Hoog bedekte haar/sjaal (onderwerp van de video), midden viel op kin/mond. Weglaten niet: zonder gesproken tekst geeft "12 uur" de context en de nieuwsgierigheid voor de eerste seconde.
**Outstanding:** feedback op v4.

## Session 1e — 2026-11-25 (v5)

**Feedback:** titel op 2 regels, mooier lettertype.
**Decisions:** Playfair Display 96: "pincurl reveal" regular / "na 12 uur" italic, borsthoogte, 0–4s. 5 fonts vergeleken (title-font-options.jpg); Playfair-mix gekozen om editorial look + leesbaarheid. fontselect-log bevestigt dat de font laadde.
**Outstanding:** feedback op v5.

## Session 1f — 2026-11-25 (v6)

**Feedback:** fontlijst van dafont (Moglite, adelia, Mistrully, …); kies 1 of combineer 2, mooi en leesbaar.
**Decisions:** dafont geblokkeerd + meestal alleen persoonlijk gebruik, dus vrije Google-lookalikes: DM Serif Display (≈Moglite) + Mrs Saint Delafield (≈adelia/Mistrully), 6 scripts vergeleken. Script \fs280, blok op y=1230 (vrij van kin en TikTok-UI).
**Outstanding:** feedback op v6.

## Session 1g — 2026-11-25 (v7)

**Feedback:** akkoord met v6-stijl, maar cijfer "12" te groot.
**Decisions:** alleen "12" op \fs190 (rest script \fs280); cijfers in dit script zijn van zichzelf te groot. Vastgelegd in tools/fonts/README.md.
**Outstanding:** feedback op v7.

## Session 1h — 2026-11-25 (v8)

**Feedback:** te veel ruimte tussen bovenste en onderste regel.
**Decisions:** titel als 2 losse events (regel 1 \an2 y=1160, regel 2 \an5 y=1220) i.p.v. \N; gap getest op 1150–1240, 1220 = strak zonder overlap.
**Outstanding:** feedback op v8.
