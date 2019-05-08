import re

from scripts.chord import Chord


class Line(object):
    def __init__(self, text: str):
        self.text = text

    def is_empty(self):
        return len(self.text.strip()) == 0

    def is_chord_line(self):
        if self.is_empty(): return False
        not_empty_parts = [part for part in self.text.split(" ") if len(part) > 0]
        return all([self.is_chord(part) or self.is_extra(part) for part in not_empty_parts])

    def is_text_line(self):
        return not self.is_empty() and not self.is_chord_line()

    def justifies_next_spaced(self):
        return self.is_chord_line() and self.text[0] != " "

    @staticmethod
    def is_chord(chars):
        return Chord.is_chord(chars)

    @staticmethod
    def is_extra(chars):
        return re.match(r"\d+x", chars)

    def rstrip(self):
        self.text = self.text.rstrip()

    def lstrip(self):
        self.text = self.text.lstrip()

    def replace(self, old, new):
        self.text = self.replace_all(self.text, old, new)

    @staticmethod
    def replace_all(text, old, new):
        while text != text.replace(old, new):
            text = text.replace(old, new)
        return text

    def remove_funny_ending(self):
        while self.text[-1] in ",.-!?":
            self.text = self.text[:-1]
            self.rstrip()

    def fix_interpunction(self):
        for c in ".!?":
            self.replace(c, ",")
        self.replace(",,", ",")
        self.text = re.sub(r"^,", "", self.text)
        self.text = re.sub(r" ,", ",", self.text)
        self.text = re.sub(r",(?![\s\w])", "", self.text)
        self.text = re.sub(r",(?=\S)", ", ", self.text)

    def upper_first_letter(self):
        for i, c in enumerate(self.text):
            if c != ' ':
                self.text = self.text[:i] + self.text[i].upper() + self.text[i + 1:]
                break

    def format_chord_naming(self):
        tuples = self.get_chords_with_indexes()
        tuples = [((i, Chord(chord).chars) if not self.is_extra(chord) else (i, chord)) for i, chord in tuples]

        text = ""

        for i, chord in tuples:
            while len(text) < i:
                text += " "

            text += chord + " "

        self.text = text.rstrip()



    def format_chord_position(self, next_line):
        start_index = 0

        if next_line is not None and not next_line.is_empty():
            start_index = len(next_line.text) - 1

            while True:
                if start_index >= len(self.text):
                    return

                if self.text[start_index] == " ":
                    break

                start_index += 1

        to_squeeze = self.text[start_index:]

        to_squeeze = Line.replace_all(to_squeeze, "  ", " ")
        to_squeeze = to_squeeze.strip()

        if start_index != 0:
            to_squeeze = " " + to_squeeze
            start_index += 1

        self.text = self.text[:start_index] + to_squeeze

    def get_chords_with_indexes(self):
        chord = ""
        chord_index = 0
        chords = []
        for i, c in enumerate(self.text + " "):
            if c != " ":
                if chord == "":
                    chord_index = i
                chord += c
            else:
                if chord != "":
                    chords.append((chord_index, chord))
                chord = ""

        return chords
