"""Design system: semantic colour roles shared by every scene.

Scenes never use raw hex colours; they ask the active theme for a role
(``THEME.ink``, ``THEME.good`` ...). Two presets exist:

* ``kinan`` (default): warm cream explainer look of the reference video.
* ``dark``: 3Blue1Brown-inspired navy background with bright accents.

Select with the environment variable ``KINAN_THEME`` (``kinan`` | ``dark``).
"""

from __future__ import annotations

import os
from dataclasses import dataclass


@dataclass(frozen=True)
class Theme:
    name: str
    bg: str  # page background
    ink: str  # primary text and outlines
    muted: str  # not-yet-spoken caption words, faded objects
    faint: str  # empty progress segments, guides
    hl: str  # yellow emphasis (current caption word, markers)
    hl_text: str  # text drawn on top of the yellow emphasis
    good: str  # green: favourable outcome, correct answer, progress
    warn: str  # orange: secondary quantity
    bad: str  # coral: excluded outcome, wrong answer
    blue: str  # first quantity / variable
    purple: str  # chapter labels, secondary accent
    card: str  # card fill
    card_stroke: str
    shadow: str
    soft_blue: str
    soft_green: str
    soft_red: str
    soft_yellow: str
    soft_orange: str
    soft_purple: str
    red_suit: str  # playing-card red
    black_suit: str  # playing-card black


KINAN = Theme(
    name="kinan",
    bg="#F8F5EF",
    ink="#201C32",
    muted="#C4BEB3",
    faint="#E4DED3",
    hl="#FFD447",
    hl_text="#201C32",
    good="#35C79D",
    warn="#E99927",
    bad="#F46B70",
    blue="#4F7CF0",
    purple="#7B61FF",
    card="#FFFFFF",
    card_stroke="#201C32",
    shadow="#201C32",
    soft_blue="#DDEAFF",
    soft_green="#D6F5EA",
    soft_red="#FDE0E1",
    soft_yellow="#FFF1C2",
    soft_orange="#FCE6C8",
    soft_purple="#ECE6FF",
    red_suit="#E5484D",
    black_suit="#201C32",
)

DARK = Theme(
    name="dark",
    bg="#101523",
    ink="#F5F5F5",
    muted="#5C6478",
    faint="#2A3147",
    hl="#FFFF00",
    hl_text="#101523",
    good="#83C167",
    warn="#F0AC5F",
    bad="#FC6255",
    blue="#58C4DD",
    purple="#9A72AC",
    card="#1A2134",
    card_stroke="#58C4DD",
    shadow="#05070D",
    soft_blue="#1E3A4F",
    soft_green="#23402F",
    soft_red="#4A2329",
    soft_yellow="#4A4620",
    soft_orange="#4A3520",
    soft_purple="#2E2745",
    red_suit="#FC6255",
    black_suit="#F5F5F5",
)

THEMES = {"kinan": KINAN, "dark": DARK}

THEME: Theme = THEMES.get(os.environ.get("KINAN_THEME", "kinan").lower(), KINAN)
