# Storyboard — Tiga koin, sedikitnya satu gambar

Durasi video final: **3:01.2** · 1080×1920 · 30 fps · suara: `id-ID-ArdiNeural` (rate -4%)

Waktu diambil dari render terakhir (`output/qc/<id>/beats.json`). Setiap baris adalah satu *beat*: narasi, teks layar, dan animasinya berjalan bersamaan.

## TANTANGAN

**1. `hook`** · 0:00.0 – 0:10.2

- **Animasi:** Three big coins drop and flip several times, landing G A G; tag 'bocoran: sedikitnya 1 gambar'; question mark.
- **Narasi:** Tiga koin dilempar. Lalu ada bocoran: sedikitnya satu sisi gambar muncul. Apakah bocoran ini mengubah peluangnya?
- **Teks layar:** Tiga koin dilempar. Lalu ada *bocoran*: sedikitnya satu sisi gambar muncul. / Apakah bocoran ini mengubah peluangnya?

## SOAL

**2. `question`** · 0:10.2 – 0:21.8

- **Animasi:** Original question card; 'sedikitnya satu sisi gambar muncul' and 'tepat dua sisi gambar' highlighted as read.
- **Narasi:** Soalnya begini. Tiga koin fair dilempar bersamaan. Jika diketahui sedikitnya satu sisi gambar muncul, berapa peluang muncul tepat dua sisi gambar?
- **Teks layar:** Soalnya begini. Tiga koin fair dilempar bersamaan. / Jika diketahui *sedikitnya* satu sisi gambar muncul, / berapa peluang *tepat* dua sisi gambar?

**3. `options`** · 0:21.8 – 0:28.9

- **Animasi:** Options A–D appear and pulse as read.
- **Narasi:** Pilihannya: dua per tujuh, tiga per tujuh, empat per tujuh, atau setengah.
- **Teks layar:** Pilihannya: 2/7, 3/7, 4/7, atau 1/2.

## PAHAMI

**4. `faces`** · 0:28.9 – 0:38.2

- **Animasi:** Coin G (gambar, gold) and coin A (angka, blue) appear, each with probability ½.
- **Narasi:** Setiap koin punya dua sisi: G untuk gambar, dan A untuk angka. Karena koinnya fair, keduanya sama mungkin.
- **Teks layar:** Setiap koin punya dua sisi: *G* untuk gambar, *A* untuk angka. / Koinnya fair, jadi keduanya *sama mungkin*.

**5. `words`** · 0:38.2 – 0:51.0

- **Animasi:** Chips 0G 1G 2G 3G; a blue brace 'sedikitnya satu' covers 1–3; a green brace 'tepat dua' marks 2 only.
- **Narasi:** Perhatikan dua frasa penting. Sedikitnya satu, artinya satu, dua, atau tiga gambar. Tepat dua, artinya dua saja, tidak lebih.
- **Teks layar:** Perhatikan dua frasa penting. / *Sedikitnya satu* = 1, 2, atau 3 gambar. / *Tepat dua* = 2 saja, tidak lebih.

## RUANG SAMPEL

**6. `tree1`** · 0:51.0 – 0:58.2

- **Animasi:** Tree diagram starts: root dot branches to G and A (Koin 1).
- **Narasi:** Kita gambar diagram pohon. Koin pertama bercabang dua: G atau A.
- **Teks layar:** Kita gambar *diagram pohon*. Koin pertama bercabang dua: G atau A.

**7. `tree2`** · 0:58.2 – 1:04.3

- **Animasi:** Each branch splits again for Koin 2, then Koin 3 (lagged).
- **Narasi:** Setiap cabang bercabang dua lagi untuk koin kedua, lalu dua lagi untuk koin ketiga.
- **Teks layar:** Setiap cabang bercabang dua lagi untuk koin *kedua*, / lalu dua lagi untuk koin *ketiga*.

**8. `tree3`** · 1:04.3 – 1:13.3

- **Animasi:** Path G→A→G highlights and its coins fly into the outcome column 'GAG'; all 8 outcomes follow; 2×2×2 = 8.
- **Narasi:** Ikuti setiap jalur dari kiri ke kanan. Dua kali dua kali dua, ada delapan hasil, dan semuanya sama mungkin.
- **Teks layar:** Ikuti setiap jalur dari kiri ke kanan. / 2 × 2 × 2 = *8* hasil, semuanya sama mungkin.

## SYARAT

