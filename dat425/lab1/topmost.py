import sys
from wordfreq import tokenize, count_words

def main():
    stopwords = open(sys.argv[1], "r").read().splitlines()
    text = open(sys.argv[2], "r").read().splitlines()
    limit = int(sys.argv[3])
    tokens = tokenize(text)
    count_list = count_words(tokens, stopwords)
    filtered_words = count_list[:limit]
    for word in filtered_words:
        print(word[0], word[1])

main()
