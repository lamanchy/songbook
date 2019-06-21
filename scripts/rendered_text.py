import re

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
    list_font_size = title_font_size * 20 // 40
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

        hyphen_size = draw.textsize("-", font)[0]
        space_size = draw.textsize(" ", font)[0]

        line_height = draw.textsize("A", font)[1] + spacing
        x = y = 0
        disable_x_reset = False

        if len(lines) > 0 and lines[0].text.startswith("[capo"):
            capo_font = get_font(self.list_font_size)
            width, height = draw.textsize(lines[0].text, capo_font)
            draw.text(
                (
                    self.text_pos[0] + self.max_width - width - mm_to_px(self.delta) // 2,
                    self.text_pos[1] - 1.9 * height
                ),
                lines[0].text,
                font=capo_font, fill=(0, 0, 0))
            lines.pop(0)
            if len(lines) > 0 and lines[0].is_empty():
                lines.pop(0)

        for i, line in enumerate(lines):
            if line.is_empty(): disable_x_reset = False
            if not disable_x_reset: x = 0

            previous_line = None if i - 1 < 0 else lines[i - 1]
            next_line = None if i + 1 == len(lines) else lines[i + 1]
            next_next_line = None if i + 2 >= len(lines) else lines[i + 2]

            if line.is_chord_line() and previous_line is not None and previous_line.is_text_line() and not line.is_tag_line():
                y += spacing / 2

            if line.is_text_line() and previous_line is not None and previous_line.is_chord_line():
                continue

            if re.match(r"\[\d+x]", line.text) or (
                    line.is_tag_line() and next_line is not None and next_line.is_chord_line() and not next_line.is_tag_line() and next_next_line is not None and next_next_line.is_chord_line()
            ):
                tag = line.text.split(" ")[0] + " "
                extra = line_height if not next_line.is_text_line() and next_next_line is not None and next_next_line.is_text_line() else 0
                draw.text((self.text_pos[0] + x, self.text_pos[1] + y + extra), tag, font=font, fill=(0, 0, 0))
                line.text = line.text[len(tag):]
                x = draw.textsize(tag, font)[0]
                disable_x_reset = True
                y -= line_height

            if line.is_chord_line() and next_line is not None and next_line.is_text_line():
                parts = line.get_parts_with_indexes()
                text_parts = next_line.get_parts_by_indexes([i for i, _ in parts], False)
                chord_parts = line.get_parts_by_indexes([i for i, _ in parts], False)
                if parts[0][0] != 0:
                    chord_parts.insert(0, (0, ""))
                    text_parts.insert(0, (0, next_line.text[:parts[0][0]]))

                extra = -space_size if next_line.text.startswith(" ") else 0
                for i in range(len(chord_parts)):
                    chord = chord_parts[i][1].replace("_", " ").replace("—", "-")
                    while chord.endswith("  "): chord = chord[:-1]
                    text = text_parts[i][1].replace("_", " ").replace("—", "-")
                    while text != text.replace("--", "-"):
                        text = text.replace("--", "-")

                    chord_size = draw.textsize(chord, font)[0]
                    text_size = draw.textsize(text, font)[0]
                    dx = max(chord_size, text_size)
                    if i < len(chord_parts) - 1 and \
                            len(text) > 0 and \
                            text[-1] not in " _," and \
                            len(text_parts[i + 1][1]) > 0 and \
                            text_parts[i + 1][1][0] not in " _,":
                        while text_size + hyphen_size <= dx:
                            text_size += hyphen_size
                            text += "-"

                        if text_parts[i + 1][1][0] == "-":
                            text_parts[i + 1] = (text_parts[i + 1][0], " " + text_parts[i + 1][1][1:])
                            if text_size + hyphen_size <= dx + draw.textsize(" ", font)[0]:
                                text += "-"

                    draw.text((self.text_pos[0] + x + extra, self.text_pos[1] + y), chord, font=font, fill=(0, 0, 0))
                    draw.text((self.text_pos[0] + x + extra, self.text_pos[1] + y + line_height), text, font=font,
                              fill=(0, 0, 0))

                    extra += dx

                y += line_height

            else:
                line.text = line.text.replace("_", " ").replace("—", "-").rstrip()
                draw.text((self.text_pos[0] + x, self.text_pos[1] + y), line.text, font=font, fill=(0, 0, 0))

            y += line_height
