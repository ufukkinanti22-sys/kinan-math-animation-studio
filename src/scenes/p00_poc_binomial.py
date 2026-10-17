"""Proof of concept: (a + b)^2 = a^2 + 2ab + b^2 seen as areas.

Render:  python scripts/render.py p00_poc_binomial
"""

import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[2]))

from manim import (  # noqa: E402
    DOWN, LEFT, RIGHT, UP, Brace, Circumscribe, Create, FadeIn, FadeOut, GrowFromCenter,
    Indicate, Line, Polygon, ReplacementTransform, TransformFromCopy, VGroup, Write, Square,
    LaggedStart,
)

from src.components.base import KinanScene  # noqa: E402
from src.components.cards import Card  # noqa: E402
from src.components.text import M  # noqa: E402
from src.components.theme import THEME  # noqa: E402

A, B = 3.2, 1.9  # side lengths in scene units (any a, b > 0 tell the same story)


def rect(x0, y0, w, h, fill):
    return Polygon([x0, y0, 0], [x0 + w, y0, 0], [x0 + w, y0 + h, 0], [x0, y0 + h, 0],
                   fill_color=fill, fill_opacity=1, stroke_color=THEME.ink, stroke_width=5)


class P00PocBinomial(KinanScene):
    problem_id = "p00_poc_binomial"

    def construct(self):
        s = A + B
        x0, y0 = -s / 2 + 0.25, -1.95  # bottom-left corner of the big square

        # ------------------------------------------------------------- hook
        with self.beat("hook"):
            claim = M("(a+b)^2", r"\overset{?}{=}", "a^2+b^2", size=78).set_y(4.9)
            claim[1].set_color(THEME.bad)
            self.play(Write(claim), run_time=1.6)
            self.until("Benarkah")
            self.play(Indicate(claim[1], color=THEME.bad, scale_factor=1.5))

        # ----------------------------------------------------------- square
        with self.beat("square"):
            seg_a = Line([x0, y0, 0], [x0 + A, y0, 0]).set_stroke(THEME.blue, 12)
            seg_b = Line([x0 + A, y0, 0], [x0 + s, y0, 0]).set_stroke(THEME.warn, 12)
            br_a = Brace(seg_a, DOWN, color=THEME.blue)
            br_b = Brace(seg_b, DOWN, color=THEME.warn)
            la = M("a", size=56, color=THEME.blue).next_to(br_a, DOWN, 0.12)
            lb = M("b", size=56, color=THEME.warn).next_to(br_b, DOWN, 0.12)
            self.play(Create(seg_a), GrowFromCenter(br_a), FadeIn(la), run_time=0.8)
            self.play(Create(seg_b), GrowFromCenter(br_b), FadeIn(lb), run_time=0.6)
            self.until("persegi")
            big = rect(x0, y0, s, s, THEME.card)
            self.play(Create(big), run_time=1.2)
            self.add(seg_a, seg_b)
            self.until("Luasnya")
            area = M("(a+b)^2", size=84).move_to(big)
            self.play(TransformFromCopy(claim[0], area), run_time=1.0)

        # -------------------------------------------------------------- cut
        with self.beat("cut"):
            v = Line([x0 + A, y0, 0], [x0 + A, y0 + s, 0]).set_stroke(THEME.ink, 6)
            h = Line([x0, y0 + A, 0], [x0 + s, y0 + A, 0]).set_stroke(THEME.ink, 6)
            self.play(FadeOut(area), run_time=0.4)
            self.until("mendatar")
            self.play(Create(h), run_time=0.8)
            self.until("tegak")
            self.play(Create(v), run_time=0.8)
            # left-edge labels confirm the cut is at the same distance a
            lb_l = Brace(Line([x0, y0, 0], [x0, y0 + A, 0]), LEFT, color=THEME.blue)
            lb_t = Brace(Line([x0, y0 + A, 0], [x0, y0 + s, 0]), LEFT, color=THEME.warn)
            la2 = M("a", size=56, color=THEME.blue).next_to(lb_l, LEFT, 0.12)
            lb2 = M("b", size=56, color=THEME.warn).next_to(lb_t, LEFT, 0.12)
            self.play(GrowFromCenter(lb_l), GrowFromCenter(lb_t), FadeIn(la2), FadeIn(lb2), run_time=0.7)

        # ------------------------------------------------------------ parts
        with self.beat("parts"):
            sq_a = rect(x0, y0, A, A, THEME.soft_blue)
            sq_b = rect(x0 + A, y0 + A, B, B, THEME.soft_orange)
            r1 = rect(x0 + A, y0, B, A, THEME.soft_green)
            r2 = rect(x0, y0 + A, A, B, THEME.soft_green)
            t_a = M("a^2", size=80, color=THEME.blue).move_to(sq_a)
            t_b = M("b^2", size=60, color=THEME.warn).move_to(sq_b)
            t_r1 = M("ab", size=60, color=THEME.ink).move_to(r1)
            t_r2 = M("ab", size=60, color=THEME.ink).move_to(r2)
            under = VGroup(sq_a, sq_b, r1, r2)
            self.add(under)
            under.set_opacity(0)
            self.bring_to_front(h, v, seg_a, seg_b)
            self.until("a²")
            self.play(sq_a.animate.set_fill(opacity=1).set_stroke(opacity=1), Write(t_a), run_time=0.8)
            self.until("b²")
            self.play(sq_b.animate.set_fill(opacity=1).set_stroke(opacity=1), Write(t_b), run_time=0.8)
            self.until("dua")
            self.play(LaggedStart(r1.animate.set_fill(opacity=1).set_stroke(opacity=1),
                                  r2.animate.set_fill(opacity=1).set_stroke(opacity=1),
                                  lag_ratio=0.3), run_time=0.9)
            self.play(Write(t_r1), Write(t_r2), run_time=0.7)

        # -------------------------------------------------------------- sum
        with self.beat("sum"):
            final = M("(a+b)^2", "=", "a^2", "+", "2ab", "+", "b^2", size=72).set_y(4.9)
            final[2].set_color(THEME.blue)
            final[6].set_color(THEME.warn)
            self.play(ReplacementTransform(claim[0], final[0]), FadeOut(claim[1:]),
                      FadeIn(final[1]), run_time=0.8)
            self.until("a²")
            self.play(TransformFromCopy(t_a, final[2]), FadeIn(final[3]), run_time=0.8)
            self.until("2ab")
            self.play(TransformFromCopy(VGroup(t_r1, t_r2), final[4]), FadeIn(final[5]), run_time=0.9)
            self.until("b²")
            self.play(TransformFromCopy(t_b, final[6]), run_time=0.8)

        # --------------------------------------------------------- takeaway
        with self.beat("takeaway"):
            self.play(Circumscribe(final[4], color=THEME.good, buff=0.12, stroke_width=8))
            self.until("dua")
            self.play(Indicate(r1, color=THEME.good, scale_factor=1.06),
                      Indicate(r2, color=THEME.good, scale_factor=1.06), run_time=1.2)
