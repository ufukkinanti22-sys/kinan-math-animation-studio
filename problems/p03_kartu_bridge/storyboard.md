# Storyboard — Dua kartu bridge: tepat satu bergambar, warna berbeda

Durasi video final: **3:09.3** · 1080×1920 · 30 fps · suara: `id-ID-ArdiNeural` (rate -4%)

Waktu diambil dari render terakhir (`output/qc/<id>/beats.json`). Setiap baris adalah satu *beat*: narasi, teks layar, dan animasinya berjalan bersamaan.

## TANTANGAN

**1. `hook`** · 0:00.0 – 0:09.9

- **Animasi:** Five cards fan in; K♥ and 7♣ lift out with tags 'bergambar', 'merah', 'hitam'; question mark.
- **Narasi:** Dua kartu diambil dari satu set kartu bridge. Hanya satu yang bergambar, dan warnanya berbeda. Berapa peluangnya?
- **Teks layar:** Dua kartu diambil dari satu set kartu bridge. / Hanya *satu* yang bergambar, dan warnanya *berbeda*. / Berapa peluangnya?

## SOAL

**2. `question`** · 0:09.9 – 0:26.9

- **Animasi:** Original question card; 'sekaligus', 'tepat satu kartu bergambar', 'berlainan warna' highlighted as read.
- **Narasi:** Soalnya begini. Dua kartu diambil sekaligus dari satu set kartu bridge standar, lima puluh dua kartu, tanpa joker. Berapa peluang tepat satu kartu bergambar, yaitu J, Q, atau K, dan kedua kartu berlainan warna?
- **Teks layar:** Dua kartu diambil *sekaligus* dari 52 kartu bridge, tanpa joker. / Berapa peluang *tepat satu* kartu bergambar (J, Q, atau K) / dan kedua kartu *berlainan warna*?

**3. `options`** · 0:26.9 – 0:35.7

- **Animasi:** Options 20/221 … 80/221 appear and pulse as read.
- **Narasi:** Pilihannya: dua puluh, empat puluh, enam puluh, atau delapan puluh, semuanya per dua ratus dua puluh satu.
- **Teks layar:** Pilihannya: 20, 40, 60, atau 80, semuanya per 221.

## PAHAMI

**4. `conditions`** · 0:35.7 – 0:48.1

- **Animasi:** Two condition tags; examples: K♥+7♣ ✓ (cocok), K♥+Q♠ ✗ (2 bergambar), K♥+7♦ ✗ (warna sama).
- **Narasi:** Ada dua syarat yang harus terpenuhi bersamaan. Pertama, tepat satu kartu bergambar. Kedua, warnanya berbeda: satu merah, satu hitam.
- **Teks layar:** Ada *dua* syarat sekaligus. / Pertama: tepat satu kartu bergambar. / Kedua: warnanya berbeda, satu merah, satu hitam.

**5. `together`** · 0:48.1 – 0:55.2

- **Animasi:** K♥ 7♣ = 7♣ K♥ (cards swap along arcs); the set {K♥, 7♣} = 1 pasangan.
- **Narasi:** Diambil sekaligus berarti urutan tidak penting. Yang kita hitung adalah pasangan kartu.
- **Teks layar:** *Sekaligus* berarti urutan tidak penting. / Kita menghitung *pasangan* kartu.

## KELOMPOK

**6. `deck`** · 0:55.2 – 1:07.0

- **Animasi:** All 52 cards deal into a 4×13 grid (♥ ♦ ♠ ♣ × A…K); red rows get a pink band, black rows a grey band.
- **Narasi:** Susun kelima puluh dua kartu. Ada empat jenis, masing-masing tiga belas kartu. Hati dan wajik berwarna merah, sekop dan keriting berwarna hitam.
- **Teks layar:** Susun ke-52 kartu: 4 jenis, masing-masing 13 kartu. / Hati dan wajik *merah*, sekop dan keriting *hitam*.

**7. `faces`** · 1:07.0 – 1:17.2

- **Animasi:** An orange frame surrounds the J, Q, K columns; 12 = 6 merah + 6 hitam.
- **Narasi:** Kartu bergambar adalah J, Q, dan K, tiga di setiap jenis. Totalnya dua belas: enam merah dan enam hitam.
- **Teks layar:** Kartu bergambar: J, Q, dan K, tiga per jenis. / Totalnya 12: *6 merah* dan *6 hitam*.

**8. `plain`** · 1:17.2 – 1:23.0

- **Animasi:** The other 40 cards pulse; 40 = 20 merah + 20 hitam.
- **Narasi:** Sisanya empat puluh kartu tidak bergambar: dua puluh merah dan dua puluh hitam.
- **Teks layar:** Sisanya 40 kartu tidak bergambar: *20 merah* dan *20 hitam*.

**9. `blocks`** · 1:23.0 – 1:27.2

