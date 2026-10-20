"""Soal 2 (Bagian 1): spinner 1-6 dan koin, peluang ganjil DAN gambar = 3/12 = 1/4.

Beginner path: what a spinner is (equal sectors, as drawn) -> ganjil = 1, 3, 5 -> gambar ->
"dan" = both at once -> examples -> 6 x 2 table of 12 pairs -> odd columns ∩ row G = 3 cells ->
3/12 = 1/4 -> check with an area model (1/2 of 1/2).

Assumption (stated in the video): the six sectors are equal, as shown on the worksheet.

Render:  python scripts/render.py p05_spinner_koin
"""

import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[2]))

from manim import (  # noqa: E402
    DOWN, LEFT, RIGHT, UP, Circle, Circumscribe, Create, FadeIn, FadeOut, GrowFromCenter, Indicate,
    LaggedStart, Rectangle, Rotate, Square, SurroundingRectangle, TransformFromCopy, VGroup, Write,
)

from src.components.base import KinanScene  # noqa: E402
from src.components.cards import Badge, Tag  # noqa: E402
from src.components.lesson import LessonMixin  # noqa: E402
from src.components.probability import Coin, Spinner  # noqa: E402
from src.components.text import BLACK, Frac, M, T  # noqa: E402
from src.components.theme import THEME  # noqa: E402

QUESTION = ("Sebuah spinner bernomor 1 sampai 6 dan sebuah koin dilempar bersamaan. Peluang muncul "
            "bilangan ganjil pada spinner dan sisi gambar pada koin adalah ...")
OPTIONS = [r"\frac{1}{6}", r"\frac{1}{4}", r"\frac{1}{3}", r"\frac{1}{2}"]
CORRECT = 1  # B
ODD = (1, 3, 5)
C = 1.0  # table cell size
X0, ROW_G, ROW_A, HEAD_Y = -2.5, 2.1, 1.0, 3.25


def num_chip(n: int, r: float = 0.32, color=None) -> VGroup:
    disc = Circle(radius=r, fill_color=color or THEME.purple, fill_opacity=1, stroke_color=THEME.ink, stroke_width=3)
    return VGroup(disc, T(str(n), size=r * 120 * 0.85, weight=BLACK, color=THEME.hl_text).move_to(disc))


