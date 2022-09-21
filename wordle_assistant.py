"""
Assistant for solving Wordle (from New York Times Games)
Aims to provide optimal suggestions for each guess

Wordle - The New York Times:
https://www.nytimes.com/games/wordle/index.html
"""


class WordleAssistant:

    def __init__(self):
        # dictionary of letters that are included in the word
        # each key is a letter
        # each value is a list of two sets:
        # element [0] is the set of identified correct positions (green tiles)
        # element [1] is the set of identified incorrect positions (yellow tiles)
        self.included_letters = {}
        # set of letters that are not included in the word (grey tiles)
        self.excluded_letters = set()


    def guess(self, word: str, colors: str) -> None:
        # iterate through the input word and feedback colors by position
        for pos in range(5):
            letter = word[pos]
            color = colors[pos]
            # "*" corresponds to a green tile
            if color == "*":
                value = self.included_letters.get(letter, [set(), set()])
                value[0].add(pos)
                self.included_letters[letter] = value
            # "o" corresponds to a yellow tile
            elif color == "o":
                value = self.included_letters.get(letter, [set(), set()])
                value[1].add(pos)
                self.included_letters[letter] = value
            # "x" corresponds to a grey tile
            elif color == "x":
                if letter not in self.included_letters:
                    self.excluded_letters.add(letter)


if __name__ == "__main__":
    assistant = WordleAssistant()
