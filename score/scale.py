from base import ScaleException
from config import config
from note import Note, MusicObject


class ScaleBase(MusicObject):

    def __init__(self, tonic, intervals=[0, 2, 4, 5, 7, 9, 11]):
        self._tonic = None
        self._intervals = None

        super(ScaleBase, self).__init__()
        self.intervals = intervals
        self.tonic = tonic

    def __str__(self):
        return str(self.note_sequence)

    def __repr__(self):
        return str(self.note_sequence)

    def _set_head(self, head):
        self.validate_type(head, Note)
        self._tonic = head
        super(ScaleBase, self)._set_head(head)
        self._update_notes()

    def _set_tonic(self, tonic):
        if Note.is_note_name(tonic) or Note.is_note_num(tonic):
            tonic = Note(tonic)
            self._tonic = tonic
            self._set_head(tonic)
        elif Note.is_note_instance(tonic):
            self._tonic = tonic
            self._set_head(tonic)
        else:
            raise ValueError('Invalid note {}'.format(tonic))

    def _update_notes(self):
        current = self._head
        for i in self._intervals[1:]:
            current.next = Note(self._tonic.number + i)
            current = current.next

    @property
    def intervals(self):
        return self._intervals

    @intervals.setter
    def intervals(self, intervals):
        is_interval, reason = self.are_scale_intervals(intervals)
        if not is_interval:
            raise ValueError(reason)
        else:
            self._intervals = intervals
            if self._tonic:
                self._set_head(self._tonic)  # This triggers _update_notes

    @property
    def tonic(self):
        return self._tonic

    @tonic.setter
    def tonic(self, tonic):
        self._set_tonic(tonic)

    @staticmethod
    def are_scale_intervals(intervals):
        reason = ''
        if not isinstance(intervals, list):
            reason = ('{} is not a valid scale '
                      'interval. It is not a '
                      'list').format(str(intervals))
            return False, reason
        for i in intervals:
            if not isinstance(i, int):
                reason = ('{} is not a valid scale '
                          'interval. Not all its items are '
                          'integers').format(str(intervals))
                return False, reason
        if (max(intervals) - min(intervals)) > 11:
            reason = ('{} is not a valid scale '
                      'interval. Not all its notes '
                      'fall within one '
                      'octave').format(str(intervals))
            return False, reason
        if not sorted(intervals) == intervals:
            reason = ('{} is not a valid scale '
                      'interval. The items are not '
                      'in ascending order').format(str(intervals))
            return False, reason
        if not intervals[0] == 0:
            reason = ('The first note of the interval {} is not '
                      '0. It should be a 0').format(str(intervals))
            return False, reason
        return True, reason

    @classmethod
    def is_scale_type(cls, scale_type):
        if not isinstance(scale_type, basestring):
            return False
        if not cls.contains(scale_type, config.SCALE_PROPS):
            return False
        else:
            return True


class Scale(ScaleBase):

    def __init__(self, tonic, scale_type='heptatonic', intervals=None):
        self._scale_type = None
        self._num_pitches = None

        self.scale_type = scale_type
        if not intervals:
            intervals = self.default_intervals(scale_type)
        super(Scale, self).__init__(tonic, intervals=intervals)

    @ScaleBase.intervals.setter
    def intervals(self, intervals):
        if len(intervals) != self._num_pitches:
            raise ScaleException('Invalid number of pitches for given scale type')
        is_interval, reason = self.are_scale_intervals(intervals)
        if not is_interval:
            raise ScaleException(reason)
        else:
            self._intervals = intervals
            if self._tonic:
                self._set_head(self._tonic)  # This triggers _update_notes

    @staticmethod
    def default_intervals(scale_type):
        return config.SCALE_PROPS[scale_type][1]

    @property
    def num_pitches(self):
        return self._num_pitches

    @property
    def scale_type(self):
        return self._scale_type

    @scale_type.setter
    def scale_type(self, scale_type):
        if not self.is_scale_type(scale_type):
            raise ValueError('Invalid scale type {}'.format(scale_type))
        else:
            self._scale_type = scale_type
            self._num_pitches = config.SCALE_PROPS[scale_type][0]

        if hasattr(self, '_intervals'):
            if self._num_pitches != len(self._intervals):
                self._intervals = self.default_intervals(self._scale_type)


