import itertools
import math
from fractions import Fraction
from functools import reduce

from mido import MidiFile, MidiTrack, MetaMessage, Message, bpm2tempo


def gcd(*numbers):
    from math import gcd
    return reduce(gcd, numbers)


def lcm(*numbers):
    def lcm(a, b):
        return (a * b) // gcd(a, b)
    return reduce(lcm, numbers, 1)


class Midi(MidiFile):

    def __init__(self, score):
        self._score = None
        super(Midi, self).__init__()
        self._set_score(score)

    def save(self, filename):
        self._score_to_midi()
        super(Midi, self).save(filename)

    def create_track_if_none(self, index=0):
        difference = index + 1 - len(self.tracks)
        if difference:
            for i in range(0, difference):
                self.tracks.append(MidiTrack())

    def add_staff(self, staff, initial_track_index=None):
        if initial_track_index is None:
            initial_track_index = len(self.tracks) # 0 if len(self.tracks) == 0 else len(self.tracks)
        for i in range(0, len(staff.clefs)):
            clef = staff.clefs[i]
            track_index = i + initial_track_index
            channel = self.correct_channel_number(track_index, clef.instrument)
            self.add_clef(clef, track_index, channel)

    def add_clef(self, clef, track_index, channel):
        self.create_track_if_none(track_index)
        channel = self.correct_channel_number(channel, clef.instrument)
        self.change_instrument_message(clef.instrument, self.tracks[track_index], channel=channel)
        current = clef.head
        if current:
            self.add_obj(current, track_index=track_index, channel=channel)
            while current.next:
                self.add_obj(current.next, track_index=track_index,
                             channel=channel)
                current = current.next

    def add_message(self, message, track_index=0):
        mido_msg = ['note_off', 'note_on', 'polytouch', 'control_change',
                    'program_change', 'aftertouch', 'pitchwheel', 'sysex',
                    'quarter_frame', 'songpos', 'song_select', 'tune_request',
                    'clock', 'start', 'continue', 'stop', 'active_sensing',
                    'reset']
        self.create_track_if_none(track_index)
        if message.type in mido_msg:
            self.tracks[track_index].append(Message(message.type,
                                                    **message.parameters))
        else:
            self.tracks[track_index].append(MetaMessage(message.type,
                                                        **message.parameters))

    def add_obj(self, obj, track_index=0, channel=0):
        self.create_track_if_none(track_index)
        if type(obj).__name__ in ['Chord', 'RomanNumeral', 'PopularChord']:
            self.add_chord(obj, track_index=track_index, channel=channel)
        elif type(obj).__name__ in ['Note', 'Rest']:
            self.add_note(obj, track_index=track_index, channel=channel)
        else:
            self.add_message(obj, track_index=track_index)

    def add_note(self, note, track_index=0, channel=0):
        self.create_track_if_none(track_index)
        time = int(note.quarter_length * self.ticks_per_beat)
        score_lyric = note.lyric
        if score_lyric:
            lyric = MetaMessage('lyrics', text=score_lyric)
            self.tracks[track_index].append(lyric)
        note_on = Message('note_on', channel=channel, note=note.number,
                          velocity=note.attack_velocity)
        note_off = Message('note_off', channel=channel, note=note.number,
                           velocity=note.release_velocity, time=time)

        self.tracks[track_index].append(note_on)
        self.tracks[track_index].append(note_off)

    def add_chord(self, chord, track_index=0, channel=0):
        self.create_track_if_none(track_index)
        score_lyric = chord.lyric
        if score_lyric:
            lyric = MetaMessage('lyrics', text=score_lyric)
            self.tracks[track_index].append(lyric)

        for i in range(0, len(chord.notes)):
            note = chord.notes[i]
            self.tracks[track_index].append(Message('note_on', channel=channel,
                                                    note=note.number,
                                                    velocity=note.attack_velocity))

        for i in range(0, len(chord.notes)):
            note = chord.notes[i]
            time = int(note.quarter_length * self.ticks_per_beat) if i == 0 else 0
            self.tracks[track_index].append(Message('note_off', channel=channel,
                                                    note=note.number, time=time,
                                                    velocity=note.release_velocity))

    def _score_to_midi(self):
        self.tracks = []
        first_track = MidiTrack()
        score = self._score
        if hasattr(score, 'copyright'):
            self.add_copyright(score.copyright, first_track)
        if hasattr(score, 'time_signature'):
            self.add_time_signature_message(score.time_signature, first_track)
        if hasattr(score, 'key_signature'):
            key = self.scorekey_to_midokey(score.key_signature)
            self.add_key_signature_message(key, first_track)
        if hasattr(score, 'instrument'):
            self.set_track_instrument(score.instrument, first_track)
            self.change_instrument_message(score.instrument, first_track)
            self.add_track_name(score.instrument.name, first_track)
        if hasattr(score, 'tempo'):
            self.add_tempo(score.tempo, first_track)
        self.tracks.append(first_track)

    def _set_score(self, score):
        self._score = score

    @staticmethod
    def add_tempo(tempo, track):
        midi_tempo = int(bpm2tempo(tempo))
        track.append(MetaMessage('set_tempo', tempo=midi_tempo))

    @staticmethod
    def add_copyright(copyright, track):
        track.append(MetaMessage('copyright', text=copyright))

    @staticmethod
    def add_track_name(name, track):
        track.append(MetaMessage('track_name', name=name))

    @staticmethod
    def add_time_signature_message(score_ts, track):
        ts = MetaMessage('time_signature', numerator=score_ts.numerator,
                         denominator=score_ts.denominator)
        track.append(ts)

    @staticmethod
    def set_track_instrument(score_instr, track):
        track.append(MetaMessage('instrument_name', name=score_instr.name))

    @staticmethod
    def add_key_signature_message(key, track):
        track.appen(MetaMessage('key_signature', key=key))

    @staticmethod
    def correct_channel_number(number, instrument):
        if instrument.is_percussion:
            return 9
        elif number not in range(0, 16):
            return 15
        else:
            return number

    @staticmethod
    def scorekey_to_midokey(key_signature):
        mido_key = '{}{}{}'
        accidental = ''
        mode = ''
        tonic_name = key_signature.scale.notes[0].name
        if '#' in tonic_name:
            accidental = '#'
        elif '-' in tonic_name:
            accidental = 'b'
        key_letter = key_signature.scale.notes[0].letter_from_name(tonic_name)
        if key_signature.key.mode_type == 'minor':
            mode = 'm'
        return mido_key.format(key_letter, accidental, mode)

    @staticmethod
    def best_ticks_per_beat(*note_lengths):
        denominators = []
        for length in note_lengths:
            length = math.modf(length)[0]
            denominators.append(Fraction(length).limit_denominator().denominator)
        min_tpb = 96
        tpb = min_tpb
        if len(denominators) > 0:
            for i in itertools.count():
                tpb = gcd(*tuple(denominators)) * max(denominators) * i
                if tpb >= min_tpb:
                    break
        return tpb

    @classmethod
    def change_instrument_message(cls, score_instr, track, channel=0):
        channel = cls.correct_channel_number(channel, score_instr)
        instrument = Message('program_change', channel=channel,
                             program=score_instr.number)
        track.append(instrument)

    @property
    def score(self):
        return self._score


