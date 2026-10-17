#!/usr/bin/env python3
"""Generate Indonesian voice-over for one or more problems.

    python scripts/narrate.py p01_dadu_berbeda          # one problem
    python scripts/narrate.py all                       # every problem

For every beat in ``problems/<id>/narration.yaml`` this writes
``assets/audio/<id>/<beat>.mp3`` and records duration plus per-word start
times in ``assets/audio/<id>/timings.json``. Beats whose text, voice and rate
are unchanged are skipped (hash check), so re-running is cheap.

Uses Microsoft Edge neural voices through ``edge-tts`` (needs internet
access; GitHub-hosted runners have it).
"""

from __future__ import annotations

import argparse
import asyncio
import json
import subprocess
import sys
import time
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT))

from src.utils.narration import AUDIO, PROBLEMS, load_script, text_hash  # noqa: E402


def problem_ids(arg: str) -> list[str]:
    if arg == "all":
        return sorted(p.name for p in PROBLEMS.iterdir() if (p / "narration.yaml").exists())
    return [a.strip() for a in arg.split(",") if a.strip()]


def mp3_duration(path: Path) -> float:
    out = subprocess.run(
        ["ffprobe", "-v", "error", "-show_entries", "format=duration", "-of", "csv=p=0", str(path)],
        capture_output=True, text=True, check=True)
    return float(out.stdout.strip())


async def synth(text: str, voice: str, rate: str, path: Path) -> list[dict]:
    import edge_tts

    words: list[dict] = []
    comm = edge_tts.Communicate(text, voice, rate=rate, boundary="WordBoundary")
    with open(path, "wb") as fh:
        async for chunk in comm.stream():
            if chunk["type"] == "audio":
                fh.write(chunk["data"])
            elif chunk["type"] == "WordBoundary":
                start = chunk["offset"] / 1e7
                words.append({"text": chunk["text"], "start": round(start, 3),
                              "end": round(start + chunk["duration"] / 1e7, 3)})
    return words


def narrate(pid: str, force: bool = False) -> int:
    script = load_script(pid)
    voice = script.get("voice", "id-ID-ArdiNeural")
    rate = script.get("rate", "+0%")
    out_dir = AUDIO / pid
    out_dir.mkdir(parents=True, exist_ok=True)
    tpath = out_dir / "timings.json"
    timings = json.loads(tpath.read_text()) if tpath.exists() else {}
    made = 0
    valid_ids = set()
    for beat in script["beats"]:
        bid = beat["id"]
        valid_ids.add(bid)
        say = " ".join(beat["say"].split())
        h = text_hash(say, voice, rate)
        mp3 = out_dir / f"{bid}.mp3"
        if not force and timings.get(bid, {}).get("hash") == h and mp3.exists():
            continue
        for attempt in range(4):
            try:
                words = asyncio.run(synth(say, voice, rate, mp3))
                dur = mp3_duration(mp3)
                break
            except Exception as exc:  # network hiccups: retry with backoff
                if attempt == 3:
                    raise RuntimeError(f"TTS failed for {pid}/{bid}: {exc}") from exc
                time.sleep(2 ** (attempt + 1))
        timings[bid] = {"hash": h, "voice": voice, "rate": rate, "duration": round(dur, 3),
                        "words": words}
        made += 1
        print(f"  {pid}/{bid}: {dur:5.2f}s, {len(words)} words")
    for stale in set(timings) - valid_ids:  # beats removed from the script
        timings.pop(stale)
        (out_dir / f"{stale}.mp3").unlink(missing_ok=True)
    tpath.write_text(json.dumps(timings, indent=1, ensure_ascii=False), encoding="utf-8")
    total = sum(t["duration"] for t in timings.values())
    print(f"{pid}: {made} beat(s) synthesised, {len(timings)} total, {total:.1f}s of speech")
    return made


def main():
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("problems", help="problem id, comma-separated ids, or 'all'")
    ap.add_argument("--force", action="store_true", help="re-synthesise even if unchanged")
    args = ap.parse_args()
    for pid in problem_ids(args.problems):
        narrate(pid, force=args.force)


if __name__ == "__main__":
    main()
