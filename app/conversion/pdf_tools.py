from pathlib import Path
import os
import subprocess
import shutil


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
    # DOCX->PDF нормально делается через LibreOffice.
    # Пока заглушка, чтобы архитектура была готова.
    out_pdf.write_text(f"TODO: convert {doc_path.name} to real PDF\n", encoding="utf-8")
    return out_pdf