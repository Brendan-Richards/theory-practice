from typing import Dict, List
import random
import os
import toml

from theory_practice.constants import CHROMATICS, INTERVALS, THEORY_MODES, TRIAD_FORMULAS


class TheoryTeacher:
    def __init__(self):
        self.correct = 0
        self.total = 0

    def set_theory_mode(self, theory_mode: str):
        self.correct = 0
        self.total = 0
        self.mode = theory_mode

    def load_config(self, config_name: str):
        config_path = os.path.join("configs", self.mode, f"{config_name}.toml")

        with open(config_path, "r") as f:
            config = toml.load(f)
            config = self.validate_config(config)
        self.config = config

        self.roots = self.get_roots()
        self.root_ids = list(
            {
                idx
                for idx, r_list in enumerate(CHROMATICS)
                for note in r_list
                if note in self.roots
            }
        )
        if self.mode == "intervals":
            self.interval_directions = {
                ivl: dctn
                for ivl, dctn in zip(
                    self.config["intervals"], self.config["directions"]
                )
            }

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

    def generate_question(self):
        if self.mode == "intervals":
            return self.generate_interval_question()
        elif self.mode == "guitar_triads":
            return self.generate_guitar_triad_question()
        else:
            raise NotImplementedError(f"Mode {self.mode} is not supported!")

    def generate_chord_spelling_question(self):
        pass

    def generate_interval_question(self):
        root_id = random.choice(self.root_ids)
        root = random.choice(
            [x for x in CHROMATICS[root_id] if x in self.roots]
        )
        interval = random.choice(self.config["intervals"])
        possible_directions = self.interval_directions[interval].split("/")
        direction = random.choice(possible_directions)
        if direction == "a":
            answer = CHROMATICS[(root_id + INTERVALS[interval]) % len(CHROMATICS)]
        else:
            answer = CHROMATICS[(root_id - INTERVALS[interval])]

        question_text = f'Root: {root} \nInterval: {interval}\nDirection: {"Ascending" if direction == "a" else "Descending"}'
        return {"question": question_text, "answer": answer}

    def grade(self, data: dict):
        guess, answer = data["guess"], data["answer"]
        results = {}

        if self.mode == "intervals":
            correct = guess in answer
            if correct:
                alt_answers = list(set(answer) - set([guess]))
                feedback = f"Correct, also would've accepted: {alt_answers}" if alt_answers else "Correct"
                self.correct += 1
            else:
                feedback = f"Incorrect, the answer was {answer}"

        elif self.mode == "guitar_triads":
            feedback = f"Answer was:\n{answer}"

        self.total += 1
        results["correct"] = self.correct
        results["total"] = self.total
        results["feedback"] = feedback
        return results

    def generate_guitar_triad_question(self):
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
        # display with + and ° notation for readability
        chord_type = chord_type.replace("dim", "°").replace("aug", "+")
        question_text = f"Low String: {low_string.upper()} \nInversion: {inversion}\nChord Name: {root + chord_type}"
        return {"question": question_text, "answer": chord_tab}
