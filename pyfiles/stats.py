#!/usr/bin/env python

import math, sys, os

def statistics(ls):
    length = len(ls)
    totsum = sum(ls)
    mean = 1.0*totsum/length
    sigma = math.sqrt(1.0*sum([(mean-v)*(mean-v) for v in ls])/(length-1))
    maximum, minimum = max(ls), min(ls)
    return (length, mean, sigma, totsum, minimum, maximum)

if __name__ == "__main__":
    nums = []
    for num in sys.stdin.readlines():
        try:
            nums.append(float(num.strip()))
        except:
            pass
        else:
            pass

    if(len(nums) <= 1):
        print "Can't calculate stuff with %i element!" % len(nums)
    else: 
        print """
        length: {0}
        mean: {1}
        sigma: {2}
        sum: {3}
        min: {4}
        max: {5}
        """.format(*statistics(nums))

    if(len(sys.argv) > 2):
        if(sys.argv[-2].strip() == "-h"):
            binwidth=sys.argv[-1]
            os.system("gnuplot -e 'set term dumb; binwidth=%s; bin(x,width)=width*floor(x/width); plot \"L1B.dat\" using (bin($1,binwidth)):(1.0) smooth freq with boxes'" % (binwidth))

