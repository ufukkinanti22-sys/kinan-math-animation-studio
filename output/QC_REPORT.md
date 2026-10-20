# Quality-control report

Date: 2026-10-17 · Renderer: Manim CE 0.19.0 (Cairo) · Encoder: FFmpeg libx264 High / AAC 48 kHz

| Video | Duration | Answer shown | Automated QC | Narration |
|---|---|---|---|---|
| `p00_poc_binomial.mp4` | 0:49 | (a+b)² = a² + 2ab + b² | 12/12 pass | 6/6 beats |
| `p01_dadu_berbeda.mp4` | 3:02 | B. 7/15 | 12/12 pass | 21/21 beats |
| `p02_tiga_koin.mp4` | 3:01 | B. 3/7 | 12/12 pass | 20/20 beats |
| `p03_kartu_bridge.mp4` | 3:09 | B. 40/221 | 12/12 pass | 21/21 beats |
| `p04_empat_koin.mp4` | 4:16 | B. 1/4 | 12/12 pass | 20/20 beats |
| `p05_spinner_koin.mp4` | 3:25 | B. 1/4 | 12/12 pass | 18/18 beats |
| `p06_dua_dadu_atau.mp4` | 3:34 | B. 5/18 | 12/12 pass | 17/17 beats |
| `p07_spinner_harapan.mp4` | 3:35 | C. 72 | 12/12 pass | 15/15 beats |

Per-video details: `output/qc/<id>/qc.json`, `contact_sheet.jpg`, `beats/*.jpg`
(last frame of every narration beat), `beats.json` (actual beat timings).

## Mathematical QC

- Every answer was solved by hand and checked independently: P1 by unordered pairs
  (7 of 15), P2 by the 1-3-3-1 grouping and by P(A|B) = P(A)/P(B) with A ⊂ B,
  P3 by sequential drawing 4 × (6/52)(20/51). See `problems/<id>/problem.md`.
- `scripts/verify_math.py` brute-forces all three answers (36 dice pairs, 8 coin
  outcomes, all 1326 card pairs). It runs in CI before every render.
- The original questions are shown verbatim (checked against the worksheet image);
  all options shown match the worksheet.
- Every displayed equation and intermediate value was re-read on the rendered
  frames: n(S) = 30, 2 + 4 + 6 + 2 = 14, 14/30 = 7/15; 8 − 1 = 7, 3/7,
  (3/8)/(7/8) = 3/7; 6 × 20 = 120 (twice) = 240, C(52,2) = 1326, ÷6 → 40/221,
  480/2652 = 40/221; traps 5/12, 3/8 and 20/221.

## Technical QC (automated, `scripts/qc.py`)

- Container/codec: H.264 High, yuv420p, 30 fps, 1080 × 1920 (9:16), `+faststart`.
- Audio present, loudness-normalised (mean ≈ −19.6 dB, peaks −2.5 … −4.5 dBFS).
- **A/V sync:** speech onset detected 0.2–0.3 s after every beat start (the voice's
  own lead-in), and every beat boundary falls in silence, so no speech is cut or
  overlapped. The check was validated with a deliberately broken timeline, which it fails.
- No black frames; no frozen stretch longer than 12 s.

## Visual QC (frames inspected by eye)

Checked contact sheets and per-beat frames at preview and final resolution.

**Problems found and fixed during production**

| Issue | Fix |
|---|---|
| Caption words highlighted with an offset; line ends cut | Glyphs are sliced per character, spaces included |
| Math expressions split across caption lines | `~` non-breaking joiner in captions |
| Pair labels and sums hidden behind table cells after `Indicate` | Explicit z-order (cells < labels < strikes) |
| Question highlights shifted by 2 characters | One glyph per character in all text |
| Highlighter briefly covering words while fading in | Card text drawn above markers |
| Option fractions too small (`\tfrac`) | `\frac`, larger cards |
| LaTeX `\varheartsuit` not available | Card pair label drawn as text glyphs |
| False "speech overrun" alarms in QC | Silence intervals parsed in order; end of audio stream counts as silence |

## Known limitations

- Narration is generated with Microsoft Edge neural TTS (`id-ID-ArdiNeural`).
  The sound check is automated (onset, overlap, loudness); nobody has listened
  to it, so pronunciation of letters (G, A, J, Q, K) should get one human listen.
- Some intermediate frames show text morphing into numbers (e.g. a card label
  becoming 6/52). These are transitions; all settled states were checked.
- Text uses Nunito; card suits ♠♥♦♣ come from DejaVu Sans (font fallback).

## P04–P07 (Lembar Guru, Bagian 1 & 2, Peluang HOTS) — 2026-10-20

- **Voice:** female `id-ID-GadisNeural` (Edge neural TTS, free), rate −8 %, on all
  70 beats (checked in every `timings.json`). Independent pitch check: median F0
  235–239 Hz on all four (female range); the old male P01 narration measures 108 Hz.
- **Theme:** dark 3Blue1Brown palette (navy `#101523`, white text, blue / yellow /
  green / red accents), LaTeX for all math.
- **Math:** answers solved by hand and brute-forced in `scripts/verify_math.py`
  (16 coin outcomes, 12 spinner–coin pairs, 36 dice pairs, primes 1–8 × 144).
  P05 assumes the six spinner sectors are equal, as drawn on the worksheet; the
  video says so. Traps shown: 1/8 and 3/8 (P04), 12/36 without removing the
  double count (P06), 90 if 1 is counted as prime (P07).
- **Automated QC:** 12/12 per video (H.264, 1080 × 1920, 30 fps, AAC, every beat
  voiced, speech onset at every beat, no speech cut, no black or frozen frames).
- **Visual fixes found while checking frames:** spinner numbers hidden by sector
  pulses (z-order); option fraction recoloured into its card while being read
  (now an outline); answer result briefly overlapping the option cards (now moves
  first); low-contrast chapter pill and white-on-yellow text in the dark theme
  (new `label` / `mark` colour roles).
