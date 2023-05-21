from typing import Dict, List
import random
import os
import toml

from constants import CHROMATICS, INTERVALS, CONFIG_DIRS, THEORY_MODES


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
                raise NotImplementedError(f"theory mode: {self.mode} not implemented!")
            else:
                raise NotImplementedError(f"theory mode: {self.mode} not implemented!")

            total += 1

        print(f"Final Score: {100*(correct / total)}% correct")


if __name__ == "__main__":
    TheoryTeacher().run_cli()
