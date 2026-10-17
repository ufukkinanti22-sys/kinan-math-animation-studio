#!/usr/bin/env python3
"""Tulis naskah rekaman suara: teks persis seperti yang diucapkan narator,
satu caption per baris, satu baris kosong di antara bagian (beat).

    python scripts/naskah.py all
    python scripts/naskah.py p01_dadu_berbeda

Hasil: problems/<id>/naskah_rekaman.txt
"""

import argparse
import re
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT))

from src.utils.narration import PROBLEMS, load_script  # noqa: E402

MAX_CHARS = 52  # kalimat lebih panjang dari ini dipecah di koma / titik dua


def split_say(say: str) -> list[str]:
    say = " ".join(say.split())
    out = []
    for sent in re.split(r"(?<=[.?!])\s+", say):
        if len(sent) <= MAX_CHARS:
            out.append(sent)
            continue
        # pecah setelah koma / titik dua, gabungkan potongan pendek
        parts = re.split(r"(?<=[,:])\s+", sent)
        cur = ""
        for p in parts:
            if cur and len(cur) + 1 + len(p) > MAX_CHARS:
                out.append(cur)
                cur = p
            else:
                cur = f"{cur} {p}".strip()
        if cur:
            out.append(cur)
    return out


def build(pid: str) -> Path:
    script = load_script(pid)
    blocks = []
    for beat in script["beats"]:
        blocks.append("\n".join(split_say(beat["say"])))
    path = PROBLEMS / pid / "naskah_rekaman.txt"
    path.write_text("\n\n".join(blocks) + "\n", encoding="utf-8")
    return path


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("problems")
    args = ap.parse_args()
    ids = (sorted(p.name for p in PROBLEMS.iterdir() if (p / "narration.yaml").exists())
           if args.problems == "all" else args.problems.split(","))
    for pid in ids:
        print(build(pid).relative_to(ROOT))


if __name__ == "__main__":
    main()
