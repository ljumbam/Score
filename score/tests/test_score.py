import unittest

from score.instrument import Instrument
from score.score import Score
from score.staff import Staff


class TestScore(unittest.TestCase):

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