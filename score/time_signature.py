import re

from score.base import ScoreObject


class TimeSignature(ScoreObject):

    def __init__(self, value='4/4'):
        self._value = None
        self._numerator = None
        self._denominator = None
        self._quarters_per_measure = None  # Number of quarter notes per measure

        self.value = value

    def __str__(self):
        return self._value

    @staticmethod
    def is_time_signature(time_signature):
        if not isinstance(time_signature, str):
            return False
        valid_format = re.compile('^\d+/\d+$')
        if not valid_format.match(str(time_signature)):
            return False
        return True

    @property
    def quarters_per_measure(self):
        return self._quarters_per_measure

    @property
    def denominator(self):
        return self._denominator

    @property
    def numerator(self):
        return self._numerator

    @property
    def value(self):
        return self._value

    @value.setter
    def value(self, value):
        if not self.is_time_signature(value):
            raise ValueError('Invalid time signature {}'.format(value))
        else:
            self._value = value
            numbers = value.split('/')
            self._numerator = int(numbers[0])
            self._denominator = int(numbers[1])
            self._quarters_per_measure = float(numbers[0])/float(numbers[1]) * 4.0


def main():
    pass


if __name__ == '__main__':
    main()