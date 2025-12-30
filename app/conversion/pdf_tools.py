from pathlib import Path

def squeeze_pdf(pdf_path: Path, out_pdf: Path) -> Path:
    # Реальное “сжатие” PDF — отдельная тема (ghostscript/qpdf и т.д.)
    # Пока делаем копию как каркас.
    out_pdf.write_bytes(pdf_path.read_bytes())
    return out_pdf


def doc_to_pdf(doc_path: Path, out_pdf: Path) -> Path:
    # DOCX->PDF нормально делается через LibreOffice.
    # Пока заглушка, чтобы архитектура была готова.
    out_pdf.write_text(f"TODO: convert {doc_path.name} to real PDF\n", encoding="utf-8")
    return out_pdf