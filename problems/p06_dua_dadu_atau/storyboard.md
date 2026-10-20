# Storyboard — Dua dadu: jumlah lebih dari 9 atau kembar

Durasi video final: **3:33.6** · 1080×1920 · 30 fps · suara: `id-ID-GadisNeural` (rate -8%)

Waktu diambil dari render terakhir (`output/qc/<id>/beats.json`). Setiap baris adalah satu *beat*: narasi, teks layar, dan animasinya berjalan bersamaan.

## SOAL

**1. `question`** · 0:00.0 – 0:14.8

- **Animasi:** Original question card; 'lebih dari 9' and 'kedua mata dadu sama' highlighted; two dice.
- **Narasi:** Yuk, baca soalnya bersama. Dua dadu dilempar bersamaan. Berapa peluang jumlah mata dadu lebih dari sembilan, atau kedua mata dadu sama?
- **Teks layar:** Yuk, baca soalnya bersama. / Dua dadu dilempar bersamaan. / Berapa peluang jumlahnya *lebih dari 9*, atau kedua mata dadu *sama*?

**2. `options`** · 0:14.8 – 0:25.2

- **Animasi:** Options A-D appear and pulse as read.
- **Narasi:** Pilihannya: seperempat, lima per delapan belas, tujuh per delapan belas, atau sebelas per delapan belas.
- **Teks layar:** Pilihannya: 1/4, 5/18, 7/18, atau 11/18.

## MAKSUDNYA

**3. `more`** · 0:25.2 – 0:44.3

- **Animasi:** Number line 2..12; 9 is crossed out; 10, 11, 12 glow.
- **Narasi:** Ada dua syarat di sini. Syarat pertama: jumlahnya lebih dari sembilan. Hati-hati, sembilan sendiri tidak termasuk. Jadi jumlahnya sepuluh, sebelas, atau dua belas.
- **Teks layar:** Syarat pertama: jumlah *lebih dari 9*. / Hati-hati, 9 sendiri *tidak* termasuk. / Jadi jumlahnya 10, 11, atau 12.

**4. `same`** · 0:44.3 – 0:58.2

- **Animasi:** Pairs of equal dice: (1,1), (5,5).
- **Narasi:** Syarat kedua: kedua mata dadu sama. Misalnya satu dan satu, atau lima dan lima. Kita sebut ini pasangan kembar.
- **Teks layar:** Syarat kedua: kedua mata dadu *sama*. / Misalnya (1,1) atau (5,5): pasangan *kembar*.

**5. `or`** · 0:58.2 – 1:11.1

- **Animasi:** Two overlapping circles: 'jumlah > 9' and 'kembar'; the whole union glows.
- **Narasi:** Lalu kata atau. Artinya, cukup salah satu syarat terpenuhi. Kalau dua-duanya terpenuhi, tentu juga boleh.
- **Teks layar:** Kata *atau*: cukup *salah satu* syarat terpenuhi. / Kalau dua-duanya terpenuhi, juga boleh.

## IDE DASAR

**6. `all`** · 1:11.1 – 1:26.2

- **Animasi:** 6×6 table with dice headers; all 36 cells appear.
- **Narasi:** Kita mulai dari semua kemungkinan. Dadu pertama punya enam mata, dadu kedua juga enam. Enam kali enam, ada tiga puluh enam pasangan.
- **Teks layar:** Mulai dari *semua* kemungkinan. / Dadu pertama 6 mata, dadu kedua 6 mata. / 6 × 6 = *36* pasangan.

**7. `sums`** · 1:26.2 – 1:32.4

- **Animasi:** Each cell shows the sum of its two dice.
- **Narasi:** Di setiap kotak, kita tulis jumlah kedua mata dadunya.
- **Teks layar:** Di setiap kotak, tulis *jumlah* kedua mata dadunya.

## SELESAIKAN

**8. `more_cells`** · 1:32.4 – 1:48.4

- **Animasi:** Cells with sum 10, 11, 12 turn orange (3 + 2 + 1 = 6).
- **Narasi:** Sekarang warnai kotak yang jumlahnya lebih dari sembilan. Jumlah sepuluh ada tiga kotak, sebelas ada dua kotak, dan dua belas ada satu kotak. Totalnya enam.
- **Teks layar:** Warnai kotak dengan jumlah lebih dari 9. / 10: tiga kotak, 11: dua kotak, 12: satu kotak. / Totalnya *6*.

**9. `same_cells`** · 1:48.4 – 1:59.2

- **Animasi:** The diagonal (equal dice) is outlined blue: 6 cells.
- **Narasi:** Lalu tandai pasangan kembar. Mereka berada di garis miring ini. Jumlahnya juga enam kotak.
- **Teks layar:** Lalu tandai pasangan *kembar*. / Mereka di garis miring ini: juga *6* kotak.

**10. `both`** · 1:59.2 – 2:10.5

- **Animasi:** Cells (5,5) and (6,6) pulse: orange and blue at once.
- **Narasi:** Perhatikan dua kotak ini: lima lima, dan enam enam. Keduanya memenuhi dua syarat sekaligus.
- **Teks layar:** Perhatikan dua kotak ini: (5,5) dan (6,6). / Keduanya memenuhi *dua* syarat sekaligus.

**11. `twice`** · 2:10.5 – 2:23.4

