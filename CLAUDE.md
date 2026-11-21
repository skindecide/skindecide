# AI Video Editor

This folder is an AI video editor. You (Claude) edit videos by conversation: the user
drops raw footage in, describes what they want, and you produce the finished video.

The repo also holds unrelated HTML pages at the root (brand kits, itineraries, trainers).
Leave them alone unless asked. Brand kits such as `skindecide-brandkit-v2.html`,
`hairdecide-brandkit.html` and `babydecide-brandkit*.html` are useful **style references**
(colours, fonts) for captions, title cards and animations.

## Start of every session

The cloud container is fresh each time, so check the tools before editing:

```bash
bash setup.sh   # installs anything missing, prints versions; safe to re-run
```

## Toolchain

| Tool | Use it for | Notes |
|---|---|---|
| **ffmpeg / ffprobe** | Cutting, joining, encoding, audio, burning subtitles, probing media | Everything ends up going through ffmpeg |
| **faster-whisper** | Local speech-to-text with word timestamps | No API key needed. Models download from Hugging Face on first use |
| **OpenCV** (`cv2`, 4.x) | Frame analysis: scene and motion detection, face detection/tracking for reframing (e.g. 16:9 → 9:16), picking thumbnails | Pinned `<5` because 5.x removed `CascadeClassifier` |
| **HyperFrames** (`hyperframes` CLI) | Motion graphics built in HTML/CSS/GSAP and rendered to MP4/WebM: title cards, lower thirds, kinetic text, animated overlays | `hyperframes init <dir> --example blank --non-interactive --skip-skills`, then `hyperframes render <dir> -o out.mp4` |
| **video-use skill** | The editing workflow (`.claude/skills/video-use/`) | **Read its `SKILL.md` before any editing task** |

## How to edit: use the video-use skill

For any editing request, load the `video-use` skill and follow its process:
inventory → ask → **confirm the plan with the user** → execute → self-check → iterate.
Its helpers live in `.claude/skills/video-use/helpers/`:

- `transcribe_local.py <dir>` transcribes with faster-whisper. **Use this by default**, not
  `transcribe.py` or `transcribe_batch.py`, which need a paid ElevenLabs key. Options:
  `--model small` (default) / `medium` / `large-v3` for harder audio; `--language nl|en|tr`;
  `--vocab "SkinDecide, HairDecide, BabyDecide"` so brand names are spelled right (always
  pass this for brand content).
- `pack_transcripts.py --edit-dir <dir>/edit` builds `takes_packed.md`, the main
  transcript to read.
- `timeline_view.py <video> <start> <end>` makes a filmstrip and waveform PNG for checking cut points.
- `render.py <edl.json> -o <out> [--draft|--preview] [--build-subtitles]` does the cuts,
  grade, overlays and subtitles.
- `grade.py` applies colour grade presets (`--list-presets`).

House caption style (from `video/references/stijl/`): `tools/style_captions.py <video>
<transcript.json> -o out.mp4 --tag "Product >>>" --fix "fout=goed"`. It burns one-word
serif captions and an optional product tag, and normalises loudness to -14 LUFS.
Use it for videos that are already cut and only need finishing.

Local transcription has limits: it can't tell speakers apart, it doesn't tag laughter or
other sounds, and Whisper sometimes drops "um"/"uh". Check the transcript and use
`timeline_view` at the cuts that matter.

## Folders

```
video/
├── footage/<project>/   ← raw clips go here, one folder per project (never modify)
│   └── edit/            ← all working files for that project (skill's convention)
│       ├── takes_packed.md, edl.json, master.srt, project.md
│       └── final.mp4
├── references/<theme>/  ← reference videos, screenshots and notes.md on what to copy from them
└── exports/             ← finished videos the user wants to keep
```

Video files and working files are **git-ignored** because they are too large. Only
`project.md` (the edit log) and `edl.json` (the edit decisions) are small enough to commit,
and committing them lets an edit be re-rendered later. Tell the user when finished videos
live only in this container: it gets wiped, so they need to download them.

## House rules

- **Check `video/references/` first.** Before proposing a plan, read the relevant `notes.md`
  and look at the references (use `timeline_view` or sample frames for videos), and match
  their pacing, caption style and look unless the user says otherwise.
- **Plan before cutting.** Describe the plan in plain language and wait for the user to agree
  (skill rule 11).
- **Check your own output before showing it.** Run `ffprobe` on the duration, look at frames at
  each cut with `timeline_view`, and measure loudness with `ffmpeg -af ebur128`. You can't hear
  the audio, so report the numbers instead of saying it sounds good.
- **Formats:** ask which platform the video is for. Defaults: Reels/TikTok/Shorts are
  1080×1920 @30; YouTube is 1920×1080; feed posts are 1080×1080 or 1080×1350.
- **Brand graphics:** take colours and fonts from the brand-kit HTML for the brand in
  question. Check that web fonts actually loaded before rendering, because a failed font
  silently falls back to another one.
- Many of the user's projects are in **Dutch or Turkish**. Pass `--language` when you know it;
  auto-detect can misfire on short clips.
- Use `--draft` renders while iterating and switch to full quality for the final render.
- Don't re-transcribe a source that already has a transcript in `edit/transcripts/`.

## Network note (cloud sessions)

faster-whisper downloads models from Hugging Face. This repo's cloud environment
("skindecide") allows those hosts. If a model download fails with a proxy 403, the session
is probably running on a different environment.
