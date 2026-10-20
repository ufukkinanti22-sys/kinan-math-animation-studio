"""Soal 3 (Bagian 2): dua dadu, peluang jumlah > 9 ATAU kembar = (6 + 6 - 2)/36 = 5/18.

Beginner path: "lebih dari 9" excludes 9 -> kembar -> "atau" = at least one (Venn) -> 36 pairs ->
sums in the table -> colour sum > 9 (6 cells) and doubles (6 cells) -> (5,5), (6,6) counted twice ->
6 + 6 - 2 = 10 -> 10/36 = 5/18 -> recount the coloured cells; the 12/36 trap.

Render:  python scripts/render.py p06_dua_dadu_atau
"""

import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[2]))

import numpy as np  # noqa: E402
from manim import (  # noqa: E402
    DOWN, LEFT, ORIGIN, PI, RIGHT, UP, AnimationGroup, Circle, Circumscribe, Create, FadeIn, FadeOut,
    GrowFromCenter, Indicate, LaggedStart, ReplacementTransform, RoundedRectangle, Square, TransformFromCopy,
    VGroup, Write,
)

from src.components.base import KinanScene  # noqa: E402
from src.components.cards import Badge, Card, Tag, strike  # noqa: E402
from src.components.lesson import LessonMixin  # noqa: E402
from src.components.probability import Die  # noqa: E402
from src.components.text import BLACK, HEAVY, Frac, M, T  # noqa: E402
from src.components.theme import THEME  # noqa: E402

QUESTION = "Dua dadu dilempar bersamaan. Peluang jumlah mata dadu lebih dari 9 atau kedua mata dadu sama adalah ..."
OPTIONS = [r"\frac{1}{4}", r"\frac{5}{18}", r"\frac{7}{18}", r"\frac{11}{18}"]
CORRECT = 1  # B
C = 0.86
GX0, GY0 = -2.1, 3.3  # left / top edge of the table
Z_LABEL = 2


def cell_center(i: int, j: int) -> np.ndarray:
    return np.array([GX0 + C * (i - 0.5), GY0 - C * (j - 0.5), 0])


