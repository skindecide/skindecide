"""House text style v2, after video/references/tekst/ ("a week of working remotely").

Pieces (all rendered with libass from one generated .ass file):

  1. CAPTIONS: one spoken word at a time, big, thin italic serif (Instrument Serif Italic),
     cream (#FFF4D6), chest height, no box, faint shadow. Hard switch per word.
  2. TITLE CARD: small white sans line typed letter by letter with a cursor, then a big
     bold rounded pink line (Nunito Black, #F7C8EA) that glitches through a pixel font
     (DotGothic16) for a few frames, then a small white sans subtitle.
  3. CHAPTERS: a big italic serif label (e.g. "maandag") stays on screen. While it is up,
     the spoken words appear SMALL in white sans underneath, not as big italics.

RULE (from the user): never change the picture itself. Only cuts and text on top.
No colour grading, filters, crops, zooms, reframing, collages or split screens.
The original colour metadata (bt709, tv range) is copied to the output.

Usage:
  python tools/house_style.py render <video> -o out.mp4 \
      [--transcript words.json] [--fix "fout=goed" ...] \
      [--title "a week of|working remotely|as a digital marketing manager" --title-at 0 --title-dur 3] \
      [--chapter "maandag@4.0-9.5" ...] [--silent] [--no-loudnorm]

Title parts are split with "|": small|BIG|subtitle (subtitle optional). In BIG, "/" makes
a line break. --transcript takes Scribe-shaped JSON (transcribe_local.py output, or a
remapped copy for cut videos).
"""
from __future__ import annotations

import argparse
import json
import re
import subprocess
from pathlib import Path

FONTS = Path(__file__).resolve().parent / "fonts"

# Colours in ASS order (&HAABBGGRR)
CREAM = "&H00D6F4FF"   # #FFF4D6
PINK = "&H00EAC8F7"    # #F7C8EA
WHITE = "&H00FFFFFF"

SERIF_I = "Instrument Serif"           # italic face selected with \i1
ROUNDED = "Nunito ExtraLight Black"    # family name as stored in Nunito-Black.ttf
PIXEL = "DotGothic16"
SANS = "Inter Medium"

HEAD = f"""[Script Info]
ScriptType: v4.00+
PlayResX: 1080
PlayResY: 1920
WrapStyle: 2
ScaledBorderAndShadow: yes

[V4+ Styles]
Format: Name, Fontname, Fontsize, PrimaryColour, SecondaryColour, OutlineColour, BackColour, Bold, Italic, Underline, StrikeOut, ScaleX, ScaleY, Spacing, Angle, BorderStyle, Outline, Shadow, Alignment, MarginL, MarginR, MarginV, Encoding
Style: Word,{SERIF_I},250,{CREAM},{CREAM},&H00000000,&H78000000,0,1,0,0,100,100,0,0,1,0,3,5,40,40,0,1
Style: Chapter,{SERIF_I},210,{CREAM},{CREAM},&H00000000,&H78000000,0,1,0,0,100,100,0,0,1,0,3,5,40,40,0,1
Style: Small,{SANS},68,{WHITE},{WHITE},&H00000000,&H50000000,0,0,0,0,100,100,0,0,1,0,3,5,40,40,0,1
Style: TSmall,{SANS},66,{WHITE},{WHITE},&H00000000,&HA0000000,0,0,0,0,100,100,0,0,1,0,2,5,40,40,0,1
Style: TBig,{ROUNDED},160,{PINK},{PINK},&H00000000,&HA0000000,0,0,0,0,100,100,-4,0,1,0,3,5,40,40,0,1
Style: TSub,{SANS},50,{WHITE},{WHITE},&H00000000,&HA0000000,0,0,0,0,100,100,0,0,1,0,2,5,40,40,0,1

[Events]
Format: Layer, Start, End, Style, Name, MarginL, MarginR, MarginV, Effect, Text
"""


# Copy the source's colour signalling so players show the same colours (sources are bt709 SDR).
COLOR_TAGS = ["-colorspace", "bt709", "-color_primaries", "bt709", "-color_trc", "bt709",
              "-color_range", "tv"]


