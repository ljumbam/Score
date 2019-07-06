import unittest

from ..base import NoteException, ScoreException, StaffException
from ..chord import Chord
from ..note import Note, Rest, Message
from ..staff import Clef, Staff


class TestClef(unittest.TestCase):

    def test_property_setters(self):
        t = Clef('Treble')
        b = Clef('Bass')
        p = Clef('Percussion')

        self.assertEqual(t.name, 'Treble')
        self.assertEqual(b.name, 'Bass')
        self.assertEqual(p.name, 'Percussion')

    def test_add_note(self):
        c = Clef()
        notes = [Note('C'), Chord(['C', 'E', 'G']), Rest()]
        for n in notes:
            c.add_note(n)
        seq = c.note_sequence
        for i in range(0, len(notes)):
            self.assertEqual(notes[i], seq[i])
        self.assertRaises(NoteException, c.add_note, note='j')

    def test_add_message(self):
        c = Clef()
        msgs = [Message('control_change', control=10, value=10),
                Message('random', a=5, b=5)]
        notes = [Note('C'), Chord(['C', 'E', 'G']), Rest()]
        for m in msgs:
            c.add_message(m)
        for n in notes:
            c.add_note(n)
        seq = c.note_sequence
        self.assertEqual(len(seq), 5)
        self.assertEqual(seq[0], msgs[0])
        self.assertEqual(seq[1], msgs[1])
        self.assertRaises(ScoreException, c.add_message, Note('D'))

    def test_round_up(self):
        c = Clef()
        qls = [1.0, 2.0, 3.0]
        for ql in qls:
            c.add_note(Note(60), quarter_length=ql)
        self.assertEqual(c.total_quarter_length, sum(qls))

        offset = 4.0
        lower_total_ql = sum(qls) - offset
        higher_total_ql = sum(qls) + offset

        c.round_up(lower_total_ql)
        self.assertEqual(len(c.note_sequence), len(qls))
        self.assertEqual(c.total_quarter_length, sum(qls))

        c.round_up(higher_total_ql)
        self.assertEqual(len(c.note_sequence), len(qls) + 1)
        self.assertEqual(c.total_quarter_length, sum(qls) + offset)
        self.assertTrue(isinstance(c.note_sequence[-1], Rest))


    def test_update_neighbors(self):
        c = Clef()
        msgs = [Message('control_change', control=10, value=10),
                Message('random', a=5, b=5)]
        notes = [Note('C'), Chord(['C', 'E', 'G']), Rest()]
        for m in msgs:
            c.add_message(m)
        for n in notes:
            c.add_note(n)
        seq = c.note_sequence
        for i in range(0, len(seq)):
            if i != 0:
                self.assertTrue(seq[i].prev, seq[i - 1])
            if i != len(seq) - 1:
                self.assertTrue(seq[i].next, seq[i + 1])

    def test_unique_quarter_lengths(self):
        notes = [Note('C', quarter_length=1.0), Note('D', quarter_length=2.0),
                 Note('E', quarter_length=1.5), Note('F', quarter_length=2.5),
                 Note('E', quarter_length=1.0), Note('F', quarter_length=2.0)]
        c = Clef('Treble')
        for n in notes:
            c.add_note(n)
        for nte in c.unique_quarter_lengths:
            self.assertIn(nte, [1.0, 2.0, 2.5, 1.5])


class TestStaff(unittest.TestCase):

    def test_round_up(self):
        clef1_ql = [1.0, 1.0, 1.0, 1.0, 1.0]
        clef2_ql = [1.0, 1.0, 1.0, 1.0, 1.0, 1.0, 1.0, 1.0]
        s = Staff('GreatStaff')
        for ql in clef1_ql:
            s.clefs[0].add_note(Note(60), quarter_length=ql)
        for ql in clef2_ql:
            s.clefs[1].add_note(Note(60), quarter_length=ql)

        self.assertEqual(s.clefs[0].total_quarter_length, sum(clef1_ql))
        self.assertEqual(len(s.clefs[0].note_sequence), len(clef1_ql))
        self.assertEqual(s.clefs[1].total_quarter_length, sum(clef2_ql))
        self.assertEqual(len(s.clefs[1].note_sequence), len(clef2_ql))

        s.round_up()
        self.assertEqual(s.clefs[0].total_quarter_length, s.clefs[1].total_quarter_length)
        self.assertEqual(len(s.clefs[0].note_sequence), len(clef1_ql) + 1)
        self.assertTrue(isinstance(s.clefs[0].note_sequence[-1], Rest))
        self.assertEqual(len(s.clefs[1].note_sequence), len(clef2_ql))

        new_total_quarter_length = 12
        s.round_up(new_total_quarter_length)
        self.assertEqual(s.clefs[0].total_quarter_length, new_total_quarter_length)
        self.assertEqual(s.clefs[1].total_quarter_length, new_total_quarter_length)
        self.assertEqual(len(s.clefs[0].note_sequence), len(clef1_ql) + 2)
        self.assertTrue(isinstance(s.clefs[0].note_sequence[-1], Rest))
        self.assertTrue(isinstance(s.clefs[0].note_sequence[-2], Rest))
        self.assertEqual(len(s.clefs[1].note_sequence), len(clef2_ql) + 1)
        self.assertTrue(isinstance(s.clefs[1].note_sequence[-1], Rest))


    def test_property_setters(self):
        names = ['TrebleStaff', 'BassStaff', 'PercussionStaff']
        for n in names:
            s = Staff(n)
            self.assertEqual(s.clefs[0].name, n.replace('Staff', ''))
        self.assertRaises(StaffException, Staff, name='')
        gs = Staff('GreatStaff')
        self.assertEqual(len(gs.clefs), 2)
        self.assertEqual(gs.clefs[0].name, 'Treble')
        self.assertEqual(gs.clefs[1].name, 'Bass')