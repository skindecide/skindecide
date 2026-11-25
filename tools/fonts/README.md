# Fonts

From Google Fonts via the @fontsource npm packages (woff2 converted to TTF with fontTools).
All are licensed under the SIL Open Font License 1.1, so they are safe for commercial and
brand content.

**House title style** (chosen by the user from their dafont inspiration list, rebuilt
with free look-alikes):
- Line 1: **DM Serif Display** (looks like Moglite), `\fs104`
- Line 2: **Mrs Saint Delafield** (signature script, looks like adelia/Mistrully), `\fs280`
- ASS: two separate events. One `\N` line leaves a big gap because the script font has
  tall line metrics, so tune the gap by eye:
  `{\an2\pos(540,1160)}line one`
  `{\an5\pos(540,1220)\fnMrs Saint Delafield\fs280}na {\fs190}12{\fs280} uur`

Other fonts here (Playfair Display, Cormorant Garamond, Bodoni Moda) were earlier options.

Why not the dafont originals: dafont.com is blocked on this network, and most of those
fonts are free for personal use only, so they need a licence for brand content.

With libass: `ass=file.ass:fontsdir=/home/user/skindecide/tools/fonts`. Check the
`fontselect:` lines (`-loglevel verbose`) to confirm the font loaded rather than a fallback.
Digits in Mrs Saint Delafield are oversized: wrap them in `{\\fs190}12{\\fs280}` so they
match the letters (the user asked for this). Script fonts render smaller in libass than in drawtext at the same size, so check a frame.
