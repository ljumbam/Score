import logging.config

from score.base import StaffException
from score.chord import Chord
from score.config import config
from score.instrument import Instrument
from score.note import MusicObject, NoteBase, Note, Message, Rest
from score.time_signature import TimeSignature

logging.config.dictConfig(config.LOGGING_CONFIG)


class Clef(MusicObject):

    def __init__(self, name='Treble'):
        self._quarter_lengths = []
        self._name = None

        self.name = name
        super(Clef, self).__init__()

    def __str__(self):
        return 'Clef: {} - Instrument: {}'.format(self._name, self._instrument)

    def __repr__(self):
        return 'Clef: {} - Instrument: {}'.format(self._name, self._instrument)

    def add_note(self, note, quarter_length=None, inherit=True):
        if not isinstance(note, (NoteBase, Chord)):
            if isinstance(note, list):
                note = Chord(note)
            else:
                note = Note(note)
        if inherit:
            note.inherit(self)
        if quarter_length is not None:
            note.quarter_length = quarter_length
        self.update_neighbors(note)
        self._quarter_lengths.append(note.quarter_length)

    def add_message(self, message):
        self.validate_type(message, Message)
        self.update_neighbors(message)

    def update_neighbors(self, obj):
        if obj.prev or obj.next:
            logging.warning('The current note/chord/message is already in use. '
                            'Adding it will break it\'s previous use case')
        if not self.head:
            self._set_head(obj)
        else:
            self._current.next = obj
            self._current = obj

    def round_up(self, quarter_length):
        current_tql = self.total_quarter_length
        if current_tql > quarter_length:
            logging.info('The quarter length to round up to, {}, is less than the '
                         'current total quarter length, {}, of the clef. No change will '
                         'result from this method'.format(quarter_length, current_tql))
        else:
            available_length = quarter_length - current_tql
            if available_length > 0:
                self.add_note(Rest(), quarter_length=available_length)

    @MusicObject.instrument.setter
    def instrument(self, instrument):
        if not isinstance(instrument, Instrument):
            self._instrument = Instrument(name=instrument)
        else:
            self._instrument = instrument
        if self._instrument.is_percussion and self._name is not 'Percussion':
            logging.warning('Updating clef to a percussion clef')
            self.name = 'Percussion'
            if self._parent:
                self._parent.name = 'PercussionStaff'

    @property
    def name(self):
        return self._name

    @name.setter
    def name(self, name):
        if not self.contains(name, ['Percussion', 'Treble', 'Bass']):
            raise ValueError('Invalid clef name')
        self._name = name

    @property
    def unique_quarter_lengths(self):
        return list(set(self._quarter_lengths))

    @property
    def parent(self):
        return self._parent

    @parent.setter
    def parent(self, parent):
        self.validate_type(parent, Staff)
        self._parent = parent


class Staff(MusicObject):

    def __init__(self, name='TrebleStaff', time_signature=TimeSignature('4/4')):

        self._name = None
        self._clefs = None

        self.name = name
        super(Staff, self).__init__(time_signature=time_signature)

    def __str__(self):
        return '{} {}'.format(self._name, self._time_signature)

    def __repr__(self):
        return '{} {}'.format(self._name, self._time_signature)

    def round_up(self, quarter_length=None):
        longest_quarter_length = 0
        for clf in self.clefs:
            tql = clf.total_quarter_length
            if tql > longest_quarter_length:
                longest_quarter_length = tql
        round_to_ql = quarter_length or longest_quarter_length
        for c in self.clefs:
            c.round_up(round_to_ql)

    def _set_clefs(self):
        if self._name == 'TrebleStaff':
            self._clefs = [Clef()]
        elif self._name == 'BassStaff':
            self._clefs = [Clef('Bass')]
        elif self._name == 'PercussionStaff':
            self._clefs = [Clef('Percussion')]
        elif self._name == 'GreatStaff':
            self._clefs = [Clef(), Clef('Bass')]
        else:
            raise StaffException('Invalid staff name')
        for c in self._clefs:
            c.parent = self

    @MusicObject.instrument.setter
    def instrument(self, instrument):
        if not isinstance(instrument, Instrument):
            self._instrument = Instrument(name=instrument)
        else:
            self._instrument = instrument

        for clef in self._clefs:
            clef.instrument = instrument

    @property
    def clefs(self):
        return self._clefs

    @property
    def name(self):
        return self._name

    @name.setter
    def name(self, name):
        if not self.contains(name, ['GreatStaff', 'GrandStaff',
                                    'TrebleStaff', 'BassStaff',
                                    'PercussionStaff']):
            raise StaffException('Invalid staff name')
        self._name = name
        self._set_clefs()


def main():
    pass


if __name__ == '__main__':
    main()
