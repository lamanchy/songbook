class Tone(object):
    tones = "CDEFGABH"
    tone_lowerers = ["b", "es", "s"]
    tone_raisers = ["#", "is"]
    tone_modifiers = tone_lowerers + tone_raisers

    def __init__(self, tone):
        if len(tone) == 0:
            raise ValueError(f"Tone is empty!")

        tone, rest = tone[0], tone[1:]
        tone = tone.upper()
        rest = rest.lower()

        if tone not in self.tones:
            raise ValueError(f"tone {tone} is not valid tone, try one of {self.tones}")

        is_lowered = rest in self.tone_lowerers
        is_raised = rest in self.tone_raisers

        if not is_lowered and not is_raised and len(rest) > 0:
            raise ValueError(f"tone modifier {rest} is invalid, use on of {self.tone_modifiers}")

        if is_lowered and tone in "CHBF":
            is_lowered = False
            tone = self.move_tone(tone, -1)

        if is_raised and tone in "EBH":
            is_raised = False
            tone = self.move_tone(tone, 1)

        self.value, self.is_raised, self.is_lowered = tone, is_raised, is_lowered

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

    @classmethod
    def move_tone(cls, tone, direction):
        return cls.tones[(cls.tones.index(tone) + direction) % len(cls.tones)]

    def normalized(self):
        if self.is_lowered:
            t = Tone(str(self))
            t.value = t.move_tone(t.value, -1)
            t.is_lowered = False
            t.is_raised = True
            return str(t)

        return str(self)
