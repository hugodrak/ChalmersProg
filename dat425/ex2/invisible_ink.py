import sys
import binaryconv as bc


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


def invisible2bin(inv):
    bin = ""
    for i in inv:
        if i == " ":
            bin += "0"
        elif i == "\t":
            bin += "1"
    return "".join(bin)


def bin2txt(bin):
    txt = ""
    for byte in [bin[i:i+8] for i in range(0, len(bin), 8)]:
        txt += chr(bc.bin2dec(byte))
    return txt


def invisible2txt(inv):
    return bin2txt(invisible2bin(inv))


def main():
    mode = sys.argv[1]
    input_file = open(sys.argv[2], "r").read()
    out_file = open("secret.txt", "w")
    if mode == "encode":
        inv = txt2invisible(input_file)
        out_file.write(inv)
        print(inv)
    elif mode == "decode":
        txt = invisible2txt(input_file)
        print(txt)


main()
