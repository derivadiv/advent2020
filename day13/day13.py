import math
import re
from functools import reduce

INT_MATCH = re.compile(r'\d+')

# maxtime non-inclusive
# ended up not using this for part 1, but a bit for part 2
def busdeparturetimes(busid, start = 0, maxtime = 60):
    times = []
    for i in range(math.ceil(maxtime/busid)):
        times.append(start + busid * i)
    return times

def parseinput(filename):
    with open(filename, 'r') as f:
        departtime = int(f.readline().strip())
        busids = [int(x) for x in f.readline().strip().split(',') if INT_MATCH.match(x)]
        return (departtime, busids)

# 5, 60, can depart at 60. 60/5 = 12 exactly
# 5, 59, can depart at 60. 59/5 = floor 11 ceil 12
# 5, 56, can depart at 60. 56/5 = floor 11 ceil 12
def firstbustimeafter(busid, starttime):
    multiplier = math.ceil(starttime/busid)
    return busid * multiplier

def firstbus(departtime, busids):
    times = [firstbustimeafter(bus, departtime) for bus in busids]
    mintime = min(times)
    busid = busids[times.index(mintime)]
    # (busid, wait time)
    return (busid, mintime - departtime)

def run(filename):
    (departtime, busids) = parseinput(filename)
    (busid, waittime) = firstbus(departtime, busids)
    return busid * waittime

# print(run('testinput1.txt'))
# print(run('input13.txt'))

# Part 2: don't need departure time, but x is now "wildcard".
def parseinput2(filename):
    with open(filename, 'r') as f:
        f.readline()
        busids = []
        for x in f.readline().strip().split(','):
            if INT_MATCH.match(x):
                busids.append(int(x))
            else:
                busids.append(None)
        return busids

"""
# Input isn't all that big:
print(len(parseinput2('input13.txt')))
# 62 
print(sorted([x for x in parseinput2('input13.txt') if x is not None]))
# [13, 17, 19, 23, 29, 37, 41, 619, 997]
Map {offset: busid} looks like
{0: 13, 3: 41, 13: 997, 21: 23, 32: 19, 42: 29, 44: 619, 50: 37, 61: 17}

Chinese Remainder Theorem: https://mathworld.wolfram.com/ChineseRemainderTheorem.html
with x % busI = aI, 
solution = sum(aI*y) where y % busI = 1, or y = (busI*n + 1) for any int n
   - nI is moderately bounded: 0 to max. product(busI) / busI
"""

def firstCoefficient(mult, modulus):
    # answer * mult % modulus = 1
    # = (answer % modulus) * (mult % modulus) % modulus.
    # so we should only need to test answers up to modulus
    factor = mult % modulus
    for b in range(modulus):
        if (b*factor) % modulus == 1:
            return b
    return None

def solution2(busidmap, busproduct):
    naiveTotal = 0
    for offset in busidmap:
        bus = busidmap[offset]
        # (x+offset) % bus = 0; x % bus = (bus - offset) % bus
        a = bus - offset
        # (b * product / bus) % bus = 1
        # b = 1 + (bus * some n we don't know)
        maxN = int(busproduct / bus)
        # overall solution part is a * b * maxN
        # where b * maxN % bus = 1; so
        b = firstCoefficient(maxN, bus)
        naiveTotal += (a * b * maxN)
    return naiveTotal % busproduct

"""
busidmap = {0:67, 1:7, 2:59, 3:61}
busproduct = 67*7*59*61
print(solution2(busidmap, busproduct))
"""

def trySolve(filename):
    busids = parseinput2(filename)
    print(busids)
    busidmap = {}
    factorproduct = 1
    for j in range(len(busids)):
        bus = busids[j]
        if bus is not None:
            # offsets meant bus ids were getting overwritten, oops
            busidmap[j] = bus
            factorproduct *= bus
    print(busidmap.values())
    print(factorproduct)
    return solution2(busidmap, factorproduct)

print(trySolve('input13.txt'))
