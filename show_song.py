import sys

from PIL import Image

from pil_quality_pdf.local_quality_constants import ANTIALIASING
from pil_quality_pdf.rendering import mm_to_px, show, save
from scripts.rendered_song import RenderedSong
from scripts.song import Song

if __name__ == "__main__":
    file_name = sys.argv[1]
    no_capo = False

    song = Song(file_name, [])
    rendered = RenderedSong(song, no_capo)
    to_show = Image.new("RGB", mm_to_px((297, 210)), (255, 255, 255))
    for i, page in enumerate(rendered.get_pages()):
        page = page.resize(mm_to_px((297 / 2, 210)), resample=ANTIALIASING)
        to_show.paste(page, mm_to_px((297 / 2 * i, 0)))

    show(to_show)
    save("shown.png", to_show)
