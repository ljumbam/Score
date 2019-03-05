import os
import unittest

from mido import MidiFile, bpm2tempo

from ..chord import Chord
from ..instrument import Instrument
from ..midi import gcd, lcm, Midi, MidiScore
from ..note import Message, Note, Rest
from ..score import Score
from ..staff import Staff, Clef
from ..time_signature import TimeSignature


class GlobalMethods(unittest.TestCase):

    def test_gcd(self):
        gcd_map = {
            4: [4, 8, 12, 80],
            2: [4, 12, 60, 90],
            1: [3, 9, 28, 60]
        }
        for ans in gcd_map:
            self.assertEqual(gcd(*gcd_map[ans]), ans)

    def test_lcm(self):
        lcm_map = {
            240: [4, 8, 12, 80],
            180: [4, 12, 60, 90],
            1260: [3, 9, 28, 60]
        }
        for ans in lcm_map:
            self.assertEqual(lcm(*lcm_map[ans]), ans)


class TestMidi(unittest.TestCase):

    def setUp(self):
        self.midi_file = '{}/test.mid'.format(os.path.dirname(os.path.realpath(__file__)))

    def tearDown(self):
        if os.path.exists(self.midi_file):
            os.remove(self.midi_file)

    def test_save(self):
        sc = Score()
        copyright = 'Copyright AlgoTunes'
        ts = TimeSignature('3/4')
        instr = 10
        sc.copyright = copyright
        sc.time_signature = ts
        sc.instrument.set_number(instr)
        tempo = 120
        sc.tempo = tempo
        st = Staff('TrebleStaff')
        st.clefs[0].add_note(60)
        sc.add_staff(st)
        m = Midi(sc)
        m.save(self.midi_file)
        self.assertTrue(os.path.exists(self.midi_file))

        mf = MidiFile(self.midi_file)
        self.assertEqual(len(mf.tracks[0]), 7)
        for msg in mf.tracks[0]:
            if msg.type == 'copyright':
                self.assertEqual(msg.text, copyright)
            if msg.type == 'time_signature':
                self.assertEqual(msg.numerator, ts.numerator)
                self.assertEqual(msg.denominator, ts.denominator)
            if msg.type == 'program_change':
                self.assertEqual(msg.program, instr)
            if msg.type == 'set_tempo':
                self.assertEqual(msg.tempo, bpm2tempo(tempo))

    def test_create_track_if_none(self):
        sc = Score()
        m = Midi(sc)
        track_idx = 2
        m.create_track_if_none(track_idx)
        self.assertEqual(len(m.tracks), track_idx + 1)

    def test_add_staff(self):
        sc = Score()
        m = Midi(sc)

        # Add treble staff
        st = Staff('TrebleStaff')
        nte = 60
        st.clefs[0].add_note(nte)
        m.add_staff(st)
        self.assertEqual(len(m.tracks), 1)
        self.assertEqual(m.tracks[0][-2].note, nte)  # note on
        self.assertEqual(m.tracks[0][-1].note, nte)  # note off

        # Add percussion
        st = Staff('PercussionStaff')
        nte = 40
        st.clefs[0].add_note(nte)
        m.add_staff(st)
        self.assertEqual(len(m.tracks), 2)
        self.assertEqual(m.tracks[1][-2].note, nte)
        self.assertEqual(m.tracks[1][-1].note, nte)

        # Add great staff
        st = Staff('GreatStaff')
        nte1 = 50
        nte2 = 54
        st.clefs[0].add_note(nte1)
        st.clefs[1].add_note(nte2)
        m.add_staff(st)
        self.assertEqual(len(m.tracks), 4)
        self.assertEqual(m.tracks[2][-2].note, nte1)
        self.assertEqual(m.tracks[2][-1].note, nte1)
        self.assertEqual(m.tracks[3][-2].note, nte2)
        self.assertEqual(m.tracks[3][-1].note, nte2)

    def test_add_clef(self):
        sc = Score()
        m = Midi(sc)

        c = Clef('Treble')
        notes = [60, 62, 64, 66]
        for n in notes:
            c.add_note(n)

        m.add_clef(c, track_index=0, channel=1)
        msg_notes = [n for n in notes for _ in (0, 1)]
        for i in range(0, len(msg_notes)):
            self.assertEqual(m.tracks[0][i].note, msg_notes[i])

        c2 = Clef()
        c2.add_note(40)
        c2.instrument = Instrument(name='Low Bongo')
        m.add_clef(c2, track_index=1, channel=3)
        self.assertEqual(m.tracks[1][0].channel, 9)

    def test_add_message(self):
        sc = Score()
        m = Midi(sc)

        m.add_message(Message('program_change', channel=1, program=10), 0)
        m.add_message(Message('program_change', channel=1, program=1), 1)
        m.add_message(Message('track_name', name='Loayeh\'s track'), 0)
        self.assertEqual(len(m.tracks), 2)
        self.assertEqual(len(m.tracks[0]), 2)
        self.assertEqual(len(m.tracks[1]), 1)

    def test_add_obj(self):
        sc = Score()
        m = Midi(sc)

        chd = Chord([60, 64, 66])
        nte = Note(62)
        rst = Rest()
        msg = Message('program_change', channel=1, program=10)

        m.add_obj(chd)
        m.add_obj(nte)
        m.add_obj(rst)
        m.add_obj(msg, track_index=1)

        self.assertEqual(len(m.tracks), 2)
        self.assertEqual(m.tracks[0][0].note, chd.note_numbers[0])
        self.assertEqual(m.tracks[0][1].note, chd.note_numbers[1])
        self.assertEqual(m.tracks[0][2].note, chd.note_numbers[2])
        self.assertEqual(m.tracks[0][7].note, nte.number)
        self.assertEqual(m.tracks[0][9].note, rst.number)
        self.assertEqual(m.tracks[1][0].type, msg.type)

    def test_add_note(self):
        nte = Note(62, quarter_length=1.25)
        nte.lyric = 'Hey'
        nte.attack_velocity = 120
        nte.release_velocity = 60
        sc = Score()
        m = Midi(sc)
        m.add_note(nte)
        self.assertEqual(m.tracks[0][0].type, 'lyrics')
        self.assertEqual(m.tracks[0][1].note, nte.number)
        self.assertEqual(m.tracks[0][1].velocity, nte.attack_velocity)
        self.assertEqual(m.tracks[0][1].time, 0)
        self.assertEqual(m.tracks[0][2].velocity, nte.release_velocity)
        self.assertEqual(m.tracks[0][2].time, int(nte.quarter_length * m.ticks_per_beat))

    def test_add_chord(self):
        chd = Chord([60, 64, 66])
        chd.lyric = 'Hey'
        sc = Score()
        m = Midi(sc)
        m.add_chord(chd)
        self.assertEqual(m.tracks[0][0].type, 'lyrics')
        self.assertEqual(m.tracks[0][1].note, chd.note_numbers[0])
        self.assertEqual(m.tracks[0][2].note, chd.note_numbers[1])
        self.assertEqual(m.tracks[0][3].note, chd.note_numbers[2])

    def test_score_to_midi(self):
        st = Staff(time_signature=TimeSignature('3/4'))
        st.copyright = 'AlgoTunes'
        st.instrument = Instrument('Whistle')
        st.tempo = 120
        m = Midi(st)
        m._score_to_midi()
        self.assertEqual(m.tracks[0][0].type, 'copyright')
        self.assertEqual(m.tracks[0][0].text, st.copyright)
        self.assertEqual(m.tracks[0][1].type, 'time_signature')
        self.assertEqual(m.tracks[0][1].numerator, st.time_signature.numerator)
        self.assertEqual(m.tracks[0][1].denominator, st.time_signature.denominator)
        self.assertEqual(m.tracks[0][2].type, 'instrument_name')
        self.assertEqual(m.tracks[0][2].name, st.instrument.name)
        self.assertEqual(m.tracks[0][3].type, 'program_change')
        self.assertEqual(m.tracks[0][3].program, st.instrument.number)
        self.assertEqual(m.tracks[0][5].tempo, bpm2tempo(st.tempo))


