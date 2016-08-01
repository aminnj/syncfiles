#!/usr/bin/env python

import ROOT as r
import argparse
from cStringIO import StringIO
import commands

import sys

if __name__ == "__main__":

    parser = argparse.ArgumentParser()
    parser.add_argument("filename", help="name of file to make classfile on")
    parser.add_argument("-t", "--tree", help="treename (default: Events)", default="Events")
    parser.add_argument("-n", "--num", help="number of top branches to show", default=30)
    args = parser.parse_args()
    fname_in = args.filename
    treename = args.tree
    maxnum = int(args.num)

    # fname_in = "/home/users/namin/2016/ss/80x/SSAnalysis/batch/tzq_10.root"
    # treename = "t"

    f = r.TFile(fname_in)
    tree = f.Get(treename)

    with open("tmp_top_branches.C","w") as fhout:
        
        fhout.write('{\n');
        fhout.write('   TChain *ch = new TChain("%s");\n' % treename);
        fhout.write('   ch->Add("%s");\n' % fname_in);
        fhout.write('   ch->Print();\n');
        fhout.write('}\n');

    stat, out = commands.getstatusoutput("root -b -q -l -n tmp_top_branches.C")

    lines = []
    info = []

    iline = 0
    tmp = []
    out = out[1:]
    for line in out.splitlines():
        iline += 1
        line = line.strip()
        if "***" in line or "..." in line:
            info.append(" ".join("\n".join(tmp[:]).split()))
            tmp = []
            continue
        tmp.append(line)

    branchInfo = []
    ibranch = 0
    while ibranch < len(info):
        bStr = info[ibranch]
        if "see below" in bStr:
            tmp = info[ibranch:ibranch+6]
            tmp[1] = ""
            bStr = " ".join(tmp)
            ibranch += 5
        branchInfo.append(bStr)
        ibranch += 1

    tree = {}
    branches = []
    treeSize = -999
    for bStr in branchInfo:
        try:
            parts = bStr.replace("*",":").split(":")
            parts = map(lambda x: x.strip(), parts)
            if "*Tree" in bStr:
                treename = parts[2]
                nevents = int(parts[parts.index("Entries")+1])

                sizeStr = parts[parts.index("Entries")+2]
                sizeParts = sizeStr.replace("bytes","=").split("=")

                uncompFileBytes = int(sizeParts[1])
                compFileBytes = int(sizeParts[3])

                compFactor = 1.0*uncompFileBytes/compFileBytes


                tree["name"] = treename
                tree["nevents"] = nevents
                tree["uncompBytes"] = uncompFileBytes
                tree["compBytes"] = compFileBytes
                treeSize = compFileBytes

            elif "*Br" in bStr:
                # print parts
                bname = parts[2]
                things = [thing.replace("bytes", "=").split("=") for thing in parts if "Total Size" in thing]
                uncompBytes = sum([int(thing[1]) for thing in things])
                compBytes = sum([int(thing[3]) for thing in things])
                # compFactor = 1.0*uncompBytes/compBytes
                d = {"bname": bname, "uncompBytes": uncompBytes, "compBytes": compBytes, "frac": 1.0*compBytes/treeSize}
                branches.append(d.copy())
        except:
            pass

    totFrac = sum([b.get("frac",0) for b in branches])

    print
    print " Tree name: %s" % tree["name"]
    print "      nevents: %i" % tree["nevents"]
    print "      file size (GB): %.2f" % (tree["compBytes"]/1.0e9)
    print "      compression factor: %.2f" % (1.0*tree["uncompBytes"]/tree["compBytes"])
    print "      parsed %.2f%% of the filesize" % (100.0*totFrac)
    print


    print "%-85s %s" % ("branchname", "size (%) [compression factor]")
    print "-" * 90
    top_branches = sorted(branches, key=lambda x: x.get("frac", 0.0), reverse=True)[:maxnum]
    maxcols = max([len(b["bname"]) for b in top_branches[:maxnum]])+4
    for b in top_branches:
        print ("%-{0}s %2.1f [%03.1f]".format(maxcols)) % (b["bname"], 100.0*b["frac"], 1.0*b["uncompBytes"]/b["compBytes"])

