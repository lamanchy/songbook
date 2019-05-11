from PIL import Image, ImageDraw

from pil_quality_pdf.fonts import get_font
from pil_quality_pdf.rendering import PdfWriter, mm_to_px
from scripts.song import Song

if __name__ == "__main__":
    songs = Song.load_songs()

    with PdfWriter("songbook") as f:
        for song in songs:
            page = Image.new("RGB", mm_to_px(210, 297), (255, 255, 255))

            draw = ImageDraw.Draw(page)

            draw.text(mm_to_px(20, 20), song.text.text, font=get_font(20))

            f.write(page)
