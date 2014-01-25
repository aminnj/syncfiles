import time, os, math, sys
from urllib2 import urlopen

class Histogram:
    """
    Histogram class
    
    You can initialize it as:
        import miscutils as mu
            h1 = mu.Histogram()
        OR  h1 = mu.Histogram([2,3,1,2,3])
    
    fill(val)           add val to points
    removeVal(val)      removes ALL values equal to input
    removeRange(x1,x2)  removes values within exclusive range
    getMean()           returns mean
    getRMS()            returns unbiased std deviation
    getMin()            returns minimum value
    getMax()            returns maximum value
    getPoints()         returns list of points
    getNumPoints()      returns number of points
    """
    def __init__(self, pts=[]):
        #points.sort()
        self.points = sorted(pts)
        self.mean = -1
        self.rms = -1
        self.maximum = -1
        self.minimum = -1
        self.numpoints = -1
        if(len(pts) > 0): self.calcParams()
        self.newpoints = False
        
    def calcParams(self):
        self.mean = self.calcMean(self.points)
        self.rms = self.calcRMS(self.points)
        self.maximum = max(self.points)
        self.minimum = min(self.points)
        self.numpoints = len(self.points)
        self.newpoints = False
        
    def fill(self, point):
        self.points.append(point)
        self.newpoints = True
        
    def calcMean(self, ls):
        return float(sum(ls))/len(ls)

    def calcRMS(self, ls):
        mu = self.calcMean(ls)
        sqdiff = [(x-mu)**2 for x in ls]
        if(len(sqdiff) == 1): return -1
        return math.sqrt(sum(sqdiff)/(len(sqdiff)-1)) #unbiased (n-1)
        
    def getMean(self):
        if(self.newpoints): self.calcParams()
        return self.mean
        
    def getRMS(self):
        if(self.newpoints): self.calcParams()
        return self.rms
        
    def getMax(self):
        if(self.newpoints): self.calcParams()
        return self.maximum
        
    def getMin(self):
        if(self.newpoints): self.calcParams()
        return self.minimum
        
    def getPoints(self):
        if(self.newpoints): self.calcParams()
        return self.points
        
    def getNumPoints(self):
        #if(self.newpoints): self.calcParams()
        return self.numpoints
        
    def removeVal(self, val):
        self.points = [x for x in self.points if not(x==val)]
        
    def removeRange(self, x1, x2):
        self.points = [x for x in self.points if not(x < x2 and x > x1)]

def dumpList(ls, filename, aw):
    """
    dumpList(list, filename, mode)
    
    Dumps list (1D or 2D) to specified file
    (appends if mode = 'a' and writes if mode = 'w')
    """
    if(not(aw == "a" or aw == "w")):
        print "Error: dumpList(list, filename, aw) where aw is \"a\" or \"w\""
        return
    out = open(filename, aw)
    for elem in ls:
        if(type(elem) == list or type(elem) == tuple):
            out.write("\t".join([str(i) for i in elem])+"\n")
        else:
            out.write(str(elem)+"\n")
    out.close()        

def dumpVal(val, filename, aw):
    """
    dumpVal(val, filename, mode)
    
    Dumps 1D list or single value to specified file
    (appends if mode = 'a' and writes if mode = 'w')
    """
    if(not(aw == "a" or aw == "w")):
        print "Error: dumpVal(val, filename, aw) where aw is \"a\" or \"w\""
        return
    out = open(filename, aw)
    if(type(val) == list or type(val) == tuple):
        out.write("\t".join([str(i) for i in val])+"\n")
    else:
        out.write(str(val)+"\n")
    out.close()

def readToList(filename, column=None):
    """
    readToList(filename, column=None)
    
    Reads file and returns contents as list
    List may have nested lists if multiple columns present
    
    If 'column' specified, will return 1D list
    using data in specified column (starts with 0)
    """
    ls = []
    input = open(filename, "r")
    for line in input.readlines():
        if(column is not None):
            ls.append(line.strip("\n").split("\t")[column])
        else:
            ls.append(line.strip("\n").split("\t"))
    return ls
    
def columnFromList(ls, column):
    """
    columnFromList(list, column=None)
    
    Takes list and returns specified column (indexed from 0)
    If certain element is not a nested list
    (i.e., 1 column for that element), element will be ignored
    and the number of malformed elements will be output.
    """
    ols = []
    malformed = 0
    
    for elem in ls:
        if((type(elem) == list or type(elem) == tuple) and len(elem) > column):
            ols.append(elem[column])
        else:
            malformed += 1
    if(malformed > 0):
        print "detected %i malformed (non-list/tuple or len < column) elements" % (malformed)        
    return ols
    
