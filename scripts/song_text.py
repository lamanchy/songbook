from scripts.line import Line


class SongText(object):
    def __init__(self, path):
        self.path = path
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
        with open(self.path, "w", encoding="UTF-8") as f:
            f.write(self.text)

    def parsed_text(self):
        lines = self.get_lines()

        for _ in range(3):  # for sure ;)
            self.clear_lines(lines)
            self.basic_formatting(lines)

        self.format_chords(lines)

        return self.join_lines(lines)

    def transpose(self):
        lines = self.get_lines()

        for line in lines:
            if line.is_chord_line():
                line.transpose()

        self.text = self.join_lines(lines)
        self.save()

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
        while lines[0].is_empty():
            lines.pop(0)

        while lines[-1].is_empty():
            lines.pop(-1)

        for i, line in list(reversed(list(enumerate(lines))))[:-1]:
            prev_line = lines[i - 1]

            if line.is_empty() and prev_line.is_empty():
                lines.pop(i)

    @staticmethod
    def format_chords(lines):
        for i, line in enumerate(lines):
            next_line = None if i + 1 == len(lines) else lines[i + 1]

            if line.is_chord_line():
                line.format_chord_naming()
                line.format_chord_position(next_line)

    @staticmethod
    def join_lines(lines):
        return "\n".join([line.text for line in lines])
