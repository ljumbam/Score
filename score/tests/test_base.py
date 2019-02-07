import unittest

from score import base


class TestBase(unittest.TestCase):

    def test_unique_permutations(self):
        items = 'ABCA'
        expected_perms = [('A', 'A', 'C', 'B'), ('A', 'A', 'B', 'C'), ('A', 'C', 'A', 'B'),
                          ('A', 'C', 'B', 'A'), ('A', 'B', 'A', 'C'), ('A', 'B', 'C', 'A'),
                          ('C', 'A', 'A', 'B'), ('C', 'A', 'B', 'A'), ('C', 'B', 'A', 'A'),
                          ('B', 'A', 'A', 'C'), ('B', 'A', 'C', 'A'), ('B', 'C', 'A', 'A')]
        actual_perms = list(base.unique_permutations(items))
        self.assertEqual(len(expected_perms), len(actual_perms))
        for p in expected_perms:
            self.assertIn(p, actual_perms)


class TestScoreObject(unittest.TestCase):

    def setUp(self):
        self.score_object = base.ScoreObject()

    def test_is_music_letter(self):
        music_letters = ['a', 'b', 'c', 'd', 'e', 'f', 'g',
                         'A', 'B', 'C', 'D', 'E', 'F', 'G']
        non_music_letters = ['h', 'i', 'j', 'H', 'I', 'J']
        for letter in music_letters:
            self.assertTrue(self.score_object.is_music_letter(letter))
        for letter in non_music_letters:
            self.assertFalse(self.score_object.is_music_letter(letter))

    def test_inherit(self):
        class A(object):
            a = 1
            b = 2
        self.score_object.inherit(A(), props=['a', 'b'])
        self.assertEqual(self.score_object.a, A().a)
        self.assertEqual(self.score_object.b, A().b)

    def test_validate_velocity(self):
        invalid = [-20, 200, 129, 300]
        for vel in invalid:
            self.assertRaises(base.ScoreException,
                              self.score_object.validate_velocity, vel=vel)
        self.score_object.validate_velocity(20)

    def test_strip_digits(self):
        digits = {
            'a2b3c4': 'abc',
            'jal839o': 'jalo'
        }
        for key in digits:
            self.assertEqual(digits[key], self.score_object.strip_digits(key))

    def test_validate_type(self):
        class A(object):
            pass
        self.score_object.validate_type(A(), A)
        self.assertRaises(base.ScoreException,
                          self.score_object.validate_type,
                          obj=0, instance=A)

    def test_contains(self):
        numbers = ['one', 'two', 'three', 'four']
        for num in numbers:
            self.assertTrue(self.score_object.contains(num, numbers))
            self.assertFalse(self.score_object.contains('{}1'.format(num), numbers))


class TestScoreMusicObject(unittest.TestCase):

    def setUp(self):
        self.music_object = base.ScoreMusicObject()
