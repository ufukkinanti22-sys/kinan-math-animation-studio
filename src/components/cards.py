"""Cards, pills, badges, markers and stamps: the reference video's UI vocabulary."""

from __future__ import annotations

import numpy as np
from manim import (
    DOWN, LEFT, ORIGIN, RIGHT, UP, Circle, Line, RoundedRectangle, VGroup, VMobject,
)

from .text import BLACK, HEAVY, T, lines, wrap
from .theme import THEME

PX = 1 / 120  # one pixel at 1080x1920


class Card(VGroup):
    """White rounded card with a thick outline and a hard offset shadow."""

    def __init__(self, width: float, height: float, fill: str | None = None,
                 stroke: str | None = None, radius: float = 0.22, shadow: bool = True,
                 stroke_width: float = 5, **kw):
        super().__init__(**kw)
        self.body = RoundedRectangle(
            width=width, height=height, corner_radius=radius,
            fill_color=fill or THEME.card, fill_opacity=1,
            stroke_color=stroke or THEME.card_stroke, stroke_width=stroke_width,
        )
        if shadow:
            self.shadow = self.body.copy().set_fill(THEME.shadow, 1).set_stroke(width=0)
            self.shadow.shift(RIGHT * 6 * PX + DOWN * 9 * PX)
            self.add(self.shadow)
        self.add(self.body)

    def restyle(self, fill: str | None = None, stroke: str | None = None):
        if fill:
            self.body.set_fill(fill, 1)
        if stroke:
            self.body.set_stroke(stroke)
        return self


class Pill(VGroup):
    """Small rounded chapter label, e.g. ``RUANG SAMPEL``."""

    def __init__(self, text: str, color: str | None = None, fill: str | None = None,
                 size: float = 34, **kw):
        super().__init__(**kw)
        label = T(text.upper(), size=size, color=color or THEME.purple, weight=BLACK)
        bg = RoundedRectangle(
            width=label.width + 0.5, height=label.height + 0.32, corner_radius=0.2,
            fill_color=fill or THEME.soft_purple, fill_opacity=1, stroke_width=0,
        )
        label.move_to(bg)
        self.add(bg, label)
        self.label = label


class Tag(VGroup):
    """Rounded tag with dark outline, e.g. ``SYARAT: mata dadu berbeda``."""

    def __init__(self, text: str, fill: str | None = None, color: str | None = None,
                 size: float = 30, stroke: str | None = None, **kw):
        super().__init__(**kw)
        label = T(text, size=size, color=color or THEME.ink, weight=HEAVY)
        bg = RoundedRectangle(
            width=label.width + 0.45, height=label.height + 0.36, corner_radius=0.18,
            fill_color=fill or THEME.hl, fill_opacity=1,
            stroke_color=stroke or THEME.card_stroke, stroke_width=4,
        )
        label.move_to(bg)
        self.add(bg, label)
        self.label = label


def check_mark(size: float = 0.5, color: str | None = None, width: float = 9) -> VMobject:
    pts = np.array([[-0.32, 0.02, 0], [-0.08, -0.24, 0], [0.34, 0.24, 0]]) * size / 0.7
    m = VMobject(stroke_color=color or THEME.card, stroke_width=width)
    m.set_points_as_corners(pts)
    return m


def cross_mark(size: float = 0.5, color: str | None = None, width: float = 9) -> VGroup:
    r = size * 0.32
    return VGroup(
        Line([-r, -r, 0], [r, r, 0]), Line([-r, r, 0], [r, -r, 0]),
    ).set_stroke(color or THEME.card, width)


class Badge(VGroup):
    """Round check (good) or cross (bad) badge."""

    def __init__(self, good: bool = True, size: float = 0.55, **kw):
        super().__init__(**kw)
        disc = Circle(radius=size / 2, fill_color=THEME.good if good else THEME.bad,
                      fill_opacity=1, stroke_color=THEME.card_stroke, stroke_width=4)
        mark = check_mark(size) if good else cross_mark(size)
        mark.move_to(disc)
        self.add(disc, mark)


def marker(mob, color: str | None = None, pad: float = 0.08, opacity: float = 1.0) -> RoundedRectangle:
    """Highlighter rectangle sized to sit *behind* ``mob``."""
    r = RoundedRectangle(
        width=mob.width + 2 * pad, height=mob.height + 2 * pad, corner_radius=0.08,
        fill_color=color or THEME.hl, fill_opacity=opacity, stroke_width=0,
    )
    r.move_to(mob)
    return r


def strike(mob, color: str | None = None, width: float = 7) -> Line:
    """Diagonal strike-through across ``mob``."""
    return Line(mob.get_corner(DOWN + LEFT), mob.get_corner(UP + RIGHT)).set_stroke(
        color or THEME.bad, width)


class Stamp(VGroup):
    """Tilted outlined stamp (``TANPA DEBAT`` style) for a dramatic verdict."""

    def __init__(self, text: str, color: str | None = None, size: float = 40,
                 angle: float = 0.12, **kw):
        super().__init__(**kw)
        c = color or THEME.bad
        label = T(text.upper(), size=size, color=c, weight=BLACK)
        frame = RoundedRectangle(width=label.width + 0.45, height=label.height + 0.4,
                                 corner_radius=0.12, stroke_color=c, stroke_width=7,
                                 fill_color=THEME.card, fill_opacity=1)
        label.move_to(frame)
        self.add(frame, label)
        self.rotate(angle)


class TextCard(VGroup):
    """Card holding wrapped text (used for the original question)."""

    def __init__(self, text: str, width: float = 8.0, size: float = 36,
                 max_chars: int = 34, pad: float = 0.4, fill: str | None = None, **kw):
        super().__init__(**kw)
        self.rows = wrap(text, max_chars)
        self.size = size
        self.text = lines(*self.rows, size=size)
        self.text.set_z_index(1)  # highlighter marks (z 0) always stay behind the words
        h = self.text.height + 2 * pad
        self.card = Card(width, h, fill=fill)
        self.text.move_to(self.card.body).align_to(self.card.body, LEFT).shift(RIGHT * pad)
        self.add(self.card, self.text)

    def mark(self, phrase: str, color: str | None = None) -> VGroup:
        """Highlighter boxes behind ``phrase`` (may span several lines)."""
        full = " ".join(self.rows)
        start = full.find(phrase)
        if start < 0:
            raise ValueError(f"phrase not in card: {phrase!r}")
        end = start + len(phrase)
        cap = self.size * 0.72 / 120
        boxes = VGroup()
        offset = 0
        for r, row in enumerate(self.rows):
            a, b = max(start, offset) - offset, min(end, offset + len(row)) - offset
            if a < b:
                glyphs = VGroup(*[g for ch, g in zip(row[a:b], self.text[r][a:b]) if ch != " "])
                base = min((g.get_bottom()[1] for ch, g in zip(row, self.text[r])
                            if ch in "acemnorsuvwxz"), default=self.text[r].get_bottom()[1])
                box = RoundedRectangle(width=glyphs.width + 0.14, height=cap * 1.9, corner_radius=0.07,
                                       fill_color=color or THEME.hl, fill_opacity=1, stroke_width=0)
                box.move_to([glyphs.get_center()[0], base + cap / 2, 0])
                boxes.add(box)
            offset += len(row) + 1
        return boxes


def column(*mobs, buff: float = 0.3, aligned_edge=ORIGIN) -> VGroup:
    return VGroup(*mobs).arrange(DOWN, buff=buff, aligned_edge=aligned_edge)
