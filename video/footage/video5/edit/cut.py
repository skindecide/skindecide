"""another day, another blowout (deel 2): ~20s silent cut, picture untouched (only cut + downscale 4K->1080)."""
import json, os, subprocess
SRC = "raw.mp4"
SHOTS = [  # v5 (user: no freeze frames; moving, fast)
    (18.4, 19.4, "sjaal af (nog sneller)"),
    (20.0, 20.3, "rondje: voorkant"),
    (22.1, 22.4, "rondje: zijkant"),
    (23.0, 23.3, "rondje: achterkant"),
    (24.3, 24.6, "rondje: andere zijkant"),
    (108.1, 109.4, "pin eruit, lange lok valt"),
    (118.6, 119.8, "bovenkant: pin eruit, bovenkant valt"),
    (122.6, 124.0, "bovenkant los, krullen vallen naar voren"),
    (126.0, 127.2, "alle krullen (glorie-shot)"),
    (157.5, 159.0, "losschudden, volume"),
    (166.0, 167.5, "grote volle krullen"),
    (245.0, 247.4, "achterkant, mooi in het midden"),
    (283.0, 284.3, "airwrap voorkantje"),
    (304.0, 305.3, "airwrap, blik in camera"),
    (393.5, 395.7, "eindresultaat: haar zit, lachen in camera (korter)"),
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
