import re


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
        return chars[0] in "CDEFGABH"

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
        self.text = self.text[0].upper() + self.text[1:]
