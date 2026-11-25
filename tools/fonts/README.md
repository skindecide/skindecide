# Fonts

From Google Fonts via the @fontsource npm packages (woff2 converted to TTF with fontTools).
All are licensed under the SIL Open Font License 1.1, so they are safe for commercial and
brand content.

**House title style** (chosen by the user from their dafont inspiration list, rebuilt
with free look-alikes):
- Line 1: **DM Serif Display** (looks like Moglite), `\fs104`
- Line 2: **Mrs Saint Delafield** (signature script, looks like adelia/Mistrully), `\fs280`
- ASS: `{\pos(540,1230)\fad(0,300)}line one\N{\fnMrs Saint Delafield\fs280}line two`

Other fonts here (Playfair Display, Cormorant Garamond, Bodoni Moda) were earlier options.

Why not the dafont originals: dafont.com is blocked on this network, and most of those
fonts are free for personal use only, so they need a licence for brand content.

With libass: `ass=file.ass:fontsdir=/home/user/skindecide/tools/fonts`. Check the
`fontselect:` lines (`-loglevel verbose`) to confirm the font loaded rather than a fallback.
Digits in Mrs Saint Delafield are oversized: wrap them in `{\\fs190}12{\\fs280}` so they
match the letters (the user asked for this). Script fonts render smaller in libass than in drawtext at the same size, so check a frame.
