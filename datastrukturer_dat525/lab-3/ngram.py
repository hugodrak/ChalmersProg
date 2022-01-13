import re
from typing import Tuple
from dataclasses import dataclass

@dataclass
class Ngram:
    words: Tuple[str]

    def __hash__(self):
        """ 
        This calculates and hash dependent on the value of 
        the characters in an ngram and the previous values.
        """
        # return hash(self.words)

        # Bad hash function.
        # Adds the character codes of all characters in the n-gram.
        #
        # Note: 'ord' gives the character code of a character.
        # e.g. ord('A') returns 65
        #
        # result = 0
        # for word in self.words:
        #     for char in word:
        #         result += ord(char)
        # return result



        # as described in lecture
        h = 0
        for word in self.words:
            for c in word:
                h = (37*h + ord(c)) # 37 is a value we got from the lectures
        return h

        # Now you make a better one!

def make_ngrams(string, n=5):
    """Return all n-grams of a given string (default n=5)."""

    # Split the string into lower-case words
    words = re.split("\\W", string.lower())
    words = [word for word in words if len(word) > 0]

    # Produce the n-grams
    ngrams = [ words[i:i+n] for i in range(len(words)) ]
    # The last few words in the string will give "n-grams" of length
    # less than n - remove them
    ngrams = [ ngram for ngram in ngrams if len(ngram) == n ]

    return [ Ngram(tuple(ngram)) for ngram in ngrams ]
