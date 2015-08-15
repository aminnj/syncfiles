# requires tesseract
# On mac: brew install tesseract
#         brew link tesseract
import pytesser as pt
import os,sys,commands
from PIL import Image
import datetime, time
import json

sys.path.append("/usr/local/bin/tesseract")

def cleanText(txt):
    newtxt = []
    for line in txt.split("\n"):
        if(len(line.strip())) < 1: continue
        newtxt.append(line.strip())
    return newtxt

# setup: get images, crop them
os.system("curl -o lhc.png https://vistar-capture.web.cern.ch/vistar-capture/lhc1.png")
os.system("curl -o cms.png https://cmspage1.web.cern.ch/cmspage1/data/page1.png")
imgCMS = Image.open("cms.png")
imgCMS.crop((0,0,800,30)).save("cmstop.png")
imgLHC = Image.open("lhc.png")
imgLHC.crop((0,0,1024,90)).save("lhctop.png")


# CMS subsystems
dy = (583.0-374)/13.0
systemsall = ["CSC","DT","ECAL","ES","HCAL","PIXEL","RPC","TRACKER","CASTOR","TRG","DAQ","DQM","SCAL","HF"]
systemsin = []
systemson = []
systemsgood = True
rgbimg = imgCMS.convert("RGB")
for i in range(14):
    coords = (498,374+i*dy)
    rgb = rgbimg.getpixel(coords)
    if(rgb[1] > 240): systemsin.append(systemsall[i])

for i in range(14):
    coords = (556,374+i*dy)
    rgb = rgbimg.getpixel(coords)
    if(rgb[1] > 240): systemson.append(systemsall[i])

for system in ["CSC","DT","ECAL","ES","HCAL","PIXEL","RPC","TRACKER","TRG","DAQ","DQM","SCAL","HF"]:
    if system not in systemsin: systemsgood = False
for system in ["CSC","DT","ECAL","ES","HCAL","PIXEL","RPC","TRACKER"]:
    if system not in systemson: systemsgood = False

print systemsin, systemson, systemsgood

# Magnetic field
txt = pt.image_to_string("cms.png")
bfield = -1.0
try:
    for line in cleanText(txt):
        if "[T]" not in line: continue
        bfield = float(line.split(" ")[-1])
except: 
    print "couldn't get bfield from:", txt
print "bfield",bfield


# Run number
txt = pt.image_to_string("cmstop.png")
run = -1
try:
    for item in cleanText(txt)[0].split():
        try:
            maybeRun = int(item)
            if maybeRun > 200000:
                run = maybeRun
        except:
            pass
except: 
    print "couldn't get run from:", txt
print "run",run

txt = pt.image_to_string("lhctop.png")

# Fill
fill = -1
try:
    fill = int(cleanText(txt)[0].split(":")[1].strip().split()[0])
except: 
    print "couldn't get fill from:", txt
print "fill",fill

# Energy
energy = -1
try:
    energy = int(cleanText(txt)[0].split(":")[2].strip().split()[0])
except: 
    print "couldn't get energy from:", txt
print "energy", energy

# Beam status
beam = ""
try:
    beam = cleanText(txt)[1].split(":")[1].strip().lower()
except: 
    print "couldn't get beam from:", txt
print "beam",beam

# Timestamp from monitor picture
timestamp, timestampparsed = "", 0
try:
    print txt
    print cleanText(txt)[0]
    print cleanText(txt)[0].split()[-2:]
    timestamp = " ".join(cleanText(txt)[0].split()[-2:]).strip()
    # 15-08-15 07:49:12
    timestampparsed = int(time.mktime(datetime.datetime.strptime(timestamp, "%d-%m-%y %H:%M:%S").timetuple()))
except: 
    print "couldn't get timestamp from:", txt
print "timestamp",timestamp


info = {}
info["bfield"] = bfield
info["systemsin"] = systemsin
info["systemson"] = systemson
info["run"] = run
info["fill"] = fill
info["energy"] = energy
info["beam"] = beam
info["realtime"] = int((datetime.datetime.now() + datetime.timedelta(hours=9)).strftime("%s"))
info["timestamp"] = timestamp
info["timestampparsed"] = timestampparsed

info["good"] = {}
info["good"]["beamsgood"] = "stable" in beam
info["good"]["systemsgood"] = systemsgood
info["good"]["bfieldgood"] = bfield > 3.7
info["good"]["energygood"] = energy > 6400
info["good"]["realtime"] = int((datetime.datetime.now() + datetime.timedelta(hours=9)).strftime("%s"))
info["good"]["timestampparsed"] = timestampparsed

print json.dumps(info, indent=4)
out = open("monitor.json","w")
out.write(json.dumps(info, indent=4))
out.close()

# os.system("scp monitor.json namin@uaf-6.t2.ucsd.edu:~/public_html/monitor.json")
