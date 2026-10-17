"""Typography helpers: rounded bold UI text (Nunito) and LaTeX mathematics."""

from __future__ import annotations

from pathlib import Path

import manimpango
from manim import MathTex, Tex, TexTemplate, Text, VGroup

from .theme import THEME

FONT_DIR = Path(__file__).resolve().parents[2] / "assets" / "fonts"

BOLD = "Kinan Nunito Bold"
HEAVY = "Kinan Nunito ExtraBold"
BLACK = "Kinan Nunito Black"
SYMBOL = "DejaVu Sans"  # card suits and other glyphs outside the Latin subset

for _font in sorted(FONT_DIR.glob("*.ttf")):
    manimpango.register_font(str(_font))

# Scale so that ``size`` is roughly the cap height in pixels at 1080x1920.
_PX = 1 / 120  # one pixel in Manim units (frame is 9 units wide)


def T(text: str, size: float = 40, color: str | None = None, weight: str = HEAVY, **kw) -> Text:
    """Rounded UI text. ``size`` ~ font size in pixels on the final 1080p video."""
    # one submobject per character (spaces included) so glyphs can be sliced by index
    kw.setdefault("disable_ligatures", True)
    t = Text(text, font=weight, color=color or THEME.ink, font_size=100, **kw)
    t.scale(size * _PX * 0.72 / _cap_height(weight))  # capital letters ~ 0.72*size px tall
    return t


_CAP: dict[str, float] = {}


def _cap_height(font: str) -> float:
    """Height of a capital 'H' at font_size=100 (cached per font)."""
    if font not in _CAP:
        _CAP[font] = Text("H", font=font, font_size=100).height
    return _CAP[font]


_TEX_CAP: list[float] = []


def _tex_cap_height() -> float:
    if not _TEX_CAP:
        _TEX_CAP.append(MathTex("H", font_size=100).height)
    return _TEX_CAP[0]


def _make_template() -> TexTemplate:
    tpl = TexTemplate()
    tpl.add_to_preamble(r"\usepackage{amssymb}")
    return tpl


TEX_TEMPLATE = _make_template()


def M(*tex: str, size: float = 56, color: str | None = None, weight: float = 1.4, **kw) -> MathTex:
    """LaTeX maths. ``size`` ~ font size in px; ``weight`` adds a thin stroke so
    Computer Modern stays legible on a phone screen."""
    m = MathTex(*tex, color=color or THEME.ink, tex_template=TEX_TEMPLATE, font_size=100, **kw)
    m.scale(size * _PX * 0.72 / _tex_cap_height())
    m.set_stroke(color=color or THEME.ink, width=weight)
    return m


def recolor(m: MathTex, index: int, color: str) -> MathTex:
    """Colour one sub-expression of a MathTex (fill and its emboldening stroke)."""
    m[index].set_fill(color).set_stroke(color)
    return m


def TT(text: str, size: float = 40, color: str | None = None, **kw) -> Tex:
    """LaTeX text mode (rarely needed; prefer :func:`T`)."""
    t = Tex(text, color=color or THEME.ink, tex_template=TEX_TEMPLATE, font_size=100, **kw)
    t.scale(size * _PX * 0.72 / _tex_cap_height())
    return t


def lines(*rows: str, size: float = 40, color: str | None = None, weight: str = HEAVY,
          buff: float = 0.18, align: str = "left") -> VGroup:
    """Several lines of text stacked with consistent spacing."""
    from manim import DOWN, LEFT, ORIGIN

    g = VGroup(*[T(r, size=size, color=color, weight=weight) for r in rows])
    g.arrange(DOWN, buff=buff, aligned_edge=LEFT if align == "left" else ORIGIN)
    return g


def wrap(text: str, max_chars: int) -> list[str]:
    """Greedy word wrap to lines of at most ``max_chars`` characters."""
    out: list[str] = []
    cur = ""
    for w in text.split():
        if cur and len(cur) + 1 + len(w) > max_chars:
            out.append(cur)
            cur = w
        else:
            cur = f"{cur} {w}".strip()
    if cur:
        out.append(cur)
    return out


def wrap_lines(text: str, max_chars: int = 34, size: float = 36, color: str | None = None,
               weight: str = HEAVY, buff: float = 0.2) -> VGroup:
    return lines(*wrap(text, max_chars), size=size, color=color, weight=weight, buff=buff)


class Frac(VGroup):
    """Stacked fraction built from separate parts (``num``, ``bar``, ``den``) so
    numerator and denominator can be animated independently."""

    def __init__(self, num, den, size: float = 64, color: str | None = None, **kw):
        from manim import DOWN, Line, UP

        super().__init__(**kw)
        c = color or THEME.ink
        self.num = num if isinstance(num, VGroup) else M(str(num), size=size, color=c)
        self.den = den if isinstance(den, VGroup) else M(str(den), size=size, color=c)
        w = max(self.num.width, self.den.width) + size / 120 * 0.35
        self.bar = Line([-w / 2, 0, 0], [w / 2, 0, 0]).set_stroke(c, size / 120 * 7)
        self.num.next_to(self.bar, UP, buff=size / 120 * 0.22)
        self.den.next_to(self.bar, DOWN, buff=size / 120 * 0.22)
        self.add(self.num, self.bar, self.den)
