from .base import ScoreObject
from .config import instrument_data


class Instrument(ScoreObject):

    def __init__(self, name='Acoustic Grand Piano'):
        self._name = str()
        self._number = int()
        self._is_percussion = False
        self.name = name

    def __str__(self):
        return self.name

    def __repr__(self):
        return self.name

    def set_number(self, num, is_percussion=False):
        if num not in range(0, 129):
            raise ValueError('Invalid instrument number {}'.format(str(num)))
        if num not in range(35, 82) and is_percussion:
            raise ValueError('Number not that of a percussion in midi.')
        else:
            self._is_percussion = is_percussion
        self.name = self.name_from_number(num, is_percussion=self._is_percussion)

    @staticmethod
    def name_from_number(num, is_percussion=False):
        if is_percussion:
            for instrument in instrument_data.PERCUSSION:
                if instrument_data.PERCUSSION[instrument][0] == num:
                    return instrument
        else:
            for instrument in instrument_data.INSTRUMENTS:
                if instrument_data.INSTRUMENTS[instrument][0] == num:
                    return instrument

    @property
    def is_keyboard(self):
        if self._number in range(0, 22):
            return True
        return False

    @property
    def is_string(self):
        if self._number in range(41, 53):
            return True
        return False

    @property
    def is_bass(self):
        if self._number in range(33, 41):
            return True
        return False

    @property
    def is_percussion(self):
        return self._is_percussion

    @property
    def number(self):
        return self._number

    @property
    def name(self):
        return self._name

    @name.setter
    def name(self, name):
        self.validate_type(name, str)
        if self.contains(name, instrument_data.INSTRUMENTS):
            self._is_percussion = False
            self._number = instrument_data.INSTRUMENTS[name][0]
        elif self.contains(name, instrument_data.PERCUSSION):
            self._is_percussion = True
            self._number = instrument_data.PERCUSSION[name][0]
        else:
            raise ValueError('{} is not a valid midi instrument name'.format(name))
        self._name = name


def main():
    pass


if __name__ == '__main__':
    main()
