# P05 — Spinner dan koin, ganjil dan gambar

**Sumber:** Lembar Guru — Bagian 1 & 2, Peluang HOTS, soal 2 (gambar lembar kerja yang dikirim).

## Soal asli (ditampilkan apa adanya di video)

> Sebuah spinner bernomor 1 sampai 6 dan sebuah koin dilempar bersamaan. Peluang muncul
> bilangan ganjil pada spinner dan sisi gambar pada koin adalah ...
>
> A. 1/6  B. 1/4  C. 1/3  D. 1/2

## Asumsi

Soal tidak menyebut "sama besar", tetapi spinner pada lembar kerja digambar dengan enam
sektor sama besar. Video memakai asumsi ini dan menyebutkannya. Tanpa asumsi ini peluang
tidak bisa ditentukan.

## Analisis

- **Diketahui:** spinner 1–6 (sektor sama besar), koin setimbang (G = gambar, A = angka).
- **Ditanya:** P(spinner ganjil **dan** koin G).
- **Prasyarat:** ruang sampel gabungan (tabel), kejadian saling bebas.

## Penyelesaian

1. Ruang sampel: 6 × 2 = 12 pasangan sama mungkin.
2. Ganjil: 1, 3, 5. Pasangan yang cocok: (1, G), (3, G), (5, G) → 3.
3. **P = 3/12 = 1/4 → jawaban B**.

## Verifikasi independen

- **Aturan perkalian (saling bebas):** P(ganjil) × P(G) = 3/6 × 1/2 = 1/4 ✓
  (model luas: setengah persegi × setengah persegi = seperempat).
- **Enumerasi komputer:** 1/4 ✓.
- **Jebakan:** 1/2 jika hanya melihat spinner; 1/6 jika menganggap ruang sampel 6.

## Ide visual utama

Spinner dengan sektor genap meredup, koin G menyala, kata DAN, tabel 6 × 2; kolom ganjil
berpotongan dengan baris G menyisakan 3 kotak. Pengecekan dengan model luas ½ × ½.

Naskah narasi: [`narration.yaml`](narration.yaml), [`naskah_rekaman.txt`](naskah_rekaman.txt) · Video: `output/videos/p05_spinner_koin.mp4`
