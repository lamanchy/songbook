import logging
import sys

from PIL import ImageDraw, Image

from pil_quality_pdf.fonts import get_font, get_max_font_size
from pil_quality_pdf.local_quality_constants import ANTIALIASING
from pil_quality_pdf.quality_constants import RESOLUTION_DPI
from pil_quality_pdf.rendering import PdfWriter, mm_to_px
from scripts.rendered_song import RenderedSong
from scripts.rendered_text import RenderedText
from scripts.song import Song

if __name__ == "__main__":
    no_capo = len(sys.argv) > 1 and sys.argv[1] == "no_capo"

    for category in ["mine"]:
        songs = Song.load_songs()
        songs = [song for song in songs if song.categories[0] == category]
        for song in songs:
            song.categories = song.categories[1:]
        c = "en" if category == "english" else "cz"

        with PdfWriter("songbook_" + c + ("_for_piano" if no_capo else "") + (
                "_print" if RESOLUTION_DPI == 300 else "") + "_A4") as f, \
                PdfWriter("songbook_" + c + ("_for_piano" if no_capo else "") + (
                        "_print" if RESOLUTION_DPI == 300 else "") + "_A5") as f2, \
                PdfWriter("songbook_" + c + ("_for_piano" if no_capo else "") + (
                "_print" if RESOLUTION_DPI == 300 else "") + "_A6") as f3:
            def write_img(img):
                f.write(img)
                f2.write(img.resize(mm_to_px((297 / 2, 210)), resample=ANTIALIASING))
                f3.write(img.resize(mm_to_px((210 / 2, 297 / 2)), resample=ANTIALIASING))


            # songs = songs[:2]
            # songs = [song for song in songs if song.title.startswith("A")]
            # songs.sort(key=lambda song: len(song.text.text.split("\n")))
            draw = ImageDraw.Draw(Image.new("RGB", (0, 0), (255, 255, 255)))

            num_of_pages = 1
            while True:
                i = (len(songs) + 1) // num_of_pages
                list_font_size = get_max_font_size(
                    draw, "\n".join(["A" for a in range(i // 2)]), None,
                    mm_to_px(RenderedText.page_size[1] - RenderedText.delta * 5), RenderedText.text_font_size
                )[0]
                if list_font_size >= RenderedText.list_font_size:
                    break
                num_of_pages += 1

            f.counter = num_of_pages * 2 + 1
            f2.counter = num_of_pages * 2 + 1
            f3.counter = num_of_pages * 2 + 1

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
                        font = get_font(RenderedText.list_font_size)
                        size = draw.textsize(text, font)
                        draw.text((page.size[0] - mm_to_px(RenderedText.delta) - size[0],
                                   page.size[1] - mm_to_px(RenderedText.delta) - size[1]),
                                  text, font=font, fill=(0, 0, 0))
                    write_img(page)


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
            f2.counter = 0
            f3.counter = 0

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

            text = [category.lower()]
            text += ["no_capo" if no_capo else "capo"]
            if RESOLUTION_DPI != 300:
                text += ["web"]
            text = "[" + ",".join(text) + "]"
            font = get_font(RenderedText.author_font_size)
            size = draw.textsize(text, font)
            draw.text((mm_to_px(RenderedText.delta * 1.5),
                       page.size[1] - mm_to_px(RenderedText.delta * 1.5) - size[1]),
                      text, font=font, fill=(0, 0, 0))

            write_img(page)

            written_songs.sort(key=lambda w: w[0].get_sort_key())
            written_songs = list(map(lambda w: (" - ".join(w[0].categories), w[0].title, str(w[1])), written_songs))
            category = None
            list_songs = []

            for written in written_songs:
                if written[0] != category:
                    category = written[0]
                    if len(list_songs) > 0:
                        list_songs.append(("", ""))
                    list_songs.append((category, ""))
                list_songs.append(("   " + written[1], written[2]))

            font = get_font(list_font_size)
            for page_i in range(num_of_pages):
                tw = list_songs[
                     page_i * len(list_songs) // num_of_pages:(page_i + 1) * len(list_songs) // num_of_pages]
                o = (len(tw) + 1) // 2
                for ttw in [tw[:o], tw[o:]]:
                    page = Image.new("RGB", mm_to_px(RenderedText.page_size), (255, 255, 255))
                    draw = ImageDraw.Draw(page)

                    text = "\n".join([x[0] for x in ttw])
                    draw.text((RenderedText.text_pos[0] * 3, RenderedText.text_pos[1]), text,
                              font=font, fill=(0, 0, 0),
                              spacing=list_font_size / 5.0 * ANTIALIASING * ANTIALIASING)

                    pages = [x[1] for x in ttw]
                    size = max(map(lambda i: draw.textsize(i, font)[0], pages), default=0)
                    text = "\n".join(pages)
                    draw.text((RenderedText.text_pos[0] * 3 - size, RenderedText.text_pos[1]),
                              text, font=font, fill=(0, 0, 0),
                              anchor="ra", align="right", spacing=list_font_size / 5.0 * ANTIALIASING * ANTIALIASING)

                    write_img(page)

            f.counter = counter
            f2.counter = counter
            f3.counter = counter
