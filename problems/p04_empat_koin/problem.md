# P04 — Empat koin, tepat tiga angka

**Sumber:** Lembar Guru — Bagian 1 & 2, Peluang HOTS, soal 1 (gambar lembar kerja yang dikirim).

## Soal asli (ditampilkan apa adanya di video)

> Empat koin setimbang dilempar bersamaan. Peluang tepat tiga sisi angka adalah ...
>
> A. 1/8  B. 1/4  C. 3/8  D. 1/2

## Analisis

- **Notasi:** A = sisi angka, G = sisi gambar; masing-masing ½ (koin setimbang).
- **Ditanya:** P(tepat tiga A).
- **Prasyarat:** ruang sampel, aturan perkalian (2 × 2 × 2 × 2), arti "tepat".

## Penyelesaian

1. Ruang sampel: 2⁴ = 16 hasil sama mungkin.
2. Tepat tiga A berarti tepat satu G. G bisa di koin ke-1, 2, 3 atau 4:
   GAAA, AGAA, AAGA, AAAG → 4 hasil.
3. **P = 4/16 = 1/4 → jawaban B**.

## Verifikasi independen

- **Kombinasi:** C(4,3) = 4, jadi P = 4/16 ✓.
- **Kelompok binomial:** banyak A per hasil menyebar 1, 4, 6, 4, 1 (jumlah 16);
  kelompok "tiga A" berisi 4 ✓.
- **Enumerasi komputer** (`scripts/verify_math.py`): 1/4 ✓.
- **Jebakan:** 1/8 muncul jika hanya menghitung satu urutan (mis. AAAG) dan lupa
  bahwa posisi G bisa berbeda-beda; 3/8 adalah peluang tepat dua A.

## Ide visual utama

Pemanasan dua koin (AA, AG, GA, GG), lalu kotak yang berlipat ganda 2 → 4 → 8 → 16.
Daftar 16 hasil; satu G dilingkari di tiap hasil yang cocok. Pengecekan dengan
kelompok 1-4-6-4-1.

Naskah narasi: [`narration.yaml`](narration.yaml), [`naskah_rekaman.txt`](naskah_rekaman.txt) · Video: `output/videos/p04_empat_koin.mp4`
