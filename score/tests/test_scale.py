import unittest

from ..base import ScaleException
from ..note import Note
from ..scale import ScaleBase, Scale, MajorScale, MinorScale, DiatonicScale


class TestScaleBase(unittest.TestCase):

    def test_has_pitch(self):
        sb = ScaleBase('C')

        scale_notes = ['C', 'D', 'E', 'F', 'G', 'A', 'B']
        non_scale_notes = ['C#', 'D#', 'F#', 'G#', 'A#']

        for i in range(0, len(scale_notes)):
            nte = scale_notes[i]
            has_pitch, idx = sb.has_pitch(nte)
            self.assertTrue(has_pitch)
            self.assertEqual(idx, i)

        for nte in non_scale_notes:
            has_pitch, idx = sb.has_pitch(nte)
            self.assertFalse(has_pitch)
            self.assertEqual(idx, None)

    def test_dict(self):
        sb = ScaleBase('C')
        sb_copy = ScaleBase(**sb.dict)
        self.assertEqual(sb.tonic.name, sb_copy.tonic.name)
        self.assertEqual(sb.intervals, sb_copy.intervals)

    def test_leap(self):
        sb = ScaleBase('C')
        self.assertRaises(ScaleException, sb.leap, 'D#', 1)
        self.assertEqual(sb.leap(Note('D3'), 2).name, 'F3')
        self.assertEqual(sb.leap(Note('D3'), 2, forward=False).name, 'B3')

    def test_property_setters(self):
        sb = ScaleBase('C')
        notes = ['C4', 'D4', 'E4', 'F4', 'G4', 'A4', 'B4']
        seq = sb.note_sequence
        for i in range(0, len(seq)):
            self.assertEqual(notes[i], seq[i].name)
        self.assertRaises(ValueError, ScaleBase, tonic='C', intervals=[3, 4])
        self.assertEqual(sb.tonic, sb.head)

    def test_set_head(self):
        sb = ScaleBase('C', intervals=[0, 2, 3, 4, 5, 7, 8])
        sb._set_head(Note('E'))
        notes = ['E4', 'F#4', 'G4', 'A-4', 'A4', 'B4', 'C5']
        seq = sb.note_sequence
        for i in range(0, len(seq)):
            self.assertEqual(notes[i], seq[i].name)
        self.assertEqual(sb.tonic, sb.head)

    def test_set_tonic(self):
        sb = ScaleBase('C')
        sb._set_tonic('G')
        self.assertEqual(sb.tonic, sb.head)
        self.assertEqual(sb.tonic.name, 'G4')

    def test_update_notes(self):
        sb = ScaleBase('C')
        sb._head = Note('D')
        sb._tonic = sb._head
        sb._update_notes()
        notes = ['D4', 'E4', 'F#4', 'G4', 'A4', 'B4', 'D-5']
        seq = sb.note_sequence
        for i in range(0, len(seq)):
            self.assertEqual(notes[i], seq[i].name)

    def test_is_scale_type(self):
        correct_types = ['tritonic', 'tetratonic', 'pentatonic', 'hexatonic',
                         'heptatonic', 'octatonic', 'nonatonic', 'dodecatonic']
        wrong_types = ['random', 'words', 'with', 'no', 'meaning']
        for t in correct_types:
            self.assertTrue(ScaleBase.is_scale_type(t))
        for t in wrong_types:
            self.assertFalse(ScaleBase.is_scale_type(t))

    def test_from_dict(self):
        s = Scale(tonic="C")
        fd = Scale.from_dict({"tonic": "C"}, Scale)
        self.assertEqual(s.dict, fd.dict)

        intervals = [0, 1, 2, 3, 4, 5, 6, 7]
        s = Scale(tonic="C", scale_type="octatonic", intervals=intervals)
        fd = Scale.from_dict({"tonic": "C", "scale_type": "octatonic", "intervals": intervals}, Scale)
        self.assertEqual(s.dict, fd.dict)


class TestScale(unittest.TestCase):

    def test_property_setters(self):
        sc = Scale('C')
        self.assertEqual(sc.intervals, [0, 2, 4, 5, 7, 9, 11])
        self.assertEqual(sc.tonic.name, 'C4')
        self.assertEqual(sc.num_pitches, 7)

        def set_intervals(intervals):
            Scale('C').intervals = intervals
        self.assertRaises(ScaleException, set_intervals, intervals=[0, 2])
        sc.scale_type = 'tritonic'
        self.assertEqual(sc.intervals, [0, 2, 3])

    def test_dict(self):
        sc = Scale('C')
        sc_copy = Scale(**sc.dict)
        self.assertEqual(sc.tonic.name, sc_copy.tonic.name)
        self.assertEqual(sc.intervals, sc_copy.intervals)
        self.assertEqual(sc.scale_type, sc_copy.scale_type)


class TestMajorScale(unittest.TestCase):

    def test_property_setters(self):
        ms = MajorScale('C')
        self.assertEqual(ms.intervals, [0, 2, 4, 5, 7, 9, 11])
        self.assertEqual(ms.scale_type, 'heptatonic')
        notes = ['C4', 'D4', 'E4', 'F4', 'G4', 'A4', 'B4']
        seq = ms.note_sequence
        for i in range(0, len(seq)):
            self.assertEqual(notes[i], seq[i].name)


class TestMinorScale(unittest.TestCase):

    def test_property_setters(self):
        ms = MinorScale('A')
        self.assertEqual(ms.intervals, [0, 2, 3, 5, 7, 8, 10])
        self.assertEqual(ms.scale_type, 'heptatonic')
        notes = ['A4', 'B4', 'C5', 'D5', 'E5', 'F5', 'G5']
        seq = ms.note_sequence
        for i in range(0, len(seq)):
            self.assertEqual(notes[i], seq[i].name)


class TestDiatonicScale(unittest.TestCase):

    def test_modes(self):
        sc = DiatonicScale('C')
        ionian = ['C4', 'D4', 'E4', 'F4', 'G4', 'A4', 'B4']
        notes = sc.ionian_mode.note_sequence
        for i in range(0, len(notes)):
            self.assertEqual(notes[i].name, ionian[i])
        dorian = ['D4', 'E4', 'F4', 'G4', 'A4', 'B4', 'C5']
        notes = sc.dorian_mode.note_sequence
        for i in range(0, len(notes)):
            self.assertEqual(notes[i].name, dorian[i])
        locrian = ['B4', 'C5', 'D5', 'E5', 'F5', 'G5', 'A5']
        notes = sc.locrian_mode.note_sequence
        for i in range(0, len(notes)):
            self.assertEqual(notes[i].name, locrian[i])

    def test_dict(self):
        s = DiatonicScale('C')
        s_copy = DiatonicScale(**s.dict)
        self.assertEqual(s.ionian_tonic, s_copy.ionian_tonic)

    def test_from_dict(self):
        d = DiatonicScale(ionian_tonic="C")
        fd = DiatonicScale.from_dict({"ionian_tonic": "C"}, DiatonicScale)

        self.assertEqual(d.ionian_mode.dict, fd.ionian_mode.dict)
        self.assertEqual(d.dorian_mode.dict, fd.dorian_mode.dict)
        self.assertEqual(d.aeolian_mode.dict, fd.aeolian_mode.dict)
