from PIL import ImageDraw

from pil_quality_pdf.fonts import get_max_font_size, get_font
from pil_quality_pdf.rendering import mm_to_px
from scripts.rendered_text import RenderedText
from scripts.song import Song


class RenderedSong(object):
    max_width = RenderedText.max_width
    max_height = RenderedText.max_height
    title_font_size = RenderedText.title_font_size
    author_font_size = RenderedText.author_font_size
    delta = RenderedText.delta

    def __init__(self, song: Song):
        self.song = song

        self.font_size, _, self.texts = self.get_best_configuration()

    def get_best_configuration(self):
        parts = self.song.text.text.split("\n\n")
        variations = []
        for split_index in range(0, len(parts)):
            split_index += 1
            first, second = "\n\n".join(parts[:split_index]), "\n\n".join(parts[split_index:])

            first = RenderedText(first)
            second = RenderedText(second)
            font_size = min(first.font_size, second.font_size)
            first = RenderedText(first.text, font_size + 1)
            second = RenderedText(second.text, font_size + 1)

            if second.text.count("\n") == 0:
                variations.append((font_size, split_index, [first]))
                continue

            if len(second.text.split("\n")) <= 4:
                continue

            variations.append((font_size, split_index, [first, second]))

        variations.sort(reverse=True)

        return variations[0]

    def get_pages(self):
        pages = [text.get_page() for text in self.texts]
        draw = ImageDraw.Draw(pages[0])
        title_size = get_max_font_size(draw, self.song.title, self.max_width, None, self.title_font_size)[0]
        draw.text(mm_to_px(self.delta, 1 * self.delta), self.song.title, font=get_font(title_size), fill=(0, 0, 0))
        author_size = get_max_font_size(draw, self.song.author, self.max_width, None, self.author_font_size)[0]
        draw.text(mm_to_px(self.delta, 2 * self.delta), self.song.author, font=get_font(author_size), fill=(0, 0, 0))
        return pages

    def get_problems(self):
        return ", ".join([", ".join(page.problems) for page in self.texts])