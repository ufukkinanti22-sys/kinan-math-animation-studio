#!/usr/bin/env python3
"""End-to-end: owner's voice recordings -> new MP4s with the converted narration.

    # 1. trial on P01 only, with full verification
    python -m voice_swap.run --zip Kinan_Voice_References.zip --seedvc-dir seed-vc --stage trial
    # 2. the other three videos (only if the trial passed verification)
    python -m voice_swap.run --zip Kinan_Voice_References.zip --seedvc-dir seed-vc --stage rest

Per video: Seed-VC conversion of every beat -> objective verification -> new audio track at the
original beat times -> stream-copy mux into the ORIGINAL final video -> QC. Outputs go to
``voice_out/`` (git-ignored) with new names; the original videos are never touched. A video that
fails verification is still written (so it can be judged by ear) but named ``..._BELUM_LOLOS``.
"""

from __future__ import annotations

import argparse
import json
import os
import shutil
import subprocess
import sys
import zipfile
from pathlib import Path

from . import assemble, check_licenses, convert_beats, prepare_reference, verify
from .common import OUT, PRIVATE, PROBLEMS, ROOT

TRIAL = PROBLEMS[0]


def qc_new_video(pid: str, mp4: Path, tmp: Path) -> dict:
    """Run the project's own QC (format, A/V sync, loudness, black/frozen frames) on the new MP4."""
    qc_dir = tmp / f"qc_{pid}"
    qc_dir.mkdir(parents=True, exist_ok=True)
    shutil.copy(ROOT / "output" / "qc" / pid / "beats.json", qc_dir / "beats.json")
    r = subprocess.run([sys.executable, str(ROOT / "scripts" / "qc.py"), str(mp4), "--qc-dir", str(qc_dir)],
                       capture_output=True, text=True)
    return {"ok": r.returncode == 0, "output": r.stdout.strip().splitlines()}


def process(pid: str, args, sv, torch, asr, reference: Path) -> dict:
    beats = PRIVATE / "converted" / pid
    print(f"\n=== {pid}: converting {len(convert_beats.beats_log(pid))} beats")
    convert_beats.convert_problem(pid, reference, beats, sv, torch, args.steps, args.cfg,
                                  convert_beats.DEFAULTS["seed"], bool(torch.cuda.is_available()))
    print(f"=== {pid}: verifying")
    ver = verify.verify(pid, beats, reference, asr)
    for attempt in (1, 2):  # beats that failed are converted again (new seed, silence padding) up to twice
        bad = ver.get("flagged_beats", [])
        if ver["ok"] or not bad:
            break
        print(f"=== {pid}: retry {attempt} for {bad}")
        for b in bad:
            (beats / f"{b}.wav").unlink(missing_ok=True)
        convert_beats.convert_problem(pid, reference, beats, sv, torch, args.steps, args.cfg,
                                      convert_beats.DEFAULTS["seed"] + 7919 * attempt,
                                      bool(torch.cuda.is_available()))
        ver = verify.verify(pid, beats, reference, asr)
        ver["retries"] = attempt
    (OUT / "reports").mkdir(parents=True, exist_ok=True)
    suffix = "_suara_kinan" if ver["ok"] else "_suara_kinan_BELUM_LOLOS"
    print(f"=== {pid}: building video ({'verified' if ver['ok'] else 'NOT verified'})")
    built = assemble.build_video(pid, beats, OUT, suffix)
    qc = qc_new_video(pid, Path(built["video"]), OUT / "tmp")
    rep = {"problem": pid, "verified": ver["ok"], "verification": ver, "build": built, "qc": qc,
           "picture_identical_to_original": bool(built["video_packets_identical"] and built["decoded_frames_identical"])}
    (OUT / "reports" / f"{pid}.json").write_text(json.dumps(rep, indent=1, ensure_ascii=False), encoding="utf-8")
    print(f"    verified={ver['ok']}  picture identical={rep['picture_identical_to_original']}  qc={'PASS' if qc['ok'] else 'FAIL'}")
    for p in ver["problems"]:
        print("    PROBLEM:", p)
    return rep


def package() -> Path:
    """One ZIP with the new MP4s, full-track WAVs, per-beat WAVs and reports. No reference audio."""
    z = OUT / "Kinan_Voice_Swap_Hasil.zip"
    with zipfile.ZipFile(z, "w", zipfile.ZIP_DEFLATED) as zf:
        for sub in ("videos", "audio", "reports"):
            for f in sorted((OUT / sub).glob("*")):
                zf.write(f, f"{sub}/{f.name}")
        for pid in PROBLEMS:
            for f in sorted((PRIVATE / "converted" / pid).glob("*.wav")):
                zf.write(f, f"audio_per_segmen/{pid}/{f.name}")
    return z


def main() -> None:
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("--zip", type=Path, help="the owner's voice recordings (ZIP)")
    ap.add_argument("--seedvc-dir", type=Path, default=Path(os.environ.get("SEEDVC_DIR", "seed-vc")))
    ap.add_argument("--stage", choices=["trial", "rest", "all"], default="trial")
    ap.add_argument("--steps", type=int, default=convert_beats.DEFAULTS["steps"])
    ap.add_argument("--cfg", type=float, default=convert_beats.DEFAULTS["cfg"])
    ap.add_argument("--asr-model", default=None)
    ap.add_argument("--force", action="store_true", help="continue to the other videos even if the trial failed")
    args = ap.parse_args()

    seedvc_dir = args.seedvc_dir.resolve()
    ref_dir = (PRIVATE / "reference").resolve()
    if not (ref_dir / "reference.wav").exists():
        if not args.zip:
            sys.exit("--zip is required the first time (to build the reference clip)")
        prepare_reference.build_reference(args.zip.resolve(), ref_dir)
    reference = ref_dir / "reference.wav"
    print("reference:", reference, "(private, never commit)")

    (OUT / "reports").mkdir(parents=True, exist_ok=True)
    lic = check_licenses.check(seedvc_dir)
    (OUT / "reports" / "licenses.json").write_text(json.dumps(lic, indent=1), encoding="utf-8")
    print("licences:", json.dumps(lic["seed_vc_code"]), [m["license"] for m in lic["models"]])

    todo = {"trial": [TRIAL], "rest": PROBLEMS[1:], "all": PROBLEMS}[args.stage]
    if args.stage in ("rest",) and not args.force:
        t = OUT / "reports" / f"{TRIAL}.json"
        if not t.exists() or not json.loads(t.read_text()).get("verified"):
            sys.exit(f"the trial ({TRIAL}) has not passed verification: not converting the other videos "
                     f"(re-run with --stage trial, or --force)")

    sv, torch = convert_beats.load_seedvc(seedvc_dir)
    asr = verify.Asr(args.asr_model)
    results = {}
    for pid in todo:
        results[pid] = process(pid, args, sv, torch, asr, reference)
        if args.stage == "all" and pid == TRIAL and not results[pid]["verified"] and not args.force:
            print("trial failed verification: stopping (use --force to continue)")
            break
    z = package()
    print("\nSUMMARY")
    for pid, r in results.items():
        print(f"  {pid}: verified={r['verified']} picture identical={r['picture_identical_to_original']} qc={r['qc']['ok']}")
    print("package:", z)


if __name__ == "__main__":
    sys.exit(main())
