from .base import ScoreObject, KeyException
from .config import config
from .scale import MajorScale, MinorScale


class Key(ScoreObject):

    def __init__(self, key):
        self._key = None
        self._tonic = None
        self._mode_type = None
        self._name = None

        self.key = key
        super(Key, self).__init__()

    def __str__(self):
        return self._name

    def is_key_string(self, key):
        if self.contains(key, config.KEY_NAMES):
            return True
        else:
            return False

    def validate(self, key):
        if not self.is_key_string(key):
            raise KeyException('Invalid music key {}'.format(key))

    def _set_tonic(self):
        self._tonic = self._key.upper()

    def _set_mode_type(self):
        if self.key.isupper():
            self._mode_type = 'major'
        else:
            self._mode_type = 'minor'

    def _set_name(self):
        self._name = '{} {}'.format(self.key.upper(), self.mode_type)

    @property
    def tonic(self):
        return self._tonic

    @property
    def mode_type(self):
        return self._mode_type

    @property
    def name(self):
        return self._name

    @property
    def key(self):
        return self._key

    @key.setter
    def key(self, key):
        self.validate(key)
        self._key = key
        self._set_tonic()
        self._set_mode_type()
        self._set_name()


class Accidentals(ScoreObject):

    def __init__(self):
        self._sharpen = []
        self._flatten = []
        self._naturalize = config.MUSIC_LETTERS

    def validate_music_letters(self, letters):
        self.validate_type(letters, list)
        for letter in letters:
            if not self.is_music_letter(letter):
                raise ValueError('Encountered invalid music letter {}'.format(letter))

    def remove_item(self, i, items):
        self.validate_type(items, list)
        return [x for x in items if x != i]

    @property
    def sharpen(self):
        return self._sharpen

    @sharpen.setter
    def sharpen(self, keys):
        self.validate_music_letters(keys)
        for k in keys:
            k = k.upper()
            if k not in self._sharpen:
                self._sharpen.append(k)
            if k in self._flatten:
                self._flatten = self.remove_item(k, self._flatten)
            if k in self._naturalize:
                self._naturalize = self.remove_item(k, self._naturalize)

    @property
    def flatten(self):
        return self._flatten

    @flatten.setter
    def flatten(self, keys):
        self.validate_music_letters(keys)
        for k in keys:
            k = k.upper()
            if k not in self._flatten:
                self._flatten.append(k)
            if k in self._sharpen:
                self._sharpen = self.remove_item(k, self._sharpen)
            if k in self._naturalize:
                self._naturalize = self.remove_item(k, self._naturalize)

    @property
    def naturalize(self):
        return self._naturalize

    @naturalize.setter
    def naturalize(self, keys):
        self.validate_music_letters(keys)
        for k in keys:
            k = k.upper()
            if k not in self._naturalize:
                self._naturalize.append(k)
            if k in self._sharpen:
                self._sharpen = self.remove_item(k, self._sharpen)
            if k in self._flatten:
                self._flatten = self.remove_item(k, self._flatten)


class KeySignature(ScoreObject):

    def __init__(self, key):
        self._accidentals = Accidentals()
        self._scale = None
        self._key = None

        self.key = key
        super(KeySignature, self).__init__()

    def __str__(self):
        return '{} {}'.format(self._key.name, self._scale)

    @property
    def accidentals(self):
        return self._accidentals

    def _set_scale(self):
        if self.key.mode_type == 'major':
            self._scale = MajorScale(self.key.tonic)
        elif self.key.mode_type == 'minor':
            self._scale = MinorScale(self.key.tonic)
        self._set_accidentals()

    def _set_accidentals(self):
        sharp_list = []
        flat_list = []
        for n in self._scale.note_sequence:
            note = self.strip_digits(n.name)
            if '#' in note:
                sharp_list.append(note.replace('#',''))
            elif '-' in note:
                flat_list.append(note.replace('-', ''))
        self.accidentals.sharpen = sharp_list
        self.accidentals.flatten = flat_list

    @property
    def scale(self):
        return self._scale

    @property
    def key(self):
        return self._key

    @key.setter
    def key(self, key):
        if isinstance(key, Key):
            self._key = key
        else:
            self._key = Key(key)
        self._set_scale()


def main():
    k = Key('d-')
    print (k)

    a = Accidentals()
    a.sharpen = ['a', 'd']
    print a.sharpen, a.flatten, a.naturalize

    ks = KeySignature('c')
    print ks


if __name__ == '__main__':
    main()
