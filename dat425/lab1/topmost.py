import sys
from wordfreq import tokenize, countWords, printTopMost


def main():
    stopwords = open(sys.argv[1], "r").read().splitlines()
    text = open(sys.argv[2], "r").read().splitlines()
    limit = int(sys.argv[3])
    tokens = tokenize(text)
    print(tokens)
    count_list = countWords(tokens, stopwords)
    printTopMost(count_list, limit)


main()
