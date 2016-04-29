#!/usr/bin/env python

import urllib, urllib2, json
import sys
import argparse

"""
examples:
       dis_client.py -t snt "*,cms3tag=CMS3_V08-00-01 | grep dataset_name,nevents_in, nevents_out"
           - this searches for all samples with the above tag in all Twikis and only prints out dataset_name, nevents_out

       dis_client.py /GJets_HT-600ToInf_TuneCUETP8M1_13TeV-madgraphMLM-pythia8/RunIISpring15DR74-Asympt25ns_MCRUN2_74_V9-v1/MINIAODSIM
           - prints out basic information (nevents, file size, number of files, number of lumi blocks) for this dataset

       dis_client.py -t files /GJets_HT-600ToInf_TuneCUETP8M1_13TeV-madgraphMLM-pythia8/RunIISpring15DR74-Asympt25ns_MCRUN2_74_V9-v1/MINIAODSIM
           - prints out filesize, nevents, location for a handful of files for this dataset

       dis_client.py -t files -d /GJets_HT-600ToInf_TuneCUETP8M1_13TeV-madgraphMLM-pythia8/RunIISpring15DR74-Asympt25ns_MCRUN2_74_V9-v1/MINIAODSIM
           - prints out above information for ALL files

Or you can import dis_client and make a query using online syntax and get a json via:
       dis_client.query(q="..." [, type="basic"] [, detail=False])
"""

BASE_URL = "http://uaf-8.t2.ucsd.edu/~namin/makers/disMaker/handler.py"

def query(q, typ="basic", detail=False):
    url = '%s?%s' % (BASE_URL, urllib.urlencode({"query": q, "type": typ, "short": "" if detail else "short"}))

    data = {}
    try:
        content =  urllib2.urlopen(url).read() 
        data = json.loads(content)
    except: print "Failed to perform URL fetching and decoding!"

    return data

        
def get_output_string(q, typ="basic", detail=False):
    buff = ""
    data = query(q, typ, detail)

    if not data:
        return "URL fetch/decode failure"

    if data["response"]["status"] != "success":
        return "DIS failure: %s" % data["response"]["fail_reason"]

    data = data["response"]["payload"]

    if type(data) == dict:
        if "files" in data: data = data["files"]

    if type(data) == list:
        for elem in data:
            if type(elem) == dict:
                for key in elem:
                    buff += "%s:%s\n" % (key, elem[key])
            else:
                buff += str(elem)
            buff += "\n"
    elif type(data) == dict:
        for key in data:
            buff += "%s: %s\n\n" % (key, data[key])

    return buff

def test():

    queries = [
    {"q":"/*/CMSSW_8_0_5*RelVal*/MINIAOD","typ":"basic","detail":False},
    {"q":"/SingleMuon/CMSSW_8_0_5-80X_dataRun2_relval_v9_RelVal_sigMu2015C-v1/MINIAOD","typ":"files","detail":True},
    {"q":"/GJets*/*/*","typ":"snt","detail":True},
    {"q":"/GJets*/*/* | grep cms3tag,dataset_name","typ":"snt","detail":False},
    {"q":"* | grep nevents_out","typ":"snt","detail":False},
    {"q":"/GJets_HT-600ToInf_TuneCUETP8M1_13TeV-madgraphMLM-pythia8/RunIISpring15DR74-Asympt25ns_MCRUN2_74_V9-v1/MINIAODSIM","typ":"mcm","detail":True},
    ]
    for q_params in queries:
        print get_output_string(**q_params)

if __name__ == '__main__':

    parser = argparse.ArgumentParser()
    parser.add_argument("query", help="query")
    parser.add_argument("-t", "--type", help="type of query")
    parser.add_argument("-d", "--detail", help="show more detailed information", action="store_true")
    args = parser.parse_args()
    if not args.type: args.type = "basic"
    print get_output_string(args.query, typ=args.type, detail=args.detail)

