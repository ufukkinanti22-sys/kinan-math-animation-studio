# P03 — Dua kartu bridge: tepat satu bergambar, warna berbeda

**Sumber:** Lembar Guru — Matematika SMP, Peluang Tingkat Tinggi, soal 3
(`assets/images/lembar-guru-peluang-tingkat-tinggi.png`).

## Soal asli (ditampilkan apa adanya di video)

> Dua kartu diambil sekaligus dari satu set kartu Bridge standar (52 kartu) tanpa joker.
> Peluang tepat satu kartu bergambar (J, Q, atau K) dan kedua kartu berlainan warna adalah ...
>
> A. 20/221  B. 40/221  C. 60/221  D. 80/221

## Analisis

- **Diketahui:** 52 kartu = 4 jenis × 13; hati & wajik merah, sekop & keriting hitam.
  Kartu bergambar = J, Q, K (12 kartu: 6 merah, 6 hitam). Tidak bergambar: 40 (20 merah, 20 hitam).
- **"Sekaligus":** urutan tidak penting → hitung pasangan (kombinasi).
- **Ditanya:** P(tepat satu bergambar **dan** warna berbeda).
- **Prasyarat:** kombinasi C(n, 2), aturan perkalian, peluang klasik.
- **Catatan:** kedua syarat harus dipenuhi bersamaan (irisan), bukan peluang bersyarat.

## Penyelesaian

1. Kelompok: merah-bergambar 6, hitam-bergambar 6, merah-tidak 20, hitam-tidak 20.
2. Tepat satu bergambar + warna berbeda ⇔ (merah-bergambar & hitam-tidak) atau
   (hitam-bergambar & merah-tidak): 6 × 20 + 6 × 20 = 240 pasangan.
3. Semua pasangan: C(52, 2) = 52 × 51 / 2 = 1326.
4. **P = 240/1326 = 40/221 → jawaban B** (dibagi 6; 221 = 13 × 17, 40 = 2³ × 5, tidak bisa disederhanakan lagi).

## Verifikasi independen

- **Pengambilan berurutan:** 2 kombinasi warna × 2 urutan = 4 susunan, masing-masing
  (6/52)(20/51); total 4 × 120/2652 = 480/2652 = 40/221 ✓.
- **Enumerasi komputer:** 1326 pasangan diperiksa, 240 cocok → 40/221 ✓.
- **Jebakan:** hanya satu kombinasi warna → 120/1326 = 20/221 (pilihan A).

## Ide visual utama

52 kartu berpindah menjadi tabel 2 × 2 (6, 6, 20, 20). Syarat "tepat satu bergambar"
menghubungkan baris atas–bawah, "warna berbeda" memaksa hubungan diagonal; pasangan
antar-kelompok ditampilkan sebagai persegi panjang titik 6 × 20.

Storyboard dan naskah narasi: [`storyboard.md`](storyboard.md) · Video: `output/videos/p03_kartu_bridge.mp4`