- **Animasi:** Cards fly into a 2×2 table of groups (Merah/Hitam × bergambar/tidak) with count badges 6, 6, 20, 20.
- **Narasi:** Jadi dek terbagi menjadi empat kelompok yang jelas.
- **Teks layar:** Jadi dek terbagi menjadi *empat* kelompok.

## PASANGAN

**10. `link`** · 1:27.2 – 1:37.2

- **Animasi:** Table shrinks; top row then bottom row outlined; two green diagonal links connect the valid group pairs.
- **Narasi:** Tepat satu bergambar berarti satu kartu dari baris atas, dan satu dari baris bawah. Warna berbeda berarti kolomnya juga harus beda.
- **Teks layar:** Tepat satu bergambar: satu dari baris *atas*, satu dari baris *bawah*. / Warna berbeda: kolomnya juga harus *beda*.

**11. `rect1`** · 1:37.2 – 1:44.2

- **Animasi:** 6 × 20 dot rectangle (red-face × black-plain pairs) grows dot by dot; 6 × 20 = 120.
- **Narasi:** Merah bergambar dengan hitam tidak bergambar: enam kali dua puluh, ada seratus dua puluh pasangan.
- **Teks layar:** Merah bergambar dengan hitam tidak bergambar: / 6 × 20 = *120* pasangan.

**12. `rect2`** · 1:44.2 – 1:53.0

- **Animasi:** Second 6 × 20 dot rectangle (black-face × red-plain); 120 + 120 = 240 circled.
- **Narasi:** Hitam bergambar dengan merah tidak bergambar: juga seratus dua puluh. Totalnya dua ratus empat puluh pasangan yang cocok.
- **Teks layar:** Hitam bergambar dengan merah tidak bergambar: juga 120. / Totalnya *240* pasangan yang cocok.

## SEMUA PASANGAN

**13. `total`** · 1:53.0 – 2:01.6

- **Animasi:** Tag 'cocok: 240'; slots Kartu ke-1: 52, Kartu ke-2: 51; 52 × 51 = 2652.
- **Narasi:** Sekarang hitung semua pasangan yang mungkin. Kartu pertama punya lima puluh dua pilihan, kartu kedua lima puluh satu.
- **Teks layar:** Sekarang hitung *semua* pasangan. / Kartu pertama: 52 pilihan, kartu kedua: 51.

**14. `double`** · 2:01.6 – 2:04.9

- **Animasi:** K♥7♣ = 7♣K♥ shown; formula becomes C(52,2) = 52×51/2 = 1326; tag 'semua: 1326'.
- **Narasi:** Tapi setiap pasangan terhitung dua kali. K hati lalu tujuh keriting, sama saja dengan tujuh keriting lalu K hati. Jadi kita bagi dua, hasilnya seribu tiga ratus dua puluh enam pasangan.
- **Teks layar:** Tapi setiap pasangan terhitung *dua kali*: / K♥ lalu 7♣ sama dengan 7♣ lalu K♥. / Bagi dua: *1326* pasangan.

## HITUNG

**15. `prob`** · 2:04.9 – 2:10.2

- **Animasi:** P = 240/1326 assembled from the two tags.
- **Narasi:** Peluangnya, dua ratus empat puluh per seribu tiga ratus dua puluh enam.
- **Teks layar:** Peluangnya 240 per 1326.

**16. `simplify`** · 2:10.2 – 2:17.5

- **Animasi:** ÷6 on numerator and denominator → 40/221; 240 = 6·40, 1326 = 6·221; circled.
- **Narasi:** Bagi pembilang dan penyebut dengan enam. Hasilnya empat puluh per dua ratus dua puluh satu.
- **Teks layar:** Bagi pembilang dan penyebut dengan 6: *40/221*.

## JAWABAN

**17. `answer`** · 2:17.5 – 2:23.3

- **Animasi:** Option B confirmed with check badge; others fade.
- **Narasi:** Jadi jawabannya adalah B, empat puluh per dua ratus dua puluh satu.
- **Teks layar:** Jawabannya *B*, yaitu 40/221.

## CEK

**18. `seq`** · 2:23.3 – 2:35.8

- **Animasi:** K♥ → 7♣ drawn one at a time; 6/52 × 20/51.
- **Narasi:** Mari kita cek dengan mengambil kartu satu per satu. Misalnya, merah bergambar dulu, lalu hitam tidak bergambar: enam per lima puluh dua, dikali dua puluh per lima puluh satu.
- **Teks layar:** Cek dengan mengambil satu per satu. / Merah bergambar dulu, lalu hitam tidak bergambar: / 6/52 × 20/51.

**19. `seq2`** · 2:35.8 – 2:47.7

