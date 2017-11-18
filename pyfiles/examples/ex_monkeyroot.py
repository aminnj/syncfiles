import monkeyroot
import ROOT as r
import numpy as np

h1 = r.TH1F("h1","not a regular hist",10,0,10)
h1.FillRandom("expo",50000)

print ">>> get integral between two values:",
print h1.IntegralBetween(0.,2.)

print ">>> now fill it with my own values -- super fast since loop is internal"
rands = np.random.normal(5.,1, 1000000)
h1.FillFromList(rands)
print ">>> done"
print ">>> entries: ",h1.GetEntries()

print ">>> get error objects (x +- y) for each bin",
binvalerrs = h1.GetBinValueErrors()
print map(lambda x: x.round(2),binvalerrs)
print ">>> sum them to show that you get the integral and Poisson error:",
print sum(binvalerrs).round(3)

print ">>> take a peek with imgcat"
h1.Show("histe")
