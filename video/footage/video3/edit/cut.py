"""v1: pincurl reveal na 12 uur, ~25s, silent (music added in-app), title text."""
import json, subprocess
SRC = "raw.mp4"
SHOTS = [  # (start, end, beat)  — v3
    (0.0, 1.6, "hook: handen gevouwen, sjaal nog om"),
    (29.2, 31.6, "sjaal af als gordijn, pins zichtbaar (netter dan v2)"),
    (108.7, 109.8, "pins eruit, krullen vallen"),
    (150.2, 151.2, "krullen"),
    (199.7, 200.7, "laatste pin eruit"),
    (207.0, 208.3, "alle krullen los (piek)"),
    (225.5, 227.0, "losschudden"),
    (265.0, 266.5, "uitborstelen"),
    (271.0, 273.0, "uitborstelen"),
    (280.0, 281.5, "krullen uitgezakt"),
    (405.0, 407.5, "redden: haarzwiep"),
    (509.8, 512.6, "eindresultaat + duim omlaag (korter dan v2)"),
]
TITLE = "pincurl reveal na 12 uur"
TITLE_END = 4.0  # alleen tijdens hook + sjaal af (gebruiker: niet de hele tijd)
total = sum(e - s for s, e, _ in SHOTS)
ass = f"""[Script Info]
ScriptType: v4.00+
PlayResX: 1080
PlayResY: 1920

[V4+ Styles]
Format: Name, Fontname, Fontsize, PrimaryColour, SecondaryColour, OutlineColour, BackColour, Bold, Italic, Underline, StrikeOut, ScaleX, ScaleY, Spacing, Angle, BorderStyle, Outline, Shadow, Alignment, MarginL, MarginR, MarginV, Encoding
Style: Title,DM Serif Display,104,&H00FFFFFF,&H00FFFFFF,&H00000000,&H60000000,0,0,0,0,100,100,0,0,1,0,4,5,60,60,0,1

[Events]
Format: Layer, Start, End, Style, Name, MarginL, MarginR, MarginV, Effect, Text
Dialogue: 0,0:00:00.00,0:00:{TITLE_END:05.2f},Title,,0,0,0,,{{\\an2\\pos(540,1160)\\fad(0,300)}}pincurl reveal
Dialogue: 0,0:00:00.00,0:00:{TITLE_END:05.2f},Title,,0,0,0,,{{\\an5\\pos(540,1220)\\fad(0,300)\\fnMrs Saint Delafield\\fs280}}na {{\\fs190}}12{{\\fs280}} uur
"""
open("edit/title.ass", "w").write(ass)
import os
os.makedirs("edit/clips", exist_ok=True)
listing = []
for i, (s0, e0, _) in enumerate(SHOTS):
    clip = f"edit/clips/shot{i:02d}.mp4"
    subprocess.run(["ffmpeg", "-hide_banner", "-loglevel", "error", "-y", "-ss", str(s0), "-i", SRC,
                    "-t", f"{e0 - s0:.3f}", "-an", "-vf", "fps=30", "-c:v", "libx264", "-preset", "fast",
                    "-crf", "12", "-pix_fmt", "yuv420p", clip], check=True)
    listing.append(f"file '{os.path.abspath(clip)}'")
open("edit/clips/list.txt", "w").write("\n".join(listing) + "\n")
subprocess.run(["ffmpeg", "-hide_banner", "-loglevel", "error", "-y", "-f", "concat", "-safe", "0",
                "-i", "edit/clips/list.txt", "-f", "lavfi", "-i", "anullsrc=r=48000:cl=stereo",
                "-vf", "ass=edit/title.ass:fontsdir=/home/user/skindecide/tools/fonts", "-map", "0:v", "-map", "1:a", "-shortest",
                "-c:v", "libx264", "-preset", "slow", "-crf", "17", "-pix_fmt", "yuv420p",
                "-c:a", "aac", "-b:a", "128k", "-movflags", "+faststart", "edit/final_v8.mp4"], check=True)
json.dump({"version": 1, "sources": {"raw": SRC}, "audio": "silent (muziek toevoegen in app)",
           "title": TITLE,
           "ranges": [{"source": "raw", "start": s, "end": e, "beat": b} for s, e, b in SHOTS],
           "total_duration_s": round(total, 2)}, open("edit/edl.json", "w"), indent=2, ensure_ascii=False)
print(f"{len(SHOTS)} shots, {total:.1f}s")
