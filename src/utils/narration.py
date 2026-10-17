"""Narration scripts, voice-over timings and caption pages.

A problem's narration lives in ``problems/<id>/narration.yaml``::

    id: p01_dadu_berbeda
    voice: id-ID-ArdiNeural
    rate: "-4%"
    beats:
      - id: hook
        chapter: TANTANGAN        # optional: starts a new progress segment
        say: "Dua dadu dilempar ..."   # exactly what the voice speaks
        caption: "Dua dadu dilempar ..." # optional on-screen text (defaults to say)
        pause: 0.4                # optional silence after the audio

Inside ``caption`` wrap words in ``*stars*`` to keep them emphasised after they
are spoken, use ``|`` to force a new caption page, and join tokens with ``~``
to keep them on one line (``(a~+~b)²``).

``scripts/narrate.py`` turns each beat into ``assets/audio/<id>/<beat>.mp3`` plus
``timings.json`` (duration and per-word start times). When no audio exists the
timings are *estimated* from the text length, so the animation can always be
rendered; the video is then silent and the QC report says so.
"""

from __future__ import annotations

import hashlib
import json
import re
from bisect import bisect_right
from dataclasses import dataclass, field
from pathlib import Path

import yaml

ROOT = Path(__file__).resolve().parents[2]
PROBLEMS = ROOT / "problems"
AUDIO = ROOT / "assets" / "audio"

CHARS_PER_SECOND = 12.5  # speaking-rate estimate used when no audio exists
DEFAULT_PAUSE = 0.45


@dataclass
class CaptionWord:
    text: str
    start: float  # seconds from the start of the beat
    key: bool = False  # emphasised (*word*) in the script


@dataclass
class CaptionPage:
    words: list[CaptionWord]
    start: float
    end: float


@dataclass
class Beat:
    id: str
    say: str
    caption: str
    chapter: str | None
    pause: float
    audio: Path | None
    speech: float  # seconds of speech
    word_times: list[tuple[str, float]] = field(default_factory=list)  # spoken words
    pages: list[CaptionPage] = field(default_factory=list)

    @property
    def duration(self) -> float:
        return self.speech + self.pause

    def time_of(self, token: str, occurrence: int = 1) -> float:
        """Start time of a caption word (case/punctuation-insensitive)."""
        want = _norm(token)
        seen = 0
        for page in self.pages:
            for w in page.words:
                if _norm(w.text) == want:
                    seen += 1
                    if seen == occurrence:
                        return w.start
        raise KeyError(f"word '{token}' not found in caption of beat '{self.id}'")


def text_hash(say: str, voice: str, rate: str) -> str:
    return hashlib.sha1(f"{voice}|{rate}|{say}".encode()).hexdigest()[:12]


def _norm(w: str) -> str:
    return re.sub(r"[^\w²³]", "", w.lower())


def _tokens(s: str) -> list[str]:
    return [t for t in s.replace("|", " | ").split() if t]


def _time_map(say_words: list[tuple[str, float]], speech: float):
    """Map 'fraction of spoken characters' -> seconds, from word start times."""
    total = sum(len(w) + 1 for w, _ in say_words) or 1
    xs, ys, acc = [], [], 0
    for w, t in say_words:
        xs.append(acc / total)
        ys.append(t)
        acc += len(w) + 1
    xs.append(1.0)
    ys.append(speech)

    def f(x: float) -> float:
        i = max(0, min(len(xs) - 2, bisect_right(xs, x) - 1))
        x0, x1, y0, y1 = xs[i], xs[i + 1], ys[i], ys[i + 1]
        return y0 if x1 == x0 else y0 + (y1 - y0) * (x - x0) / (x1 - x0)

    return f


def _paginate(caption: str, times, max_chars: int = 46) -> list[list[CaptionWord]]:
    """Split the caption into pages (sentences, or '|' breaks) of <= 2 short lines."""
    raw = _tokens(caption)
    words_only = [t for t in raw if t != "|"]
    total = sum(len(w.strip("*")) + 1 for w in words_only) or 1
    pages: list[list[CaptionWord]] = [[]]
    acc = 0
    for tok in raw:
        if tok == "|":
            if pages[-1]:
                pages.append([])
            continue
        key = tok.startswith("*") or tok.rstrip(".,:;?!").endswith("*")
        clean = tok.replace("*", "").replace("~", " ")  # ~ joins tokens that must not wrap
        pages[-1].append(CaptionWord(clean, times(acc / total), key))
        acc += len(clean) + 1
        if re.search(r"[.?!]$", clean) and not re.fullmatch(r"\d+\.", clean):
            pages.append([])
    pages = [p for p in pages if p]
    # Long sentences: split into chunks of about two lines.
    out: list[list[CaptionWord]] = []
    for p in pages:
        chunk: list[CaptionWord] = []
        n = 0
        for w in p:
            if chunk and n + len(w.text) > 2 * max_chars - 10:
                out.append(chunk)
                chunk, n = [], 0
            chunk.append(w)
            n += len(w.text) + 1
        if chunk:
            out.append(chunk)
    return out


def load_script(problem_id: str) -> dict:
    path = PROBLEMS / problem_id / "narration.yaml"
    with open(path, encoding="utf-8") as fh:
        return yaml.safe_load(fh)


def load_beats(problem_id: str, use_audio: bool = True) -> tuple[dict, dict[str, Beat]]:
    script = load_script(problem_id)
    voice = script.get("voice", "id-ID-ArdiNeural")
    rate = script.get("rate", "+0%")
    tpath = AUDIO / problem_id / "timings.json"
    timings = json.loads(tpath.read_text()) if (use_audio and tpath.exists()) else {}

    beats: dict[str, Beat] = {}
    for b in script["beats"]:
        say = " ".join(b["say"].split())
        caption = " ".join(b.get("caption", say).split())
        t = timings.get(b["id"])
        audio = AUDIO / problem_id / f"{b['id']}.mp3"
        if t and t.get("hash") == text_hash(say, voice, rate) and audio.exists():
            speech = float(t["duration"])
            word_times = [(w["text"], float(w["start"])) for w in t.get("words", [])]
        else:
            audio = None
            speech = round(len(say) / CHARS_PER_SECOND + 0.3, 2)
            word_times = []
        if not word_times:  # estimate: words spread by character count
            ws = say.split()
            total = sum(len(w) + 1 for w in ws) or 1
            acc, word_times = 0, []
            for w in ws:
                word_times.append((w, 0.15 + (speech - 0.4) * acc / total))
                acc += len(w) + 1
        beat = Beat(
            id=b["id"], say=say, caption=caption, chapter=b.get("chapter"),
            pause=float(b.get("pause", DEFAULT_PAUSE)), audio=audio,
            speech=speech, word_times=word_times,
        )
        times = _time_map(word_times, speech)
        page_words = _paginate(caption, times)
        for i, ws in enumerate(page_words):
            end = page_words[i + 1][0].start if i + 1 < len(page_words) else beat.duration
            beat.pages.append(CaptionPage(ws, ws[0].start if i else 0.0, end))
        beats[beat.id] = beat
    return script, beats
