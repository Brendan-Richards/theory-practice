from enum import Enum


class TheoryMode(Enum):
    INTERVALS = 'Intervals'
    CHORD_SPELLING = 'Chord Spelling'
    GUITAR_TRIADS = 'Guitar Triads'

CONFIG_DIRS = {
    TheoryMode.INTERVALS: 'configs/intervals',
    TheoryMode.CHORD_SPELLING: 'configs/chord_spelling',
    TheoryMode.GUITAR_TRIADS: 'configs/triads'
}

CHROMATICS = [['A'], ['A#', 'Bb'], ['B'], ['C'], ['C#', 'Db'], ['D'], ['D#', 'Eb'], ['E'], ['F'], ['F#', 'Gb'], ['G'], ['G#', 'Ab']]
INTERVALS = {
    'm2': 1,
    'M2': 2,
    'm3': 3,
    'M3': 4,
    'P4': 5,
    'Tritone': 6,
    'P5': 7,
    'm6': 8,
    'M6': 9,
    'm7': 10,
    'M7': 11
}
