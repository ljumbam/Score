import itertools
import logging

DEBUG = True

# max and min notes by MIDI standards
MIN_NOTE_NUM = 0
MAX_NOTE_NUM = 127

MIN_VOL_NUM = 0
MAX_VOL_NUM = 127

MIN_VEL_NUM = 0
MAX_VEL_NUM = 127
AVE_ATTACK_VEL = 75
AVE_RELEASE_VEL = 64

MIN_TEMPO_NUM = 0
MAX_TEMPO_NUM = 1000

MIN_OCTAVE = 0
MAX_OCTAVE = 10

KEY_NAMES = [  # all major and minor keys
    'A',  'B',  'C',  'D',  'E',  'F',  'G',
    'a',  'b',  'c',  'd',  'e',  'f',  'g',
    'A#', 'B#', 'C#', 'D#', 'E#', 'F#', 'G#',  # NB: E# nor B# exists
    'a#', 'b#', 'c#', 'd#', 'e#', 'f#', 'g#',  # NB: e# nor b# exists
    'A-', 'B-', 'C-', 'D-', 'E-', 'F-', 'G-',  # NB: F- nor C- exists
    'a-', 'b-', 'c-', 'd-', 'e-', 'f-', 'g-'   # NB: f- nor c- exists
]

PITCHCLASS_NOTENAMES = {
    0: ['C',  'B#'],  # NB: B# doesn't exist
    1: ['D-', 'C#'],
    2: ['D'],
    3: ['E-', 'D#'],
    4: ['E',  'F-'],  # NB: F- doesn't exist
    5: ['F',  'E#'],  # NB: E# doesn't exist
    6: ['F#', 'G-'],
    7: ['G'],
    8: ['A-', 'G#'],
    9: ['A'],
    10: ['B-', 'A#'],
    11: ['B',  'C-']  # NB: C- doesn't exist
}

NATURAL_NOTENAMES = [PITCHCLASS_NOTENAMES[x][0] for x in PITCHCLASS_NOTENAMES]

NOTENAMES_PITCHCLASS = {
    'C' : 0,
    'B#': 0,
    'C#': 1,
    'D-': 1,
    'D' : 2,
    'D#': 3,
    'E-': 3,
    'E' : 4,
    'F-': 4,
    'F' : 5,
    'E#': 5,
    'F#': 6,
    'G-': 6,
    'G' : 7,
    'G#': 8,
    'A-': 8,
    'A' : 9,
    'A#': 10,
    'B-': 10,
    'B' : 11,
    'C-': 11
}

NOTE_NAMES = list(itertools.chain(
                *[i for i in PITCHCLASS_NOTENAMES.values()])
            )

MUSIC_LETTERS = ['A', 'B', 'C', 'D', 'E', 'F', 'G']

SYMBOLS = ['tie', 'slur', 'legato', 'staccato', 'phrase']

SCALE_PROPS = {
    # scale type    num notes  default intervals
    'tritonic': (3,  [0, 2, 3]),  # arbitrary. Example is from wikipedia
    'tetratonic': (4,  [0, 3, 5, 7]),  # arbitrary. Most common example from online
    'pentatonic': (5,  [0, 2, 4, 7, 9]),  # major pentatonic scale
    'hexatonic': (6,  [0, 2, 4, 6, 8, 10]),  # arbitrary. Whole tone scale example from wikipedia
    'heptatonic': (7,  [0, 2, 4, 5, 7, 9, 11]),  # major scale
    'octatonic': (8,  [0, 2, 3, 5, 6, 8, 9, 11]),  # alternating whole and half tones (as example in wikipedia)
    'nonatonic': (9,  [0, 2, 3, 4, 5, 6, 7, 9, 10]),  # minor nonatonic scale
    'dodecatonic': (12, [0, 1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11])  # 12 notes chromatic scale
}

LOGGING_CONFIG = dict(
    version = 1,
    formatters = {
        'fmt': {'format': '%(asctime)s %(name)-12s %(levelname)-8s %(message)s'}
    },
    handlers = {
        'stream': {
            'class': 'logging.StreamHandler',
            'formatter': 'fmt',
            'level': logging.DEBUG
        },
    },
    loggers = {
        '': {
            'handlers': ['stream'],
            'level': logging.DEBUG if DEBUG else logging.WARNING
        }
    }
)
