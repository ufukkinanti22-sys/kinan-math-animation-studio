"""Karaoke captions synchronised with the narration.

Words already spoken are dark, upcoming words are muted, and the word being
spoken sits on a yellow box (reference-video style). Words marked ``*key*`` in
the script keep a soft yellow marker after they are spoken.

Each caption line is typeset as one ``Text`` (correct kerning and baseline);
glyphs are then sliced per word so words can be coloured individually.
"""

from __future__ import annotations

from manim import RoundedRectangle, VGroup

from ..utils.narration import Beat
from .text import HEAVY, T
from .theme import THEME

CAPTION_Y = -4.7  # centre of the caption block (lower third, above platform UI)
MAX_CHARS = 26  # per line at SIZE; keeps lines inside the safe width
SIZE = 54
FADE_IN = 0.18


def _rows(words: list[str], max_chars: int) -> list[list[int]]:
    rows: list[list[int]] = [[]]
    n = 0
    for i, w in enumerate(words):
        if rows[-1] and n + 1 + len(w) > max_chars:
            rows.append([])
            n = 0
        n += len(w) + (1 if rows[-1] else 0)
        rows[-1].append(i)
    return rows


class KaraokeCaption(VGroup):
    def __init__(self, beat: Beat, y: float = CAPTION_Y, size: float = SIZE, **kw):
        super().__init__(**kw)
        self.beat = beat
        self.pages: list[dict] = []
        cap = size * 0.72 / 120
        line_step = cap * 2.15
        for page in beat.pages:
            texts = [w.text for w in page.words]
            rows = _rows(texts, MAX_CHARS)
            words: list[VGroup] = [None] * len(texts)  # type: ignore[list-item]
            boxes: list[RoundedRectangle] = [None] * len(texts)  # type: ignore[list-item]
            lines = VGroup()
            for r, idx in enumerate(rows):
                line = T("H " + " ".join(texts[i] for i in idx), size=size, weight=HEAVY,
                         disable_ligatures=True)
                # Text keeps one submobject per character, spaces included
                ref, glyphs = line[0], line[2:]
                base = ref.get_bottom()[1]
                k = 0
                row = VGroup()
                for i in idx:
                    n = len(texts[i])
                    word = VGroup(*glyphs[k:k + n])
                    k += n + 1
                    words[i] = word
                    row.add(word)
                # centre the row horizontally, baselines on a common grid
                row.shift([-row.get_center()[0], -base - r * line_step, 0])
                for i in idx:
                    w = words[i]
                    b = RoundedRectangle(width=w.width + 0.18, height=cap * 1.75, corner_radius=0.08,
                                         fill_color=THEME.hl, fill_opacity=0, stroke_width=0)
                    b.move_to([w.get_center()[0], -r * line_step + cap / 2, 0])
                    boxes[i] = b
                lines.add(row)
            group = VGroup(VGroup(*boxes), lines)
            group.shift([0, y - (cap / 2 - (len(rows) - 1) * line_step / 2), 0])
            group.set_opacity(0)
            self.pages.append({"page": page, "words": words, "boxes": boxes,
                               "group": group, "state": None})
            self.add(group)
        self.clock = 0.0
        self.set_z_index(50)
        self.add_updater(self._tick)

    def _tick(self, m, dt):
        self.clock += dt
        t = self.clock
        last = len(self.pages) - 1
        for p, entry in enumerate(self.pages):
            page = entry["page"]
            visible = page.start <= t and (t < page.end or p == last)
            if not visible:
                if entry["state"] != "hidden":
                    entry["group"].set_opacity(0)
                    entry["state"] = "hidden"
                continue
            current = -1
            for i, w in enumerate(page.words):
                if w.start <= t:
                    current = i
            # after the final word of the beat is spoken, let the line rest (no box)
            if p == last and current == len(page.words) - 1 and t > self.beat.speech + 0.2:
                current = len(page.words)
            fade = min(1.0, (t - page.start) / FADE_IN)
            state = (current, round(fade, 2))
            if entry["state"] == state:
                continue
            entry["state"] = state
            for i, (word, box) in enumerate(zip(entry["words"], entry["boxes"])):
                key = page.words[i].key
                if i == current:
                    word.set_fill(THEME.hl_text, opacity=fade)
                    box.set_fill(THEME.hl, opacity=fade)
                elif i < current:
                    word.set_fill(THEME.ink, opacity=fade)
                    box.set_fill(THEME.soft_yellow, opacity=fade if key else 0)
                else:
                    word.set_fill(THEME.muted, opacity=fade)
                    box.set_fill(THEME.hl, opacity=0)
                word.set_stroke(opacity=0)
