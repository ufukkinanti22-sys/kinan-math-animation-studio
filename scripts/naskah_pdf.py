#!/usr/bin/env python3
"""Gabungkan naskah_rekaman.txt semua video menjadi satu PDF (besar, nyaman dibaca
di HP) dan satu ZIP berisi TXT asli + PDF.

    pip install reportlab
    python scripts/naskah_pdf.py

Teks narasi dan line break TIDAK diubah. Karena layar HP sempit, baris yang lebih
lebar dari halaman dibungkus secara visual; baris lanjutan diberi indentasi
(menjorok) supaya line break asli tetap terlihat.

Hasil: output/naskah/Naskah_Rekaman_Voice_Over_Matematika.pdf dan .zip
"""

import sys
import zipfile
from pathlib import Path

import yaml
from reportlab.pdfbase import pdfmetrics
from reportlab.pdfbase.ttfonts import TTFont
from reportlab.pdfgen import canvas

ROOT = Path(__file__).resolve().parents[1]
OUT = ROOT / "output" / "naskah"
TITLE = "Naskah Rekaman Voice Over Matematika"
STEM = "Naskah_Rekaman_Voice_Over_Matematika"

# urutan video: soal 1-3 dari lembar guru, lalu video contoh
VIDEOS = ["p01_dadu_berbeda", "p02_tiga_koin", "p03_kartu_bridge", "p00_poc_binomial"]
LABELS = {"p01_dadu_berbeda": "Video 1", "p02_tiga_koin": "Video 2",
          "p03_kartu_bridge": "Video 3", "p00_poc_binomial": "Video 4"}
NOTES = {"p00_poc_binomial": "Video contoh (uji coba)"}  # baris kecil di bawah judul

# halaman berukuran layar HP (9:16), font besar
MM = 72 / 25.4
W, H = 110 * MM, 195 * MM
MARGIN = 9 * MM
BODY_PT, LEAD = 21, 30
HANG = 16  # indentasi baris lanjutan (pt)
BLOCK_GAP = 30  # jarak antarblok narasi (pt)
INK, GREY, ACCENT = (0.09, 0.08, 0.15), (0.45, 0.43, 0.5), (0.2, 0.36, 0.9)

FONT_DIR = ROOT / "assets" / "fonts"
pdfmetrics.registerFont(TTFont("Body", str(FONT_DIR / "KinanNunito-Bold.ttf")))
pdfmetrics.registerFont(TTFont("Head", str(FONT_DIR / "KinanNunito-Black.ttf")))


def wrap_visual(line: str, font: str, size: float, width: float) -> list[str]:
    """Bungkus satu baris asli menjadi beberapa baris visual (hanya jika terlalu lebar).
    Baris lanjutan lebih sempit sebesar HANG karena menjorok."""
    out, cur = [], ""
    limit = width
    for w in line.split(" "):
        trial = f"{cur} {w}".strip()
        if cur and pdfmetrics.stringWidth(trial, font, size) > limit:
            out.append(cur)
            cur = w
            limit = width - HANG
        else:
            cur = trial
    out.append(cur)
    return out


def load_blocks(pid: str) -> list[list[str]]:
    text = (ROOT / "problems" / pid / "naskah_rekaman.txt").read_text(encoding="utf-8")
    return [b.split("\n") for b in text.strip("\n").split("\n\n")]


