import re

from scripts.chord import Chord


class Line(object):
    def __init__(self, text: str):
        self.text = text

    def is_empty(self):
        return len(self.text.strip()) == 0

    def is_tag_line(self):
        return all([self.is_tag(c) for c in self.text.split(" ")])

    def is_chord_line(self):
        if self.is_empty(): return False
        not_empty_parts = [part for part in self.text.split(" ") if len(part) > 0]
        for part in not_empty_parts:
            if not self.is_chord(part) and not self.is_extra(part):
                return False
        return True

    def is_text_line(self):
        return not self.is_empty() and not self.is_chord_line() and not self.is_tag_line()

    def justifies_next_spaced(self):
        return self.is_chord_line() and self.text[0] != " "

    @staticmethod
    def is_chord(chars):
        return Chord.is_chord(chars)

    @staticmethod
    def is_extra(chars):
        return re.match(r"\[?\d+]?", chars) or chars == "|"

    @staticmethod
    def is_tag(chars):
        return re.match(r"\[\w+( \d)?]", chars)

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
        while len(self.text) > 0 and self.text[-1] in ",.-!?:_":
            self.text = self.text[:-1]
            self.rstrip()

    def remove_funny_beginning(self):
        for start in ["R: "] + [f"{i + 1}. " for i in range(10)]:
            if self.text.startswith(start):
                self.text = self.text[len(start):]

    def fix_interpunction(self):
        self.replace("[:", "")
        self.replace(":]", "")
        self.replace("_ ", " _")
        for c in ".!?;\"…–":
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

    def format_chord_naming(self, next_line, fn):
        if next_line is None: next_line = Line("")
        tuples = self.get_parts_with_indexes()
        next_tuples = next_line.get_parts_by_indexes([i for i, _ in tuples])
        for i, (index, chord) in enumerate(tuples):
            if self.is_chord(chord):
                new_chord = fn(chord)
                diff = len(new_chord) - len(chord)
                if diff > 0:
                    for o, (ondex, c) in list(enumerate(tuples))[i + 1:]:
                        tuples[o] = ondex + diff, c
                    for o, (ondex, c) in list(enumerate(next_tuples))[i + 1:]:
                        next_tuples[o] = ondex + diff, c

                tuples[i] = index, new_chord + " "

        self.put_parts_with_indexes(tuples)
        next_line.put_parts_with_indexes(next_tuples)

    def put_parts_with_indexes(self, tuples):
        text = self.text[:tuples[0][0]]
        is_chord_line = self.is_chord_line()
        for i, part in tuples:
            if self.is_empty() or len(text) == 0 or is_chord_line:
                to_add = " "
            elif text[-1] in " _":
                to_add = "_"
            else:
                to_add = "-"

            while len(text) < i:
                text += to_add

            text += part
        self.text = text.rstrip()

    def transpose(self):
        tuples = self.get_parts_with_indexes()
        for index, (i, chord) in enumerate(tuples):
            if self.is_chord(chord):
                chord = Chord(chord)
                chord.transpose()
                tuples[index] = i, str(chord)

        self.put_parts_with_indexes(tuples)

    def format_chord_position(self, next_line):
        start_index = 0

        if next_line is not None and next_line.is_text_line():
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
            start_index += 1

        self.text = self.text[:start_index] + to_squeeze

    def get_parts_with_indexes(self):
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

    def remove_extra_padding(self, prev_line=None):
        if prev_line is None: prev_line = Line("")

        for i in range(len(self.text)):
            if i >= len(self.text) - 1: break
            while i >= len(prev_line.text) - 1:
                prev_line.text += " "

            if prev_line.text[i] != " " or prev_line.text[i + 1] != " ": continue
            if self.text[i + 1] not in " _-": continue
            if self.text[i + 1] in " _" and self.text[i] not in " _": continue

            self.text = self.text[:i + 1] + self.text[i + 1 + 1:]
            prev_line.text = prev_line.text[:i + 1] + prev_line.text[i + 1 + 1:]

        prev_line.text = prev_line.text.rstrip()

    def get_parts_by_indexes(self, indexes, move_left=True):
        res = []
        for i, index in enumerate(indexes):
            end = len(self.text) if i + 1 == len(indexes) else indexes[i + 1]
            res.append((index, self.text[index:end]))

        if move_left:
            for i in range(len(res[:-1])):
                index, part = res[i]
                while part.count(" ") > 0 and part[-1] != " ":
                    res[i + 1] = res[i + 1][0] - 1, part[-1] + res[i + 1][1]
                    part = part[:-1]
                res[i] = index, part

        return res

    def __repr__(self):
        return self.text
