# Kinan Math Animation Studio

Animated, narrated mathematics explainers for vertical video (Instagram Reels,
TikTok, YouTube Shorts), built with **Manim Community Edition**, LaTeX and FFmpeg,
rendered automatically by **GitHub Actions** — nothing to install on your device.

| Video | Topic | Answer | Length |
|---|---|---|---|
| [`p00_poc_binomial`](problems/p00_poc_binomial/problem.md) | Proof of concept: (a + b)² as areas | — | 0:49 |
| [`p01_dadu_berbeda`](problems/p01_dadu_berbeda/problem.md) | Two dice, distinct faces, prime sum | **B. 7/15** | 3:02 |
| [`p02_tiga_koin`](problems/p02_tiga_koin/problem.md) | Three coins, at least one picture side | **B. 3/7** | 3:01 |
| [`p03_kartu_bridge`](problems/p03_kartu_bridge/problem.md) | Two bridge cards, one face card, different colours | **B. 40/221** | 3:09 |
| [`p04_empat_koin`](problems/p04_empat_koin/problem.md) | Four coins, exactly three number sides | **B. 1/4** | 4:16 |
| [`p05_spinner_koin`](problems/p05_spinner_koin/problem.md) | Spinner 1–6 and a coin: odd and picture | **B. 1/4** | 3:25 |
| [`p06_dua_dadu_atau`](problems/p06_dua_dadu_atau/problem.md) | Two dice: sum above 9 or a double | **B. 5/18** | 3:34 |
| [`p07_spinner_harapan`](problems/p07_spinner_harapan/problem.md) | 8-sector spinner, expected frequency of primes | **C. 72** | 3:35 |

Finished videos live in [`output/videos/`](output/videos) (MP4 + `.srt` subtitles);
quality-control frames and reports in [`output/qc/`](output/qc); the summary is in
[`output/QC_REPORT.md`](output/QC_REPORT.md).

P00–P03: male voice (`id-ID-ArdiNeural`), cream theme. P04–P07: female voice
(`id-ID-GadisNeural`), dark 3Blue1Brown theme (`theme: dark` in `narration.yaml`).

## Render a video (no installation needed)

1. Open the repository on GitHub → **Actions** → **Render math videos** → **Run workflow**.
2. Fill in the form:
   - **problems**: `p01_dadu_berbeda`, several ids separated by commas, or `all`
   - **quality**: `final` (1080×1920) or `preview` (540×960, faster)
   - **theme**: `kinan` (cream, like the reference video) or `dark` (3Blue1Brown style)
   - **narration**: generate the Indonesian voice-over (on by default)
   - **force**: re-render even if `output/videos` already has the finished video
   - **commit_outputs**: also commit the new video back into the repository
3. When the run is green, download the **math-videos-N** artifact at the bottom of
   the run page. It contains the MP4, subtitles and QC report. The run summary
   lists every video with resolution, duration and QC results.

> The *Run workflow* button appears once `.github/workflows/render.yml` is on the
> default branch (`main`). On `claude/**` branches every push also runs a smoke
> test automatically: it regenerates narration for changed scripts, commits the
> audio back to the branch, and renders every problem at preview quality.

A full render of a 3-minute problem takes about 7–10 minutes on a GitHub runner.

## Add a new problem

1. Create `problems/pNN_slug/` with
   - `problem.md`: the original question (verbatim), solution and an independent check,
   - `narration.yaml`: the beats (what is said, what is shown), see below.
2. Add `src/scenes/pNN_slug.py` with a `KinanScene` subclass (copy an existing one).
3. Add a brute-force check to `scripts/verify_math.py`.
4. Push, or run the workflow. Previously completed videos are never overwritten
   unless **force** is chosen.

### Narration script (`narration.yaml`)

```yaml
id: p01_dadu_berbeda
scene_file: src/scenes/p01_dadu_berbeda.py
scene_class: P01DaduBerbeda
voice: id-ID-ArdiNeural        # Microsoft Edge neural voice (Indonesian, male)
rate: "-4%"
beats:
  - id: doubles
    chapter: SYARAT             # starts a new segment of the progress bar
    visual: "Diagonal cells turn pink, then are struck through."
    say: "Pasangan kembar, satu satu, dua dua, ... tidak mungkin terjadi."   # spoken
    caption: "Pasangan kembar (1,1), (2,2), ... *tidak~mungkin*."         # on screen
```

- `say` is written the way it should be **pronounced** ("tujuh per lima belas"),
  `caption` the way it should be **read** ("7/15").
- In captions: `*word*` keeps a yellow marker after it is spoken, `|` starts a new
  caption page, `~` keeps tokens together on one line.

### Synchronising animation with speech

```python
with self.beat("doubles"):            # plays the audio, shows karaoke captions
    self.until("kembar")              # wait until that caption word is spoken
    self.play(...)                    # animate exactly then
# the beat waits for the narration to finish before the next one starts
```

Word timings come from the TTS engine (`assets/audio/<id>/timings.json`). Without
audio the timing is estimated from the text, so silent previews still work.

## Project layout

```
src/
  components/   theme (colour roles, 2 presets), text (Nunito + LaTeX), captions,
                progress bar, cards/tags/badges, probability objects, KinanScene base
  scenes/       one file per problem
  utils/        narration loading, timing, caption pagination
problems/       per problem: problem.md (verification), narration.yaml, storyboard.md
assets/
  audio/        generated voice-over (mp3 + word timings), committed by CI
  fonts/        Nunito (SIL Open Font License)
  images/       source worksheet
scripts/
  render.py       Manim → H.264/AAC MP4 (1080×1920, 30 fps, loudness-normalised)
  narrate.py      Indonesian TTS with per-word timings (edge-tts)
  qc.py           technical QC: format, A/V sync, loudness, black/frozen frames, frames for review
  storyboard.py   storyboard.md with real timestamps + full narration script
  verify_math.py  brute-force check of every answer
output/
  videos/       final MP4 + SRT
  qc/           contact sheets, per-beat frames, beats.json, qc.json
.github/workflows/render.yml
```

## Local rendering (optional)

```bash
sudo apt-get install ffmpeg libcairo2-dev libpango1.0-dev texlive-latex-extra \
    texlive-fonts-recommended texlive-science dvisvgm cm-super
pip install -r requirements.txt
python scripts/narrate.py p01_dadu_berbeda      # needs internet
python scripts/render.py p01_dadu_berbeda --quality preview
```

## Ganti suara narator (voice swap)

[`voice_swap/`](voice_swap/README.md) mengganti **hanya suara narator** pada video yang sudah jadi dengan suara
pemilik (Seed-VC, speech-to-speech), tanpa menyentuh gambar. Rekaman suara pribadi tidak pernah disimpan di
repositori ini.

## Credits

- Visual language inspired by the provided reference explainer (cream canvas, bold
  rounded type, karaoke captions, segmented progress); mathematical approach
  inspired by 3Blue1Brown. All illustrations are generated in code.
- Font: Nunito by the Nunito Project Authors, SIL Open Font License 1.1.
- Voice: Microsoft Edge neural TTS (`id-ID-ArdiNeural`) via `edge-tts`.
