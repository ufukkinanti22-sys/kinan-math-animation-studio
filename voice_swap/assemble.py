#!/usr/bin/env python3
"""Rebuild the narration track and mux it into the ORIGINAL final video.

    python -m voice_swap.assemble self-test p01_dadu_berbeda       # no model needed
    python -m voice_swap.assemble build p01_dadu_berbeda --beats voice_private/converted/p01_dadu_berbeda

What it guarantees
* every beat starts at exactly the same time as in the original video (times come from
  ``output/qc/<id>/beats.json``, written by the render that produced the video);
* each converted beat is fitted to the length of the original beat (pause/tempo kept) and
  its speech level matched to the original beat;
* the same loudness normalisation as the original render (loudnorm I=-16 TP=-1.5 LRA=11);
* the picture is copied with ``-c:v copy`` and proven identical (frame-by-frame MD5).
"""

from __future__ import annotations

import argparse
import json
import sys
from pathlib import Path

import numpy as np

from .common import (OUT, PROBLEMS, ROOT, SR, active_rms, beats_log, decode, envelope, probe, sh,
                     source_mp3, video_path, write_wav)

MAX_LEN_DIFF = 0.60  # s: larger length mismatch between a converted beat and its source is an error
LOUDNORM = "loudnorm=I=-16:TP=-1.5:LRA=11"
# The original videos were encoded to AAC twice, which shifted their audio 1024 samples
# (21.3 ms) later than the beat schedule. Reproduce it so the new audio sits where the old did.
AAC_DELAY = 1024


def fit_length(x: np.ndarray, n: int) -> np.ndarray:
    """Pad with silence / trim the end so the beat has exactly ``n`` samples."""
    if len(x) >= n:
        y = x[:n].copy()
        k = min(len(y), int(0.01 * SR))  # 10 ms fade-out so a trim never clicks
        y[-k:] *= np.linspace(1, 0, k, dtype=np.float32)
        return y
    return np.concatenate([x, np.zeros(n - len(x), dtype=np.float32)])


def build_track(pid: str, beat_dir: Path | None, total_s: float) -> tuple[np.ndarray, list[dict]]:
    """Mix one narration track. ``beat_dir=None`` rebuilds the ORIGINAL narrator (self-test)."""
    track = np.zeros(int(round(total_s * SR)), dtype=np.float32)
    report = []
    for b in beats_log(pid):
        src = decode(source_mp3(pid, b["id"]))
        if beat_dir is None:
            x = src
        else:
            wav = beat_dir / f"{b['id']}.wav"
            if not wav.exists():
                raise FileNotFoundError(f"missing converted beat: {wav}")
            x = decode(wav)
            diff = (len(x) - len(src)) / SR
            if abs(diff) > MAX_LEN_DIFF:
                raise ValueError(f"{pid}/{b['id']}: converted beat differs {diff:+.2f}s from the source")
            x = fit_length(x, len(src))
            g = active_rms(src) / active_rms(x)  # match speech level to the original beat
            x = np.clip(x * min(max(g, 0.25), 4.0), -1.0, 1.0)
            report.append({"id": b["id"], "len_diff_s": round(diff, 3), "gain": round(float(g), 3)})
        s = int(round(b["start"] * SR)) + AAC_DELAY
        e = min(s + len(x), len(track))
        track[s:e] += x[: e - s]
    return track, report


def loudnorm_wav(inp: Path, out: Path) -> None:
    sh(["ffmpeg", "-y", "-v", "error", "-i", str(inp), "-af", LOUDNORM, "-ar", str(SR), "-ac", "1",
        "-c:a", "pcm_s16le", str(out)])


def mux(video: Path, wav: Path, out: Path) -> None:
    """Original picture untouched (stream copy) + new audio."""
    out.parent.mkdir(parents=True, exist_ok=True)
    sh(["ffmpeg", "-y", "-v", "error", "-i", str(video), "-i", str(wav), "-map", "0:v:0", "-map", "1:a:0",
        "-c:v", "copy", "-c:a", "aac", "-b:a", "160k", "-ar", str(SR), "-movflags", "+faststart",
        "-shortest", str(out)])


