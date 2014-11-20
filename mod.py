import rsm

#This document contains a class of objects that behave as integers mod p.
#Since it is both self-explanatory and only used in the main program in
#very intuitive ways, I have left it uncommented.

class modp(object):
    def __init__(self, n, p):
        self.val = n % p
        self.p = p
    def __str__(self):
        return str(self.val)
    def __call__(self):
        return self.val
    def __add__(self, other):
        if isinstance(other, modp):
            return modp(self.val + other.val % self.p, self.p)
        else:
            return modp(self.val + other % self.p, self.p)
    def __radd__(self,other):
        if not isinstance(other, modp):
            other = modp(other, self.p)
        return modp.__add__(self, other)
    def __neg__(self):
        return modp(-self.val, self.p)
    def __mul__(self, other):
        if isinstance(other, modp):
            return modp(self.val * other.val % self.p, self.p)
        else:
            return modp(self.val * other % self.p, self.p)
    def __rmul__(self,other):
        if not isinstance(other, modp):
            other = modp(other, self.p)
        return modp.__mul__(self, other)
    def __div__(self, other):
        if isinstance(other, modp):
            return modp(self.val * rsm.rsm(other.val, self.p-1, self.p) % self.p, self.p)
        else:
            return modp(self.val * rsm.rsm(other, self.p-1, self.p) % self.p, self.p)
    def __rdiv__(self,other):
        if not isinstance(other, modp):
            other = modp(other, self.p)
        return modp.__div__(self, other)
    def __inv__(self):
        return modp (rsm.rsm(self.val, self.p-1, self.p),p)
    def __gt__(self,other):
        if isinstance(other, modp):
            return self.val > other.val
        else:
            return self.val > other
    def __ge__(self,other):
        if isinstance(other, modp):
            return self.val >= other.val
        else:
            return self.val >= other
    def __eq__(self,other):
        if isinstance(other, modp):
            return self.val == other.val
        else:
            return self.val == other
    def __ne__(self,other):
        if isinstance(other, modp):
            return self.val != other.val
        else:
            return self.val != other
    def __le__(self,other):
        if isinstance(other, modp):
            return self.val <= other.val
        else:
            return self.val <= other
    def __lt__(self,other):
        if isinstance(other, modp):
            return self.val < other.val
        else:
            return self.val < other
    def __mod__(self,other):
        if isinstance(other, modp):
            return self.val % other.val
        else:
            return self.val % other
