"""Problem 2: three fair coins, at least one picture side (G); P(exactly two G) = 3/7.

Key visual idea: a tree diagram builds the 8 equally likely outcomes; the
condition deletes AAA (8 -> 7); exactly-two-G outcomes are GGA, GAG, AGG (3).
Check: regroup outcomes by number of G into 1-3-3-1 bins, then the formula
P(A|B) = P(A n B)/P(B) with A n B = A because A is inside B.

Render:  python scripts/render.py p02_tiga_koin
"""

import sys
from itertools import product
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[2]))

import numpy as np  # noqa: E402
from manim import (  # noqa: E402
    DOWN, LEFT, RIGHT, UP, AnimationGroup, Brace, Circle, Circumscribe, Create, Dot, Ellipse,
    FadeIn, FadeOut, FadeTransform, Flash, GrowFromCenter, Indicate, LaggedStart, Line,
    ReplacementTransform, RoundedRectangle, TransformFromCopy, VGroup, Write, rate_functions,
)

from src.components.base import KinanScene  # noqa: E402
from src.components.cards import Badge, Card, Tag, TextCard, strike  # noqa: E402
from src.components.probability import Choices, Coin  # noqa: E402
from src.components.text import BLACK, HEAVY, Frac, M, T  # noqa: E402
from src.components.theme import THEME  # noqa: E402

QUESTION = ("Tiga koin fair dilempar bersamaan. Jika diketahui sedikitnya satu sisi "
            "gambar muncul, peluang tepat dua sisi gambar adalah ...")
OPTIONS = [r"\frac{2}{7}", r"\frac{3}{7}", r"\frac{4}{7}", r"\frac{1}{2}"]
CORRECT = 1  # B

OUTCOMES = ["".join(p) for p in product("GA", repeat=3)]  # GGG, GGA, ..., AAA
LEVEL_X = [-3.7, -2.3, -0.9, 0.5]  # root, coin 1, coin 2, coin 3
ROW_X = [1.55, 2.12, 2.69]  # outcome triple
BADGE_X = 3.6
TOP_Y = 5.5
NODE_R = 0.26


def leaf_y(k: int) -> float:
    return 4.0 - k * 0.82


def node_y(prefix: str) -> float:
    ks = [k for k, o in enumerate(OUTCOMES) if o.startswith(prefix)]
    return float(np.mean([leaf_y(k) for k in ks]))


def triple(outcome: str, r: float = 0.25, spacing: float = 0.57) -> VGroup:
    g = VGroup(*[Coin(f, radius=r) for f in outcome])
    for i, c in enumerate(g):
        c.move_to([i * spacing, 0, 0])
    return g


def count_badge(n: int, fill: str) -> VGroup:
    disc = Circle(radius=0.27, fill_color=fill, fill_opacity=1, stroke_color=THEME.ink, stroke_width=3)
    return VGroup(disc, T(str(n), size=34, weight=BLACK).move_to(disc))


