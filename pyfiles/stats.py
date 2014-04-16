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
    column = -1
    if(len(sys.argv) > 1): column = int(sys.argv[-1])
    for num in sys.stdin:
        try:
            if(column == -1): nums.append(float(num.strip()))
            else: nums.append(float(num.strip().split()[column-1]))
        except: pass
        else: pass

    if(len(nums) <= 1):
        print "Can't calculate stuff with %i element!" % len(nums)
    else: 
        print """
        length: {0}
        mean:   {1}
        sigma:  {2}
        sum:    {3}
        min:    {4}
        max:    {5}
        """.format(*statistics(nums))
