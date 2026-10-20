# Storyboard — Spinner dan koin: ganjil dan gambar

Durasi video final: **3:25.2** · 1080×1920 · 30 fps · suara: `id-ID-GadisNeural` (rate -8%)

Waktu diambil dari render terakhir (`output/qc/<id>/beats.json`). Setiap baris adalah satu *beat*: narasi, teks layar, dan animasinya berjalan bersamaan.

## SOAL

**1. `question`** · 0:00.0 – 0:16.9

- **Animasi:** Original question card; 'bilangan ganjil pada spinner' and 'sisi gambar pada koin' highlighted; spinner and coin icons.
- **Narasi:** Yuk, baca soalnya bersama. Sebuah spinner bernomor satu sampai enam dan sebuah koin dilempar bersamaan. Berapa peluang muncul bilangan ganjil pada spinner dan sisi gambar pada koin?
- **Teks layar:** Yuk, baca soalnya bersama. / Sebuah spinner bernomor 1 sampai 6 dan sebuah koin dilempar bersamaan. / Berapa peluang bilangan *ganjil* pada spinner dan sisi *gambar* pada koin?

**2. `options`** · 0:16.9 – 0:25.1

- **Animasi:** Options A-D appear and pulse as read.
- **Narasi:** Pilihannya: seperenam, seperempat, sepertiga, atau setengah.
- **Teks layar:** Pilihannya: 1/6, 1/4, 1/3, atau 1/2.

## MAKSUDNYA

**3. `spinner`** · 0:25.1 – 0:39.2

- **Animasi:** Big spinner; the needle spins and stops on 4.
- **Narasi:** Pertama, kenali spinnernya. Spinner adalah papan bundar yang diputar. Jarumnya akan berhenti di salah satu dari enam bagian.
- **Teks layar:** Pertama, kenali *spinner*-nya. / Papan bundar yang diputar; jarumnya berhenti di salah satu dari *enam* bagian.

**4. `equal`** · 0:39.2 – 0:50.7

- **Animasi:** The six sectors pulse one by one: all the same size.
- **Narasi:** Keenam bagiannya sama besar, seperti pada gambar. Jadi setiap angka punya kesempatan yang sama untuk terpilih.
- **Teks layar:** Keenam bagiannya *sama besar*, seperti pada gambar. / Jadi setiap angka punya kesempatan yang sama.

**5. `odd`** · 0:50.7 – 1:04.3

- **Animasi:** Sectors 1, 3, 5 glow; 2, 4, 6 dim. Tag 'ganjil: 1, 3, 5'.
- **Narasi:** Bilangan ganjil adalah bilangan yang tidak habis dibagi dua. Di spinner ini, bilangan ganjilnya adalah satu, tiga, dan lima.
- **Teks layar:** Bilangan *ganjil* tidak habis dibagi 2. / Di spinner ini: 1, 3, dan 5.

**6. `coin`** · 1:04.3 – 1:13.7

- **Animasi:** Coin shows G and A; G is circled.
- **Narasi:** Koinnya punya dua sisi, gambar dan angka. Yang diminta adalah sisi gambar.
- **Teks layar:** Koin punya dua sisi: gambar (G) dan angka (A). / Yang diminta: sisi *gambar*.

**7. `and`** · 1:13.7 – 1:24.8

- **Animasi:** Two condition tags joined by a big 'DAN'.
- **Narasi:** Kata dan berarti kedua hal itu harus terjadi bersamaan. Spinner harus ganjil, dan koin harus gambar.
- **Teks layar:** Kata *dan* berarti keduanya terjadi *bersamaan*: / spinner ganjil, *dan* koin gambar.

## IDE DASAR

**8. `examples`** · 1:24.8 – 1:42.5

- **Animasi:** Example pairs: (3, G) tick, (3, A) cross, (4, G) cross.
- **Narasi:** Coba kita lihat contohnya. Spinner tiga dan koin gambar: cocok! Spinner tiga dan koin angka: tidak cocok. Spinner empat dan koin gambar: juga tidak cocok.
- **Teks layar:** Contoh: spinner 3 dan gambar: *cocok!* / Spinner 3 dan angka: tidak cocok. / Spinner 4 dan gambar: juga tidak cocok.

## SELESAIKAN

**9. `table`** · 1:42.5 – 1:53.0

- **Animasi:** Table: six columns (spinner 1..6) and two rows (G, A); 12 cells fill in.
- **Narasi:** Sekarang kita susun semua kemungkinan dalam tabel. Ada enam angka spinner, dan dua sisi koin.
- **Teks layar:** Sekarang susun semua kemungkinan dalam *tabel*. / Enam angka spinner, dua sisi koin.

**10. `twelve`** · 1:53.0 – 2:02.5

- **Animasi:** 6 × 2 = 12 written; all cells shimmer.
- **Narasi:** Enam kali dua, jadi ada dua belas pasangan. Semuanya punya kesempatan yang sama.
- **Teks layar:** 6 × 2 = *12* pasangan, semuanya sama mungkin.

**11. `cols`** · 2:02.5 – 2:10.8

- **Animasi:** Columns 1, 3, 5 are shaded blue.
- **Narasi:** Sekarang warnai kolom bilangan ganjil, yaitu satu, tiga, dan lima.
- **Teks layar:** Warnai kolom *ganjil*: 1, 3, dan 5.

