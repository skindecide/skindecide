"""Burn captions in the house style (see video/references/stijl/notes.md).

- One word at a time, white serif (Liberation Serif ~ Times), lowercase, no punctuation,
  chest height, soft shadow, no box  (ref1 style)
- Optional subtle product tag line under it for the whole video  (ref2 style)
- Loudness normalised to -14 LUFS / -1 dBTP

Usage:
  python tools/style_captions.py <video> <transcript.json> -o out.mp4 \
      [--tag "Brand Product >>>"] [--fix "fout=goed" ...] [--y 1180] [--size 165]

--fix replaces a transcribed word (case-insensitive, punctuation ignored) before rendering.
Use it for Whisper mistakes: --fix "groothijd=roodheid" --fix "mondje=wondje".
"""
import argparse, json, re, subprocess, sys
from pathlib import Path

ap = argparse.ArgumentParser()
ap.add_argument("video"); ap.add_argument("transcript")
ap.add_argument("-o", "--output", required=True)
ap.add_argument("--tag", default=None)
ap.add_argument("--fix", action="append", default=[])
ap.add_argument("--y", type=int, default=1180, help="caption centre, in 1920-high frame")
ap.add_argument("--size", type=int, default=165)
a = ap.parse_args()

fixes = {}
for f in a.fix:
    k, v = f.split("=", 1)
    fixes[k.strip().lower()] = v.strip()

words = [w for w in json.load(open(a.transcript))["words"] if w["type"] == "word"]
dur = float(subprocess.check_output(["ffprobe", "-v", "error", "-show_entries", "format=duration",
                                     "-of", "csv=p=0", a.video]).decode())

def t(s):
    h, s = divmod(max(s, 0), 3600); m, s = divmod(s, 60)
    return f"{int(h)}:{int(m):02d}:{s:05.2f}"

def clean(txt):
    return re.sub(r"[.,!?;:\"]", "", txt).lower()

head = f"""[Script Info]
ScriptType: v4.00+
PlayResX: 1080
PlayResY: 1920
WrapStyle: 2

[V4+ Styles]
Format: Name, Fontname, Fontsize, PrimaryColour, SecondaryColour, OutlineColour, BackColour, Bold, Italic, Underline, StrikeOut, ScaleX, ScaleY, Spacing, Angle, BorderStyle, Outline, Shadow, Alignment, MarginL, MarginR, MarginV, Encoding
Style: Word,Liberation Serif,{a.size},&H00FFFFFF,&H00FFFFFF,&H00000000,&H60000000,0,0,0,0,100,100,0,0,1,0,4,5,40,40,0,1
Style: Tag,Liberation Sans,40,&H1AFFFFFF,&H00FFFFFF,&H00000000,&H80000000,0,0,0,0,100,100,0,0,1,0,2,5,40,40,0,1

[Events]
Format: Layer, Start, End, Style, Name, MarginL, MarginR, MarginV, Effect, Text
"""
ev = []
for i, w in enumerate(words):
    txt = clean(w["text"])
    txt = clean(fixes.get(txt, txt))
    if not txt:
        continue
    nxt = words[i + 1]["start"] if i + 1 < len(words) else None
    end = nxt if nxt is not None and nxt - w["end"] < 0.35 else w["end"] + 0.25
    ev.append(f"Dialogue: 1,{t(w['start'])},{t(min(end, dur))},Word,,0,0,0,,"
              f"{{\\pos(540,{a.y})\\fad(40,0)}}{txt}")
if a.tag:
    ev.append(f"Dialogue: 0,{t(0)},{t(dur)},Tag,,0,0,0,,{{\\pos(540,{a.y + 140})}}{a.tag}")

out = Path(a.output)
ass = out.with_suffix(".ass")
ass.write_text(head + "\n".join(ev) + "\n")
subprocess.run(["ffmpeg", "-hide_banner", "-loglevel", "error", "-y", "-i", a.video,
                "-vf", f"ass={ass}", "-c:v", "libx264", "-preset", "medium", "-crf", "18",
                "-pix_fmt", "yuv420p", "-af", "loudnorm=I=-14:TP=-1:LRA=11",
                "-c:a", "aac", "-b:a", "192k", "-ar", "48000", "-movflags", "+faststart",
                str(out)], check=True)
print(f"{len(ev)} cues -> {out}  (captions: {ass})")