class P02TigaKoin(KinanScene):
    problem_id = "p02_tiga_koin"

    def construct(self):
        self.hook()
        self.question()
        self.understand()
        self.tree()
        self.condition()
        self.count()
        self.answer()
        self.check_groups()
        self.check_formula()
        self.takeaway()

    # -------------------------------------------------------- helpers
    def flip(self, coins: VGroup, faces: str, run_time: float = 0.3):
        """Flip coins in place (squash, swap face, unsquash)."""
        self.play(*[c.animate.stretch(0.03, 0) for c in coins], run_time=run_time / 2)
        new = VGroup()
        for c, f in zip(coins, faces):
            n = Coin(f).scale_to_fit_height(c.height).move_to(c).stretch(0.03, 0)
            self.remove(c)
            self.add(n)
            new.add(n)
        self.play(*[n.animate.stretch(1 / 0.03, 0) for n in new], run_time=run_time / 2)
        return new

    # ------------------------------------------------------------ hook
    def hook(self):
        with self.beat("hook"):
            coins = VGroup(*[Coin(f, radius=0.85) for f in "GAG"]).arrange(RIGHT, buff=0.45)
            coins.move_to([0, 2.6, 0])
            start = coins.copy().shift(UP * 4)
            self.play(ReplacementTransform(start, coins, rate_func=rate_functions.ease_out_cubic),
                      run_time=0.6)
            for faces in ("AGA", "GGA", "AAG", "GAG"):
                coins = self.flip(coins, faces, run_time=0.32)
            self.until("bocoran")
            tag = Tag("bocoran: sedikitnya 1 gambar", fill=THEME.soft_yellow, size=38).move_to([0, 0.4, 0])
            self.play(FadeIn(tag, shift=0.2 * UP), Indicate(coins[0]), Indicate(coins[2]), run_time=0.8)
            self.until("Apakah")
            q = T("?", size=150, weight=BLACK, color=THEME.purple).move_to([0, 4.9, 0])
            self.play(FadeIn(q, scale=0.4), run_time=0.5)
            self.hook_group = VGroup(coins, tag, q)

    # -------------------------------------------------------- question
    def question(self):
        with self.beat("question"):
            card = TextCard(QUESTION, width=8.0, size=42, max_chars=30, pad=0.42).move_to([0, 3.0, 0])
            self.play(FadeOut(self.hook_group, shift=0.3 * UP), run_time=0.5)
            self.play(FadeIn(card, shift=0.3 * UP), run_time=0.7)
            self.until("sedikitnya")
            m1 = card.mark("sedikitnya satu sisi gambar muncul")
            self.play(FadeIn(m1), run_time=0.5)
            self.until("tepat")
            m2 = card.mark("tepat dua sisi gambar")
            self.play(FadeIn(m2), run_time=0.5)
            self.qcard = VGroup(card.card, m1, m2, card.text)
            self.bring_to_front(card.text)
        with self.beat("options"):
            choices = Choices(OPTIONS, width=8.0, height=1.45, size=50).move_to([0, -0.35, 0])
            self.play(LaggedStart(*[FadeIn(c, shift=0.2 * UP) for c in choices], lag_ratio=0.15),
                      run_time=0.9)
            for i, token in enumerate(("2/7", "3/7", "4/7", "1/2")):
                self.until(token)
                self.play(Indicate(choices[i], color=THEME.purple, scale_factor=1.08), run_time=0.5)
            self.choices = choices

    # ------------------------------------------------------ understand
    def understand(self):
        with self.beat("faces"):
            self.play(FadeOut(self.choices), FadeOut(self.qcard), run_time=0.6)
            g = Coin("G", radius=0.75).move_to([-1.7, 3.6, 0])
            a = Coin("A", radius=0.75).move_to([1.7, 3.6, 0])
            lg = T("gambar", size=40, weight=BLACK, color=THEME.warn).next_to(g, DOWN, 0.25)
            la = T("angka", size=40, weight=BLACK, color=THEME.blue).next_to(a, DOWN, 0.25)
            self.until("G")
            self.play(GrowFromCenter(g), FadeIn(lg), run_time=0.6)
            self.until("A")
            self.play(GrowFromCenter(a), FadeIn(la), run_time=0.6)
            self.until("sama~mungkin")
            half_g = M(r"\tfrac{1}{2}", size=56).next_to(lg, DOWN, 0.25)
            half_a = M(r"\tfrac{1}{2}", size=56).next_to(la, DOWN, 0.25)
            self.play(FadeIn(half_g), FadeIn(half_a), run_time=0.6)
            self.faces_group = VGroup(g, a, lg, la, half_g, half_a)
        with self.beat("words"):
            # number of G on a 0..3 scale; brackets show what each phrase allows
            chips = VGroup()
            for n in range(4):
                box = RoundedRectangle(width=1.3, height=1.0, corner_radius=0.18, fill_color=THEME.card,
                                       fill_opacity=1, stroke_color=THEME.ink, stroke_width=4)
                chips.add(VGroup(box, T(f"{n} G", size=40, weight=BLACK).move_to(box)))
            chips.arrange(RIGHT, buff=0.3).move_to([0, -0.2, 0])
            self.play(self.faces_group.animate.scale(0.75).move_to([0, 3.9, 0]),
                      LaggedStart(*[FadeIn(c, shift=0.2 * UP) for c in chips], lag_ratio=0.1), run_time=0.8)
            self.until("Sedikitnya~satu")
            b1 = Brace(VGroup(*chips[1:]), UP, color=THEME.blue)
            l1 = T("sedikitnya satu", size=36, weight=BLACK, color=THEME.blue).next_to(b1, UP, 0.12)
            self.play(GrowFromCenter(b1), FadeIn(l1),
                      *[c[0].animate.set_fill(THEME.soft_blue) for c in chips[1:]], run_time=0.7)
            self.until("Tepat~dua")
            b2 = Brace(chips[2], DOWN, color=THEME.good)
            l2 = T("tepat dua", size=36, weight=BLACK, color=THEME.good).next_to(b2, DOWN, 0.12)
            self.play(GrowFromCenter(b2), FadeIn(l2), chips[2][0].animate.set_fill(THEME.soft_green),
                      run_time=0.7)
            self.words_group = VGroup(chips, b1, l1, b2, l2)

    # ------------------------------------------------------------ tree
    def tree(self):
        self.nodes, self.edges = {}, {}
        root = Dot([LEVEL_X[0], node_y(""), 0], radius=0.13, color=THEME.ink)
        for d in range(1, 4):
            for p in {o[:d] for o in OUTCOMES}:
                c = Coin(p[-1], radius=NODE_R).move_to([LEVEL_X[d], node_y(p), 0])
                self.nodes[p] = c
                start = root.get_center() if d == 1 else self.nodes[p[:-1]].get_center()
                ra = 0.13 if d == 1 else NODE_R
                self.edges[p] = Line(*self._trim(start, c.get_center(), ra)).set_stroke(THEME.ink, 4)
        self.root = root

        heads = VGroup(*[T(f"Koin {d}", size=28, weight=BLACK, color=THEME.purple).move_to([LEVEL_X[d], 4.75, 0])
                         for d in (1, 2, 3)],
                       T("Hasil", size=28, weight=BLACK, color=THEME.purple).move_to([ROW_X[1], 4.75, 0]))

        def level(d):
            ps = sorted(p for p in self.nodes if len(p) == d)
            ps.sort(key=lambda p: -node_y(p))
            return ps

        with self.beat("tree1"):
            self.play(FadeOut(self.words_group), FadeOut(self.faces_group), run_time=0.5)
            self.play(GrowFromCenter(root), FadeIn(heads[0]), run_time=0.4)
            for p, tok in (("G", "G"), ("A", "A")):
                self.until(tok)
                self.play(Create(self.edges[p]), GrowFromCenter(self.nodes[p]), run_time=0.5)
        with self.beat("tree2"):
            self.until("kedua,")
            self.play(FadeIn(heads[1]), LaggedStart(*[AnimationGroup(Create(self.edges[p]), GrowFromCenter(self.nodes[p]))
                                                      for p in level(2)], lag_ratio=0.2), run_time=1.2)
            self.until("ketiga.")
            self.play(FadeIn(heads[2]), LaggedStart(*[AnimationGroup(Create(self.edges[p]), GrowFromCenter(self.nodes[p]))
                                                      for p in level(3)], lag_ratio=0.12), run_time=1.6)
        self.rows, self.row_bg = {}, {}
        with self.beat("tree3"):
            self.until("jalur")
            demo = "GAG"
            path = [self.edges[demo[:d]] for d in (1, 2, 3)]
            self.play(*[e.animate.set_stroke(THEME.warn, 9) for e in path],
                      *[Indicate(self.nodes[demo[:d]], color=THEME.warn) for d in (1, 2, 3)], run_time=0.9)
            for k, o in enumerate(OUTCOMES):
                self.rows[o] = triple(o).move_to([ROW_X[1], leaf_y(k), 0])
            self.play(FadeIn(heads[3]),
                      TransformFromCopy(VGroup(*[self.nodes[demo[:d]] for d in (1, 2, 3)]), self.rows[demo]),
                      run_time=0.9)
            self.play(*[e.animate.set_stroke(THEME.ink, 4) for e in path], run_time=0.3)
            rest = [o for o in OUTCOMES if o != demo]
            self.play(LaggedStart(*[TransformFromCopy(VGroup(*[self.nodes[o[:d]] for d in (1, 2, 3)]), self.rows[o])
                                    for o in rest], lag_ratio=0.12), run_time=1.8)
            self.until("2~×~2~×~2")
            self.counter = M(r"2 \times 2 \times 2 = 8", size=56).move_to([1.8, TOP_Y, 0])
            self.play(Write(self.counter), run_time=0.8)
        self.heads = heads

    @staticmethod
    def _trim(a, b, ra=NODE_R, rb=NODE_R):
        a, b = np.array(a), np.array(b)
        u = (b - a) / np.linalg.norm(b - a)
        return a + u * ra, b - u * rb

    # ------------------------------------------------------- condition
    def condition(self):
        with self.beat("condition"):
            self.until("sedikitnya")
            self.syarat = Tag("sedikitnya 1 G", fill=THEME.soft_yellow, size=40).move_to([-2.2, TOP_Y, 0])
            self.play(FadeIn(self.syarat, shift=0.2 * DOWN), run_time=0.5)
            self.until("AAA.")
            o = "AAA"
            bg = RoundedRectangle(width=2.35, height=0.72, corner_radius=0.2, fill_color=THEME.soft_red,
                                  fill_opacity=1, stroke_width=0).move_to(self.rows[o])
            path = [self.edges[o[:d]] for d in (1, 2, 3)]
            self.play(FadeIn(bg), *[e.animate.set_stroke(THEME.bad, 8) for e in path], run_time=0.6)
            self.bring_to_front(self.rows[o])
            self.aaa_bg = bg
        with self.beat("shrink"):
            self.until("dicoret.")
            x = strike(self.rows["AAA"], width=8).scale(1.1)
            self.play(Create(x), self.rows["AAA"].animate.set_opacity(0.35),
                      *[self.edges["AAA"[:d]].animate.set_stroke(opacity=0.3) for d in (2, 3)],
                      *[self.nodes["AAA"[:d]].animate.set_opacity(0.3) for d in (2, 3)], run_time=0.7)
            self.aaa_x = x
            self.until("8~−~1")
            new = M(r"8 - 1 = 7", size=56).move_to(self.counter)
            self.play(ReplacementTransform(self.counter, new), run_time=0.7)
            self.until("7.")
            box = Card(2.4, 1.0, fill=THEME.soft_blue, radius=0.18, stroke_width=4)
            n7 = VGroup(box, M("n(S) = 7", size=50).move_to(box.body)).move_to([2.0, TOP_Y, 0])
            self.play(FadeTransform(new, n7), Flash(n7, color=THEME.blue), run_time=0.8)
            self.counter = n7

    # ----------------------------------------------------------- count
    def count(self):
        live = [o for o in OUTCOMES if o != "AAA"]
        self.badges = {}
        with self.beat("badges"):
            for o in live:
                self.badges[o] = count_badge(o.count("G"), THEME.soft_yellow).move_to(
                    [BADGE_X, self.rows[o].get_y(), 0])
            self.until("gambar")
            self.play(LaggedStart(*[AnimationGroup(
                Indicate(VGroup(*[c for c in self.rows[o] if c.face == "G"]), color=THEME.warn),
                FadeIn(self.badges[o], scale=0.5)) for o in live], lag_ratio=0.15), run_time=2.2)
        with self.beat("exactly"):
            self.good_bg = VGroup()
            for o in ("GGA", "GAG", "AGG"):
                self.until(f"{o},") if o != "AGG" else self.until("AGG.")
                bg = RoundedRectangle(width=3.1, height=0.72, corner_radius=0.2, fill_color=THEME.soft_green,
                                      fill_opacity=1, stroke_width=0).move_to([(ROW_X[0] + BADGE_X) / 2 - 0.12,
                                                                               self.rows[o].get_y(), 0])
                self.add(bg)
                bg.set_z_index(-1)
                self.play(FadeIn(bg), self.badges[o][0].animate.set_fill(THEME.good),
                          *[e.animate.set_stroke(THEME.good, 7) for e in (self.edges[o[:d]] for d in (1, 2, 3))],
                          run_time=0.45)
                self.good_bg.add(bg)
            self.until("3.")
            self.n_good = Tag("tepat 2 G: 3", fill=THEME.soft_green, size=40).move_to([-2.2, TOP_Y, 0])
            self.play(FadeTransform(self.syarat, self.n_good), run_time=0.6)
        with self.beat("fraction"):
            lhs = M("P", "=", size=64)
            f = Frac(3, 7, size=64)
            f.num.set_color(THEME.good)
            f.den.set_color(THEME.blue)
            row = VGroup(lhs, f).arrange(RIGHT, buff=0.3).move_to([0, -2.75, 0])
            self.play(FadeIn(lhs), Create(f.bar), run_time=0.4)
            self.until("3")
            self.play(TransformFromCopy(self.n_good[1][-1], f.num), run_time=0.7)
            self.until("7")
            self.play(TransformFromCopy(self.counter[1][0][-1], f.den), run_time=0.7)
            self.until("3/7.")
            self.play(Circumscribe(row, color=THEME.good, buff=0.15), run_time=0.8)
            self.result = row

    # ---------------------------------------------------------- answer
    def answer(self):
        with self.beat("answer"):
            tree_stuff = VGroup(self.root, *self.nodes.values(), *self.edges.values(), self.heads,
                                *self.badges.values(), self.good_bg, self.aaa_bg, self.aaa_x)
            self.play(FadeOut(tree_stuff), FadeOut(VGroup(*self.rows.values())), FadeOut(self.counter),
                      FadeOut(self.n_good), self.result.animate.move_to([0, 3.4, 0]).scale(1.2), run_time=0.8)
            choices = Choices(OPTIONS, width=8.0, height=1.45, size=50).move_to([0, 0.9, 0])
            self.play(FadeIn(choices, shift=0.2 * UP), run_time=0.5)
            self.until("B,")
            self.play(*[choices[i].animate.set_opacity(0.3) for i in range(4) if i != CORRECT],
                      choices[CORRECT].animate.scale(1.12), run_time=0.6)
            badge = choices.mark(CORRECT)
            self.play(choices[CORRECT][0].body.animate.set_fill(THEME.soft_green), GrowFromCenter(badge),
                      run_time=0.5)
            self.answer_group = VGroup(choices, badge, self.result)

    # ------------------------------------------------------ check: bins
    def check_groups(self):
        bins_x = [-3.0, -1.0, 1.0, 3.0]
        with self.beat("groups"):
            self.play(FadeOut(self.answer_group), run_time=0.5)
            rows = {o: triple(o, r=0.24, spacing=0.55) for o in OUTCOMES}
            for k, o in enumerate(OUTCOMES):
                rows[o].move_to([0, leaf_y(k) + 0.1, 0])
            self.play(LaggedStart(*[FadeIn(rows[o], shift=0.1 * RIGHT) for o in OUTCOMES], lag_ratio=0.06),
                      run_time=0.9)
            self.until("Kelompokkan")
            bins = VGroup()
            for n, x in enumerate(bins_x):
                card = Card(1.9, 3.3, radius=0.2, stroke_width=4).move_to([x, 2.2, 0])
                head = T(f"{n} G", size=38, weight=BLACK, color=THEME.purple).move_to([x, 4.3, 0])
                bins.add(VGroup(card, head))
            self.play(LaggedStart(*[FadeIn(b, shift=0.2 * UP) for b in bins], lag_ratio=0.1), run_time=0.7)
            slots = {n: 0 for n in range(4)}
            moves = []
            for o in OUTCOMES:
                n = o.count("G")
                count_in_bin = sum(1 for p in OUTCOMES if p.count("G") == n)
                y = 2.2 + (count_in_bin - 1) * 0.42 - slots[n] * 0.84
                slots[n] += 1
                moves.append(rows[o].animate.move_to([bins_x[n], y, 0]))
            self.play(LaggedStart(*moves, lag_ratio=0.08), run_time=2.0)
            self.bins, self.bin_rows = bins, rows
        with self.beat("pascal"):
            counts = VGroup(*[M(str(c), size=64).move_to([x, 0.05, 0]) for c, x in zip((1, 3, 3, 1), bins_x)])
            self.play(LaggedStart(*[Write(c) for c in counts], lag_ratio=0.25), run_time=1.2)
            self.until("membuang")
            x0 = strike(self.bins[0][0], width=9)
            self.play(self.bins[0][0].body.animate.set_fill(THEME.soft_red), Create(x0),
                      self.bin_rows["AAA"].animate.set_opacity(0.35), counts[0].animate.set_opacity(0.35),
                      run_time=0.7)
            self.until("3~+~3~+~1")
            br = Brace(VGroup(*self.bins[1:]), DOWN, color=THEME.blue).shift(0.75 * DOWN)
            n7 = M(r"3 + 3 + 1 = 7", size=56, color=THEME.blue).next_to(br, DOWN, 0.15)
            self.play(GrowFromCenter(br), Write(n7), run_time=0.9)
            self.until("3", occurrence=3)  # "Yang tepat dua: 3." (after "1, 3, 3, 1")
            self.play(self.bins[2][0].body.animate.set_fill(THEME.soft_green),
                      Circumscribe(counts[2], color=THEME.good), run_time=0.8)
            self.bins_group = VGroup(self.bins, *self.bin_rows.values(), counts, x0, br, n7)

    # ---------------------------------------------------- check: formula
    def check_formula(self):
        with self.beat("subset"):
            self.play(FadeOut(self.bins_group), run_time=0.5)
            universe = Card(8.0, 4.1, radius=0.25).move_to([0, 3.55, 0])
            s_lab = T("S: 8 hasil", size=32, weight=BLACK, color=THEME.muted).move_to([-2.9, 5.25, 0])
            big = Ellipse(width=6.9, height=3.2, fill_color=THEME.soft_blue, fill_opacity=1,
                          stroke_color=THEME.blue, stroke_width=5).move_to([-0.35, 3.45, 0])
            small = Ellipse(width=3.3, height=1.9, fill_color=THEME.soft_green, fill_opacity=1,
                            stroke_color=THEME.good, stroke_width=5).move_to([1.05, 3.2, 0])
            b_lab = M(r"B", size=56, color=THEME.blue).move_to([-3.2, 4.4, 0])
            a_lab = M(r"A", size=56, color=THEME.good).move_to([2.35, 3.95, 0])
            inside_a = VGroup(*[T(o, size=30, weight=BLACK) for o in ("GGA", "GAG", "AGG")]).arrange(DOWN, buff=0.12)
            inside_a.move_to(small)
            inside_b = VGroup(*[T(o, size=30, weight=BLACK) for o in ("GGG", "GAA", "AGA", "AAG")])
            inside_b.arrange_in_grid(2, 2, buff=(0.4, 0.25)).move_to([-1.9, 3.3, 0])
            out = T("AAA", size=30, weight=BLACK, color=THEME.bad).move_to([3.0, 2.0, 0])
            legend = VGroup(
                VGroup(M("A", size=44, color=THEME.good), T(": tepat 2 G", size=34, weight=HEAVY)).arrange(RIGHT, buff=0.1),
                VGroup(M("B", size=44, color=THEME.blue), T(": sedikitnya 1 G", size=34, weight=HEAVY)).arrange(RIGHT, buff=0.1),
            ).arrange(RIGHT, buff=0.6).move_to([0, 0.95, 0])
            self.play(FadeIn(universe), FadeIn(s_lab), run_time=0.4)
            self.play(Create(big), FadeIn(b_lab), FadeIn(inside_b), FadeIn(out), run_time=0.8)
            self.play(Create(small), FadeIn(a_lab), FadeIn(inside_a), FadeIn(legend), run_time=0.8)
            self.until("termasuk")
            self.play(Indicate(VGroup(small, inside_a), color=THEME.good, scale_factor=1.06), run_time=0.9)
            self.until("irisannya")
            f1 = M(r"P(A \mid B)", "=", r"\frac{P(A \cap B)}{P(B)}", "=", r"\frac{P(A)}{P(B)}", size=50)
            f1.move_to([0, -0.55, 0])
            self.play(Write(f1[:3]), run_time=1.0)
            note = M(r"A \cap B = A", size=44, color=THEME.good).next_to(f1, DOWN, 0.2)
            self.play(FadeIn(note), Write(f1[3:]), run_time=0.9)
            self.venn = VGroup(universe, s_lab, big, small, b_lab, a_lab, inside_a, inside_b, out, legend)
            self.f1, self.note = f1, note
        with self.beat("formula"):
            self.play(FadeOut(self.note), self.venn.animate.scale(0.82).move_to([0, 3.9, 0]),
                      self.f1.animate.move_to([0, 0.8, 0]), run_time=0.7)
            f2 = M("=", r"\dfrac{3/8}{7/8}", size=58).move_to([-0.6, -1.5, 0])
            self.play(Write(f2), run_time=0.9)
            self.until("menghilangkan:")
            f3 = M("=", r"\dfrac{3/\cancel{8}}{7/\cancel{8}}", size=58).move_to(f2)
            f3[1].set_color(THEME.ink)
            self.play(FadeTransform(f2, f3), run_time=0.7)
            res = VGroup(M("=", size=58), Frac(3, 7, size=62)).arrange(RIGHT, buff=0.25).next_to(f3, RIGHT, 0.25)
            self.play(Write(res), run_time=0.7)
            self.play(Circumscribe(res[1], color=THEME.good, buff=0.12), run_time=0.8)
            self.formula = VGroup(self.venn, self.f1, f3, res)
        with self.beat("trap"):
            self.play(FadeOut(self.formula), run_time=0.6)
            card = Card(7.6, 4.4).move_to([0, 1.8, 0])
            title = T("Tanpa memakai syarat:", size=44, weight=BLACK).move_to([0, 3.4, 0])
            row = VGroup(M("P =", size=66), Frac(3, 8, size=70)).arrange(RIGHT, buff=0.3).move_to([-0.3, 1.8, 0])
            x = Badge(False, size=0.7).next_to(row, RIGHT, 0.4)
            note = T("tidak ada di pilihan", size=38, color=THEME.bad, weight=BLACK).move_to([0, 0.35, 0])
            self.play(FadeIn(card, shift=0.2 * UP), FadeIn(title), run_time=0.6)
            self.until("3/8.")
            self.play(Write(row), run_time=0.8)
            self.until("Tidak")
            self.play(GrowFromCenter(x), FadeIn(note), run_time=0.5)
            self.trap = VGroup(card, title, row, x, note)

    # -------------------------------------------------------- takeaway
    def takeaway(self):
        with self.beat("takeaway"):
            self.play(FadeOut(self.trap), run_time=0.5)
            card = Card(8.0, 6.4).move_to([0, 2.2, 0])
            head = T("Syarat mengubah ruang sampel", size=44, weight=BLACK, color=THEME.purple).move_to([0, 4.75, 0])
            c1 = VGroup(*[Coin(f, radius=0.42) for f in "GAG"]).arrange(RIGHT, buff=0.15).move_to([-2.0, 3.45, 0])
            same = T("koinnya sama", size=36, weight=HEAVY).next_to(c1, RIGHT, 0.4)
            s_row = VGroup(M("n(S):", size=54), M("8", size=60), M(r"\to", size=60), M("7", size=60, color=THEME.blue))
            s_row.arrange(RIGHT, buff=0.3).move_to([0, 2.15, 0])
            p_row = VGroup(M("P:", size=54), Frac(3, 8, size=56), M(r"\to", size=60), Frac(3, 7, size=56))
            p_row.arrange(RIGHT, buff=0.3).move_to([0, 0.55, 0])
            p_row[-1].set_color(THEME.good)
            self.play(FadeIn(card, shift=0.2 * UP), FadeIn(head), FadeIn(c1), FadeIn(same), run_time=0.7)
            self.until("ruang~sampel:")
            self.play(Write(s_row), run_time=1.0)
            self.until("naik")
            self.play(Write(p_row), run_time=1.0)
            self.play(Circumscribe(p_row[-1], color=THEME.good, buff=0.12), run_time=0.9)
