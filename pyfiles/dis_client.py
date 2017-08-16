#!/usr/bin/env python

import urllib, urllib2, json
import sys
import argparse
import socket
import time

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
       dis_client.query(q="..." [, typ="basic"] [, detail=False])
"""

BASE_URL_PATTERN = "http://uaf-{NUM}.t2.ucsd.edu/~namin/makers/disMaker/handler.py"
HOST = "localhost"
PORT = 8888
NBYTES_HEADER = 8

def query(q, typ="basic", detail=False):
    query_dict = {"query": q, "type": typ, "short": "" if detail else "short"}
    url_pattern = '%s?%s' % (BASE_URL_PATTERN, urllib.urlencode(query_dict))

    data = {}

    # try to connect via socket, and if that fails just do regular web request
    try:
        if "uaf-10" not in socket.gethostname():
            # FIXME later. only hosting socket server on uaf-10,
            # so no chance on other computers at the moment
            raise
        # connect to socket
        s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        s.connect((HOST,PORT))

        # calculate message size and send it
        msg = json.dumps(query_dict)
        nbytes = str(len(msg)).zfill(NBYTES_HEADER)
        s.sendall(nbytes+msg)

        # get received payload size and fetch it
        nbytes = int(s.recv(NBYTES_HEADER))
        data = s.recv(nbytes)
        data = json.loads(data)

        s.close()
    except:

        # try all uafs in order of decreasing reliability (subjective)
        # for num in map(str,[10,8,6,3,4,5]):
        for num in map(str,[8,10,6,3,4,5]):
            try:
                url = url_pattern.replace("{NUM}",num)
                content =  urllib2.urlopen(url).read() 
                data = json.loads(content)
                break
            except: print "Failed to perform URL fetching and decoding (using uaf-%s)!" % num
            if "test" in BASE_URL_PATTERN: break

    return data

def listofdicts_to_table(lod):
    colnames = list(set(sum([thing.keys() for thing in lod],[])))

    # key is col name and value is maximum length of any entry in that column
    d_colsize = {}
    for thing in lod:
        for colname in colnames:
            val = str(thing.get(colname,""))
            if colname not in d_colsize: d_colsize[colname] = len(colname)+1
            d_colsize[colname] = max(len(val)+1, d_colsize[colname])

    # sort colnames from longest string lengths to shortest
    colnames = sorted(colnames, key=d_colsize.get, reverse=True)

    try:
        from pytable import Table
        if not sys.stdout.isatty():
            raise Exception

        tab = Table()
        tab.set_column_names(colnames)

        for row in lod:
            tab.add_row([row.get(colname) for colname in colnames])
        tab.sort(column=colnames[0], descending=False)
                
        return "".join(tab.get_table_string())

    except:
        buff = ""
        header = ""
        for icol,colname in enumerate(colnames):
            header += ("%%%s%is" % ("-" if icol==0 else "", d_colsize[colname])) % colname
        buff += header + "\n"
        for thing in lod:
            line = ""
            for icol,colname in enumerate(colnames):
                tmp = "%%%s%is" % ("-" if icol==0 else "", d_colsize[colname])
                tmp = tmp % str(thing.get(colname,""))
                line += tmp
            buff += line + "\n"
                
        return buff

        
def get_output_string(q, typ="basic", detail=False, show_json=False, pretty_table=False):
    buff = ""
    data = query(q, typ, detail)

    if not data:
        return "URL fetch/decode failure"

    if data["response"]["status"] != "success":
        return "DIS failure: %s" % data["response"]["fail_reason"]

    data = data["response"]["payload"]
    
    if show_json:
        return json.dumps(data, indent=4)


    if type(data) == dict:
        if "files" in data: data = data["files"]


    if type(data) == list:

        if pretty_table:
            buff += listofdicts_to_table(data)
        else:
            for elem in data:
                if type(elem) == dict:
                    for key in elem:
                        buff += "%s:%s\n" % (key, elem[key])
                else:
                    buff += str(elem)
                buff += "\n"

    elif type(data) == dict:
        for ikey,key in enumerate(data):
            buff += "%s: %s\n\n" % (key, data[key])


    # ignore whitespace at end
    buff = buff.rstrip()
    return buff

def test(one=False):

    queries = [
    {"q":"/*/CMSSW_8_0_5*RelVal*/MINIAOD","typ":"basic","detail":False},
    {"q":"/SingleMuon/CMSSW_8_0_5-80X_dataRun2_relval_v9_RelVal_sigMu2015C-v1/MINIAOD","typ":"files","detail":True},
    {"q":"/GJets*/*/*","typ":"snt","detail":True},
    {"q":"/GJets*/*/* | grep cms3tag,dataset_name","typ":"snt","detail":False},
    {"q":"* | grep nevents_out","typ":"snt","detail":False},
    {"q":"/GJets_HT-600ToInf_TuneCUETP8M1_13TeV-madgraphMLM-pythia8/RunIISpring15DR74-Asympt25ns_MCRUN2_74_V9-v1/MINIAODSIM","typ":"mcm","detail":True},
    {"q":"/GJets*/*/* | grep cms3tag,dataset_name","typ":"snt","detail":False,"pretty_table":True},
    ]
    if one: queries = queries[3:4]
    for q_params in queries:
        print get_output_string(**q_params)

if __name__ == '__main__':
    
    # test(one=True)

    parser = argparse.ArgumentParser()
    parser.add_argument("query", help="query")
    parser.add_argument("-t", "--type", help="type of query")
    parser.add_argument("-d", "--detail", help="show more detailed information", action="store_true")
    parser.add_argument("-j", "--json", help="show output as full json", action="store_true")
    parser.add_argument("-p", "--table", help="show output as pretty table", action="store_true")
    parser.add_argument("-v", "--dev", help="use developer instance", action="store_true")
    args = parser.parse_args()

    
    if args.dev: 
        print ">>> Using dev instance"
        BASE_URL_PATTERN = BASE_URL_PATTERN.replace("disMaker","test_disMaker")

    if not args.type: args.type = "basic"

    print get_output_string(args.query, typ=args.type, detail=args.detail, show_json=args.json, pretty_table=args.table)

