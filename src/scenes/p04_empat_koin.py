"""Soal 1 (Bagian 1): empat koin setimbang, peluang tepat tiga sisi angka = 4/16 = 1/4.

Beginner path: what a fair coin is -> what "tepat tiga" means -> peluang = cocok / semua ->
warm-up with two coins (AG and GA are different) -> doubling 2, 4, 8, 16 -> list of 16 ->
"where is the single G?" -> 4/16 = 1/4 -> check with groups 1-4-6-4-1.

Render:  python scripts/render.py p04_empat_koin
"""

import sys
from itertools import product
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[2]))

import numpy as np  # noqa: E402
from manim import (  # noqa: E402
    DOWN, LEFT, RIGHT, UP, Arrow, Circle, Circumscribe, Create, FadeIn, FadeOut, GrowFromCenter,
    Indicate, LaggedStart, Line, Polygon, ReplacementTransform, RoundedRectangle, Square,
    SurroundingRectangle, TransformFromCopy, VGroup, Write,
)

from src.components.base import KinanScene  # noqa: E402
from src.components.cards import Badge, Card, Tag  # noqa: E402
from src.components.lesson import LessonMixin, coin_row  # noqa: E402
from src.components.probability import Coin  # noqa: E402
from src.components.text import BLACK, HEAVY, Frac, M, T  # noqa: E402
from src.components.theme import THEME  # noqa: E402

QUESTION = "Empat koin setimbang dilempar bersamaan. Peluang tepat tiga sisi angka adalah ..."
OPTIONS = [r"\frac{1}{8}", r"\frac{1}{4}", r"\frac{3}{8}", r"\frac{1}{2}"]
CORRECT = 1  # B
OUTCOMES = ["".join(p) for p in product("AG", repeat=4)]


def flip_anim(scene, coin: Coin, face: str, run_time: float = 0.4) -> Coin:
    scene.play(coin.animate.stretch(0.03, 0), run_time=run_time / 2)
    new = Coin(face).scale_to_fit_height(coin.height).move_to(coin).stretch(0.03, 0)
    scene.remove(coin)
    scene.add(new)
    scene.play(new.animate.stretch(1 / 0.03, 0), run_time=run_time / 2)
    return new


