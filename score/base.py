from .config import config
from .midi import MidiFactory


def unique_permutations(elements):
    if len(elements) == 1:
        yield (elements[0],)
    else:
        unique_elements = set(elements)
        for first_element in unique_elements:
            remaining_elements = list(elements)
            remaining_elements.remove(first_element)
            for sub_permutation in unique_permutations(remaining_elements):
                yield (first_element,) + sub_permutation


class ScoreObject(object):

    def is_music_letter(self, letter):
        if not self.contains(str(letter).upper(), config.MUSIC_LETTERS):
            return False
        else:
            return True

    def inherit(self, obj, props=[]):
        for prop in props:
            setattr(self, prop, getattr(obj, prop))

    def validate_velocity(self, vel):
        self.validate_type(vel, int)
        vel_range = range(config.MIN_VEL_NUM, config.MAX_VEL_NUM + 1)
        if not self.contains(vel, vel_range):
            raise ScoreException('Invalid velocity number {}. velocity '
                                 'must be an integer between {} and {}'
                                 ''.format(str(vel),
                                           str(config.MIN_VEL_NUM),
                                           str(config.MAX_VEL_NUM)))

    @classmethod
    def strip_digits(cls, str_obj):
        cls.validate_type(str_obj, str)
        return ''.join([i for i in str_obj if not i.isdigit()])

    @staticmethod
    def validate_type(obj, instance):
        if not isinstance(obj, instance):
            obj_cls = getattr(obj, '__class__').__name__
            if isinstance(instance, tuple):
                instances = []
                for i in instance:
                    instances.append(getattr(i, '__name__'))
                instance_cls = ' or '.join(instances)
            else:
                instance_cls = getattr(instance, '__name__')
            raise ScoreException('Expected an instance of type {}. '
                                 'Got an instance of type {} instead'
                                 ''.format(instance_cls, obj_cls))

    @staticmethod
    def contains(item, collection):
        return item in collection


class ScoreMusicObject(ScoreObject):

    def __init__(self):
        self._head = None
        self._current = None
        self._midi = None
        self._parent = None

        self._set_midi()

    def inherit(self, obj, props=['time_signature', 'tempo', 'volume',
                                  'attack_velocity', 'release_velocity']):
        super(ScoreMusicObject, self).inherit(obj, props=props)

    def _set_head(self, head):
        self._head = head
        self._current = head

    def _set_midi(self):
        self._midi = MidiFactory.create_midi(self)

    @property
    def parent(self):
        return self._parent

    @property
    def midi(self):
        return self._midi

    @property
    def head(self):
        return self._head

    @property
    def current(self):
        return self._current


class ScoreException(Exception):
    pass


class NoteException(ScoreException):
    pass


class ChordException(ScoreException):
    pass


class ScaleException(ScoreException):
    pass


class StaffException(ScoreException):
    pass


class KeyException(ScoreException):
    pass


def main():
    pass


if __name__ == '__main__':
    main()