**9. `condition`** · 1:13.3 – 1:23.0

- **Animasi:** Tag 'sedikitnya 1 G'; the AAA path turns red and its row gets a red background.
- **Narasi:** Sekarang pakai bocorannya: sedikitnya satu gambar. Hanya ada satu hasil yang sama sekali tidak punya gambar, yaitu A A A.
- **Teks layar:** Sekarang pakai bocorannya: sedikitnya satu gambar. / Hanya satu hasil tanpa gambar sama sekali: *AAA*.

**10. `shrink`** · 1:23.0 – 1:28.6

- **Animasi:** AAA is struck and faded; counter 8−1=7 → boxed n(S) = 7.
- **Narasi:** Hasil itu kita coret. Ruang sampel baru tinggal tujuh.
- **Teks layar:** Hasil itu dicoret. Ruang sampel baru: 8 − 1 = *7*.

## HITUNG

**11. `badges`** · 1:28.6 – 1:33.2

- **Animasi:** G coins in each remaining outcome pulse while a count badge (3,2,2,1,2,1,1) appears.
- **Narasi:** Sekarang hitung banyaknya gambar di setiap hasil yang tersisa.
- **Teks layar:** Sekarang hitung banyaknya *gambar* di setiap hasil yang tersisa.

**12. `exactly`** · 1:33.2 – 1:41.4

- **Animasi:** GGA, GAG, AGG rows turn green with their tree paths; tag 'tepat 2 G: 3'.
- **Narasi:** Yang tepat dua gambar adalah G G A, G A G, dan A G G. Ada tiga.
- **Teks layar:** Tepat dua gambar: GGA, GAG, dan AGG. Ada *3*.

**13. `fraction`** · 1:41.4 – 1:47.2

- **Animasi:** P = 3/7 assembled from the tag (3) and n(S) (7); circled.
- **Narasi:** Jadi peluangnya tiga dari tujuh hasil yang masih mungkin, yaitu tiga per tujuh.
- **Teks layar:** Peluangnya 3 dari 7 hasil yang masih mungkin: *3/7*.

## JAWABAN

**14. `answer`** · 1:47.2 – 1:52.1

- **Animasi:** Tree clears; P = 3/7 at the top; option B confirmed with a check badge.
- **Narasi:** Jadi jawabannya adalah B, tiga per tujuh.
- **Teks layar:** Jawabannya *B*, yaitu 3/7.

## CEK

**15. `groups`** · 1:52.1 – 2:02.8

- **Animasi:** The 8 outcomes reappear and slide into four bins 0G, 1G, 2G, 3G.
- **Narasi:** Mari kita cek dari strukturnya. Kelompokkan kedelapan hasil menurut banyak gambarnya: nol, satu, dua, atau tiga gambar.
- **Teks layar:** Cek dari strukturnya. / Kelompokkan hasil menurut banyak gambar: 0, 1, 2, atau 3.

**16. `pascal`** · 2:02.8 – 2:18.8

- **Animasi:** Counts 1, 3, 3, 1 written; bin 0 turns red and is struck; brace 3+3+1 = 7; bin 2 turns green.
- **Narasi:** Isinya satu, tiga, tiga, satu. Syarat sedikitnya satu gambar membuang kelompok nol. Tersisa tiga ditambah tiga ditambah satu, yaitu tujuh. Yang tepat dua: tiga.
- **Teks layar:** Isinya 1, 3, 3, 1. / Syaratnya membuang kelompok 0: tersisa 3 + 3 + 1 = 7. / Yang tepat dua: *3*.

**17. `subset`** · 2:18.8 – 2:29.5

- **Animasi:** Venn diagram inside S (8): B = sedikitnya 1 G (7 outcomes) contains A = tepat 2 G (3 outcomes); AAA outside. P(A|B) = P(A∩B)/P(B) = P(A)/P(B) with A∩B = A.
- **Narasi:** Dengan rumus peluang bersyarat. Karena tepat dua gambar pasti termasuk sedikitnya satu gambar, irisan kedua kejadian adalah kejadian tepat dua itu sendiri.
- **Teks layar:** Dengan rumus peluang bersyarat. / Tepat dua gambar pasti termasuk sedikitnya satu, / jadi *irisannya* adalah kejadian tepat dua itu sendiri.

**18. `formula`** · 2:29.5 – 2:38.5

