from note import MusicObject
from staff import Staff
from time_signature import TimeSignature


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

    @property
    def staves(self):
        return self._staves

    @property
    def genre(self):
        return self._genre

    @genre.setter
    def genre(self, genre):
        self.validate_type(genre, basestring)
        self._genre = genre

    @property
    def music_by(self):
        return self._music_by

    @music_by.setter
    def music_by(self, music_by):
        self.validate_type(music_by, basestring)
        self._music_by = music_by

    @property
    def lyrics_by(self):
        return self._lyrics_by

    @lyrics_by.setter
    def lyrics_by(self, lyrics_by):
        self.validate_type(lyrics_by, basestring)
        self._lyrics_by = lyrics_by

    @property
    def title(self):
        return self._title

    @title.setter
    def title(self, title):
        self.validate_type(title, basestring)
        self._title = title


def main():
    pass


if __name__ == '__main__':
    main()
