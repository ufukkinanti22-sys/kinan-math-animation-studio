# P07 — Spinner 8 sektor, frekuensi harapan bilangan prima

**Sumber:** Lembar Guru — Bagian 1 & 2, Peluang HOTS, soal 4 (gambar lembar kerja yang dikirim).

## Soal asli (ditampilkan apa adanya di video)

> Sebuah spinner dengan 8 sektor sama besar bernomor 1 sampai 8 diputar 144 kali.
> Frekuensi harapan muncul bilangan prima adalah ...
>
> A. 54  B. 64  C. 72  D. 81

## Analisis

- **Ditanya:** frekuensi harapan = P(prima) × banyak percobaan.
- **Prasyarat:** definisi bilangan prima (tepat dua pembagi; 1 bukan prima).

## Penyelesaian

1. Bilangan prima 1–8: 2, 3, 5, 7 → 4 dari 8 sektor.
2. P(prima) = 4/8 = 1/2.
3. **Fh = 1/2 × 144 = 72 → jawaban C**.

## Verifikasi independen

- **Pembagi:** 1 (satu pembagi), 4 = 2·2, 6 = 2·3, 8 = 2·4 bukan prima ✓.
- **Gambar:** 144 titik (12 × 12), separuhnya 72 ✓.
- **Komputer:** 4/8 × 144 = 72 ✓.
- **Jebakan:** jika 1 dianggap prima, 5/8 × 144 = 90 (tidak ada di pilihan).

## Ide visual utama

Contoh 10 koin → 10 × ½ = 5, rumus frekuensi harapan, spinner yang sektornya menyala hijau
untuk bilangan prima, 144 titik dengan 72 menyala, garis bilangan untuk "perkiraan".

Naskah narasi: [`narration.yaml`](narration.yaml), [`naskah_rekaman.txt`](naskah_rekaman.txt) · Video: `output/videos/p07_spinner_harapan.mp4`