def ts(s: float) -> str:
    s = max(0.0, s)
    h, s = divmod(s, 3600)
    m, s = divmod(s, 60)
    return f"{int(h)}:{int(m):02d}:{s:05.2f}"


def ev(start, end, style, text, layer=1):
    return f"Dialogue: {layer},{ts(start)},{ts(end)},{style},,0,0,0,,{text}"


def clean(word: str) -> str:
    return re.sub(r"[.,!?;:\"]", "", word).lower()


_font_cache = {}


def fit_size(text, base=250, max_w=940, font="InstrumentSerif-Italic.ttf"):
    """Shrink the font size so one long word never runs off a 1080-wide frame."""
    from PIL import ImageFont
    if font not in _font_cache:
        _font_cache[font] = ImageFont.truetype(str(FONTS / font), 100)
    w = _font_cache[font].getlength(text) * base / 100
    return base if w <= max_w else int(base * max_w / w)


def caption_events(words, fixes, chapters, dur, y=1180):
    out = []
    for i, w in enumerate(words):
        txt = clean(fixes.get(clean(w["text"]), w["text"]))
        if not txt:
            continue
        nxt = words[i + 1]["start"] if i + 1 < len(words) else None
        end = nxt if nxt is not None and nxt - w["end"] < 0.35 else w["end"] + 0.25
        end = min(end, dur)
        in_chapter = next((c for c in chapters if c[1] <= w["start"] < c[2]), None)
        if in_chapter:
            cy = in_chapter[3]
            out.append(ev(w["start"], end, "Small", f"{{\\an5\\pos(540,{cy + 150})}}{txt}"))
        else:
            fs = fit_size(txt)
            size = f"\\fs{fs}" if fs != 250 else ""
            out.append(ev(w["start"], end, "Word", f"{{\\an5\\pos(540,{y}){size}}}{txt}"))
    return out


def chapter_events(chapters):
    return [ev(s, e, "Chapter", f"{{\\an5\\pos(540,{y})\\fad(120,150)}}{label}", layer=2)
            for label, s, e, y in chapters]


TITLE_LINE_STEP = 105  # px between big lines: tight, lines sit right under each other (user)


def title_events(spec: str, t0: float, dur: float, y=1185, step=TITLE_LINE_STEP):
    parts = spec.split("|")
    small, big = parts[0], parts[1]
    sub = parts[2] if len(parts) > 2 else ""
    lines = big.split("/")
    n = len(lines)
    # one event per big line, so the spacing is ours and not the font's tall line height
    ys = [round(y + (k - (n - 1) / 2) * step) for k in range(n)]
    out = []
    end = t0 + dur
    per_char = 0.025  # fast: the hook must land within ~0.5s (user)
    y_small = ys[0] - step // 2 - 60
    y_sub = ys[-1] + step // 2 + 45

    def big_events(a, b, extra="", layer=3):
        return [ev(a, b, "TBig", f"{{\\an5\\pos(540,{yy}){extra}}}{txt}", layer=layer)
                for txt, yy in zip(lines, ys)]

    # 1. typewriter with cursor
    for i in range(1, len(small) + 1):
        a = t0 + (i - 1) * per_char
        b = t0 + i * per_char
        out.append(ev(a, b, "TSmall", f"{{\\an5\\pos(540,{y_small})}}{small[:i]}|", layer=3))
    typed = t0 + len(small) * per_char
    big_at = typed + 0.04
    out.append(ev(typed, big_at, "TSmall", f"{{\\an5\\pos(540,{y_small})}}{small}|", layer=3))
    out.append(ev(big_at, end, "TSmall", f"{{\\an5\\pos(540,{y_small})\\fad(0,150)}}{small}", layer=3))
    # 2. big lines with pixel glitch frames
    pix = f"\\fn{PIXEL}\\fsp6"
    glitch = [(0.00, 0.05, False), (0.05, 0.11, True), (0.11, 0.16, False), (0.16, 0.22, True)]
    for a, b, g in glitch:
        out += big_events(big_at + a, big_at + b, pix if g else "")
    out += big_events(big_at + 0.22, end, "\\fad(0,150)")
    out += big_events(end - 0.22, end - 0.12, pix, layer=4)  # glitch out
    # 3. subtitle
    if sub:
        out.append(ev(big_at + 0.22, end, "TSub", f"{{\\an5\\pos(540,{y_sub})\\fad(120,150)}}{sub}", layer=3))
    return out


