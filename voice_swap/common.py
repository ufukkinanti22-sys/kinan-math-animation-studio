"""Shared helpers for the voice-swap pipeline (source narrator -> owner's voice).

Nothing in this package modifies the Manim project, the captions, the scenes or the
rendered pictures: the pipeline only rebuilds the audio track and re-muxes it with the
ORIGINAL video stream (``-c:v copy``).
"""

from __future__ import annotations

import json
import subprocess
from pathlib import Path

import numpy as np
import soundfile as sf

ROOT = Path(__file__).resolve().parents[1]
PROBLEMS = ["p01_dadu_berbeda", "p02_tiga_koin", "p03_kartu_bridge", "p00_poc_binomial"]
SR = 48000  # sample rate of the final audio track (same as the original videos)
PRIVATE = ROOT / "voice_private"  # git-ignored: reference clip, per-beat conversions
OUT = ROOT / "voice_out"  # git-ignored: final videos / WAVs of the swapped voice


def sh(cmd: list[str], **kw) -> subprocess.CompletedProcess:
    return subprocess.run(cmd, check=True, capture_output=True, text=True, **kw)


def probe(path: Path, entries: str, stream: str | None = None) -> str:
    cmd = ["ffprobe", "-v", "error"] + (["-select_streams", stream] if stream else []) + [
        "-show_entries", entries, "-of", "csv=p=0", str(path)]
    return sh(cmd).stdout.strip()


def video_path(pid: str) -> Path:
    return ROOT / "output" / "videos" / f"{pid}.mp4"


def beats_log(pid: str) -> list[dict]:
    """Start/end of every narration beat in the FINAL video (written by the render)."""
    return json.loads((ROOT / "output" / "qc" / pid / "beats.json").read_text())["beats"]


def source_mp3(pid: str, beat_id: str) -> Path:
    """The separate narrator track of one beat (before it was mixed into the video)."""
    return ROOT / "assets" / "audio" / pid / f"{beat_id}.mp3"


def decode(path: Path, sr: int = SR) -> np.ndarray:
    """Any audio/video file -> mono float32 at ``sr`` (ffmpeg, soxr resampling)."""
    raw = subprocess.run(
        ["ffmpeg", "-v", "error", "-i", str(path), "-vn", "-ac", "1", "-ar", str(sr),
         "-af", "aresample=resampler=soxr", "-f", "f32le", "-"],
        check=True, capture_output=True).stdout
    return np.frombuffer(raw, dtype=np.float32).copy()


def write_wav(path: Path, x: np.ndarray, sr: int = SR) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    sf.write(str(path), np.clip(x, -1.0, 1.0), sr, subtype="PCM_16")


def active_rms(x: np.ndarray, sr: int = SR) -> float:
    """RMS over speech-active 20 ms frames (ignores pauses), used to match levels."""
    n = int(0.02 * sr)
    f = x[: len(x) // n * n].reshape(-1, n)
    e = np.sqrt((f ** 2).mean(1))
    if e.size == 0 or e.max() < 1e-6:
        return 1e-6
    return float(np.sqrt((f[e > 0.1 * e.max()] ** 2).mean()))


def envelope(x: np.ndarray, sr: int = SR, hop_ms: int = 10) -> np.ndarray:
    n = int(hop_ms / 1000 * sr)
    f = x[: len(x) // n * n].reshape(-1, n)
    return np.sqrt((f ** 2).mean(1))
