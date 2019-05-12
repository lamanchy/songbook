import logging

from pil_quality_pdf.rendering import PdfWriter
from scripts.rendered_song import RenderedSong
from scripts.rendered_text import RenderedText
from scripts.song import Song

if __name__ == "__main__":
    songs = Song.load_songs()

    with PdfWriter("songbook") as f:
        # songs = songs[:4]
        # songs = [song for song in songs if song.title.startswith("Bíl")]

        single_page_waiting_for_another = None
        worst = []
        for i, song in enumerate(songs):
            rendered = RenderedSong(song)
            pages = rendered.get_pages()

            if len(pages) == 2:
                for page in pages:
                    f.write(page)

            else:
                if single_page_waiting_for_another is None:
                    single_page_waiting_for_another = pages[0]
                else:
                    f.write(single_page_waiting_for_another)
                    f.write(pages[0])
                    single_page_waiting_for_another = None

            if rendered.font_size < RenderedText.text_font_size:
                logging.warning(
                    f"Song {song.title} has too large {rendered.get_problems()} {rendered.font_size}/{RenderedText.text_font_size}.")
                worst.append((rendered.font_size, song.title, rendered.get_problems()))

        if single_page_waiting_for_another is not None:
            f.write(single_page_waiting_for_another)

        print()
        if len(worst) > 0:
            logging.warning(f"10 smallest songs:")
            for font_size, title, problem in reversed(list(sorted(worst, key=lambda t: t[0]))[:10]):
                logging.warning(
                    f"Font size: {font_size}/{RenderedText.text_font_size}, problem: {problem}, song: {title}")
