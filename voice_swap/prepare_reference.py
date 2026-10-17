#!/usr/bin/env python3
"""Pick the cleanest 1-speaker clips from the owner's voice recordings -> ``reference.wav``.

    python -m voice_swap.prepare_reference --zip Kinan_Voice_References.zip --out voice_private/reference

The recordings may contain pauses, music, noise, a second speaker. For every sliding window
the script measures
  * speaker consistency  (Resemblyzer embeddings vs. the dominant speaker of all recordings),
  * background tones     (stationary narrow-band peaks in the quiet frames = music / hum),
  * noise floor          (10th percentile level) and speech activity,
  * clipping,
and keeps the best ``--clips`` windows (non-overlapping, far apart). Seed-VC uses at most 25 s
of reference, so the default is 2 x 12 s = 24 s.

PRIVACY: the reference and its report are written under ``voice_private/`` (git-ignored).
Never commit them: the repository is public.
"""

from __future__ import annotations

import argparse
import json
import subprocess
import sys
import zipfile
from pathlib import Path

import numpy as np
import soundfile as sf
from scipy.ndimage import uniform_filter1d

from .common import PRIVATE, SR, sh

AUDIO_EXT = {".m4a", ".mp3", ".wav", ".aac", ".ogg", ".opus", ".flac", ".mp4", ".mov", ".webm"}
A_SR = 16000  # analysis rate
OUT_SR = 22050  # Seed-VC's native rate for the speech model


def safe_extract(zip_path: Path, dest: Path) -> list[Path]:
    """Extract only audio files, ignore paths that try to leave ``dest`` (zip-slip)."""
    dest.mkdir(parents=True, exist_ok=True)
    found = []
    with zipfile.ZipFile(zip_path) as z:
        for info in z.infolist():
            name = Path(info.filename)
            if info.is_dir() or name.suffix.lower() not in AUDIO_EXT:
                continue
            target = (dest / name.name).resolve()
            if dest.resolve() not in target.parents:
                continue
            target.write_bytes(z.read(info))
            found.append(target)
    return sorted(found)


def to_wav(src: Path, sr: int) -> np.ndarray:
    raw = subprocess.run(["ffmpeg", "-v", "error", "-i", str(src), "-vn", "-ac", "1", "-ar", str(sr),
                          "-f", "f32le", "-"], check=True, capture_output=True).stdout
    return np.frombuffer(raw, dtype=np.float32).copy()


