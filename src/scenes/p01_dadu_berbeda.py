"""Problem 1: two fair dice, faces known to differ; P(sum is prime) = 7/15.

Key visual idea: the 6x6 sample-space table. The condition deletes the
diagonal (36 -> 30 cells); equal sums lie on anti-diagonals, so the prime sums
3, 5, 7, 11 light up as whole lines (2 + 4 + 6 + 2 = 14 cells). The answer is
checked again on the half table of unordered pairs (7 of 15).

Render:  python scripts/render.py p01_dadu_berbeda
"""

import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[2]))

import numpy as np  # noqa: E402
from manim import (  # noqa: E402
    DOWN, LEFT, ORIGIN, PI, RIGHT, UP, AnimationGroup, Circumscribe, Create, DashedLine,
    FadeIn, FadeOut, FadeTransform, Flash, GrowFromCenter, Indicate, LaggedStart, Line,
    ReplacementTransform, RoundedRectangle, Square, TransformFromCopy, VGroup, Write,
    rate_functions,
)

from src.components.base import KinanScene  # noqa: E402
from src.components.cards import Badge, Card, Tag, TextCard, strike  # noqa: E402
from src.components.probability import Choices, Die  # noqa: E402
from src.components.text import BLACK, HEAVY, Frac, M, T  # noqa: E402
from src.components.theme import THEME  # noqa: E402

QUESTION = ("Dua dadu fair dilempar bersamaan. Diketahui kedua mata dadu berbeda. "
            "Peluang jumlah mata dadu merupakan bilangan prima adalah ...")
OPTIONS = [r"\frac{1}{3}", r"\frac{7}{15}", r"\frac{8}{15}", r"\frac{17}{30}"]
# drawing order inside the table: cells < labels < strike-throughs
Z_LABEL, Z_STRIKE = 2, 3
CORRECT = 1  # B

C = 0.9  # cell size
GX0, GY0 = -2.0, 3.1  # left edge and top edge of the 6x6 table
PRIMES = (2, 3, 5, 7, 11)
STRIP_Y = -3.0
TOP_Y = 5.3


def cell_center(i: int, j: int) -> np.ndarray:
    """Centre of the cell for die 1 = i (column) and die 2 = j (row)."""
    return np.array([GX0 + C * (i - 0.5), GY0 - C * (j - 0.5), 0])


def sum_line(s: int) -> list[tuple[int, int]]:
    return [(i, s - i) for i in range(1, 7) if 1 <= s - i <= 6]


