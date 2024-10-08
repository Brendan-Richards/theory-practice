THEORY_MODES = ["intervals", "chord_spelling", "guitar_triads"]

CHROMATICS = [
    ["A"],
    ["A#", "Bb"],
    ["B"],
    ["C"],
    ["C#", "Db"],
    ["D"],
    ["D#", "Eb"],
    ["E"],
    ["F"],
    ["F#", "Gb"],
    ["G"],
    ["G#", "Ab"],
]

INTERVALS = {
    "m2": 1,
    "M2": 2,
    "m3": 3,
    "M3": 4,
    "P4": 5,
    "Tritone": 6,
    "P5": 7,
    "m6": 8,
    "M6": 9,
    "m7": 10,
    "M7": 11,
}

TRIAD_FORMULAS = {
    # minor chords
    "m_e_0": [(0, 0), (1, 2), (2, 3)],
    "m_a_0": [(0, 0), (1, 2), (2, 3)],
    "m_d_0": [(0, 0), (1, 2), (2, 2)],
    "m_g_0": [(0, 0), (1, 1), (2, 2)],
    "m_e_1": [(0, 0), (1, 1), (2, 1)],
    "m_a_1": [(0, 0), (1, 1), (2, 1)],
    "m_d_1": [(0, 0), (1, 1), (2, 0)],
    "m_g_1": [(0, 0), (1, 0), (2, 0)],
    "m_e_2": [(0, 0), (1, 0), (2, 2)],
    "m_a_2": [(0, 0), (1, 0), (2, 2)],
    "m_d_2": [(0, 0), (1, 0), (2, 1)],
    "m_g_2": [(0, 0), (1, -1), (2, 1)],
    # major chords
    "M_e_0": [(0, 0), (1, 1), (2, 3)],
    "M_a_0": [(0, 0), (1, 1), (2, 3)],
    "M_d_0": [(0, 0), (1, 1), (2, 2)],
    "M_g_0": [(0, 0), (1, 0), (2, 2)],
    "M_e_1": [(0, 0), (1, 2), (2, 2)],
    "M_a_1": [(0, 0), (1, 2), (2, 2)],
    "M_d_1": [(0, 0), (1, 2), (2, 1)],
    "M_g_1": [(0, 0), (1, 1), (2, 1)],
    "M_e_2": [(0, 0), (1, 0), (2, 1)],
    "M_a_2": [(0, 0), (1, 0), (2, 1)],
    "M_d_2": [(0, 0), (1, 0), (2, 0)],
    "M_g_2": [(0, 0), (1, -1), (2, 0)],
    # diminished chords
    "dim_e_0": [(0, 0), (1, 2), (2, 4)],
    "dim_a_0": [(0, 0), (1, 2), (2, 4)],
    "dim_d_0": [(0, 0), (1, 2), (2, 3)],
    "dim_g_0": [(0, 0), (1, 1), (2, 3)],
    "dim_e_1": [(0, 0), (1, 2), (2, 1)],
    "dim_a_1": [(0, 0), (1, 2), (2, 1)],
    "dim_d_1": [(0, 0), (1, 2), (2, 0)],
    "dim_g_1": [(0, 0), (1, 1), (2, 0)],
    "dim_e_2": [(0, 0), (1, -1), (2, 1)],
    "dim_a_2": [(0, 0), (1, -1), (2, 1)],
    "dim_d_2": [(0, 0), (1, -1), (2, 0)],
    "dim_g_2": [(0, 0), (1, -2), (2, 0)],
    # augmented chords
    "aug_e_0": [(0, 0), (1, 1), (2, 2)],
    "aug_a_0": [(0, 0), (1, 1), (2, 2)],
    "aug_d_0": [(0, 0), (1, 1), (2, 1)],
    "aug_g_0": [(0, 0), (1, 0), (2, 1)],
    "aug_e_1": [(0, 0), (1, 1), (2, 2)],
    "aug_a_1": [(0, 0), (1, 1), (2, 2)],
    "aug_d_1": [(0, 0), (1, 1), (2, 1)],
    "aug_g_1": [(0, 0), (1, 0), (2, 1)],
    "aug_e_2": [(0, 0), (1, 1), (2, 2)],
    "aug_a_2": [(0, 0), (1, 1), (2, 2)],
    "aug_d_2": [(0, 0), (1, 1), (2, 1)],
    "aug_g_2": [(0, 0), (1, 0), (2, 1)],
}
