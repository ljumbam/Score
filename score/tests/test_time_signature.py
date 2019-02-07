import unittest

from score.time_signature import TimeSignature


class TestTimeSignature(unittest.TestCase):

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
