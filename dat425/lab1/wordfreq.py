def tokenize(lines) -> list:
    tokens = []
    for line in lines:
        splitted = line.split(" ")  # splits on space
        for word in splitted:
            new_word = ""  # for words
            new_char = ""  # for other chars
            for char in word:
                if char.isalpha():  # checks if char is letter
                    if new_char:  # if char string exists, append to token list
                        tokens.append(new_char)
                        new_char = ""
                    new_word += char  # add this letter to letter word

                elif char != "" and char != "\t":  # if not separator
                    if new_word:  # if word exists add to tokens
                        tokens.append(new_word.lower())
                        new_word = ""
                    if char.isdigit():  # if is digit, add to char word
                        new_char += char
                    else:
                        if new_char:  # if new char appears that is not digit, and digit word exists, add to tokens
                            tokens.append(new_char)
                            new_char = ""
                        tokens.append(char)  # add single char to token, due to non digit char should not be grouped
                else:
                    continue  # if separator, skip

            if new_word:
                tokens.append(new_word.lower())
            if new_char:
                tokens.append(new_char)

    return tokens  # returns list of tokens


# takes words and filter out stopwords, and then counts
# returns a dict with word as key and count as value
def countWords(words, stopwords) -> dict:
    count_dict = {}

    for word in words:
        if word not in stopwords:
            if word in count_dict.keys():
                count_dict[word] += 1
            else:
                count_dict[word] = 1

    return count_dict


# prints words with counts and limits the print by the limit variable
def printTopMost(frequencies: dict, limit: int) -> None:
    # takes the dict and splits it into a 2 long list with word first and count second
    count_list = [[i, frequencies[i]] for i in frequencies.keys()]
    # then sorts the list of lists using second(count values)
    count_list.sort(key=lambda x: -x[1])

    limited_words = count_list[:limit]
    for word in limited_words:
        print(word[0].ljust(19), str(word[1]).rjust(5))