def analyse(files: list[Path], clip_s: int, log=print):
    from librosa import stft
    from resemblyzer import VoiceEncoder
    from sklearn.cluster import AgglomerativeClustering

    enc = VoiceEncoder("cpu", verbose=False)
    audio = {f.name: to_wav(f, A_SR) for f in files}

    # 1) dominant speaker over all recordings (3 s blocks)
    blocks = []
    for y in audio.values():
        for s in range(0, len(y) - 3 * A_SR, 3 * A_SR):
            seg = y[s:s + 3 * A_SR]
            if np.sqrt((seg ** 2).mean()) > 1e-3:
                blocks.append(enc.embed_utterance(seg))
    E = np.array(blocks)
    lab = AgglomerativeClustering(n_clusters=2, metric="cosine", linkage="average").fit_predict(E)
    main = np.bincount(lab).argmax()
    centroid = E[lab == main].mean(0)
    centroid /= np.linalg.norm(centroid)
    share = float((lab == main).mean())
    log(f"dominant speaker covers {share:.0%} of {len(E)} blocks")

    # 2) windows
    wins = []
    for name, y in audio.items():
        sim = np.array([enc.embed_utterance(y[s * A_SR:(s + 3) * A_SR]) @ centroid
                        for s in range(0, len(y) // A_SR - 3)])
        mag = np.abs(stft(y, n_fft=512, hop_length=160))  # 10 ms frames, 31 Hz bins
        L = np.log(mag ** 2 + 1e-9)
        energy = mag.sum(0)  # amplitude (not power) so the 3 % activity threshold is ~ -30 dB
        for s in range(0, len(y) // A_SR - clip_s - 1):
            a, b = s * 100, (s + clip_s) * 100
            e = energy[a:b]
            quiet = e < np.percentile(e, 30)
            if quiet.sum() < 60:
                continue
            Ls = uniform_filter1d(L[16:160, a:b], size=15, axis=1)  # 0.5-5 kHz, 150 ms smoothing
            Q = Ls[:, quiet]
            tonal = float(np.mean(np.percentile(Q - uniform_filter1d(Q, size=9, axis=0), 98, axis=0)))
            seg = y[s * A_SR:(s + clip_s) * A_SR]
            rms = np.sqrt(np.convolve(seg ** 2, np.ones(320) / 320, "same"))[::160]
            db = 20 * np.log10(rms + 1e-6)
            sm = sim[s:s + clip_s - 2]
            wins.append({"file": name, "start": s, "cons_mean": float(sm.mean()), "cons_min": float(sm.min()),
                         "tonal": tonal, "noise_floor_db": float(np.percentile(db, 10)),
                         "activity": float((e > np.percentile(e, 95) * 0.03).mean()),
                         "clip": float((np.abs(seg) >= 0.985).mean())})
    return audio, wins, share


def score(w: dict) -> float:
    """Lower is better."""
    return (w["tonal"] - 3 * (w["cons_mean"] - 0.85) + 0.03 * (w["noise_floor_db"] + 40)
            - 0.8 * (w["activity"] - 0.7))


def choose(wins: list[dict], n: int, clip_s: int) -> list[dict]:
    # NB: no clipping filter. Low-bitrate AAC decodes to peaks above full scale (float peak ~1.4)
    # without any damage; the reference is peak-normalised afterwards (see build_reference).
    ok = [w for w in wins if w["cons_min"] >= 0.80 and 0.55 <= w["activity"] <= 0.97]
    if len(ok) < n:  # recordings are worse than hoped: relax, but say so in the report
        ok = [w for w in wins if w["cons_min"] >= 0.70] or wins
    ok.sort(key=score)
    picked: list[dict] = []
    for w in ok:
        if all(not (w["file"] == p["file"] and abs(w["start"] - p["start"]) < 3 * clip_s) for p in picked):
            picked.append(w)
        if len(picked) == n:
            break
    return picked


def build_reference(zip_path: Path, out: Path, clips: int = 2, clip_s: int = 12, log=print) -> dict:
    out.mkdir(parents=True, exist_ok=True)
    work = out / "_extracted"
    files = safe_extract(zip_path, work)
    if not files:
        raise SystemExit("no audio files found in the ZIP")
    log(f"{len(files)} recordings: " + ", ".join(f.name for f in files))
    audio, wins, share = analyse(files, clip_s, log)
    picked = choose(wins, clips, clip_s)
    parts = []
    gap = np.zeros(int(0.25 * OUT_SR), dtype=np.float32)
    by_name = {f.name: f for f in files}
    for w in sorted(picked, key=score):
        y = to_wav(by_name[w["file"]], OUT_SR)[w["start"] * OUT_SR:(w["start"] + clip_s) * OUT_SR]
        k = int(0.02 * OUT_SR)
        y[:k] *= np.linspace(0, 1, k, dtype=np.float32)
        y[-k:] *= np.linspace(1, 0, k, dtype=np.float32)
        parts += [y, gap]
    ref = np.concatenate(parts[:-1])
    peak = float(np.abs(ref).max())
    if peak > 0.95:  # keep headroom, no other processing (no denoising: it damages the timbre)
        ref *= 0.95 / peak
    sf.write(str(out / "reference.wav"), ref, OUT_SR, subtype="PCM_16")
    report = {"recordings": [f.name for f in files], "dominant_speaker_share": round(share, 3),
              "windows_analysed": len(wins), "clips": [{k: (round(v, 3) if isinstance(v, float) else v)
                                                         for k, v in w.items()} for w in picked],
              "reference_seconds": round(len(ref) / OUT_SR, 2),
              "warnings": ([] if share > 0.8 else ["more than one speaker is present in the recordings"]) +
                          (["source recordings are low-bitrate (see ffprobe); similarity is limited by them"])}
    (out / "reference_report.json").write_text(json.dumps(report, indent=1), encoding="utf-8")
    try:  # spectrogram of the chosen reference for a quick visual check (optional)
        import librosa
        import matplotlib
        matplotlib.use("Agg")
        import matplotlib.pyplot as plt
        M = librosa.power_to_db(librosa.feature.melspectrogram(y=ref, sr=OUT_SR, n_fft=1024, hop_length=220,
                                                               n_mels=96, fmax=8000), ref=np.max)
        fig, ax = plt.subplots(figsize=(11, 3.2))
        ax.imshow(M, origin="lower", aspect="auto", cmap="magma", vmin=-70, vmax=0,
                  extent=[0, len(ref) / OUT_SR, 0, 8])
        ax.set_xlabel("s"); ax.set_ylabel("kHz"); fig.tight_layout()
        fig.savefig(out / "reference_spectrogram.png", dpi=80)
    except Exception:  # noqa: BLE001
        pass
    import shutil
    shutil.rmtree(work, ignore_errors=True)  # do not leave extra copies of the recordings around
    return report


def main() -> None:
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("--zip", type=Path, required=True)
    ap.add_argument("--out", type=Path, default=PRIVATE / "reference")
    ap.add_argument("--clips", type=int, default=2)
    ap.add_argument("--clip-seconds", type=int, default=12)
    a = ap.parse_args()
    rep = build_reference(a.zip, a.out, a.clips, a.clip_seconds)
    print(json.dumps(rep, indent=1))


if __name__ == "__main__":
    sys.exit(main())
