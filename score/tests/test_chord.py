import unittest

from ..base import ChordException, NoteException
from ..chord import Chord, PopularChord, RomanNumeral
from ..note import Note


class TestChord(unittest.TestCase):

    def test_treblelize(self):
        chd = Chord([Note("C1"), Note("E1"), Note("C2")])
        chd.quarter_length = 2.0

        new_chord = Chord.treblelize(chd)
        self.assertEqual(chd.quarter_length, new_chord.quarter_length)
        new_numbers = [60, 64, 72]
        for i in range(0, len(new_chord.notes)):
            self.assertEqual(new_numbers[i], new_chord.notes[i].number)

    def test_bassify(self):
        chd = Chord([Note("C1"), Note("E1"), Note("C2")])
        chd.quarter_length = 2.0

        new_chord = Chord.bassify(chd)
        self.assertEqual(chd.quarter_length, new_chord.quarter_length)
        new_numbers = [36, 40, 48]
        for i in range(0, len(new_chord.notes)):
            self.assertEqual(new_numbers[i], new_chord.notes[i].number)

    def test_has_pitch(self):
        chd = RomanNumeral('C', numeral='I')
        self.assertTrue(chd.has_pitch(Note('C')))
        self.assertTrue(chd.has_pitch(Note('E8')))
        self.assertTrue(chd.has_pitch(Note('G1')))
        self.assertFalse(chd.has_pitch(Note('D')))

    def test_property_setters(self):
        example = [60, 64, 68]
        names = ['C5', 'E5', 'A-5']
        lyric = 'one'
        quarter_length = 2.0
        c = Chord()
        c.input = example
        c.lyric = lyric
        c.quarter_length = quarter_length
        self.assertEqual(c.input, example)
        self.assertEqual(c.lyric, lyric)
        self.assertEqual(c.note_names, names)
        self.assertEqual(c.quarter_length, quarter_length)
        self.assertEqual(c.note_numbers, example)

    def test_add_note(self):
        c = Chord()
        c.add_note(4)
        self.assertEqual(len(c.notes), 4)
        self.assertEqual(c.note_names[-1], 'E0')
        self.assertRaises(NoteException, c.add_note, note='None')

    def test_set_attack_velocities(self):
        c = Chord()
        vel = 100
        c.set_attack_velocities(vel)
        for n in c.notes:
            self.assertEqual(n.attack_velocity, vel)

    def test_set_release_velocities(self):
        c = Chord()
        vel = 100
        c.set_release_velocities(vel)
        for n in c.notes:
            self.assertEqual(n.release_velocity, vel)

    def test_inversion_numbers(self):
        c = Chord()
        inversions1 = [[7, 12, 16], [19, 24, 28], [31, 36, 40], [43, 48, 52], [55, 60, 64],
                      [67, 72, 76], [79, 84, 88], [91, 96, 100], [103, 108, 112],
                      [115, 120, 124], [4, 7, 12], [16, 19, 24], [28, 31, 36], [40, 43, 48],
                      [52, 55, 60], [64, 67, 72], [76, 79, 84], [88, 91, 96], [100, 103, 108],
                      [112, 115, 120], [0, 4, 7], [12, 16, 19], [24, 28, 31], [36, 40, 43],
                      [48, 52, 55], [60, 64, 67], [72, 76, 79], [84, 88, 91], [96, 100, 103],
                      [108, 112, 115]]
        inversions2 = c.inversion_numbers
        for chd in inversions2:
            self.assertIn(chd, inversions1)
        self.assertEqual(len(inversions2), 30)

    def test_from_dict(self):
        c = Chord()
        fd = Chord.from_dict({}, class_name=Chord)
        self.assertEqual(c.dict, fd.dict)

        c = Chord(quarter_length=2.0, chord_input=['C3', 'F4', 'A4'])
        fd = Chord.from_dict({"quarter_length": 2.0, "chord_input": ['C3', 'F4', 'A4']}, class_name=Chord)
        self.assertEqual(c.dict, fd.dict)


class TestPopularChord(unittest.TestCase):

    def test_property_setters(self):
        p = PopularChord()
        self.assertEqual(p.name, 'major')
        self.assertEqual(p.root.number, 48)
        names = ['augmented-major-ninth', 'Neapolitan', 'Tristan', 'minor']
        numbers = [[48, 52, 56, 59, 62], [48, 49, 52, 54], [48, 54, 58, 63], [48, 51, 55]]
        for i in range(0, len(names)):
            p = PopularChord('C', name=names[i])
            self.assertEqual(p.note_numbers, numbers[i])
        p.root = 'A'
        self.assertEqual(p.note_numbers, [57, 60, 64])


class TestRomanNumeral(unittest.TestCase):

    def test_property_setters(self):
        r = RomanNumeral()
        self.assertEqual(r.numeral, 'I')
        self.assertEqual(r.root.number, 48)
        numerals = ['I', 'IV', 'vi']
        numbers = [[48, 52, 55], [53, 57, 48], [57, 48, 52]]
        for i in range(0, len(numerals)):
            r = RomanNumeral('C', numeral=numerals[i])
            self.assertEqual(r.note_numbers, numbers[i])
        r.root = 'A'
        r.numeral = 'i'
        self.assertEqual(r.note_numbers, [57, 60, 64])
        self.assertRaises(ChordException, RomanNumeral, numeral='iv')