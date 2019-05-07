import re
from typing import List


class SongText(object):
    def __init__(self, text):
        self.text = text
        self.parsed_text()

    def parsed_text(self):
        # rstrp all lines
        lines = self.text.split("\n")
        lines = [line.rstrip() for line in lines]

        # max two empty lines
        lines = "\n".join(lines)
        while lines != lines.replace(3 * "\n", 2 * "\n"):
            lines = lines.replace(3 * "\n", 2 * "\n")

        return lines
