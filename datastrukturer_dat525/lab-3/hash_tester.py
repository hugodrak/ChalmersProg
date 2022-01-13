"""A program for testing your hash table implementation.

You do not need to read or understand this code!"""

from dataclasses import dataclass
from hash_table import HashTable
from typing import Any
import random
import sys
import traceback

@dataclass
class Command:
    model: Any
    func: Any
    args: Any

    def __str__(self):
        if len(self.args) == 1:
            return "table.%s(%r)" % (self.func.__name__, self.args[0])
        else:
            return "table.%s%r" % (self.func.__name__, tuple(self.args))

    def __repr__(self):
        return str(self)

    def run(self, obj):
        return self.func(obj, *self.args)

    def run_model(self, obj):
        return self.model(obj, *self.args)

    def update_args(self, args):
        return Command(self.model, self.func, args)

def key(state):
    if len(state) > 0 and random.randint(1, 2) == 2:
        return random.choice(list(state.keys()))
    else:
        return random.randint(1, (len(state)+2)*2)

def value():
    return random.randint(1, 10)

def generate_commands(n):
    commands = []
    model = {}
    for i in range(n):
        # 30%: add new, 30%: update, 20%: lookup existing, 20%: lookup new
        roll = random.randint(1, 5)

        if roll <= 3:
            model_func = dict.__setitem__
            func = HashTable.put
            args = [key(model), value()]
        else:
            model_func = dict.get
            func = HashTable.get
            args = [key(model)]

        command = Command(model_func, func, args)
        command.run_model(model)
        commands.append(command)

    return commands

def shrink_list(shrink_arg, lst):
    for cand in [[], lst[:len(lst)//2], lst[len(lst)//2:]]:
        if cand != lst:
            yield cand
    for i in range(len(lst)):
        yield lst[:i] + lst[i+1:]
    for i in range(len(lst)):
        for x in shrink_arg(lst[i]):
            yield lst[:i] + [x] + lst[i+1:]

def shrink_unit(shrink, tup):
    for x in shrink(tup[0]):
        yield (x,)

def shrink_pair(shrink1, shrink2, tup):
    x, y = tup
    for x1 in shrink1(x):
        yield (x1, y)
    for y1 in shrink2(y):
        yield (x, y1)

def shrink_int(n):
    return range(n)

def shrink_command(cmd):
    if cmd.func == HashTable.put:
        for args in shrink_pair(shrink_int, shrink_int, cmd.args):
            yield cmd.update_args(args)
    elif cmd.func == HashTable.get:
        for args in shrink_unit(shrink_int, cmd.args):
            yield cmd.update_args(args)
    else:
        raise Exception("Unknown command in hash_tester.py.")

def shrink_commands(cmds):
    return shrink_list(shrink_command, cmds)

def test_commands(cmds, table):
    model = {}

    for cmd in cmds:
        result = cmd.run(table)
        expected = cmd.run_model(model)
        table.check()

        if result != expected:
            raise AssertionError("%s should return %r but returned %r" % (cmd, expected, result))

def test_result(cmds, table):
    try:
        test_commands(cmds, table)
    except Exception as e:
        return e

def shrink_test(cmds, table, result):
    while True:
        for shrunk in shrink_commands(cmds):
            new_table = HashTable()
            new_result = test_result(shrunk, new_table)
            if new_result is not None:
                cmds = shrunk
                table = new_table
                result = new_result
                break
        else:
            return cmds, table, result

def quickcheck():
    print("Testing the HashTable class...", end="")
    sys.stdout.flush()

    for size in range(200):
        print(".", end="")
        sys.stdout.flush()

        cmds = generate_commands(size)
        table = HashTable()
        result = test_result(cmds, table)
        if result is not None:
            print("a test failed! Please wait.")
            print()

            cmds, table, result = shrink_test(cmds, table, result)

            print("The following program goes wrong:")
            print("  table = HashTable()")
            for cmd in cmds:
                print("  %s" % cmd)

            if isinstance(result, AssertionError):
                print("Because:", result)
            else:
                print()
                print("It raised the following exception:")
                traceback.print_tb(result.__traceback__, file=sys.stdout)
                print("%s: %r" % (type(result).__name__, result))

            print()
            print("Hash table contents:")
            print("  table._keys = %r" % table._keys)
            print("  table._values = %r" % table._values)
            print("  table._size = %r" % table._size)

            return
    print("all tests passed!")

if __name__ == '__main__':
    quickcheck()