**12. `row`** · 2:10.8 – 2:19.4

- **Animasi:** Row G is outlined yellow; the three cells in both turn green.
- **Narasi:** Lalu ambil hanya baris gambar. Kotak yang memenuhi kedua syarat ada tiga.
- **Teks layar:** Lalu ambil hanya baris *gambar*. / Kotak yang memenuhi keduanya: *3*.

**13. `compute`** · 2:19.4 – 2:31.2

- **Animasi:** Peluang = 3/12, ÷3 -> 1/4.
- **Narasi:** Jadi peluangnya tiga per dua belas. Bagi atas dan bawah dengan tiga. Hasilnya satu per empat.
- **Teks layar:** Peluangnya 3/12. / Bagi atas dan bawah dengan 3: *1/4*.

## JAWABAN

**14. `answer`** · 2:31.2 – 2:37.4

- **Animasi:** Options return; B is confirmed.
- **Narasi:** Jadi, jawabannya adalah B, seperempat.
- **Teks layar:** Jawabannya *B*, yaitu 1/4.

**15. `check1`** · 2:37.4 – 2:47.8

- **Animasi:** Area model: a square; the odd half (spinner) is shaded.
- **Narasi:** Ada cara cepat untuk mengeceknya. Peluang spinner ganjil adalah tiga dari enam, yaitu setengah.
- **Teks layar:** Cara cepat untuk mengecek: / peluang spinner ganjil = 3/6 = *1/2*.

**16. `check2`** · 2:47.8 – 2:58.4

- **Animasi:** Half of that half (coin G) is shaded: one quarter of the square; 1/2 × 1/2 = 1/4.
- **Narasi:** Peluang koin gambar juga setengah. Setengah dari setengah adalah seperempat. Hasilnya sama!
- **Teks layar:** Peluang koin gambar juga 1/2. / Setengah dari setengah = *1/4*. Sama!

**17. `check3`** · 2:58.4 – 3:08.4

- **Animasi:** Note: spinner and coin do not affect each other.
- **Narasi:** Kita boleh mengalikan, karena hasil spinner tidak memengaruhi koin, dan hasil koin tidak memengaruhi spinner.
- **Teks layar:** Boleh dikalikan, karena spinner dan koin / *tidak saling memengaruhi*.

## INGAT

**18. `remember`** · 3:08.9 – 3:25.2

- **Animasi:** Summary card: 'dan' = kotak yang memenuhi kedua syarat; jika tidak saling memengaruhi, kalikan.
- **Narasi:** Yang perlu diingat. Untuk kejadian dan, cari kotak yang memenuhi kedua syarat sekaligus. Kalau kedua benda tidak saling memengaruhi, peluangnya boleh dikalikan.
- **Teks layar:** Yang perlu diingat: / kejadian *dan* = kotak yang memenuhi *kedua* syarat. / Tidak saling memengaruhi? Peluangnya boleh *dikalikan*.

---

## Naskah narasi lengkap


**[SOAL]**

Yuk, baca soalnya bersama. Sebuah spinner bernomor satu sampai enam dan sebuah koin dilempar bersamaan. Berapa peluang muncul bilangan ganjil pada spinner dan sisi gambar pada koin?

Pilihannya: seperenam, seperempat, sepertiga, atau setengah.


**[MAKSUDNYA]**

Pertama, kenali spinnernya. Spinner adalah papan bundar yang diputar. Jarumnya akan berhenti di salah satu dari enam bagian.

Keenam bagiannya sama besar, seperti pada gambar. Jadi setiap angka punya kesempatan yang sama untuk terpilih.

Bilangan ganjil adalah bilangan yang tidak habis dibagi dua. Di spinner ini, bilangan ganjilnya adalah satu, tiga, dan lima.

Koinnya punya dua sisi, gambar dan angka. Yang diminta adalah sisi gambar.

Kata dan berarti kedua hal itu harus terjadi bersamaan. Spinner harus ganjil, dan koin harus gambar.


**[IDE DASAR]**

Coba kita lihat contohnya. Spinner tiga dan koin gambar: cocok! Spinner tiga dan koin angka: tidak cocok. Spinner empat dan koin gambar: juga tidak cocok.


**[SELESAIKAN]**

Sekarang kita susun semua kemungkinan dalam tabel. Ada enam angka spinner, dan dua sisi koin.

Enam kali dua, jadi ada dua belas pasangan. Semuanya punya kesempatan yang sama.

Sekarang warnai kolom bilangan ganjil, yaitu satu, tiga, dan lima.

Lalu ambil hanya baris gambar. Kotak yang memenuhi kedua syarat ada tiga.

Jadi peluangnya tiga per dua belas. Bagi atas dan bawah dengan tiga. Hasilnya satu per empat.


**[JAWABAN]**

Jadi, jawabannya adalah B, seperempat.

Ada cara cepat untuk mengeceknya. Peluang spinner ganjil adalah tiga dari enam, yaitu setengah.

Peluang koin gambar juga setengah. Setengah dari setengah adalah seperempat. Hasilnya sama!

Kita boleh mengalikan, karena hasil spinner tidak memengaruhi koin, dan hasil koin tidak memengaruhi spinner.


**[INGAT]**

Yang perlu diingat. Untuk kejadian dan, cari kotak yang memenuhi kedua syarat sekaligus. Kalau kedua benda tidak saling memengaruhi, peluangnya boleh dikalikan.