def fromListIfMatches(ls, checkCol, checkVal, column=None):
    """
    fromListIfMatches(list, checkCol, checkVal, column=None)
    
    Returns column of list if value in checkCol is equal to checkVal.
    
    If certain element is not a nested list
    (i.e., 1 column for that element), element will be ignored
    and the number of malformed elements will be output.
    
    If column not specified (by default), entire row will be returned
    if value in checkCol is equal to checkVal.
    """
    ols = []
    malformed = 0
    for elem in ls:
        if((type(elem) == list or type(elem) == tuple) and len(elem) > checkCol and elem[checkCol] ==checkVal):
            if(column is not None):
                if((type(elem) == list or type(elem) == tuple) and len(elem) > column):
                    ols.append(elem[column])
                else:
                    malformed += 1
            else:
                ols.append(elem)
    if(malformed > 0):
        print "detected %i malformed (non-list/tuple or len < column) elements" % (malformed)        
    return ols    

def removeDuplicates(ls,index=None):
    """
    removeDuplicates(list,index=None)
    
    Returns list with no duplicates.
    
    If index specified, duplication checking will be
    done by comparing the index'th value of each element
    (i.e., uniquification is done using a specified column
    of a 2D list, if specified)
    """
    outls = []
    checkls = []
    if(index is None):
        for elem in ls:
            if(elem not in outls):
                outls.append(elem)
    else:
        if(index < len(ls[0])):
            for elem in ls:
                try:
                    if(elem[index] not in checkls):
                        checkls.append(elem[index])
                        outls.append(elem)
                except IndexError: continue
                else: pass
        else:
            print "index out of range. returning input."
            return ls
    return outls
    
def mathematicaFormat(ls,variable=""):
    """
    mathematicaFormat(list,variable="")
    
    This function facilitates the conversion of python
    lists into mathematica lists without having to go into,
    say, Notepad++ and using regular expression replacements.
    
    If list is [1, 2, 3], this function will return
        " = {1, 2, 3};" as a string.
        
    If list is [1, 2, 3] and variable is "test",
    this function will return
        "test = {1, 2, 3};" as a string.
    """
    return str(variable) + " = {" + ", ".join([str(e) for e in ls]) + "};"
        
def avg(ls):
    """
    avg(list)
    
    Returns the average of the input list.
    """
    return float(sum(ls))/len(ls)
    
def sleep(t, verbose=False):
    """
    sleep(t, verbose=False)
    
    Sleeps for t seconds.
    
    If verbose is True, this prints "sleeping for %i seconds."
    and "done sleeping." on the same line.
    """
    if(verbose): print "sleeping for %i seconds." % (t),
    time.sleep(t)
    if(verbose): print "done sleeping."
    
def sleepForMins(mins):
    """
    sleepForMins(numMinutes)
    
    Sleeps for specified number of minutes. Displays a progress bar.
    """
    print "sleeping for " + str(mins) + " minutes.",
    for i in range(mins*10):
        time.sleep(6)
        progressbar(1.0*i/(mins*10), True)
    print "done sleeping for " + str(mins) + " minutes"
    
def ascii(s):
    """
    ascii(s)
    
    Returns input string after stripping non-ascii characters.
    """
    return s.encode('ascii','ignore')

def cls():
    """
    cls()
    
    Shorthand for os.system("cls")
    """
    os.system("cls")
    
def progressbar(fraction, continuous=True):
    """
    progressbar(fraction, continuous=False)
    
    Returns a bar like [################----] where the fill
    amount is determined by fraction.
    
    If continuous is true (default), then print line uses "\\r"
    to overwrite itself (no need to use cls() to clear screen
    to make it nice to see). However, only use this in 
    situations where things are not being printed out between
    progressbar() calls.
    
    If false, progress bar is printed on new line each time,
    so if necessary, must use cls() explicitly to make it
    look pretty.
    """
    width = 40
    if(fraction > 1): fraction = 1
    if(fraction < 0): fraction = 0
    filled = int(round(fraction*width))
    if continuous:
        print "\r[{0}{1}]".format("#" * filled, "-" * (width-filled)),
        print "%d%%" % (round(fraction*100)),
        #\r takes cursor to beginning of line, so it will overwrite itself
    else:
        print "[{0}{1}]".format("#" * filled, "-" * (width-filled)),
        print "%3d%%" % (round(fraction*100))
        
