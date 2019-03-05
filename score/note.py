import logging.config
import re

from .base import ScoreMusicObject, NoteException
from .config import config
from .config.controllers_data import MIDI_CONTROLLERS
from .instrument import Instrument
from .time_signature import TimeSignature

logging.config.dictConfig(config.LOGGING_CONFIG)


class MusicObject(ScoreMusicObject):

    def __init__(self, time_signature=TimeSignature('4/4')):
        self._time_signature = None
        self._tempo = 120
        self._volume = 64
        self._instrument = Instrument()
        self._attack_velocity = config.AVE_ATTACK_VEL
        self._release_velocity = config.AVE_RELEASE_VEL

        self.time_signature = time_signature
        super(MusicObject, self).__init__()

    def _set_head(self, head):
        self.validate_type(head, NoteBase)
        super(MusicObject, self)._set_head(head)

    @property
    def note_sequence(self):
        objects = []
        current = self.head
        if current:
            objects.append(current)
            while current.next:
                objects.append(current.next)
                current = current.next
        return objects

    @property
    def instrument(self):
        return self._instrument

    @instrument.setter
    def instrument(self, instrument):
        if not isinstance(instrument, Instrument):
            self._instrument = Instrument(name=instrument)
        else:
            self._instrument = instrument

    @property
    def tempo(self):
        return self._tempo

    @tempo.setter
    def tempo(self, tempo):
        self.validate_type(tempo, int)
        if config.MIN_TEMPO_NUM > tempo or tempo > config.MAX_TEMPO_NUM:
            raise ValueError('Invalid tempo {}'.format(tempo))
        self._tempo = tempo

    @property
    def volume(self):
        return self._volume

    @volume.setter
    def volume(self, volume):
        self.validate_type(volume, int)
        if config.MIN_VEL_NUM > volume or volume > config.MAX_VEL_NUM:
            raise ValueError('Invalid volume {}'.format(volume))
        self._volume = volume

    @property
    def attack_velocity(self):
        return self._attack_velocity

    @attack_velocity.setter
    def attack_velocity(self, vel):
        self.validate_velocity(vel)
        self._attack_velocity = vel

    @property
    def release_velocity(self):
        return self._release_velocity

    @release_velocity.setter
    def release_velocity(self, vel):
        self.validate_velocity(vel)
        self._release_velocity = vel

    @property
    def time_signature(self):
        return self._time_signature

    @time_signature.setter
    def time_signature(self, time_signature):
        if not isinstance(time_signature, TimeSignature):
            time_signature = TimeSignature(time_signature)
        self._time_signature = time_signature


class NoteBase(MusicObject):

    def __init__(self, quarter_length=1.0):
        self._quarter_length = None
        self._lyric = None
        self._next = None
        self._prev = None
        self.quarter_length = quarter_length
        super(NoteBase, self).__init__()
        self._set_head(self)

    def reset_position(self):
        self._next = None
        self._prev = None

    def set_prev(self, prev_item):
        self.validate_type(prev_item, NoteBase)
        self._prev = prev_item

    @property
    def quarter_length(self):
        return self._quarter_length

    @quarter_length.setter
    def quarter_length(self, length):
        self.validate_type(length, (int, float))
        if length < 0:
            raise ValueError('Quarter length should be positive')
        else:
            self._quarter_length = float(length)

    @property
    def lyric(self):
        return self._lyric

    @lyric.setter
    def lyric(self, lyric):
        self.validate_type(lyric, str)
        self._lyric = lyric

    @property
    def next(self):
        return self._next

    @next.setter
    def next(self, next_item):
        self.validate_type(next_item, NoteBase)
        next_item.set_prev(self)
        self._next = next_item

    @property
    def prev(self):
        return self._prev


class Message(NoteBase):

    def __init__(self, msg_type, **parameters):
        self._type = None
        self._parameters = None

        self.parameters = parameters
        self.type = msg_type
        super(Message, self).__init__()

    def __str__(self):
        return '{} {}'.format(self._type, self._parameters)

    @property
    def parameters(self):
        return self._parameters

    @parameters.setter
    def parameters(self, parameters):
        self._parameters = parameters

    @property
    def type(self):
        return self._type

    @type.setter
    def type(self, msg_type):
        self.validate_type(msg_type, str)
        if msg_type == 'control_change':
            control = self._parameters.get('control', None)
            value = self._parameters.get('value', None)
            if control is None or value is None:
                raise ValueError('Expected properties \'control\' '
                                 'and \'value\' for control_change '
                                 'message')
            self.validate_control(control, value)
        else:
            # NB: Mido's pitchbend message implementation is missing one
            # parameter - value
            pass
        self._type = msg_type

    def validate_control(self, control, value):
        if not self.contains(control, MIDI_CONTROLLERS.keys()):
            raise ValueError('Invalid control {}'.format(control))
        if not self.contains(value, MIDI_CONTROLLERS[control][1]):
            raise ValueError('Invalid value {} for control {}'
                             ''.format(value, MIDI_CONTROLLERS[control][0]))


