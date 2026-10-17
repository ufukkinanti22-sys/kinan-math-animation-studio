# Storyboard — Dua dadu, mata berbeda, jumlah prima

Durasi video final: **3:02.6** · 1080×1920 · 30 fps · suara: `id-ID-ArdiNeural` (rate -4%)

Waktu diambil dari render terakhir (`output/qc/<id>/beats.json`). Setiap baris adalah satu *beat*: narasi, teks layar, dan animasinya berjalan bersamaan.

## TANTANGAN

**1. `hook`** · 0:00.0 – 0:09.3

- **Animasi:** Two dice drop and bounce (2 and 5); a red ≠ appears with the tag 'petunjuk: mata dadu berbeda'; a purple question mark pops above.
- **Narasi:** Dua dadu dilempar, dan kita diberi satu petunjuk: kedua mata dadunya berbeda. Apakah petunjuk ini mengubah peluangnya?
- **Teks layar:** Dua dadu dilempar, dan kita diberi satu *petunjuk*: kedua mata dadunya *berbeda*. / Apakah petunjuk ini mengubah peluangnya?

## SOAL

**2. `question`** · 0:09.3 – 0:21.8

- **Animasi:** The original question card slides in; 'kedua mata dadu berbeda' and 'bilangan prima' get yellow highlighter marks as they are read.
- **Narasi:** Soalnya begini. Dua dadu fair dilempar bersamaan. Diketahui kedua mata dadu berbeda. Berapa peluang jumlah mata dadunya merupakan bilangan prima?
- **Teks layar:** Soalnya begini. Dua dadu fair dilempar bersamaan. / Diketahui kedua mata dadu *berbeda*. / Berapa peluang jumlahnya merupakan bilangan *prima*?

**3. `options`** · 0:21.8 – 0:29.9

- **Animasi:** Options A–D appear as cards and pulse as each value is read.
- **Narasi:** Pilihannya: sepertiga, tujuh per lima belas, delapan per lima belas, atau tujuh belas per tiga puluh.
- **Teks layar:** Pilihannya: 1/3, 7/15, 8/15, atau 17/30.

## PAHAMI

**4. `keyword`** · 0:29.9 – 0:36.8

- **Animasi:** The question card shrinks to the top; the highlighted condition flies out into a red SYARAT tag.
- **Narasi:** Kata kuncinya adalah diketahui. Informasi itu mempersempit kemungkinan yang tersisa.
- **Teks layar:** Kata kuncinya: *diketahui*. Informasi itu mempersempit kemungkinan yang tersisa.

**5. `idea`** · 0:36.8 – 0:43.7

- **Animasi:** A word fraction: Peluang = hasil yang cocok (green) / hasil yang masih mungkin (red).
- **Narasi:** Jadi peluangnya adalah banyak hasil yang cocok, dibagi banyak hasil yang masih mungkin setelah syarat dipakai.
- **Teks layar:** Peluang = hasil yang *cocok* dibagi hasil yang *masih mungkin* setelah syarat dipakai.

## RUANG SAMPEL

**6. `axes`** · 0:43.7 – 0:52.3

- **Animasi:** Die faces 1–6 form the column header (Dadu 1, blue) and the row header (Dadu 2, orange).
- **Narasi:** Mari susun semua kemungkinan. Dadu pertama bisa muncul satu sampai enam. Dadu kedua juga.
- **Teks layar:** Mari susun semua kemungkinan. Dadu pertama: 1 sampai 6. / Dadu kedua juga.

**7. `cells`** · 0:52.3 – 1:01.1

- **Animasi:** Pair (2,5) is located from its two headers, then all 36 cells fill with pairs 'i,j'; 6×6 = 36 is written; all cells shimmer (equally likely).
- **Narasi:** Setiap pasangan menempati satu kotak. Enam kali enam, ada tiga puluh enam hasil, dan semuanya sama mungkin.
- **Teks layar:** Setiap pasangan menempati satu kotak. / 6 × 6 = 36 hasil, semuanya *sama mungkin*.

## SYARAT

**8. `doubles`** · 1:01.1 – 1:12.3

- **Animasi:** Condition tag appears; the six diagonal cells turn pink, then are struck through.
- **Narasi:** Sekarang pakai petunjuknya: mata dadu berbeda. Pasangan kembar, satu satu, dua dua, sampai enam enam, tidak mungkin terjadi.
- **Teks layar:** Sekarang pakai petunjuknya: mata dadu *berbeda*. / Pasangan kembar (1,1), (2,2), ..., (6,6) *tidak mungkin*.