- **Animasi:** = (3/8)/(7/8); the 8s are cancelled; = 3/7 circled.
- **Narasi:** Jadi tiga per delapan, dibagi tujuh per delapan. Penyebut delapan saling menghilangkan, tersisa tiga per tujuh.
- **Teks layar:** Jadi 3/8 dibagi 7/8. / Penyebut 8 saling *menghilangkan*: tersisa 3/7.

**19. `trap`** · 2:38.5 – 2:46.9

- **Animasi:** Card: without the condition P = 3/8, red cross, 'tidak ada di pilihan'.
- **Narasi:** Hati-hati. Kalau bocorannya diabaikan, peluangnya tiga per delapan, dan itu tidak ada di pilihan.
- **Teks layar:** Hati-hati: tanpa syarat, peluangnya 3/8. / Tidak ada di pilihan.

## INTINYA

**20. `takeaway`** · 2:46.9 – 3:01.2

- **Animasi:** Card: 'Syarat mengubah ruang sampel': coins unchanged; n(S): 8 → 7; P: 3/8 → 3/7.
- **Narasi:** Intinya, syarat tidak mengubah koinnya. Syarat mengubah ruang sampelnya, dari delapan menjadi tujuh. Karena itu peluangnya naik, dari tiga per delapan menjadi tiga per tujuh.
- **Teks layar:** Intinya: syarat tidak mengubah koinnya, tapi mengubah *ruang sampel*: 8 → 7. / Peluangnya naik dari 3/8 menjadi *3/7*.

---

## Naskah narasi lengkap


**[TANTANGAN]**

Tiga koin dilempar. Lalu ada bocoran: sedikitnya satu sisi gambar muncul. Apakah bocoran ini mengubah peluangnya?


**[SOAL]**

Soalnya begini. Tiga koin fair dilempar bersamaan. Jika diketahui sedikitnya satu sisi gambar muncul, berapa peluang muncul tepat dua sisi gambar?

Pilihannya: dua per tujuh, tiga per tujuh, empat per tujuh, atau setengah.


**[PAHAMI]**

Setiap koin punya dua sisi: G untuk gambar, dan A untuk angka. Karena koinnya fair, keduanya sama mungkin.

Perhatikan dua frasa penting. Sedikitnya satu, artinya satu, dua, atau tiga gambar. Tepat dua, artinya dua saja, tidak lebih.


**[RUANG SAMPEL]**

Kita gambar diagram pohon. Koin pertama bercabang dua: G atau A.

Setiap cabang bercabang dua lagi untuk koin kedua, lalu dua lagi untuk koin ketiga.

Ikuti setiap jalur dari kiri ke kanan. Dua kali dua kali dua, ada delapan hasil, dan semuanya sama mungkin.


**[SYARAT]**

Sekarang pakai bocorannya: sedikitnya satu gambar. Hanya ada satu hasil yang sama sekali tidak punya gambar, yaitu A A A.

Hasil itu kita coret. Ruang sampel baru tinggal tujuh.


**[HITUNG]**

Sekarang hitung banyaknya gambar di setiap hasil yang tersisa.

Yang tepat dua gambar adalah G G A, G A G, dan A G G. Ada tiga.

Jadi peluangnya tiga dari tujuh hasil yang masih mungkin, yaitu tiga per tujuh.


**[JAWABAN]**

Jadi jawabannya adalah B, tiga per tujuh.


**[CEK]**

Mari kita cek dari strukturnya. Kelompokkan kedelapan hasil menurut banyak gambarnya: nol, satu, dua, atau tiga gambar.

Isinya satu, tiga, tiga, satu. Syarat sedikitnya satu gambar membuang kelompok nol. Tersisa tiga ditambah tiga ditambah satu, yaitu tujuh. Yang tepat dua: tiga.

Dengan rumus peluang bersyarat. Karena tepat dua gambar pasti termasuk sedikitnya satu gambar, irisan kedua kejadian adalah kejadian tepat dua itu sendiri.

Jadi tiga per delapan, dibagi tujuh per delapan. Penyebut delapan saling menghilangkan, tersisa tiga per tujuh.

Hati-hati. Kalau bocorannya diabaikan, peluangnya tiga per delapan, dan itu tidak ada di pilihan.


**[INTINYA]**

Intinya, syarat tidak mengubah koinnya. Syarat mengubah ruang sampelnya, dari delapan menjadi tujuh. Karena itu peluangnya naik, dari tiga per delapan menjadi tiga per tujuh.
