#!/usr/bin/env python

import math, sys, os

def parseCols(inputcols, maxcols):
    cols = []
    columnOfMultirow=-1
    for i,col in enumerate(inputcols):
        if(col.strip() == "-"):
            cols.append(" ")
        elif("multirow" in col):
            # multirow 2 $10 \pm 15$
            # ^-- I want 2 rows that show 10\pm15
            ncols = int(col.split()[1].strip())
            content = " ".join(col.split()[2:])
            # content = content.replace("\\","\\\\")
            cols.append("\\multirow{%i}{*}{%s}" % (ncols, content))
            columnOfMultirow=i
        else: cols.append(col)

        pass
    print " & ".join(cols),
    if(len(cols) < maxcols):
        print " & " * (maxcols - len(cols)),

    if(columnOfMultirow > -1):
        if(columnOfMultirow == len(cols)-1): # last one
            print " \\\\ \\cline{%i-%i}" % (1, len(cols)-1)
        else: # first one
            print " \\\\ \\cline{%i-%i}" % (2, len(cols))
    else:
        print " \\\\ \\hline"


if __name__ == "__main__":
    lines = []
    maxcols = -1

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

    print "    \\begin{tabular}{|","c|" * maxcols,"}"
    print "    \\hline"

    for line in lines:
        if(len("".join(line).strip()) < 1):
            print "    \\hline"
        else:
            parseCols(line, maxcols)

    print "    \\end{tabular}"
    print "\\end{center}"
    print "\\end{document}"


