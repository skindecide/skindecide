# Tekst-reference: "a week of working remotely" (gedeeld 2026-11-26)

Screenrecording van een TikTok (12s, `ref-tekst1.mp4`, niet in git). Gebruiker vindt de
manier van tekst-editing en het lettertype mooi.

## Wat er gebeurt

1. **Woord-voor-woord captions bij de voice-over:** één woord tegelijk, **groot**, in een
   **dunne cursieve schreefletter met sierlijke uithalen** (hoog contrast, lange staart aan
   de j, "editorial"), kleur **crème/ivoor** (warm gebroken wit, ~#FFF4D6) in plaats van
   puur wit. Midden in beeld op borsthoogte, geen box, nauwelijks schaduw. Harde wissel per
   woord, geen animatie.
2. **Titelkaart (~1.6–3s):** collage van 3 horizontale strips (typ-shots, split screen).
   Klein wit sans "a week of" verschijnt **letter voor letter (typewriter met cursor)**,
   dan groot **lichtroze, vet, rond sans** "working remotely" met een kort
   **pixel/kruissteek-glitch-effect**, plus kleine witte ondertitel
   "as a digital marketing manager".
3. **Hoofdstuk-labels:** "monday" in dezelfde cursieve schreefletter blijft staan midden in
   beeld, met **eronder klein sans** het gesproken woord dat wisselt ("to", "my", "calls").
   Dus: groot label + kleine meelopende captions.
4. **Montage:** snel (cuts ~0.5–1s), afwisselend dichtbij en wijde shots, split screen.

## Toepassen

- Captions: zelfde opzet als nu (één woord, borsthoogte), maar groter, cursief, crème.
  Lettertype dat het dichtst bij komt uit `tools/fonts/`: Playfair Display Italic
  (mock: `analyse/caption-mock.jpg`, links = huidige stijl). De echte reference is iets
  dunner/sierlijker.
- Titelkaart/hoofdstukken: voor vlogs of "dag/week van"-video's.

## Status: overgenomen als huisstijl v2 (2026-11-26)

Gebruiker: "alles, lettertypes en animaties". Gebouwd in `tools/house_style.py`:
captions Instrument Serif Italic crème (#FFF4D6) 250px met auto-verkleinen; titelkaart
typewriter (Inter Medium) + groot roze (#F7C8EA) Nunito Black met DotGothic16-pixelglitch
in/uit + witte ondertitel; hoofdstuklabels Instrument Serif Italic met kleine Inter-captions
eronder; collage van 3 stroken. Eerste toepassingen: Lancôme, Paula's Choice
(hoofdstuk "1 uur later"), pincurl v9 (collage + titelkaart).

## Harde regel gebruiker (2026-11-26)

**Niks aan het beeld veranderen.** Wel knippen, volgorde en tekst/animaties erop. Géén
kleurcorrectie, filters, bijsnijden, inzoomen, collages of split screen. (De collage uit
de tekst-reference wordt daarom níet overgenomen.)
