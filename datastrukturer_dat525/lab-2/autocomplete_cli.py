
from term import Term
from autocompleter import Autocompleter


def read_dictionary(dict_file):
    dictionary = []
    with open(dict_file, encoding="utf-8") as DF:
        for line in DF:
            weight, word = line.split(maxsplit = 1)
            dictionary.append(Term(word.strip(), int(weight)))
    return dictionary


def autocomplete(dict_file, max_matches):
    dictionary = read_dictionary(dict_file)
    print(f"Loaded dictionary {dict_file} containing {len(dictionary)} words.")
    print(f"Maximum number of matches to display: {max_matches}")
    completer = Autocompleter(dictionary)
    while True:
        try:
            prefix = input("Enter search prefix (CTRL-C/D/Z to quit)\n").strip()
        except:
            return

        # Print the number of matches.
        nr_matches = completer.number_of_matches(prefix)
        print(f"Number of matches for prefix '{prefix}': {nr_matches}")

        # Find all matches and print the top-most ones.
        results = completer.all_matches(prefix)
        for term in results[:max_matches]:
            print(f"{term.weight:12}    {term.word}")
        print()


USAGE = """
Usage: you have to provide two program arguments:
  (1) the path to a dictionary file,
  (2) the maximum number of matches to display.
"""

if __name__ == '__main__':
    import sys
    # try:
    #     _, dict_file, max_matches = sys.argv
    #     max_matches = int(max_matches)
    # except:
    #     sys.exit(USAGE)
    dict_file = "dictionaries/romaner.txt"
    max_matches = 10
    autocomplete(dict_file, max_matches)
