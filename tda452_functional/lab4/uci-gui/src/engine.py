#! /usr/bin/env python3
import sys

print("HEllo world!")

with open("output2.txt", "w+") as f:
    f.write("gustav was here")

from pathlib import Path

p = Path("output.txt")

p.touch(exist_ok=True)

with open(p, mode="w+") as f:
    f.write("sciript started")

def t(line):
    with open(p, mode="a") as f:
        f.write(line+ "\n")




def read():
    t("start receving")
    i = input().strip()
    t("receved: " + repr(i))
    return i


def respond(line):
    t("responding: " + repr(line))
    print(line)


while True:
    cmd =read()

    if cmd == "uci":
        respond("id name derpengine")
        respond("id author gustav")
        respond("uciok")
    elif cmd == "isready":
        respond("readyok")
    elif cmd == "quit":
        break
    elif cmd.startswith("position"):
        if not read().startswith("go"):
            t("error 1")
            continue
        import time
        time.sleep(1)
        respond("bestmove g7g5")

    elif cmd == "stop":
        respond("bestmove g7g5")
    else:
        t("unknown")

