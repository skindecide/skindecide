"""One-word serif captions (ref1 style) + subtle product tag (ref2 style) as ASS."""
import json, re, sys
src, out = sys.argv[1], sys.argv[2]
words = [w for w in json.load(open(src))["words"] if w["type"] == "word"]
def t(s):
    h, s = divmod(s, 3600); m, s = divmod(s, 60)
    return f"{int(h)}:{int(m):02d}:{s:05.2f}"
head = """[Script Info]
ScriptType: v4.00+
PlayResX: 1080
PlayResY: 1920
WrapStyle: 2

[V4+ Styles]
Format: Name, Fontname, Fontsize, PrimaryColour, SecondaryColour, OutlineColour, BackColour, Bold, Italic, Underline, StrikeOut, ScaleX, ScaleY, Spacing, Angle, BorderStyle, Outline, Shadow, Alignment, MarginL, MarginR, MarginV, Encoding
Style: Word,Liberation Serif,165,&H00FFFFFF,&H00FFFFFF,&H00000000,&H60000000,0,0,0,0,100,100,0,0,1,0,4,5,40,40,0,1
Style: Tag,Liberation Sans,40,&H1AFFFFFF,&H00FFFFFF,&H00000000,&H80000000,0,0,0,0,100,100,0,0,1,0,2,5,40,40,0,1

[Events]
Format: Layer, Start, End, Style, Name, MarginL, MarginR, MarginV, Effect, Text
"""
ev = []
for i, w in enumerate(words):
    txt = re.sub(r"[.,!?;:]", "", w["text"]).lower()
    start = w["start"]
    nxt = words[i + 1]["start"] if i + 1 < len(words) else None
    end = nxt if nxt is not None and nxt - w["end"] < 0.35 else w["end"] + 0.25
    ev.append(f"Dialogue: 1,{t(start)},{t(end)},Word,,0,0,0,,{{\\pos(540,1180)\\fad(40,0)}}{txt}")
dur = float(sys.argv[3])
ev.append(f"Dialogue: 0,{t(0)},{t(dur)},Tag,,0,0,0,,{{\\pos(540,1320)}}Lancôme Absolue Longevity MD >>>")
open(out, "w").write(head + "\n".join(ev) + "\n")
print(f"{len(words)} word cues -> {out}")
