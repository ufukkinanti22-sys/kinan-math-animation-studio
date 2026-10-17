# Voice swap: narator AI → suara pemilik (Seed-VC)

Mengganti **hanya suara narator** di video yang sudah jadi. Metode: *speech-to-speech voice
conversion* zero-shot dengan [Seed-VC](https://github.com/Plachtaa/seed-vc), bukan membuat ulang
narasi lewat TTS. Kata, jeda, tempo, dan waktu mulai tiap segmen mengikuti narator asli.

| Tidak diubah | Cara dijamin |
|---|---|
| Gambar, animasi, caption, urutan adegan, resolusi, durasi | video asli disalin `-c:v copy`; MD5 tiap paket dan tiap frame hasil decode dibandingkan dengan video asli |
| Naskah | segmen sumber = `assets/audio/<id>/<beat>.mp3` (trek narator terpisah, tanpa musik); teks tidak disentuh |

## Alur

```
ZIP rekaman suara ──► prepare_reference ──► reference.wav (24 s, satu pembicara, paling bersih)
assets/audio/<id>/<beat>.mp3 ──► convert_beats (Seed-VC) ──► <beat>.wav
        ──► verify (kata lengkap? waktu? mirip suara?) ──► assemble (jadwal asli + loudnorm + mux) ──► MP4 baru
```

* `prepare_reference.py` memilih klip dari rekaman: konsistensi pembicara (Resemblyzer), nada-latar/musik
  (puncak sempit stasioner di frame sunyi), lantai noise, aktivitas bicara. Tanpa denoise (merusak timbre).
* `convert_beats.py` memuat Seed-VC sekali, mengonversi tiap segmen (`diffusion-steps 30`,
  `length-adjust 1.0`, `cfg 0.7`, tanpa f0), seed tetap per segmen, bisa dilanjutkan bila terputus.
* `verify.py`: (1) faster-whisper (Indonesia) mentranskripsi narator asli *dan* hasil konversi lalu
  membandingkannya dengan naskah (WER/CER), jadi konversi tidak boleh menambah kesalahan; (2) selisih
  durasi, korelasi/lag envelope, selisih waktu mulai kata; (3) kemiripan suara terhadap referensi
  dengan narator asli sebagai garis dasar.
* `assemble.py`: tiap segmen diletakkan pada waktu mulainya di `output/qc/<id>/beats.json`
  (+1024 sampel, tunda AAC yang sama dengan video asli), panjangnya disamakan dengan segmen asli,
  level bicara disamakan, `loudnorm I=-16 TP=-1.5 LRA=11` seperti render asli.
* `run.py` menjalankan semuanya. Tahap `trial` hanya P01; tahap `rest` menolak jalan bila P01 belum lolos.

## Menjalankan

**Colab (GPU gratis, cadangan):** buka
[`kinan_voice_swap_colab.ipynb`](https://colab.research.google.com/github/ufukkinanti22-sys/kinan-math-animation-studio/blob/claude/math-animation-studio-577wfc/voice_swap/kinan_voice_swap_colab.ipynb).

**Lokal / CPU atau GPU:**

```bash
git clone https://github.com/Plachtaa/seed-vc seed-vc
pip install -r voice_swap/requirements.txt   # versi dipatok: transformers<5 dan huggingface_hub<1.0 wajib
python -m voice_swap.run --zip Kinan_Voice_References.zip --seedvc-dir seed-vc --stage trial
python -m voice_swap.run --zip Kinan_Voice_References.zip --seedvc-dir seed-vc --stage rest
```

Perlu akses ke `huggingface.co` (model Seed-VC, Whisper, BigVGAN, CAM++, faster-whisper). Hasil di
`voice_out/` (video baru bernama `<id>_suara_kinan.mp4`, atau `..._BELUM_LOLOS.mp4` bila verifikasi gagal;
WAV penuh per video di `voice_out/audio/`, WAV per segmen di `voice_private/converted/`).
Perkiraan waktu di CPU 4 inti: 1–1,5 jam untuk keempat video (diukur: difusi ±7–10× lebih lambat dari
waktu nyata); di GPU T4: hitungan menit.

## Privasi

`voice_private/` dan `voice_out/` ada di `.gitignore`, begitu juga `*.m4a`, `*.aac`, `*.wav`.
**Jangan** menyimpan rekaman suara, klip referensi, atau hasil konversi di repositori publik ini.
Hasil diserahkan lewat unduhan langsung (Colab / lampiran), bukan lewat commit.

## Lisensi (untuk penggunaan Kinan Learning)

| Komponen | Lisensi | Status verifikasi |
|---|---|---|
| Kode Seed-VC | **GPL-3.0** (berkas `LICENSE` di repositori Seed-VC) | terverifikasi |
| Model Seed-VC `Plachta/Seed-VC` | **gpl-3.0** | terverifikasi dari kartu model, 2026-10-17 |
| `openai/whisper-small` | **apache-2.0** | terverifikasi dari kartu model, 2026-10-17 |
| `nvidia/bigvgan_v2_22khz_80band_256x` | **mit** | terverifikasi dari kartu model, 2026-10-17 |
| `funasr/campplus` | **apache-2.0** | terverifikasi dari kartu model, 2026-10-17 |

`python -m voice_swap.check_licenses --seedvc-dir seed-vc` membaca lisensi tiap model langsung dari kartu
model di Hugging Face dan menulisnya ke `voice_out/reports/licenses.json` (dijalankan otomatis oleh `run.py`).
Kartu model hanya menyebut lisensi bobot model; kebijakan penggunaan data pelatihan tidak ikut terperiksa.

Catatan GPL-3.0: Seed-VC dipakai sebagai program terpisah (di-*clone* saat dijalankan, tidak disalin ke
repositori ini). GPL mewajibkan sumber terbuka bila Anda *mendistribusikan* kode Seed-VC (atau turunannya);
audio keluaran bukan karya turunan kode tersebut.

## Hasil uji nyata (P01, 2026-10-17, CPU 4 inti)

* Konversi 21 segmen P01 jalan penuh dengan Seed-VC (30 langkah, ±25× lebih lambat dari waktu nyata di CPU).
* Kemiripan dengan suara pemilik: narator AI 0,545 → hasil konversi **0,874** (klip rekaman pemilik saling 0,88).
* Durasi tiap segmen identik (selisih < 12 ms), selisih waktu 0 s/d −10 ms, korelasi envelope 0,81–0,89.
* Gambar identik dengan video asli (paket dan frame), kelantangan −16,0 LUFS, QC proyek lulus.
* Pengenalan ucapan (Whisper medium): 19 dari 21 segmen sama dengan narator asli. Dua segmen masih ditandai
  setelah dua kali konversi ulang (dan `cfg` 1,0): `axes` ("sampai" tidak terdengar) dan `trap`
  ("pilihan" terdengar "pimihan"). Perlu didengarkan oleh telinga manusia.

Temuan selama uji: Whisper *small* memberi alarm palsu dan melewatkan cacat nyata, karena itu verifikasi memakai
*medium*; awal segmen bisa rusak bila tidak diberi jeda hening di depan (sekarang selalu diberi 0,5 s); versi
`transformers`/`huggingface_hub` terbaru tidak cocok dengan Seed-VC (lihat `requirements.txt`).

## Yang belum diuji
Notebook Colab (belum pernah dijalankan), serta video P02, P03, dan P00 (menunggu keputusan setelah P01).
