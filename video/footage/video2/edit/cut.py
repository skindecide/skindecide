"""Trim Paula's Choice video per approved plan, remap transcript, hold last frame."""
import json, subprocess
SRC = "raw.mp4"
RANGES = [(1.20, 17.42, "opening ingekort; hook start sneller"),
          (20.45, 40.55, "zin 'ik had ze zelf nog niet eerder gezien...' eruit"),
          (41.15, 42.72, "hapering 'om ... dit wondje' ingekort")]
HOLD = 0.5
F = 0.03
parts, labels = [], []
for i, (s, e, _) in enumerate(RANGES):
    d = e - s
    parts.append(f"[0:v]trim={s}:{e},setpts=PTS-STARTPTS[v{i}];"
                 f"[0:a]atrim={s}:{e},asetpts=PTS-STARTPTS,afade=t=in:st=0:d={F},afade=t=out:st={d-F:.3f}:d={F}[a{i}];")
    labels.append(f"[v{i}][a{i}]")
fc = "".join(parts) + "".join(labels) + f"concat=n={len(RANGES)}:v=1:a=1[vc][ac];" \
     f"[vc]tpad=stop_mode=clone:stop_duration={HOLD}[v];[ac]apad=pad_dur={HOLD}[a]"
subprocess.run(["ffmpeg", "-hide_banner", "-loglevel", "error", "-y", "-i", SRC, "-filter_complex", fc,
                "-map", "[v]", "-map", "[a]", "-c:v", "libx264", "-preset", "medium", "-crf", "16",
                "-pix_fmt", "yuv420p", "-c:a", "aac", "-b:a", "256k", "edit/cut.mp4"], check=True)
# remap transcript to output timeline
words = json.load(open("edit/transcripts/raw.json"))["words"]
out, off = [], 0.0
for s, e, _ in RANGES:
    for w in words:
        if w["type"] == "word" and w["start"] >= s - 0.05 and w["start"] < e:
            out.append({**w, "start": round(max(w["start"], s) - s + off, 3),
                        "end": round(min(w["end"], e) - s + off, 3)})
    off += e - s
json.dump({"words": out}, open("edit/cut_transcript.json", "w"), ensure_ascii=False, indent=1)
json.dump({"version": 1, "sources": {"raw": SRC},
           "ranges": [{"source": "raw", "start": s, "end": e, "reason": r} for s, e, r in RANGES],
           "hold_last_frame_s": HOLD, "total_duration_s": round(off + HOLD, 2)},
          open("edit/edl.json", "w"), indent=2, ensure_ascii=False)
print(f"{len(out)} words, expected duration {off + HOLD:.2f}s")
