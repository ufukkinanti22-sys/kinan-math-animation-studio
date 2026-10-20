"""Soal 4 (Bagian 2): spinner 8 sektor sama besar, diputar 144 kali; frekuensi harapan
bilangan prima = 4/8 x 144 = 72.

Beginner path: what "frekuensi harapan" means -> warm-up: a coin 10 times -> rule
F_h = peluang x banyak percobaan -> what a prime is, checked 1..8 (1 is NOT prime) ->
P = 4/8 = 1/2 -> 1/2 x 144 = 72 -> picture of 144 spins -> it is an estimate -> the 90 trap.

Render:  python scripts/render.py p07_spinner_harapan
"""

import random
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[2]))

from manim import (  # noqa: E402
    DOWN, LEFT, RIGHT, UP, Brace, Circumscribe, Create, Dot, FadeIn, FadeOut, GrowFromCenter, Indicate,
    LaggedStart, Line, NumberLine, ReplacementTransform, Rotate, Triangle, VGroup, Write,
)

from src.components.base import KinanScene  # noqa: E402
from src.components.cards import Badge, Card, Tag, strike  # noqa: E402
from src.components.lesson import LessonMixin  # noqa: E402
from src.components.probability import Coin, Spinner  # noqa: E402
from src.components.text import BLACK, HEAVY, Frac, M, T  # noqa: E402
from src.components.theme import THEME  # noqa: E402

QUESTION = ("Sebuah spinner dengan 8 sektor sama besar bernomor 1 sampai 8 diputar 144 kali. "
            "Frekuensi harapan muncul bilangan prima adalah ...")
OPTIONS = ["54", "64", "72", "81"]
CORRECT = 2  # C
PRIMES = (2, 3, 5, 7)
DIVISORS = {n: [d for d in range(1, n + 1) if n % d == 0] for n in range(1, 9)}


