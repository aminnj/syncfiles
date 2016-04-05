from ROOT import *

def merge_files(fnames_in, fname_out=None, treename="Events"):
    """
    # takes list of root files (or single string with wildcard). merges the entries in the given tree.

    basedir = "/hadoop/cms/store/user/namin/T2bW_575_2875_1_step3/crab_T2bW_575_2875_1_step3_apatters-T2bW_mSTOP575_mNLSP2875_mLSP1_seed42484-eb69b0448a13fda070ca35fd76ab/160327_061942/0000/"
    fnames = ["ntuple_1*.root", "ntuple_2*.root"]
    n_evts = merge_files(fnames)
    print "%i events merged" % n_evts
    """

    if not fname_out: fname_out = "merged.root"

    ch = TChain(treename)

    if type(fnames_in) in [list, tuple]:
        for fname in fnames_in:
            ch.Add(fname)
            print "Adding %s" % fname
    else:
        ch.Add(fnames_in)

    n_entries = ch.GetEntries()
    ch.Merge(fname_out)

    return n_entries

def get_chunks(v,n=50): return [ v[i:i+n] for i in range(0, len(v), n) ]

def copy_events(fname_in, runlumievts, fname_out=None, treename="Events"):
    # takes list of 3-tuples (run,lumi,evt), input root file (or wildcard), output name (if None, construct it)
    """
    rles = [(1,1,evt) for evt in [5,9,17,20,29,32,33,26,38,40,42]]
    n_evts = copy_events("/hadoop/cms/store/user/namin/T2bW_575_2875_1_step3/crab_T2bW_575_2875_1_step3_apatters-T2bW_mSTOP575_mNLSP2875_mLSP1_seed42484-eb69b0448a13fda070ca35fd76ab/160327_061942/0000/ntuple_1.root", rles)
    print "%i events selected" % n_evts
    """

    if not fname_out: 
        if "*" not in fname_in: fname_out = fname_in.split("/")[-1].replace(".root", "_skim.root")
        else: fname_out = "skim.root"

    d_rle = set()
    for rle in runlumievts:
        rle = map(int, list(rle)) # make sure all ints
        d_rle.add( tuple(rle) )

    ch = TChain(treename)
    ch.Add(fname_in)
    n_entries = ch.GetEntries()

    ch.SetBranchStatus("*",0)
    ch.SetBranchStatus("*_eventMaker_*",1)

    for chunk in get_chunks(runlumievts, n=50):
        cut_str = " || ".join(["(evt_run==%i && evt_lumiBlock==%i && evt_event==%i)" % tuple(rle) for rle in chunk])
        ch.Draw(">>+elist", cut_str, "goff")
    elist = gDirectory.Get("elist")

    ch.SetBranchStatus("*",1)

    new_file = TFile(fname_out,"RECREATE") 
    ch.SetEventList(elist)
    ch_new = ch.CopyTree("")
 
    ch_new.GetCurrentFile().Write() 
    ch_new.GetCurrentFile().Close()

def copy_events_SLOW(fname_in, runlumievts, fname_out=None, treename="Events"):
    """
    # takes list of 3-tuples (run,lumi,evt), input root file (or wildcard), output name (if None, construct it)

    rles = [(1,1,evt) for evt in [5,9,17,20,29,32,33,26,38,40,42]]
    n_evts = copy_events("/hadoop/cms/store/user/namin/T2bW_575_2875_1_step3/crab_T2bW_575_2875_1_step3_apatters-T2bW_mSTOP575_mNLSP2875_mLSP1_seed42484-eb69b0448a13fda070ca35fd76ab/160327_061942/0000/ntuple_1.root", rles)
    print "%i events selected" % n_evts
    """

    if not fname_out: 
        if "*" not in fname_in: fname_out = fname_in.split("/")[-1].replace(".root", "_skim.root")
        else: fname_out = "skim.root"

    d_rle = set()
    for rle in runlumievts:
        rle = map(int, list(rle)) # make sure all ints
        d_rle.add( tuple(rle) )

    ch = TChain(treename)
    ch.Add(fname_in)
    n_entries = ch.GetEntries()
    print "Looping over %i events" % n_entries

    # speed up loop by only enabling eventMaker branches
    ch.SetBranchStatus("*",0)
    ch.SetBranchStatus("*_eventMaker_*",1)
    print "Disabled all but *_eventMaker_* branches"

    newFile = TFile(fname_out,"RECREATE") 
    ch_new = ch.CloneTree(0) 
    print "Initialized cloned tree"

    num_fill = 0
    for i in range(n_entries): 
        if (i % (n_entries // 100)) == 0: print "%i / %i" % (i, n_entries)

        ch.GetEntry(i)
        evt = ch.ull_eventMaker_evtevent_CMS3.product()[0]
        lumi = ch.uint_eventMaker_evtlumiBlock_CMS3.product()[0]
        run = ch.uint_eventMaker_evtrun_CMS3.product()[0]

        if (int(run), int(lumi), int(evt)) not in d_rle: continue

        ch_new.Fill() 
        num_fill += 1
 
    ch_new.GetCurrentFile().Write() 
    ch_new.GetCurrentFile().Close()

    return num_fill


if __name__ == "__main__":
    basedir = "/hadoop/cms/store/user/namin/T2bW_575_2875_1_step3/crab_T2bW_575_2875_1_step3_apatters-T2bW_mSTOP575_mNLSP2875_mLSP1_seed42484-eb69b0448a13fda070ca35fd76ab/160327_061942/0000/"
    fnames = [basedir+fname for fname in ["ntuple_11*.root", "ntuple_21*.root"]]
    n_evts = merge_files(fnames)
    print "%i events merged" % n_evts
