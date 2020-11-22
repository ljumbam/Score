from score.base import unique_permutations, ChordException
from score.config import chord_data
from score.config import config
from score.consonance import ChordConsonance
from score.note import Note, NoteBase


class Chord(NoteBase):

    def __init__(self, chord_input=['C3', 'E4', 'G4'],
                 quarter_length=1.0):
        self._lyric = None
        self._notes = None
        self._input = None
        self._note_names = None
        self._note_numbers = None
        self._consonance = None

        super(Chord, self).__init__(quarter_length=quarter_length)
        self.input = chord_input

    def __str__(self):
        return '{}'.format(self._notes)

    def __repr__(self):
        return '{}'.format(self._notes)

    def __lt__(self, other):
        """
        Implemented this method to enable the bisect module to compare
        chords by consonance
        """
        return self.consonance < other.consonance

    def has_pitch(self, note):
        if not isinstance(note, Note):
            note = Note(note)
        for i in range(0, len(self.notes)):
            nte = self.notes[i]
            if Note.are_equal(nte, note) or \
                    Note.strip_digits(nte.name) == Note.strip_digits(note.name):
                return True
        return False

    def has_note(self, note):
        for nte in self._notes:
            if nte.number == note.number:
                return True
        return False

    def add_note(self, note):
        if isinstance(note, Note):
            note.quarter_length = self.quarter_length
        else:
            note = Note(note, quarter_length=self.quarter_length)
        if not self.has_note(note):
            self._notes.append(note)

    def set_attack_velocities(self, vel):
        for note in self._notes:
            note.attack_velocity = vel

    def set_release_velocities(self, vel):
        for note in self._notes:
            note.release_velocity = vel

    def _set_consonance(self):
        cns = ChordConsonance(notes=self.notes)
        self._consonance = cns.consonance

    @staticmethod
    def shift_range(numbers, top, bottom, interval=12):
        new_numbers = []
        for n in numbers:
            while n > top or n in new_numbers:
                n -= interval
            while n < bottom or n in new_numbers:
                n += interval
            new_numbers.append(n)
        return new_numbers

    @staticmethod
    def treblelize(chd, top=84, bottom=60):
        numbers = chd.note_numbers
        new_numbers = Chord.shift_range(numbers, top, bottom)
        new_chd = Chord(new_numbers)
        new_chd.quarter_length = chd.quarter_length
        return new_chd

    @staticmethod
    def bassify(chd, top=60, bottom=36):
        numbers = chd.note_numbers
        new_numbers = Chord.shift_range(numbers, top, bottom)
        new_chd = Chord(new_numbers)
        new_chd.quarter_length = chd.quarter_length
        return new_chd

    @staticmethod
    def are_treble_clef_numbers(chd):
        top = 84
        bottom = 60
        if (min(chd) >= bottom) and (max(chd) <= top):
            return True
        return False

    @staticmethod
    def are_bass_clef_numbers(chd):
        top = 60
        bottom = 36
        if (min(chd) >= bottom) and (max(chd) <= top):
            return True
        return False

    @property
    def quarter_length(self):
        return self._quarter_length

    @quarter_length.setter
    def quarter_length(self, quarter_length):
        if self._notes is not None:
            for note in self._notes:
                note.quarter_length = quarter_length
        self._quarter_length = quarter_length

    @property
    def consonance(self):
        if not self._consonance:
            self._set_consonance()
        return self._consonance

    @property
    def notes(self):
        return self._notes

    @property
    def input(self):
        return self._input

    @input.setter
    def input(self, chord_input):
        self.validate_type(chord_input, list)
        self._notes = []
        for n in chord_input:
            self.add_note(n)
        self._input = chord_input

    @property
    def note_names(self):
        names = []
        for note in self._notes:
            names.append(note.name)
        return names

    @property
    def note_numbers(self):
        numbers = []
        for note in self._notes:
            numbers.append(note.number)
        return numbers

    @property
    def inversion_numbers(self):
        num_of_notes = len(self._notes)
        if num_of_notes == 1:
            return [self._numbers]

        pitches = [n.pitch for n in self._notes]
        perms = list(unique_permutations(pitches))
        numbers = {}

        for i in range(0, len(pitches)):
            note = pitches[i]
            base_num = Note.get_base_note_number(note)
            numbers[note] = [j for j in range(base_num, config.MAX_NOTE_NUM, 12)]

        inversions = []
        for chord in perms:
            first_pitch = chord[0]
            for i in numbers[first_pitch]:
                inv = [i]
                for j in range(1, len(chord)):
                    if j != len(inv): break
                    for k in numbers[chord[j]]:
                        # if j != len(inv): break
                        if (k > inv[j - 1]) and (k - inv[0] <= 12):
                            inv.append(k)
                            break
                if len(inv) == len(chord):
                    inversions.append(inv)
        return inversions


class PopularChord(Chord):

    def __init__(self, root='C4', name='major', quarter_length=1.0):
        self._quarter_length = None
        self._root = None
        self._name = None

        super(PopularChord, self).__init__()
        self.quarter_length = quarter_length
        self.root = root
        self.name = name

    def _update_notes(self):
        if self._root and self._name:
            chord_props = chord_data.CHORD_TYPES[self._name]
            degrees = chord_props[0].split(',')
            self._notes = []
            notes = [int(n) + self.root.number for n in degrees]
            for n in notes:
                note = Note(n, quarter_length=self._quarter_length)
                self._notes.append(note)

    @property
    def root(self):
        return self._root

    @root.setter
    def root(self, root):
        if not isinstance(root, Note):
            root = Note(root)
        self._root = root
        self._update_notes()

    @property
    def name(self):
        return self._name

    @name.setter
    def name(self, name):
        if not self.contains(name, chord_data.CHORD_TYPES):
            raise ChordException('Invalid chord name {}'.format(name))
        self._name = name
        self._update_notes()


class RomanNumeral(Chord):

    def __init__(self, root='C4', numeral='I', quarter_length=1.0):
        self._quarter_length = None
        self._root = None
        self._numeral = None

        super(RomanNumeral, self).__init__()
        self.quarter_length = quarter_length
        self.root = root
        self.numeral = numeral

    def _update_notes(self):
        if self._root and self._numeral:
            chord_props = chord_data.ROMAN_NUMERALS[self._numeral]
            degrees = chord_props[0].split(',')
            self._notes = []
            notes = [int(n) + self.root.number for n in degrees]
            for n in notes:
                note = Note(n, quarter_length=self._quarter_length)
                self._notes.append(note)

    @property
    def root(self):
        return self._root

    @root.setter
    def root(self, root):
        if not isinstance(root, Note):
            root = Note(root)
        self._root = root
        self._update_notes()

    @property
    def numeral(self):
        return self._numeral

    @numeral.setter
    def numeral(self, numeral):
        if not self.contains(numeral, chord_data.ROMAN_NUMERALS):
            raise ChordException('Invalid chord numeral {}'.format(numeral))
        self._numeral = numeral
        self._update_notes()


def main():
    pass


if __name__ == '__main__':
    main()
