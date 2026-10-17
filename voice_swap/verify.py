#!/usr/bin/env python3
"""Objective checks of the converted narration, beat by beat.

    python -m voice_swap.verify p01_dadu_berbeda --beats voice_private/converted/p01_dadu_berbeda \
        --reference voice_private/reference/reference.wav

1. completeness / pronunciation: a speech recogniser (faster-whisper, Indonesian) transcribes the
   ORIGINAL narrator beat and the CONVERTED beat; both are compared with the script (``say``) and
   with each other. Conversion must not add errors compared with the original narrator.
2. timing: length difference, envelope lag/correlation and word start times (ASR word timestamps)
   against the original beat, i.e. words, pauses and tempo are preserved.
3. voice similarity: Resemblyzer speaker embeddings, converted vs. the owner's reference clip,
   with the original narrator vs. the reference as baseline.

The numbers are objective evidence, they do not replace listening to the result.
"""

from __future__ import annotations

import argparse
import difflib
import json
import re
import sys
from pathlib import Path

import numpy as np
import yaml

from .assemble import lag_and_corr
from .common import PRIVATE, PROBLEMS, ROOT, SR, beats_log, decode, source_mp3

# pass / fail thresholds
MAX_LEN_DIFF_S = 0.25
MIN_ENV_CORR, MAX_LAG_MS = 0.60, 40
MAX_CER_EXTRA = 0.05  # converted may be at most this much worse than the original narrator (per beat)
MAX_WER_EXTRA_MEAN = 0.05
MIN_SIM, MIN_SIM_GAIN = 0.65, 0.08
MIN_TIMING_BEAT_S = 1.5  # shorter beats are too short for envelope / embedding statistics


def say_text(pid: str) -> dict[str, str]:
    d = yaml.safe_load((ROOT / "problems" / pid / "narration.yaml").read_text(encoding="utf-8"))
    return {b["id"]: " ".join(b["say"].split()) for b in d["beats"]}


def normalise(text: str) -> str:
    """Lower-case, numbers/fractions/symbols spelled out in Indonesian, no punctuation."""
    from num2words import num2words

    def num(s: str) -> str:
        return num2words(int(s), lang="id")

    t = text.lower().replace("−", "-").replace("×", " kali ")
    t = re.sub(r"(\d+)\s*/\s*(\d+)", lambda m: f" {num(m[1])} per {num(m[2])} ", t)
    t = re.sub(r"(?<=\d)\s*\+\s*(?=\d)", " tambah ", t)
    t = re.sub(r"\d+", lambda m: f" {num(m.group())} ", t)
    t = re.sub(r"[^\w\s]|_", " ", t)
    return " ".join(t.split())


def error_rates(ref: str, hyp: str) -> tuple[float, float]:
    """(word error rate, character error rate ignoring spaces: robust to 'a b' vs 'ab')."""
    import jiwer

    r, h = normalise(ref), normalise(hyp)
    wer = jiwer.wer(r, h) if r else 0.0
    cer = jiwer.cer(r.replace(" ", ""), h.replace(" ", "")) if r else 0.0
    return float(wer), float(cer)


class Asr:
    def __init__(self, size: str | None = None):
        import torch
        from faster_whisper import WhisperModel

        gpu = torch.cuda.is_available()
        self.model = WhisperModel(size or ("medium" if gpu else "small"),
                                  device="cuda" if gpu else "cpu", compute_type="float16" if gpu else "int8")

    def __call__(self, wav: Path) -> tuple[str, list[tuple[str, float]]]:
        # decode with ffmpeg ourselves (faster-whisper's PyAV decoder breaks on some PyAV versions)
        segs, _ = self.model.transcribe(decode(wav, 16000), language="id", beam_size=5, word_timestamps=True,
                                        condition_on_previous_text=False)
        words = [(w.word, float(w.start)) for s in segs for w in (s.words or [])]
        return " ".join(w for w, _ in words), words


def word_shift(a: list[tuple[str, float]], b: list[tuple[str, float]]) -> list[float]:
    """Start-time differences (s) of the words both recognitions agree on."""
    na = [normalise(w) for w, _ in a]
    nb = [normalise(w) for w, _ in b]
    out = []
    for blk in difflib.SequenceMatcher(None, na, nb, autojunk=False).get_matching_blocks():
        for k in range(blk.size):
            out.append(b[blk.b + k][1] - a[blk.a + k][1])
    return out


