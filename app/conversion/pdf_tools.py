from pathlib import Path
import os
import subprocess
import shutil

from PyPDF2 import PdfMerger


def squeeze_pdf(pdf_path: Path, out_pdf: Path) -> Path:
    gs = shutil.which("gswin64c") or shutil.which("gs")
    if not gs and os.name == "nt":
        candidates = [
            r"C:\Program Files\gs\gs10.06.0\bin\gswin64c.exe",
            r"C:\Program Files\gs\gs10.06.0\bin\gswin64c",
        ]
        for c in candidates:
            if Path(c).exists():
                gs = c
                break

    if not gs:
        raise RuntimeError("Ghostscript not found. Install it and make sure it's in PATH.")

    out_pdf.parent.mkdir(parents=True, exist_ok=True)

    cmd = [
        gs,
        "-sDEVICE=pdfwrite",
        "-dCompatibilityLevel=1.4",
        "-dPDFSETTINGS=/ebook",
        "-dNOPAUSE",
        "-dQUIET",
        "-dBATCH",
        f"-sOutputFile={str(out_pdf)}",
        str(pdf_path),
    ]
    subprocess.run(cmd, check=True)
    return out_pdf

def doc_to_pdf(doc_path: Path, out_pdf: Path) -> Path:
    soffice = shutil.which("soffice") or shutil.which("libreoffice")

    if not soffice and os.name == "nt":
        candidates = [
            r"C:\Program Files\LibreOffice\program\soffice.com",
            r"C:\Program Files\LibreOffice\program\soffice.exe",
            r"C:\Program Files (x86)\LibreOffice\program\soffice.com",
            r"C:\Program Files (x86)\LibreOffice\program\soffice.exe",
        ]
        for c in candidates:
            if Path(c).exists():
                soffice = c
                break

    if not soffice:
        raise RuntimeError("LibreOffice (soffice) not found. Install LibreOffice and/or add it to PATH.")

    out_pdf.parent.mkdir(parents=True, exist_ok=True)

    outdir = out_pdf.parent
    expected = outdir / f"{doc_path.stem}.pdf"

    cmd = [
        soffice,
        "--headless",
        "--nologo",
        "--nofirststartwizard",
        "--convert-to", "pdf",
        "--outdir", str(outdir),
        str(doc_path),
    ]

    subprocess.run(cmd, check=True)

    if not expected.exists():
        raise RuntimeError("LibreOffice did not produce output PDF.")

    if expected != out_pdf:
        if out_pdf.exists():
            out_pdf.unlink()
        expected.rename(out_pdf)

    return out_pdf


def pdf_to_one(pdf_path: list[Path], out_pdf: Path) -> Path:
    out_pdf.parent.mkdir(parents=True, exist_ok=True)

    merger = PdfMerger()

    try:
        for p in pdf_path:
            merger.append(str(p))
        with open(out_pdf, "wb") as file:
            merger.write(file)
    finally:
        merger.close()
    return out_pdf

