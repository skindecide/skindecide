"""another day, another blowout (deel 2): ~20s silent cut, picture untouched (only cut + downscale 4K->1080)."""
import json, os, subprocess
SRC = "raw.mp4"
SHOTS = [  # v1
    (14.8, 17.4, "sjaal af als gordijn, pincurls zichtbaar (titel)"),
    (52.4, 54.0, "pin eruit, spiraalkrul hangt"),
    (108.1, 110.0, "pin eruit, krul valt, volle krullen"),
    (118.4, 119.9, "bovenkant: pin eruit, bovenkant valt"),
    (120.5, 122.0, "bovenkant: tweede deel los"),
    (126.0, 127.2, "alle krullen (glorie-shot)"),
    (157.5, 159.0, "losschudden, volume"),
    (166.0, 167.5, "grote volle krullen"),
    (239.0, 240.2, "over schouder kijken"),
    (243.0, 244.8, "achterkant, haar zwiept"),
    (283.0, 284.3, "airwrap voorkantje"),
    (304.0, 305.3, "airwrap, blik in camera"),
    (380.0, 382.8, "eindresultaat voorkant"),
]
COLOR = ["-colorspace", "bt709", "-color_primaries", "bt709", "-color_trc", "bt709", "-color_range", "tv"]
os.makedirs("edit/clips", exist_ok=True)
lines = []
for i, (s, e, _) in enumerate(SHOTS):
    out = f"edit/clips/shot{i:02d}.mp4"
    subprocess.run(["ffmpeg", "-hide_banner", "-loglevel", "error", "-y", "-ss", str(s), "-i", SRC,
                    "-t", f"{e - s:.3f}", "-map", "0:v:0", "-an", "-vf", "scale=1080:1920:flags=lanczos",
                    "-r", "30", "-c:v", "libx264", "-preset", "medium", "-crf", "14", "-pix_fmt", "yuv420p",
                    *COLOR, out], check=True)
    lines.append(f"file '{os.path.abspath(out)}'")
open("edit/clips/list.txt", "w").write("\n".join(lines) + "\n")
subprocess.run(["ffmpeg", "-hide_banner", "-loglevel", "error", "-y", "-f", "concat", "-safe", "0",
                "-i", "edit/clips/list.txt", "-c", "copy", "edit/base.mp4"], check=True)
total = sum(e - s for s, e, _ in SHOTS)
json.dump({"version": 1, "sources": {"raw": SRC}, "output": "1080x1920@30, silent",
           "title": "another day | another blowout",
           "ranges": [{"source": "raw", "start": s, "end": e, "beat": b} for s, e, b in SHOTS],
           "total_duration_s": round(total, 2)}, open("edit/edl.json", "w"), indent=2, ensure_ascii=False)
print(f"{len(SHOTS)} shots, {total:.1f}s")
