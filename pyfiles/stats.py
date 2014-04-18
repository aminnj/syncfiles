#!/usr/bin/env python

import math, sys, os

def statistics(ls):
    length = len(ls)
    totsum = sum(ls)
    mean = 1.0*totsum/length
    sigma = math.sqrt(1.0*sum([(mean-v)*(mean-v) for v in ls])/(length-1))
    maximum, minimum = max(ls), min(ls)
    return (length, mean, sigma, totsum, minimum, maximum)

def freq(ls):
    dout = {}
    for elem in ls:
        if(elem not in dout.keys()): dout[elem] = 1
        else: dout[elem] += 1
    return dout

def makehisto(ls):
    d = freq(ls)
    maxval = max([d[k] for k in d.keys()])
    maxstrlen = max([len(k) for k in d.keys()])
    scaleto=80-maxstrlen
    for w in sorted(d, key=d.get, reverse=True):
        strbuff = "%%-%is | %%s (%%i)" % (maxstrlen)
        # strbuff = "%-9s | %s (%i)"
        if(maxval < scaleto):
            print strbuff % (w, "*" * d[w], d[w])
        else: # scale to scaleto width
            print strbuff % (w, "*" * max(1,int(float(scaleto)*d[w]/maxval)), d[w])


if __name__ == "__main__":
    nums, words = [], []
    column = -1
    if(len(sys.argv) > 1): column = int(sys.argv[-1])
    for item in sys.stdin:
        try:
            if(column == -1): nums.append(float(item.strip()))
            else: nums.append(float(item.strip().split()[column-1]))
        except: 
            try:
                if(column == -1): words.append(item.strip())
                else: words.append(item.strip().split()[column-1])
            except: pass
        else: pass

    if(len(nums) <= 1):
        if(len(words) < 3):
            print "Can't calculate stuff with %i element!" % len(nums)
        else:
            print "Found %i words, so histo will be made!" % len(words)
            makehisto(words)
    else: 
        print """
        length: {0}
        mean:   {1}
        sigma:  {2}
        sum:    {3}
        min:    {4}
        max:    {5}
        """.format(*statistics(nums))