class MidiMusicObject(Midi):
    pass


class MidiMessage(Midi):

    def _score_to_midi(self):
        super(MidiMessage, self)._score_to_midi()
        message = self._score
        self.add_message(message, track_index=0)
        end = MetaMessage('end_of_track')
        self.tracks[0].append(end)


class MidiNoteBase(Midi):
    pass


class MidiNote(MidiNoteBase):

    def _score_to_midi(self):
        super(MidiNote, self)._score_to_midi()
        note = self._score
        self.ticks_per_beat = self.best_ticks_per_beat(note.quarter_length)
        self.add_note(note, track_index=0, channel=0)
        end = MetaMessage('end_of_track')
        self.tracks[0].append(end)


class MidiRest(MidiNote):

    def _score_to_midi(self):
        super(MidiRest, self)._score_to_midi()


class MidiChord(Midi):

    def _score_to_midi(self):
        super(MidiChord, self)._score_to_midi()
        chord = self._score
        quarter_lengths = [ql.quarter_length for ql in chord.notes]
        self.ticks_per_beat = self.best_ticks_per_beat(*quarter_lengths)
        self.add_chord(chord, track_index=0, channel=0)
        end = MetaMessage('end_of_track')
        self.tracks[0].append(end)


class MidiPopularChord(MidiChord):
    pass


class MidiRomanNumeral(MidiChord):
    pass


class MidiScaleBase(Midi):

    def _score_to_midi(self):
        super(MidiScaleBase, self)._score_to_midi()
        scale = self._score
        quarter_lengths = [ql.quarter_length for ql in scale.note_sequence]
        self.ticks_per_beat = self.best_ticks_per_beat(*quarter_lengths)
        for note in scale.note_sequence:
            self.add_note(note, track_index=0, channel=0)


class MidiScale(MidiScaleBase):
    pass


class MidiMajorScale(MidiScaleBase):
    pass


class MidiMinorScale(MidiScaleBase):
    pass


class MidiDiatonicScale(Midi):

    def save(self):
        raise NotImplementedError

    def _score_to_midi(self):
        raise NotImplemented


class MidiClef(Midi):

    def _score_to_midi(self):
        super(MidiClef, self)._score_to_midi()
        clef = self._score
        quarter_lengths = clef.unique_quarter_lengths
        self.ticks_per_beat = self.best_ticks_per_beat(*quarter_lengths)
        self.add_clef(clef, track_index=0, channel=0)


class MidiStaff(Midi):

    def _score_to_midi(self):
        super(MidiStaff, self)._score_to_midi()
        staff = self._score
        quarter_lengths = []
        for clef in staff.clefs:
            quarter_lengths += clef.unique_quarter_lengths
        self.ticks_per_beat = self.best_ticks_per_beat(*quarter_lengths)
        self.add_staff(staff, initial_track_index=0)


class MidiScore(Midi):

    def _score_to_midi(self):
        super(MidiScore, self)._score_to_midi()
        score = self._score
        quarter_lengths = []
        for staff in score.staves:
            for clef in staff.clefs:
                quarter_lengths += clef.unique_quarter_lengths
        self.ticks_per_beat = self.best_ticks_per_beat(*quarter_lengths)

        for staff in score.staves:
            self.add_staff(staff, initial_track_index=len(self.tracks))


class MidiFactory(object):

    @staticmethod
    def get_class(class_name):
        parts = class_name.split('.')
        module = '.'.join(parts[:-1])
        m = __import__(module)
        for comp in parts[1:]:
            m = getattr(m, comp)
        return m

    @staticmethod
    def create_midi(score_obj):
        class_name = type(score_obj).__name__
        try:
            midi = MidiFactory.get_class('midi.Midi{}'.format(class_name))
        except:
            midi = MidiFactory.get_class('score.midi.Midi{}'.format(class_name))
        return midi(score_obj)


def main():
    pass


if __name__ == '__main__':
    main()
