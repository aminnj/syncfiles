class E:
    """
    Properly propagates errors using all standard operations
    """
    def __init__(self, val, err=None):
        # assume poisson
        if err is None: err = abs(1.0*val)**0.5
        self.val, self.err = 1.0*val, 1.0*err

    def __add__(self, other):
        other_val, other_err = self.get_val(other)
        new_val = self.val + other_val
        new_err = (self.err**2.0 + other_err**2.0)**0.5
        return E(new_val, new_err)

    __radd__ = __add__

    def __sub__(self, other):
        other_val, other_err = self.get_val(other)
        new_val = self.val - other_val
        new_err = (self.err**2.0 + other_err**2.0)**0.5
        return E(new_val, new_err)

    def __rsub__(self, other):
        other_val, other_err = self.get_val(other)
        new_val = -(self.val - other_val)
        new_err = (self.err**2.0 + other_err**2.0)**0.5
        return E(new_val, new_err)


    def __mul__(self, other):
        other_val, other_err = self.get_val(other)
        new_val = self.val * other_val
        new_err = ((self.err * other_val)**2.0 + (other_err * self.val)**2.0)**0.5
        return E(new_val, new_err)

    __rmul__ = __mul__

    def __div__(self, other):
        other_val, other_err = self.get_val(other)
        new_val = self.val / other_val
        new_err = ((self.err/other_val)**2.0+(other_err*self.val/(other_val)**2.0)**2.0)**0.5
        return E(new_val, new_err)

    def __rdiv__(self, other):
        other_val, other_err = self.get_val(other)
        new_val = other_val / self.val
        new_err = ((other_err/self.val)**2.0+(self.err*other_val/(self.val)**2.0)**2.0)**0.5
        return E(new_val, new_err)

    def __pow__(self, other):
        # doesn't accept an argument of class E, only normal number
        new_val = self.val ** other
        new_err = ((other * self.val**(other-1) * self.err)**2.0)**0.5
        return E(new_val, new_err)

    def get_val(self, other):
        other_val, other_err = other, 0.0
        if type(other)==type(self):
            other_val, other_err = other.val, other.err
        return other_val, other_err

    def __str__(self):
        # why use strings? I want python to choose ndecimal places for me
        return "%s +- %s" % (str(self.val), str(self.err))

    def __repr__(self):
        return "%s +- %s" % (str(self.val), str(self.err))

    def __getitem__(self, idx):
        if idx==0: return self.val
        elif idx==1: return self.err
        else: raise IndexError

if __name__ == "__main__":
    v1 = E(10.0,1.0)
    v2 = E(10.0,1.0)
    v3 = E(10.0,2.0)
    v4 = E(20.0,1.0)

    print v1+v2
    print v1+1.0
    print v1-v2
    print v1-1.0
    print v1/v2
    print v1*v2
    print (v1+v2)*(v1*3.0-v2)/(v1*2.0)
    print v1*1.0
    print 1.0*v1
    print 1.0+v1
    print 1.0-v1
    print 1.0/v1
    print v1/1.0
    print v1**2
    print (v1+v2)[0], (v1+v2)[1]
    print v3/v4
    val, err = v4/v3
    print 
