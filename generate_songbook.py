import logging

from PIL import ImageDraw, Image

from pil_quality_pdf.fonts import get_font, get_max_font_size
from pil_quality_pdf.quality_constants import RESOLUTION_DPI, ANTIALIASING
from pil_quality_pdf.rendering import PdfWriter, mm_to_px
from scripts.rendered_song import RenderedSong
from scripts.rendered_text import RenderedText
from scripts.song import Song


class SongbookGenerator:
    def __init__(self, capo_setting: str, category):
        self.keep_order = category == 'mine'
        self.capo_setting = capo_setting
        self.category = category
        self.pdf_writer = None

    def generate(self):
        songs = self.get_songs()
        list_font_size, num_of_pages = self.get_number_of_pages(songs)

        with PdfWriter(self.get_songbook_name()) as self.pdf_writer:
            self.pdf_writer.counter = num_of_pages * 2 + 1

            worst, written_songs = self.write_songs(songs)

            counter = self.pdf_writer.counter
            self.pdf_writer.counter = 0

            self.write_first_page()
            self.write_list(list_font_size, num_of_pages, written_songs)
            self.print_worst(worst)

            self.pdf_writer.counter = counter

    def write_list(self, list_font_size, num_of_pages, written_songs):
        list_songs = self.get_songs_list(written_songs)

        font = get_font(list_font_size)
        for page_i in range(num_of_pages):
            tw = list_songs[page_i * len(list_songs) // num_of_pages:(page_i + 1) * len(list_songs) // num_of_pages]
            o = (len(tw) + 1) // 2
            for ttw in [tw[:o], tw[o:]]:
                page = Image.new("RGB", mm_to_px(RenderedText.page_size), (255, 255, 255))
                draw = ImageDraw.Draw(page)

                text = "\n".join([x[0] for x in ttw])
                draw.text((RenderedText.text_pos[0] * 3, RenderedText.text_pos[1]), text,
                          font=font, fill=(0, 0, 0),
                          spacing=list_font_size / 5.0 * ANTIALIASING * ANTIALIASING)

                pages = [x[1] for x in ttw]
                size = max(map(lambda i: draw.textbbox((0, 0), i, font)[2], pages), default=0)
                text = "\n".join(pages)
                draw.text((RenderedText.text_pos[0] * 3 - size, RenderedText.text_pos[1]),
                          text, font=font, fill=(0, 0, 0),
                          anchor="ra", align="right", spacing=list_font_size / 5.0 * ANTIALIASING * ANTIALIASING)

                self.write_page(page)

    def get_songs_list(self, written_songs):
        written_songs.sort(key=lambda w: w[0].get_sort_key())
        written_songs = list(map(lambda w: (" - ".join(w[0].categories), w[0].nice_title, str(w[1])), written_songs))
        category = None
        list_songs = []
        for written in written_songs:
            if written[0] != category:
                category = written[0]
                if len(list_songs) > 0:
                    list_songs.append(("", ""))
                list_songs.append(("   " + category.upper(), ""))
            list_songs.append(("   " + written[1], written[2]))
        return list_songs

    def write_first_page(self):
        page = Image.new("RGB", mm_to_px(RenderedText.page_size), (255, 255, 255))
        draw = ImageDraw.Draw(page)
        text = "Blonďákův"
        font = get_font(RenderedText.title_font_size * 1.5)
        size = draw.textbbox((0, 0), text, font)
        draw.text((page.size[0] // 2 - size[2] // 2, page.size[1] // 2 - size[3] * 1.1),
                  text, font=font, fill=(0, 0, 0))
        text = "zpěvník"
        size = draw.textbbox((0, 0), text, font)
        draw.text((page.size[0] // 2 - size[2] // 2, page.size[1] // 2),
                  text, font=font, fill=(0, 0, 0))
        text = [self.category.lower()]
        text += [self.capo_setting]
        if RESOLUTION_DPI != 300:
            text += ["web"]
        text = "[" + ",".join(text) + "]"
        font = get_font(RenderedText.author_font_size)
        size = draw.textbbox((0, 0), text, font)
        draw.text((mm_to_px(RenderedText.delta * 1.5),
                   page.size[1] - mm_to_px(RenderedText.delta * 1.5) - size[3]),
                  text, font=font, fill=(0, 0, 0))
        self.write_page(page)

    def print_worst(self, worst):
        print()
        if len(worst) > 0:
            logging.warning(f"Smallest songs:")
            for font_size, title, problem in reversed(list(sorted(worst, key=lambda t: t[0]))[:100]):
                logging.warning(
                    f"Font size: {font_size}/{RenderedText.text_font_size}, problem: {problem}, song: {title}")

    def write_songs(self, songs):
        single_song_waiting_for_another = None
        worst = []
        written_songs = []
        current_page = [0]
        for i, song in enumerate(songs):
            print(f'{i}/{len(songs)}, {song.title}')
            rendered = RenderedSong(song, self.capo_setting)

            if rendered.has_problems():
                worst.append((rendered.font_size, song.title, rendered.get_problems()))

            if len(rendered.texts) == 2:
                if self.keep_order and single_song_waiting_for_another:
                    self.write_song(single_song_waiting_for_another, current_page, written_songs, force_two=True)
                    single_song_waiting_for_another = None

                self.write_song(rendered, current_page, written_songs)

            else:
                if single_song_waiting_for_another is None:
                    single_song_waiting_for_another = rendered
                else:
                    self.write_song(single_song_waiting_for_another, current_page, written_songs)
                    self.write_song(rendered, current_page, written_songs)
                    single_song_waiting_for_another = None

        if single_song_waiting_for_another is not None:
            self.write_song(single_song_waiting_for_another, current_page, written_songs)

        return worst, written_songs

    def get_number_of_pages(self, songs):
        draw = ImageDraw.Draw(Image.new("RGB", (0, 0), (255, 255, 255)))
        num_of_pages = 1
        while True:
            i = (len(songs) + 1) // num_of_pages
            list_font_size = get_max_font_size(
                draw, "\n".join(["A" for a in range(i // 2)]), None,
                mm_to_px(RenderedText.page_size[1] - RenderedText.delta * 6), RenderedText.text_font_size
            )[0]
            if list_font_size >= RenderedText.list_font_size:
                break
            num_of_pages += 1

        return list_font_size, num_of_pages

    def get_songbook_name(self):
        songbook_name = "en" if category == "english" else "cz" if category == "czech" else category
        songbook_name += f"_for_{self.capo_setting}"
        return f"songbook_{songbook_name}"

    def get_songs(self):
        songs = Song.load_songs()
        songs = [song for song in songs if song.categories[0] == self.category]
        for song in songs:
            song.categories = song.categories[1:]

        # songs = songs[:2]
        # songs = [song for song in songs if song.title.startswith("A")]
        # songs.sort(key=lambda song: len(song.text.text.split("\n")))
        return songs

    def write_page(self, img):
        self.pdf_writer.write(img)

    def write_song(self, rendered, current_page, written_songs, force_two=False):
        song = rendered.song
        written_songs.append((song, current_page[0] + 1))

        pages = rendered.get_pages()
        if force_two and len(pages) == 1:
            pages.append(Image.new(mode=pages[0].mode, size=pages[0].size, color=(255, 255, 255)))

        for page in pages:
            current_page[0] += 1
            if current_page[0] % 2 == 0:
                self.write_page_number(current_page, page)
            self.write_page(page)

    def write_page_number(self, current_page, page):
        draw = ImageDraw.Draw(page)
        text = f"{current_page[0]}."
        font = get_font(RenderedText.list_font_size)
        size = draw.textbbox((0, 0), text, font)
        draw.text((page.size[0] - mm_to_px(RenderedText.delta) - size[2],
                   page.size[1] - mm_to_px(RenderedText.delta) - size[3]),
                  text, font=font, fill=(0, 0, 0))


if __name__ == "__main__":
    _capo_settings = [
        'guitar',
        # 'piano',
        # 'ukulele',
    ]
    _categories = [
        # "czech",
        # "english",
        # "mine",
        # "carols",
        "poems",
    ]
    for capo_setting in _capo_settings:
        for category in _categories:
            generator = SongbookGenerator(capo_setting, category)
            generator.generate()
