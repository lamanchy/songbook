import logging
import sys

from PIL import Image

from pil_quality_pdf.quality_constants import ANTIALIASING
from pil_quality_pdf.rendering import mm_to_px, show, save
from scripts.rendered_song import RenderedSong
from scripts.rendered_text import RenderedText
from scripts.song import Song

if __name__ == "__main__":
    file_name = sys.argv[1][6:]
    capo_setting = [
        'guitar',
        'piano',
        'ukulele',
    ][0]

    song = Song(file_name, [])
    rendered = RenderedSong(song, capo_setting)
    to_show = Image.new("RGB", mm_to_px((297, 210)), (255, 255, 255))
    for i, page in enumerate(rendered.get_pages()):
        page = page.resize(mm_to_px((297 / 2, 210)), resample=ANTIALIASING)
        to_show.paste(page, mm_to_px((297 / 2 * i, 0)))

    if rendered.font_size < RenderedText.text_font_size:
        logging.warning(f"Song {song.title} has too large {rendered.get_problems()} "
                        f"{rendered.font_size}/{RenderedText.text_font_size}.")

    show(to_show)
    input()
    save("shown.png", to_show)
