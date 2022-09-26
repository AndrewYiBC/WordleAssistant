"""
Assistant for solving Wordle (from New York Times Games)
Aims to provide optimal suggestions for each guess

Wordle - The New York Times:
https://www.nytimes.com/games/wordle/index.html
"""


import os
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

        # DataFrame of possible words with 6 columns
        # each of the first 5 columns is a single letter
        # the last column is the entire 5-letter word
        # the list of possible words (possible_words.txt) is from 3b1b's GitHub:
        # https://github.com/3b1b/videos/tree/master/_2022/wordle
        # where the possible_words.txt is located in the data directory
        self._possible_words = self._load_possible_words(
            os.path.join("data", "possible_words.txt")
        )

        # DataFrame of valid words with 6 columns
        # valid words is a subset of possible words that
        # satisfies all currently identified information
        self._valid_words = self._possible_words


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
        self._update_valid_words()
    

    def get_valid_words(self, verbose=False) -> list:
        valid_words_list = self._valid_words[5].to_list()
        if verbose:
            lim = 10
            count = len(valid_words_list)
            print("There are {:d} valid words".format(count))
            if count > lim:
                print("Please refer to the returned list for all valid words")
            else:
                print("All valid words:")
                for word in valid_words_list:
                    print(word)
        return valid_words_list


    def _update_valid_words(self) -> None:
        incorrect_letters = set()
        valid_df = self._valid_words
        # select words that have included letters at correct positions
        for pos in range(5):
            if self.correct_pos[pos] is not None:
                valid_df = valid_df.loc[valid_df[pos] == self.correct_pos[pos]]
        # select words that don't have included letters at incorrect positions
        for pos in range(5):
            if len(self.incorrect_pos[pos]) != 0:
                incorrect_letters = incorrect_letters | self.incorrect_pos[pos]
                valid_df = valid_df.loc[~valid_df[pos].isin(self.incorrect_pos[pos])]
        # select words that have included letters not at incorrect positions
        for letter in incorrect_letters:
            valid_df = valid_df.loc[valid_df[5].str.contains(letter)]
        # select words that don't have not included letters
        if len(self.excluded_letters) != 0:
            for pos in range(5):
                valid_df = valid_df.loc[~valid_df[pos].isin(self.excluded_letters)]
        self._valid_words = valid_df.reset_index(drop=True)


    @staticmethod
    def _load_possible_words(path: str) -> pd.DataFrame:
        with open(path) as f:
            words = f.readlines()
            words = [w.rstrip() for w in words]
            words_split = [list(w) + [w] for w in words]
            words_df = pd.DataFrame(words_split)
            return words_df


if __name__ == "__main__":
    assistant = WordleAssistant()
