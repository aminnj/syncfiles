from datetime import date
import random, os, time

BLUE = '\033[94m'
GREEN = '\033[92m'
GREEN2 = '\033[32m'
PURPLE = '\033[95m'
CYAN = '\033[36m'
WHITEONRED = '\033[1;39;41m'
REDBG = '\033[101m'
YELLOW = '\033[93m'
RED = '\033[41m'
ENDC = '\033[0m'

def purple(txt): return PURPLE + str(txt) + ENDC
def cyan(txt): return CYAN + str(txt) + ENDC
def green(txt): return GREEN + str(txt) + ENDC
def green2(txt): return GREEN2 + str(txt) + ENDC
def yellow(txt): return YELLOW + str(txt) + ENDC
def blue(txt): return BLUE + str(txt) + ENDC
def red(txt): return WHITEONRED + str(txt) + ENDC


lines = [line.strip() for line in open("majorsystem2.txt","r").readlines()]

isCorrect = False

wordnums = []
for line in lines:
    number, words = line.split("|")
    wordnums.append([int(number),words.split(",")]) 

while(not isCorrect):
    t1 = time.time()

    pair = random.choice(wordnums)
    num = pair[0]
    word = random.choice(pair[1])

    tips = """
    0 = S, Z, and soft c (as in city)
    1 = T, D, and th (as in the)
    2 = N
    3 = M
    4 = R
    5 = L
    6 = J, the sh, ch, dg, and soft g (as in age) sounds
    7 = K, Q, the hard c (as in can), the hard g (as in go) sounds
    8 = F and V
    9 = P and B
    """

    print tips
    inputDay = raw_input("Enter number for '%s': " % (green(word)) )
    if(inputDay == str(num)):
        isCorrect = True

        print "Correct!"
        print "Took you %d seconds to answer." % (time.time() - t1)
        time.sleep(1)
        os.system("exit")
    else:
        isCorrect = False
        print "Wrong. Correct answer:", num
        time.sleep(1)
    print "\n"

