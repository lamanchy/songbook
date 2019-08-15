import re

from scripts.chord import Chord
from scripts.line import Line


class SongText(object):
    def __init__(self, path=None, text=None):
        self.text = text
        self.path = path
        self.transposed_by = 0
        if path is not None:
            with open(path, "r", encoding="UTF-8") as f:
                self.text = f.read()

        self.parse()

    def get_lines(self):
        return [Line(line) for line in self.text.split("\n")]

    def parse(self):
        while self.text != self.parsed_text():
            self.text = self.parsed_text()
            self.save()

    def save(self):
        if self.path is not None:
            with open(self.path, "w", encoding="UTF-8") as f:
                f.write(self.text)
        self.parse()

    def parsed_text(self):
        lines = self.get_lines()

        for _ in range(3):  # for sure ;)
            self.clear_lines(lines)
            self.basic_formatting(lines)

        self.format_chords(lines)
        self.basic_formatting(lines)

        return self.join_lines(lines)

    def transpose(self, steps=1):
        lines = self.get_lines()
        self.transposed_by += steps

        for i, line in enumerate(lines):
            next_line = None if i + 1 == len(lines) else lines[i + 1]

            fn = lambda chord: str(Chord(chord).transpose(steps))
            if line.is_chord_line():
                line.format_chord_naming(next_line, fn)
            else:
                last = line.text.split(" ")[-1]
                if last.startswith("_"):
                    last = last.replace("_", "").strip()
                    if Chord.is_chord(last):
                        i = line.text.rindex("_")
                        line.text = line.text[:i + 1] + fn(last)

        self.text = self.join_lines(lines)

    @staticmethod
    def basic_formatting(lines):
        for i, line in enumerate(lines):
            line.rstrip()

            if line.is_text_line():
                line.replace("  ", " ")
                line.remove_funny_ending()
                line.remove_funny_beginning()
                line.fix_interpunction()
                if i > 0 and not lines[i - 1].justifies_next_spaced():
                    line.lstrip()

                line.upper_first_letter()

    @staticmethod
    def clear_lines(lines):
        while len(lines) > 0 and lines[0].is_empty():
            lines.pop(0)

        while len(lines) > 0 and lines[-1].is_empty():
            lines.pop(-1)

        for i, line in list(reversed(list(enumerate(lines))))[:-1]:
            prev_line = lines[i - 1]

            if line.is_empty() and prev_line.is_empty():
                lines.pop(i)

    @staticmethod
    def format_chords(lines):
        for i, line in enumerate(lines):
            next_line = None if i + 1 == len(lines) else lines[i + 1]
            prev_line = None if i - 1 < 0 else lines[i - 1]

            if line.is_chord_line():
                line.format_chord_naming(next_line, lambda chord: str(Chord(chord)))
                line.format_chord_position(next_line)

            line.remove_funny_ending()

            if prev_line is not None and line.is_text_line() and prev_line.is_chord_line():
                line.remove_extra_padding(prev_line)

            elif line.is_text_line():
                line.remove_extra_padding()

    @staticmethod
    def join_lines(lines):
        return "\n".join([line.text for line in lines])

    @property
    def width(self):
        return max(map(lambda line: len(line.text), self.get_lines()))

    @property
    def height(self):
        return len(self.get_lines())

    def get_text_to_size(self):
        lines = self.get_lines()
        res = []

        if len(lines) > 0 and lines[0].text.startswith("[capo"):
            lines.pop(0)
            if len(lines) > 0 and lines[0].is_empty():
                lines.pop(0)

        for i, line in enumerate(lines):
            next_line = None if i + 1 == len(lines) else lines[i + 1]
            next_next_line = None if i + 2 >= len(lines) else lines[i + 2]

            if line.is_tag_line() \
                    and next_line is not None and next_line.is_chord_line() \
                    and next_next_line is not None and next_next_line.is_chord_line():
                continue

            if re.match(r"\[\d+x]", line.text):
                continue

            Line(line.text.replace("—", "-"))

            res.append(line)

        return self.join_lines(res)

    def process_capo(self, no_capo):
        if self.text.startswith("[capo"):
            steps = int(self.text[5:self.text.index("]")])
            self.transposed_by -= steps
            if no_capo:
                self.text = self.text.split("\n", 1)[1]
                if self.text.startswith("\n"):
                    self.text = self.text.split("\n", 1)[1]

                self.transpose(steps)
