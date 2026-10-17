#!/usr/bin/env python3
"""Speech-to-speech voice conversion of every narration beat with Seed-VC (zero-shot).

    python -m voice_swap.convert_beats p01_dadu_berbeda \
        --reference voice_private/reference/reference.wav --seedvc-dir /path/to/seed-vc

SOURCE voice = the narrator's separate per-beat tracks (assets/audio/<id>/<beat>.mp3, clean TTS,
no music). TARGET voice = the reference clip made by ``prepare_reference``. The conversion keeps
words, pauses and tempo (``length_adjust=1.0``); the DiT only changes the voice identity.

Seed-VC (https://github.com/Plachtaa/seed-vc, GPL-3.0) is imported at run time from a separate
checkout, it is not copied into this repository. Its models are downloaded from Hugging Face.

Resumable: beats whose WAV already exists are skipped. Output: ``<out>/<beat>.wav`` (22.05 kHz).
"""

from __future__ import annotations

import argparse
import json
import os
import shutil
import sys
import tempfile
import time
from pathlib import Path
from types import SimpleNamespace

import numpy as np

from .common import PRIVATE, PROBLEMS, beats_log, decode, source_mp3, write_wav

DEFAULTS = {"steps": 30, "cfg": 0.7, "seed": 20261017}


def load_seedvc(seedvc_dir: Path):
    """Import Seed-VC's ``inference`` module once and make its model loading cached."""
    import torch

    seedvc_dir = seedvc_dir.resolve()
    if not (seedvc_dir / "inference.py").exists():
        raise SystemExit(f"Seed-VC not found in {seedvc_dir} (git clone https://github.com/Plachtaa/seed-vc)")
    sys.path.insert(0, str(seedvc_dir))
    os.chdir(seedvc_dir)  # Seed-VC uses relative paths (configs/, ./checkpoints cache)
    sys.argv = [sys.argv[0]]
    if not torch.cuda.is_available():
        import transformers  # CPU: Whisper must not be loaded in float16

        orig = transformers.WhisperModel.from_pretrained

        def fp32(name, *a, **k):
            k["torch_dtype"] = torch.float32
            return orig(name, *a, **k)

        transformers.WhisperModel.from_pretrained = fp32
        torch.set_num_threads(os.cpu_count() or 4)
    import inference as sv

    cache: dict = {}
    real = sv.load_models

    def cached(args):
        if "m" not in cache:
            cache["m"] = real(args)
        return cache["m"]

    sv.load_models = cached
    return sv, torch


def convert_problem(pid: str, reference: Path, out_dir: Path, sv, torch, steps: int, cfg: float,
                    seed: int, fp16: bool, log=print) -> list[dict]:
    out_dir.mkdir(parents=True, exist_ok=True)
    stats = []
    reference = reference.resolve()
    for i, b in enumerate(beats_log(pid)):
        dst = out_dir / f"{b['id']}.wav"
        if dst.exists():
            continue
        with tempfile.TemporaryDirectory() as td:
            td = Path(td)
            src = td / f"{b['id']}.wav"
            audio = decode(source_mp3(pid, b["id"]), 22050)
            write_wav(src, audio, 22050)
            args = SimpleNamespace(source=str(src), target=str(reference), output=str(td / "out"),
                                   diffusion_steps=steps, length_adjust=1.0, inference_cfg_rate=cfg,
                                   f0_condition=False, auto_f0_adjust=False, semi_tone_shift=0,
                                   checkpoint=None, config=None, fp16=fp16)
            torch.manual_seed(seed + i)
            t0 = time.time()
            sv.main(args)
            produced = list((td / "out").glob("vc_*.wav"))
            if len(produced) != 1:
                raise RuntimeError(f"{pid}/{b['id']}: Seed-VC produced {len(produced)} files")
            shutil.move(str(produced[0]), str(dst))
            dt = time.time() - t0
        stats.append({"beat": b["id"], "source_s": round(len(audio) / 22050, 2), "seconds": round(dt, 1),
                      "rtf": round(dt / (len(audio) / 22050), 2)})
        log(f"  {pid}/{b['id']:<10} {stats[-1]['source_s']:5.1f}s speech  ->  {dt:5.1f}s")
    return stats


def main() -> None:
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("problem", help="problem id or 'all'")
    ap.add_argument("--reference", type=Path, default=PRIVATE / "reference" / "reference.wav")
    ap.add_argument("--seedvc-dir", type=Path, default=Path(os.environ.get("SEEDVC_DIR", "seed-vc")))
    ap.add_argument("--out", type=Path, default=PRIVATE / "converted")
    ap.add_argument("--steps", type=int, default=DEFAULTS["steps"])
    ap.add_argument("--cfg", type=float, default=DEFAULTS["cfg"])
    ap.add_argument("--seed", type=int, default=DEFAULTS["seed"])
    a = ap.parse_args()
    ref, out = a.reference.resolve(), a.out.resolve()  # resolve before Seed-VC changes the cwd
    sv, torch = load_seedvc(a.seedvc_dir)
    fp16 = bool(torch.cuda.is_available())
    ids = PROBLEMS if a.problem == "all" else [a.problem]
    for pid in ids:
        stats = convert_problem(pid, ref, out / pid, sv, torch, a.steps, a.cfg, a.seed, fp16)
        (out / pid / "conversion_stats.json").write_text(json.dumps(stats, indent=1))


if __name__ == "__main__":
    sys.exit(main())