- **Animasi:** 4 × (6/52 × 20/51) = 480/2652 = 40/221 ✓, with 4 = 2 colour pairings × 2 orders.
- **Narasi:** Ada empat susunan seperti itu: dua pasangan warna, masing-masing dengan dua urutan. Empat kali hasil tadi, juga sama dengan empat puluh per dua ratus dua puluh satu.
- **Teks layar:** Ada *4* susunan: 2 pasangan warna × 2 urutan. / Hasilnya juga *40/221*.

**20. `trap`** · 2:47.7 – 2:58.3

- **Animasi:** Card: only one colour pairing gives 120/1326 = 20/221 ✗ — 'jebakan pilihan A'.
- **Narasi:** Hati-hati. Kalau hanya menghitung satu pasangan warna, kamu mendapat dua puluh per dua ratus dua puluh satu. Itu jebakan di pilihan A.
- **Teks layar:** Hati-hati: hanya satu pasangan warna memberi 20/221. / Itu *jebakan* di pilihan A.

## INTINYA

**21. `takeaway`** · 2:58.3 – 3:09.3

- **Animasi:** Card: 1. kelompok 6, 6, 20, 20; 2. pasangkan: 6×20 + 6×20 = 240; 3. bagi: 240/1326 = 40/221.
- **Narasi:** Intinya, pecah kartu menjadi kelompok yang jelas. Pasangkan kelompok yang memenuhi semua syarat, lalu kalikan untuk menghitung pasangannya.
- **Teks layar:** Intinya: pecah menjadi *kelompok* yang jelas. / Pasangkan kelompok yang memenuhi *semua* syarat, lalu *kalikan*.

---

## Naskah narasi lengkap


**[TANTANGAN]**

Dua kartu diambil dari satu set kartu bridge. Hanya satu yang bergambar, dan warnanya berbeda. Berapa peluangnya?


**[SOAL]**

Soalnya begini. Dua kartu diambil sekaligus dari satu set kartu bridge standar, lima puluh dua kartu, tanpa joker. Berapa peluang tepat satu kartu bergambar, yaitu J, Q, atau K, dan kedua kartu berlainan warna?

Pilihannya: dua puluh, empat puluh, enam puluh, atau delapan puluh, semuanya per dua ratus dua puluh satu.


**[PAHAMI]**

Ada dua syarat yang harus terpenuhi bersamaan. Pertama, tepat satu kartu bergambar. Kedua, warnanya berbeda: satu merah, satu hitam.

Diambil sekaligus berarti urutan tidak penting. Yang kita hitung adalah pasangan kartu.


**[KELOMPOK]**

Susun kelima puluh dua kartu. Ada empat jenis, masing-masing tiga belas kartu. Hati dan wajik berwarna merah, sekop dan keriting berwarna hitam.

Kartu bergambar adalah J, Q, dan K, tiga di setiap jenis. Totalnya dua belas: enam merah dan enam hitam.

Sisanya empat puluh kartu tidak bergambar: dua puluh merah dan dua puluh hitam.

Jadi dek terbagi menjadi empat kelompok yang jelas.


**[PASANGAN]**

Tepat satu bergambar berarti satu kartu dari baris atas, dan satu dari baris bawah. Warna berbeda berarti kolomnya juga harus beda.

Merah bergambar dengan hitam tidak bergambar: enam kali dua puluh, ada seratus dua puluh pasangan.

Hitam bergambar dengan merah tidak bergambar: juga seratus dua puluh. Totalnya dua ratus empat puluh pasangan yang cocok.


**[SEMUA PASANGAN]**

Sekarang hitung semua pasangan yang mungkin. Kartu pertama punya lima puluh dua pilihan, kartu kedua lima puluh satu.

Tapi setiap pasangan terhitung dua kali. K hati lalu tujuh keriting, sama saja dengan tujuh keriting lalu K hati. Jadi kita bagi dua, hasilnya seribu tiga ratus dua puluh enam pasangan.


**[HITUNG]**

Peluangnya, dua ratus empat puluh per seribu tiga ratus dua puluh enam.

Bagi pembilang dan penyebut dengan enam. Hasilnya empat puluh per dua ratus dua puluh satu.


**[JAWABAN]**

Jadi jawabannya adalah B, empat puluh per dua ratus dua puluh satu.


**[CEK]**

Mari kita cek dengan mengambil kartu satu per satu. Misalnya, merah bergambar dulu, lalu hitam tidak bergambar: enam per lima puluh dua, dikali dua puluh per lima puluh satu.

Ada empat susunan seperti itu: dua pasangan warna, masing-masing dengan dua urutan. Empat kali hasil tadi, juga sama dengan empat puluh per dua ratus dua puluh satu.

Hati-hati. Kalau hanya menghitung satu pasangan warna, kamu mendapat dua puluh per dua ratus dua puluh satu. Itu jebakan di pilihan A.


**[INTINYA]**

Intinya, pecah kartu menjadi kelompok yang jelas. Pasangkan kelompok yang memenuhi semua syarat, lalu kalikan untuk menghitung pasangannya.