class P06DuaDaduAtau(LessonMixin, KinanScene):
    problem_id = "p06_dua_dadu_atau"

    def construct(self):
        icon = VGroup(Die(4, size=0.95), Die(6, size=0.95)).arrange(RIGHT, buff=0.4)
        self.read_question("question", "options", QUESTION, OPTIONS,
                           [("*lebih~dari~9*,", "lebih dari 9"), ("*sama*?", "kedua mata dadu sama")],
                           ["1/4,", "5/18,", "7/18,", "11/18."], icon=icon, size=46, max_chars=28)
        self.understand()
        self.table()
        self.solve()
        self.reveal_answer("answer", OPTIONS, CORRECT, "B,", result=self.result)
        self.check()
        self.play(FadeOut(self.trap_group), run_time=0.5)
        self.summary_card("remember", "Yang perlu diingat", [
            T("Kejadian 'atau': gabungkan", size=40, weight=BLACK),
            T("semua kotak yang cocok,", size=40, weight=BLACK),
            T("yang masuk dua kelompok", size=40, weight=BLACK, color=THEME.hl),
            T("dihitung satu kali.", size=40, weight=BLACK, color=THEME.hl),
            M(r"6 + 6 - 2 = 10", size=58, color=THEME.good),
        ], ["*atau*", None, "dua", None, None])

    # ------------------------------------------------------------ meaning
    def understand(self):
        with self.beat("more"):
            self.clear_question()
            chips = VGroup()
            for n in range(2, 13):
                box = RoundedRectangle(width=0.6, height=0.66, corner_radius=0.12, fill_color=THEME.card,
                                       fill_opacity=1, stroke_color=THEME.faint, stroke_width=3)
                chips.add(VGroup(box, T(str(n), size=30, weight=BLACK).move_to(box)))
            chips.arrange(RIGHT, buff=0.08).move_to([0, 3.6, 0])
            cap = T("jumlah kedua dadu", size=30, weight=BLACK, color=THEME.muted).next_to(chips, UP, 0.25)
            self.play(FadeIn(cap), LaggedStart(*[FadeIn(c, shift=0.1 * UP) for c in chips], lag_ratio=0.05), run_time=1.0)
            self.until("*tidak*")
            nine = chips[7]
            x9 = strike(nine, width=7)
            self.play(Indicate(nine, color=THEME.bad, scale_factor=1.3), run_time=0.6)
            self.play(Create(x9), nine[0].animate.set_fill(THEME.soft_red), run_time=0.5)
            self.until("10,")
            self.play(*[chips[k][0].animate.set_fill(THEME.warn).set_stroke(THEME.warn) for k in (8, 9, 10)],
                      *[chips[k][1].animate.set_color(THEME.hl_text) for k in (8, 9, 10)], run_time=0.7)
            self.numline = VGroup(cap, chips, x9)

        with self.beat("same"):
            pairs = VGroup()
            for a, cue in ((1, "(1,1)"), (5, "(5,5):")):
                p = VGroup(Die(a, size=0.85), Die(a, size=0.85)).arrange(RIGHT, buff=0.15)
                pairs.add(p)
            pairs.arrange(RIGHT, buff=1.0).move_to([0, 1.3, 0])
            lab = T("pasangan kembar", size=40, weight=BLACK, color=THEME.blue).next_to(pairs, DOWN, 0.4)
            self.until("(1,1)")
            self.play(FadeIn(pairs[0], shift=0.2 * UP), run_time=0.5)
            self.until("(5,5):")
            self.play(FadeIn(pairs[1], shift=0.2 * UP), run_time=0.5)
            self.until("*kembar*.")
            self.play(Write(lab), run_time=0.6)
            self.same = VGroup(pairs, lab)

        with self.beat("or"):
            self.play(FadeOut(self.same), self.numline.animate.scale(0.7).move_to([0, 4.9, 0]), run_time=0.6)
            a = Circle(radius=1.5, fill_color=THEME.warn, fill_opacity=0.35, stroke_color=THEME.warn,
                       stroke_width=6).move_to([-0.9, 1.4, 0])
            b = Circle(radius=1.5, fill_color=THEME.blue, fill_opacity=0.35, stroke_color=THEME.blue,
                       stroke_width=6).move_to([0.9, 1.4, 0])
            la = T("jumlah > 9", size=32, weight=BLACK, color=THEME.warn).move_to([-1.55, 3.2, 0])
            lb = T("kembar", size=32, weight=BLACK, color=THEME.blue).move_to([1.6, 3.2, 0])
            self.play(Create(a), Create(b), FadeIn(la), FadeIn(lb), run_time=0.9)
            self.until("*salah~satu*")
            self.play(a.animate.set_fill(opacity=0.7), b.animate.set_fill(opacity=0.7), run_time=0.6)
            word = T("ATAU = boleh salah satu, boleh keduanya", size=30, weight=BLACK, color=THEME.hl)
            word.move_to([0, -0.6, 0])
            self.play(FadeIn(word), run_time=0.5)
            self.until("dua-duanya")
            mid = T("dua-duanya", size=26, weight=BLACK, color=THEME.ink).move_to([0, 1.4, 0])
            self.play(FadeIn(mid), Indicate(mid, scale_factor=1.3), run_time=0.8)
            self.venn = VGroup(a, b, la, lb, word, mid)

    # --------------------------------------------------------------- table
    def table(self):
        with self.beat("all"):
            self.play(FadeOut(self.venn), FadeOut(self.numline), run_time=0.5)
            top = VGroup(*[Die(i, size=0.58).move_to([cell_center(i, 1)[0], GY0 + 0.5, 0]) for i in range(1, 7)])
            side = VGroup(*[Die(j, size=0.58).move_to([GX0 - 0.5, cell_center(1, j)[1], 0]) for j in range(1, 7)])
            for d in top:
                d.body.set_stroke(THEME.blue)
            for d in side:
                d.body.set_stroke(THEME.warn)
            l1 = T("Dadu 1", size=32, weight=BLACK, color=THEME.blue).move_to([cell_center(3.5, 1)[0], GY0 + 1.12, 0])
            l2 = T("Dadu 2", size=32, weight=BLACK, color=THEME.warn).rotate(PI / 2).move_to([GX0 - 1.15, cell_center(1, 3.5)[1], 0])
            self.play(FadeIn(l1), LaggedStart(*[FadeIn(d, shift=0.2 * DOWN) for d in top], lag_ratio=0.1), run_time=1.0)
            self.until("kedua")
            self.play(FadeIn(l2), LaggedStart(*[FadeIn(d, shift=0.2 * RIGHT) for d in side], lag_ratio=0.1), run_time=1.0)
            self.cells = {}
            for j in range(1, 7):
                for i in range(1, 7):
                    self.cells[i, j] = Square(C, fill_color=THEME.card, fill_opacity=1, stroke_color=THEME.faint,
                                              stroke_width=3).move_to(cell_center(i, j))
            self.until("6~×~6")
            self.play(LaggedStart(*[FadeIn(self.cells[k], scale=0.6) for k in sorted(self.cells, key=lambda k: (k[1], k[0]))],
                                  lag_ratio=0.03), run_time=1.6)
            self.until("*36*")
            t36 = Tag("36 pasangan", fill=THEME.soft_blue, size=38).move_to([0, -2.25, 0])
            self.play(FadeIn(t36), run_time=0.4)
            self.headers, self.t36 = VGroup(top, side, l1, l2), t36

        self.sums = {}
        with self.beat("sums"):
            self.until("*jumlah*")
            for (i, j), sq in self.cells.items():
                self.sums[i, j] = T(str(i + j), size=36, weight=BLACK).move_to(sq).set_z_index(Z_LABEL)
            order = sorted(self.cells, key=lambda k: (k[0] + k[1], k[0]))
            self.play(LaggedStart(*[FadeIn(self.sums[k]) for k in order], lag_ratio=0.03), run_time=2.0)

    # --------------------------------------------------------------- solve
    def solve(self):
        more = [(i, j) for i in range(1, 7) for j in range(1, 7) if i + j > 9]
        same = [(k, k) for k in range(1, 7)]
        both = [k for k in more if k in same]
        with self.beat("more_cells"):
            self.play(FadeOut(self.t36), run_time=0.3)
            for s, cue in ((10, "10:"), (11, "11:"), (12, "12:")):
                self.until(cue)
                ks = [k for k in more if sum(k) == s]
                self.play(*[self.cells[k].animate.set_fill(THEME.warn) for k in ks],
                          *[self.sums[k].animate.set_color(THEME.hl_text) for k in ks], run_time=0.5)
            self.until("*6*.")
            t1 = Tag("jumlah > 9: 6 kotak", fill=THEME.soft_orange, size=36).move_to([-1.95, -2.25, 0])
            self.play(FadeIn(t1, shift=0.2 * UP), run_time=0.5)
            self.t1 = t1

        with self.beat("same_cells"):
            self.until("*kembar*.")
            rings = VGroup(*[Square(C * 0.78, stroke_color=THEME.blue, stroke_width=9, fill_opacity=0)
                             .move_to(self.cells[k]).set_z_index(3) for k in same])
            self.play(LaggedStart(*[Create(r) for r in rings], lag_ratio=0.15), run_time=1.2)
            self.until("*6*")
            t2 = Tag("kembar: 6 kotak", fill=THEME.soft_blue, size=36).move_to([1.95, -2.25, 0])
            self.play(FadeIn(t2, shift=0.2 * UP), run_time=0.5)
            self.rings, self.t2 = rings, t2

        with self.beat("both"):
            self.until("(5,5)")
            self.play(*[Indicate(VGroup(self.cells[k], self.sums[k]), color=THEME.hl, scale_factor=1.25) for k in both],
                      run_time=1.0)
            self.until("*dua*", occurrence=2)  # 1st is "Perhatikan dua kotak ini"
            self.play(*[Circumscribe(self.cells[k], color=THEME.hl, buff=0.06) for k in both], run_time=1.0)

        with self.beat("twice"):
            self.play(FadeOut(self.t1), FadeOut(self.t2), run_time=0.3)
            eq = M("6", "+", "6", "=", "12", size=62).move_to([0, -2.25, 0])
            eq[0].set_color(THEME.warn)
            eq[2].set_color(THEME.blue)
            self.until("langsung")
            self.play(Write(eq), run_time=0.8)
            self.until("*dua~kali*.")
            marks = VGroup(*[T("x2", size=26, weight=BLACK, color=THEME.bad).next_to(self.cells[k], RIGHT, 0.02)
                             .shift(UP * 0.25).set_z_index(4) for k in both])
            self.play(FadeIn(marks, scale=1.4), eq[4].animate.set_color(THEME.bad), run_time=0.7)
            self.until("*satu~kali*.")
            self.play(*[Indicate(self.cells[k], color=THEME.good, scale_factor=1.15) for k in both], run_time=0.8)
            self.eq12, self.marks = eq, marks

        with self.beat("minus"):
            eq2 = M("6", "+", "6", "-", "2", "=", "10", size=66).move_to(self.eq12)
            eq2[0].set_color(THEME.warn)
            eq2[2].set_color(THEME.blue)
            eq2[4].set_color(THEME.bad)
            eq2[6].set_color(THEME.good)
            self.play(ReplacementTransform(self.eq12, eq2), FadeOut(self.marks), run_time=0.9)
            self.until("*10*")
            self.play(Circumscribe(eq2[6], color=THEME.good), run_time=0.8)
            self.eq10 = eq2

        with self.beat("compute"):
            board = VGroup(*self.cells.values(), *self.sums.values(), self.rings, self.headers)
            self.board = board
            self.play(board.animate.scale(0.55).move_to([0, 4.0, 0]), FadeOut(self.eq10), run_time=0.8)
            lhs = M("P", "=", size=70)
            f1 = Frac(10, 36, size=72)
            f1.num.set_color(THEME.good)
            f1.den.set_color(THEME.blue)
            eq = M("=", size=70)
            f2 = Frac(5, 18, size=72)
            VGroup(lhs, f1, eq, f2).arrange(RIGHT, buff=0.35).move_to([0, 0.0, 0])
            self.play(Write(lhs), Write(f1), run_time=0.9)
            self.until("Bagi")
            d1 = M(r"\div 2", size=40, color=THEME.purple).next_to(VGroup(f1.num, f2.num), UP, 0.2)
            d2 = M(r"\div 2", size=40, color=THEME.purple).next_to(VGroup(f1.den, f2.den), DOWN, 0.2)
            self.play(FadeIn(d1), FadeIn(d2), FadeIn(eq), run_time=0.6)
            self.play(TransformFromCopy(f1.num, f2.num), TransformFromCopy(f1.den, f2.den), Create(f2.bar),
                      run_time=0.9)
            self.until("*5/18*.")
            self.play(Circumscribe(f2, color=THEME.hl, buff=0.15), run_time=0.9)
            self.play(FadeOut(board), FadeOut(d1), FadeOut(d2), run_time=0.4)
            self.result = VGroup(lhs, f1, eq, f2)

    # --------------------------------------------------------------- check
    def check(self):
        coloured = sorted({(i, j) for i in range(1, 7) for j in range(1, 7) if i + j > 9 or i == j},
                          key=lambda k: (k[1], k[0]))
        with self.beat("check"):
            self.play(FadeOut(self.answer_group), run_time=0.5)
            self.board.scale(1 / 0.55).move_to(ORIGIN)
            self.board.shift(cell_center(3.5, 3.5) - VGroup(*self.cells.values()).get_center())
            self.play(FadeIn(self.board), run_time=0.7)
            counter = M("0", size=70, color=THEME.good).move_to([0, -2.25, 0])
            self.add(counter)
            badges = VGroup()
            self.until("1,")
            for n, k in enumerate(coloured, 1):
                b = Circle(radius=0.2, fill_color=THEME.good, fill_opacity=1, stroke_width=0).move_to(
                    self.cells[k].get_corner(UP + RIGHT) + [-0.17, -0.17, 0]).set_z_index(5)
                bt = T(str(n), size=20, weight=BLACK, color=THEME.hl_text).move_to(b).set_z_index(6)
                new = M(str(n), size=70, color=THEME.good).move_to(counter)
                self.play(FadeIn(VGroup(b, bt), scale=1.5), ReplacementTransform(counter, new), run_time=0.32)
                counter = new
                badges.add(VGroup(b, bt))
            self.until("Cocok!")
            self.play(Circumscribe(counter, color=THEME.hl), run_time=0.8)
            self.count_group = VGroup(self.board, badges, counter)

        with self.beat("trap"):
            self.play(FadeOut(self.count_group), run_time=0.5)
            card = Card(7.6, 4.2).move_to([0, 2.0, 0])
            title = T("Kalau terhitung dua kali:", size=42, weight=BLACK).move_to([0, 3.5, 0])
            row = M(r"\frac{12}{36} = \frac{1}{3}", size=70).move_to([-0.3, 1.9, 0])
            x = Badge(False, size=0.7).next_to(row, RIGHT, 0.4)
            note = T("tidak ada di pilihan", size=38, weight=BLACK, color=THEME.bad).move_to([0, 0.55, 0])
            self.play(FadeIn(card, shift=0.2 * UP), FadeIn(title), run_time=0.6)
            self.until("12/36")
            self.play(Write(row), run_time=0.8)
            self.until("*tidak*")
            self.play(GrowFromCenter(x), FadeIn(note), run_time=0.5)
            self.trap_group = VGroup(card, title, row, x, note)