class P04EmpatKoin(LessonMixin, KinanScene):
    problem_id = "p04_empat_koin"

    def construct(self):
        self.read_question("question", "options", QUESTION, OPTIONS,
                           [("Empat", "Empat koin setimbang"), ("tepat~tiga", "tepat tiga sisi angka")],
                           ["1/8,", "1/4,", "3/8,", "1/2."], icon=coin_row("GGGG", r=0.42, gap=0.2), size=46, max_chars=28)
        self.understand()
        self.warm_up()
        self.solve()
        self.reveal_answer("answer", OPTIONS, CORRECT, "B,", result=self.result)
        self.check()
        self.play(FadeOut(self.check_group), run_time=0.5)
        self.summary_card("remember", "Yang perlu diingat", [
            T("1. Hitung semua hasil", size=40, weight=BLACK),
            M(r"\text{setiap koin} \times 2:\ 2 \to 4 \to 8 \to 16", size=46, color=THEME.blue),
            T("2. Hitung hasil yang cocok", size=40, weight=BLACK),
            M(r"P = \frac{4}{16} = \frac{1}{4}", size=58, color=THEME.good),
        ], ["semua", None, "cocok", "bagi"])

    # ------------------------------------------------------------ meaning
    def understand(self):
        with self.beat("sides"):
            self.clear_question()
            coin = Coin("A", radius=1.1).move_to([0, 2.6, 0])
            self.play(GrowFromCenter(coin), run_time=0.6)
            for f in "GAG":
                coin = flip_anim(self, coin, f)
            self.until("A,")
            a = Coin("A", radius=0.9).move_to([-1.7, 2.6, 0])
            g = Coin("G", radius=0.9).move_to([1.7, 2.6, 0])
            la = T("A = angka", size=40, weight=BLACK, color=THEME.blue).next_to(a, DOWN, 0.35)
            lg = T("G = gambar", size=40, weight=BLACK, color=THEME.hl).next_to(g, DOWN, 0.35)
            self.play(ReplacementTransform(coin, a), FadeIn(la), run_time=0.7)
            self.until("G.")
            self.play(GrowFromCenter(g), FadeIn(lg), run_time=0.6)
            self.faces = VGroup(a, g, la, lg)

        with self.beat("fair"):
            self.play(self.faces.animate.scale(0.7).move_to([0, 4.7, 0]), run_time=0.6)
            pivot = np.array([0, -0.2, 0])
            tri = Polygon(pivot, pivot + [-0.55, -0.9, 0], pivot + [0.55, -0.9, 0], fill_color=THEME.purple,
                          fill_opacity=1, stroke_color=THEME.ink, stroke_width=4)
            beam = Line(pivot + [-2.8, 0, 0], pivot + [2.8, 0, 0]).set_stroke(THEME.ink, 12)
            ca = Coin("A", radius=0.6).next_to(beam.get_start(), UP, 0).shift(RIGHT * 0.6)
            cg = Coin("G", radius=0.6).next_to(beam.get_end(), UP, 0).shift(LEFT * 0.6)
            saw = VGroup(beam, ca, cg)
            saw.rotate(0.22, about_point=pivot)
            self.play(FadeIn(tri), FadeIn(saw), run_time=0.7)
            self.until("*sama*")
            self.play(saw.animate.rotate(-0.22, about_point=pivot), run_time=1.2)
            self.until("1/2.")
            ha = M(r"\tfrac{1}{2}", size=64, color=THEME.blue).move_to([-2.2, -1.9, 0])
            hg = M(r"\tfrac{1}{2}", size=64, color=THEME.hl).move_to([2.2, -1.9, 0])
            self.play(FadeIn(ha, shift=0.2 * UP), FadeIn(hg, shift=0.2 * UP), run_time=0.6)
            self.seesaw = VGroup(tri, saw, ha, hg)

        with self.beat("exactly"):
            self.play(FadeOut(self.seesaw), run_time=0.5)
            title = T("tepat tiga angka?", size=46, weight=BLACK, color=THEME.hl).move_to([0, 3.4, 0])
            self.play(Write(title), run_time=0.6)
            rows = []
            for k, (faces, ok, note, cue) in enumerate((("AAAG", True, "3 angka", "Dari"),
                                                         ("AAAA", False, "4 angka: kelebihan", "lebih,"),
                                                         ("AAGG", False, "2 angka: kurang", "kurang."))):
                r = coin_row(faces, r=0.42, gap=0.14).move_to([-1.45, 2.0 - 1.35 * k, 0])
                b = Badge(ok, size=0.62).next_to(r, RIGHT, 0.35)
                n = T(note, size=32, weight=BLACK, color=THEME.good if ok else THEME.bad).next_to(r, DOWN, 0.18)
                self.until(cue)
                self.play(FadeIn(r, shift=0.2 * RIGHT), GrowFromCenter(b), FadeIn(n), run_time=0.7)
                rows.append(VGroup(r, b, n))
            self.examples = VGroup(title, self.faces, *rows)

    # --------------------------------------------------------- idea + 2 coins
    def warm_up(self):
        with self.beat("idea"):
            self.play(FadeOut(self.examples), run_time=0.5)
            q = T("Bagaimana menghitung peluang?", size=42, weight=BLACK).move_to([0, 3.6, 0])
            self.play(FadeIn(q), run_time=0.5)
            wf = self.word_fraction("hasil yang kita inginkan", "semua hasil yang mungkin", y=1.4)
            self.play(FadeIn(wf.lhs), Create(wf.bar), run_time=0.6)
            self.until("*inginkan*")
            self.play(Write(wf.num), run_time=0.8)
            self.until("*semua*")
            self.play(Write(wf.den), run_time=0.8)
            self.idea = VGroup(q, wf)

        with self.beat("small1"):
            self.play(FadeOut(self.idea[0]), self.idea[1].animate.scale(0.62).move_to([0, 5.15, 0]), run_time=0.6)
            self.until("dua")
            c1, c2 = Coin("A", radius=0.75).move_to([-1.1, 2.6, 0]), Coin("G", radius=0.75).move_to([1.1, 2.6, 0])
            t1 = T("koin 1", size=34, weight=BLACK, color=THEME.blue).next_to(c1, DOWN, 0.25)
            t2 = T("koin 2", size=34, weight=BLACK, color=THEME.warn).next_to(c2, DOWN, 0.25)
            self.play(GrowFromCenter(c1), GrowFromCenter(c2), FadeIn(t1), FadeIn(t2), run_time=0.7)
            self.two = VGroup(c1, c2, t1, t2)

        cells = {}
        with self.beat("small2"):
            self.play(self.two.animate.scale(0.6).move_to([0, 3.75, 0]), run_time=0.5)
            spots = {"AA": (-1.8, 2.0), "AG": (1.8, 2.0), "GA": (-1.8, 0.35), "GG": (1.8, 0.35)}
            for faces, (x, y) in spots.items():
                row = coin_row(faces, r=0.45, gap=0.16)
                u1 = Line(row[0].get_corner(DOWN + LEFT), row[0].get_corner(DOWN + RIGHT)).set_stroke(THEME.blue, 7)
                u2 = Line(row[1].get_corner(DOWN + LEFT), row[1].get_corner(DOWN + RIGHT)).set_stroke(THEME.warn, 7)
                VGroup(u1, u2).shift(DOWN * 0.12)
                box = RoundedRectangle(width=2.6, height=1.35, corner_radius=0.2, stroke_color=THEME.faint,
                                       stroke_width=3, fill_color=THEME.card, fill_opacity=1)
                g = VGroup(box, VGroup(row, u1, u2).move_to(box))
                g.move_to([x, y, 0])
                cells[faces] = g
                self.until(f"{faces}," if faces != "GG" else "GG.")
                self.play(FadeIn(g, scale=0.8), run_time=0.45)
            self.until("*empat*")
            n4 = Tag("4 kemungkinan", fill=THEME.soft_blue, size=38).move_to([0, -1.05, 0])
            self.play(FadeIn(n4, shift=0.2 * UP), run_time=0.5)
            self.cells2, self.n4 = cells, n4

        with self.beat("small3"):
            self.until("*berbeda*,")
            self.play(Indicate(cells["AG"], color=THEME.hl, scale_factor=1.08),
                      Indicate(cells["GA"], color=THEME.hl, scale_factor=1.08), run_time=1.0)
            self.until("pertama")
            self.play(Indicate(self.two[0], color=THEME.blue), Indicate(self.two[2], color=THEME.blue), run_time=0.7)
            self.until("kedua")
            self.play(Indicate(self.two[1], color=THEME.warn), Indicate(self.two[3], color=THEME.warn), run_time=0.7)

        with self.beat("small4"):
            self.until("*2*")
            self.play(*[cells[k][0].animate.set_fill(THEME.soft_green).set_stroke(THEME.good, 5) for k in ("AG", "GA")],
                      run_time=0.6)
            self.until("2/4.")
            f = Frac(2, 4, size=70)
            f.num.set_color(THEME.good)
            f.den.set_color(THEME.blue)
            f.move_to([0, -2.3, 0])
            self.play(FadeOut(self.n4), FadeIn(f), run_time=0.6)
            self.warm = VGroup(self.idea[1], self.two, *cells.values(), f)

    # --------------------------------------------------------------- solve
    def solve(self):
        with self.beat("double1"):
            self.play(FadeOut(self.warm), run_time=0.5)
            four = coin_row("AGAG", r=0.45, gap=0.2).move_to([0, 4.7, 0])
            self.play(FadeIn(four, shift=0.2 * DOWN), run_time=0.5)
            self.until("*dua~kali~lipat*.")
            self.four = four

        rows = VGroup()
        with self.beat("double2"):
            labels = []
            for i, n in enumerate((2, 4, 8, 16)):
                sq = VGroup(*[Square(0.3, fill_color=THEME.blue if j % 2 == 0 else THEME.hl, fill_opacity=0.9,
                                     stroke_color=THEME.bg, stroke_width=2) for j in range(n)])
                sq.arrange(RIGHT, buff=0.04)
                lab = T(f"{i + 1} koin", size=32, weight=BLACK)
                num = M(str(n), size=56, color=THEME.good)
                y = 3.3 - i * 1.15
                lab.move_to([-3.45, y, 0])
                sq.next_to(lab, RIGHT, 0.35)
                num.move_to([3.85, y, 0])
                rows.add(VGroup(lab, sq, num))
                labels.append(lab)
            arrows = VGroup(*[M(r"\times 2", size=36, color=THEME.purple).move_to([2.9, 3.3 - i * 1.15 - 0.58, 0])
                              for i in range(3)])
            cues = [None, "4.", "8.", "*16*"]
            for i, row in enumerate(rows):
                if cues[i]:
                    self.until(cues[i])
                anims = [FadeIn(row[0]), LaggedStart(*[GrowFromCenter(s) for s in row[1]], lag_ratio=0.05),
                         FadeIn(row[2])]
                if i:
                    anims.append(FadeIn(arrows[i - 1]))
                self.play(*anims, run_time=0.8)
            prod = M(r"2 \times 2 \times 2 \times 2 = 16", size=58).move_to([0, -1.4, 0])
            self.play(Write(prod), run_time=0.9)
            self.doubling = VGroup(rows, arrows, prod, self.four)

        grid = {}
        with self.beat("list"):
            self.play(FadeOut(self.doubling), run_time=0.5)
            for k, o in enumerate(OUTCOMES):
                col, r = divmod(k, 8)
                row = coin_row(o, r=0.22, gap=0.07)
                bg = RoundedRectangle(width=2.5, height=0.58, corner_radius=0.14, fill_color=THEME.card,
                                      fill_opacity=1, stroke_width=0)
                g = VGroup(bg, row.move_to(bg))
                g.move_to([-1.7 + 3.4 * col, 4.55 - r * 0.68, 0])
                grid[o] = g
            self.play(LaggedStart(*[FadeIn(grid[o], shift=0.1 * RIGHT) for o in OUTCOMES], lag_ratio=0.08),
                      run_time=2.6)
            total = Tag("16 hasil", fill=THEME.soft_blue, size=38).move_to([0, -1.05, 0])
            self.play(FadeIn(total), run_time=0.4)
            self.grid, self.total = grid, total

        match = [o for o in OUTCOMES if o.count("A") == 3]
        with self.beat("find"):
            self.until("*satu*.")
            rings = VGroup()
            for o in match:
                gcoin = grid[o][1][o.index("G")]
                rings.add(Circle(radius=0.3, stroke_color=THEME.hl, stroke_width=6).move_to(gcoin))
            self.play(*[grid[o].animate.set_opacity(0.3) for o in OUTCOMES if o not in match], run_time=0.6)
            self.play(LaggedStart(*[Create(r) for r in rings], lag_ratio=0.25), run_time=1.2)
            self.rings = rings

        with self.beat("four"):
            order = sorted(match, key=lambda o: o.index("G"))
            targets = VGroup()
            self.play(FadeOut(self.rings), FadeOut(self.total),
                      *[FadeOut(grid[o]) for o in OUTCOMES if o not in match], run_time=0.5)
            for i, o in enumerate(order):
                self.until(f"ke-{i + 1}," if i < 3 else "ke-4.")
                row = coin_row(o, r=0.42, gap=0.14)
                bg = RoundedRectangle(width=3.0, height=1.0, corner_radius=0.2, fill_color=THEME.soft_green,
                                      fill_opacity=1, stroke_color=THEME.good, stroke_width=4)
                g = VGroup(bg, row.move_to(bg)).move_to([-0.9, 3.7 - i * 1.25, 0])
                lab = T(f"G di koin ke-{i + 1}", size=30, weight=BLACK, color=THEME.hl).next_to(g, RIGHT, 0.3)
                self.play(ReplacementTransform(grid[o], g), FadeIn(lab), run_time=0.6)
                targets.add(VGroup(g, lab))
            self.until("*4*")
            n = Tag("4 hasil cocok", fill=THEME.soft_green, size=40).move_to([0, -1.25, 0])
            self.play(FadeIn(n, shift=0.2 * UP), run_time=0.5)
            self.matches, self.n_match = targets, n

        with self.beat("compute"):
            self.play(self.matches.animate.scale(0.6).move_to([0, 4.2, 0]), FadeOut(self.n_match), run_time=0.6)
            lhs = M("P", "=", size=70)
            f1 = Frac(4, 16, size=72)
            f1.num.set_color(THEME.good)
            f1.den.set_color(THEME.blue)
            eq = M("=", size=70)
            f2 = Frac(1, 4, size=72)
            row = VGroup(lhs, f1, eq, f2).arrange(RIGHT, buff=0.35).move_to([0, 0.6, 0])
            self.play(Write(lhs), Write(f1), run_time=0.9)
            self.until("Bagi")
            d1 = M(r"\div 4", size=40, color=THEME.purple).next_to(VGroup(f1.num, f2.num), UP, 0.2)
            d2 = M(r"\div 4", size=40, color=THEME.purple).next_to(VGroup(f1.den, f2.den), DOWN, 0.2)
            self.play(FadeIn(d1), FadeIn(d2), FadeIn(eq), run_time=0.6)
            self.play(TransformFromCopy(f1.num, f2.num), TransformFromCopy(f1.den, f2.den), Create(f2.bar),
                      run_time=0.9)
            self.until("*1/4*.")
            self.play(Circumscribe(f2, color=THEME.hl, buff=0.15), run_time=0.9)
            self.play(FadeOut(self.matches), FadeOut(d1), FadeOut(d2), run_time=0.4)
            self.result = VGroup(lhs, f1, eq, f2)

    # --------------------------------------------------------------- check
    def check(self):
        bins_x = [-3.25, -1.62, 0.0, 1.62, 3.25]
        with self.beat("check1"):
            self.play(FadeOut(self.answer_group), run_time=0.5)
            minis = {o: coin_row(o, r=0.15, gap=0.04).set_z_index(2) for o in OUTCOMES}
            for k, o in enumerate(OUTCOMES):
                col, r = divmod(k, 8)
                minis[o].move_to([-1.7 + 3.4 * col, 4.4 - r * 0.5, 0])
            self.play(LaggedStart(*[FadeIn(minis[o]) for o in OUTCOMES], lag_ratio=0.04), run_time=1.0)
            self.until("Kelompokkan")
            bins = VGroup()
            for n, x in enumerate(bins_x):
                card = Card(1.5, 3.6, radius=0.16, stroke_width=3).move_to([x, 1.3, 0])
                head = T(f"{n} angka", size=28, weight=BLACK, color=THEME.blue).move_to([x, 3.4, 0])
                bins.add(VGroup(card, head))
            self.play(LaggedStart(*[FadeIn(b, shift=0.2 * UP) for b in bins], lag_ratio=0.1), run_time=0.8)
            slot = {n: 0 for n in range(5)}
            moves = []
            for o in OUTCOMES:
                n = o.count("A")
                moves.append(minis[o].animate.move_to([bins_x[n], 2.75 - slot[n] * 0.52, 0]))
                slot[n] += 1
            self.play(LaggedStart(*moves, lag_ratio=0.06), run_time=2.0)
            self.bins, self.minis = bins, minis

        with self.beat("check2"):
            counts = VGroup(*[M(str(c), size=60).move_to([x, -0.85, 0]) for c, x in zip((1, 4, 6, 4, 1), bins_x)])
            self.play(LaggedStart(*[Write(c) for c in counts], lag_ratio=0.2), run_time=1.2)
            self.until("16.")
            tot = M(r"1 + 4 + 6 + 4 + 1 = 16", size=50, color=THEME.blue).move_to([0, -1.9, 0])
            self.play(Write(tot), run_time=0.8)
            self.until("*4*.")
            self.play(self.bins[3][0].body.animate.set_fill(THEME.soft_green),
                      Circumscribe(counts[3], color=THEME.hl), run_time=0.9)
            self.check_group = VGroup(self.bins, *self.minis.values(), counts, tot)
