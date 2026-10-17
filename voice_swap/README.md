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
pip install torch torchaudio munch einops transformers huggingface_hub pyyaml pydub scipy librosa soundfile \
    descript-audio-codec resemblyzer faster-whisper jiwer num2words matplotlib scikit-learn
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
| Model Seed-VC `Plachta/Seed-VC` | ? | **belum terverifikasi** (huggingface.co tidak bisa diakses saat pembuatan) |
| `openai/whisper-small` | ? | belum terverifikasi |
| `nvidia/bigvgan_v2_22khz_80band_256x` | ? | belum terverifikasi |
| `funasr/campplus` | ? | belum terverifikasi |

`python -m voice_swap.check_licenses --seedvc-dir seed-vc` membaca lisensi tiap model langsung dari kartu
model di Hugging Face dan menulisnya ke `voice_out/reports/licenses.json` (dijalankan otomatis oleh `run.py`).
**Periksa hasilnya sebelum memakai audio untuk keperluan komersial.**

Catatan GPL-3.0: Seed-VC dipakai sebagai program terpisah (di-*clone* saat dijalankan, tidak disalin ke
repositori ini). GPL mewajibkan sumber terbuka bila Anda *mendistribusikan* kode Seed-VC (atau turunannya);
audio keluaran bukan karya turunan kode tersebut.

## Yang sudah dan belum diuji

Sudah diuji (tanpa model, di sesi pembuatan): pemilihan referensi pada rekaman asli; susunan ulang audio
dari narator asli vs audio di video jadi (korelasi 0,996–0,999, selisih waktu 0,0 ms); penempelan ke
video asli (paket dan frame identik); normalisasi teks / WER; jalur ukur waktu dan kemiripan.

**Belum diuji:** konversi Seed-VC itu sendiri, pengenalan ucapan Whisper, dan notebook Colab: sesi
pembuatan tidak punya GPU dan `huggingface.co` diblokir (403). Belum ada hasil suara hasil konversi.
