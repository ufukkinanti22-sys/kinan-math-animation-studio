"""``KinanScene``: base class for every problem video.

It owns the header (segmented progress + chapter pill), narration audio and
karaoke captions, and exposes ``beat()`` / ``until()`` so animations can be
synchronised with what the narrator is saying::

    with self.beat("syarat") as b:
        self.play(Create(grid))
        self.until("diagonal")          # wait until that word is spoken
        self.play(Indicate(diagonal))

When the ``with`` block ends the scene waits until the beat's narration (plus
its pause) has finished, so audio and visuals never drift apart.
"""

from __future__ import annotations

import json
import os
from contextlib import contextmanager
from pathlib import Path

from manim import FadeIn, FadeOut, Scene, UP, config

from ..utils.narration import ROOT, Beat, load_beats
from .caption import KaraokeCaption
from .cards import Pill
from .progress import SegmentedProgress
from .theme import THEME

config.frame_width = 9
config.frame_height = 16
config.background_color = THEME.bg

PROGRESS_Y = 7.2
PILL_Y = 6.55


class KinanScene(Scene):
    problem_id: str = ""

    def setup(self):
        self.camera.background_color = THEME.bg
        use_audio = os.environ.get("KINAN_AUDIO", "1") != "0"
        self.script, self.beats = load_beats(self.problem_id, use_audio=use_audio)
        self.chapters: list[str] = []
        self.chapter_plan: dict[str, float] = {}
        current = None
        for b in self.beats.values():
            if b.chapter:
                current = b.chapter
                if current not in self.chapters:
                    self.chapters.append(current)
            if current:
                self.chapter_plan[current] = self.chapter_plan.get(current, 0) + b.duration
        self.progress = SegmentedProgress(len(self.chapters)).set_y(PROGRESS_Y)
        self.progress.set_z_index(60)
        self.add(self.progress)
        self.pill: Pill | None = None
        self.log: list[dict] = []
        self._beat: Beat | None = None
        self._beat_start = 0.0

    # ------------------------------------------------------------------ timing
    @property
    def now(self) -> float:
        return self.renderer.time

    @contextmanager
    def beat(self, beat_id: str):
        b = self.beats[beat_id]
        self._beat, self._beat_start = b, self.now
        if b.audio is not None:
            self.add_sound(str(b.audio))
        caption = KaraokeCaption(b)
        self.add(caption)
        if b.chapter:
            self._enter_chapter(b.chapter)
        yield b
        remaining = self._beat_start + b.duration - self.now
        if remaining > 1 / config.frame_rate:
            self.wait(remaining)
        self.remove(caption)
        self.log.append({
            "id": b.id, "start": round(self._beat_start, 3), "end": round(self.now, 3),
            "chapter": b.chapter, "audio": b.audio is not None, "say": b.say,
            "pages": [{"start": round(self._beat_start + p.start, 3),
                       "end": round(self._beat_start + min(p.end, b.duration), 3),
                       "text": " ".join(w.text for w in p.words)} for p in b.pages],
        })
        self._beat = None

    def until(self, token: str | None = None, occurrence: int = 1, offset: float = 0.0,
              at: float | None = None):
        """Wait until ``token`` is spoken in the current beat (or ``at`` seconds into it)."""
        assert self._beat is not None, "until() must be called inside beat()"
        t = at if at is not None else self._beat.time_of(token, occurrence)
        remaining = self._beat_start + t + offset - self.now
        if remaining > 1 / config.frame_rate:
            self.wait(remaining)

    def left(self) -> float:
        """Seconds of narration left in the current beat."""
        assert self._beat is not None
        return max(0.0, self._beat_start + self._beat.duration - self.now)

    # ----------------------------------------------------------------- header
    def _enter_chapter(self, name: str):
        idx = self.chapters.index(name)
        self.progress.start_chapter(idx, self.chapter_plan.get(name, 5))
        new = Pill(name).set_y(PILL_Y).set_z_index(60)
        if self.pill is None:
            self.play(FadeIn(new, shift=0.15 * UP), run_time=0.35)
        else:
            self.play(FadeOut(self.pill, shift=0.15 * UP), FadeIn(new, shift=0.15 * UP), run_time=0.35)
        self.pill = new

    # ------------------------------------------------------------------ output
    def tear_down(self):
        out = Path(os.environ.get("KINAN_LOG_DIR", ROOT / "output" / "tmp" / self.problem_id))
        out.mkdir(parents=True, exist_ok=True)
        (out / "beats.json").write_text(json.dumps(
            {"problem": self.problem_id, "theme": THEME.name, "duration": round(self.now, 3),
             "beats": self.log}, indent=2, ensure_ascii=False), encoding="utf-8")
        cues = [p for b in self.log for p in b["pages"]]
        srt = []
        for i, c in enumerate(cues, 1):
            srt += [str(i), f"{_ts(c['start'])} --> {_ts(c['end'])}", c["text"], ""]
        (out / "subtitles.srt").write_text("\n".join(srt), encoding="utf-8")


def _ts(t: float) -> str:
    ms = int(round(t * 1000))
    h, ms = divmod(ms, 3_600_000)
    m, ms = divmod(ms, 60_000)
    s, ms = divmod(ms, 1000)
    return f"{h:02d}:{m:02d}:{s:02d},{ms:03d}"
