#!/usr/bin/env python

import ROOT as r
import argparse
import sys


def get_total_size(br):
    f = r.TMemFile("buffer","CREATE")
    if br.GetTree().GetCurrentFile():
        f.SetCompressionSettings(br.GetTree().GetCurrentFile().GetCompressionSettings())
    f.WriteObject(br,"thisbranch")
    key = f.GetKey("thisbranch");
    basket_size_zip, basket_size_tot = get_basket_size(br)
    return [int(basket_size_zip + key.GetNbytes()), int(basket_size_tot + key.GetNbytes())]

def get_basket_size(br):
    brs = [br]
    subbrs = br.GetListOfBranches()
    if subbrs: brs += subbrs

    ret_zip, ret_tot = 0, 0
    for br in brs:
        ret_zip += br.GetZipBytes()
        ret_tot += br.GetTotBytes()

    return ret_zip, ret_tot

def main(fname_in, treename, maxnum):

    f = r.TFile(fname_in)
    tree = f.Get(treename)

    info = []
    for br in tree.GetListOfBranches():
        z,uz = get_total_size(br) # zipped and unzipped sizes
        info.append([br.GetName(), z, uz])

    tot_z = sum(x[1] for x in info)
    tot_uz = sum(x[2] for x in info)
    branches = []
    for n,z,uz in info:
        branches.append({"bname": n, "frac": 1.0*z/tot_z, "uncompBytes": uz, "compBytes": z})

    print
    print " Tree name: %s" % tree.GetName()
    print "      nevents: %i" % tree.GetEntries()
    print
    top_branches = sorted(branches, key=lambda x: x.get("frac",-1), reverse=True)[:maxnum]
    maxcols = max([len(b["bname"]) for b in top_branches[:maxnum]])+4
    print ("%-{0}s %s".format(maxcols)) % ("branchname", "size (%) [compression factor]")
    print "-" * (maxcols+15)
    for b in top_branches:
        print ("%-{0}s %2.1f [%03.1f]".format(maxcols)) % (b["bname"], 100.0*b["frac"], 1.0*b["uncompBytes"]/b["compBytes"])

if __name__ == "__main__":

    parser = argparse.ArgumentParser()
    parser.add_argument("filename", help="name of file to make classfile on")
    parser.add_argument("-t", "--tree", help="treename (default: Events)", default="Events")
    parser.add_argument("-n", "--num", help="number of top branches to show", default=30)
    args = parser.parse_args()
    fname_in = args.filename
    treename = args.tree
    maxnum = int(args.num)

    main(fname_in, treename, maxnum)