class Note(NoteBase):

    def __init__(self, note_input, quarter_length=1.0):
        self._name = None
        self._number = None
        self._octave = None
        self._pitch = None
        self._input = None
        self._enharmonic = None
        self._attack_velocity = config.AVE_ATTACK_VEL
        self._release_velocity = config.AVE_RELEASE_VEL

        self.input = note_input
        super(Note, self).__init__(quarter_length=quarter_length)

    # TODO: Add play option for midi?
    # TODO: Add symbol and command only at the end

    def __str__(self):
        return '{0} {1}'.format(self.name, str(self.quarter_length))

    def __repr__(self):
        return '{0} {1}'.format(self.name, str(self.quarter_length))

    @property
    def name(self):
        return self._name

    @property
    def number(self):
        return self._number

    @property
    def octave(self):
        return self._octave

    @property
    def pitch(self):
        return self._pitch

    @property
    def enharmonic(self):
        return self._enharmonic

    @property
    def input(self):
        return self._input

    @input.setter
    def input(self, note_input):
        if self.is_note(note_input):
            if self.is_note_name(note_input):
                self._note_input = note_input
                self._name = self.sanitize_name(note_input)
                self._number = self.name_to_number(note_input)
                self._enharmonic = self.enharmonic_from_name(self._name)
                self._octave = self.octave_from_name(note_input)
                self._pitch = self.pitch_from_name(note_input)
            elif self.is_note_num(note_input):
                self._note_input = note_input
                self._number = note_input
                self._name = self.number_to_name(note_input)
                self._enharmonic = self.enharmonic_from_name(self._name)
                self._octave = self.octave_from_number(note_input)
                self._pitch = self.pitch_from_number(note_input)
            self._input = note_input
        else:
            raise NoteException('Invalid note {0}'.format(note_input))

    @property
    def frequency(self):
        """
        Source: http://www.phy.mtu.edu/~suits/NoteFreqCalcs.html

        fn = f0 * (a)^n

        Where:
        f0 = the frequency of one fixed note which must be defined.
             A common choice is setting the A above middle C (A4) at
             f0 = 440 Hz.
        n  = the number of half steps away from the fixed note you are.
             If you are at a higher note, n is positive. If you are on a
             lower note, n is negative.
        fn = the frequency of the note n half steps away.
        a  = (2)1/12 = the twelth root of 2 = the number which when
             multiplied by itself 12 times equals 2 = 1.059463094359...
        """
        fn = 440.00 * 1.0594630943592953 ** (self.number - 57)
        return int(fn * 100 + .5) / 100.0  # Round to first two decimals

    @property
    def attack_velocity(self):
        return self._attack_velocity

    @attack_velocity.setter
    def attack_velocity(self, vel):
        self.validate_velocity(vel)
        self._attack_velocity = vel

    @property
    def release_velocity(self):
        return self._release_velocity

    @release_velocity.setter
    def release_velocity(self, vel):
        self.validate_velocity(vel)
        self._release_velocity = vel

    @classmethod
    def letter_from_number(cls, num):
        pitch = cls.pitch_from_number(num)
        return cls.letter_from_name(pitch)

    @classmethod
    def sanitize_name(cls, name):
        name = name.upper()
        bad_names = {
            'E#': 'F',
            'B#': 'C',
            'F-': 'E',
            'C-': 'B'
        }
        for n in bad_names:
            if n in name:
                logging.warning('The note name {0} is not a standard note name. '
                                'It will be replaced with its valid equivalent '
                                ''.format(name))
                name = name.replace(n, bad_names[n])
                base_num = cls.get_base_note_number(name)
                base_name = config.PITCHCLASS_NOTENAMES[base_num][0]
                octave = cls.octave_from_name(name)
                name = base_name + str(octave)
                return name

        # add octave if absent
        digits = re.findall('\d+', name)
        if len(digits) == 0:
            name += str(4)
        else:  # make sure digit is at the end of the string
            name = cls.strip_digits(name) + digits[0]
        return name

    @classmethod
    def is_note(cls, note):
        if cls.is_note_num(note) or cls.is_note_name(note) \
                or cls.is_note_instance(note):
            return True
        else:
            return False

    @staticmethod
    def is_note_instance(note):
        return isinstance(note, Note)

    @classmethod
    def is_note_num(cls, num):
        if isinstance(num, int):
            if cls.contains(num, range(config.MIN_NOTE_NUM,
                                       config.MAX_NOTE_NUM + 1)):
                return True
            else:
                return False
        else:
            return False

    @classmethod
    def is_note_name(cls, name):
        if isinstance(name, str):
            count_sharps = name.count('#')
            count_flats = name.count('-')
            if count_sharps and count_flats:
                return False
            if count_sharps > 1 or count_flats > 1:
                return False
            # remove sharps/flats and check if format is [c][d], where
            # [c] represents a character, and [d] a digit
            note_name = name.replace('#', '').replace('-', '')
            valid_format = re.compile('^([a-gA-G])(\d+)?$')
            if not valid_format.match(note_name) \
                    or not cls.has_valid_octave(note_name) \
                    or not cls.is_midi_note(note_name):
                return False
            else:
                return True
        else:
            return False

    @classmethod
    def has_valid_octave(cls, name):
        octave = cls.octave_from_name(name)
        if octave is False:
            return False
        if int(octave) < config.MIN_OCTAVE \
                or int(octave) > config.MAX_OCTAVE:
            return False
        else:
            return True

    @classmethod
    def is_midi_note(cls, name):
        note_num = cls.name_to_number(name)
        if cls.is_note_num(note_num):
            return True
        else:
            return False

    @classmethod
    def name_to_number(cls, name):
        octave = cls.octave_from_name(name)
        base_note_num = cls.get_base_note_number(name)
        note_num = octave * 12 + base_note_num
        return note_num

    @staticmethod
    def octave_from_name(note_name):
        digits = re.findall('\d+', note_name)
        if len(digits) == 0:  # no number implies octave = 4
            return 4
        elif len(digits) == 1:
            return int(digits[0])
        else:
            raise ValueError('Invalid note name {} provided'.format(note_name))
            # invalid octave. if this ever occurs
            # it will be from invalid note with two
            # digits e.g. C#2-3

    @staticmethod
    def get_base_note_number(name):
        num_sharps = name.count('#')
        num_flats = name.count('-')
        letter = Note.letter_from_name(name)
        base_pitch_class = config.NOTENAMES_PITCHCLASS[letter]
        base_note_number = num_sharps - num_flats + base_pitch_class
        if base_note_number == 12:
            base_note_number = 0
        if base_note_number < 0:
            base_note_number += 12
        return base_note_number

    @staticmethod
    def letter_from_name(note_name):
        # pitch = filter(lambda x: x.isalpha(), note_name) # filter works differently in python 3
        pitch = ''.join(letter for letter in note_name if letter.isalpha())
        return pitch.strip('-').strip('#').upper()

    @staticmethod
    def are_equal(nte1, nte2):
        input_notes = [nte1, nte2]
        for nte in input_notes:
            if not Note.is_note(nte):
                return False
        if nte1 == nte2:
            return True
        if not Note.is_note_instance(nte1):
            nte1 = Note(nte1)
        if not Note.is_note_instance(nte2):
            nte2 = Note(nte2)
        if nte1.number == nte2.number:
            return True
        else:
            return False

    @staticmethod
    def has_valid_octave(name):
        octave = Note.octave_from_name(name)
        if octave is False:
            return False
        if octave < config.MIN_OCTAVE \
                or octave > config.MAX_OCTAVE:
            return False
        else:
            return True

    @staticmethod
    def octave_from_number(num):
        return int((num - (num % 12))/12)

    @staticmethod
    def pitch_from_name(note_name):
        if note_name.count('#') == note_name.count('-'):
            return Note.letter_from_name(note_name)
        elif note_name.count('#') > 1 or note_name.count('-') > 1:
            note_number = Note.name_to_number(note_name)
            note_name = Note.number_to_name(note_number)
        return ''.join([i for i in note_name if not i.isdigit()]).upper()

    @staticmethod
    def pitch_from_number(note_number):
        base_pitch_class = note_number % 12
        return config.PITCHCLASS_NOTENAMES[base_pitch_class][0]

    @staticmethod
    def enharmonic_from_name(name):
        note_number = Note.name_to_number(name)
        base_note_num = note_number % 12
        note_names = config.PITCHCLASS_NOTENAMES[base_note_num]
        enharmonic = None
        for n in note_names:
            # Assumption: There can only be one enharmonic of a note
            if n != Note.strip_digits(name):  # stripping off digits (octave)
                enharmonic = n
        octave = Note.octave_from_name(name)
        if enharmonic:
            enharmonic += str(octave)
        return enharmonic

    @staticmethod
    def number_to_name(num):
        octave = Note.octave_from_number(num)
        letter = Note.pitch_from_number(num)
        return str(letter) + str(octave)

    @staticmethod
    def get_accidental(note_name):
        if not Note.is_note_name(note_name):
            raise ValueError('Expected a note name')
        if '#' in note_name:
            return '#'
        elif '-' in note_name:
            return '-'
        else:
            return None


class Rest(NoteBase):

    def __init__(self, quarter_length=1.0):
        self.number = 60  # random
        super(Rest, self).__init__(quarter_length=quarter_length)
        self.attack_velocity = 0
        self.release_velocity = 0

    def __str__(self):
        return 'Rest {}'.format(self._quarter_length)


def main():
    pass


if __name__ == '__main__':
    main()