class P07SpinnerHarapan(LessonMixin, KinanScene):
    problem_id = "p07_spinner_harapan"

    def construct(self):
        self.read_question("question", "options", QUESTION, OPTIONS,
                           [("*sama~besar*,", "8 sektor sama besar"), ("*144*", "diputar 144 kali."),
                            ("*frekuensi~harapan*", "Frekuensi harapan"), ("*prima*?", "bilangan prima")],
                           ["54,", "64,", "72,", "81."], icon=Spinner(8, radius=0.95), size=40, max_chars=32)
        self.meaning()
        self.warm_up()
        self.solve()
        self.reveal_answer("answer", OPTIONS, CORRECT, "C,", result=self.result)
        self.after()
        self.play(FadeOut(self.trap_group), run_time=0.5)
        self.summary_card("remember", "Yang perlu diingat", [
            M(r"\text{frekuensi harapan} = P \times n", size=52, color=THEME.good),
            T("P = peluang,  n = banyak percobaan", size=36, weight=BLACK, color=THEME.blue),
            T("1 bukan bilangan prima", size=42, weight=BLACK, color=THEME.hl),
        ], ["*peluang*", None, "Dan"])

    # ------------------------------------------------------------ meaning
    def meaning(self):
        with self.beat("frequency"):
            self.clear_question()
            c1 = Card(7.8, 2.4).move_to([0, 3.6, 0])
            h1 = T("Frekuensi", size=46, weight=BLACK, color=THEME.blue).move_to(c1.body.get_top() + DOWN * 0.55)
            d1 = T("= berapa kali sesuatu terjadi", size=36, weight=HEAVY).next_to(h1, DOWN, 0.3)
            self.play(FadeIn(c1), Write(h1), run_time=0.7)
            self.play(FadeIn(d1), run_time=0.6)
            c2 = Card(7.8, 2.4).move_to([0, 0.6, 0])
            h2 = T("Frekuensi harapan", size=46, weight=BLACK, color=THEME.good).move_to(c2.body.get_top() + DOWN * 0.55)
            d2 = T("= berapa kali kita perkirakan", size=36, weight=HEAVY).next_to(h2, DOWN, 0.3)
            self.until("*frekuensi~harapan*")
            self.play(FadeIn(c2), Write(h2), run_time=0.7)
            self.until("*perkirakan*")
            self.play(FadeIn(d2), run_time=0.6)
            self.cards = VGroup(c1, h1, d1, c2, h2, d2)

    def warm_up(self):
        faces = "GAGGAAGAGA"  # five G out of ten, as the expectation says (one possible outcome)
        with self.beat("coins10"):
            self.play(FadeOut(self.cards), run_time=0.5)
            coins = VGroup(*[Coin("A", radius=0.42) for _ in range(10)]).arrange_in_grid(2, 5, buff=0.3).move_to([0, 3.3, 0])
            lab = T("koin dilempar 10 kali", size=36, weight=BLACK, color=THEME.muted).next_to(coins, UP, 0.35)
            self.play(FadeIn(lab), LaggedStart(*[GrowFromCenter(c) for c in coins], lag_ratio=0.06), run_time=1.0)
            self.until("*10*")
            new = VGroup()
            for c, f in zip(coins, faces):
                n = Coin(f, radius=0.42).move_to(c)
                new.add(n)
            self.play(LaggedStart(*[ReplacementTransform(c, n) for c, n in zip(coins, new)], lag_ratio=0.1), run_time=1.4)
            self.until("1/2,")
            p = M(r"P(\text{gambar}) = \tfrac{1}{2}", size=52, color=THEME.hl).move_to([0, 1.0, 0])
            self.play(Write(p), run_time=0.7)
            self.until("*5*")
            calc = M(r"10 \times \tfrac{1}{2} = 5", size=62, color=THEME.good).move_to([0, -0.4, 0])
            gs = [c for c, f in zip(new, faces) if f == "G"]
            self.play(Write(calc), *[Indicate(c, color=THEME.hl) for c in gs], run_time=1.0)
            self.warm = VGroup(lab, new, p, calc)

        with self.beat("formula"):
            self.play(self.warm.animate.scale(0.6).move_to([0, 4.4, 0]), run_time=0.6)
            f = M(r"\text{frekuensi harapan}", "=", "P", r"\times", "n", size=60).move_to([0, 1.0, 0])
            f[2].set_color(THEME.hl)
            f[4].set_color(THEME.blue)
            self.play(Write(f), run_time=1.0)
            self.until("*peluang*")
            tp = VGroup(M("P", size=50, color=THEME.hl), T("= peluang", size=40, weight=BLACK, color=THEME.hl))
            tp.arrange(RIGHT, buff=0.2).move_to([0, -0.3, 0])
            self.play(FadeIn(tp, shift=0.2 * UP), Indicate(f[2], color=THEME.hl, scale_factor=1.4), run_time=0.7)
            self.until("*banyak~percobaan*.")
            tn = VGroup(M("n", size=50, color=THEME.blue), T("= banyak percobaan", size=40, weight=BLACK, color=THEME.blue))
            tn.arrange(RIGHT, buff=0.2).next_to(tp, DOWN, 0.35)
            self.play(FadeIn(tn, shift=0.2 * UP), Indicate(f[4], color=THEME.blue, scale_factor=1.4), run_time=0.7)
            self.formula = VGroup(f, tp, tn)

    # --------------------------------------------------------------- solve
    def solve(self):
        with self.beat("prime"):
            self.play(FadeOut(self.warm), self.formula.animate.scale(0.7).move_to([0, 5.0, 0]), run_time=0.6)
            card = Card(7.8, 2.5).move_to([0, 2.6, 0])
            h = T("Bilangan prima", size=44, weight=BLACK, color=THEME.good).move_to(card.body.get_top() + DOWN * 0.5)
            d = T("tepat 2 pembagi: 1 dan dirinya sendiri", size=32, weight=HEAVY).next_to(h, DOWN, 0.35)
            self.play(FadeIn(card), Write(h), run_time=0.7)
            self.until("*dua*")
            self.play(FadeIn(d), run_time=0.6)
            ex = VGroup(
                VGroup(M(r"5:\ 1,\ 5", size=46), Badge(True, size=0.5)).arrange(RIGHT, buff=0.3),
                VGroup(M(r"6:\ 1,\ 2,\ 3,\ 6", size=46), Badge(False, size=0.5)).arrange(RIGHT, buff=0.3),
            ).arrange(RIGHT, buff=0.8).move_to([0, 0.3, 0])
            self.play(FadeIn(ex, shift=0.2 * UP), run_time=0.7)
            self.prime_card = VGroup(card, h, d, ex)

        with self.beat("check_numbers"):
            self.play(FadeOut(self.prime_card[3]), self.prime_card[:3].animate.scale(0.75).move_to([0, 3.95, 0]),
                      run_time=0.6)
            sp = Spinner(8, radius=1.9).move_to([-1.5, 0.6, 0])
            self.play(GrowFromCenter(sp), run_time=0.7)
            notes = VGroup()
            occ = {"2": 1}
            for n in range(2, 9):
                self.until(str(n), occurrence=occ.get(str(n), 1))
                prime = n in PRIMES
                line = T(f"{n}: " + ", ".join(map(str, DIVISORS[n])), size=36, weight=BLACK,
                         color=THEME.good if prime else THEME.muted)
                line.move_to([2.6, 2.05 - (n - 2) * 0.6, 0]).align_to([1.2, 0, 0], LEFT)
                anims = [FadeIn(line, shift=0.15 * LEFT)]
                if prime:
                    anims.append(Indicate(sp.sectors[n - 1], color=THEME.good, scale_factor=1.08))
                else:
                    anims += [sp.sectors[n - 1].animate.set_fill(opacity=0.15), sp.labels[n - 1].animate.set_opacity(0.3)]
                self.play(*anims, run_time=0.45)
                notes.add(line)
            self.sp, self.notes = sp, notes

        with self.beat("one"):
            self.until("1?")
            l1 = T("1: 1", size=36, weight=BLACK, color=THEME.bad).move_to([2.6, 2.65, 0]).align_to([1.2, 0, 0], LEFT)
            self.play(Indicate(self.sp.sectors[0], color=THEME.bad, scale_factor=1.1), FadeIn(l1), run_time=0.8)
            self.until("*bukan*")
            self.play(self.sp.sectors[0].animate.set_fill(opacity=0.15), self.sp.labels[0].animate.set_opacity(0.3),
                      run_time=0.6)
            tag = Tag("1 bukan prima", fill=THEME.soft_red, size=34).move_to([0, -2.2, 0])
            self.play(FadeIn(tag, shift=0.2 * UP), run_time=0.5)
            self.notes.add(l1)
            self.one_tag = tag

        with self.beat("probability"):
            self.play(FadeOut(self.one_tag), run_time=0.3)
            self.until("2,")
            self.play(*[Indicate(self.sp.labels[n - 1], color=THEME.good, scale_factor=1.6) for n in PRIMES], run_time=0.9)
            self.until("*4*")
            f = Frac(4, 8, size=66)
            f.num.set_color(THEME.good)
            row = VGroup(M("P", "=", size=62), f).arrange(RIGHT, buff=0.3)
            self.until("4/8")
            row.move_to([0, -2.1, 0])
            self.play(Write(row), run_time=0.8)
            self.until("*1/2*.")
            half = VGroup(M("=", size=62), Frac(1, 2, size=66)).arrange(RIGHT, buff=0.3).next_to(row, RIGHT, 0.3)
            self.play(Write(half), run_time=0.7)
            self.prob = VGroup(row, half)

        with self.beat("multiply"):
            self.play(FadeOut(VGroup(self.sp, self.notes, self.prime_card[:3], self.prob)),
                      self.formula.animate.scale(1 / 0.7).move_to([0, 3.4, 0]), run_time=0.8)
            calc = M(r"\tfrac{1}{2}", r"\times", "144", "=", "72", size=78).move_to([0, 0.8, 0])
            calc[0].set_color(THEME.hl)
            calc[2].set_color(THEME.blue)
            calc[4].set_color(THEME.good)
            self.play(Write(calc[:3]), run_time=1.0)
            self.until("*72*.")
            self.play(Write(calc[3:]), run_time=0.7)
            self.play(Circumscribe(calc[4], color=THEME.hl, buff=0.12), run_time=0.8)
            self.calc = calc

        with self.beat("picture"):
            self.play(FadeOut(self.formula), self.calc.animate.scale(0.6).move_to([0, 4.9, 0]), run_time=0.6)
            dots = VGroup(*[Dot(radius=0.13, color=THEME.faint) for _ in range(144)]).arrange_in_grid(12, 12, buff=0.22)
            dots.move_to([0, 1.25, 0])
            lab = T("144 putaran", size=32, weight=BLACK, color=THEME.muted).next_to(dots, UP, 0.25)
            self.play(FadeIn(lab), LaggedStart(*[GrowFromCenter(d) for d in dots], lag_ratio=0.004), run_time=1.4)
            rng = random.Random(7)
            pick = sorted(rng.sample(range(144), 72))
            self.until("*72*")
            self.play(LaggedStart(*[dots[k].animate.set_color(THEME.good) for k in pick], lag_ratio=0.012), run_time=2.2)
            legend = T("72 kali prima (kira-kira separuh)", size=32, weight=BLACK, color=THEME.good).next_to(dots, DOWN, 0.3)
            self.play(FadeIn(legend), run_time=0.5)
            self.picture = VGroup(dots, lab, legend, self.calc)
            self.result = M(r"\text{frekuensi harapan} = 72", size=60, color=THEME.good).move_to([0, 3.3, 0])
            self.play(FadeOut(self.picture), FadeIn(self.result), run_time=0.6)

    # --------------------------------------------------------------- after
    def after(self):
        with self.beat("estimate"):
            self.play(FadeOut(self.answer_group), run_time=0.5)
            nl = NumberLine(x_range=[60, 84, 4], length=7.4, include_numbers=True, font_size=34,
                            color=THEME.ink).move_to([0, 2.2, 0])
            for n in nl.numbers:
                n.set_color(THEME.ink)
            mark = Triangle(fill_color=THEME.good, fill_opacity=1, stroke_width=0).scale(0.18).rotate(3.1416)
            mark.next_to(nl.n2p(72), UP, 0.1)
            l72 = M("72", size=50, color=THEME.good).next_to(mark, UP, 0.12)
            self.play(Create(nl), run_time=0.8)
            self.play(FadeIn(mark), Write(l72), run_time=0.6)
            sims = VGroup()
            for v, cue in ((70, "70"), (75, "75.")):
                self.until(cue)
                d = Dot(nl.n2p(v), radius=0.14, color=THEME.blue)
                t = M(str(v), size=40, color=THEME.blue).next_to(d, DOWN, 1.05)
                self.play(GrowFromCenter(d), FadeIn(t), run_time=0.5)
                sims.add(d, t)
            note = T("hasil nyata bisa sedikit berbeda", size=32, weight=BLACK, color=THEME.muted).move_to([0, 0.3, 0])
            self.play(FadeIn(note), run_time=0.5)
            self.until("*72*")
            self.play(Indicate(l72, color=THEME.hl, scale_factor=1.4), run_time=0.8)
            self.est = VGroup(nl, mark, l72, sims, note)

        with self.beat("trap"):
            self.play(FadeOut(self.est), run_time=0.5)
            card = Card(7.6, 4.4).move_to([0, 2.0, 0])
            title = T("Kalau 1 dianggap prima:", size=42, weight=BLACK).move_to([0, 3.55, 0])
            row = M(r"\tfrac{5}{8} \times 144 = 90", size=66).move_to([-0.3, 1.9, 0])
            x = Badge(False, size=0.7).next_to(row, RIGHT, 0.4)
            note = T("tidak ada di pilihan", size=38, weight=BLACK, color=THEME.bad).move_to([0, 0.5, 0])
            self.play(FadeIn(card, shift=0.2 * UP), FadeIn(title), run_time=0.6)
            self.until("90.")
            self.play(Write(row), run_time=0.8)
            self.until("*tidak*")
            self.play(GrowFromCenter(x), FadeIn(note), run_time=0.5)
            self.trap_group = VGroup(card, title, row, x, note)
