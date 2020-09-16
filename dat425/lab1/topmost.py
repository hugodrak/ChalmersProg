import sys
from wordfreq import tokenize, countWords, printTopMost


def main():
    # Loads the files needed for the execution
    stopwords = open(sys.argv[1], "r", encoding="utf8").read().splitlines()
    text = open(sys.argv[2], "r", encoding="utf8").read().splitlines()

    limit = int(sys.argv[3])  # sets the limit for how many words will be shown
    tokens = tokenize(text)  # calls the tokenize function
    count_list = countWords(tokens, stopwords)  # calls the count word function
    printTopMost(count_list, limit)  # prints the top most words in correct order


main()
