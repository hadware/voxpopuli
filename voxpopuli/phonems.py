
"""Objects and functions used for parsing and manipulating mbrola phonems"""
from typing import Tuple, List, Union


def pairwise(iterable):
    "s -> (s0, s1), (s2, s3), (s4, s5), ..."
    a = iter(iterable)
    return zip(a, a)


class Phonem:

    def __init__(self, name : str, duration : int, pitch_mods : List[Tuple[int, int]] = None):
        self.name = name
        self.duration = duration
        self.pitch_modifiers = pitch_mods if pitch_mods is not None else []

    def __str__(self):
        return self.name + "\t" \
               + str(self.duration) + "\t" \
               + " ".join([str(percent) + " " + str(pitch) for percent, pitch in self.pitch_modifiers])

    @classmethod
    def from_str(cls, pho_str):
        split_pho = pho_str.split()
        name = split_pho.pop(0)  # type:str
        duration = int(split_pho.pop(0))  # type:int
        return cls(name, duration, [(int(percent), int(pitch)) for percent, pitch in pairwise(split_pho)])

    def set_from_pitches_list(self, pitch_list : List[int]):
        segment_length = 100 / (len(pitch_list) - 1)
        self.pitch_modifiers = [(i * segment_length, pitch) for i, pitch in enumerate(pitch_list)]


class PhonemList(list):

    def __init__(self, pho_str_list : Union[List[Phonem], str]):
        if isinstance(pho_str_list, str):
            super().__init__([Phonem.from_str(pho_str) for pho_str in pho_str_list.split("\n") if pho_str])
        elif isinstance(pho_str_list, list):
            super().__init__(pho_str_list)

    def __str__(self):
        return "\n".join([str(phonem) for phonem in self])

    @property
    def phonemes_str(self):
        return "".join([str(phonem.name) for phonem in self])


class AbstractPhonemGroup:
    _all = set()

    def __contains__(self, item):
        return item in self._all


## all these sets are made from information taken here: http://www.phon.ucl.ac.uk/home/sampa/
## It's the SAMPA (based on IPA) standard for writing phonems in lots of langages


class FrenchPhonems:
    PLOSIVES = {"p", "b", "t", "d", "k", "g"}
    FRICATIVES = {'S', 'Z', 'f', 's', 'v', 'z', 'j'}
    NASAL_CONSONANTS = {'J', 'm', 'n', 'N'}
    LIQUIDS = {'H', 'R', 'j', 'l', 'w'}
    CONSONANTS = PLOSIVES | FRICATIVES | LIQUIDS | NASAL_CONSONANTS
    ORALS = {'2', '9', '@', 'A', 'E', 'O', 'a', 'e', 'i', 'o', 'u', 'y'}
    NASAL_WOVELS = {'9~', 'a~', 'e~', 'o~'}
    INDETERMINATE_WOVELS = {'&/', 'A/', 'E/', 'O/', 'U~/'}
    VOWELS = ORALS | NASAL_WOVELS | INDETERMINATE_WOVELS
    _all = VOWELS | CONSONANTS


class SpanishPhonems(AbstractPhonemGroup):
    pass


class BritishEnglishPhonems(AbstractPhonemGroup):
    PLOSIVES = {'b', 'd', 'g', 'k', 'p', 't'}
    AFFRICATES = {'dZ', 'tS'}
    FRICATIVES = {'D', 'S', 'T', 'Z', 'f', 'h', 's', 'v', 'z'}
    LIQUIDS = {'l', 'r'}
    NASALS = {'N', 'm', 'n'}
    GLIDES = {'j', 'w'}
    SONORANTS = LIQUIDS | NASALS | GLIDES
    CONSONANTS = PLOSIVES | FRICATIVES | SONORANTS | AFFRICATES
    CHECKED = {'I', 'Q', 'U', 'V', 'e', '{'}
    FREE = {'A:', 'I@', '@U', 'OI,', 'eI', 'e@', 'aI', '3:', 'U@', 'aU,', 'O:', 'i:', 'u:'}
    INDETERMINATE = {'i', 'u'}
    CENTRAL = {'@'}
    VOWELS = CHECKED | FREE | INDETERMINATE | CENTRAL
    ADDITIONALS = {"?", "x"}
    _all = VOWELS | CONSONANTS


class GermanPhonems(AbstractPhonemGroup):
    PLOSIVES = {'b', 'd', 'g', 'k', 'p', 't'}
    GLOTTAL_STOP = "?"
    AFFRICATES = {'dZ', 'pf', 'tS', 'ts'}
    FRICATIVES = {'C', 'S', 'Z', 'f', 'h', 'j', 's', 'v', 'x', 'z'}
    SONORANTS = {'N', 'R', 'l', 'm', 'n'}
    CONSONANTS = PLOSIVES | AFFRICATES | FRICATIVES | SONORANTS
    CHECKED = {'9', 'E', 'I', 'O', 'U', 'Y', 'a'}
    PURE = {'2:', 'E:', 'a:', 'e:', 'i:', 'o:', 'u:', 'y:'}
    DIPHTONGS = {'OY', 'aI', 'aU'}
    VOWELS = CHECKED | PURE | DIPHTONGS
    SCHWA = {"@"}
    CENTRING_DIPHTONGS = {'2:6', '6', '96', 'E6', 'E:6', 'I6', 'O6', 'U6', 'Y6',
                          'a6', 'a:6', 'e:6', 'i:6', 'o:6', 'u:6', 'y:6'}
    _all = VOWELS | SCHWA | CENTRING_DIPHTONGS | CONSONANTS




