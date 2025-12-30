from pathlib import Path
from PIL import Image

# Фото в pdf
def photo_to_pdf(image_path: Path, out_pdf: Path) -> Path:
    image = Image.open(image_path).convert('RGB')
    image.save(out_pdf, "PDF")
    return out_pdf

# Несколько фото в один pdf
def combine_images_to_pdf(image_path: list[Path], out_pdf: Path) -> Path:
    imgs = [Image.open(p).convert('RGB') for p in image_path]
    first, rest = imgs[0], imgs[1:]
    first.save(out_pdf, "PDF", save_all=True, append_images=rest)
    return out_pdf



