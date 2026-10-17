#!/usr/bin/env python3
"""Automated technical QC of a rendered video.

    python scripts/qc.py output/videos/p01_dadu_berbeda.mp4 --qc-dir output/qc/p01_dadu_berbeda

Checks container/codec/resolution/frame-rate/duration, audio presence and
loudness, black or empty frames, and writes for human review:
* ``contact_sheet.jpg``: one frame every few seconds,
* ``beats/<n>_<beat>.jpg``: the last frame of every narration beat,
* ``qc.json``: machine-readable results (``ok`` is false on any failure).

This does not judge mathematical correctness or visual taste; those are
reviewed by looking at the generated frames.
"""

from __future__ import annotations

import argparse
import json
import re
import subprocess
import sys
from pathlib import Path


def probe(path: Path) -> dict:
    out = subprocess.run(["ffprobe", "-v", "error", "-show_streams", "-show_format", "-of", "json",
                          str(path)], capture_output=True, text=True, check=True)
    return json.loads(out.stdout)


def frame_at(video: Path, t: float, dest: Path, width: int = 540):
    subprocess.run(["ffmpeg", "-y", "-v", "error", "-ss", f"{max(0, t):.3f}", "-i", str(video),
                    "-frames:v", "1", "-vf", f"scale={width}:-2", "-q:v", "3", str(dest)], check=True)


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("video", type=Path)
    ap.add_argument("--qc-dir", type=Path, required=True)
    ap.add_argument("--expect-audio", dest="expect_audio", action="store_true", default=True)
    ap.add_argument("--no-expect-audio", dest="expect_audio", action="store_false")
    args = ap.parse_args()
    qc = args.qc_dir
    qc.mkdir(parents=True, exist_ok=True)
    checks: list[dict] = []

    def check(name: str, ok: bool, detail: str = ""):
        checks.append({"check": name, "ok": bool(ok), "detail": detail})

    info = probe(args.video)
    v = next(s for s in info["streams"] if s["codec_type"] == "video")
    a = next((s for s in info["streams"] if s["codec_type"] == "audio"), None)
    dur = float(info["format"]["duration"])
    num, den = map(int, v["r_frame_rate"].split("/"))
    check("codec h264", v["codec_name"] == "h264", v["codec_name"])
    check("pixel format yuv420p", v.get("pix_fmt") == "yuv420p", v.get("pix_fmt", ""))
    check("frame rate 30", abs(num / den - 30) < 0.01, v["r_frame_rate"])
    check("vertical 9:16", v["width"] * 16 == v["height"] * 9, f"{v['width']}x{v['height']}")
    check("duration > 10 s", dur > 10, f"{dur:.2f}s")
    check("audio stream present", a is not None, a["codec_name"] if a else "none")

    narrated = None
    beats_file = qc / "beats.json"
    beats = json.loads(beats_file.read_text())["beats"] if beats_file.exists() else []
    if beats:
        narrated = all(b.get("audio") for b in beats)
        check("narration audio on every beat" if args.expect_audio else "silent render (no narration)",
              narrated if args.expect_audio else True,
              f"{sum(1 for b in beats if b.get('audio'))}/{len(beats)} beats have voice-over")

    if a is not None:
        r = subprocess.run(["ffmpeg", "-v", "info", "-i", str(args.video), "-af", "volumedetect",
                            "-vn", "-f", "null", "-"], capture_output=True, text=True)
        mean = re.search(r"mean_volume: (-?[\d.]+) dB", r.stderr)
        peak = re.search(r"max_volume: (-?[\d.]+) dB", r.stderr)
        if mean and peak:
            m, p = float(mean.group(1)), float(peak.group(1))
            if narrated:
                check("speech loudness reasonable", -30 < m < -10 and p <= 0.0, f"mean {m} dB, peak {p} dB")
            else:
                check("audio level", True, f"mean {m} dB, peak {p} dB (silent track expected)")

    # A/V sync: every narrated beat must start speaking right when its visuals start,
    # and speech must not run past the end of its beat (truncation / overlap).
    if narrated and a is not None:
        r = subprocess.run(["ffmpeg", "-v", "info", "-i", str(args.video), "-af",
                            "silencedetect=noise=-38dB:d=0.18", "-vn", "-f", "null", "-"],
                           capture_output=True, text=True)
        onsets = [float(x) for x in re.findall(r"silence_end: ([\d.]+)", r.stderr)]
        offsets = [float(x) for x in re.findall(r"silence_start: ([\d.]+)", r.stderr)]
        late, overrun = [], []
        for b in beats:
            hits = [o for o in onsets if b["start"] - 0.05 <= o <= b["start"] + 0.8]
            if not hits and not (b["start"] < 0.1):  # speech at t=0 has no preceding silence
                late.append(b["id"])
            ends = [o for o in offsets if b["start"] < o <= b["end"] + 0.5]
            if ends and max(ends) > b["end"] + 0.15:
                overrun.append(b["id"])
        check("speech starts with its beat (A/V sync)", not late,
              f"{len(beats) - len(late)}/{len(beats)} beats" + (f"; late: {late}" if late else ""))
        check("no speech runs past its beat", not overrun, ", ".join(overrun))

    # blank frames: blackdetect on luma; our backgrounds are never black
    r = subprocess.run(["ffmpeg", "-v", "info", "-i", str(args.video), "-vf",
                        "blackdetect=d=0.2:pix_th=0.05", "-an", "-f", "null", "-"],
                       capture_output=True, text=True)
    blacks = re.findall(r"black_start:([\d.]+)", r.stderr)
    check("no black frames", not blacks, ", ".join(blacks[:5]))

    # frozen video longer than 12 s usually means a broken timeline
    r = subprocess.run(["ffmpeg", "-v", "info", "-i", str(args.video), "-vf",
                        "freezedetect=n=0.0005:d=12", "-an", "-f", "null", "-"],
                       capture_output=True, text=True)
    freezes = re.findall(r"freeze_start: ([\d.]+)", r.stderr)
    check("no frozen stretch > 12 s", not freezes, ", ".join(freezes[:5]))

    # human-review material
    step = max(2.0, dur / 24)
    n_tiles = int(dur // step) + 1
    rows = (n_tiles + 5) // 6
    subprocess.run(["ffmpeg", "-y", "-v", "error", "-i", str(args.video), "-vf",
                    f"fps=1/{step:.3f},scale=270:-2,tile=6x{rows}:padding=6:color=white",
                    "-frames:v", "1", "-q:v", "4", str(qc / "contact_sheet.jpg")], check=True)
    bdir = qc / "beats"
    bdir.mkdir(exist_ok=True)
    for old in bdir.glob("*.jpg"):
        old.unlink()
    for i, b in enumerate(beats, 1):
        frame_at(args.video, b["end"] - 0.1, bdir / f"{i:02d}_{b['id']}.jpg")

    ok = all(c["ok"] for c in checks)
    report = {"video": str(args.video), "duration": round(dur, 2), "ok": ok, "checks": checks}
    (qc / "qc.json").write_text(json.dumps(report, indent=2), encoding="utf-8")
    for c in checks:
        print(f"[{'PASS' if c['ok'] else 'FAIL'}] {c['check']}: {c['detail']}")
    print(f"QC {'PASSED' if ok else 'FAILED'} for {args.video.name}")
    sys.exit(0 if ok else 1)


if __name__ == "__main__":
    main()