def probe_duration(path) -> float:
    return float(subprocess.check_output(["ffprobe", "-v", "error", "-show_entries", "format=duration",
                                          "-of", "csv=p=0", str(path)]).decode())


def cmd_render(a):
    dur = probe_duration(a.video)
    fixes = {}
    for f in a.fix:
        k, v = f.split("=", 1)
        fixes[k.strip().lower()] = v.strip()
    chapters = []
    for c in a.chapter:
        label, rng = c.rsplit("@", 1)
        s, e = (float(x) for x in rng.split("-"))
        chapters.append((label, s, e, a.chapter_y))
    events = []
    if a.title:
        events += title_events(a.title, a.title_at, a.title_dur)
    events += chapter_events(chapters)
    if a.transcript:
        words = [w for w in json.load(open(a.transcript))["words"] if w["type"] == "word"]
        if a.title:  # no captions while the title card is up
            t_end = a.title_at + a.title_dur
            words = [w for w in words if not (a.title_at <= w["start"] < t_end)]
        events += caption_events(words, fixes, chapters, dur, a.caption_y)

    out = Path(a.output)
    ass = out.with_suffix(".ass")
    ass.write_text(HEAD + "\n".join(events) + "\n")
    cmd = ["ffmpeg", "-hide_banner", "-loglevel", "verbose" if a.debug else "error", "-y", "-i", a.video]
    if a.silent:
        cmd += ["-f", "lavfi", "-i", "anullsrc=r=48000:cl=stereo"]
    cmd += ["-vf", f"ass={ass}:fontsdir={FONTS}", "-c:v", "libx264", "-preset", "medium", "-crf", str(a.crf),
            "-pix_fmt", "yuv420p", *COLOR_TAGS]
    if a.silent:
        cmd += ["-map", "0:v", "-map", "1:a", "-shortest", "-c:a", "aac", "-b:a", "128k"]
    else:
        if not a.no_loudnorm:
            cmd += ["-af", "loudnorm=I=-14:TP=-1:LRA=11"]
        cmd += ["-c:a", "aac", "-b:a", "192k", "-ar", "48000"]
    cmd += ["-movflags", "+faststart", str(out)]
    r = subprocess.run(cmd, capture_output=True, text=True)
    if r.returncode != 0:
        raise SystemExit(r.stderr[-2000:])
    if a.debug:
        for line in sorted(set(l for l in r.stderr.splitlines() if "fontselect" in l)):
            print(line.split("] ", 1)[-1])
    print(f"{len(events)} events -> {out}  ({ass})")


def main():
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    sub = ap.add_subparsers(dest="cmd", required=True)
    r = sub.add_parser("render")
    r.add_argument("video")
    r.add_argument("-o", "--output", required=True)
    r.add_argument("--transcript")
    r.add_argument("--fix", action="append", default=[])
    r.add_argument("--title")
    r.add_argument("--title-at", type=float, default=0.0)
    r.add_argument("--title-dur", type=float, default=3.0)
    r.add_argument("--chapter", action="append", default=[], help='"label@start-end"')
    r.add_argument("--caption-y", type=int, default=1180)
    r.add_argument("--chapter-y", type=int, default=1120)
    r.add_argument("--silent", action="store_true", help="replace audio with silence")
    r.add_argument("--no-loudnorm", action="store_true")
    r.add_argument("--debug", action="store_true", help="print which fonts libass picked")
    r.add_argument("--crf", type=int, default=17, help="x264 quality; 19-20 for 60fps exports to keep files small")
    a = ap.parse_args()
    cmd_render(a)


if __name__ == "__main__":
    main()
