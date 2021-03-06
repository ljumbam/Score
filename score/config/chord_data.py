import collections

CHORD_TYPES = collections.OrderedDict([
    ('major',                        ['0, 4, 7',  ['',  'M',  'maj']]),
    ('minor',                        ['0, 3, 7',  ['m',  'min']]),
    ('augmented',                    ['0, 4, 8',  ['+',  'aug']]),
    ('diminished',                   ['0, 3, 6',  ['dim',  'o']]),
    ('dominant-seventh',             ['0, 4, 7, 10',  ['7',  'dom7']]),
    ('major-seventh',                ['0, 4, 7, 11',  ['maj7',  'M7']]),
    ('minor-major-seventh',          ['0, 3, 7, 11',  ['mM7',  'm#7',  'minmaj7']]),
    ('minor-seventh',                ['0, 3, 7, 10',  ['m7',  'min7']]),
    ('augmented-major seventh',      ['0, 4, 8, 11',  ['+M7',  'augmaj7']]),
    ('augmented-seventh',            ['0, 4, 8, 10',  ['7+',  '+7',  'aug7']]),
    ('half-diminished-seventh',      ['0, 3, 6, 10',  ['/o7',  'm7b5']]),
    ('diminished-seventh',           ['0, 3, 6, 9',  ['o7',  'dim7']]),
    ('seventh-flat-five',            ['0, 4, 6, 10',  ['dom7dim5']]),
    ('major-sixth',                  ['0, 4, 7, 9',  ['6']]),
    ('minor-sixth',                  ['0, 3, 7, 9',  ['m6',  'min6']]),
    ('major-ninth',                  ['0, 4, 7, 11, 14',  ['M9',  'Maj9']]),
    ('dominant-ninth',               ['0, 4, 7, 10, 14',  ['9',  'dom9']]),
    ('minor-major-ninth',            ['0, 3, 7, 11, 14',  ['mM9',  'minmaj9']]),
    ('minor-ninth',                  ['0, 3, 7, 10, 14',  ['m9',  'min9']]),
    ('augmented-major-ninth',        ['0, 4, 8, 11, 14',  ['+M9',  'augmaj9']]),
    ('augmented-dominant-ninth',     ['0, 4, 8, 10, 14',  ['9#5',  '+9',  'aug9']]),
    ('half-diminished-ninth',        ['0, 3, 6, 10, 14',  ['/o9']]),
    ('half-diminished-minor-ninth',  ['0, 3, 6, 10, 13',  ['/ob9']]),
    ('diminished-ninth',             ['0, 3, 6, 9, 14',  ['o9',  'dim9']]),
    ('diminished-minor-ninth',       ['0, 3, 6, 9, 13',  ['ob9',  'dimb9']]),
    ('dominant-11th',                ['0, 4, 7, 10, 14, 17',  ['11',  'dom11']]),
    ('major-11th',                   ['0, 4, 7, 11, 14, 17',  ['M11',  'Maj11']]),
    ('minor-major-11th',             ['0, 3, 7, 11, 14, 17',  ['mM11',  'minmaj11']]),
    ('minor-11th',                   ['0, 3, 7, 10, 14, 17',  ['m11',  'min11']]),
    ('augmented-major-11th',         ['0, 4, 8, 11, 14, 17',  ['+M11',  'augmaj11']]),
    ('augmented-11th',               ['0, 4, 8, 10, 14, 17',  ['+11',  'aug11']]),
    ('half-diminished-11th',         ['0, 3, 6, 10, 13, 17',  ['/o11']]),
    ('diminished-11th',              ['0, 3, 6, 9, 13, 16',  ['o11',  'dim11']]),
    ('major-13th',                   ['0, 4, 7, 11, 14, 17, 21',  ['M13',  'Maj13']]),
    ('dominant-13th',                ['0, 4, 7, 10, 14, 17, 21',  ['13',  'dom13']]),
    ('minor-major-13th',             ['0, 3, 7, 11, 14, 17, 21',  ['mM13',  'minmaj13']]),
    ('minor-13th',                   ['0, 3, 7, 10, 14, 17, 21',  ['m13',  'min13']]),
    ('augmented-major-13th',         ['0, 4, 8, 11, 14, 17, 21',  ['+M13',  'augmaj13']]),
    ('augmented-dominant-13th',      ['0, 4, 8, 10, 14, 17, 21',  ['+13',  'aug13']]),
    ('half-diminished-13th',         ['0, 3, 6, 10, 14, 17, 21',  ['/o13']]),
    ('suspended-second',             ['0, 2, 7',  ['sus2']]),
    ('suspended-fourth',             ['0, 5, 7',  ['sus',  'sus4']]),
    ('Neapolitan',                   ['0, 1, 4, 6',  ['N6']]),
    ('Italian',                      ['0, 6, 8',  ['It+6',  'It']]),
    ('French',                       ['0, 2, 6, 8',  ['Fr+6',  'Fr']]),
    ('German',                       ['0, 3, 6, 8',  ['Gr+6',  'Ger']]),
    ('pedal',                        ['0',  ['pedal']]),
    ('power',                        ['0, 7',  ['power']]),
    ('Tristan',                      ['0, 6, 10, 15',  ['tristan']]),
])


ROMAN_NUMERALS = {
    'ii6'     :['5, 9, 2'],
    'iio42'   :['11, 2, 5, 8'],
    'VII7'    :['11, 3, 6, 9'],
    'viio6'   :['2, 5, 11'],
    'viio7'   :['11, 2, 5, 8'],
    'V65'     :['11, 2, 5, 7'],
    'ii65'    :['5, 9, 0, 2'],
    'iio43'   :['8, 11, 2, 5'],
    'vi6'     :['0, 4, 9'],
    'V'       :['7, 11, 2'],
    'iio'     :['2, 5, 8'],
    'iii'     :['4, 7, 11'],
    '#viio6'  :['3, 6, 0'],
    'VII'     :['11, 3, 6'],
    'IV6'     :['9, 0, 5'],
    'I64'     :['7, 0, 4'],
    'IV7'     :['5, 9, 0, 4'],
    '#viio'   :['0, 3, 6'],
    'v'       :['7, 10, 2'],
    'bII6'    :['5, 8, 1'],
    '#viio65' :['3, 6, 9, 0'],
    'iio65'   :['5, 8, 11, 2'],
    'vi'      :['9, 0, 4'],
    'ii'      :['2, 5, 9'],
    'II'      :['2, 6, 9'],
    'V43'     :['2, 5, 7, 11'],
    'V42'     :['5, 7, 11, 2'],
    '#vio6'   :['1, 4, 10'],
    'I6'      :['4, 7, 0'],
    'ii42'    :['0, 2, 5, 9'],
    'ii43'    :['9, 0, 2, 5'],
    'V6'      :['11, 2, 7'],
    'V7'      :['7, 11, 2, 5'],
    'III'     :['4, 8, 11'],
    'IV65'    :['9, 0, 4, 5'],
    'I'       :['0, 4, 7'],
    'VI'      :['9, 1, 4'],
    'viio65'  :['2, 5, 8, 11'],
    '#VI'     :['10, 2, 5'],
    'IV'      :['5, 9, 0'],
    'i6'      :['3, 7, 0'],
    'i'       :['0, 3, 7'],
    'iii6'    :['7, 11, 4'],
    '#vio'    :['10, 1, 4'],
}