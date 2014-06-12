#!/usr/bin/env python

import commands, os, sys

print sys.argv

def red(txt): return '\033[91m' + txt + '\033[0m'

def doLL(output):
    for i,line in enumerate(output.split("\n")):
        try:
            first, last = line.split(":")
        except:
            continue
        first += ":" + last[:2]
        last = last[2:]
        number = red(str(i).zfill(2))
        print first, number, last.replace(" ","")

def doSimpleLs(output, num, a):
    for i,line in enumerate(output.split("\n")):
        if(i == num-1):
            if(a == "cd"):
                print "TEST"
                print "cd %s" % line
                status, output = commands.getstatusoutput("cd %s" % line)
            elif(a == "vim"):
                os.system("vim %s" % line)
            elif(a == "lk"):
                os.system("ls -lthr %s" % line)
            elif(a == "ll"):
                os.system("ls -l %s" % line)

if(len(sys.argv) < 2): sys.exit()


a = sys.argv[1]

if(a == "lk"):
    status, output = commands.getstatusoutput("ls -lthr --color")
    doLL(output)
#elif(a == "lk"):
    #status, output = commands.getstatusoutput("ls -lthr --color")
    #doLL(output)
elif(a in ["cd", "vim", "lk", "ll"]):
    if(len(sys.argv) < 3): sys.exit()
    status, output = commands.getstatusoutput("ls -1tr")
    doSimpleLs(output, int(sys.argv[2]), a)
    #doSimpleLs(sys.argv[-1])
