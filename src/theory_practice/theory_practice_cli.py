from typing import Dict, List
import random
import os
import toml

from constants import CHROMATICS, INTERVALS, CONFIG_DIRS, THEORY_MODES, TRIAD_FORMULAS


class TheoryTeacher:
    def __init__(self):
        self.mode = self.get_theory_mode()
        self.config = self.get_config()
        self.roots = self.get_roots()
        self.root_ids = list(
            {
                idx
                for idx, r_list in enumerate(CHROMATICS)
                for note in r_list
                if note in self.roots
            }
        )
        if self.mode == "Intervals":
            self.interval_directions = {
                ivl: dctn
                for ivl, dctn in zip(
                    self.config["intervals"], self.config["directions"]
                )
            }

    def get_theory_mode(self):
        os.system("cls" if os.name == "nt" else "clear")
        indexed_modes = {
            str(idx): theory_mode for idx, theory_mode in enumerate(THEORY_MODES)
        }
        mode_display_string = "".join(
            [str(idx) + ") " + m + "\n" for idx, m in indexed_modes.items()]
        )

        mode_idx = input(f"{mode_display_string}\nEnter mode number:")
        while mode_idx not in indexed_modes.keys():
            mode_idx = input(
                f"Invalid input, \n{mode_display_string}\nEnter mode number:"
            )

        return indexed_modes[mode_idx]

    def get_config(self):
        possible_configs = {
            str(idx): c for idx, c in enumerate(os.listdir(CONFIG_DIRS[self.mode]))
        }
        if len(possible_configs) == 0:
            raise ValueError(f"No configs available for mode: {self.mode}")

        choice_string = "".join(
            [str(idx) + ") " + c + "\n" for idx, c in possible_configs.items()]
        )

        config_num = input(f"\n{choice_string}\nEnter config number:")
        while config_num not in possible_configs.keys():
            config_num = input(f"Invalid input, \n{choice_string}\nEnter config num:")

        with open(
            os.path.join(CONFIG_DIRS[self.mode], possible_configs[config_num]), "r"
        ) as f:
            config = toml.load(f)
            config = self.validate_config(config)
        return config

    def validate_config(self, config: Dict) -> bool:
        if self.mode == "Intervals":
            if (
                "intervals" not in config.keys()
                or "directions" not in config.keys()
                or "roots" not in config.keys()
            ):
                raise ValueError(f"Malformed config: {config}")
            if set(config["intervals"]) - set(INTERVALS.keys()):
                raise ValueError("Unexpected intervals found in config")
            if len(config["intervals"]) != len(config["directions"]):
                raise ValueError(
                    "Config should have same number of directions and intervals"
                )
            if set(config["directions"]) - {"a", "d", "a/d"}:
                raise ValueError("Unexpected directions found in config")
            if set(config["roots"]) - set([y for x in CHROMATICS for y in x]):
                if (
                    config["roots"] != ["naturals"]
                    and config["roots"] != ["accidentals"]
                    and config["roots"] != ["flats"]
                    and config["roots"] != ["sharps"]
                    and config["roots"] != []
                    or len(config["roots"]) > 1
                ):
                    raise ValueError("Unexpected roots found in config")
        elif self.mode == "Chord Spelling":
            # TODO: implement chord mode config validation
            pass
        elif self.mode == "Guitar Triads":
            expected_options = {"low_strings", "roots", "chord_types", "inversions"}
            if not set(config.keys()) == expected_options:
                raise ValueError(
                    f"Expected config to have the following options only: {expected_options}"
                )
            if set(config["low_strings"]) - {"e", "a", "d", "g"}:
                raise ValueError("Unexpected low strings found in config")
            if set(config["roots"]) - set([y for x in CHROMATICS for y in x]):
                if (
                    config["roots"] != ["naturals"]
                    and config["roots"] != ["accidentals"]
                    and config["roots"] != ["flats"]
                    and config["roots"] != ["sharps"]
                    and config["roots"] != []
                    or len(config["roots"]) > 1
                ):
                    raise ValueError("Unexpected roots found in config")
            if set(config["chord_types"]) - {"m", "M", "dim", "aug"}:
                raise ValueError("Unexpected chord types found in config")
            if set(config["inversions"]) - {0, 1, 2}:
                raise ValueError("Unexpected inversions found in config")

        return config

    def get_roots(self) -> List[str]:
        roots = self.config["roots"]
        possible_notes = [y for x in CHROMATICS for y in x]

        if roots == []:
            return possible_notes
        elif roots == ["naturals"]:
            return [x for x in possible_notes if "b" not in x and "#" not in x]
        elif roots == ["accidentals"]:
            return [x for x in possible_notes if "b" in x or "#" in x]
        elif roots == ["flats"]:
            return [x for x in possible_notes if "b" in x]
        elif roots == ["sharps"]:
            return [x for x in possible_notes if "#" in x]
        else:
            return roots

    def get_chord_tab(
        self, low_string: str, inversion: int, chord_type: str, root_idx: int
    ) -> str:
        formula = TRIAD_FORMULAS[f"{chord_type}_{low_string}_{inversion}"]

        if inversion == 0:
            lowest_note = CHROMATICS[root_idx][0]
        elif inversion == 1:
            if chord_type in ["m", "dim"]:
                lowest_note = CHROMATICS[(root_idx + 3) % 12][0]
            elif chord_type in ["M", "aug"]:
                lowest_note = CHROMATICS[(root_idx + 4) % 12][0]
        elif inversion == 2:
            lowest_note = CHROMATICS[(root_idx + 7) % 12][0]
        else:
            raise ValueError(f"Inversion num: {inversion} not supported!")
        starting_fret_num = self.distance(low_string.upper(), lowest_note.upper())

        # if any chord note would put us into negative frets, just transpose the whole chord up an octave
        for point in formula:
            if starting_fret_num - point[1] < 0:
                starting_fret_num += 12
                break

        string_chunks = []
        point = 0
        for string in ["E", "A", "D", "G", "B", "E"]:
            if string == low_string.upper() and point < len(formula):
                string_chunks.append(f"{string} -{starting_fret_num}-\n")
                point = 1
            elif point == 0 or point >= len(formula):
                string_chunks.append(f"{string} ---\n")
            else:
                y = formula[point][1]
                string_chunks.append(f"{string} -{starting_fret_num - y}-\n")
                point += 1

        string_chunks = string_chunks[::-1]
        chord_tab = "".join(string_chunks)
        return chord_tab

    def distance(self, n1: str, n2: str) -> int:
        idx1 = [
            i
            for i, note_list in enumerate(CHROMATICS)
            for note in note_list
            if note == n1
        ][0]

        for i in range(idx1, idx1 + 12):
            for note in CHROMATICS[i % 12]:
                if note == n2:
                    return i - idx1

    def run_cli(self):
        quit = False
        correct = 0
        total = 0
        os.system("cls" if os.name == "nt" else "clear")
        while not quit:
            if self.mode == "Intervals":
                root_id = random.choice(self.root_ids)
                root = random.choice(
                    [x for x in CHROMATICS[root_id] if x in self.roots]
                )
                interval = random.choice(self.config["intervals"])
                possible_directions = self.interval_directions[interval].split("/")
                direction = random.choice(possible_directions)
                if direction == "a":
                    ans = CHROMATICS[(root_id + INTERVALS[interval]) % len(CHROMATICS)]
                else:
                    ans = CHROMATICS[(root_id - INTERVALS[interval])]

                guess = input(
                    f'Root: {root} \nInterval: {interval}\nDirection: {"Ascending" if direction == "a" else "Descending"}\n'
                )
                if guess in ans:
                    print("Correct!\n")
                    if len(ans) > 1:
                        print(f"Also correct: {[x for x in ans if x != guess]}")
                    correct += 1
                else:
                    print(f"Wrong!\nCorrect answers were: {ans}")

                inp = input("hit enter to continue \n")
                if inp not in {""}:
                    quit = True

                os.system("cls" if os.name == "nt" else "clear")

            elif self.mode == "Chord Spelling":
                raise NotImplementedError(f"theory mode: {self.mode} not implemented!")

            elif self.mode == "Guitar Triads":
                root_id = random.choice(self.root_ids)
                root = random.choice(
                    [x for x in CHROMATICS[root_id] if x in self.roots]
                )
                low_string = random.choice(self.config["low_strings"])
                inversion = random.choice(self.config["inversions"])
                chord_type = random.choice(self.config["chord_types"])
                chord_tab = self.get_chord_tab(
                    low_string, inversion, chord_type, root_id
                )
                input(
                    f"Low String: {low_string.upper()} \nInversion: {inversion}\nChord Name: {root + chord_type}\n\nhit enter for answer \n"
                )

                print(f"\n{chord_tab}\n")
                inp = input("hit enter to continue \n")
                os.system("cls" if os.name == "nt" else "clear")

            else:
                raise NotImplementedError(f"theory mode: {self.mode} not implemented!")

            total += 1

        print(f"Final Score: {100*(correct / total)}% correct")


if __name__ == "__main__":
    TheoryTeacher().run_cli()
