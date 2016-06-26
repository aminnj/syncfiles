#!/usr/bin/env python

import ROOT as r
import argparse

def classname_to_type(cname): return "const " + cname.strip()

if __name__ == "__main__":

    parser = argparse.ArgumentParser()
    parser.add_argument("filename", help="name of file to make classfile on")
    parser.add_argument("-q", "--quiet", help="don't show all filenames", action="store_true")
    parser.add_argument("-t", "--tree", help="treename (default: Events)", default="Events")
    parser.add_argument("-o", "--namespace", help="namespace (default: tas)", default="tas")
    parser.add_argument("-n", "--objectname", help="objectname (default: cms3)", default="cms3")
    parser.add_argument("-c", "--classname", help="classname (default: CMS3)", default="CMS3")
    args = parser.parse_args()

    fname_in = args.filename
    treename = args.tree
    classname = args.classname
    objectname = args.objectname
    namespace = args.namespace

    f = r.TFile(fname_in)
    tree = f.Get(treename)
    aliases = tree.GetListOfAliases()
    branches = tree.GetListOfBranches()

    d_bname_to_info = {}

    # cuts = ["filtcscBeamHalo2015","evtevent","evtlumiBlock","evtbsp4","hltprescales","hltbits","hlttrigNames","musp4","evtpfmet","muschi2","ak8jets_pfcandIndicies","hlt_prescales"]
    cuts = ["lep1_p4","lep2_p4"]
    isCMS3 = False
    have_aliases = False
    for branch in branches:
        bname = branch.GetName()
        cname = branch.GetClassName()
        btitle = branch.GetTitle()

        if bname in ["EventSelections", "BranchListIndexes", "EventAuxiliary", "EventProductProvenance"]: continue
        # if not any([cut in bname for cut in cuts]): continue

        # sometimes root is stupid and gives no class name, so must infer it from btitle (stuff like "btag_up/F")
        if not cname:
            if btitle.endswith("/i"): cname = "unsigned int"
            elif btitle.endswith("/l"): cname = "unsigned long long"
            elif btitle.endswith("/F"): cname = "float"
            elif btitle.endswith("/I"): cname = "int"
            elif btitle.endswith("/O"): cname = "bool"
            elif btitle.endswith("/D"): cname = "double"

        typ = cname[:]
        if "edm::Wrapper" in cname:
            isCMS3 = True
            typ = cname.replace("edm::Wrapper<","")[:-1]
        typ = classname_to_type(typ)

        d_bname_to_info[bname] = {
                "class": cname,
                "alias": bname.replace(".",""),
                "type": typ,
                }

    if aliases:
        have_aliases = True
        for ialias, alias in enumerate(aliases):
            aliasname = alias.GetName()
            branch = tree.GetBranch(tree.GetAlias(aliasname))
            branchname = branch.GetName().replace("obj","")
            if branchname not in d_bname_to_info: continue
            d_bname_to_info[branchname]["alias"] = aliasname.replace(".","")


    buff = ""

    ########################################
    ################ ***.h ################
    ########################################
    buff += '// -*- C++ -*-\n'
    buff += '#ifndef %s_H\n' % classname
    buff += '#define %s_H\n' % classname
    buff += '#include "Math/LorentzVector.h"\n'
    buff += '#include "Math/Point3D.h"\n'
    buff += '#include "TMath.h"\n'
    buff += '#include "TBranch.h"\n'
    buff += '#include "TTree.h"\n'
    buff += '#include "TH1F.h"\n'
    buff += '#include "TFile.h"\n'
    buff += '#include "TBits.h"\n'
    buff += '#include <vector>\n'
    buff += '#include <unistd.h>\n'
    buff += 'typedef ROOT::Math::LorentzVector<ROOT::Math::PxPyPzE4D<float> > LorentzVector;\n\n'
    buff += '// Generated with file: %s\n\n' % fname_in
    buff += 'using namespace std;\n'
    buff += 'class %s {\n' % classname
    buff += 'private:\n'
    buff += 'protected:\n'
    buff += '\tunsigned int index;\n'
    for bname in d_bname_to_info:
        alias = d_bname_to_info[bname]["alias"]
        typ = d_bname_to_info[bname]["type"]
        buff += '\t%s %s_;\n' % (typ.replace("const","").strip(), alias)
        buff += '\tTBranch *%s_branch;\n' % (alias)
        buff += '\tbool %s_isLoaded;\n' % (alias)
    buff += 'public:\n'
    buff += '\tvoid Init(TTree *tree);\n'
    buff += '\tvoid GetEntry(unsigned int idx);\n'
    buff += '\tvoid LoadAllBranches();\n'
    for bname in d_bname_to_info:
        alias = d_bname_to_info[bname]["alias"]
        typ = d_bname_to_info[bname]["type"]
        buff += '\t%s &%s();\n' % (typ, alias)
    buff += "\tstatic void progress( int nEventsTotal, int nEventsChain );\n"
    buff += '};\n\n'

    buff += "#ifndef __CINT__\n"
    buff += "extern %s %s;\n" % (classname, objectname)
    buff += "#endif\n"
    buff += "\n"
    buff += "namespace %s {\n" % (namespace)
    buff += "\n"
    for bname in d_bname_to_info:
        alias = d_bname_to_info[bname]["alias"]
        typ = d_bname_to_info[bname]["type"]
        buff += "\t%s &%s();\n" % (typ, alias)
    buff += "}\n"
    buff += "#endif\n"

    with open("%s.h" % classname, "w") as fhout:
        fhout.write(buff)

    print ">>> Saved %s.h" % (classname)

    ########################################
    ############### ***.cc ################
    ########################################

    buff = ""
    buff += '#include "%s.h"\n' % classname
    buff += "%s %s;\n\n" % (classname, objectname)
    buff += "void %s::Init(TTree *tree) {\n" % (classname)
    for bname in d_bname_to_info:
        alias = d_bname_to_info[bname]["alias"]
        buff += '\t%s_branch = 0;\n' % (alias)
        if have_aliases:
            buff += '\tif (tree->GetAlias("%s") != 0) {\n' % (alias)
            buff += '\t\t%s_branch = tree->GetBranch(tree->GetAlias("%s"));\n' % (alias, alias)
        else:
            buff += '\tif (tree->GetBranch("%s") != 0) {\n' % (alias)
            buff += '\t\t%s_branch = tree->GetBranch("%s");\n' % (alias, alias)
        buff += '\t\tif (%s_branch) { %s_branch->SetAddress(&%s_); }\n' % (alias, alias, alias)
        buff += '\t}\n'

    buff += '\ttree->SetMakeClass(0);\n'
    buff += "}\n"

    buff += "void %s::GetEntry(unsigned int idx) {\n" % classname
    buff += "\tindex = idx;\n"
    for bname in d_bname_to_info:
        alias = d_bname_to_info[bname]["alias"]
        buff += '\t%s_isLoaded = false;\n' % (alias)
    buff += "}\n"

    buff += "void %s::LoadAllBranches() {\n" % classname
    for bname in d_bname_to_info:
        alias = d_bname_to_info[bname]["alias"]
        buff += '\tif (%s_branch != 0) %s();\n' % (alias, alias)
    buff += "}\n"

    for bname in d_bname_to_info:
        alias = d_bname_to_info[bname]["alias"]
        typ = d_bname_to_info[bname]["type"]
        buff += "%s &%s::%s() {\n" % (typ, classname, alias)
        buff += "\tif (not %s_isLoaded) {\n" % (alias)
        buff += "\t\tif (%s_branch != 0) {\n" % (alias)
        buff += "\t\t\t%s_branch->GetEntry(index);\n" % (alias)
        buff += "\t\t} else {\n"
        buff += '\t\t\tprintf("branch %s_branch does not exist!\\n");\n' % (alias)
        buff += "\t\t\texit(1);\n"
        buff += "\t\t}\n"
        buff += "\t\t%s_isLoaded = true;\n" % (alias)
        buff += "\t}\n"
        buff += "\treturn %s_;\n" % (alias)
        buff += "}\n"

    buff += "void %s::progress( int nEventsTotal, int nEventsChain ){\n" % (classname)
    buff += "  int period = 1000;\n"
    buff += "  if(nEventsTotal%1000 == 0) {\n"
    buff += "    if (isatty(1)) {\n"
    buff += "      if( ( nEventsChain - nEventsTotal ) > period ){\n"
    buff += "        float frac = (float)nEventsTotal/(nEventsChain*0.01);\n"
    buff += "        printf(\"\\015\\033[32m ---> \\033[1m\\033[31m%4.1f%%\"\n"
    buff += "             \"\\033[0m\\033[32m <---\\033[0m\\015\", frac);\n"
    buff += "        fflush(stdout);\n"
    buff += "      }\n"
    buff += "      else {\n"
    buff += "        printf(\"\\015\\033[32m ---> \\033[1m\\033[31m%4.1f%%\"\n"
    buff += "               \"\\033[0m\\033[32m <---\\033[0m\\015\", 100.);\n"
    buff += "        cout << endl;\n"
    buff += "      }\n"
    buff += "    }\n"
    buff += "  }\n"
    buff += "}\n"

    buff += "namespace %s {\n" % (namespace)
    for bname in d_bname_to_info:
        alias = d_bname_to_info[bname]["alias"]
        typ = d_bname_to_info[bname]["type"]
        buff += "\t%s &%s() { return %s.%s(); }\n" % (typ, alias, objectname, alias)
    buff += "}\n"

    with open("%s.cc" % classname, "w") as fhout:
        fhout.write(buff)
    print ">>> Saved %s.cc" % (classname)