class MajorScale(Scale):

    def __init__(self, tonic):
        _intervals = [0, 2, 4, 5, 7, 9, 11]
        _scale_type = 'heptatonic'
        super(MajorScale, self).__init__(tonic, intervals=_intervals,
                                         scale_type=_scale_type)


class MinorScale(Scale):

    def __init__(self, tonic):
        _intervals = [0, 2, 3, 5, 7, 8, 10]
        _scale_type = 'heptatonic'
        super(MinorScale, self).__init__(tonic, intervals=_intervals,
                                         scale_type=_scale_type)


class DiatonicScale(object):

    def __init__(self, ionian_tonic):
        self._ionian_mode = None
        self._dorian_mode = None
        self._phrygian_mode = None
        self._lydian_mode = None
        self._mixolydian_mode = None
        self._aeolian_mode = None
        self._locrian_mode = None
        self._ionian_tonic = None

        self.ionian_tonic = ionian_tonic

    def __str__(self):
        return str(self._ionian_tonic)

    @property
    def ionian_tonic(self):
        return self._ionian_tonic

    @ionian_tonic.setter
    def ionian_tonic(self, ionian_tonic):
        self._update_modes(ionian_tonic)
        self._ionian_tonic = ionian_tonic

    def _update_modes(self, ionian_tonic):
        # degree_intervals = [2, 2, 1, 2, 2, 2, 1]
        ionian_intervals = [0, 2, 4, 5, 7, 9, 11]
        self._ionian_mode = ScaleBase(ionian_tonic,
                                      intervals=ionian_intervals)
        ionian_notes = self._ionian_mode.note_sequence

        dorian_intervals = [0, 2, 3, 5, 7, 9, 10]
        dorian_tonic = ionian_notes[1].name
        self._dorian_mode = ScaleBase(dorian_tonic,
                                      intervals=dorian_intervals)
        phrygian_intervals = [0, 1, 3, 5, 7, 8, 10]
        phrygian_tonic = ionian_notes[2].name
        self._phrygian_mode = ScaleBase(phrygian_tonic,
                                        intervals=phrygian_intervals)
        lydian_intervals = [0, 2, 4, 6, 7, 9, 11]
        lydian_tonic = ionian_notes[3].name
        self._lydian_mode = ScaleBase(lydian_tonic,
                                      intervals=lydian_intervals)
        mixolydian_intervals = [0, 2, 4, 5, 7, 9, 10]
        mixolydian_tonic = ionian_notes[4].name
        self._mixolydian_mode = ScaleBase(mixolydian_tonic,
                                          intervals=mixolydian_intervals)
        aeolian_intervals = [0, 2, 3, 5, 7, 8, 10]
        aeolian_tonic = ionian_notes[5].name
        self._aeolian_mode = ScaleBase(aeolian_tonic,
                                       intervals=aeolian_intervals)
        locrian_intervals = [0, 1, 3, 5, 6, 8, 10]
        locrian_tonic = ionian_notes[6].name
        self._locrian_mode = ScaleBase(locrian_tonic,
                                       intervals=locrian_intervals)

    @property
    def ionian_mode(self):
        return self._ionian_mode

    @property
    def dorian_mode(self):
        return self._dorian_mode

    @property
    def phrygian_mode(self):
        return self._phrygian_mode

    @property
    def lydian_mode(self):
        return self._lydian_mode

    @property
    def mixolydian_mode(self):
        return self._mixolydian_mode

    @property
    def aeolian_mode(self):
        return self._aeolian_mode

    @property
    def locrian_mode(self):
        return self._locrian_mode


class ChromaticScale(Scale):
    pass


class WholeToneScale(Scale):
    pass


def main():
    pass


if __name__ == '__main__':
    main()
