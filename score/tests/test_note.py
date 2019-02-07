import unittest

from score.base import ScoreException
from score.config import config
from score.instrument import Instrument
from score.note import MusicObject, Note, NoteBase, Message, Rest
from score.time_signature import TimeSignature


class TestMusicObject(unittest.TestCase):

    def test_set_head(self):
        mo = MusicObject(time_signature=TimeSignature('4/4'))
        n = Note(60)
        mo._set_head(n)
        self.assertRaises(ScoreException, mo._set_head, 10)

    def test_note_sequence(self):
        mo = MusicObject(time_signature=TimeSignature('4/4'))
        n = Note(60)
        n.next = Note(62)
        n.next.next = Note(64)
        mo._set_head(n)
        notes = mo.note_sequence
        self.assertEqual(notes[0].number, n.number)
        self.assertEqual(notes[1].number, n.next.number)
        self.assertEqual(notes[2].number, n.next.next.number)

    def test_property_setters(self):
        ts = '3/4'
        tempo = 92
        vol = 43
        attack_vel = 120
        release_vel = 20
        inst = Instrument()
        mo = MusicObject(time_signature=TimeSignature(ts))
        mo.tempo = tempo
        mo.volume = vol
        mo.attack_velocity = attack_vel
        mo.release_velocity = release_vel
        mo.instrument = inst
        self.assertEqual(mo.time_signature.value, ts)
        self.assertEqual(mo.tempo, tempo)
        self.assertEqual(mo.volume, vol)
        self.assertEqual(mo.release_velocity, release_vel)
        self.assertEqual(mo.attack_velocity, attack_vel)
        self.assertEqual(mo.instrument.number, inst.number)


class TestNoteBase(unittest.TestCase):

    def test_property_setters(self):
        nb = NoteBase()
        self.assertRaises(ScoreException, setattr, nb, 'quarter_length', 'one')
        self.assertRaises(ScoreException, setattr, nb, 'lyric', 100)
        self.assertRaises(ScoreException, setattr, nb, 'next', 'n')
        props = {
            'quarter_length': 1.0,
            'lyric': 'Random',
            'next': Note(60),
        }
        for key in props:
            setattr(nb, key, props[key])
        self.assertEqual(nb.next.prev, nb)

    def test_reset_position(self):
        nb = NoteBase()
        nb.next = Note(60)
        nb.next.next = Note(64)
        self.assertIsNotNone(nb.next)
        self.assertIsNotNone(nb.next.prev)
        nb.next.reset_position()
        self.assertIsNone(nb.next.next)
        self.assertIsNone(nb.next.prev)

    def test_set_prev(self):
        nb = NoteBase()
        nb.set_prev(Note(60))
        self.assertEqual(nb.prev.number, 60)
        self.assertRaises(ScoreException, nb.set_prev, prev_item=100)


class TestMessage(unittest.TestCase):

    def test_property_setters(self):
        message_type = 'random'
        m = Message(message_type, a=1, b=2)
        self.assertEqual(m.type, message_type)
        self.assertEqual(m.parameters['a'], 1)
        self.assertEqual(m.parameters['b'], 2)
        message_type = 'control_change'
        Message(message_type, control=10, value=10)
        self.assertRaises(ValueError, Message, msg_type=message_type,
                          control=128, value=10)

    def test_validate_control(self):
        message_type = 'random'
        m = Message(message_type, a=1, b=2)
        m.validate_control(10, 10)
        self.assertRaises(ValueError, m.validate_control, control=128, value=10)


