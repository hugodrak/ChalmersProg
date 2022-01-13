from range_binary_search import first_index_of, last_index_of
from term import Term

class Autocompleter:
    def __init__(self, dictionary):
        """Initializes the dictionary from the given list of terms."""
        self.dictionary = dictionary
        self.sort_dictionary()  # calls the class function to always sort the list when creating the object

    def sort_dictionary(self):
        """Sorts the dictionary in *case-insensitive* lexicographic order.
        Complexity: O(N log N) where N is the number of dictionary terms."""
        self.dictionary.sort(key = Term.lexicographic_order) #calling the built in sorting function

    def number_of_matches(self, prefix):
        """Returns the number of terms that start with the given prefix.
        Precondition: the internal dictionary is in lexicographic order.
        Complexity: O(log N) where N is the number of dictionary terms."""

        T = Term(prefix, 0)
        start = first_index_of(self.dictionary, T, Term.prefix_order(len(prefix)))  # use bst to find the first occurance of the item matching the term in the array
        end = last_index_of(self.dictionary, T, Term.prefix_order(len(prefix)))     # -||-
        if start == -1 or end == -1:    # if start or end returns -1 == no match, then return 0 matches
            return 0
        diff = end + 1 - start # increase end by one due to that we want diff in number of matches and not diff in index (inclusive)
        return diff

    def all_matches(self, prefix):
        """Returns all terms that start with the given prefix, in descending order of weight.
        Precondition: the internal dictionary is in lexicographic order.
        Complexity: O(log N + M log M) where M is the number of matching terms."""
        # follows the same concept as no of matches, with the addition of returning the items that are in the match range.
        # and then sorts the values in decending order on weight
        T = Term(prefix, 0)
        start = first_index_of(self.dictionary, T, Term.prefix_order(len(prefix)))
        end = last_index_of(self.dictionary, T, Term.prefix_order(len(prefix)))
        if start == -1 or end == -1:
            return []
        res = self.dictionary[start:end+1]
        res.sort(key = Term.reverse_weight_order)
        return res

def read_dictionary(dict_file):
    dictionary = []
    with open(dict_file, encoding="utf-8") as DF:
        for line in DF:
            weight, word = line.split(maxsplit = 1)
            dictionary.append(Term(word.strip(), int(weight)))
    return dictionary

if __name__ == "__main__":
    dictionary = read_dictionary('dictionaries/romaner.txt')

    for i in range(1, 62000, 500):
        #print('lim', i)
        completer = Autocompleter(dictionary[:i])
        prefix = 'a'
        nr_matches = completer.number_of_matches(prefix)
        #print("")
        #print(f"Number of matches for prefix '{prefix}': {nr_matches}")
        # results = completer.all_matches(prefix)
        # for term in results[:10]:
        #     print(f"{term.weight:12}    {term.word}")

