#!/usr/bin/env python3
"""Render problem videos to platform-ready MP4.

    python scripts/render.py p01_dadu_berbeda                 # final 1080x1920
    python scripts/render.py p01_dadu_berbeda --quality preview
    python scripts/render.py all --theme dark
    python scripts/render.py p01_dadu_berbeda --force         # replace an existing final video

Pipeline per problem:
1. Manim renders the scene (narration audio is placed per beat when
   ``assets/audio/<id>/timings.json`` matches the script; otherwise timing is
   estimated and the video is silent).
2. FFmpeg re-encodes to H.264 High / yuv420p / 30 fps / AAC 48 kHz with
   loudness normalisation and ``+faststart`` (Reels, TikTok, Shorts, phones).
3. QC: ffprobe checks, contact sheet and per-beat frames in ``output/qc/<id>/``.

Completed final videos are never overwritten unless ``--force`` is given.
"""

from __future__ import annotations

import argparse
import json
import os
import shutil
import subprocess
import sys
import time
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT))

from src.utils.narration import PROBLEMS, load_script  # noqa: E402

QUALITY = {
    "final": {"res": (1080, 1920), "fps": 30, "crf": 18, "dir": ROOT / "output" / "videos"},
    "preview": {"res": (540, 960), "fps": 30, "crf": 23, "dir": ROOT / "output" / "preview"},
}


def problem_ids(arg: str) -> list[str]:
    if arg == "all":
        return sorted(p.name for p in PROBLEMS.iterdir()
                      if (p / "narration.yaml").exists() and load_script(p.name).get("scene_class"))
    return [a.strip() for a in arg.split(",") if a.strip()]


def run(cmd: list[str], env: dict | None = None, timeout: int | None = None):
    print("+", " ".join(cmd), flush=True)
    subprocess.run(cmd, check=True, env=env, timeout=timeout)


def has_audio(path: Path) -> bool:
    out = subprocess.run(["ffprobe", "-v", "error", "-select_streams", "a", "-show_entries",
                          "stream=index", "-of", "csv=p=0", str(path)], capture_output=True, text=True)
    return bool(out.stdout.strip())


def render(pid: str, quality: str, theme: str, audio: bool, force: bool, timeout: int) -> Path:
    q = QUALITY[quality]
    script = load_script(pid)
    suffix = "" if theme == "kinan" else f"__{theme}"
    final = q["dir"] / f"{pid}{suffix}.mp4"
    if quality == "final" and final.exists() and not force:
        print(f"SKIP {pid}: {final.relative_to(ROOT)} already exists (use --force to replace)")
        return final
    q["dir"].mkdir(parents=True, exist_ok=True)
    log_dir = ROOT / "output" / "tmp" / f"{pid}{suffix}"
    env = dict(os.environ, KINAN_THEME=theme, KINAN_AUDIO="1" if audio else "0",
               KINAN_LOG_DIR=str(log_dir), PYTHONPATH=str(ROOT))
    w, h = q["res"]
    raw_name = f"{pid}{suffix}_{quality}"
    started = time.time()
    run([sys.executable, str(ROOT / "scripts" / "manim_entry.py"), "render",
         "-r", f"{w},{h}", "--fps", str(q["fps"]), "--media_dir", str(ROOT / "media"),
         "-o", raw_name, "--disable_caching", "--progress_bar", "none",
         str(ROOT / script["scene_file"]), script["scene_class"]], env=env, timeout=timeout)
    stem = Path(script["scene_file"]).stem
    raw = ROOT / "media" / "videos" / stem / f"{h}p{q['fps']}" / f"{raw_name}.mp4"
    if not raw.exists():
        raise FileNotFoundError(f"Manim finished but {raw} is missing")

    enc = ["ffmpeg", "-y", "-v", "error", "-i", str(raw)]
    if has_audio(raw):
        enc += ["-map", "0:v", "-map", "0:a", "-af", "loudnorm=I=-16:TP=-1.5:LRA=11",
                "-c:a", "aac", "-b:a", "160k", "-ar", "48000"]
    else:  # silent track keeps every platform/player happy
        enc += ["-f", "lavfi", "-i", "anullsrc=r=48000:cl=stereo", "-map", "0:v", "-map", "1:a",
                "-shortest", "-c:a", "aac", "-b:a", "96k"]
    tmp = final.with_suffix(".tmp.mp4")
    enc += ["-c:v", "libx264", "-preset", "slow", "-crf", str(q["crf"]), "-profile:v", "high",
            "-level", "4.1", "-pix_fmt", "yuv420p", "-r", str(q["fps"]), "-movflags", "+faststart",
            str(tmp)]
    run(enc)
    tmp.replace(final)

    qc_root = ROOT / "output" / ("qc" if quality == "final" else "preview/qc")
    qc_dir = qc_root / f"{pid}{suffix}"
    qc_dir.mkdir(parents=True, exist_ok=True)
    for name in ("beats.json", "subtitles.srt"):
        if (log_dir / name).exists():
            shutil.copy(log_dir / name, qc_dir / name)
    if (log_dir / "subtitles.srt").exists():
        shutil.copy(log_dir / "subtitles.srt", final.with_suffix(".srt"))
    run([sys.executable, str(ROOT / "scripts" / "qc.py"), str(final), "--qc-dir", str(qc_dir),
         "--expect-audio" if audio else "--no-expect-audio"])
    print(f"DONE {pid}: {final.relative_to(ROOT)} in {time.time() - started:.0f}s")
    return final


def main():
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("problems", help="problem id, comma-separated ids, or 'all'")
    ap.add_argument("--quality", choices=QUALITY, default="final")
    ap.add_argument("--theme", choices=["kinan", "dark"], default="kinan")
    ap.add_argument("--no-audio", action="store_true", help="ignore narration audio (silent video)")
    ap.add_argument("--force", action="store_true", help="overwrite an existing final video")
    ap.add_argument("--timeout", type=int, default=5400, help="seconds per Manim render")
    args = ap.parse_args()
    results = {}
    for pid in problem_ids(args.problems):
        try:
            results[pid] = str(render(pid, args.quality, args.theme, not args.no_audio,
                                      args.force, args.timeout).relative_to(ROOT))
        except Exception as exc:  # report every failure, keep rendering the rest
            print(f"FAILED {pid}: {exc}", file=sys.stderr)
            results[pid] = f"FAILED: {exc}"
    print(json.dumps(results, indent=2))
    if any(v.startswith("FAILED") for v in results.values()):
        sys.exit(1)


if __name__ == "__main__":
    main()
