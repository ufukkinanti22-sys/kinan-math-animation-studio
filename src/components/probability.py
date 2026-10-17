"""Probability objects: dice, coins, playing cards and answer choices."""

from __future__ import annotations

from manim import (
    DOWN, LEFT, RIGHT, UP, Circle, Dot, RoundedRectangle, VGroup,
)

from .cards import Badge, Card
from .text import BLACK, HEAVY, M, SYMBOL, T
from .theme import THEME

PIPS = {
    1: [(0, 0)],
    2: [(-1, 1), (1, -1)],
    3: [(-1, 1), (0, 0), (1, -1)],
    4: [(-1, 1), (1, 1), (-1, -1), (1, -1)],
    5: [(-1, 1), (1, 1), (0, 0), (-1, -1), (1, -1)],
    6: [(-1, 1), (1, 1), (-1, 0), (1, 0), (-1, -1), (1, -1)],
}


class Die(VGroup):
    """Die face showing ``n`` pips."""

    def __init__(self, n: int, size: float = 0.8, fill: str | None = None, pip: str | None = None,
                 stroke_width: float = 5, **kw):
        super().__init__(**kw)
        self.n = n
        self.body = RoundedRectangle(width=size, height=size, corner_radius=size * 0.2,
                                     fill_color=fill or THEME.card, fill_opacity=1,
                                     stroke_color=THEME.card_stroke, stroke_width=stroke_width)
        self.pips = VGroup(*[
            Dot([x * size * 0.26, y * size * 0.26, 0], radius=size * 0.085, color=pip or THEME.ink)
            for x, y in PIPS[n]
        ])
        self.add(self.body, self.pips)


class Coin(VGroup):
    """Coin showing ``G`` (gambar, picture side) or ``A`` (angka, number side)."""

    def __init__(self, face: str, radius: float = 0.32, **kw):
        super().__init__(**kw)
        self.face = face
        gold = face == "G"
        self.disc = Circle(radius=radius, fill_color=THEME.hl if gold else THEME.soft_blue,
                           fill_opacity=1, stroke_color=THEME.card_stroke, stroke_width=4)
        self.rim = Circle(radius=radius * 0.78, stroke_color=THEME.warn if gold else THEME.blue,
                          stroke_width=3, fill_opacity=0)
        self.label = T(face, size=radius * 120 * 0.95, weight=BLACK,
                       color=THEME.ink).move_to(self.disc)
        self.add(self.disc, self.rim, self.label)


SUIT_GLYPH = {"S": "♠", "H": "♥", "D": "♦", "C": "♣"}
RED_SUITS = {"H", "D"}


def suit_symbol(suit: str, size: float = 40):
    color = THEME.red_suit if suit in RED_SUITS else THEME.black_suit
    return T(SUIT_GLYPH[suit], size=size, weight=SYMBOL, color=color)


class PlayingCard(VGroup):
    """Playing card with rank in the corner and suit in the middle."""

    def __init__(self, rank: str, suit: str, width: float = 0.9, **kw):
        super().__init__(**kw)
        self.rank, self.suit = rank, suit
        self.red = suit in RED_SUITS
        self.face = rank in ("J", "Q", "K")
        h = width * 1.4
        color = THEME.red_suit if self.red else THEME.black_suit
        self.body = RoundedRectangle(width=width, height=h, corner_radius=width * 0.12,
                                     fill_color=THEME.card, fill_opacity=1,
                                     stroke_color=THEME.card_stroke, stroke_width=max(2.5, width * 5))
        px = width * 120
        self.rank_label = T(rank, size=px * 0.36, weight=BLACK, color=color)
        self.rank_label.move_to(self.body.get_corner(UP + LEFT) + [width * 0.22, -h * 0.17, 0])
        self.suit_label = suit_symbol(suit, size=px * 0.5).move_to(self.body).shift(DOWN * h * 0.1)
        self.add(self.body, self.rank_label, self.suit_label)


class MiniCard(VGroup):
    """Compact card for a 52-card overview grid (rank + small suit)."""

    def __init__(self, rank: str, suit: str, width: float = 0.56, **kw):
        super().__init__(**kw)
        self.rank, self.suit = rank, suit
        self.red = suit in RED_SUITS
        self.face = rank in ("J", "Q", "K")
        h = width * 1.36
        color = THEME.red_suit if self.red else THEME.black_suit
        self.body = RoundedRectangle(width=width, height=h, corner_radius=width * 0.14,
                                     fill_color=THEME.card, fill_opacity=1,
                                     stroke_color=THEME.card_stroke, stroke_width=2.5)
        px = width * 120
        self.rank_label = T(rank, size=px * 0.42, weight=BLACK, color=color)
        self.suit_label = suit_symbol(suit, size=px * 0.36)
        VGroup(self.rank_label, self.suit_label).arrange(DOWN, buff=h * 0.07).move_to(self.body)
        self.add(self.body, self.rank_label, self.suit_label)


class Choices(VGroup):
    """Answer options A-D, each a small card with a letter and a LaTeX value."""

    def __init__(self, options: list[str], width: float = 8.0, height: float = 1.25,
                 size: float = 44, **kw):
        super().__init__(**kw)
        n = len(options)
        gap = 0.18
        w = (width - gap * (n - 1)) / n
        self.cards, self.letters, self.values = VGroup(), VGroup(), VGroup()
        for i, tex in enumerate(options):
            card = Card(w, height, radius=0.18, stroke_width=4)
            letter = T("ABCDE"[i], size=34, weight=BLACK, color=THEME.purple)
            value = M(tex, size=size)
            row = VGroup(letter, value).arrange(RIGHT, buff=0.18).move_to(card.body)
            self.cards.add(card)
            self.letters.add(letter)
            self.values.add(value)
            self.add(VGroup(card, row))
        self.arrange(RIGHT, buff=gap)

    def item(self, i: int) -> VGroup:
        return self[i]

    def mark(self, i: int, good: bool = True) -> Badge:
        """A badge positioned on the top-right corner of option ``i``."""
        return Badge(good, size=0.5).move_to(self.cards[i].body.get_corner(UP + RIGHT) + [-0.06, -0.02, 0])


def outcome_row(*mobs, buff: float = 0.12) -> VGroup:
    return VGroup(*mobs).arrange(RIGHT, buff=buff)
