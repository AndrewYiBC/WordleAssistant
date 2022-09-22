"""
Assistant for solving Wordle (from New York Times Games)
Aims to provide optimal suggestions for each guess

Wordle - The New York Times:
https://www.nytimes.com/games/wordle/index.html
"""


import pandas as pd


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

        # DataFrame of possible words with 5 columns
        # each column is a single letter
        # the list of possible words (possible_words.txt) is from 3b1b's GitHub:
        # https://github.com/3b1b/videos/tree/master/_2022/wordle
        # where the possible_words.txt is located in the data directory
        self._possible_words = self._load_possible_words("data\possible_words.txt")


    def guess(self, word: str, colors: str) -> None:
        # iterate through the input word and feedback colors by position
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


    @staticmethod
    def _load_possible_words(path: str) -> pd.DataFrame:
        with open(path) as f:
            words = f.readlines()
            words_split = [list(w.rstrip()) for w in words]
            words_df = pd.DataFrame(words_split)
            return words_df


if __name__ == "__main__":
    assistant = WordleAssistant()
