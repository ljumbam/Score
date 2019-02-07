import unittest

from score.config import instrument_data
from score.instrument import Instrument


class TestInstrument(unittest.TestCase):

    def test_property_setters(self):
        name = 'Acoustic Grand Piano'
        i = Instrument(name=name)
        self.assertEqual(i.name, name)
        self.assertEqual(i.number, instrument_data.INSTRUMENTS[name][0])
        self.assertTrue(i.is_keyboard)
        self.assertFalse(i.is_percussion)
        self.assertFalse(i.is_string)

    def test_set_number_and_name_from_number(self):
        i = Instrument()
        self.assertRaises(ValueError, i.set_number, num=200)
        self.assertRaises(ValueError, i.set_number, num=20, is_percussion=True)
        num = 40

        i.set_number(num)
        name = Instrument.name_from_number(num)
        self.assertEqual(i.name, name)

        i.set_number(num, is_percussion=True)
        name = Instrument.name_from_number(num, is_percussion=True)
        self.assertEqual(i.name, name)
