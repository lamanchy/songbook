class UnknownChordError(BaseException):
    pass


class Chord(object):
    tones = "CDEFGABH"
    tone_lowerers = ["b", "es", "s"]
    tone_raisers = ["#", "is"]
    tone_modifiers = tone_lowerers + tone_raisers

    dictionary = {
        "5,8": "",
        "4,8": "m",
        "5,8,11": "7",
        "4,8,11": "m7",
        "5,8,12": "maj7",
        "4,8,12": "minmaj",
        "5,8,10": "6",
        "4,8,10": "m6",
        "3,5,8,10": "6add9",
        "8": "5",
        "3,5,8,11": "9",
        "3,4,8,11": "m9",
        "3,5,8,12": "maj9",
        "3,5,6,8,11": "11",
        "3,4,6,8,11": "m11",
        "3,5,6,8,10,11": "13",
        "3,4,6,8,10,11": "m13",
        "3,5,8": "add9",
        "5,7,11": "7b5",
        "5,9,11": "aug7",
        "6,8": "sus4",
        "3,8": "sus2",
        "6,8,11": "7sus4",
        "3,8,11": "7sus2",
        "4,7": "dim",
        "4,7,10": "dim7",
        "4,7,11": "m7b5",
        "5,9": "aug",
    }

    def __init__(self, chars: str):
        self.tone = ""
        self.chars = chars
        self.is_tone_lowered = False
        self.is_bass_tone_lowered = False
        self.is_tone_raised = False
        self.is_bass_tone_raised = False
        self.has_3 = True
        self.is_moll = None
        self.has_5 = True
        self.is_5_lowered = False
        self.is_5_raised = False
        self.has_7 = False
        self.is_7_raised = False
        self.has_9 = False
        self.has_11 = False
        self.has_13 = False
        self.bass_tone = None
        try:
            self.parse()
        except ValueError as e:
            raise ValueError(f"error parsing chord {chars}, \n\n{e.args[0]}")
        except UnknownChordError as e:
            raise UnknownChordError(f"{e.args[0]}\n\nCan parse {chars}, but dont know the chord, add it.")

    def get_ints(self):
        res = []
        if self.has_3: res.append(4 if self.is_moll else 5)
        if self.has_5: res.append(7 if self.is_5_lowered else 9 if self.is_5_raised else 8)
        if self.has_7: res.append(12 if self.is_7_raised else 11)
        if self.has_9: res.append(3)
        if self.has_11: res.append(6)
        if self.has_13: res.append(10)
        res.sort()
        res = [str(i) for i in res]
        return ",".join(res)

    def tone_lowered(self):
        self.is_tone_lowered = True

    def tone_raised(self):
        self.is_tone_raised = True

    def bass_tone_lowered(self):
        self.is_bass_tone_lowered = True

    def bass_tone_raised(self):
        self.is_bass_tone_raised = True

    def moll(self):
        self.is_moll = True

    def no3(self):
        self.has_3 = False

    def is7(self):
        self.has_7 = True

    def is9(self):
        self.is7()
        self.add9()

    def is11(self):
        self.is9()
        self.add11()

    def is13(self):
        self.is11()
        self.add13()

    def add9(self):
        self.has_9 = True

    def add11(self):
        self.has_11 = True

    def add13(self):
        self.has_13 = True

    def lowered5(self):
        self.is_5_lowered = True

    def aug(self):
        self.is_5_raised = True

    def maj7(self):
        self.is7()
        self.is_7_raised = True

    def maj9(self):
        self.maj7()
        self.has_9 = True

    def sus2(self):
        self.no3()
        self.add9()

    def sus4(self):
        self.no3()
        self.has_11 = True

    def dim(self):
        self.moll()
        self.lowered5()

    def dim7(self):
        self.dim()
        self.add13()

    def minmaj(self):
        self.maj7()
        self.moll()

    @classmethod
    def is_chord(cls, chars):
        try:
            Chord(chars)
            return True
        except ValueError:
            return False

    def parse(self):
        self.chars = self.chars.replace("6/9", "6add9")

        if "/" in self.chars:
            self.chars, self.bass_tone = self.chars.split("/", 1)
            self.parse_bass_tone()

        if len(self.chars) == 0:
            raise ValueError(f"Chord cannot be empty")

        self.tone, self.chars = self.chars[0], self.chars[1:].lower()

        self.find_mark("sus2", self.sus2)
        self.find_mark(["sus4", "sus"], self.sus4)
        self.find_mark(["add2", "add9"], self.add9)
        self.find_mark(["minmaj", "mm7"], self.minmaj)
        self.find_mark(["dimi7", "dim7", "°7"], self.dim7)
        self.find_mark(["dimi", "dim", "°"], self.dim)
        self.find_mark(["maj7", "△7"], self.maj7)
        self.find_mark(["maj9", "△9"], self.maj9)
        self.find_mark("no3", self.no3)
        self.find_mark(["7+5", "7#5"], lambda: [self.is7(), self.aug()])
        self.find_mark(["7-5", "7b5"], lambda: [self.is7(), self.lowered5()])
        self.find_mark(["aug", "(#5)", "+", "5#"], self.aug)
        self.find_mark("ø", lambda: [self.is7(), self.lowered5(), self.moll()])
        self.find_mark("5", self.no3)
        self.find_mark("6", self.add13)
        self.find_mark("7", self.is7)
        self.find_mark("9", self.is9)
        self.find_mark("11", self.is11)
        self.find_mark("13", self.is13)
        self.find_mark(["maj", "△", "dur"], lambda: None)
        self.find_mark(["min", "mi", "mol", "m"], self.moll)

        self.tone += self.chars
        self.parse_tone()

        self.chars = self.tone

        if self.is_tone_raised:
            self.chars += "#"
        if self.is_tone_lowered:
            self.chars += "b"

        try:
            self.chars += self.dictionary[self.get_ints()]
        except KeyError as e:
            raise UnknownChordError("Can parse this chord, but I don't know it, please add it (or call Ondra)\n\n" +
                                    e.args[0])

        if self.bass_tone is not None:
            self.chars += f"/{self.bass_tone}"
            if self.is_bass_tone_raised:
                self.chars += "#"
            if self.is_bass_tone_lowered:
                self.chars += "b"

    def parse_tone(self):
        self.tone, is_moll, self.is_tone_lowered, self.is_tone_raised = self.parse_tone_level(self.tone)
        if self.is_moll is None:
            self.is_moll = is_moll

    def parse_bass_tone(self):
        self.bass_tone, _, self.is_bass_tone_lowered, self.is_bass_tone_raised = self.parse_tone_level(self.bass_tone)

    def find_mark(self, marks, fn, match_whole=False):
        if not isinstance(marks, list): marks = [marks]
        for mark in marks:
            if mark in self.chars or (not match_whole and mark == self.chars):
                fn()
                self.chars = self.chars.replace(mark, "")

    @classmethod
    def parse_tone_level(cls, tone):
        if len(tone) == 0:
            raise ValueError(f"Tone is empty!")

        tone, rest = tone[0], tone[1:]
        is_moll = tone.islower()
        tone = tone.upper()
        rest = rest.lower()

        if tone not in cls.tones:
            raise ValueError(f"tone {tone} is not valid tone, try one of {cls.tones}")

        is_lowered = rest in cls.tone_lowerers
        is_raised = rest in cls.tone_raisers

        if not is_lowered and not is_raised and len(rest) > 0:
            raise ValueError(f"tone modifier {rest} is invalid, use on of {cls.tone_modifiers}")

        if is_lowered and tone in "CHBF":
            is_lowered = False
            tone = cls.tones[(cls.tones.index(tone) - 1) % len(cls.tones)]

        if is_raised and tone in "EBH":
            is_raised = False
            tone = cls.tones[(cls.tones.index(tone) + 1) % len(cls.tones)]

        return tone, is_moll, is_lowered, is_raised


