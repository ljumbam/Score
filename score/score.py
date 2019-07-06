from score.base import ScoreException
from score.note import MusicObject
from score.staff import Staff
from score.time_signature import TimeSignature


class Score(MusicObject):

    def __init__(self, time_signature=TimeSignature('4/4')):
        self._title = 'Untitled'
        self._lyrics_by = 'Unknown'
        self._music_by = 'Uknown'
        self._genre = 'Pop'
        self._staves = []
        super(Score, self).__init__(time_signature=time_signature)

    def add_staff(self, staff, position=None, inherit=True):
        position = position or len(self._staves)
        self.validate_type(position, int)
        self.validate_type(staff, Staff)
        if inherit:
            staff.inherit(self)
        self._staves.insert(position, staff)

    def has_instrument(self, number, is_percussion=False):
        for staff in self.staves:
            if staff.instrument.number == number and \
                    staff.instrument.is_percussion == is_percussion:
                return True
        return False

    def round_up(self, quarter_length=None):
        longest_quater_length = 0
        for staff in self.staves:
            staff.round_up(quarter_length=quarter_length)
            tql = staff.clefs[0].total_quarter_length
            if longest_quater_length < tql:
                longest_quater_length = tql
        for staff in self.staves:
            staff.round_up(quarter_length=longest_quater_length)

    def merge(self, score):
        self.validate_type(score, Score)
        self.round_up()
        score.round_up()

        if len(self.staves) != len(score.staves):
            raise ScoreException('Cannot merge two scores with '
                                 'different number of staves.')
        for i in range(0, len(self.staves)):
            if self.staves[i].name != score.staves[i].name:
                raise ScoreException('Encountered mismatching staves '
                                     'while attempted to merge scores.')

        for i in range(0, len(self.staves)):
            stf = self.staves[i]
            for j in range(0, len(stf.clefs)):
                clf = stf.clefs[j]
                if len(score.staves[i].clefs[j].note_sequence) > 0:
                    nte = score.staves[i].clefs[j].note_sequence[0]
                    if len(clf.note_sequence) > 0:
                        clf.note_sequence[-1].next = nte

    @property
    def staves(self):
        return self._staves

    @property
    def genre(self):
        return self._genre

    @genre.setter
    def genre(self, genre):
        self.validate_type(genre, str)
        self._genre = genre

    @property
    def music_by(self):
        return self._music_by

    @music_by.setter
    def music_by(self, music_by):
        self.validate_type(music_by, str)
        self._music_by = music_by

    @property
    def lyrics_by(self):
        return self._lyrics_by

    @lyrics_by.setter
    def lyrics_by(self, lyrics_by):
        self.validate_type(lyrics_by, str)
        self._lyrics_by = lyrics_by

    @property
    def title(self):
        return self._title

    @title.setter
    def title(self, title):
        self.validate_type(title, str)
        self._title = title


def main():
    pass


if __name__ == '__main__':
    main()
