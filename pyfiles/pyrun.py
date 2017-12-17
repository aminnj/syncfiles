#!/usr/bin/env python

import time
import os
import sys
import commands
import argparse

from tqdm import format_meter, StatusPrinter
from multiprocessing import Pool


"""
# Usage:
$ for i in `seq 1 50`; do echo sleep $(echo "$RANDOM/15000" | bc -l); done | pyrun.py -n 6
"""

def f_test((idx,x)):
    time.sleep(x)
    toret = x+x
    return idx,toret

def f_bash((idx,x)):
    status, out = commands.getstatusoutput(x)
    return idx,status

class Runner(object):
    def __init__(self,nproc):
        self.pool = Pool(processes=nproc)
        self.args = []
        self.indices_with_args = []
        self.indices_status = []
        self.ntotal = 0
        self.ndone = 0
        self.elapsed = 0
        self.t0 = None
        self.func = f_bash

    def add_args(self,args):
        next_idx = len(self.indices_with_args)
        for iarg,arg in enumerate(args):
            self.args.append(arg)
            self.indices_with_args.append((next_idx+iarg,arg))
            self.indices_status.append(0)
            self.ntotal += 1

    def get_args(self):
        # Make it possible to append to args during running
        # NOTE: This isn't actually possible because imap_unordered
        # listifies the whole generator first!!!
        i = 0
        while i < self.ntotal:
            yield self.indices_with_args[i]
            i += 1

    def run(self):
        if not self.t0: 
            self.t0 = time.time()

        sp = StatusPrinter(sys.stderr)
        for idx,ret in self.pool.imap_unordered(self.func,self.get_args()):
            self.indices_status[idx] = True
            # Try to add another arg, but won't work (see reason in get_args)
            # if self.ndone == 6:
            #     self.add_args(["sleep 2"])
            self.ndone += 1
            self.elapsed = time.time()-self.t0
            dots = " "+"".join(u"\033[92m\u2022\033[0m" if x == 1 else u"\033[90m\u2219\033[0m" for x in self.indices_status)
            sp.print_status(format_meter(self.ndone, self.ntotal, self.elapsed, size=13,extra=dots))
        print

if __name__ == '__main__':

    parser = argparse.ArgumentParser()
    parser.add_argument("-f", "--file", help="text file with one command per line")
    parser.add_argument("-n", "--nproc", help="number of processes in pool", default="5")
    cli_args = parser.parse_args()

    func_args = []
    if cli_args.file:
        fname = cli_args.file
        func = f_bash
        for line in fname:
            if line.strip():
                func_args.append(line.strip())
    else:
        for item in sys.stdin:
            func = f_bash
            func_args.append(item.strip())

    runner = Runner(int(cli_args.nproc))
    runner.add_args(func_args)
    runner.run()

