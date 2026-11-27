"""another day, another blowout: ~20s silent cut, picture untouched (only cut + downscale 4K->1080)."""
import json, os, subprocess
SRC = "raw.mp4"
SHOTS = [
    (14.6, 17.0, "sjaal af als gordijn, rollers zichtbaar (titel)"),
    (61.0, 62.2, "pin eruit, krullen"),
    (105.0, 106.2, "krullen met rollers bovenop"),
    (111.0, 112.2, "roller eruit"),
    (140.0, 141.0, "laatste roller eruit"),
    (147.0, 148.0, "haarzwiep voorover"),
    (162.0, 163.2, "losschudden, volume"),
    (188.0, 189.8, "grote volle krullen"),
    (255.0, 256.2, "volume met handen"),
    (400.0, 401.3, "airwrap voorkantjes"),
    (419.0, 420.2, "airwrap"),
    (502.0, 503.5, "achterkant"),
    (523.0, 526.3, "eindresultaat voorkant"),
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
