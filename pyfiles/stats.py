#!/usr/bin/env python

import math, sys

def statistics(ls):
    length = len(ls)
    mean = 1.0*sum(ls)/length
    sigma = math.sqrt(1.0*sum([(mean-v)*(mean-v) for v in ls])/(length-1))
    totsum = mean*length
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

