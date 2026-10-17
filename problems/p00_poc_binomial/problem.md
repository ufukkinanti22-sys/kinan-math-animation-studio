# P00 — Proof of concept: (a + b)² = a² + 2ab + b²

A short video used to verify the whole pipeline (design system, karaoke captions,
LaTeX, narration timing, rendering, H.264 encoding, CI artifact) before the real
problems were produced.

## Mathematics

A square of side a + b has area (a + b)². Cutting it at distance a from one corner,
horizontally and vertically, gives four non-overlapping regions: a square a², a square
b², and two rectangles a × b. Areas add, so (a + b)² = a² + 2ab + b² for all a, b > 0
(and, as a polynomial identity, for all real a, b). The common mistake
(a + b)² = a² + b² misses exactly the two rectangles, 2ab.

Storyboard and narration: [`storyboard.md`](storyboard.md) · Video: `output/videos/p00_poc_binomial.mp4`
