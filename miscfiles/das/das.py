import cli, json, sys

if(len(sys.argv) < 2):
    print "first argument must be dataset name!"
    sys.exit()

dataset = sys.argv[-1]

host = 'https://cmsweb.cern.ch'
query = 'file dataset={0}'.format(dataset)
idx, limit = 0, 0
debug, thr = 1, 300
ckey, cert = "", ""


data = cli.get_data(host, query, idx, limit, debug, thr, ckey, cert)

instance = data['data'][0]['das']['instance']


print "-"*20
totfiles, totsize, totevents = 0,0,0
for fe in data['data']:
    f = fe['file'][0]
    print f.keys()
    name, nevents, size, date = f['name'], f['nevents'], f['size'], f['modification_time']
    totfiles += 1
    totsize += size
    totevents += nevents
    print name, nevents, cli.size_format(size,10), date

print "-"*20
print "total number of files:", totfiles
print "total dataset size:", cli.size_format(totsize,10)
print "total number of events:", totevents
print "url: https://cmsweb.cern.ch/das/request?input=file%20dataset%3D{0}&instance={1}&idx=0&limit=0".format(dataset, instance)
print "instance:", instance

