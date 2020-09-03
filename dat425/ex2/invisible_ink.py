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
	# TODO
    pass


def bin2txt(bin):
	# TODO
    pass


def invisible2txt(inv):
    return bin2txt(invisible2bin(inv))


def main():
	# TODO
	pass

main()
