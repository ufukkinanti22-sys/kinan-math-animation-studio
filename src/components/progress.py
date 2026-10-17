"""Segmented green progress indicator (one segment per chapter)."""

from __future__ import annotations

from manim import LEFT, RIGHT, Line, VGroup
from manim.constants import CapStyleType

from .theme import THEME

PX = 1 / 120


class SegmentedProgress(VGroup):
    """Pill segments that fill continuously while a chapter plays.

    ``start_chapter(i, planned_seconds)`` marks earlier segments full and makes
    segment ``i`` fill over ``planned_seconds`` of scene time.
    """

    def __init__(self, n: int, width: float = 7.6, gap: float = 0.14, thickness_px: float = 20, **kw):
        super().__init__(**kw)
        self.n = max(1, n)
        seg_w = (width - gap * (self.n - 1)) / self.n
        r = thickness_px * PX / 2
        self.tracks, self.fills, self.spans = VGroup(), VGroup(), []
        stroke = thickness_px * 0.9  # Manim stroke width units ~ px at this frame size
        for i in range(self.n):
            x0 = -width / 2 + i * (seg_w + gap) + r
            x1 = x0 + seg_w - 2 * r
            track = Line([x0, 0, 0], [x1, 0, 0]).set_stroke(THEME.faint, stroke)
            fill = Line([x0, 0, 0], [x0 + 1e-3, 0, 0]).set_stroke(THEME.good, stroke, opacity=0)
            for ln in (track, fill):
                ln.cap_style = CapStyleType.ROUND
            self.tracks.add(track)
            self.fills.add(fill)
            self.spans.append((x0, x1))
        self.add(self.tracks, self.fills)
        self.clock = 0.0
        self.chapter = -1
        self.chapter_start = 0.0
        self.planned = 1.0
        self.add_updater(self._tick)

    def start_chapter(self, i: int, planned_seconds: float):
        self.chapter = i
        self.chapter_start = self.clock
        self.planned = max(planned_seconds, 0.5)

    def _set_fill(self, i: int, frac: float):
        x0, x1 = self.spans[i]
        line = self.fills[i]
        if frac <= 0:
            line.set_stroke(opacity=0)
            return
        y = self.tracks[i].get_center()[1]
        line.put_start_and_end_on([x0, y, 0], [x0 + max(1e-3, (x1 - x0) * frac), y, 0])
        line.set_stroke(opacity=1)

    def _tick(self, m, dt):
        self.clock += dt
        for i in range(self.n):
            if i < self.chapter:
                frac = 1.0
            elif i == self.chapter:
                frac = min(1.0, (self.clock - self.chapter_start) / self.planned)
            else:
                frac = 0.0
            self._set_fill(i, frac)
