#!/usr/bin/env python3
"""Write ``problems/<id>/storyboard.md``: scene-by-scene storyboard with real
timestamps (from the last final render's ``output/qc/<id>/beats.json``) and
the complete Indonesian narration script.

    python scripts/storyboard.py p01_dadu_berbeda
    python scripts/storyboard.py all
"""

from __future__ import annotations

import argparse
import json
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT))

from src.utils.narration import PROBLEMS, load_beats  # noqa: E402


def ts(t: float) -> str:
    return f"{int(t // 60)}:{t % 60:04.1f}"


def build(pid: str) -> Path:
    script, beats = load_beats(pid)
    log_path = ROOT / "output" / "qc" / pid / "beats.json"
    log = {b["id"]: b for b in json.loads(log_path.read_text())["beats"]} if log_path.exists() else {}
    total = json.loads(log_path.read_text())["duration"] if log_path.exists() else None
    out = [f"# Storyboard — {script.get('title', pid)}", ""]
    if total:
        out += [f"Durasi video final: **{ts(total)}** · 1080×1920 · 30 fps · suara: `{script.get('voice')}` "
                f"(rate {script.get('rate')})", ""]
    else:
        out += ["_Timestamps are estimates: no final render log found yet._", ""]
    out += ["Waktu diambil dari render terakhir (`output/qc/<id>/beats.json`). "
            "Setiap baris adalah satu *beat*: narasi, teks layar, dan animasinya berjalan bersamaan.", ""]
    chapter = None
    t_est = 0.0
    for i, raw in enumerate(script["beats"], 1):
        b = beats[raw["id"]]
        start, end = (log[b.id]["start"], log[b.id]["end"]) if b.id in log else (t_est, t_est + b.duration)
        t_est = end
        if b.chapter and b.chapter != chapter:
            chapter = b.chapter
            out += [f"## {chapter}", ""]
        out += [f"**{i}. `{b.id}`** · {ts(start)} – {ts(end)}", "",
                f"- **Animasi:** {raw.get('visual', '—')}",
                f"- **Narasi:** {b.say}",
                f"- **Teks layar:** {b.caption.replace('~', ' ').replace(' | ', ' / ')}", ""]
    out += ["---", "", "## Naskah narasi lengkap", ""]
    chapter = None
    for raw in script["beats"]:
        b = beats[raw["id"]]
        if b.chapter and b.chapter != chapter:
            chapter = b.chapter
            out += ["", f"**[{chapter}]**", ""]
        out.append(b.say)
        out.append("")
    path = PROBLEMS / pid / "storyboard.md"
    path.write_text("\n".join(out), encoding="utf-8")
    return path


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("problems", help="problem id, comma-separated ids, or 'all'")
    args = ap.parse_args()
    ids = (sorted(p.name for p in PROBLEMS.iterdir() if (p / "narration.yaml").exists())
           if args.problems == "all" else args.problems.split(","))
    for pid in ids:
        print(build(pid).relative_to(ROOT))


if __name__ == "__main__":
    main()
