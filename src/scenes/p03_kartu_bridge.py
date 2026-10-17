"""Problem 3: two cards drawn together from 52; P(exactly one face card (J, Q, K)
and the two cards have different colours) = 40/221.

Key visual idea: the 52 cards physically regroup into a 2x2 table
(face / not face x red / black) = 6, 6, 20, 20. "Exactly one face" links the
top row to the bottom row; "different colour" forces the diagonal links.
Pairs between two groups are a rectangle of dots: 6 x 20 = 120, twice -> 240.
All pairs: 52 x 51 / 2 = 1326. P = 240/1326 = 40/221. Checked by drawing one
card at a time: 4 x (6/52)(20/51) = 40/221.

Render:  python scripts/render.py p03_kartu_bridge
"""

import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[2]))

import numpy as np  # noqa: E402
from manim import (  # noqa: E402
    DOWN, LEFT, RIGHT, UP, AnimationGroup, ArcBetweenPoints, Circumscribe, Create, CurvedDoubleArrow,
    Dot, DoubleArrow, FadeIn, FadeOut, FadeTransform, GrowFromCenter, Indicate, LaggedStart, Line,
    ReplacementTransform, RoundedRectangle, SurroundingRectangle, TransformFromCopy, VGroup, Write,
    rate_functions,
)

from src.components.base import KinanScene  # noqa: E402
from src.components.cards import Badge, Card, Tag, TextCard, strike  # noqa: E402
from src.components.probability import Choices, MiniCard, PlayingCard  # noqa: E402
from src.components.text import BLACK, HEAVY, Frac, M, T  # noqa: E402
from src.components.theme import THEME  # noqa: E402

QUESTION = ("Dua kartu diambil sekaligus dari satu set kartu Bridge standar (52 kartu) tanpa joker. "
            "Peluang tepat satu kartu bergambar (J, Q, atau K) dan kedua kartu berlainan warna adalah ...")
OPTIONS = [r"\frac{20}{221}", r"\frac{40}{221}", r"\frac{60}{221}", r"\frac{80}{221}"]
CORRECT = 1  # B

RANKS = ["A", "2", "3", "4", "5", "6", "7", "8", "9", "10", "J", "Q", "K"]
SUITS = ["H", "D", "S", "C"]  # hearts, diamonds (red); spades, clubs (black)
FACES = {"J", "Q", "K"}

# 2x2 table of groups: (face?, red?) -> block centre and inner grid shape
BLOCKS = {
    (True, True): {"center": (-1.95, 3.85), "size": (3.8, 2.6), "grid": (3, 2), "title": "Merah bergambar"},
    (True, False): {"center": (1.95, 3.85), "size": (3.8, 2.6), "grid": (3, 2), "title": "Hitam bergambar"},
    (False, True): {"center": (-1.95, 0.05), "size": (3.8, 4.5), "grid": (5, 4), "title": "Merah tidak bergambar"},
    (False, False): {"center": (1.95, 0.05), "size": (3.8, 4.5), "grid": (5, 4), "title": "Hitam tidak bergambar"},
}


