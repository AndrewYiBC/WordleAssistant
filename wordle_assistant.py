"""
Assistant for solving Wordle (from New York Times Games)
Aims to provide optimal suggestions for each guess

Wordle - The New York Times:
https://www.nytimes.com/games/wordle/index.html
"""


import os
import copy
import itertools
import numpy as np


class WordleAssistant:

    def __init__(self):
        # list of identified correct positions (green tiles), with 5 elements
        # each element corresponds to the correct letter at the position
        self.correct_pos = [None, None, None, None, None]

        # list of identified incorrect positions (yellow tiles), with 5 elements
        # each element corresponds to a set of incorrect letters at the position
        self.incorrect_pos = [set(), set(), set(), set(), set()]

        # set of letters that are included in the word (green or yellow tiles)
        self.included_letters = set()

        # set of letters that are not included in the word (grey tiles)
        self.excluded_letters = set()

        # 2D array of possible words with 6 columns
        # each of the first 5 columns is the letter at the corresponding position
        # the last column is the entire 5-letter word
        # the list of possible words (possible_words.txt) is from 3b1b's GitHub:
        # https://github.com/3b1b/videos/tree/master/_2022/wordle
        # where the possible_words.txt is located in the data directory
        self._possible_words = self._load_possible_words(
            os.path.join("data", "possible_words.txt")
        )

        # 2D array of valid words with 6 columns
        # valid words is a subset of possible words that
        # satisfies all currently identified information
        self._valid_words = self._possible_words


    def guess(self, word: str, colors: str) -> None:
        # iterate over the input word and feedback colors by position
        for pos in range(5):
            letter = word[pos]
            color = colors[pos]
            # "x" corresponds to a grey tile
            if color == "x":
                if letter not in self.included_letters:
                    self.excluded_letters.add(letter)
            # "o" corresponds to a yellow tile
            elif color == "o":
                self.included_letters.add(letter)
                self.incorrect_pos[pos].add(letter)
            # "*" corresponds to a green tile
            elif color == "*":
                self.included_letters.add(letter)
                self.correct_pos[pos] = letter
        self._update_valid_words()


    def suggest(self, verbose=True, lim=5) -> list[tuple[str, float]]:
        optimal_guesses = self._find_optimal_guesses()
        if verbose:
            count = len(optimal_guesses)
            print("There are {:d} valid words remaining".format(count))
            lim = min(count, lim)
            print("The {:d} most optimal next guesses are:".format(lim))
            print(" word    average remaining")
            print("           valid words")
            for word, score in optimal_guesses[:lim]:
                print("{:s}{:14.2f}".format(word, score))
        return optimal_guesses


    def _update_valid_words(self) -> None:
        incorrect_letters = set()
        valid_array = self._valid_words
        # select words that have included letters at correct positions
        for pos in range(5):
            if self.correct_pos[pos] is not None:
                row_indices = valid_array[:, pos] == self.correct_pos[pos]
                valid_array = valid_array[row_indices, :]
        # select words that don't have included letters at incorrect positions
        for pos in range(5):
            if len(self.incorrect_pos[pos]) != 0:
                incorrect_letters = incorrect_letters | self.incorrect_pos[pos]
                row_indices = ~np.isin(valid_array[:, pos], list(self.incorrect_pos[pos]))
                valid_array = valid_array[row_indices, :]
        # select words that have included letters not at incorrect positions
        for letter in incorrect_letters:
            row_indices = np.char.find(valid_array[:, 5], letter) != -1
            valid_array = valid_array[row_indices, :]
        # select words that don't have not included letters
        if len(self.excluded_letters) != 0:
            for pos in range(5):
                row_indices = ~np.isin(valid_array[:, pos], list(self.excluded_letters))
                valid_array = valid_array[row_indices, :]
        self._valid_words = valid_array


    def _find_optimal_guesses(self) -> list[tuple[str, float]]:
        valid_words = self._valid_words[:, 5].tolist()
        # generate all possible feedback colors
        all_possible_colors = list(itertools.product(["*", "o", "x"], repeat=5))
        # the score of the guess is the average remaining valid words after the guess
        scores = {}
        for word in valid_words:
            scores[word] = self._calc_guess_score(word, all_possible_colors)
        # sort the words by score in ascending order
        words_sorted = sorted(scores, key=scores.get)
        optimal_guesses = [(word, scores[word]) for word in words_sorted]
        return optimal_guesses


    def _calc_guess_score(self, word: str, all_possible_colors: list[str]) -> float:
        remaining_valid_words = []
        # iterate over all possible feedback colors
        for colors in all_possible_colors:
            # Make a deep copy of the current instance before simulating a guess
            # so the current instance will not be modified
            next_guess = copy.deepcopy(self)
            next_guess.guess(word, colors)
            next_count = next_guess._valid_words.shape[0]
            # no remaining valid words means the feedback colors are invalid
            if next_count > 0:
                remaining_valid_words.append(next_count)
        # the score is the average remaining valid words across all valid feedback colors
        guess_score = sum(remaining_valid_words) / len(remaining_valid_words)
        return guess_score


    @staticmethod
    def _load_possible_words(path: str) -> np.ndarray:
        with open(path) as f:
            words = f.readlines()
            words = [w.rstrip() for w in words]
            words_split = [list(w) + [w] for w in words]
            words_array = np.array(words_split)
            return words_array


if __name__ == "__main__":
    assistant = WordleAssistant()
