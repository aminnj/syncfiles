#!/usr/bin/env python

import math, sys, os

def parseCols(cols, maxcols):
    cols = [col.replace("-"," ") for col in cols]
    print " & ".join(cols),
    if(len(cols) < maxcols):
        print " & " * (maxcols - len(cols)),
    print " \\\\ \\hline"


if __name__ == "__main__":
    lines = []
    maxcols = -1

    for item in sys.stdin:
        line = item.strip().split()
        if(len(line) > maxcols): maxcols = len(line)
        lines.append(line)

    if(len(lines) < 1):
        print "Pipe in some stuff, doofus."
        sys.exit(1)

    print "\\documentclass{article}"
    print "\\begin{document}"
    print "\\pagenumbering{gobble}% remove (eat) page numbers"
    print "\\begin{center}"

    print "    \\begin{tabular}{|","c|" * maxcols,"}"
    print "    \\hline"

    for line in lines:
        parseCols(line, maxcols)

    print "    \\end{tabular}"
    print "\\end{center}"
    print "\\end{document}"