**9. `shrink`** · 1:12.3 – 1:20.2

- **Animasi:** Counter morphs 6×6=36 → 36−6=30 → boxed n(S) = 30.
- **Narasi:** Enam kotak di diagonal dicoret. Ruang sampel kita menyusut, dari tiga puluh enam menjadi tiga puluh.
- **Teks layar:** Enam kotak diagonal dicoret. / Ruang sampel menyusut: 36 − 6 = *30*.

## JUMLAH

**10. `sums`** · 1:20.2 – 1:25.2

- **Animasi:** Each pair label morphs into its sum, sweeping along anti-diagonals.
- **Narasi:** Sekarang, ganti setiap pasangan dengan jumlah kedua matanya.
- **Teks layar:** Sekarang ganti setiap pasangan dengan *jumlah* kedua matanya.

**11. `pattern`** · 1:25.2 – 1:35.1

- **Animasi:** An orange band outlines the anti-diagonal of 7s; the six 7s pulse.
- **Narasi:** Lihat polanya. Jumlah yang sama selalu berjajar miring. Misalnya, semua jumlah tujuh ada di satu garis.
- **Teks layar:** Lihat polanya: jumlah yang sama berjajar *miring*. / Semua jumlah 7 ada di satu garis.

## PRIMA

**12. `primes`** · 1:35.1 – 1:45.2

- **Animasi:** A 2…12 number strip appears; 2, 3, 5, 7, 11 turn green as they are named.
- **Narasi:** Jumlahnya berkisar dari dua sampai dua belas. Yang prima adalah dua, tiga, lima, tujuh, dan sebelas.
- **Teks layar:** Jumlahnya dari 2 sampai 12. / Yang prima: 2, 3, 5, 7, dan 11.

**13. `two`** · 1:45.2 – 1:53.7

- **Animasi:** Cell (1,1) pulses red; '2' on the strip turns red and is struck out.
- **Narasi:** Tapi jumlah dua hanya bisa dari satu dan satu. Itu pasangan kembar yang sudah dicoret, jadi tidak ikut dihitung.
- **Teks layar:** Tapi jumlah 2 hanya dari (1,1): pasangan kembar yang sudah *dicoret*.

## HITUNG

**14. `light`** · 1:53.7 – 2:00.1

- **Animasi:** Anti-diagonals for sums 3, 5, 7, 11 light up green (only non-diagonal cells).
- **Narasi:** Sekarang nyalakan jajaran jumlah tiga, lima, tujuh, dan sebelas.
- **Teks layar:** Nyalakan jajaran jumlah 3, 5, 7, dan 11.

**15. `count`** · 2:00.1 – 2:08.5

- **Animasi:** Strip is replaced by 2 + 4 + 6 + 2 = 14; each term appears while its line pulses; 14 is circled.
- **Narasi:** Dua, ditambah empat, ditambah enam, ditambah dua. Ada empat belas kotak yang cocok.
- **Teks layar:** 2 + 4 + 6 + 2 = *14* kotak yang cocok.

**16. `fraction`** · 2:08.5 – 2:17.1

- **Animasi:** Table shrinks to the top; P(prima | berbeda) = 14/30 is assembled from the tally (14) and n(S) (30); ÷2 on both parts gives 7/15, circled.
- **Narasi:** Jadi peluangnya empat belas per tiga puluh. Bagi pembilang dan penyebut dengan dua, hasilnya tujuh per lima belas.
- **Teks layar:** Peluangnya 14/30. / Bagi pembilang dan penyebut dengan 2: *7/15*.

## JAWABAN

**17. `answer`** · 2:17.1 – 2:22.2

- **Animasi:** Options return; B scales up, turns green and gets a check badge; others fade.
- **Narasi:** Jadi jawabannya adalah B, tujuh per lima belas.
- **Teks layar:** Jawabannya *B*, yaitu 7/15.

## CEK

**18. `symmetry`** · 2:22.2 – 2:32.8

- **Animasi:** Full table returns; a dashed purple mirror line is drawn on the diagonal; the lower half fades; tag '15 pasangan'.
- **Narasi:** Mari kita cek dengan cara lain. Tabelnya simetris, jadi cukup lihat setengahnya: lima belas pasangan berbeda, tanpa memperhatikan urutan.
- **Teks layar:** Cek dengan cara lain. Tabelnya *simetris*. / Cukup lihat setengahnya: 15 pasangan tanpa urutan.

**19. `half`** · 2:32.8 – 2:41.6

