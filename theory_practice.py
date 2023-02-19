from typing import Dict, List
import random
import os
import toml

CONFIG_DIR = 'configs'
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

def validate_config(config_: Dict, mode_: str) -> bool:
    if mode_ == 'i':
        if 'intervals' not in config_.keys() or 'directions' not in config_.keys() or 'roots' not in config_.keys():
            raise ValueError(f'Malformed config: {config_}')
        if set(config_['intervals']) - set(INTERVALS.keys()):
            raise ValueError('Unexpected intervals found in config')
        if len(config_['intervals']) != len(config_['directions']):
            raise ValueError('Config should have same number of directions and intervals')
        if set(config_['directions']) - {'a', 'd', 'a/d'}:
            raise ValueError('Unexpected directions found in config')
        if set(config_['roots']) - set([y for x in CHROMATICS for y in x]):
            if config_['roots'] != ['naturals'] \
                and config_['roots'] != ['accidentals'] \
                and config_['roots'] != ['flats'] \
                and config_['roots'] != ['sharps'] \
                and config_['roots'] != [] \
                or len(config_['roots']) > 1: 
                raise ValueError('Unexpected roots found in config')
    elif mode_ == 'c':
        # TODO: implement chord mode config validation
        pass

def get_roots(config_: Dict) -> List[str]:
    roots_ = config_['roots']
    possible_notes_ = [y for x in CHROMATICS for y in x]

    if roots_ == []:
        return possible_notes_
    elif roots_ == ['naturals']:
        return [x for x in possible_notes_ if 'b' not in x and '#' not in x]
    elif roots_ == ['accidentals']:
        return [x for x in possible_notes_ if 'b' in x or '#' in x]
    elif roots_ == ['flats']:
        return [x for x in possible_notes_ if 'b' in x]
    elif roots_ == ['sharps']:
        return [x for x in possible_notes_ if '#' in x]
    else:
        return roots_

os.system('cls' if os.name == 'nt' else 'clear')
possible_modes = {str(idx): m for idx, m in enumerate(['intervals', 'chords'])}
mode_string = ''.join([str(idx) + ") " + m + "\n" for idx, m in possible_modes.items()])
mode = input(f'{mode_string}\nEnter mode number:')
while mode not in possible_modes.keys():
    mode = input(f'Invalid input, \n{mode_string}\nEnter mode number:')

possible_configs = {str(idx): c for idx, c in enumerate(os.listdir(CONFIG_DIR))}
choice_string = ''.join([str(idx) + ") " + c + "\n" for idx, c in possible_configs.items()])

config_num = input(f'{choice_string}\nEnter config number:')
while config_num not in possible_configs.keys():
    config_num = input(f'Invalid input, \n{choice_string}\nEnter config num:')

with open(os.path.join(CONFIG_DIR, possible_configs[config_num]), 'r') as f:
    config = toml.load(f)
    validate_config(config, mode)
    roots = get_roots(config)
    root_ids = list({idx for idx, r_list in enumerate(CHROMATICS) for note in r_list if note in roots})
    if mode == '0':
        interval_directions = {ivl: dctn for ivl, dctn in zip(config['intervals'], config['directions'])}

quit = False
correct = 0
total = 0
os.system('cls' if os.name == 'nt' else 'clear')
while not quit:
    if mode == '0':
        root_id = random.choice(root_ids)
        root = random.choice([x for x in CHROMATICS[root_id] if x in roots])
        interval = random.choice(config['intervals'])
        possible_directions = interval_directions[interval].split('/')
        direction = random.choice(possible_directions)
        if direction == 'a':
            ans = CHROMATICS[(root_id + INTERVALS[interval]) % len(CHROMATICS)]
        else:
            ans = CHROMATICS[(root_id - INTERVALS[interval])]

        guess = input(f'Root: {root} \nInterval: {interval}\nDirection: {"Ascending" if direction == "a" else "Descending"}\n')
        if guess in ans:
            print('Correct!\n')
            if len(ans) > 1:
                print(f'Also correct: {[x for x in ans if x != guess]}')
            correct += 1
        else:
            print(f'Wrong!\nCorrect answers were: {ans}')

        inp = input('hit enter to continue \n')
        if inp not in {''}:
            quit = True

        os.system('cls' if os.name == 'nt' else 'clear')

    elif mode == '1':
        print('chord mode not implemented')
        quit = True

    total += 1

print(f'Final Score: {100*(correct / total)}% correct')
