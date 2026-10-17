# P02 — Tiga koin, sedikitnya satu gambar

**Sumber:** Lembar Guru — Matematika SMP, Peluang Tingkat Tinggi, soal 2
(`assets/images/lembar-guru-peluang-tingkat-tinggi.png`).

## Soal asli (ditampilkan apa adanya di video)

> Tiga koin fair dilempar bersamaan. Jika diketahui sedikitnya satu sisi gambar muncul,
> peluang tepat dua sisi gambar adalah ...
>
> A. 2/7  B. 3/7  C. 4/7  D. 1/2

## Analisis

- **Notasi:** G = sisi gambar, A = sisi angka; masing-masing ½ (koin fair).
- **Diketahui:** syarat *B*: sedikitnya satu G.
- **Ditanya:** P(A₂ | B), dengan *A₂*: tepat dua G.
- **Prasyarat:** diagram pohon / aturan perkalian, peluang bersyarat, arti "sedikitnya" vs "tepat".

## Penyelesaian

1. Ruang sampel: 2 × 2 × 2 = 8 hasil sama mungkin
   (GGG, GGA, GAG, GAA, AGG, AGA, AAG, AAA).
2. Syarat B membuang satu-satunya hasil tanpa G, yaitu AAA: n(B) = 7.
3. Tepat dua G: GGA, GAG, AGG → 3 hasil, semuanya di dalam B.
4. **P(A₂ | B) = 3/7 → jawaban B**.

## Verifikasi independen

- **Rumus:** A₂ ⊂ B, jadi A₂ ∩ B = A₂ dan
  P(A₂ | B) = P(A₂) / P(B) = (3/8) / (7/8) = 3/7 ✓.
- **Struktur binomial:** banyak G per hasil menyebar 1, 3, 3, 1 (C(3,k));
  syarat membuang kelompok 0 → 3 + 3 + 1 = 7, yang tepat dua = 3 ✓.
- **Enumerasi komputer:** 3/7 ✓.
- **Jebakan:** tanpa syarat, peluangnya 3/8, tidak ada di pilihan.

## Ide visual utama

Diagram pohon menghasilkan 8 jalur; syarat mencoret jalur AAA. Pengecekan
mengelompokkan ulang hasil menjadi 1-3-3-1 dan memakai diagram Venn (A di dalam B).

Storyboard dan naskah narasi: [`storyboard.md`](storyboard.md) · Video: `output/videos/p02_tiga_koin.mp4`
