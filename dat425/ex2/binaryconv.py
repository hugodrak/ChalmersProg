import math


def bin2dec(bin):
    dec = 0
    for b in range(len(bin)):
        dec = dec + (2**(len(bin)-b-1)) * int(bin[b])
    return dec


def dec2bin(dec):
    bin = ""
    while dec > 0:
        bit = str(dec % 2)
        bin = bit + bin
        dec = dec // 2
    return bin


def binTable(dec):
    for n in range(1,dec+1):
        bn = dec2bin(n)
        print(n,"\t",bn)


def testDecBin(dec):
    bin  = dec2bin(dec)
    bdec = bin2dec(bin)
    if bdec == dec:
        print(dec,bin,"OK")
    else:
        print(dec,bin,bdec,"ERROR")


def padzero(bin,n):
    need = n - len(bin)
    bin = need *'0' + bin
    return bin
