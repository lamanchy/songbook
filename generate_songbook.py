import logging

import czech_sort
from PIL import ImageDraw, Image

from pil_quality_pdf.fonts import get_font, get_max_font_size
from pil_quality_pdf.rendering import PdfWriter, mm_to_px
from scripts.rendered_song import RenderedSong
from scripts.rendered_text import RenderedText
from scripts.song import Song

if __name__ == "__main__":
    songs = Song.load_songs()
    no_capo = True

    with PdfWriter("songbook") as f:
        # songs = songs[:10]
        # songs = [song for song in songs if song.title.startswith("Divokej ")]
        draw = ImageDraw.Draw(Image.new("RGB", (0, 0), (255, 255, 255)))

        num_of_pages = 1
        while True:
            i = (len(songs) + 1) // num_of_pages
            list_font_size = get_max_font_size(
                draw, "\n".join(["A" for a in range(i // 2)]), None,
                mm_to_px(RenderedText.page_size[1] - RenderedText.delta * 2), RenderedText.text_font_size
            )[0]
            if list_font_size >= RenderedText.list_font_size:
                break
            num_of_pages += 1

        f.counter = num_of_pages * 2 + 1

        single_song_waiting_for_another = None
        worst = []

        written_songs = []
        c = 0


        def write(rendered):
            song = rendered.song
            global c
            written_songs.append((song, c + 1))
            for page in rendered.get_pages():
                c += 1
                if c % 2 == 0:
                    draw = ImageDraw.Draw(page)
                    text = f"{c}."
                    font = get_font(RenderedText.note_font_size)
                    size = draw.textsize(text, font)
                    draw.text((page.size[0] - mm_to_px(RenderedText.delta) - size[0],
                               page.size[1] - mm_to_px(RenderedText.delta) - size[1]),
                              text, font=font, fill=(0, 0, 0))
                f.write(page)

        for i, song in enumerate(songs):
            rendered = RenderedSong(song, no_capo)

            if len(rendered.texts) == 2:
                write(rendered)

            else:
                if single_song_waiting_for_another is None:
                    single_song_waiting_for_another = rendered
                else:
                    write(single_song_waiting_for_another)
                    write(rendered)
                    single_song_waiting_for_another = None

            if rendered.font_size < RenderedText.text_font_size:
                logging.warning(
                    f"Song {song.title} has too large {rendered.get_problems()} {rendered.font_size}/{RenderedText.text_font_size}.")
                worst.append((rendered.font_size, song.title, rendered.get_problems()))

        if single_song_waiting_for_another is not None:
            write(single_song_waiting_for_another)

        print()
        if len(worst) > 0:
            logging.warning(f"Smallest songs:")
            for font_size, title, problem in reversed(list(sorted(worst, key=lambda t: t[0]))[:100]):
                logging.warning(
                    f"Font size: {font_size}/{RenderedText.text_font_size}, problem: {problem}, song: {title}")

        counter = f.counter
        f.counter = 0

        page = Image.new("RGB", mm_to_px(RenderedText.page_size), (255, 255, 255))
        draw = ImageDraw.Draw(page)
        text = "Blonďákův"
        font = get_font(RenderedText.title_font_size * 1.5)
        size = draw.textsize(text, font)
        draw.text((page.size[0] // 2 - size[0] // 2, page.size[1] // 2 - size[1] * 1.1),
                  text, font=font, fill=(0, 0, 0))
        text = "zpěvník"
        size = draw.textsize(text, font)
        draw.text((page.size[0] // 2 - size[0] // 2, page.size[1] // 2),
                  text, font=font, fill=(0, 0, 0))

        text = "lamanchy@gmail.com"
        font = get_font(RenderedText.text_font_size)
        size = draw.textsize(text, font)
        draw.text((page.size[0] - mm_to_px(RenderedText.delta) - size[0],
                   page.size[1] - mm_to_px(RenderedText.delta) - size[1]),
                  text, font=font, fill=(0, 0, 0))

        f.write(page)

        written_songs.sort(key=lambda written: czech_sort.key(written[0].title))
        font = get_font(list_font_size)
        for page_i in range(num_of_pages):
            tw = written_songs[
                 page_i * len(written_songs) // num_of_pages:(page_i + 1) * len(written_songs) // num_of_pages]
            o = (len(tw) + 1) // 2
            for ttw in [tw[:o], tw[o:]]:
                page = Image.new("RGB", mm_to_px(RenderedText.page_size), (255, 255, 255))
                draw = ImageDraw.Draw(page)

                text = "\n".join(list(map(lambda song: song[0].title, ttw)))
                draw.text((RenderedText.text_pos[0] * 2, RenderedText.text_pos[1]), text,
                          font=font, fill=(0, 0, 0), spacing=list_font_size / 15.0)

                pages = list(map(lambda song: str(song[1]), ttw))
                size = draw.textsize("A" * max(map(lambda i: len(i), pages), default=1), font)[0]
                text = "\n".join(pages)
                draw.text((page.size[0] - RenderedText.text_pos[0] * 2 - size, RenderedText.text_pos[1]),
                          text, font=font, fill=(0, 0, 0),
                          anchor="right", align="right", spacing=list_font_size / 15.0)

                f.write(page)

        f.counter = counter
