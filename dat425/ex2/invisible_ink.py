import binaryconv as bc
import argparse

parser = argparse.ArgumentParser()
parser.add_argument("--encode", action="store_true")
parser.add_argument("--decode", action="store_true")
parser.add_argument("--input", "-i")


def txt2bin(txt):
    bin = []
    for c in txt:
        bin.append(bc.padzero(bc.dec2bin(ord(c)),8))
    return "".join(bin)


def bin2invisible(bin):
    inv = []
    for b in bin:
        if b == '0':
            inv.append(' ')
        else:
            inv.append('\t')
    return "".join(inv)


def txt2invisible(txt):
    return bin2invisible(txt2bin(txt))


# Added this
def invisible2bin(inv):
    bin = []
    # for separator in string
    for i in inv:
        if i == " ":  # if space then eq 0
            bin.append("0")
        elif i == "\t":  # if tab eq 1
            bin.append("1")
    return "".join(bin)  # return joined string


# Added this
def bin2txt(bin):
    txt = []
    # uses list comprehension to split byte string into chunks of 8, due to byte is 8 long
    for byte in [bin[i:i+8] for i in range(0, len(bin), 8)]:
        txt.append(chr(bc.bin2dec(byte)))  # then calls bin to dec and converts int to char
    return "".join(txt)  # return joined string


def invisible2txt(inv):
    return bin2txt(invisible2bin(inv))


# Added this
def main():
    args = parser.parse_args()  # loads arguments
    input_file = open(args.input, "r").read()  # reads input file
    if args.encode:
        out_file = open("secret.txt", "w")  # opens file to write if encode mode
        inv = txt2invisible(input_file)  # converts text to invisible
        out_file.write(inv)
        print(inv)
    elif args.decode:
        txt = invisible2txt(input_file)  # converts invisible to text
        print(txt)


main()
