

class SimpleCounter:
    val = 0
    def __init__(self):
        pass

    def count(self):
        self.val += 1

    def reset(self):
        self.val = 0

    def getValue(self):
        return self.val

class BoundedCounter(SimpleCounter):
    def __init__(self, init, modulus):
        self.val = init
        self.mod = modulus-1

    def count(self):
            self.val = self.val % self.mod
            self.val += 1


class ChainedCounter(BoundedCounter):
    def __init__(self, init, modulus, next_counter):
        self.mod = modulus-1
        self.next_counter = next_counter

    def count(self):
            self.val = self.val % self.mod
            if self.val == 0 and self.next_counter:
                self.next_counter.count()
            self.val += 1

