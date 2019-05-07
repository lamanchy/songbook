from scripts.line import Line


class SongText(object):
    def __init__(self, text):
        self.text = text
        self.parsed_text()

    def parsed_text(self):
        lines = [Line(line) for line in self.text.split("\n")]

        for i, line in enumerate(lines):
            line.rstrip()

            if line.is_text_line():
                line.replace("  ", " ")
                line.remove_funny_ending()
                line.fix_interpunction()

            lines[i] = line

        lines = "\n".join([line.text for line in lines])

        lines = Line.replace_all(lines, "\n\n\n", "\n\n")
        return lines

