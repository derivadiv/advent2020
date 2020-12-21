def neighbors(poslist):
    if len(poslist) == 0:
        return []
    if len(poslist) == 1:
        return [[poslist[0] - 1], [poslist[0] + 1]]
    allpos = []
    # add neighbors where curpos has changed
    curpos = poslist[0]
    allpos.append([curpos + 1] + poslist[1:])
    allpos.append([curpos - 1] + poslist[1:])
    otherpos = neighbors(poslist[1:])
    # add neighbors where otherpos have changed
    for pos in otherpos:
        allpos.append([curpos + 1] + pos)
        allpos.append([curpos] + pos)
        allpos.append([curpos - 1] + pos)
    return allpos

def activeFromGrid(initGrid):
    activeLocs = []
    z = 0
    for y in range(len(initGrid)):
        for x in range(len(initGrid[y])):
            if initGrid[y][x] == '#':
                activeLocs.append([x, y, z])
    return activeLocs

def processCycle(activeLocs):
    # state changes will only happen around activeLocs.
    # could probably optimize to activeLocs' neighbors, but skipping for now
    xs = [x[0] for x in activeLocs]
    ys = [x[1] for x in activeLocs]
    zs = [x[2] for x in activeLocs]
    minX = min(xs) - 1
    maxX = max(xs) + 2
    minY = min(ys) - 1
    maxY = max(ys) + 2
    minZ = min(zs) - 1
    maxZ = max(zs) + 2
    newActiveLocs = []
    for x in range(minX, maxX):
        for y in range(minY, maxY):
            for z in range(minZ, maxZ):
                active = [x,y,z] in activeLocs
                neigh = neighbors([x,y,z])
                numActiveNeighbors = 0
                for n in neigh:
                    if n in activeLocs:
                        numActiveNeighbors += 1
                if active and (numActiveNeighbors in [2,3]):
                    newActiveLocs.append([x,y,z])
                elif (not active) and numActiveNeighbors == 3:
                    newActiveLocs.append([x,y,z])
    return newActiveLocs

def run1(inputfilename, numCycles):
    initGrid = []
    with open(inputfilename) as f:
        for line in f:
            initGrid.append(line.strip())
    activeLocs = activeFromGrid(initGrid)
    for i in range(numCycles):
        activeLocs = processCycle(activeLocs)
    return len(activeLocs)
                    
# print(run1('testinput1.txt', 3))
# print(run1('testinput1.txt', 6))
# print(run1('input17.txt', 6))

def activeFrom4DGrid(initGrid):
    activeLocs = []
    w = 0
    z = 0
    for y in range(len(initGrid)):
        for x in range(len(initGrid[y])):
            if initGrid[y][x] == '#':
                activeLocs.append([x, y, z, w])
    return activeLocs

def processCycle4D(activeLocs):
    # state changes will only happen around activeLocs.
    # this time probably need to limit to activeLocs and neighbors
    neighborsFreq = {} # map of inactive pos tuple to # neighboring active
    newActiveLocs = []
    # first consider already active locs (but can add to neighbors)
    for pos in activeLocs:
        numActiveNeighbors = 0
        for n in neighbors(pos):
            if n in activeLocs:
                # active neighbor, will be considered in activeLocs loop
                numActiveNeighbors += 1
            else:
                # inactive neighbor to consider separately
                tupn = tuple(n)
                if tupn not in neighborsFreq:
                    neighborsFreq[tupn] = 0
                neighborsFreq[tupn] += 1
        if numActiveNeighbors == 2 or numActiveNeighbors == 3:
            newActiveLocs.append(pos)
    # now consider all inactive neighbors of active pos
    for pos in neighborsFreq:
        if neighborsFreq[pos] == 3:
            newActiveLocs.append(list(pos))
    return newActiveLocs

def run2(inputfilename, numCycles):
    initGrid = []
    with open(inputfilename) as f:
        for line in f:
            initGrid.append(line.strip())
    activeLocs = activeFrom4DGrid(initGrid)
    for i in range(numCycles):
        activeLocs = processCycle4D(activeLocs)
    return len(activeLocs)

# print(run2('testinput1.txt', 6))
print(run2('input17.txt', 6))
