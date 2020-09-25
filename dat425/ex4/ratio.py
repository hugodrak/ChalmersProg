import math

class Ratio:
    def __init__(self, num, denom):
        gcd = math.gcd(num, denom)
        self.num = num//gcd
        self.denom = denom//gcd
    
    def __repr__(self):
        return f"Ratio({self.num},{self.denom})"

    def __add__(self, other):
        a = self.num
        b = self.denom
        c = other.num
        d = other.denom
        num = (a*d)+(c*b)
        denom = b*d
        return Ratio(num, denom)

    def __sub__(self, other):
        a = self.num
        b = self.denom
        c = other.num
        d = other.denom
        num = (a*d)-(c*b)
        denom = b*d
        return Ratio(num, denom)
    
    def __mul__(self, other):
        a = self.num
        b = self.denom
        c = other.num
        d = other.denom
        return Ratio(a*c, b*d)

    def __eq__(self, other):
        if self.num == other.num and self.denom == other.denom:
            return True
        else:
            return False

    def __ne__(self, other):
        if self.num != other.num and self.denom != other.denom:
            return True
        return False

    def __gt__(self, other):
        if float(self) > float(other):
            return True
        return False
    
    def __ge__(self, other):
        if self > other or self == other:
            return True
        return False

    def __lt__(self, other):
        if float(self) < float(other):
            return True
        return False

    def __le__(self, other):
        if self < other or self == other:
            return True
        return False
    
    def __float__(self):
        return self.num/self.denom
    
    def __int__(self):
        return self.num//self.denom

    def __str__(self):
        return f"{self.num}/{self.denom}"