def framemd5(path: Path) -> str:
    """MD5 of every packet of the video stream (equal => pictures byte-identical)."""
    r = sh(["ffmpeg", "-v", "error", "-i", str(path), "-map", "0:v:0", "-c", "copy", "-f", "md5", "-"])
    return r.stdout.strip()


def decoded_md5(path: Path) -> str:
    """MD5 of every decoded frame (stronger: what the viewer actually sees)."""
    r = sh(["ffmpeg", "-v", "error", "-i", str(path), "-map", "0:v:0", "-f", "md5", "-"])
    return r.stdout.strip()


def lag_and_corr(a: np.ndarray, b: np.ndarray, max_lag_ms: int = 300) -> tuple[float, float]:
    """Envelope cross-correlation: (lag of b relative to a in ms, correlation at that lag)."""
    ea, eb = envelope(a), envelope(b)
    n = min(len(ea), len(eb))
    ea, eb = ea[:n] - ea[:n].mean(), eb[:n] - eb[:n].mean()
    best, best_lag = -2.0, 0
    for lag in range(-max_lag_ms // 10, max_lag_ms // 10 + 1):
        x, y = (ea[lag:], eb[: n - lag]) if lag >= 0 else (ea[: n + lag], eb[-lag:])
        c = float((x * y).sum() / (np.linalg.norm(x) * np.linalg.norm(y) + 1e-12))
        if c > best:
            best, best_lag = c, lag
    return best_lag * 10.0, best


def build_video(pid: str, beat_dir: Path, out_dir: Path = OUT, suffix: str = "_suara_kinan") -> dict:
    video = video_path(pid)
    total = float(probe(video, "stream=duration", "v:0"))
    track, beat_report = build_track(pid, beat_dir, total)
    raw = out_dir / "tmp" / f"{pid}_raw.wav"
    write_wav(raw, track)
    final_wav = out_dir / "audio" / f"{pid}{suffix}.wav"
    final_wav.parent.mkdir(parents=True, exist_ok=True)
    loudnorm_wav(raw, final_wav)
    out_mp4 = out_dir / "videos" / f"{pid}{suffix}.mp4"
    mux(video, final_wav, out_mp4)
    raw.unlink()
    same_packets = framemd5(video) == framemd5(out_mp4)
    same_frames = decoded_md5(video) == decoded_md5(out_mp4)
    return {"problem": pid, "video": str(out_mp4.resolve()),
            "audio_wav": str(final_wav), "video_packets_identical": same_packets,
            "decoded_frames_identical": same_frames,
            "duration_original": round(total, 3), "duration_new": float(probe(out_mp4, "format=duration")),
            "beats": beat_report}


def self_test(pid: str) -> dict:
    """Prove the timeline model WITHOUT any voice conversion: rebuild the audio from the ORIGINAL
    narrator beats and compare with the audio inside the real video."""
    video = video_path(pid)
    total = float(probe(video, "stream=duration", "v:0"))
    rebuilt, _ = build_track(pid, None, total)
    actual = decode(video)
    n = min(len(rebuilt), len(actual))
    lag, corr = lag_and_corr(actual[:n], rebuilt[:n])
    # level: both are normalised to the same loudness target
    ratio_db = 20 * np.log10(active_rms(rebuilt[:n]) / active_rms(actual[:n]) + 1e-9)
    return {"problem": pid, "video_s": round(total, 3), "rebuilt_s": round(len(rebuilt) / SR, 3),
            "envelope_lag_ms": lag, "envelope_corr": round(corr, 4), "pre_loudnorm_level_diff_db": round(float(ratio_db), 2)}


def main() -> None:
    ap = argparse.ArgumentParser()
    sub = ap.add_subparsers(dest="cmd", required=True)
    t = sub.add_parser("self-test")
    t.add_argument("problem", nargs="?", default="all")
    b = sub.add_parser("build")
    b.add_argument("problem")
    b.add_argument("--beats", type=Path, required=True, help="folder with <beat>.wav (converted)")
    a = ap.parse_args()
    ids = PROBLEMS if getattr(a, "problem", "all") == "all" else [a.problem]
    if a.cmd == "self-test":
        for pid in ids:
            print(json.dumps(self_test(pid)))
    else:
        print(json.dumps(build_video(a.problem, a.beats), indent=1))


if __name__ == "__main__":
    sys.exit(main())