class P01DaduBerbeda(KinanScene):
    problem_id = "p01_dadu_berbeda"

    def construct(self):
        self.hook()
        self.question()
        self.understand()
        self.sample_space()
        self.condition()
        self.sums_and_primes()
        self.count()
        self.answer()
        self.check()
        self.takeaway()

    # ------------------------------------------------------------- hook
    def hook(self):
        with self.beat("hook"):
            d1 = Die(2, size=1.7).move_to([-1.6, 2.4, 0])
            d2 = Die(5, size=1.7).move_to([1.6, 2.4, 0])
            for d, ang in ((d1, -0.5), (d2, 0.6)):
                d.save_state()
                d.shift(UP * 5).rotate(ang)
            self.play(d1.animate(rate_func=rate_functions.ease_out_bounce).restore(),
                      d2.animate(rate_func=rate_functions.ease_out_bounce).restore(), run_time=1.3)
            self.until("petunjuk")
            neq = M(r"\neq", size=120, color=THEME.bad).move_to([0, 2.4, 0])
            tag = Tag("petunjuk: mata dadu berbeda", fill=THEME.soft_red, size=38).move_to([0, 0.2, 0])
            self.play(GrowFromCenter(neq), FadeIn(tag, shift=0.2 * UP), run_time=0.7)
            self.until("Apakah")
            q = T("?", size=150, weight=BLACK, color=THEME.purple).move_to([0, 4.85, 0])
            self.play(FadeIn(q, scale=0.4), run_time=0.5)
            self.hook_group = VGroup(d1, d2, neq, tag, q)

    # ---------------------------------------------------------- question
    def question(self):
        with self.beat("question"):
            card = TextCard(QUESTION, width=8.0, size=42, max_chars=30, pad=0.42).move_to([0, 3.0, 0])
            self.play(FadeOut(self.hook_group, shift=0.3 * UP), run_time=0.5)
            self.play(FadeIn(card, shift=0.3 * UP), run_time=0.7)
            self.until("Diketahui")
            m1 = card.mark("kedua mata dadu berbeda")
            self.play(FadeIn(m1), run_time=0.5)
            self.bring_to_front(card.text)
            self.until("prima")
            m2 = card.mark("bilangan prima")
            self.play(FadeIn(m2), run_time=0.5)
            self.bring_to_front(card.text)
            self.qcard = VGroup(card.card, m1, m2, card.text)
        with self.beat("options"):
            choices = Choices(OPTIONS, width=8.0, height=1.45, size=50).move_to([0, -0.35, 0])
            self.play(LaggedStart(*[FadeIn(c, shift=0.2 * UP) for c in choices], lag_ratio=0.15),
                      run_time=0.9)
            for i, token in enumerate(("1/3", "7/15", "8/15", "17/30")):
                self.until(token)
                self.play(Indicate(choices[i], color=THEME.purple, scale_factor=1.08), run_time=0.5)
            self.choices = choices

    # ------------------------------------------------------- understand
    def understand(self):
        with self.beat("keyword"):
            self.play(FadeOut(self.choices), self.qcard.animate.scale(0.8).move_to([0, 4.5, 0]),
                      run_time=0.7)
            self.until("diketahui")
            tag = Tag("SYARAT: kedua mata dadu berbeda", fill=THEME.soft_red, size=38)
            tag.move_to([0, 2.0, 0])
            self.play(TransformFromCopy(self.qcard[1], tag[0]), FadeIn(tag[1]), run_time=0.9)
            self.until("mempersempit")
            self.play(Indicate(tag, color=THEME.bad, scale_factor=1.06), run_time=0.8)
            self.cond_tag = tag
        with self.beat("idea"):
            lhs = T("Peluang =", size=50, weight=BLACK).move_to([-2.45, -0.5, 0])
            num = T("hasil yang cocok", size=44, color=THEME.good, weight=BLACK)
            den = T("hasil yang masih mungkin", size=44, color=THEME.bad, weight=BLACK)
            bar = Line(LEFT, RIGHT).set_stroke(THEME.ink, 7)
            bar.set_width(max(num.width, den.width) + 0.3)
            frac = VGroup(num, bar, den).arrange(DOWN, buff=0.25)
            frac.next_to(lhs, RIGHT, buff=0.35)
            VGroup(lhs, frac).move_to([0, -0.4, 0])
            self.play(FadeIn(lhs), Create(bar), run_time=0.6)
            self.until("cocok")
            self.play(Write(num), run_time=0.7)
            self.until("masih~mungkin")
            self.play(Write(den), run_time=0.8)
            self.idea = VGroup(lhs, frac)

    # ----------------------------------------------------- sample space
    def sample_space(self):
        with self.beat("axes"):
            self.play(FadeOut(self.qcard), FadeOut(self.idea), FadeOut(self.cond_tag), run_time=0.6)
            top = VGroup(*[Die(i, size=0.6) for i in range(1, 7)])
            for i, d in enumerate(top, 1):
                d.move_to([cell_center(i, 1)[0], GY0 + 0.5, 0])
            side = VGroup(*[Die(j, size=0.6) for j in range(1, 7)])
            for j, d in enumerate(side, 1):
                d.move_to([GX0 - 0.5, cell_center(1, j)[1], 0])
            lab1 = T("Dadu 1", size=34, color=THEME.blue, weight=BLACK).move_to([cell_center(3.5, 1)[0], GY0 + 1.15, 0])
            lab2 = T("Dadu 2", size=34, color=THEME.warn, weight=BLACK).rotate(PI / 2)
            lab2.move_to([GX0 - 1.2, cell_center(1, 3.5)[1], 0])
            for d in top:
                d.body.set_stroke(THEME.blue)
            for d in side:
                d.body.set_stroke(THEME.warn)
            self.play(FadeIn(lab1), LaggedStart(*[FadeIn(d, shift=0.3 * DOWN) for d in top], lag_ratio=0.12),
                      run_time=1.2)
            self.until("kedua")
            self.play(FadeIn(lab2), LaggedStart(*[FadeIn(d, shift=0.3 * RIGHT) for d in side], lag_ratio=0.12),
                      run_time=1.2)
            self.headers = VGroup(top, side, lab1, lab2)

        with self.beat("cells"):
            self.cells, self.labels = {}, {}
            for j in range(1, 7):
                for i in range(1, 7):
                    sq = Square(C, fill_color=THEME.card, fill_opacity=1,
                                stroke_color=THEME.ink, stroke_width=3).move_to(cell_center(i, j))
                    lab = T(f"{i},{j}", size=30, color=THEME.ink, weight=HEAVY).move_to(sq)
                    lab.set_z_index(Z_LABEL)
                    self.cells[i, j], self.labels[i, j] = sq, lab
            # demonstrate one pair first, then fill the table row by row
            demo = (2, 5)
            self.play(Indicate(self.headers[0][demo[0] - 1], color=THEME.blue),
                      Indicate(self.headers[1][demo[1] - 1], color=THEME.warn), run_time=0.6)
            self.play(FadeIn(self.cells[demo], scale=0.6), FadeIn(self.labels[demo]), run_time=0.5)
            rest = [(i, j) for j in range(1, 7) for i in range(1, 7) if (i, j) != demo]
            self.play(LaggedStart(*[AnimationGroup(FadeIn(self.cells[k], scale=0.6), FadeIn(self.labels[k]))
                                    for k in rest], lag_ratio=0.04), run_time=2.2)
            self.until("6~×~6")
            self.counter = M(r"6 \times 6 = 36", size=56).move_to([2.0, TOP_Y, 0])
            self.play(Write(self.counter), run_time=0.8)
            self.until("sama~mungkin")
            self.play(LaggedStart(*[Indicate(self.cells[k], color=THEME.soft_blue, scale_factor=1.0)
                                    for k in sorted(self.cells)], lag_ratio=0.01), run_time=1.0)

    # -------------------------------------------------------- condition
    def condition(self):
        diag = [(k, k) for k in range(1, 7)]
        with self.beat("doubles"):
            self.until("berbeda")
            self.syarat = Tag("mata dadu berbeda", fill=THEME.soft_red, size=40).move_to([-2.1, TOP_Y, 0])
            self.play(FadeIn(self.syarat, shift=0.2 * DOWN), run_time=0.5)
            self.until("kembar")
            self.play(LaggedStart(*[self.cells[k].animate.set_fill(THEME.soft_red) for k in diag],
                                  lag_ratio=0.2), run_time=1.4)
            self.until("tidak~mungkin")
            self.strikes = VGroup(*[strike(self.cells[k], width=6).scale(0.8) for k in diag])
            self.strikes.set_z_index(Z_STRIKE)
            self.play(LaggedStart(*[Create(s) for s in self.strikes], lag_ratio=0.15),
                      *[self.labels[k].animate.set_color(THEME.muted) for k in diag], run_time=1.2)
        with self.beat("shrink"):
            new = M(r"36 - 6 = 30", size=56).move_to(self.counter)
            self.until("menyusut")
            self.play(ReplacementTransform(self.counter, new), run_time=0.8)
            self.counter = new
            self.until("30")
            box = Card(2.6, 1.0, fill=THEME.soft_blue, radius=0.18, stroke_width=4)
            n30 = VGroup(box, M("n(S) = 30", size=50).move_to(box.body))
            n30.move_to([2.0, TOP_Y, 0])
            self.play(FadeTransform(self.counter, n30), Flash(n30, color=THEME.blue), run_time=0.8)
            self.counter = n30

    # ------------------------------------------------- sums and primes
    def sums_and_primes(self):
        diag = {(k, k) for k in range(1, 7)}
        self.sum_labels = {}
        with self.beat("sums"):
            self.until("ganti")
            anims = []
            order = sorted(self.labels, key=lambda k: (k[0] + k[1], k[0]))
            for k in order:
                s = T(str(k[0] + k[1]), size=40, weight=BLACK,
                      color=THEME.muted if k in diag else THEME.ink).move_to(self.cells[k])
                s.set_z_index(Z_LABEL)
                self.sum_labels[k] = s
                anims.append(ReplacementTransform(self.labels[k], s))
            self.play(LaggedStart(*anims, lag_ratio=0.05), run_time=2.6)
        with self.beat("pattern"):
            self.until("miring")
            line7 = sum_line(7)
            a, b = cell_center(*line7[0]), cell_center(*line7[-1])
            band = RoundedRectangle(width=np.linalg.norm(b - a) + C * 0.9, height=C * 0.82,
                                    corner_radius=C * 0.4, stroke_color=THEME.warn, stroke_width=8,
                                    fill_opacity=0)
            band.rotate(np.arctan2(*(b - a)[1::-1])).move_to((a + b) / 2)
            self.play(Create(band), run_time=1.0)
            self.until("7")
            self.play(LaggedStart(*[Indicate(self.sum_labels[k], color=THEME.warn, scale_factor=1.4)
                                    for k in line7], lag_ratio=0.12), run_time=1.2)
            self.play(FadeOut(band), run_time=0.4)

        with self.beat("primes"):
            strip = VGroup()
            for n in range(2, 13):
                box = RoundedRectangle(width=0.6, height=0.62, corner_radius=0.12, fill_color=THEME.card,
                                       fill_opacity=1, stroke_color=THEME.ink, stroke_width=3)
                strip.add(VGroup(box, T(str(n), size=32, weight=BLACK).move_to(box)))
            strip.arrange(RIGHT, buff=0.07).move_to([0.2, STRIP_Y, 0])
            self.play(LaggedStart(*[FadeIn(b, shift=0.15 * UP) for b in strip], lag_ratio=0.06), run_time=1.0)
            for p, tok, occ in ((2, "2", 2), (3, "3", 1), (5, "5", 1), (7, "7", 1), (11, "11", 1)):
                self.until(tok, occurrence=occ)
                cell = strip[p - 2]
                self.play(cell[0].animate.set_fill(THEME.good), cell[1].animate.set_color(THEME.card),
                          run_time=0.35)
            self.strip = strip
        with self.beat("two"):
            self.until("(1,1):")
            self.play(Indicate(self.cells[1, 1], color=THEME.bad, scale_factor=1.25), run_time=0.9)
            self.until("dicoret")
            two = self.strip[0]
            x = strike(two, width=6)
            self.play(two[0].animate.set_fill(THEME.soft_red), two[1].animate.set_color(THEME.bad),
                      Create(x), run_time=0.6)
            self.strip.add(x)

    # ------------------------------------------------------------ count
    def count(self):
        diag = {(k, k) for k in range(1, 7)}
        groups = {s: [k for k in sum_line(s) if k not in diag] for s in (3, 5, 7, 11)}
        with self.beat("light"):
            for s in (3, 5, 7, 11):
                self.until(str(s))
                self.play(*[self.cells[k].animate.set_fill(THEME.soft_green).set_stroke(THEME.good)
                            for k in groups[s]],
                          *[self.sum_labels[k].animate.set_color(THEME.good) for k in groups[s]],
                          run_time=0.45)
        with self.beat("count"):
            tally = M("2", "+", "4", "+", "6", "+", "2", "=", "14", size=60).move_to([0.2, STRIP_Y, 0])
            tally[-1].set_color(THEME.good)
            self.play(FadeOut(self.strip, shift=0.2 * DOWN), run_time=0.4)
            parts = [(3, 0, None), (5, 2, 1), (7, 4, 3), (11, 6, 5)]
            for idx, (s, term, plus) in enumerate(parts):
                self.until(["2", "4", "6", "2"][idx], occurrence=2 if idx == 3 else 1)
                anims = [Write(tally[term])] + ([FadeIn(tally[plus])] if plus is not None else [])
                self.play(*anims, *[Indicate(self.cells[k], color=THEME.good, scale_factor=1.12)
                                    for k in groups[s]], run_time=0.55)
            self.until("14")
            self.play(FadeIn(tally[7]), Write(tally[8]), run_time=0.6)
            self.play(Circumscribe(tally[8], color=THEME.good, buff=0.1), run_time=0.8)
            self.tally = tally
        with self.beat("fraction"):
            board = VGroup(*self.cells.values(), *self.sum_labels.values(), self.strikes, self.headers)
            self.board = board
            self.play(board.animate.scale(0.55).move_to([0, 3.15, 0]),
                      FadeOut(self.syarat), run_time=0.9)
            p = M(r"P(\text{prima}\mid\text{berbeda})", size=52)
            eq1, eq2 = M("=", size=60), M("=", size=60)
            f1 = Frac(14, 30, size=66)
            f1.num.set_color(THEME.good)
            f1.den.set_color(THEME.blue)
            f2 = Frac(7, 15, size=66)
            row = VGroup(p, eq1, f1, eq2, f2).arrange(RIGHT, buff=0.3).move_to([0, -1.3, 0])
            self.play(FadeIn(p), FadeIn(eq1), Create(f1.bar), run_time=0.6)
            self.play(TransformFromCopy(self.tally[8], f1.num),
                      TransformFromCopy(self.counter[1], f1.den), run_time=1.0)
            self.play(FadeOut(self.tally), FadeOut(self.counter), run_time=0.4)
            self.until("Bagi")
            d_top = M(r"\div 2", size=36, color=THEME.purple).next_to(VGroup(f1.num, f2.num), UP, 0.15)
            d_bot = M(r"\div 2", size=36, color=THEME.purple).next_to(VGroup(f1.den, f2.den), DOWN, 0.15)
            self.play(FadeIn(d_top), FadeIn(d_bot), FadeIn(eq2), run_time=0.6)
            self.play(TransformFromCopy(f1.num, f2.num), TransformFromCopy(f1.den, f2.den),
                      Create(f2.bar), run_time=0.9)
            self.until("7/15")
            self.play(Circumscribe(f2, color=THEME.good, buff=0.15), run_time=0.9)
            self.result = VGroup(p, eq1, f1, eq2, f2, d_top, d_bot)

    # ----------------------------------------------------------- answer
    def answer(self):
        with self.beat("answer"):
            choices = Choices(OPTIONS, width=8.0, height=1.45, size=50).move_to([0, -3.0 + 0.0, 0])
            self.play(FadeOut(self.board), self.result.animate.move_to([0, 3.2, 0]), run_time=0.7)
            choices.move_to([0, 0.9, 0])
            self.play(FadeIn(choices, shift=0.2 * UP), run_time=0.5)
            self.until("B,")
            self.play(*[choices[i].animate.set_opacity(0.3) for i in range(4) if i != CORRECT],
                      choices[CORRECT].animate.scale(1.12), run_time=0.6)
            badge = choices.mark(CORRECT)
            self.play(choices[CORRECT][0].body.animate.set_fill(THEME.soft_green),
                      GrowFromCenter(badge), run_time=0.5)
            self.answer_group = VGroup(choices, badge)

    # ------------------------------------------------------------ check
    def check(self):
        upper = [(i, j) for i in range(1, 7) for j in range(1, 7) if i > j]
        lower = [(i, j) for i in range(1, 7) for j in range(1, 7) if i < j]
        with self.beat("symmetry"):
            self.play(FadeOut(self.answer_group), FadeOut(self.result), run_time=0.5)
            self.board.scale(1 / 0.55).move_to(ORIGIN)
            # restore the board at full size in its original place
            self.board.shift(cell_center(3.5, 3.5) - VGroup(*self.cells.values()).get_center())
            self.play(FadeIn(self.board), run_time=0.7)
            self.until("simetris")
            a, b = self.cells[1, 1].get_corner(UP + LEFT), self.cells[6, 6].get_corner(DOWN + RIGHT)
            mirror = DashedLine(a, b, dash_length=0.18).set_stroke(THEME.purple, 6)
            self.play(Create(mirror), run_time=0.8)
            pairs = VGroup(*[VGroup(self.cells[k], self.sum_labels[k]) for k in lower])
            self.play(Indicate(VGroup(*[self.cells[k] for k in upper]), color=THEME.purple,
                               scale_factor=1.0),
                      Indicate(VGroup(*[self.cells[k] for k in lower]), color=THEME.purple,
                               scale_factor=1.0), run_time=0.9)
            self.until("setengahnya:")
            self.play(pairs.animate.set_opacity(0.12), run_time=0.8)
            self.until("15")
            n15 = Tag("15 pasangan", fill=THEME.soft_blue, size=40).move_to([2.0, TOP_Y, 0])
            self.play(FadeIn(n15, shift=0.2 * DOWN), run_time=0.5)
            self.mirror, self.n15 = mirror, n15
        with self.beat("half"):
            good = [k for k in upper if (k[0] + k[1]) in PRIMES]
            self.until("7", occurrence=1)
            self.play(LaggedStart(*[Indicate(self.cells[k], color=THEME.good, scale_factor=1.2)
                                    for k in good], lag_ratio=0.12), run_time=1.3)
            f = Frac(7, 15, size=60).move_to([-2.0, TOP_Y - 0.05, 0])
            f.num.set_color(THEME.good)
            self.play(FadeIn(f, shift=0.2 * DOWN), run_time=0.5)
            self.until("sama")
            badge = Badge(True, size=0.6).next_to(f, RIGHT, 0.2)
            self.play(GrowFromCenter(badge), run_time=0.4)
            self.check_group = VGroup(self.board, self.mirror, self.n15, f, badge)
        with self.beat("trap"):
            self.play(FadeOut(self.check_group), run_time=0.6)
            card = Card(7.6, 4.6, fill=THEME.card).move_to([0, 1.6, 0])
            title = T("Tanpa memakai syarat:", size=44, weight=BLACK).move_to([0, 3.3, 0])
            f1, f2 = Frac(15, 36, size=70), Frac(5, 12, size=70)
            eq = M("=", size=66)
            row = VGroup(f1, eq, f2).arrange(RIGHT, buff=0.35).move_to([-0.3, 1.6, 0])
            x = Badge(False, size=0.7).next_to(row, RIGHT, 0.4)
            note = T("tidak ada di pilihan", size=38, color=THEME.bad, weight=BLACK).move_to([0, 0.0, 0])
            self.play(FadeIn(card, shift=0.2 * UP), FadeIn(title), run_time=0.6)
            self.until("15/36")
            self.play(Write(f1), run_time=0.8)
            self.until("5/12.")
            self.play(FadeIn(eq), Write(f2), run_time=0.7)
            self.until("Tidak")
            self.play(GrowFromCenter(x), FadeIn(note), run_time=0.5)
            self.trap = VGroup(card, title, row, x, note)

    # --------------------------------------------------------- takeaway
    def takeaway(self):
        with self.beat("takeaway"):
            self.play(FadeOut(self.trap), run_time=0.5)
            card = Card(8.0, 6.6).move_to([0, 2.2, 0])
            head = T("Peluang bersyarat", size=50, weight=BLACK, color=THEME.purple).move_to([0, 4.85, 0])
            s1 = VGroup(Badge(True, size=0.55), T("1. Coret yang tidak mungkin", size=38, weight=BLACK))
            s1.arrange(RIGHT, buff=0.25)
            v1 = M(r"36 \to 30", size=50, color=THEME.bad)
            s2 = VGroup(Badge(True, size=0.55), T("2. Hitung yang cocok", size=38, weight=BLACK))
            s2.arrange(RIGHT, buff=0.25)
            v2 = M(r"14", size=50, color=THEME.good)
            res = VGroup(M("P =", size=56), Frac(14, 30, size=56), M("=", size=56), Frac(7, 15, size=56))
            res.arrange(RIGHT, buff=0.25)
            for s, v, y in ((s1, v1, 3.5), (s2, v2, 2.2)):
                s.move_to([-0.75, y, 0]).align_to([-3.6, 0, 0], LEFT)
                v.move_to([2.85, y, 0])
            res.move_to([0, 0.35, 0])
            self.play(FadeIn(card, shift=0.2 * UP), FadeIn(head), run_time=0.6)
            self.until("Coret")
            self.play(FadeIn(s1, shift=0.2 * RIGHT), FadeIn(v1), run_time=0.6)
            self.until("hitung")
            self.play(FadeIn(s2, shift=0.2 * RIGHT), FadeIn(v2), run_time=0.6)
            self.play(Write(res), run_time=1.0)
            self.play(Circumscribe(res[-1], color=THEME.good, buff=0.12), run_time=0.9)