- **Animasi:** The 7 green cells in the upper half pulse; 7/15 with a check badge appears.
- **Narasi:** Di setengah ini, yang jumlahnya prima ada tujuh. Tujuh dari lima belas. Hasilnya sama!
- **Teks layar:** Yang jumlahnya prima ada 7. / 7 dari 15, hasilnya *sama*!

**20. `trap`** · 2:41.6 – 2:52.9

- **Animasi:** Card: 'Tanpa memakai syarat': 15/36 = 5/12 with a red cross, 'tidak ada di pilihan'.
- **Narasi:** Hati-hati. Kalau syaratnya diabaikan, kamu akan membagi dengan tiga puluh enam, dan mendapat lima per dua belas. Itu tidak ada di pilihan.
- **Teks layar:** Hati-hati: tanpa syarat, peluangnya 15/36 = 5/12. / Tidak ada di pilihan.

## INTINYA

**21. `takeaway`** · 2:52.9 – 3:02.6

- **Animasi:** Summary card: 1. Coret yang tidak mungkin (36→30), 2. Hitung yang cocok (14), P = 14/30 = 7/15 circled.
- **Narasi:** Intinya, kata diketahui berarti ruang sampel menyusut. Coret dulu yang tidak mungkin, baru hitung yang cocok.
- **Teks layar:** Intinya: *diketahui* berarti ruang sampel *menyusut*. / Coret dulu yang tidak mungkin, baru hitung yang cocok.

---

## Naskah narasi lengkap


**[TANTANGAN]**

Dua dadu dilempar, dan kita diberi satu petunjuk: kedua mata dadunya berbeda. Apakah petunjuk ini mengubah peluangnya?


**[SOAL]**

Soalnya begini. Dua dadu fair dilempar bersamaan. Diketahui kedua mata dadu berbeda. Berapa peluang jumlah mata dadunya merupakan bilangan prima?

Pilihannya: sepertiga, tujuh per lima belas, delapan per lima belas, atau tujuh belas per tiga puluh.


**[PAHAMI]**

Kata kuncinya adalah diketahui. Informasi itu mempersempit kemungkinan yang tersisa.

Jadi peluangnya adalah banyak hasil yang cocok, dibagi banyak hasil yang masih mungkin setelah syarat dipakai.


**[RUANG SAMPEL]**

Mari susun semua kemungkinan. Dadu pertama bisa muncul satu sampai enam. Dadu kedua juga.

Setiap pasangan menempati satu kotak. Enam kali enam, ada tiga puluh enam hasil, dan semuanya sama mungkin.


**[SYARAT]**

Sekarang pakai petunjuknya: mata dadu berbeda. Pasangan kembar, satu satu, dua dua, sampai enam enam, tidak mungkin terjadi.

Enam kotak di diagonal dicoret. Ruang sampel kita menyusut, dari tiga puluh enam menjadi tiga puluh.


**[JUMLAH]**

Sekarang, ganti setiap pasangan dengan jumlah kedua matanya.

Lihat polanya. Jumlah yang sama selalu berjajar miring. Misalnya, semua jumlah tujuh ada di satu garis.


**[PRIMA]**

Jumlahnya berkisar dari dua sampai dua belas. Yang prima adalah dua, tiga, lima, tujuh, dan sebelas.

Tapi jumlah dua hanya bisa dari satu dan satu. Itu pasangan kembar yang sudah dicoret, jadi tidak ikut dihitung.


**[HITUNG]**

Sekarang nyalakan jajaran jumlah tiga, lima, tujuh, dan sebelas.

Dua, ditambah empat, ditambah enam, ditambah dua. Ada empat belas kotak yang cocok.

Jadi peluangnya empat belas per tiga puluh. Bagi pembilang dan penyebut dengan dua, hasilnya tujuh per lima belas.


**[JAWABAN]**

Jadi jawabannya adalah B, tujuh per lima belas.


**[CEK]**

Mari kita cek dengan cara lain. Tabelnya simetris, jadi cukup lihat setengahnya: lima belas pasangan berbeda, tanpa memperhatikan urutan.

Di setengah ini, yang jumlahnya prima ada tujuh. Tujuh dari lima belas. Hasilnya sama!

Hati-hati. Kalau syaratnya diabaikan, kamu akan membagi dengan tiga puluh enam, dan mendapat lima per dua belas. Itu tidak ada di pilihan.


**[INTINYA]**

Intinya, kata diketahui berarti ruang sampel menyusut. Coret dulu yang tidak mungkin, baru hitung yang cocok.