if __name__ == "__main__":
    test_chords = [
        ["", "maj", "△", "dur"],
        ["m", "min", "mol", "mi"],
        ["7", "dur7"],
        ["m7", "min7", "mol7", "mi7"],
        ["maj7", "△7"],
        ["minmaj", "mM7"],
        ["6"],
        ["m6", "min6", "mol6", "mi6"],
        ["6add9", "6/9"],
        ["5", "no3"],
        ["9"],
        ["m9", "min9", "mi9"],
        ["maj9", "△9"],
        ["11"],
        ["m11", "mi11"],
        ["13"],
        ["m13", "mi13"],
        ["add9", "add2"],
        ["7b5", "7-5"],
        ["aug7", "7+5", "7#5"],
        ["sus4"],
        ["sus2"],
        ["dim", "°", "dimi"],
        ["dim7", "°7", "dimi7"],
        ["m7b5", "ø"],
        ["aug", "+", "(#5)", "5#"],
        ["/G"],
        ["/Gb"],
        ["/G#"],
        ["/F", "/E#"],
        ["/E", "/Fb"],
    ]

    for chords in test_chords:
        for chord in chords:
            for tone in Chord.tones:
                for type in [("normal", [""]), ("lowered", Chord.tone_lowerers), ("raised", Chord.tone_raisers)]:
                    if type[0] == "lowered" and tone in "CHBF":
                        continue

                    if type[0] == "raised" and tone in "EBH":
                        continue

                    for typer in type[1]:
                        c = tone + typer + chord

                        if Chord(c).chars != tone + type[1][0] + chords[0]:
                            print(f"{Chord(c).chars} is not {tone + type[1][0] + chords[0]}")