class P03KartuBridge(KinanScene):
    problem_id = "p03_kartu_bridge"

    def construct(self):
        self.hook()
        self.question()
        self.understand()
        self.deck()
        self.pairs()
        self.all_pairs()
        self.compute()
        self.answer()
        self.check()
        self.takeaway()

    # ------------------------------------------------------------ hook
    def hook(self):
        with self.beat("hook"):
            fan_cards = [("9", "S"), ("K", "H"), ("4", "D"), ("7", "C"), ("Q", "S")]
            fan = VGroup(*[PlayingCard(r, s, width=1.35) for r, s in fan_cards])
            for i, c in enumerate(fan):
                ang = (2 - i) * 0.16
                c.rotate(ang, about_point=c.get_bottom())
                c.move_to([(i - 2) * 0.95, 2.5 - abs(i - 2) * 0.12, 0])
            self.play(LaggedStart(*[FadeIn(c, shift=0.4 * UP) for c in fan], lag_ratio=0.12), run_time=1.0)
            self.until("satu", occurrence=2)  # "Hanya satu yang bergambar"
            k, seven = fan[1], fan[3]
            self.play(k.animate.rotate(-0.16).move_to([-1.3, 1.1, 0]).scale(1.15),
                      seven.animate.rotate(0.16).move_to([1.3, 1.1, 0]).scale(1.15),
                      *[c.animate.set_opacity(0.25) for c in (fan[0], fan[2], fan[4])], run_time=0.9)
            t1 = Tag("bergambar", fill=THEME.soft_yellow, size=32).next_to(k, DOWN, 0.25)
            self.play(FadeIn(t1, shift=0.1 * UP), run_time=0.4)
            self.until("berbeda.")
            t2 = Tag("merah", fill=THEME.soft_red, size=32).next_to(t1, DOWN, 0.15)
            t3 = Tag("hitam", fill=THEME.faint, size=32).next_to(seven, DOWN, 0.25).align_to(t2, DOWN)
            self.play(FadeIn(t2, shift=0.1 * UP), FadeIn(t3, shift=0.1 * UP), run_time=0.5)
            self.until("Berapa")
            q = T("?", size=150, weight=BLACK, color=THEME.purple).move_to([0, 5.0, 0])
            self.play(FadeIn(q, scale=0.4), run_time=0.5)
            self.hook_group = VGroup(fan, t1, t2, t3, q)

    # -------------------------------------------------------- question
    def question(self):
        with self.beat("question"):
            card = TextCard(QUESTION, width=8.0, size=40, max_chars=32, pad=0.4).move_to([0, 3.0, 0])
            self.play(FadeOut(self.hook_group, shift=0.3 * UP), run_time=0.5)
            self.play(FadeIn(card, shift=0.3 * UP), run_time=0.7)
            marks = VGroup()
            for token, phrase in (("sekaligus", "sekaligus"), ("tepat~satu", "tepat satu kartu bergambar"),
                                  ("berlainan~warna", "berlainan warna")):
                self.until(token)
                m = card.mark(phrase)
                self.add(m)
                self.bring_to_front(card.text)
                self.play(FadeIn(m), run_time=0.4)
                marks.add(m)
            self.qcard = VGroup(card.card, marks, card.text)
        with self.beat("options"):
            choices = Choices(OPTIONS, width=8.0, height=1.45, size=46).move_to([0, -0.4, 0])
            self.play(LaggedStart(*[FadeIn(c, shift=0.2 * UP) for c in choices], lag_ratio=0.15),
                      run_time=0.9)
            for i, token in enumerate(("20,", "40,", "60,", "80,")):
                self.until(token)
                self.play(Indicate(choices[i], color=THEME.purple, scale_factor=1.08), run_time=0.45)
            self.choices = choices

    # ------------------------------------------------------ understand
    def understand(self):
        with self.beat("conditions"):
            self.play(FadeOut(self.choices), FadeOut(self.qcard), run_time=0.6)
            c1 = Tag("1  Tepat satu kartu bergambar", fill=THEME.soft_yellow, size=38).move_to([0, 4.7, 0])
            c2 = Tag("2  Warna berbeda: merah + hitam", fill=THEME.soft_blue, size=38).move_to([0, 3.7, 0])
            self.until("Pertama:")
            self.play(FadeIn(c1, shift=0.2 * DOWN), run_time=0.5)
            self.until("Kedua:")
            self.play(FadeIn(c2, shift=0.2 * DOWN), run_time=0.5)
            # examples: one pair satisfying both, two failing one condition each
            ex = VGroup()
            for (a, b), ok, why in (((("K", "H"), ("7", "C")), True, "cocok"),
                                    ((("K", "H"), ("Q", "S")), False, "2 bergambar"),
                                    ((("K", "H"), ("7", "D")), False, "warna sama")):
                pair = VGroup(PlayingCard(*a, width=0.85), PlayingCard(*b, width=0.85)).arrange(RIGHT, buff=0.12)
                badge = Badge(ok, size=0.48).next_to(pair, UP, 0.12)
                label = T(why, size=28, weight=BLACK, color=THEME.good if ok else THEME.bad).next_to(pair, DOWN, 0.15)
                ex.add(VGroup(pair, badge, label))
            ex.arrange(RIGHT, buff=0.45).move_to([0, 0.7, 0])
            self.play(LaggedStart(*[FadeIn(e, shift=0.2 * UP) for e in ex], lag_ratio=0.3), run_time=1.4)
            self.cond_group = VGroup(c1, c2, ex)
        with self.beat("together"):
            self.play(self.cond_group.animate.set_opacity(0.0), run_time=0.4)
            self.remove(self.cond_group)
            p1 = VGroup(PlayingCard("K", "H", width=1.1), PlayingCard("7", "C", width=1.1)).arrange(RIGHT, buff=0.15)
            p2 = VGroup(PlayingCard("7", "C", width=1.1), PlayingCard("K", "H", width=1.1)).arrange(RIGHT, buff=0.15)
            eq = M("=", size=90)
            row = VGroup(p1, eq, p2).arrange(RIGHT, buff=0.4).move_to([0, 3.0, 0])
            self.play(FadeIn(p1, shift=0.2 * UP), run_time=0.5)
            self.until("urutan")
            self.play(TransformFromCopy(p1[0], p2[1], path_arc=-1.2), TransformFromCopy(p1[1], p2[0], path_arc=-1.2),
                      FadeIn(eq), run_time=1.0)
            self.until("pasangan")
            label = T("{K♥, 7♣}", size=70, weight=BLACK).move_to([0, 0.6, 0])
            label[1:3].set_color(THEME.red_suit)  # characters: { K ♥ , space 7 ♣ }
            note = T("1 pasangan", size=40, weight=BLACK, color=THEME.purple).next_to(label, DOWN, 0.3)
            self.play(Write(label), FadeIn(note), run_time=0.9)
            self.together = VGroup(row, label, note)

    # ------------------------------------------------------------ deck
    def deck(self):
        self.minis = {}
        rows_y = [4.2, 3.32, 2.44, 1.56]
        with self.beat("deck"):
            self.play(FadeOut(self.together), run_time=0.5)
            bands = VGroup()
            for k, (suit, y) in enumerate(zip(SUITS, rows_y)):
                for i, r in enumerate(RANKS):
                    m = MiniCard(r, suit, width=0.54).move_to([-3.6 + i * 0.6, y, 0]).set_z_index(2)
                    self.minis[r, suit] = m
            for ys, fill in ((rows_y[:2], THEME.soft_red), (rows_y[2:], THEME.faint)):
                band = RoundedRectangle(width=8.3, height=abs(ys[0] - ys[1]) + 0.98, corner_radius=0.2,
                                        fill_color=fill, fill_opacity=1, stroke_width=0)
                band.move_to([0, np.mean(ys), 0]).set_z_index(-1)
                bands.add(band)
            order = [(r, s) for s in SUITS for r in RANKS]
            self.play(LaggedStart(*[FadeIn(self.minis[k], shift=0.15 * DOWN) for k in order], lag_ratio=0.012),
                      run_time=2.4)
            self.until("13")
            self.play(Indicate(VGroup(*[self.minis[r, "H"] for r in RANKS]), color=THEME.purple, scale_factor=1.04),
                      run_time=0.8)
            self.until("merah,")
            self.play(FadeIn(bands[0]), run_time=0.5)
            self.until("hitam.")
            self.play(FadeIn(bands[1]), run_time=0.5)
            self.bands = bands
            self.labels = VGroup()
        with self.beat("faces"):
            self.until("J,")
            box = RoundedRectangle(width=3 * 0.6 + 0.12, height=4 * 0.88 + 0.12, corner_radius=0.15,
                                   stroke_color=THEME.warn, stroke_width=8, fill_opacity=0)
            box.move_to([-3.6 + 11 * 0.6, np.mean(rows_y), 0])
            self.play(Create(box), run_time=0.8)
            self.until("6~merah")
            t = M(r"12 = ", r"6\ \text{merah}", "+", r"6\ \text{hitam}", size=48).move_to([0, -0.2, 0])
            t[1].set_color(THEME.red_suit)
            self.play(Write(t), run_time=1.0)
            self.face_box, self.face_tex = box, t
        with self.beat("plain"):
            t2 = M(r"40 = ", r"20\ \text{merah}", "+", r"20\ \text{hitam}", size=48).move_to([0, -1.2, 0])
            t2[1].set_color(THEME.red_suit)
            self.until("40")
            self.play(Indicate(VGroup(*[self.minis[r, s] for (r, s) in self.minis if r not in FACES]),
                               color=THEME.blue, scale_factor=1.02), Write(t2), run_time=1.2)
            self.plain_tex = t2
        with self.beat("blocks"):
            self.blocks = {}
            frames = VGroup()
            for key, spec in BLOCKS.items():
                card = Card(*spec["size"], radius=0.2, stroke_width=4).move_to([*spec["center"], 0])
                fill = THEME.soft_red if key[1] else THEME.faint
                card.body.set_fill(fill)
                title = T(spec["title"], size=30, weight=BLACK,
                          color=THEME.red_suit if key[1] else THEME.ink)
                title.move_to(card.body.get_top() + DOWN * 0.32)
                frames.add(VGroup(card, title))
                self.blocks[key] = {"frame": VGroup(card, title), "cards": VGroup(), "spec": spec}
            moves = []
            for key, block in self.blocks.items():
                face, red = key
                members = [k for k in self.minis if (k[0] in FACES) == face and (k[1] in "HD") == red]
                cols, rows = block["spec"]["grid"]
                cx, cy = block["spec"]["center"]
                top = cy + block["spec"]["size"][1] / 2 - 0.85
                for n, k in enumerate(members):
                    col, row = n % cols, n // cols
                    target = [cx + (col - (cols - 1) / 2) * 0.62, top - row * 0.82, 0]
                    moves.append(self.minis[k].animate.move_to(target))
                    block["cards"].add(self.minis[k])
            self.play(FadeOut(self.bands), FadeOut(self.face_box), FadeOut(self.face_tex), FadeOut(self.plain_tex),
                      run_time=0.5)
            self.play(LaggedStart(*[FadeIn(f) for f in frames], lag_ratio=0.1), run_time=0.5)
            self.bring_to_front(*self.minis.values())
            self.play(LaggedStart(*moves, lag_ratio=0.01), run_time=2.0)
            self.counts = {}
            for key, block in self.blocks.items():
                n = len(block["cards"])
                badge = Card(0.95, 0.72, fill=THEME.hl, radius=0.18, stroke_width=4)
                badge = VGroup(badge, M(str(n), size=48).move_to(badge.body))
                badge.move_to(block["frame"][0].body.get_corner(DOWN + RIGHT) + [-0.55, 0.45, 0]).set_z_index(3)
                self.counts[key] = badge
            self.play(LaggedStart(*[GrowFromCenter(b) for b in self.counts.values()], lag_ratio=0.15), run_time=0.8)

    # ----------------------------------------------------------- pairs
    def pairs(self):
        table = VGroup(*[VGroup(b["frame"], b["cards"], self.counts[k]) for k, b in self.blocks.items()])
        self.table = table
        with self.beat("link"):
            self.play(table.animate.scale(0.56).move_to([0, 3.85, 0]), run_time=0.9)
            fr, fb = self.blocks[True, True]["frame"][0], self.blocks[True, False]["frame"][0]
            nr, nb = self.blocks[False, True]["frame"][0], self.blocks[False, False]["frame"][0]
            self.until("atas,")
            top_row = SurroundingRectangle(VGroup(fr, fb), color=THEME.warn, buff=0.06, corner_radius=0.15,
                                           stroke_width=6)
            self.play(Create(top_row), run_time=0.5)
            self.until("bawah.")
            bot_row = SurroundingRectangle(VGroup(nr, nb), color=THEME.blue, buff=0.06, corner_radius=0.15,
                                           stroke_width=6)
            self.play(Create(bot_row), run_time=0.5)
            self.until("beda.")
            l1 = Line(fr.get_center(), nb.get_center()).set_stroke(THEME.good, 12)
            l2 = Line(fb.get_center(), nr.get_center()).set_stroke(THEME.good, 12)
            for ln in (l1, l2):
                ln.set_z_index(5)
            self.play(Create(l1), Create(l2), FadeOut(top_row), FadeOut(bot_row), run_time=0.9)
            self.links = VGroup(l1, l2)

        def dot_rect(color: str) -> VGroup:
            dots = VGroup(*[Dot([c * 0.265, -r * 0.24, 0], radius=0.075, color=color)
                            for r in range(6) for c in range(20)])
            return dots

        with self.beat("rect1"):
            self.play(self.links[1].animate.set_stroke(opacity=0.25), run_time=0.4)
            d1 = dot_rect(THEME.red_suit).move_to([1.25, 0.55, 0])
            lab_r = T("6 merah bergambar", size=26, weight=BLACK, color=THEME.red_suit).rotate(np.pi / 2)
            lab_r.next_to(d1, LEFT, 0.15)
            lab_c = T("20 hitam tidak bergambar", size=26, weight=BLACK).next_to(d1, UP, 0.12)
            self.play(TransformFromCopy(self.counts[True, True], lab_r),
                      TransformFromCopy(self.counts[False, False], lab_c), run_time=0.8)
            self.play(LaggedStart(*[GrowFromCenter(d) for d in d1], lag_ratio=0.006), run_time=1.6)
            self.until("6~×~20")
            v1 = M(r"6 \times 20", "=", "120", size=52).move_to([-2.85, 0.35, 0])
            v1.scale_to_fit_width(min(v1.width, 2.0))
            self.play(Write(v1), run_time=0.9)
            self.rect1 = VGroup(d1, lab_r, lab_c, v1)
        with self.beat("rect2"):
            self.play(self.links[1].animate.set_stroke(opacity=1), self.links[0].animate.set_stroke(opacity=0.25),
                      run_time=0.4)
            d2 = dot_rect(THEME.black_suit).move_to([1.25, -1.55, 0])
            lab_r2 = T("6 hitam bergambar", size=26, weight=BLACK).rotate(np.pi / 2).next_to(d2, LEFT, 0.15)
            lab_c2 = T("20 merah tidak bergambar", size=26, weight=BLACK, color=THEME.red_suit).next_to(d2, UP, 0.12)
            self.play(FadeIn(lab_r2), FadeIn(lab_c2), LaggedStart(*[GrowFromCenter(d) for d in d2], lag_ratio=0.004),
                      run_time=1.4)
            v2 = M(r"6 \times 20", "=", "120", size=52).move_to([-2.85, -1.75, 0])
            v2.scale_to_fit_width(min(v2.width, 2.0))
            self.play(Write(v2), run_time=0.8)
            self.until("240")
            self.play(self.links[0].animate.set_stroke(opacity=1), run_time=0.3)
            tot = M(r"120 + 120 = 240", size=54).move_to([0, -2.95, 0])
            tot.set_color_by_tex("240", THEME.good)
            self.play(Write(tot), run_time=0.9)
            self.play(Circumscribe(tot, color=THEME.good, buff=0.1), run_time=0.7)
            self.rect2 = VGroup(d2, lab_r2, lab_c2, v2)
            self.total_tex = tot

    # ------------------------------------------------------- all pairs
    def all_pairs(self):
        with self.beat("total"):
            self.good_tag = Tag("cocok: 240", fill=THEME.soft_green, size=40).move_to([-2.1, 5.4, 0])
            self.play(FadeOut(VGroup(self.table, self.links, self.rect1, self.rect2)),
                      ReplacementTransform(self.total_tex, self.good_tag), run_time=0.8)
            s1 = Card(3.4, 2.6, radius=0.22).move_to([-1.9, 2.6, 0])
            s2 = Card(3.4, 2.6, radius=0.22).move_to([1.9, 2.6, 0])
            h1 = T("Kartu ke-1", size=34, weight=BLACK, color=THEME.purple).move_to(s1.body.get_top() + DOWN * 0.4)
            h2 = T("Kartu ke-2", size=34, weight=BLACK, color=THEME.purple).move_to(s2.body.get_top() + DOWN * 0.4)
            n1 = M("52", size=90).move_to(s1.body).shift(DOWN * 0.25)
            n2 = M("51", size=90).move_to(s2.body).shift(DOWN * 0.25)
            self.play(FadeIn(VGroup(s1, h1, s2, h2), shift=0.2 * UP), run_time=0.6)
            self.until("52")
            self.play(Write(n1), run_time=0.6)
            self.until("51.")
            self.play(Write(n2), run_time=0.6)
            prod = M(r"52 \times 51 = 2652", size=58).move_to([0, 0.4, 0])
            self.play(TransformFromCopy(VGroup(n1, n2), prod), run_time=0.9)
            self.slots, self.prod = VGroup(s1, h1, s2, h2, n1, n2), prod
        with self.beat("double"):
            self.until("dua~kali:")
            p1 = VGroup(PlayingCard("K", "H", width=0.8), PlayingCard("7", "C", width=0.8)).arrange(RIGHT, buff=0.1)
            p2 = VGroup(PlayingCard("7", "C", width=0.8), PlayingCard("K", "H", width=0.8)).arrange(RIGHT, buff=0.1)
            row = VGroup(p1, M("=", size=70), p2).arrange(RIGHT, buff=0.35).move_to([0, -1.2, 0])
            self.play(FadeIn(p1, shift=0.2 * UP), run_time=0.5)
            self.until("7♣", occurrence=2)
            self.play(FadeIn(row[1]), FadeIn(p2, shift=0.2 * UP), run_time=0.6)
            self.until("1326")
            res = M(r"\binom{52}{2}", "=", r"\frac{52 \times 51}{2}", "=", "1326", size=56).move_to([0, 0.4, 0])
            res[-1].set_color(THEME.blue)
            self.play(FadeOut(row), FadeTransform(self.prod, res), run_time=0.9)
            self.all_tag = Tag("semua: 1326", fill=THEME.soft_blue, size=40).move_to([2.0, 5.4, 0])
            self.play(TransformFromCopy(res[-1], self.all_tag), run_time=0.7)
            self.double_group = VGroup(self.slots, res)

    # --------------------------------------------------------- compute
    def compute(self):
        with self.beat("prob"):
            self.play(FadeOut(self.double_group), run_time=0.5)
            f1 = Frac(240, 1326, size=70)
            f1.num.set_color(THEME.good)
            f1.den.set_color(THEME.blue)
            row = VGroup(M("P", "=", size=70), f1).arrange(RIGHT, buff=0.3).move_to([-1.2, 2.3, 0])
            self.play(FadeIn(row[0]), Create(f1.bar), run_time=0.4)
            self.play(TransformFromCopy(self.good_tag[1][-3:], f1.num),
                      TransformFromCopy(self.all_tag[1][-4:], f1.den), run_time=1.0)
            self.p_row = row
        with self.beat("simplify"):
            self.until("6:")
            f2 = Frac(40, 221, size=70)
            eq = M("=", size=70)
            VGroup(eq, f2).arrange(RIGHT, buff=0.3).next_to(self.p_row, RIGHT, 0.3)
            d_top = M(r"\div 6", size=38, color=THEME.purple).next_to(VGroup(self.p_row[1].num, f2.num), UP, 0.15)
            d_bot = M(r"\div 6", size=38, color=THEME.purple).next_to(VGroup(self.p_row[1].den, f2.den), DOWN, 0.15)
            self.play(FadeIn(d_top), FadeIn(d_bot), FadeIn(eq), run_time=0.5)
            self.play(TransformFromCopy(self.p_row[1].num, f2.num), TransformFromCopy(self.p_row[1].den, f2.den),
                      Create(f2.bar), run_time=0.9)
            fact = M(r"240 = 6 \cdot 40,\quad 1326 = 6 \cdot 221", size=44, color=THEME.ink).move_to([0, -0.4, 0])
            self.play(FadeIn(fact, shift=0.2 * UP), run_time=0.6)
            self.until("40/221.")
            self.play(Circumscribe(f2, color=THEME.good, buff=0.15), run_time=0.8)
            self.result = VGroup(self.p_row, eq, f2, d_top, d_bot)
            self.fact = fact

    # ---------------------------------------------------------- answer
    def answer(self):
        with self.beat("answer"):
            self.play(FadeOut(self.fact), FadeOut(self.good_tag), FadeOut(self.all_tag),
                      self.result.animate.move_to([0, 3.5, 0]), run_time=0.7)
            choices = Choices(OPTIONS, width=8.0, height=1.45, size=46).move_to([0, 0.6, 0])
            self.play(FadeIn(choices, shift=0.2 * UP), run_time=0.5)
            self.until("B,")
            self.play(*[choices[i].animate.set_opacity(0.3) for i in range(4) if i != CORRECT],
                      choices[CORRECT].animate.scale(1.12), run_time=0.6)
            badge = choices.mark(CORRECT)
            self.play(choices[CORRECT][0].body.animate.set_fill(THEME.soft_green), GrowFromCenter(badge),
                      run_time=0.5)
            self.answer_group = VGroup(choices, badge, self.result)

    # ----------------------------------------------------------- check
    def check(self):
        with self.beat("seq"):
            self.play(FadeOut(self.answer_group), run_time=0.5)
            a = PlayingCard("K", "H", width=1.15).move_to([-1.4, 3.9, 0])
            b = PlayingCard("7", "C", width=1.15).move_to([1.4, 3.9, 0])
            arrow = M(r"\longrightarrow", size=70).move_to([0, 3.9, 0])
            la = T("merah bergambar", size=28, weight=BLACK, color=THEME.red_suit).next_to(a, DOWN, 0.2)
            lb = T("hitam tidak bergambar", size=28, weight=BLACK).next_to(b, DOWN, 0.2)
            self.until("Merah")
            self.play(FadeIn(a, shift=0.2 * DOWN), FadeIn(la), run_time=0.5)
            self.until("hitam")
            self.play(FadeIn(arrow), FadeIn(b, shift=0.2 * DOWN), FadeIn(lb), run_time=0.5)
            self.until("6/52~×~20/51.")
            f = M(r"\frac{6}{52}", r"\times", r"\frac{20}{51}", size=64).move_to([0, 1.2, 0])
            self.play(TransformFromCopy(la, f[0]), FadeIn(f[1]), TransformFromCopy(lb, f[2]), run_time=1.0)
            self.seq_group, self.seq_f = VGroup(a, b, arrow, la, lb), f
        with self.beat("seq2"):
            self.until("4")
            four = M(r"4 \times", size=64).next_to(self.seq_f, LEFT, 0.25)
            why = M(r"4 = \underbrace{2}_{\text{pasangan warna}} \times \underbrace{2}_{\text{urutan}}",
                    size=44).move_to([0, -0.45, 0])
            grp = VGroup(four, self.seq_f)
            self.play(Write(four), FadeIn(why, shift=0.2 * UP), run_time=0.9)
            self.play(grp.animate.move_to([-1.5, 1.2, 0]), run_time=0.5)
            res = M("=", r"\frac{480}{2652}", "=", r"\frac{40}{221}", size=64).next_to(grp, RIGHT, 0.25)
            res.set_color_by_tex(r"\frac{40}{221}", THEME.good)
            self.until("40/221.")
            self.play(Write(res), run_time=1.0)
            badge = Badge(True, size=0.62).next_to(res, UP, 0.2).align_to(res, RIGHT)
            self.play(GrowFromCenter(badge), run_time=0.4)
            self.seq2 = VGroup(self.seq_group, grp, why, res, badge)
        with self.beat("trap"):
            self.play(FadeOut(self.seq2), run_time=0.5)
            card = Card(7.6, 4.6).move_to([0, 2.0, 0])
            title = T("Hanya satu pasangan warna:", size=42, weight=BLACK).move_to([0, 3.75, 0])
            row = M(r"\frac{120}{1326}", "=", r"\frac{20}{221}", size=66).move_to([-0.3, 2.1, 0])
            x = Badge(False, size=0.7).next_to(row, RIGHT, 0.4)
            note = T("jebakan pilihan A", size=38, color=THEME.bad, weight=BLACK).move_to([0, 0.55, 0])
            self.play(FadeIn(card, shift=0.2 * UP), FadeIn(title), run_time=0.6)
            self.until("20/221.")
            self.play(Write(row), run_time=0.9)
            self.until("jebakan")
            self.play(GrowFromCenter(x), FadeIn(note), run_time=0.5)
            self.trap = VGroup(card, title, row, x, note)

    # -------------------------------------------------------- takeaway
    def takeaway(self):
        with self.beat("takeaway"):
            self.play(FadeOut(self.trap), run_time=0.5)
            card = Card(8.0, 6.8).move_to([0, 2.1, 0])
            head = T("Menghitung pasangan", size=48, weight=BLACK, color=THEME.purple).move_to([0, 4.95, 0])
            steps = VGroup(
                T("1. Pecah menjadi kelompok", size=36, weight=BLACK),
                M(r"6,\ 6,\ 20,\ 20", size=48),
                T("2. Pasangkan sesuai semua syarat", size=36, weight=BLACK),
                M(r"6 \times 20 + 6 \times 20 = 240", size=48, color=THEME.good),
                T("3. Bagi dengan semua pasangan", size=36, weight=BLACK),
                M(r"\frac{240}{1326} = \frac{40}{221}", size=52),
            ).arrange(DOWN, buff=0.22).move_to([0, 1.95, 0])
            self.play(FadeIn(card, shift=0.2 * UP), FadeIn(head), run_time=0.6)
            self.play(FadeIn(steps[:2], shift=0.15 * RIGHT), run_time=0.6)
            self.until("Pasangkan")
            self.play(FadeIn(steps[2:4], shift=0.15 * RIGHT), run_time=0.6)
            self.until("kalikan.")
            self.play(FadeIn(steps[4:], shift=0.15 * RIGHT), run_time=0.6)
            self.play(Circumscribe(steps[-1], color=THEME.good, buff=0.1), run_time=0.9)
