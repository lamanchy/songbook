from scripts.line import Line


class SongText(object):
    def __init__(self, text):
        self.text = text

    def parsed_text(self):
        lines = [Line(line) for line in self.text.split("\n")]

        self.clear_lines(lines)

        for i, line in enumerate(lines):
            line.rstrip()

            if line.is_text_line():
                line.replace("  ", " ")
                line.remove_funny_ending()
                line.fix_interpunction()
                if i > 0 and not lines[i - 1].justifies_next_spaced():
                    line.lstrip()

                line.upper_first_letter()

            # if line.is_chord_line() and i + 1 != len(lines):
            #     if lines[i+1].is_chord_line():

            lines[i] = line

        lines = "\n".join([line.text for line in lines])

        return lines

    def clear_lines(self, lines):
        while lines[0].is_empty():
            lines.pop(0)

        while lines[-1].is_empty():
            lines.pop(-1)

        for i, line in reversed(list(enumerate(lines))):
            if i >= 1:
                prev_line = lines[i - 1]
                if line.is_chord_line() and prev_line.is_chord_line():
                    prev_line.text += " " + line.text
                    lines.pop(i)

                if line.is_empty() and prev_line.is_empty():
                    lines.pop(i)
