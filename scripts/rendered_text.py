from PIL import ImageDraw, Image

from pil_quality_pdf.fonts import get_max_font_size, get_font
from pil_quality_pdf.rendering import mm_to_px
from scripts.song_text import SongText


class RenderedText(object):
    page_size = (210, 297)
    delta = 15
    draw = ImageDraw.Draw(Image.new("RGB", mm_to_px(page_size), (255, 255, 255)))
    title_font_size = get_max_font_size(draw, "A", None, mm_to_px(delta * .7), 100)[0]
    author_font_size = title_font_size * 30 // 40
    text_font_size = title_font_size * 25 // 40
    max_width = mm_to_px(page_size[0] - 2 * delta)
    max_height = mm_to_px(page_size[1] - 5 * delta)
    text_pos = mm_to_px(delta, 3 * delta)

    def __init__(self, text, font_size=text_font_size):
        self.text = SongText(None, text)
        self.font_size, self.problems = get_max_font_size(
            self.draw, self.text.text, self.max_width, self.max_height, font_size)

    def get_page(self):
        page = Image.new("RGB", mm_to_px(self.page_size), (255, 255, 255))
        draw = ImageDraw.Draw(page)
        self.draw_lines(draw)
        return page

    def draw_lines(self, draw):
        lines = self.text.get_lines()

        font = get_font(self.font_size)
        spacing = mm_to_px(self.font_size / 10.)

        line_height = draw.textsize("A", font)[1] + spacing
        y = 0
        for i, line in enumerate(lines):
            x = 0
            previous_line = None if i - 1 < 0 else lines[i - 1]
            next_line = None if i + 1 == len(lines) else lines[i + 1]

            # if next_line is not None and line.is_tag_line() and not next_line.is_empty() and line.text.count(" ") == 0:
            #     to_print = line.text[1:-1]
            # if to_print == "s": to_print = "S"
            # if to_print == "c": to_print = "R"
            # if to_print == "v": to_print = "V"
            # if to_print == "b": to_print = "B"
            # if line.text[-2].isdigit():
            #     to_print += line.text[-2]

            # to_print += ": "
            # width = draw.textsize(to_print, font)[0]
            # draw.text((self.text_pos[0] - width, self.text_pos[1] + y), to_print, font=font, fill=(0, 0, 0))
            # continue

            if line.is_chord_line() and previous_line is not None and previous_line.is_text_line():
                y += spacing / 2

            if line.is_text_line() and previous_line is not None and previous_line.is_chord_line():
                continue

            if line.is_chord_line() and next_line is not None and next_line.is_text_line():
                parts = line.get_parts_with_indexes()
                text_parts = next_line.get_parts_by_indexes([i for i, _ in parts], False)
                chord_parts = line.get_parts_by_indexes([i for i, _ in parts], False)
                if parts[0][0] != 0:
                    chord_parts.insert(0, (0, ""))
                    text_parts.insert(0, (0, next_line.text[:parts[0][0]]))

                for i in range(len(chord_parts)):
                    chord = chord_parts[i][1]
                    text = text_parts[i][1].replace("_", " ")
                    while text != text.replace("--", "-"):
                        text = text.replace("--", "-")

                    draw.text((self.text_pos[0] + x, self.text_pos[1] + y), chord, font=font, fill=(0, 0, 0))
                    draw.text((self.text_pos[0] + x, self.text_pos[1] + y + line_height), text, font=font,
                              fill=(0, 0, 0))

                    x += max(
                        draw.textsize(chord, font)[0],
                        draw.textsize(text, font)[0]
                    )

                y += line_height

            else:
                draw.text((self.text_pos[0], self.text_pos[1] + y), line.text, font=font, fill=(0, 0, 0))

            y += line_height
