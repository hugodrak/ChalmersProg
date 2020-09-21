import sys
from wordfreq import tokenize, countWords, printTopMost
import urllib.request


def main():
    # Loads the files needed for the execution
    stopwords = open(sys.argv[1], "r", encoding="utf8").read().splitlines()

    text_source = sys.argv[2]

    if '://' in text_source:
        # text-source is an internet url. Download over internet
        text = urllib.request.urlopen(text_source).read().decode('utf-8')
    else:
        # text-source is a local file
        with open(text_source, mode='r', encoding='utf-8') as f:
            text = f.read()

    # Split into a list of lines
    lines = text.splitlines()

    limit = int(sys.argv[3])  # sets the limit for how many words will be shown
    tokens = tokenize(lines)  # calls the tokenize function
    count_list = countWords(tokens, stopwords)  # calls the count word function
    printTopMost(count_list, limit)  # prints the top most words in correct order


main()