def verify(pid: str, beat_dir: Path, reference: Path, asr: Asr | None, log=print) -> dict:
    from resemblyzer import VoiceEncoder

    enc = VoiceEncoder("cpu", verbose=False)
    ref_emb = enc.embed_utterance(decode(reference, 16000))
    ref_emb = ref_emb / np.linalg.norm(ref_emb)
    say = say_text(pid)
    rows = []
    for b in beats_log(pid):
        bid = b["id"]
        src_mp3, conv = source_mp3(pid, bid), beat_dir / f"{bid}.wav"
        x_src, x_conv = decode(src_mp3), decode(conv)
        row = {"beat": bid, "len_diff_s": round((len(x_conv) - len(x_src)) / SR, 3)}
        long_enough = len(x_src) / SR >= MIN_TIMING_BEAT_S
        if long_enough:
            n = min(len(x_src), len(x_conv))
            lag, corr = lag_and_corr(x_src[:n], x_conv[:n])
            row.update(env_lag_ms=lag, env_corr=round(corr, 3))
            e1, e2 = (enc.embed_utterance(decode(p, 16000)) for p in (src_mp3, conv))
            row["sim_src_ref"] = round(float(e1 @ ref_emb / np.linalg.norm(e1)), 3)
            row["sim_conv_ref"] = round(float(e2 @ ref_emb / np.linalg.norm(e2)), 3)
        if asr is not None:
            t_src, w_src = asr(src_mp3)
            t_conv, w_conv = asr(conv)
            row["asr_src"], row["asr_conv"] = t_src, t_conv
            row["wer_src"], row["cer_src"] = (round(v, 3) for v in error_rates(say[bid], t_src))
            row["wer_conv"], row["cer_conv"] = (round(v, 3) for v in error_rates(say[bid], t_conv))
            sh = word_shift(w_src, w_conv)
            if sh:
                row["word_shift_median_ms"] = round(1000 * float(np.median(np.abs(sh))))
                row["word_shift_max_ms"] = round(1000 * float(np.max(np.abs(sh))))
        rows.append(row)
        log(f"  {bid:<10} " + "  ".join(f"{k}={v}" for k, v in row.items() if k.startswith(("len", "env", "sim_conv", "cer_conv"))))

    problems = []
    for r in rows:
        if abs(r["len_diff_s"]) > MAX_LEN_DIFF_S:
            problems.append(f"{r['beat']}: length differs {r['len_diff_s']:+.2f}s from the original")
        if "env_corr" in r and (r["env_corr"] < MIN_ENV_CORR or abs(r["env_lag_ms"]) > MAX_LAG_MS):
            problems.append(f"{r['beat']}: timing envelope corr {r['env_corr']} lag {r['env_lag_ms']} ms")
        if "cer_conv" in r and r["cer_conv"] > r["cer_src"] + MAX_CER_EXTRA:
            problems.append(f"{r['beat']}: converted CER {r['cer_conv']} vs original {r['cer_src']} -> words lost/changed?")
        if r.get("word_shift_max_ms", 0) > 250:
            problems.append(f"{r['beat']}: a word starts {r['word_shift_max_ms']} ms away from the original")
    sims = [(r["sim_src_ref"], r["sim_conv_ref"]) for r in rows if "sim_conv_ref" in r]
    summary = {"beats": len(rows)}
    if sims:
        s_src, s_conv = (float(np.mean(v)) for v in zip(*sims))
        summary.update(sim_original_narrator_vs_reference=round(s_src, 3), sim_converted_vs_reference=round(s_conv, 3))
        if s_conv < MIN_SIM or s_conv < s_src + MIN_SIM_GAIN:
            problems.append(f"voice similarity {s_conv:.2f} (narrator baseline {s_src:.2f}) below the threshold")
    if asr is not None:
        w_src = float(np.mean([r["wer_src"] for r in rows]))
        w_conv = float(np.mean([r["wer_conv"] for r in rows]))
        summary.update(mean_wer_original=round(w_src, 3), mean_wer_converted=round(w_conv, 3))
        if w_conv > w_src + MAX_WER_EXTRA_MEAN:
            problems.append(f"mean WER {w_conv:.3f} vs original narrator {w_src:.3f}")
    else:
        problems.append("speech recognition was NOT run: pronunciation / missing words are unverified")
    return {"problem": pid, "ok": not problems, "problems": problems, "summary": summary, "per_beat": rows}


def main() -> None:
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("problem")
    ap.add_argument("--beats", type=Path)
    ap.add_argument("--reference", type=Path, default=PRIVATE / "reference" / "reference.wav")
    ap.add_argument("--asr-model", default=None)
    ap.add_argument("--no-asr", action="store_true")
    ap.add_argument("--out", type=Path)
    a = ap.parse_args()
    ids = PROBLEMS if a.problem == "all" else [a.problem]
    asr = None if a.no_asr else Asr(a.asr_model)
    for pid in ids:
        beats = a.beats or PRIVATE / "converted" / pid
        rep = verify(pid, beats, a.reference, asr)
        out = a.out or beats / "verification.json"
        out.write_text(json.dumps(rep, indent=1, ensure_ascii=False), encoding="utf-8")
        print(json.dumps({k: rep[k] for k in ("problem", "ok", "problems", "summary")}, indent=1, ensure_ascii=False))


if __name__ == "__main__":
    sys.exit(main())
