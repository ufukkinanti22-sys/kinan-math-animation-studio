# P01 — Dua dadu, mata berbeda, jumlah prima

**Sumber:** Lembar Guru — Matematika SMP, Peluang Tingkat Tinggi, soal 1
(`assets/images/lembar-guru-peluang-tingkat-tinggi.png`).

## Soal asli (ditampilkan apa adanya di video)

> Dua dadu fair dilempar bersamaan. Diketahui kedua mata dadu berbeda.
> Peluang jumlah mata dadu merupakan bilangan prima adalah ...
>
> A. 1/3  B. 7/15  C. 8/15  D. 17/30

## Analisis

- **Diketahui:** dua dadu fair (36 pasangan berurutan, sama mungkin); syarat *B*: kedua mata berbeda.
- **Ditanya:** P(A | B), dengan *A*: jumlah mata prima.
- **Konsep prasyarat:** ruang sampel pasangan berurutan, peluang bersyarat
  P(A | B) = n(A ∩ B) / n(B) (berlaku karena semua titik sampel sama mungkin), bilangan prima.

## Penyelesaian

1. n(S) = 6 × 6 = 36. Pasangan kembar (1,1), …, (6,6) melanggar syarat, jadi n(B) = 36 − 6 = 30.
2. Jumlah berada di 2…12; yang prima: 2, 3, 5, 7, 11.
3. Hitung pasangan berbeda untuk setiap jumlah prima:
   - 2: hanya (1,1), kembar → 0
   - 3: (1,2), (2,1) → 2
   - 5: (1,4), (4,1), (2,3), (3,2) → 4
   - 7: (1,6), (6,1), (2,5), (5,2), (3,4), (4,3) → 6
   - 11: (5,6), (6,5) → 2
4. n(A ∩ B) = 2 + 4 + 6 + 2 = 14, sehingga **P(A | B) = 14/30 = 7/15 → jawaban B**.

## Verifikasi independen

- **Pasangan tanpa urutan:** dengan syarat berbeda, setiap pasangan tak berurutan {a, b} (a ≠ b)
  sama mungkin (masing-masing 2/30). Ada C(6,2) = 15 pasangan; yang jumlahnya prima:
  {1,2}, {1,4}, {2,3}, {1,6}, {2,5}, {3,4}, {5,6} = 7. Peluang 7/15 ✓.
- **Enumerasi komputer:** semua 36 pasangan diperiksa (`a != b` dan `a+b` prima): 14/30 = 7/15 ✓.
- **Jebakan:** tanpa syarat, peluangnya 15/36 = 5/12 (termasuk (1,1)), tidak ada di pilihan.

## Ide visual utama

Tabel 6 × 6: syarat menghapus diagonal; jumlah yang sama terletak pada garis miring
(anti-diagonal), jadi jumlah prima menyala sebagai garis utuh 2, 4, 6, 2 kotak.

Storyboard dan naskah narasi: [`storyboard.md`](storyboard.md) · Video: `output/videos/p01_dadu_berbeda.mp4`