def readSiteToString(url):
    """
    readSiteToString(url)
    
    Returns as a string the contents of website at the url
    """
    return urlopen(url).read()

def gcd(n,d):
    """
    gcd(numerator, denominator)
    
    Returns the greatest common divisor of n/d
    """
    while(d):
        n, d = d, n%d
    return n
    
def isInt(a):
    """
    isInt(a)
    
    Returns True if a is integer
    """
    return not (a-int(a))
    
def digSum(n):
    """
    digSum(num)
    
    Returns sum of digits of num.
    Ex. If num = 123, digSum(num) = 6
    """
    s = 0
    while(n >= 1):
        s += n%10
        n //= 10
    return s
    
fcache = {}
def factorize(n):
    """
    factorize(n)
    
    Takes integer and returns prime factors. Prime factors
    are not uniquified, so multiplicity can be seen.
    """
    if n in fcache: return fcache[n]
    for d in xrange(2, int(n**0.5)+1):
        if n%d == 0:
            fcache[n] = factorize(n/d)+factorize(d)
            return fcache[n]
    fcache[n] = [n]
    return [n]
    
def primeSieve(n):
    """
    primeSieve(n)
    
    Returns list of primes up to integer n.
    Snippet from stackoverflow.com/questions/16004407.
    Note that primeSieve(10000)[37] gives the 38th prime
    due to zero-based indexing of lists in python.
    Generation of primes up to 100M takes 
    7 seconds, and returns list of length 5761509 (5.7M).
    """
    size = n//2
    sieve = [1]*size
    limit = int(n**0.5)
    for i in range(1,limit):
        if sieve[i]:
            val = 2*i+1
            tmp = ((size-1) - i)//val 
            sieve[i+val::val] = [0]*tmp
    return [2] + [i*2+1 for i, v in enumerate(sieve) if v and i>0]
    
def handleParams():
    """
    handleParams()
    
    Takes piped arguments and appends them to end of command line
    arguments. Returns a list.   
    """
    args = sys.argv
    if not sys.stdin.isatty():
        args += sys.stdin.read().replace('\n','').replace('\r','').split(' ')
        args = filter(None, args) # removes empty elems
    return args
    
t0 = {}
def startTimer(id="_"):
    """
    startTimer()
        
    Starts timing a block of code between {start,end}Timer functions.
    Accepts a timer ID to allow for multiple simultaneous timers.
    """
    global t0
    t0[id] = time.time()
    
def endTimer(id="_"):
    """
    endTimer()
    
    Ends timing between {start,end}Timer functions. Prints
    a message about run time and timer ID, if not default value.
    """
    global t0
    if(id not in t0):
        print "Timer ID of %s not found." % (id)
        return
    print "Running of %s took %.3f seconds." % (id,time.time()-t0[id])
    
def listToHistogram(ls):
    """
    listToHistogram()
    
    Returns a dictionary, where the keys are the unique
    elements of the input list, and the values are the
    number of occurences in the list.
    """
    dout = {}
    for elem in ls:
        if(elem not in dout.keys()):
            dout[elem] = 1
        else:
            dout[elem] += 1
    return dout
    
if __name__ == '__main__':

    print """
    Histogram - class
        fill(val)           add val to points
        removeVal(val)      removes ALL values equal to input
        removeRange(x1,x2)  removes values within exclusive range
        getMean()           returns mean
        getRMS()            returns unbiased std deviation
        getMin()            returns minimum value
        getMax()            returns maximum value
        getPoints()         returns list of points
        getNumPoints()      returns number of points
    dumpList - dumps 1/2D list to file
    dumpVal - dumps 1D list or single value to file
    readToList - reads file to list
    columnFromList - returns column from list
    fromListIfMatches - returns column if meets condition
    removeDuplicates - returns de-duplicated list
    mathematicaFormat - turns list into mathematica list
    avg - returns mean of list
    sleep - sleep for specified time in seconds
    sleepForMins - sleep with progress bar
    ascii - strips non-ascii characters from string
    cls - clear console screen
    progressbar - displays progressbar
    readSiteToString - reads URL html to string
    gcd - returns greatest common divisor
    isInt - checks if input is integer
    digSum - sums digits of input integer
    factorize - returns list of factors of integer
    primeSieve - returns list of primes up to integer n
    handleParams - returns list of piped and cmdline args
    startTimer - starts timer
    endTimer - ends timer; prints time between start, end
    listToHistogram - returns frequency dictionary of list
    """
