#!/usr/bin/env bash
# Installs the AI video editor toolchain. Idempotent; safe to re-run.
set -euo pipefail
cd "$(dirname "$0")"
command -v ffmpeg >/dev/null || { apt-get update -qq && apt-get install -y -qq ffmpeg; }
pip install -q -r requirements.txt
command -v hyperframes >/dev/null || npm install -g -q hyperframes
echo "ffmpeg: $(ffmpeg -version | head -1 | cut -d' ' -f3)"
python3 -c "import faster_whisper, cv2; print('faster-whisper', faster_whisper.__version__, '| opencv', cv2.__version__)"
echo "hyperframes: $(hyperframes --version)"
