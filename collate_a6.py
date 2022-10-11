import os
from os.path import join

import img2pdf
from PIL import Image

from pil_quality_pdf.quality_constants import RESOLUTION_DPI
from pil_quality_pdf.rendering import PdfWriter, mm_to_px, do_antialiasing
from scripts.rendered_text import RenderedText
from scripts.settings import BASE_DIR

dirname = join(BASE_DIR, 'to_collate')

def get_png_path(i, prefix=''):
    return os.path.join(dirname, f"{prefix}{i:09}" + ".png")

def rename(a, b):
    print(f'renaming {a} to {b}')
    os.rename(a, b)

if __name__ == "__main__":
    images = list(os.listdir(dirname))
    num = len(images) // 8 + 1

    for i in range(num):
        number = i * 8
        switch = [2, 6, 8, 7, 4, 5, 3]

        rename(get_png_path(number), get_png_path(number, 'collated_'))

        for o in range(len(switch)):
            if os.path.exists(get_png_path(number + switch[o] - 1)):
                rename(
                    get_png_path(number + switch[o] - 1),
                    get_png_path(number + switch[(o+1) % len(switch)] - 1, 'collated_')
                )
            else:
                page = Image.new("RGB", mm_to_px(RenderedText.page_size), (255, 255, 255))
                page = do_antialiasing(page)
                page.save(get_png_path(number + switch[(o+1) % len(switch)] - 1, 'collated_'), dpi=(RESOLUTION_DPI, RESOLUTION_DPI))

    images = [join(dirname, img) for img in os.listdir(dirname)]
    with open("collated.pdf", "wb") as f:
        f.write(img2pdf.convert(images))
