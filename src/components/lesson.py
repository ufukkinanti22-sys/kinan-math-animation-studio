"""Reusable lesson steps shared by the problem scenes (read the question, show options,
reveal the answer, summary card). Used as a mixin on :class:`KinanScene`."""

from __future__ import annotations

from manim import (
    DOWN, LEFT, RIGHT, UP, Circumscribe, Create, FadeIn, FadeOut, GrowFromCenter, Indicate,
    LaggedStart, Line, VGroup, Write,
)

from .cards import Card, TextCard
from .probability import Choices, Coin
from .text import BLACK, HEAVY, M, T
from .theme import THEME


def coin_row(faces: str, r: float = 0.3, gap: float = 0.12) -> VGroup:
    return VGroup(*[Coin(f, radius=r) for f in faces]).arrange(RIGHT, buff=gap)


class LessonMixin:
    def read_question(self, beat_q: str, beat_opts: str, question: str, options: list[str],
                      marks: list[tuple[str, str]], option_tokens: list[str], icon=None,
                      size: float = 42, max_chars: int = 30):
        """Question card (verbatim) with highlighter marks synced to the narration, then options."""
        with self.beat(beat_q):
            card = TextCard(question, width=8.0, size=size, max_chars=max_chars, pad=0.42).move_to([0, 3.1, 0])
            group = VGroup(card)
            if icon is not None:
                icon.next_to(card, DOWN, buff=0.4)
                group.add(icon)
            self.play(FadeIn(card, shift=0.3 * UP), run_time=0.8)
            if icon is not None:
                self.play(FadeIn(icon, scale=0.8), run_time=0.6)
            ms = VGroup()
            for token, phrase in marks:
                self.until(token)
                m = card.mark(phrase)
                self.add(m)
                self.play(FadeIn(m), run_time=0.5)
                ms.add(m)
            self.qcard = VGroup(card.card, ms, card.text)
            self.q_icon = icon
        with self.beat(beat_opts):
            choices = Choices(options, width=8.0, height=1.45, size=50)
            choices.move_to([0, (icon.get_bottom()[1] if icon is not None else card.get_bottom()[1]) - 1.15, 0])
            self.play(LaggedStart(*[FadeIn(c, shift=0.2 * UP) for c in choices], lag_ratio=0.15), run_time=0.9)
            for i, tok in enumerate(option_tokens):
                self.until(tok)
                # outline only: Indicate() would recolour the fraction into the card while it is read
                self.play(Circumscribe(choices[i], color=THEME.hl, buff=0.06, stroke_width=6), run_time=0.7)
            self.choices = choices

    def clear_question(self, keep_top: bool = False):
        mobs = [self.qcard, self.choices] + ([self.q_icon] if self.q_icon is not None else [])
        self.play(*[FadeOut(m) for m in mobs], run_time=0.6)

    def word_fraction(self, num: str, den: str, y: float = -0.6, lhs: str = "Peluang =") -> VGroup:
        left = T(lhs, size=50, weight=BLACK)
        n = T(num, size=44, color=THEME.good, weight=BLACK)
        d = T(den, size=44, color=THEME.blue, weight=BLACK)
        bar = Line(LEFT, RIGHT).set_stroke(THEME.ink, 7)
        bar.set_width(max(n.width, d.width) + 0.3)
        frac = VGroup(n, bar, d).arrange(DOWN, buff=0.25)
        row = VGroup(left, frac).arrange(RIGHT, buff=0.35).move_to([0, y, 0])
        row.num, row.den, row.bar, row.lhs = n, d, bar, left
        return row

    def reveal_answer(self, beat: str, options: list[str], correct: int, token: str, result=None):
        with self.beat(beat):
            choices = Choices(options, width=8.0, height=1.45, size=50).move_to([0, 0.6, 0])
            if result is not None:  # make room first so the result never sits on the cards
                self.play(result.animate.move_to([0, 3.3, 0]), run_time=0.6)
            self.play(FadeIn(choices, shift=0.2 * UP), run_time=0.6)
            self.until(token)
            self.play(*[choices[i].animate.set_opacity(0.3) for i in range(len(options)) if i != correct],
                      choices[correct].animate.scale(1.12), run_time=0.6)
            badge = choices.mark(correct)
            self.play(choices[correct][0].body.animate.set_fill(THEME.soft_green), GrowFromCenter(badge),
                      run_time=0.5)
            self.answer_group = VGroup(choices, badge) if result is None else VGroup(choices, badge, result)

    def summary_card(self, beat: str, title: str, rows: list, cues: list[str | None], highlight_last=True):
        """Card with a title and rows (text or mobjects) revealed on narration cues."""
        with self.beat(beat):
            mobs = [r if not isinstance(r, str) else T(r, size=38, weight=HEAVY) for r in rows]
            body = VGroup(*mobs).arrange(DOWN, buff=0.38, aligned_edge=LEFT)
            head = T(title, size=46, weight=BLACK, color=THEME.hl)
            h = body.height + head.height + 1.6
            card = Card(8.1, h).move_to([0, 2.6, 0])
            head.move_to(card.body.get_top() + DOWN * 0.6)
            body.next_to(head, DOWN, buff=0.5)
            if body.width > 7.4:
                body.scale_to_fit_width(7.4)
            body.set_x(0)
            self.play(FadeIn(card, shift=0.2 * UP), Write(head), run_time=0.8)
            for m, cue in zip(mobs, cues):
                if cue:
                    self.until(cue)
                self.play(FadeIn(m, shift=0.15 * RIGHT), run_time=0.6)
            if highlight_last:
                self.play(Circumscribe(mobs[-1], color=THEME.hl, buff=0.12), run_time=0.9)