- **Animasi:** 6 + 6 = 12 with the two shared cells marked twice.
- **Narasi:** Kalau kita langsung menjumlahkan enam ditambah enam, dua kotak ini terhitung dua kali. Padahal setiap kotak cukup dihitung satu kali.
- **Teks layar:** Kalau langsung 6 + 6, dua kotak ini terhitung *dua kali*. / Padahal setiap kotak cukup dihitung *satu kali*.

**12. `minus`** · 2:23.4 – 2:31.8

- **Animasi:** 6 + 6 − 2 = 10.
- **Narasi:** Jadi, enam ditambah enam, dikurangi dua, sama dengan sepuluh kotak.
- **Teks layar:** Jadi 6 + 6 − 2 = *10* kotak.

**13. `compute`** · 2:31.8 – 2:44.0

- **Animasi:** Peluang = 10/36, ÷2 -> 5/18.
- **Narasi:** Peluangnya sepuluh per tiga puluh enam. Bagi atas dan bawah dengan dua. Hasilnya lima per delapan belas.
- **Teks layar:** Peluangnya 10/36. / Bagi atas dan bawah dengan 2: *5/18*.

## JAWABAN

**14. `answer`** · 2:44.0 – 2:51.4

- **Animasi:** Options return; B is confirmed.
- **Narasi:** Jadi, jawabannya adalah B, lima per delapan belas.
- **Teks layar:** Jawabannya *B*, yaitu 5/18.

**15. `check`** · 2:51.4 – 3:05.7

- **Animasi:** The 10 coloured cells are counted one by one with a counter.
- **Narasi:** Kita cek dengan menghitung langsung kotak yang berwarna. Satu, dua, tiga, sampai sepuluh. Cocok, sepuluh kotak!
- **Teks layar:** Cek: hitung langsung kotak yang berwarna. / 1, 2, 3, ... sampai *10*. Cocok!

**16. `trap`** · 3:05.7 – 3:18.5

- **Animasi:** 12/36 = 1/3 with a red cross: not among the options.
- **Narasi:** Kalau dua kotak tadi terhitung dua kali, hasilnya dua belas per tiga puluh enam, yaitu sepertiga. Itu tidak ada di pilihan.
- **Teks layar:** Kalau terhitung dua kali: 12/36 = 1/3. / Itu *tidak* ada di pilihan.

## INGAT

**17. `remember`** · 3:19.0 – 3:33.6

- **Animasi:** Summary card: 'atau' = gabungkan; yang masuk dua kelompok dihitung sekali.
- **Narasi:** Yang perlu diingat. Untuk kejadian atau, gabungkan semua kotak yang cocok. Tapi kotak yang masuk dua kelompok cukup dihitung satu kali.
- **Teks layar:** Yang perlu diingat: / kejadian *atau* = gabungkan semua kotak yang cocok, / tapi yang masuk dua kelompok dihitung *satu kali*.

---

## Naskah narasi lengkap


**[SOAL]**

Yuk, baca soalnya bersama. Dua dadu dilempar bersamaan. Berapa peluang jumlah mata dadu lebih dari sembilan, atau kedua mata dadu sama?

Pilihannya: seperempat, lima per delapan belas, tujuh per delapan belas, atau sebelas per delapan belas.


**[MAKSUDNYA]**

Ada dua syarat di sini. Syarat pertama: jumlahnya lebih dari sembilan. Hati-hati, sembilan sendiri tidak termasuk. Jadi jumlahnya sepuluh, sebelas, atau dua belas.

Syarat kedua: kedua mata dadu sama. Misalnya satu dan satu, atau lima dan lima. Kita sebut ini pasangan kembar.

Lalu kata atau. Artinya, cukup salah satu syarat terpenuhi. Kalau dua-duanya terpenuhi, tentu juga boleh.


**[IDE DASAR]**

Kita mulai dari semua kemungkinan. Dadu pertama punya enam mata, dadu kedua juga enam. Enam kali enam, ada tiga puluh enam pasangan.

Di setiap kotak, kita tulis jumlah kedua mata dadunya.


**[SELESAIKAN]**

Sekarang warnai kotak yang jumlahnya lebih dari sembilan. Jumlah sepuluh ada tiga kotak, sebelas ada dua kotak, dan dua belas ada satu kotak. Totalnya enam.

Lalu tandai pasangan kembar. Mereka berada di garis miring ini. Jumlahnya juga enam kotak.

Perhatikan dua kotak ini: lima lima, dan enam enam. Keduanya memenuhi dua syarat sekaligus.

Kalau kita langsung menjumlahkan enam ditambah enam, dua kotak ini terhitung dua kali. Padahal setiap kotak cukup dihitung satu kali.

Jadi, enam ditambah enam, dikurangi dua, sama dengan sepuluh kotak.

Peluangnya sepuluh per tiga puluh enam. Bagi atas dan bawah dengan dua. Hasilnya lima per delapan belas.


**[JAWABAN]**

Jadi, jawabannya adalah B, lima per delapan belas.

Kita cek dengan menghitung langsung kotak yang berwarna. Satu, dua, tiga, sampai sepuluh. Cocok, sepuluh kotak!

Kalau dua kotak tadi terhitung dua kali, hasilnya dua belas per tiga puluh enam, yaitu sepertiga. Itu tidak ada di pilihan.


**[INGAT]**

Yang perlu diingat. Untuk kejadian atau, gabungkan semua kotak yang cocok. Tapi kotak yang masuk dua kelompok cukup dihitung satu kali.