def build(pdf_path: Path, pages_of: dict[str, int] | None = None) -> dict[str, int]:
    c = canvas.Canvas(str(pdf_path), pagesize=(W, H))
    c.setTitle(TITLE)
    c.setAuthor("Kinan Math Animation Studio")
    c.setSubject("Naskah rekaman suara untuk video animasi matematika")
    text_w = W - 2 * MARGIN
    state = {"page": 0, "section": None}
    first_pages: dict[str, int] = {}

    def footer():
        c.setFont("Body", 9)
        c.setFillColorRGB(*GREY)
        c.drawCentredString(W / 2, 6 * MM, f"{state['section'] or TITLE}  ·  {state['page']}")

    def new_page(section: str | None):
        if state["page"]:
            footer()
            c.showPage()
        state["page"] += 1
        state["section"] = section
        return H - MARGIN

    # ---- sampul
    y = new_page(None)
    c.setFillColorRGB(*ACCENT)
    c.rect(0, H - 14 * MM, W, 14 * MM, stroke=0, fill=1)
    y = H - 52 * MM
    c.setFillColorRGB(*INK)
    for line in ["Naskah Rekaman", "Voice Over", "Matematika"]:
        c.setFont("Head", 34)
        c.drawString(MARGIN, y, line)
        y -= 42
    y -= 14
    c.setFont("Body", 15)
    c.setFillColorRGB(*GREY)
    for line in ["Baca persis seperti tertulis.", "Satu baris = satu caption.",
                 "Jarak kosong = ganti bagian.", "Baris menjorok = lanjutan", "baris di atasnya (masih satu baris)."]:
        c.drawString(MARGIN, y, line)
        y -= 22
    y -= 18
    c.setFont("Head", 16)
    c.setFillColorRGB(*INK)
    c.drawString(MARGIN, y, "Isi")
    y -= 26
    for pid in VIDEOS:
        c.setFont("Body", 15)
        c.setFillColorRGB(*INK)
        c.drawString(MARGIN, y, LABELS[pid] + (" (contoh)" if pid in NOTES else ""))
        if pages_of:
            c.drawRightString(W - MARGIN, y, f"hal. {pages_of[pid]}")
        y -= 24

    # ---- tiap video
    for pid in VIDEOS:
        script = yaml.safe_load((ROOT / "problems" / pid / "narration.yaml").read_text(encoding="utf-8"))
        y = new_page(LABELS[pid])
        first_pages[pid] = state["page"]
        c.setFillColorRGB(*ACCENT)
        c.rect(0, H - 14 * MM, W, 14 * MM, stroke=0, fill=1)
        y = H - 34 * MM
        c.setFillColorRGB(*INK)
        c.setFont("Head", 30)
        c.drawString(MARGIN, y, LABELS[pid].upper())
        y -= 30
        c.setFont("Body", 15)
        c.setFillColorRGB(*GREY)
        for part in wrap_visual(script["title"], "Body", 15, text_w):
            c.drawString(MARGIN, y, part)
            y -= 21
        if pid in NOTES:
            c.drawString(MARGIN, y, NOTES[pid])
            y -= 21
        y -= 22
        bottom = MARGIN + 6 * MM

        for block in load_blocks(pid):
            visual = [wrap_visual(line, "Body", BODY_PT, text_w) for line in block]
            height = sum(len(v) for v in visual) * LEAD
            if y - height < bottom and y < H - MARGIN - 40:  # blok utuh pindah ke halaman baru
                y = new_page(f"{LABELS[pid]} (lanjutan)")
            for parts in visual:
                for k, part in enumerate(parts):
                    c.setFont("Body", BODY_PT)
                    c.setFillColorRGB(*INK)
                    c.drawString(MARGIN + (HANG if k else 0), y - BODY_PT, part)
                    y -= LEAD
            # jarak + garis tipis antarblok
            c.setStrokeColorRGB(0.85, 0.84, 0.88)
            c.setLineWidth(1.2)
            c.line(MARGIN, y - BLOCK_GAP / 2 + 6, MARGIN + 24, y - BLOCK_GAP / 2 + 6)
            y -= BLOCK_GAP
    footer()
    c.save()
    return first_pages


def main():
    OUT.mkdir(parents=True, exist_ok=True)
    pdf = OUT / f"{STEM}.pdf"
    pages = build(pdf)  # lintasan 1: cari halaman awal tiap video
    build(pdf, pages)  # lintasan 2: daftar isi dengan nomor halaman
    zpath = OUT / f"{STEM}.zip"
    with zipfile.ZipFile(zpath, "w", zipfile.ZIP_DEFLATED) as z:
        z.write(pdf, f"{STEM}/{pdf.name}")
        for pid in VIDEOS:
            z.write(ROOT / "problems" / pid / "naskah_rekaman.txt", f"{STEM}/{pid}/naskah_rekaman.txt")
    print(pdf.relative_to(ROOT), pdf.stat().st_size)
    print(zpath.relative_to(ROOT), zpath.stat().st_size)


if __name__ == "__main__":
    sys.exit(main())
