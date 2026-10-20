# P06 — Dua dadu, jumlah lebih dari 9 atau kembar

**Sumber:** Lembar Guru — Bagian 1 & 2, Peluang HOTS, soal 3 (gambar lembar kerja yang dikirim).

## Soal asli (ditampilkan apa adanya di video)

> Dua dadu dilempar bersamaan. Peluang jumlah mata dadu lebih dari 9 atau kedua mata dadu
> sama adalah ...
>
> A. 1/4  B. 5/18  C. 7/18  D. 11/18

## Analisis

- **Kejadian K:** jumlah > 9, yaitu 10, 11, 12 (9 tidak termasuk).
- **Kejadian L:** kedua mata sama (kembar).
- **Ditanya:** P(K atau L) = P(K ∪ L).
- **Prasyarat:** tabel 6 × 6, arti "lebih dari", gabungan dua kejadian.

## Penyelesaian

1. Ruang sampel: 6 × 6 = 36 pasangan.
2. K: (4,6), (5,5), (6,4), (5,6), (6,5), (6,6) → 6.
3. L: (1,1) … (6,6) → 6.
4. Terhitung dua kali (K dan L): (5,5), (6,6) → 2.
5. n(K ∪ L) = 6 + 6 − 2 = 10. **P = 10/36 = 5/18 → jawaban B**.

## Verifikasi independen

- **Hitung ulang langsung** di tabel (setiap kotak sekali): 10 ✓.
- **Rumus:** P(K) + P(L) − P(K ∩ L) = 6/36 + 6/36 − 2/36 = 10/36 ✓.
- **Enumerasi komputer:** 5/18 ✓.
- **Jebakan:** 12/36 = 1/3 jika irisan tidak dikurangi (tidak ada di pilihan);
  jika "lebih dari 9" dibaca "9 atau lebih", hasilnya 14/36 = 7/18 (pilihan C).

## Ide visual utama

Garis bilangan dengan 9 dicoret, diagram Venn, tabel jumlah 6 × 6; kotak jumlah > 9
berwarna oranye, kembar dilingkari biru; (5,5) dan (6,6) berkedip karena terhitung dua kali.

Naskah narasi: [`narration.yaml`](narration.yaml), [`naskah_rekaman.txt`](naskah_rekaman.txt) · Video: `output/videos/p06_dua_dadu_atau.mp4`