class P05SpinnerKoin(LessonMixin, KinanScene):
    problem_id = "p05_spinner_koin"

    def construct(self):
        icon = VGroup(Spinner(6, radius=0.8), Coin("G", radius=0.5)).arrange(RIGHT, buff=0.6)
        self.read_question("question", "options", QUESTION, OPTIONS,
                           [("*ganjil*", "bilangan ganjil pada spinner"), ("*gambar*", "sisi gambar pada koin")],
                           ["1/6,", "1/4,", "1/3,", "1/2."], icon=icon, size=40, max_chars=32)
        self.understand()
        self.examples()
        self.solve()
        self.reveal_answer("answer", OPTIONS, CORRECT, "B,", result=self.result)
        self.check()
        self.play(FadeOut(self.check_group), run_time=0.5)
        self.summary_card("remember", "Yang perlu diingat", [
            T("1. Kejadian 'dan' = kotak yang", size=38, weight=BLACK),
            T("    memenuhi kedua syarat", size=38, weight=BLACK),
            T("2. Tidak saling memengaruhi: kalikan", size=38, weight=BLACK),
            M(r"\tfrac{1}{2} \times \tfrac{1}{2} = \tfrac{1}{4}", size=60, color=THEME.good),
        ], ["*dan*", None, "Tidak", "*dikalikan*."])

    # ------------------------------------------------------------ meaning
    def understand(self):
        with self.beat("spinner"):
            self.clear_question()
            sp = Spinner(6, radius=2.2).move_to([0, 2.2, 0])
            self.play(GrowFromCenter(sp), run_time=0.8)
            self.until("diputar;")
            self.play(Rotate(sp.needle, angle=sp.turn_to(4, 2), about_point=sp.get_center()), run_time=2.2)
            self.sp = sp

        with self.beat("equal"):
            self.until("*sama~besar*,")
            self.play(LaggedStart(*[Indicate(s, color=THEME.ink, scale_factor=1.06) for s in self.sp.sectors],
                                  lag_ratio=0.2), run_time=1.8)
            note = T("6 bagian sama besar", size=38, weight=BLACK, color=THEME.hl).move_to([0, -0.6, 0])
            self.play(FadeIn(note, shift=0.2 * UP), run_time=0.5)
            self.note = note

        with self.beat("odd"):
            self.play(FadeOut(self.note), run_time=0.3)
            self.until("1,")
            evens = [k for k in range(1, 7) if k not in ODD]
            self.play(*[self.sp.sectors[k - 1].animate.set_fill(opacity=0.18) for k in evens],
                      *[self.sp.labels[k - 1].animate.set_opacity(0.35) for k in evens], run_time=0.7)
            tag = Tag("ganjil: 1, 3, 5", fill=THEME.soft_blue, size=40).move_to([0, -0.6, 0])
            self.play(FadeIn(tag, shift=0.2 * UP), *[Indicate(self.sp.labels[k - 1], scale_factor=1.4) for k in ODD],
                      run_time=0.9)
            self.odd_tag = tag

        with self.beat("coin"):
            self.play(VGroup(self.sp, self.odd_tag).animate.scale(0.6).move_to([-2.0, 3.6, 0]), run_time=0.7)
            g, a = Coin("G", radius=0.65), Coin("A", radius=0.65)
            pair = VGroup(g, a).arrange(RIGHT, buff=0.6).move_to([2.0, 3.8, 0])
            lg = T("gambar", size=30, weight=BLACK, color=THEME.hl).next_to(g, DOWN, 0.2)
            la = T("angka", size=30, weight=BLACK, color=THEME.blue).next_to(a, DOWN, 0.2)
            self.play(GrowFromCenter(g), GrowFromCenter(a), FadeIn(lg), FadeIn(la), run_time=0.7)
            self.until("*gambar*.", occurrence=2)  # 1st "gambar" is in "gambar (G) dan angka (A)"
            ring = Circle(radius=0.8, stroke_color=THEME.hl, stroke_width=7).move_to(g)
            self.play(Create(ring), a.animate.set_opacity(0.35), la.animate.set_opacity(0.35), run_time=0.6)
            self.coins = VGroup(g, a, lg, la, ring)

        with self.beat("and"):
            t1 = Tag("spinner ganjil", fill=THEME.soft_blue, size=40)
            dan = T("DAN", size=60, weight=BLACK, color=THEME.hl)
            t2 = Tag("koin gambar", fill=THEME.soft_yellow, size=40)
            row = VGroup(t1, dan, t2).arrange(DOWN, buff=0.35).move_to([0, 0.4, 0])
            self.until("*dan*")
            self.play(FadeIn(t1, shift=0.2 * DOWN), Write(dan), FadeIn(t2, shift=0.2 * UP), run_time=0.9)
            self.play(Indicate(dan, color=THEME.hl, scale_factor=1.3), run_time=0.7)
            self.and_row = row

    def examples(self):
        with self.beat("examples"):
            self.play(FadeOut(self.and_row), run_time=0.4)
            rows = VGroup()
            for k, (n, f, ok, cue) in enumerate(((3, "G", True, "*cocok!*"), (3, "A", False, "angka:"),
                                                 (4, "G", False, "4"))):
                chip = num_chip(n, r=0.4, color=THEME.blue if n % 2 else THEME.faint)
                c = Coin(f, radius=0.4)
                b = Badge(ok, size=0.6)
                r = VGroup(chip, c, b).arrange(RIGHT, buff=0.5).move_to([0, 1.2 - 1.15 * k, 0])
                self.until(cue)
                self.play(FadeIn(r, shift=0.2 * RIGHT), run_time=0.6)
                rows.add(r)
            self.example_rows = rows

    # --------------------------------------------------------------- solve
    def solve(self):
        cells = {}
        with self.beat("table"):
            self.play(FadeOut(VGroup(self.example_rows, self.coins, self.sp, self.odd_tag)), run_time=0.5)
            heads = VGroup(*[num_chip(n, r=0.33, color=self.sp.sectors[n - 1].get_fill_color())
                             .move_to([X0 + (n - 1) * C, HEAD_Y, 0]) for n in range(1, 7)])
            side = VGroup(Coin("G", radius=0.33).move_to([X0 - 1.0, ROW_G, 0]),
                          Coin("A", radius=0.33).move_to([X0 - 1.0, ROW_A, 0]))
            lab_s = T("spinner", size=30, weight=BLACK, color=THEME.purple).move_to([0, HEAD_Y + 0.65, 0])
            lab_k = T("koin", size=30, weight=BLACK, color=THEME.purple).rotate(1.5708).move_to([X0 - 1.75, (ROW_G + ROW_A) / 2, 0])
            self.until("enam")
            self.play(FadeIn(lab_s), LaggedStart(*[GrowFromCenter(h) for h in heads], lag_ratio=0.1), run_time=1.0)
            self.until("dua")
            self.play(FadeIn(lab_k), LaggedStart(*[GrowFromCenter(s) for s in side], lag_ratio=0.2), run_time=0.7)
            for n in range(1, 7):
                for face, y in (("G", ROW_G), ("A", ROW_A)):
                    sq = Square(C * 0.94, fill_color=THEME.card, fill_opacity=1, stroke_color=THEME.faint,
                                stroke_width=3).move_to([X0 + (n - 1) * C, y, 0])
                    lab = T(f"{n},{face}", size=28, weight=BLACK).move_to(sq).set_z_index(2)
                    cells[n, face] = VGroup(sq, lab)
            self.play(LaggedStart(*[FadeIn(cells[k], scale=0.6) for k in sorted(cells)], lag_ratio=0.05), run_time=1.4)
            self.cells, self.heads, self.side, self.labs = cells, heads, side, VGroup(lab_s, lab_k)

        with self.beat("twelve"):
            self.until("6~×~2")
            eq = M(r"6 \times 2 = 12", size=62).move_to([0, -0.3, 0])
            self.play(Write(eq), run_time=0.8)
            self.until("mungkin.")
            self.play(LaggedStart(*[Indicate(cells[k][0], color=THEME.blue, scale_factor=1.0) for k in sorted(cells)],
                                  lag_ratio=0.03), run_time=1.0)
            self.eq12 = eq

        with self.beat("cols"):
            self.until("*ganjil*:")
            self.play(*[cells[n, f][0].animate.set_fill(THEME.soft_blue).set_stroke(THEME.blue, 4)
                        for n in ODD for f in "GA"],
                      *[Indicate(self.heads[n - 1], scale_factor=1.3) for n in ODD], run_time=0.9)

        with self.beat("row"):
            self.until("*gambar*.")
            box = SurroundingRectangle(VGroup(*[cells[n, "G"] for n in range(1, 7)], self.side[0]), color=THEME.hl,
                                       buff=0.08, corner_radius=0.15, stroke_width=7)
            self.play(Create(box), run_time=0.7)
            self.until("*3*.")
            self.play(*[cells[n, "G"][0].animate.set_fill(THEME.soft_green).set_stroke(THEME.good, 6) for n in ODD],
                      *[Indicate(cells[n, "G"][1], color=THEME.good, scale_factor=1.5) for n in ODD], run_time=0.9)
            n3 = Tag("3 kotak cocok", fill=THEME.soft_green, size=40).move_to([0, -0.3, 0])
            self.play(FadeOut(self.eq12), FadeIn(n3), run_time=0.5)
            self.box, self.n3 = box, n3

        with self.beat("compute"):
            table = VGroup(*self.cells.values(), self.heads, self.side, self.labs, self.box)
            self.play(table.animate.scale(0.62).move_to([0, 3.9, 0]), FadeOut(self.n3), run_time=0.7)
            lhs = M("P", "=", size=70)
            f1 = Frac(3, 12, size=72)
            f1.num.set_color(THEME.good)
            f1.den.set_color(THEME.blue)
            eq = M("=", size=70)
            f2 = Frac(1, 4, size=72)
            VGroup(lhs, f1, eq, f2).arrange(RIGHT, buff=0.35).move_to([0, 0.4, 0])
            self.play(Write(lhs), Write(f1), run_time=0.9)
            self.until("Bagi")
            d1 = M(r"\div 3", size=40, color=THEME.purple).next_to(VGroup(f1.num, f2.num), UP, 0.2)
            d2 = M(r"\div 3", size=40, color=THEME.purple).next_to(VGroup(f1.den, f2.den), DOWN, 0.2)
            self.play(FadeIn(d1), FadeIn(d2), FadeIn(eq), run_time=0.6)
            self.play(TransformFromCopy(f1.num, f2.num), TransformFromCopy(f1.den, f2.den), Create(f2.bar),
                      run_time=0.9)
            self.until("*1/4*.")
            self.play(Circumscribe(f2, color=THEME.hl, buff=0.15), run_time=0.9)
            self.play(FadeOut(table), FadeOut(d1), FadeOut(d2), run_time=0.4)
            self.result = VGroup(lhs, f1, eq, f2)

    # --------------------------------------------------------------- check
    def check(self):
        size = 4.4
        with self.beat("check1"):
            self.play(FadeOut(self.answer_group), run_time=0.5)
            sq = Square(size, stroke_color=THEME.ink, stroke_width=5).move_to([0, 2.1, 0])
            title = T("semua kemungkinan", size=32, weight=BLACK, color=THEME.muted).next_to(sq, UP, 0.2)
            self.play(Create(sq), FadeIn(title), run_time=0.8)
            self.until("*1/2*.")
            half = Rectangle(width=size / 2, height=size, fill_color=THEME.blue, fill_opacity=0.55,
                             stroke_width=0).align_to(sq, LEFT).align_to(sq, UP)
            lh = M(r"\text{ganjil} = \tfrac{1}{2}", size=46, color=THEME.blue).next_to(sq, DOWN, 0.25).align_to(sq, LEFT)
            self.play(FadeIn(half), Write(lh), run_time=0.8)
            self.area = VGroup(sq, title, half, lh)

        with self.beat("check2"):
            self.until("1/2.")
            q = Rectangle(width=size / 2, height=size / 2, fill_color=THEME.good, fill_opacity=0.85,
                          stroke_color=THEME.ink, stroke_width=4).align_to(self.area[0], LEFT).align_to(self.area[0], UP)
            lq = M(r"\text{gambar}", size=40, color=THEME.hl_text).move_to(q)
            self.play(FadeIn(q), FadeIn(lq), run_time=0.8)
            self.until("*1/4*.")
            eq = M(r"\tfrac{1}{2} \times \tfrac{1}{2} = \tfrac{1}{4}", size=62, color=THEME.good).move_to([0, -1.25, 0])
            self.play(Write(eq), run_time=0.9)
            self.play(Circumscribe(q, color=THEME.hl), run_time=0.8)
            self.area.add(q, lq, eq)

        with self.beat("check3"):
            self.until("memengaruhi*.")
            tag = Tag("tidak saling memengaruhi", fill=THEME.soft_purple, size=36).move_to([0, -2.4, 0])
            self.play(FadeIn(tag, shift=0.2 * UP), run_time=0.6)
            self.check_group = VGroup(self.area, tag)
