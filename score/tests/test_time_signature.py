import unittest

from ..time_signature import TimeSignature


class TestTimeSignature(unittest.TestCase):

    def test_quarters_per_measure(self):
        ts_options = {
                 "2/4": 2,
                 "1/4": 1,
                 "2/2": 4,
                 "1/2": 2,
                 "7/8": 3.5,
                 "6/8": 3,
                 "5/8": 2.5,
                 "3/8": 1.5,
                 "3/4": 3,
                 "4/4": 4
        }
        for k in ts_options:
            ts = TimeSignature(k)
            self.assertEqual(ts.quarters_per_measure, ts_options[k])

    def test_property_setters(self):
        correct = ['1/1', '2/3', '4/4', '5/3', '233/23']
        wrong = ['1/3t', '3', 4, '1.2/3']

        for i in correct:
            [num, den] = i.split('/')
            ts = TimeSignature(i)
            quarters_per_measure = float(num) / float(den) * 4.0
            self.assertTrue(TimeSignature.is_time_signature(i))
            self.assertEqual(ts.numerator, int(num))
            self.assertEqual(ts.denominator, int(den))
            self.assertEqual(ts.quarters_per_measure, quarters_per_measure)

        for i in wrong:
            self.assertFalse(TimeSignature.is_time_signature(i))
            self.assertRaises(ValueError, TimeSignature, value=i)

    def test_from_dict(self):
        fd = TimeSignature.from_dict({}, TimeSignature)
        ts = TimeSignature()
        self.assertEqual(fd.dict, ts.dict)

        fd = TimeSignature.from_dict({"value": "3/4"}, TimeSignature)
        ts = TimeSignature(value="3/4")
        self.assertEqual(fd.dict, ts.dict)
