from enum import Enum

from scripts.tone import Tone


class ScaleTypes(Enum):
    Major = 1
    NaturalMinor = 2
    HarmonicMinor = 3
    MelodicMinor = 4


class Scale(object):
    def __init__(self, tone: Tone, type: ScaleTypes):
        self.tone = tone
        self.type = type
