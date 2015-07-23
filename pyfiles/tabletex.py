#!/usr/bin/env python

import math, sys, os
from itertools import groupby

def listToRanges(a):
    # turns [1,2,4,5,9] into ['1-2','4-5','9-9'] for use with cline
    ranges = []
    for k, iterable in groupby(enumerate(sorted(a)), lambda x: x[1]-x[0]):
         rng = list(iterable)
         if len(rng) == 1: s = str(rng[0][1])+"-"+str(rng[0][1])
         else: s = "%s-%s" % (rng[0][1], rng[-1][1])
         ranges.append(s)
    return ranges

def parseCols(inputcols, maxcols, prevmulti):
    cols = []
    colsMultirow = []
    for i,col in enumerate(inputcols):
        if(col.strip() == "-"):
            cols.append(" ")
        elif("multirow" in col):
            # multirow 2 $\met$
            # ^-- I want 2 rows that show \met (defined below!)
            nrows = int(col.split()[1].strip())
            content = " ".join(col.split()[2:])
            cols.append("\\multirow{%i}{*}{%s}" % (nrows, content))
            colsMultirow.append(i+1)

            prevmulti[i+1] = nrows
        else: 
            cols.append(col)
        
        if( i+1 in prevmulti.keys() ):
            prevmulti[i+1] -= 1

            if(prevmulti[i+1] == 0): del prevmulti[i+1]

    colsMultirow = prevmulti.keys()
    colsNotMultirow = list(set(range(1,maxcols+1))-set(colsMultirow))
    
    print "     ",
    print " & ".join(cols),
    if(len(cols) < maxcols):
        print " & " * (maxcols - len(cols)),

    print "\\\\ ",
    if(len(colsMultirow) > 0):
        for r in listToRanges(colsNotMultirow): print "\\cline{%s}" % r,
        print
    else:
        print "\\hline"
    return prevmulti


if __name__ == "__main__":
    lines = []
    maxcols = -1

    # content = [x.strip('\n') for x in open("test.txt","r").readlines()]
    # for item in content:
    for item in sys.stdin:
        line = item.strip().split("|")
        if(len(line) > maxcols): maxcols = len(line)
        lines.append(line)

    if(len(lines) < 1):
        print "Pipe in some stuff, doofus."
        sys.exit(1)

    print "\\documentclass{article}"
    print "\\usepackage{multirow}"
    print "\\usepackage{slashed}"
    print "\\newcommand{\\met}{\\slashed{E}_\\mathrm{T}}"
    print "\\begin{document}"
    print "\\pagenumbering{gobble}% remove (eat) page numbers"
    print "\\begin{center}"
    print "    \\begin{tabular}{|"+"c|" * maxcols+"}"
    print "    \\hline"
    prevMultiRowInfo={}
    for line in lines:
        # if line is empty, draw double horizontal line
        if(len("".join(line).strip()) < 1):
            print "    \\hline"
        else:
            prevMultiRowInfo = parseCols(line, maxcols, prevMultiRowInfo)
    print "    \\end{tabular}"
    print "\\end{center}"
    print "\\end{document}"


