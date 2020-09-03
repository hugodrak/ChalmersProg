def tokenize(lines):
    tokens = []
    for line in lines:
        splitted = line.split(" ")
        for word in splitted:
            new_word = ""
            new_char = ""
            for char in word:
                if char.isalpha():
                    if new_char:
                        tokens.append(new_char)
                        new_char = ""
                    new_word += char
                elif char != "" and char != "\t":
                    if new_word:
                        tokens.append(new_word.lower())
                        new_word = ""
                    if char.isdigit():
                        new_char += char
                    else:
                        tokens.append(char)
                else:
                    continue
            if new_word:
                tokens.append(new_word.lower())
            if new_char:
                tokens.append(new_char)

    return tokens


def countWords(words, stopwords):
    count_dict = {}

    for word in words:
        if word not in stopwords:
            if word in count_dict.keys():
                count_dict[word] += 1
            else:
                count_dict[word] = 1

    return count_dict


def printTopMost(frequencies, limit):
    count_list = [[i, frequencies[i]] for i in frequencies.keys()]
    count_list.sort(key=lambda x: -x[1])

    filtered_words = count_list[:limit]
    for word in filtered_words:
        print(word[0].ljust(19), str(word[1]).rjust(5))
