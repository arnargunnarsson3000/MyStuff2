class sym:
    """
    A symbolic math tool
    """
    def __init__(self, key, sdict=[]):
        if not sdict:
            self.sdict = [key]
        else:
            self.sdict = sdict
        self.key = '{}'.format(key)

    def __add__(self, other):
        if isinstance(other, list):
            return other.append(self.key)
        if isinstance(other, sym):
            return sym('{}+{}'.format(self.key, other.key), sdict=self.sdict+other)
        else:
            return sym('{}+{}'.format(self.key, other), sdict=self.sdict+other)
    def __radd__(self, other):
        if isinstance(other, list):
            return other.append(self.key)
        if isinstance(other, sym):
            return sym('{}+{}'.format(self.key, other.key, sdict=self.sdict.append(other)))
        else:
            return sym('{}+{}'.format(self.key, other, sdict=self.sdict.append(other)))

    def __str__(self):
        return self.key

if __name__ == "__main__":
    a = sym('a')
    b = sym('b')
    print(a)
    print(a+b)
    c = a + b
    print(c)
    print(c.sdict)
