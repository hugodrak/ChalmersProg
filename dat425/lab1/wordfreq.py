def tokenize(lines):
    tokens = []
    for line in lines:
        splitted = line.split(" ")
        for word in splitted:
            new_word = ""
            new_char = ""
            char_before = False
            for char in word:
                if char.isalpha():
                    new_word += char
                elif char != "":
                    if new_word:
                        tokens.append(new_word.lower())
                        new_word = ""
                    new_char += char
                else:
                    continue
            if new_word:
                tokens.append(new_word.lower())
            if new_char:
                tokens.append(new_char)

    return tokens


def count_words(words, stopwords):
    count_dict = {}

    for word in words:
        if word not in stopwords:
            if word in count_dict.keys():
                count_dict[word] += 1
            else:
                count_dict[word] = 1
    count_list = [[i, count_dict[i]] for i in count_dict.keys()]
    count_list.sort(key=lambda x:-x[1])

    return count_list


#tokens = tokenize(open("./lab1/examples/article1.txt", "r").read().splitlines())
#stopwords = ["the"]
#count_words(tokens, stopwords)
# tokenize(open("./test.txt", "r").read().splitlines())
