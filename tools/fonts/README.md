# Fonts

From Google Fonts via the @fontsource npm packages (woff2 converted to TTF with fontTools).
All are licensed under the SIL Open Font License 1.1.

- **Playfair Display** (Regular + Italic): **house title font**. Line 1 regular, line 2 italic.
- Cormorant Garamond, Bodoni Moda, DM Serif Display: alternatives the user was shown
  (`video/references/stijl/analyse/title-font-options.jpg`).

With libass: `ass=file.ass:fontsdir=/home/user/skindecide/tools/fonts`. Check the
`fontselect:` lines (`-loglevel verbose`) to confirm the font loaded rather than a fallback.
