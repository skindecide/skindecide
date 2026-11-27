"""another day, another blowout: ~20s silent cut, picture untouched (only cut + downscale 4K->1080)."""
import json, os, subprocess
SRC = "raw.mp4"
SHOTS = [  # v4
    (14.6, 17.0, "sjaal af als gordijn, rollers zichtbaar (titel)"),
    (36.4, 38.4, "pin eruit, strakke spiraalkrul springt"),
    (46.8, 48.4, "lange gedefinieerde spiraalkrullen"),
    (111.2, 112.6, "bovenkant: roller afgerold, haar valt los"),
    (123.7, 125.0, "alle krullen gelijkmatig (glorie-shot)"),
    (140.8, 142.2, "bovenkant: laatste roller eruit, bovenkant los"),
    (147.0, 148.0, "haarzwiep voorover"),
    (188.0, 189.8, "grote volle krullen"),
    (405.0, 406.3, "airwrap voorkantje"),
    (478.5, 479.8, "airwrap, arm omhoog"),
    (512.6, 513.8, "over schouder kijken"),
    (514.3, 515.9, "achterkant, haar zwiept (knip: omdraaien eruit)"),
    (523.0, 525.8, "eindresultaat voorkant"),
]
COLOR = ["-colorspace", "bt709", "-color_primaries", "bt709", "-color_trc", "bt709", "-color_range", "tv"]
os.makedirs("edit/clips", exist_ok=True)
lines = []
for i, (s, e, _) in enumerate(SHOTS):
    out = f"edit/clips/shot{i:02d}.mp4"
    subprocess.run(["ffmpeg", "-hide_banner", "-loglevel", "error", "-y", "-ss", str(s), "-i", SRC,
                    "-t", f"{e - s:.3f}", "-map", "0:v:0", "-an", "-vf", "scale=1080:1920:flags=lanczos",
                    "-r", "60", "-c:v", "libx264", "-preset", "medium", "-crf", "14", "-pix_fmt", "yuv420p",
                    *COLOR, out], check=True)
    lines.append(f"file '{os.path.abspath(out)}'")
open("edit/clips/list.txt", "w").write("\n".join(lines) + "\n")
subprocess.run(["ffmpeg", "-hide_banner", "-loglevel", "error", "-y", "-f", "concat", "-safe", "0",
                "-i", "edit/clips/list.txt", "-c", "copy", "edit/base.mp4"], check=True)
total = sum(e - s for s, e, _ in SHOTS)
json.dump({"version": 1, "sources": {"raw": SRC}, "output": "1080x1920@60, silent",
           "title": "another day | another blowout",
           "ranges": [{"source": "raw", "start": s, "end": e, "beat": b} for s, e, b in SHOTS],
           "total_duration_s": round(total, 2)}, open("edit/edl.json", "w"), indent=2, ensure_ascii=False)
print(f"{len(SHOTS)} shots, {total:.1f}s")
