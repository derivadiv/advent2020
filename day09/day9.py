
def getnumfrom(line):
    return int(line.strip())

def getpreamble(fhandle, prelength):
    preamble = []
    for i in range(prelength):
        preamble.append(getnumfrom(fhandle.readline()))
    return preamble

def pairsums(preamble):
    # If every key maps to the pairsums with the numbers after it, when we
    # move the preamble forwards we can just remove the head key and add
    # sums with the new tail number. We don't need to know the other
    # numbers that made up the sum either (though ofc we could derive that).
    # Note that the tail key maps to an empty list - on purpose. 
    cache = {}
    for i in range(len(preamble)):
        firstnum = preamble[i]
        # we expect sums to be unique anyway, if we expect other
        # numbers in preamble range to be different. but even if not,
        # keep a list for counting purposes (see updatepairsums).
        cache[firstnum] = []
        for j in range(i+1, len(preamble)):
            secondnum = preamble[j]
            cache[firstnum].append(firstnum + secondnum)
    return cache

def updatepairsums(cache, newnum):
    # the head key is the one with the most individual sums,
    # specifically, = len(preamble) - 1
    head = [k for k in cache if len(cache[k]) == (len(cache) - 1)][0]
    del cache[head]
    for k in cache:
        newsom = k + newnum
        cache[k].append(newsom)
    cache[newnum] = []
    return cache

def isvalid(newnum, cache):
    for k in cache:
        for pairsum in cache[k]:
            if pairsum == newnum:
                return True
    return False

# part 1
def iterateUntilInvalid(filename, n):
    with open(filename, 'r') as f:
        preamble = getpreamble(f, n)
        cache = pairsums(preamble)
        for line in f:
            newnum = getnumfrom(line)
            if not isvalid(newnum, cache):
                return newnum
            updatepairsums(cache, newnum)

print(iterateUntilInvalid('testinput9.txt', 5)) #127 
print(iterateUntilInvalid('input9.txt', 25)) #393911906 

# part 2
def updatecontiguoussums(cache, newnum):
    # key is start num. value is a list of numbers from startnum to newnum.
    for k in cache:
        cache[k].append(newnum)
    cache[newnum] = [newnum]
    return cache

def iterateUntilSum(filename, desiredSum):
    cache = {}
    with open(filename, 'r') as f:
        for line in f:
            newnum = getnumfrom(line)
            cache = updatecontiguoussums(cache, newnum)
            for k in cache:
                if sum(cache[k]) == desiredSum:
                    return min(cache[k]) + max(cache[k])

print(iterateUntilSum('testinput9.txt', 127))
print(iterateUntilSum('input9.txt', 393911906))
