import math
import re

MEM_PATTERN = r'mem\[(?P<location>\d+)\]\s*\=\s*(?P<numwrite>\d+)\s*'
MEM_COMPILE = re.compile(MEM_PATTERN)

# i = 1, mask_str[34] = 0, 
# "XXXXXXXXXXXXXXXXXXXXXXXXXXXXX1XXXX0X"
def process_mask(mask_str):
    n = len(mask_str)
    mask_places = {}
    for i in range(n):
        val = mask_str[n-i-1]
        if val != 'X':
            mask_places[i] = int(val)
    return mask_places

# returns all powers where binary representation has 1 in digit
def decimal2binary(num):
    powers = []
    remainder = num
    while remainder > 0:
        nearestpower = math.floor(math.log2(remainder))
        powers.append(nearestpower)
        remainder = remainder - (2**nearestpower)
    return powers

def default(maxlen):
    d = {}
    for i in range(maxlen):
        d[i] = 0
    return d

def binary2decimal(dict_places):
    num = 0
    for digit in dict_places:
        if dict_places[digit] == 1:
            num += (2**digit)
    return num

def newdecimal(num, maskplaces, maxlen):
    dec = default(maxlen) # always starting anew?
    powers = decimal2binary(num)
    for p in powers:
        dec[p] = 1
    for m in maskplaces:
        dec[m] = maskplaces[m]
    return binary2decimal(dec)

def run1(inputfilename):
    memory = {}
    with open(inputfilename, 'r') as f:
        # defaults
        maskplaces = {}
        masklen = 36
        for line in f:
            m = MEM_COMPILE.match(line.strip())
            if m is None:
                mask = line.split('=')[1].strip()
                maskplaces = process_mask(mask)
                masklen = len(mask)
            else:
                loc = int(m.group('location'))
                num = int(m.group('numwrite'))
                memory[loc] = newdecimal(num, maskplaces, masklen)
    return sum(memory.values())

print(run1('testinput1.txt'))
print(run1('input14.txt'))

"""
Part 2: mask modifies bit
- can still store decimal in memory, but potentially way more bits
- need combos for all X
- length is pretty fixed at 36, no need to support changes
"""

def defaultstr(maxlen):
    d = []
    for i in range(maxlen):
        d.append('0')
    return d

def newbinstr(num, maskstr):
    n = len(maskstr)
    binstr = defaultstr(n)
    powers = decimal2binary(num)
    for p in powers:
        binstr[n-p-1] = '1'
    for i in range(len(maskstr)):
        bit = maskstr[i]
        # skip bit = 0
        if bit == '1':
            binstr[i] = '1'
        if bit == 'X':
            binstr[i] = 'X'
    return binstr

def allXcombos(xpowers):
    n = len(xpowers)
    if n == 0:
        return []
    newpossibility = 2**xpowers[0]
    if n == 1:
        return [newpossibility, 0]
    later = allXcombos(xpowers[1:])
    return later + [newpossibility + x for x in later]

def allvalues(binstr):
    # X means both values.
    xs = []
    n = len(binstr)
    basenum = {}
    for i in range(n):
        if binstr[i] == 'X':
            xs.append(n - i - 1)
            basenum[n - i - 1] = 0
        else:
            basenum[n - i - 1] = int(binstr[i])
    basenum = binary2decimal(basenum)
    return [basenum + x for x in allXcombos(xs)]

def run2(inputfilename):
    memory = {} # maps location to binary string
    with open(inputfilename, 'r') as f:
        for line in f:
            m = MEM_COMPILE.match(line.strip())
            if m is None:
                maskstr = line.split('=')[1].strip()
            else:
                loc = int(m.group('location'))
                num = int(m.group('numwrite'))
                masklocstr = newbinstr(loc, maskstr)
                masklocs = allvalues(masklocstr)
                for maskloc in masklocs:
                    memory[maskloc] = num
    return sum(memory.values())

print(run2('testinput2.txt'))
print(run2('input14.txt'))
