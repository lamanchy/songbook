class Tone(object):
    tones = "CDEFGABH"
    tone_lowerers = ["b", "es", "s"]
    tone_raisers = ["#", "is"]
    tone_modifiers = tone_lowerers + tone_raisers

    def __init__(self, tone):
        if len(tone) == 0:
            raise ValueError(f"Tone is empty!")

        tone, rest = tone[0], tone[1:]
        self.value = tone.upper()
        rest = rest.lower()

        if self.value not in self.tones:
            raise ValueError(f"tone {self.value} is not valid tone, try one of {self.tones}")

        self.is_lowered = rest in self.tone_lowerers
        self.is_raised = rest in self.tone_raisers

        if not self.is_lowered and not self.is_raised and len(rest) > 0:
            raise ValueError(f"tone modifier {rest} is invalid, use on of {self.tone_modifiers}")

        if self.is_lowered and self.value in "CHBF":
            self.is_lowered = False
            self.move_tone(-1)

        if self.is_raised and self.value in "EABH":
            self.is_raised = False
            self.move_tone(1)

    def get_rest(self):
        res = ""
        if self.is_raised:
            res += self.tone_raisers[0]
        if self.is_lowered:
            res += self.tone_lowerers[0]

        return res

    def __str__(self):
        return self.value + self.get_rest()

    def __eq__(self, other):
        return self.normalized() == other.normalized()

    def move_tone(self, direction):
        self.value = self.tones[(self.tones.index(self.value) + direction) % len(self.tones)]

    def normalized(self):
        if self.is_lowered:
            t = Tone(str(self))
            t.move_tone(-1)
            t.is_lowered = False
            t.is_raised = True
            return str(t)

        return str(self)

    def transpose(self):
        if self.is_lowered:
            self.is_lowered = False

        elif self.is_raised:
            self.is_raised = False
            self.move_tone(1)

        else:
            self.is_raised = True
            t = Tone(str(self))
            self.value, self.is_raised, self.is_lowered = t.value, t.is_raised, t.is_lowered
