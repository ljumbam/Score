"""
Chord consonance based on frequency ratio
"""
from fractions import Fraction
from itertools import combinations

from score.base import ScoreObject
from score.note import Note

"""
TODO: Experiment with consonance. Consider always setting a tonic, and
      getting the consonance of 3 or more notes by the theory described in
      http://ray.tomes.biz/alex.htm
"""

class FrequencyRatios(ScoreObject):
    """
    Frequency ratios of the 12 notes that fall
    whithin an octave in an equal temparament scale
    """
    def __init__(self):
        self._ratios = [Fraction(1, 1), Fraction(15, 16), Fraction(8, 9),
                        Fraction(5, 6), Fraction(4, 5), Fraction(3, 4),
                        Fraction(5, 7), Fraction(2, 3), Fraction(5, 8),
                        Fraction(3, 5), Fraction(9, 16), Fraction(8, 15)]
        self._errors = [0, 10, 4, 16, 14, 2, 17, 2, 14, 16, 2, 12]

    @property
    def ratios(self):
        return self._ratios

    @property
    def errors(self):
        return self._errors


class Consonance(FrequencyRatios):
    """Main purpose is to return a measure of the consonance
    between the tonic and another note.

    Example:
    >>> tonic = Note('C')
    >>> nte = Note('E')
    >>> csn = Consonance(tonic=tonic)
    >>> print (csn.get_consonance(nte))
    20
    """
    def __init__(self, tonic=Note('C')):
        super(Consonance, self).__init__()
        self._tonic = None
        self._chromatic_scale = None
        self.tonic = tonic

    def get_consonance(self, nte):
        """Returns a measure of the consonance between the
        tonic note of this class and the input, nte. The consonance
        is a product of the frequency ratios between both notes.
        The smaller the product, the higher the consonance
        """
        self.validate_type(nte, Note)
        note_number = Note.get_base_note_number(nte.name)
        note_index = self._chromatic_scale.index(note_number)
        ratio = self.ratios[note_index]
        if ratio == float('inf'):
            return ratio
        else:
            consonance = ratio.numerator * ratio.denominator
            consonance = consonance # + consonance*self.errors[note_index] # Perfornamce is better without adding the errors
            return consonance

    @property
    def tonic(self):
        return self._tonic

    @tonic.setter
    def tonic(self, tonic):
        self.validate_type(tonic, Note)
        self._tonic = tonic
        self._chromatic_scale = []
        for num in range(0, 12):
            #note_name = self.strip_digits(Note(tonic.number + num).name)
            nte = Note(tonic.number + num)
            note_number = Note.get_base_note_number(nte.name)
            self._chromatic_scale.append(note_number)

    @property
    def chromatic_scale(self):
        """Chromatic scale by base note number
        """
        return self._chromatic_scale


class ChordConsonance(ScoreObject):
    """Takes in a list of notes and returns a
    consonance value

    Example:
    >>> con = ChordConsonance(notes=[Note('C'), Note('E')])
    >>> print (con.consonance)
    20
    """
    def __init__(self, notes=[]):
        self._notes = []
        self._consonance = 0
        self.notes = notes

    def _set_consonance(self):
        note_list = []
        for nte in self._notes:
                number = Note.get_base_note_number(nte.name)
                if number not in note_list:
                    note_list.append(number)

        total_consonance = 0
        for note_pair in combinations(note_list, 2):
            #smaller note should always be tonic
            tonic = Note(min(note_pair))
            nte = Note(max(note_pair))
            consonance = Consonance(tonic=tonic)
            total_consonance += consonance.get_consonance(nte)
        self._consonance = total_consonance

    @property
    def consonance(self):
        return self._consonance

    @property
    def notes(self):
        return self._notes

    @notes.setter
    def notes(self, notes):
        self.validate_type(notes, list)
        for nte in notes:
            self.validate_type(nte, Note)
        self._notes = notes
        self._set_consonance()


def main():
    pass


if __name__ == '__main__':
    main()