class TestNote(unittest.TestCase):

    def test_property_setters(self):
        num = 60
        ql = 20.0
        nte = Note(num, quarter_length=ql)
        self.assertEqual(nte.name, 'C5')
        self.assertEqual(nte.number, num)
        self.assertEqual(nte.octave, 5)
        self.assertEqual(nte.pitch, 'C')
        self.assertEqual(nte.input, num)
        self.assertEqual(nte.enharmonic, 'B#5')
        self.assertEqual(nte.quarter_length, ql)

    def test_frequency(self):
        notes = [30, 40, 45, 60, 73]
        for n in notes:
            nte = Note(n)
            freq = int((440.00 * 1.0594630943592953 ** (n - 57)) * 100 +.5) / 100.0
            self.assertEqual(freq, nte.frequency)

    def test_sanitzie_name(self):
        bad_names = ['E#', 'B#', 'F-', 'C-', '6C', 'G#']
        good_names = ['F4', 'C4', 'E4', 'B4', 'C6', 'G#4']
        for i in range(0, len(bad_names)):
            self.assertEqual(Note.sanitize_name(bad_names[i]),
                             good_names[i])

    def test_is_note_number(self):
        self.assertFalse(Note.is_note_num(-1))
        self.assertFalse(Note.is_note_num(128))
        self.assertTrue(Note.is_note_num(0))
        self.assertTrue(Note.is_note_num(127))

    def test_is_note_name(self):
        bad = [1, 'y', 'c##', '#3C']
        good = ['C#', 'c-', 'd', 'E#']
        for n in bad:
            self.assertFalse(Note.is_note_name(n))
        for n in good:
            self.assertTrue(Note.is_note_name(n))

    def test_has_valid_octave(self):
        bad = ['C200', 'd100', 'c-13']
        good = ['c3', 'd5', 'c-7']
        for n in bad:
            self.assertFalse(Note.has_valid_octave(n))
        for n in good:
            self.assertTrue(Note.has_valid_octave(n))

    def test_is_midi_note(self):
        bad = ['C500', 'd100', 'c-13']
        good = ['c3', 'd5', 'c-7']
        for n in bad:
            self.assertFalse(Note.is_midi_note(n))
        for n in good:
            self.assertTrue(Note.is_midi_note(n))

    def test_name_to_number(self):
        name = ['C4', 'd-2', 'c#5', 'g-4']
        number = [48, 25, 61, 54]
        for i in range(0, len(name)):
            self.assertEqual(Note.name_to_number(name[i]), number[i])

    def test_octave_from_name(self):
        name = ['C', 'd-2', 'g6']
        octave = [4, 2, 6]
        for i in range(0, len(name)):
            self.assertEqual(Note.octave_from_name(name[i]), octave[i])
        self.assertRaises(ValueError, Note.octave_from_name, note_name='c2-3')

    def test_get_base_note_number(self):
        names = ['C', 'C#', 'D', 'D#', 'E', 'F', 'F#']
        base_num = [0, 1, 2, 3, 4, 5, 6]
        for i in range(0, len(names)):
            self.assertEqual(Note.get_base_note_number(names[i]),
                             base_num[i])

    def test_letter_from_name(self):
        names = ['C', 'C#', 'D43', 'F#5', 'g32']
        letter = ['C', 'C', 'D', 'F', 'G']
        for i in range(0, len(names)):
            self.assertEqual(Note.letter_from_name(names[i]),
                             letter[i])

    def test_are_equal(self):
        n1 = [Note(60), 'C5']
        n2 = [60, Note(60)]
        n3 = ['F', 'G']
        for i in range(0, len(n1)):
            self.assertTrue(Note.are_equal(n1[i], n2[i]))
            self.assertFalse(Note.are_equal(n1[i], n3[i]))

    def test_has_valid_octave(self):
        bad = ['c100', 'g12', 'd200']
        good = ['C6', 'G10', 'd8']
        for n in bad:
            self.assertFalse(Note.has_valid_octave(n))
        for n in good:
            self.assertTrue(Note.has_valid_octave(n))

    def test_octave_from_number(self):
        numbers = [60, 65, 70, 75, 80, 85]
        octaves = [5, 5, 5, 6, 6, 7]

        for i in range(0, len(numbers)):
            self.assertEqual(Note.octave_from_number(numbers[i]),
                             octaves[i])

    def test_pitch_from_name(self):
        names = ['c#3', 'D2', 'f#4', 'd4', 'g#-5', 'd-4']
        pitches = ['C#', 'D', 'F#', 'D', 'G', 'D-']
        for i in range(0, len(names)):
            self.assertEqual(Note.pitch_from_name(names[i]),
                             pitches[i])

    def test_pitch_from_number(self):
        numbers = [20, 25, 35, 50, 73]
        pitches = ['A-', 'D-', 'B', 'D', 'D-']
        for i in range(0, len(numbers)):
            self.assertEqual(Note.pitch_from_number(numbers[i]),
                             pitches[i])

    def test_letter_from_number(self):
        numbers = [20, 25, 35, 50, 73]
        pitches = ['A', 'D', 'B', 'D', 'D']
        for i in range(0, len(numbers)):
            self.assertEqual(Note.letter_from_number(numbers[i]),
                             pitches[i])

    def test_enharmonic_from_name(self):
        names = ['c#3', 'D2', 'f#4', 'd4', 'g#-5', 'd-4']
        enharmonics = ['C#3', None, 'G-4', 'D4', 'G5', 'C#4']
        for i in range(0, len(names)):
            self.assertEqual(Note.enharmonic_from_name(names[i]),
                             enharmonics[i])

    def test_number_to_name(self):
        name = ['C4', 'D-2', 'D-5', 'F#4']
        number = [48, 25, 61, 54]
        for i in range(0, len(number)):
            self.assertEqual(Note.number_to_name(number[i]),
                             name[i])

    def test_get_accidental(self):
        self.assertRaises(ValueError, Note.get_accidental, note_name=4)
        self.assertEqual(Note.get_accidental('f#'), '#')
        self.assertEqual(Note.get_accidental('g-'), '-')

    def test_is_note(self):
        correct_notes = ['A', 'D-', 'f#', 0, 43, 'C5']
        wrong_notes = ['dd', 'l', 1000, 'k', 'C12', 'A11']
        for note in correct_notes:
            self.assertTrue(Note.is_note(note))
        for note in wrong_notes:
            self.assertFalse(Note.is_note(note))
        for note_num in config.PITCHCLASS_NOTENAMES:
            self.assertTrue(Note.is_note(note_num))
        for note_string in config.KEY_NAMES:
            self.assertTrue(Note.is_note(note_string))


class TestRest(unittest.TestCase):

    def test_init(self):
        r = Rest()
        self.assertEqual(r.attack_velocity, 0)
        self.assertEqual(r.release_velocity, 0)
