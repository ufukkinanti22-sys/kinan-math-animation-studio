#!/usr/bin/env python3
"""Read the licence of every model Seed-VC downloads, straight from Hugging Face.

    python -m voice_swap.check_licenses --out voice_out/reports/licenses.json

Code licence is read from the cloned Seed-VC ``LICENSE`` (GPL-3.0). Model licences come from
the model cards on huggingface.co; when the site is unreachable the entry says "unverified"
instead of guessing.
"""

from __future__ import annotations

import argparse
import json
import os
import sys
from pathlib import Path

# repo id, role in the pipeline
MODELS = [
    ("Plachta/Seed-VC", "voice-conversion DiT (seed-uvit-whisper-small-wavenet)"),
    ("openai/whisper-small", "content encoder (Whisper-small encoder)"),
    ("nvidia/bigvgan_v2_22khz_80band_256x", "vocoder"),
    ("funasr/campplus", "speaker-style encoder (CAM++)"),
]


def seedvc_code_license(seedvc_dir: Path) -> str:
    f = seedvc_dir / "LICENSE"
    if not f.exists():
        return "unverified (LICENSE not found)"
    head = f.read_text(errors="ignore")[:200].upper()
    return "GPL-3.0" if "GNU GENERAL PUBLIC LICENSE" in head and "VERSION 3" in head else "see LICENSE"


def check(seedvc_dir: Path) -> dict:
    out = {"seed_vc_code": seedvc_code_license(seedvc_dir), "models": []}
    try:
        from huggingface_hub import HfApi

        api = HfApi()
    except Exception as exc:  # noqa: BLE001
        api, err = None, str(exc)
    for repo, role in MODELS:
        entry = {"repo": repo, "role": role, "license": "unverified", "url": f"https://huggingface.co/{repo}"}
        if api is not None:
            try:
                info = api.model_info(repo)
                lic = (info.card_data.license if info.card_data else None) or next(
                    (t.split(":", 1)[1] for t in (info.tags or []) if t.startswith("license:")), None)
                entry["license"] = lic or "no license field on the model card"
            except Exception as exc:  # noqa: BLE001
                entry["license"] = f"unverified ({type(exc).__name__}: huggingface.co not reachable?)"
        out["models"].append(entry)
    return out


def main() -> None:
    ap = argparse.ArgumentParser()
    ap.add_argument("--seedvc-dir", type=Path, default=Path(os.environ.get("SEEDVC_DIR", "seed-vc")))
    ap.add_argument("--out", type=Path)
    a = ap.parse_args()
    res = check(a.seedvc_dir)
    print(json.dumps(res, indent=1))
    if a.out:
        a.out.parent.mkdir(parents=True, exist_ok=True)
        a.out.write_text(json.dumps(res, indent=1), encoding="utf-8")


if __name__ == "__main__":
    sys.exit(main())
