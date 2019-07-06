import unittest

from ..base import ScoreException
from ..instrument import Instrument
from ..note import Note, Rest
from ..score import Score
from ..staff import Staff


class TestScore(unittest.TestCase):

    def test_merge(self):
        sc1 = Score()
        sc2 = Score()
        sc3 = Score()
        self.assertRaises(ScoreException, sc2.merge, "")

        sc1.add_staff(Staff('GreatStaff'))
        self.assertRaises(ScoreException, sc1.merge, sc2)

        sc2.add_staff(Staff('TrebleStaff'))
        self.assertRaises(ScoreException, sc1.merge, sc2)

        sc3.add_staff(Staff('GreatStaff'))
        sc3.add_staff(Staff('GreatStaff'))
        self.assertRaises(ScoreException, sc1.merge, sc3)

        sc1.add_staff(Staff('GreatStaff'))
        sc1_ql = [
            {
                'treble': [1.0, 2.0],
                'bass': [1.0]
            },
            {
                'treble': [1.0, 2.0, 1.0, 0.5],
                'bass': [1.0, 0.5]
            }
        ]
        sc3_ql = [
            {
                'treble': [1.0, 2.0, 4.0],
                'bass': [1.0, 2.0, 1.0]
            },
            {
                'treble': [1.0, 2.0, 1.0, 0.5, 3.0],
                'bass': [1.0, 0.5, 1.0]
            }
        ]

        for i in range(0, len(sc1_ql)):
            for ql in sc1_ql[i]['treble']:
                sc1.staves[i].clefs[0].add_note(Note(60), quarter_length=ql)
            for ql in sc1_ql[i]['bass']:
                sc1.staves[i].clefs[1].add_note(Note(60), quarter_length=ql)

        for i in range(0, len(sc3_ql)):
            for ql in sc3_ql[i]['treble']:
                sc3.staves[i].clefs[0].add_note(Note(60), quarter_length=ql)
            for ql in sc3_ql[i]['bass']:
                sc3.staves[i].clefs[1].add_note(Note(60), quarter_length=ql)

        sc1.merge(sc3)
        longest_quarter_length = 0
        for i in range(0, len(sc1_ql)):
            treble_ql = sum(sc1_ql[i]['treble'] + sc3_ql[i]['treble'])
            bass_ql = sum(sc1_ql[i]['bass'] + sc3_ql[i]['bass'])

            if treble_ql > longest_quarter_length:
                longest_quarter_length = treble_ql

            if bass_ql > longest_quarter_length:
                longest_quarter_length = bass_ql

        for i in range(0, len(sc1_ql)):
            self.assertEqual(longest_quarter_length, sc1.staves[i].clefs[0].total_quarter_length)
            self.assertEqual(longest_quarter_length, sc1.staves[i].clefs[1].total_quarter_length)

        self.assertEqual(len(sc1.staves), len(sc1_ql))
        self.assertEqual(len(sc3.staves), len(sc3_ql))

    def test_round_up(self):
        sc = Score()
        staves = [
            {
                'Treble': [1.0, 1.0, 1.0],
                'Bass': [1.0, 1.0, 1.0, 1.0, 1.0, 1.0]
            },
            {
                'Treble': [1.0, 1.0, 1.0, 1.0],
                'Bass': [1.0, 1.0, 1.0, 1.0, 1.0, 1.0, 1.0, 1.0]
            },
            {
                'Treble': [1.0, 1.0, 1.0],
                'Bass': [1.0, 1.0, 1.0, 1.0, 1.0, 1.0]
            },
            {
                'Treble': [1.0],
                'Bass': [1.0, 1.0, 1.0, 1.0, 1.0, 1.0, 1.0, 1.0, 1.0]
            }
        ]
        for stf in staves:
            sc.add_staff(Staff('GreatStaff'))
            for ql in stf['Treble']:
                sc.staves[-1].clefs[0].add_note(Note(60), quarter_length=ql)
            for ql in stf['Bass']:
                sc.staves[-1].clefs[1].add_note(Note(60), quarter_length=ql)

        for i in range(0, len(sc.staves)):
            stf = sc.staves[i]
            self.assertEqual(len(stf.clefs[0].note_sequence), len(staves[i]['Treble']))
            self.assertEqual(stf.clefs[0].total_quarter_length, sum(staves[i]['Treble']))
            self.assertEqual(len(stf.clefs[1].note_sequence), len(staves[i]['Bass']))
            self.assertEqual(stf.clefs[1].total_quarter_length, sum(staves[i]['Bass']))

        longest_quarter_length = 0
        stf_idx = None
        clf_idx = None
        for i in range(0, len(staves)):
            stf = staves[i]
            for clf in stf:
                clf_ql = sum(stf[clf])
                if longest_quarter_length < clf_ql:
                    longest_quarter_length = clf_ql
                    stf_idx = i
                    clf_idx = 0 if clf == 'Treble' else 1

        sc.round_up()
        for i in range(0, len(sc.staves)):
            stf = sc.staves[i]
            self.assertEqual(stf.clefs[0].total_quarter_length, longest_quarter_length)
            self.assertEqual(stf.clefs[1].total_quarter_length, longest_quarter_length)

            if i == stf_idx:
                if clf_idx == 0:
                    self.assertEqual(len(stf.clefs[0].note_sequence), len(staves[i]['Treble']))
                elif clf_idx == 1:
                    self.assertEqual(len(stf.clefs[1].note_sequence), len(staves[i]['Bass']))
            else:
                self.assertTrue(isinstance(stf.clefs[0].note_sequence[-1], Rest))
                self.assertTrue(isinstance(stf.clefs[1].note_sequence[-1], Rest))

    def test_property_setters(self):
        props = {
            'title': 'Test Score',
            'lyrics_by': 'Composer',
            'music_by': 'AlgoTunes',
            'genre': 'AfroPop'
        }
        sc = Score()
        for key in props:
            setattr(sc, key, props[key])

        for key in props:
            self.assertEqual(getattr(sc, key), props[key])
        self.assertEqual(sc.staves, [])
        self.assertEqual(sc.time_signature.value, '4/4')

    def test_add_staff(self):
        st = Staff()
        sc = Score()
        sc.add_staff(st)
        self.assertEqual(sc.staves[0], st)

    def test_has_instrument(self):
        st1 = Staff()
        st1.instrument = Instrument(name='Cello')
        st2 = Staff()
        st2.instrument = Instrument(name='Voice Oohs')
        st3 = Staff()
        st3.instrument = Instrument(name='Bass Drum 2')
        sc = Score()
        sc.add_staff(st1)
        sc.add_staff(st2)
        sc.add_staff(st3)
        self.assertTrue(sc.has_instrument(st1.instrument.number))
        self.assertTrue(sc.has_instrument(st2.instrument.number))
        self.assertTrue(sc.has_instrument(st3.instrument.number, is_percussion=True))
        self.assertFalse(sc.has_instrument(st3.instrument.number))
        self.assertFalse(sc.has_instrument(st2.instrument.number, is_percussion=True))
        self.assertFalse(sc.has_instrument(1))