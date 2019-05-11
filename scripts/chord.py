from scripts.tone import Tone


class UnknownChordError(BaseException):
    pass


class Chord(object):
    chord_dictionary = {
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
        self.tone: Tone = None
        self.bass_tone: Tone = None
        self.is_moll = None
        self.has_3 = True
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
            self.parse(chars)
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

    parsers = [
        (["sus2"], sus2),
        (["sus4", "sus"], sus4),
        (["add2", "add9"], add9),
        (["minmaj", "mm7"], minmaj),
        (["dimi7", "dim7", "°7"], dim7),
        (["dimi", "dim", "°"], dim),
        (["maj7", "△7"], maj7),
        (["maj9", "△9"], maj9),
        (["no3"], no3),
        (["7+5", "7#5"], lambda s: [Chord.is7(s), Chord.aug(s)]),
        (["7-5", "7b5"], lambda s: [Chord.is7(s), Chord.lowered5(s)]),
        (["aug", "(#5)", "+", "5#"], aug),
        (["ø"], lambda s: [Chord.is7(s), Chord.lowered5(s), Chord.moll(s)]),
        (["2"], sus2),
        (["4"], sus4),
        (["5"], no3),
        (["6"], add13),
        (["7"], is7),
        (["9"], is9),
        (["11"], is11),
        (["13"], is13),
        (["maj", "△", "dur"], lambda _: None),
        (["min", "mi", "mol", "m"], moll),
    ]

    def parse(self, chars):
        chars = chars.replace("6/9", "6add9")

        if "/" in chars:
            chars, bass_tone = chars.split("/", 1)
            self.bass_tone = Tone(bass_tone)

        if len(chars) == 0:
            raise ValueError(f"Chord cannot be empty")

        if chars[0].islower():
            self.moll()

        tone, chars = chars[0], chars[1:].lower()

        Tone(tone)  # just optimisation

        for marks, parser in self.parsers:
            chars = self.find_mark(chars, marks, parser)
            if len(chars) == 0:
                break

        tone += chars
        self.tone = Tone(tone)

        if self.get_ints() not in self.chord_dictionary:
            raise UnknownChordError(f"Can parse chord {self.get_ints()}, but I don't know it, "
                                    f"please add it (or call Ondra)")

    def __str__(self):
        res = str(self.tone)
        res += self.chord_dictionary[self.get_ints()]

        if self.bass_tone is not None:
            res += f"/{self.bass_tone}"

        return res

    def find_mark(self, chars, marks, fn):
        for mark in marks:
            while mark in chars:
                fn(self)
                chars = chars.replace(mark, "")

        return chars

    def transpose(self):
        self.tone.transpose()
        if self.bass_tone is not None:
            self.bass_tone.transpose()


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
        ["sus4", "4"],
        ["sus2", "2"],
        ["dim", "°", "dimi"],
        ["dim7", "°7", "dimi7"],
        ["m7b5", "ø"],
        ["aug", "+", "(#5)", "5#"],
        ["/G"],
        ["/Ab"],
        ["/C#"],
        ["/F", "/E#"],
        ["/E", "/Fb"],
    ]

    for chords in test_chords:
        for chord in chords:
            for tone in Tone.tones:
                for type in [("normal", [""]), ("lowered", Tone.tone_lowerers), ("raised", Tone.tone_raisers)]:
                    if type[0] == "lowered" and tone in "CHBF":
                        continue

                    if type[0] == "raised" and tone in "EBH":
                        continue

                    for typer in type[1]:
                        c = tone + typer + chord
                        prefix = tone + type[1][0]

                        if str(Chord(c)) != prefix + chords[0]:
                            print(f"{Chord(c)} is not {prefix + chords[0]}")
