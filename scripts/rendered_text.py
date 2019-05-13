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
    note_font_size = title_font_size * 15 // 40
    max_width = mm_to_px(page_size[0] - 2 * delta)
    max_height = mm_to_px(page_size[1] - 4.5 * delta)
    text_pos = mm_to_px(delta, 3 * delta)

    def __init__(self, text, min_font_size, font_size=text_font_size):
        self.text = SongText(None, text)
        self.font_size, self.problems = get_max_font_size(
            self.draw, self.text.get_text_to_size(), self.max_width, self.max_height, font_size,
            min_font_size=min_font_size)

    def get_page(self):
        page = Image.new("RGB", mm_to_px(self.page_size), (255, 255, 255))
        draw = ImageDraw.Draw(page)
        self.draw_lines(draw)
        return page

    def draw_lines(self, draw):
        lines = self.text.get_lines()

        font = get_font(self.font_size)
        spacing = mm_to_px(self.font_size / 15.)

        line_height = draw.textsize("A", font)[1] + spacing
        y = 0
        disable_x_reset = False

        if len(lines) > 0 and lines[0].text.startswith("[capo"):
            width = draw.textsize(lines[0].text, font)[0]
            draw.text((self.text_pos[0] + self.max_width - 2 * self.delta - width, self.text_pos[1]), lines[0].text,
                      font=font, fill=(0, 0, 0))
            lines.pop(0)
            if len(lines) > 0 and lines[0].is_empty():
                lines.pop(0)

        for i, line in enumerate(lines):
            if line.is_empty(): disable_x_reset = False
            if not disable_x_reset: x = 0

            previous_line = None if i - 1 < 0 else lines[i - 1]
            next_line = None if i + 1 == len(lines) else lines[i + 1]

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
                draw.text((self.text_pos[0] + x, self.text_pos[1] + y), line.text, font=font, fill=(0, 0, 0))

            if not line.is_tag_line() and line.is_tag(line.text.split(" ")[0]):
                tag = line.text.split(" ")[0] + " "
                x = draw.textsize(tag, font)[0]
                disable_x_reset = True

            y += line_height
