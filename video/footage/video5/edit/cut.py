"""another day, another blowout (deel 2): ~20s silent cut, picture untouched (only cut + downscale 4K->1080)."""
import json, os, subprocess
SRC = "raw.mp4"
# ("freeze", t, hold): one frame of the source held for `hold` seconds (user's "stops" idea)
SHOTS = [  # v2
    (14.8, 17.4, "sjaal af als gordijn, pincurls zichtbaar (titel)"),
    ("freeze", 25.5, 0.35, "rondje: voorkant"),
    ("freeze", 24.5, 0.35, "rondje: zijkant links"),
    ("freeze", 27.9, 0.35, "rondje: achterkant"),
    ("freeze", 28.8, 0.35, "rondje: zijkant rechts"),
    (52.4, 54.0, "pin eruit, spiraalkrul hangt"),
    (108.1, 110.0, "pin eruit, krul valt, volle krullen"),
    (118.4, 119.9, "bovenkant: pin eruit, bovenkant valt"),
    (120.5, 122.0, "bovenkant: tweede deel los"),
    (126.0, 127.2, "alle krullen (glorie-shot)"),
    (157.5, 159.0, "losschudden, volume"),
    (239.0, 240.2, "over schouder kijken"),
    (243.0, 244.8, "achterkant, haar zwiept"),
    (283.0, 284.3, "airwrap voorkantje"),
    (304.0, 305.3, "airwrap, blik in camera"),
    (380.0, 382.8, "eindresultaat voorkant"),
]
COLOR = ["-colorspace", "bt709", "-color_primaries", "bt709", "-color_trc", "bt709", "-color_range", "tv"]
os.makedirs("edit/clips", exist_ok=True)
lines = []
for i, shot in enumerate(SHOTS):
    out = f"edit/clips/shot{i:02d}.mp4"
    if shot[0] == "freeze":
        _, t, hold, _ = shot
        args = ["-ss", str(t), "-i", SRC, "-map", "0:v:0", "-an", "-vf",
                f"scale=1080:1920:flags=lanczos,trim=end_frame=1,setpts=PTS-STARTPTS,"
                f"tpad=stop_mode=clone:stop_duration={hold}", "-t", f"{hold:.3f}"]
    else:
        s0, e0, _ = shot
        args = ["-ss", str(s0), "-i", SRC, "-t", f"{e0 - s0:.3f}", "-map", "0:v:0", "-an",
                "-vf", "scale=1080:1920:flags=lanczos"]
    subprocess.run(["ffmpeg", "-hide_banner", "-loglevel", "error", "-y", *args,
                    "-r", "30", "-c:v", "libx264", "-preset", "medium", "-crf", "14", "-pix_fmt", "yuv420p",
                    *COLOR, out], check=True)
    lines.append(f"file '{os.path.abspath(out)}'")
open("edit/clips/list.txt", "w").write("\n".join(lines) + "\n")
subprocess.run(["ffmpeg", "-hide_banner", "-loglevel", "error", "-y", "-f", "concat", "-safe", "0",
                "-i", "edit/clips/list.txt", "-c", "copy", "edit/base.mp4"], check=True)
total = sum(x[2] if x[0] == 'freeze' else x[1] - x[0] for x in SHOTS)
json.dump({"version": 1, "sources": {"raw": SRC}, "output": "1080x1920@30, silent",
           "title": "another day | another blowout",
           "ranges": [({"source": "raw", "freeze_at": x[1], "hold": x[2], "beat": x[3]} if x[0] == "freeze" else {"source": "raw", "start": x[0], "end": x[1], "beat": x[2]}) for x in SHOTS],
           "total_duration_s": round(total, 2)}, open("edit/edl.json", "w"), indent=2, ensure_ascii=False)
print(f"{len(SHOTS)} shots, {total:.1f}s")
