"""Transcribe videos locally with faster-whisper (no API key, no upload).

Local alternative to transcribe.py / transcribe_batch.py (ElevenLabs Scribe).
Writes the SAME JSON shape Scribe returns, so pack_transcripts.py,
timeline_view.py and render.py work unchanged:

    {"language_code": "en", "text": "...", "source": "faster-whisper",
     "words": [{"text": "Hello", "start": 0.12, "end": 0.40,
                "type": "word", "speaker_id": "speaker_0"},
               {"text": " ", "start": 0.40, "end": 0.55, "type": "spacing",
                "speaker_id": "speaker_0"}, ...]}

Differences vs Scribe (know these when editing):
  - No speaker diarization: every word is speaker_0.
  - No audio-event tags such as (laughter).
  - Whisper tends to drop fillers ("um", "uh"). A filler-heavy initial prompt
    is passed to coax verbatim output, but check takes_packed.md by ear-logic.
  - Word timestamps can drift ~50-150ms: keep cut padding in the 30-200ms window.

Cached per source, same paths as transcribe.py (<edit>/transcripts/<stem>.json).

Usage:
    python helpers/transcribe_local.py <video_or_dir>
    python helpers/transcribe_local.py <video_or_dir> --model small --language nl
    python helpers/transcribe_local.py <video_or_dir> --edit-dir /custom/edit --audio-track 1
    python helpers/transcribe_local.py <video_or_dir> --vocab "SkinDecide, BabyDecide"

Models: tiny, base, small (default), medium, large-v3, distil-large-v3.
Bigger = more accurate, slower. On CPU, `small` is a good default; use
`medium`/`large-v3` for final cuts on hard audio or non-English speech.
"""

from __future__ import annotations

import argparse
import json
import sys
import tempfile
import time
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
from transcribe import count_audio_tracks, extract_audio, peak_dbfs, transcript_path  # noqa: E402

VIDEO_EXTS = {".mp4", ".mov", ".mkv", ".avi", ".m4v", ".webm", ".mts",
              ".wav", ".mp3", ".m4a", ".aac", ".flac"}

FILLER_PROMPT = "Umm, let me think like, hmm... Okay, uh, so, you know, I mean, er, yeah."

_model_cache: dict[tuple, object] = {}


def get_model(name: str, device: str, compute_type: str):
    key = (name, device, compute_type)
    if key not in _model_cache:
        from faster_whisper import WhisperModel
        _model_cache[key] = WhisperModel(name, device=device, compute_type=compute_type)
    return _model_cache[key]


def to_scribe_shape(segments, language: str) -> dict:
    words: list[dict] = []
    prev_end: float | None = None
    for seg in segments:
        for w in seg.words or []:
            text = w.word.strip()
            if not text:
                continue
            start, end = round(float(w.start), 3), round(float(w.end), 3)
            if prev_end is not None and start > prev_end:
                words.append({"text": " ", "start": prev_end, "end": start,
                              "type": "spacing", "speaker_id": "speaker_0"})
            words.append({"text": text, "start": start, "end": max(end, start),
                          "type": "word", "speaker_id": "speaker_0",
                          "probability": round(float(w.probability), 3)})
            prev_end = max(end, start)
    full = " ".join(w["text"] for w in words if w["type"] == "word")
    return {"language_code": language, "text": full, "words": words,
            "source": "faster-whisper"}


def transcribe_one_local(video: Path, edit_dir: Path, model_name: str, language: str | None,
                         audio_track: int, device: str, compute_type: str,
                         verbatim: bool = True, vocab: str | None = None) -> Path:
    out_path = transcript_path(edit_dir, video, audio_track)
    out_path.parent.mkdir(parents=True, exist_ok=True)
    if out_path.exists():
        print(f"cached: {out_path.name}")
        return out_path

    n_tracks = count_audio_tracks(video)
    if n_tracks == 0:
        raise RuntimeError(f"{video.name} has no audio track")
    if n_tracks > 1:
        print(f"  note: {video.name} has {n_tracks} audio tracks, using track "
              f"{audio_track + 1} (--audio-track to change)", flush=True)

    t0 = time.time()
    with tempfile.TemporaryDirectory() as tmp:
        audio = Path(tmp) / f"{video.stem}.wav"
        extract_audio(video, audio, audio_track)
        peak = peak_dbfs(audio)
        if peak < -60.0:
            raise RuntimeError(f"track {audio_track + 1} of {video.name} is silent "
                               f"(peak {peak:.1f} dBFS)")
        print(f"  transcribing {video.name} with faster-whisper/{model_name}", flush=True)
        model = get_model(model_name, device, compute_type)
        segments, info = model.transcribe(
            str(audio),
            language=language,
            word_timestamps=True,
            vad_filter=False,              # keep true gap timing for cut decisions
            condition_on_previous_text=False,  # fewer hallucinated repeats
            initial_prompt=" ".join(x for x in [vocab, FILLER_PROMPT if verbatim else None] if x) or None,
            beam_size=5,
        )
        payload = to_scribe_shape(list(segments), info.language)

    out_path.write_text(json.dumps(payload, indent=2, ensure_ascii=False))
    n = sum(1 for w in payload["words"] if w["type"] == "word")
    print(f"  saved: {out_path} ({n} words, lang={info.language}) in {time.time() - t0:.1f}s")
    return out_path


def main() -> None:
    ap = argparse.ArgumentParser(description="Local word-level transcription with faster-whisper")
    ap.add_argument("path", type=Path, help="Video/audio file, or a directory of them")
    ap.add_argument("--edit-dir", type=Path, default=None,
                    help="Edit output dir (default: <videos_dir>/edit)")
    ap.add_argument("--model", default="small", help="Whisper model (default: small)")
    ap.add_argument("--language", default=None, help="ISO code, e.g. en, nl, tr. Omit to auto-detect.")
    ap.add_argument("--audio-track", type=int, default=0, help="Zero-based audio track")
    ap.add_argument("--device", default="auto", help="cpu, cuda, or auto")
    ap.add_argument("--compute-type", default="int8",
                    help="int8 (CPU default), float16 (GPU), int8_float16 ...")
    ap.add_argument("--no-verbatim", action="store_true",
                    help="Don't prompt Whisper to keep filler words")
    ap.add_argument("--vocab", default=None,
                    help='Names/terms to spell right, e.g. "SkinDecide, HairDecide, niacinamide"')
    args = ap.parse_args()

    target = args.path.resolve()
    if not target.exists():
        sys.exit(f"not found: {target}")
    if target.is_dir():
        files = sorted(p for p in target.iterdir() if p.is_file() and p.suffix.lower() in VIDEO_EXTS)
        videos_dir = target
    else:
        files, videos_dir = [target], target.parent
    if not files:
        sys.exit(f"no media files in {target}")

    edit_dir = (args.edit_dir or (videos_dir / "edit")).resolve()
    failed = []
    for f in files:
        try:
            transcribe_one_local(f, edit_dir, args.model, args.language, args.audio_track,
                                 args.device, args.compute_type, not args.no_verbatim, args.vocab)
        except Exception as e:  # keep going on batch runs
            print(f"  FAILED {f.name}: {e}", file=sys.stderr)
            failed.append(f.name)
    if failed:
        sys.exit(f"{len(failed)} file(s) failed: {', '.join(failed)}")


if __name__ == "__main__":
    main()
