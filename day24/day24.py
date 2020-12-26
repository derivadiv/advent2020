"""
Coordinate systems - let's try odd-r horizontal layout
https://www.redblobgames.com/grids/hexagons/#coordinates-offset

- if row is even: (x,y) for y%2 = 0:
    - NE = (x, y+1) ;  NW = (x-1, y+1)
    - E = (x+1, y) ; W = (x-1, y)
    - SE = (x, y-1) ; SW = (x-1, y-1)

- if row is odd: (x,y) for y%2 = 1:
    - NE = (x+1, y+1) ; NW = (x, y+1)
    - E = (x+1, y) ; W = (x-1, y)  <- SAME
    - SE = (x+1, y-1); SW = (x, y-1)

Shared rules?
  - NE = (x + (y%2), y+1); NW = (x - 1 + (y%2), y+1)
  - SE = (x + (y%2), y-1); SW = (x - 1 + (y%2), y-1)

N and S x offsets differ depending on y being odd or even
"""

def applyDirection(x, y, direction):
    add = y % 2
    if direction == 'e':
        return (x+1, y)
    elif direction == 'w':
        return (x-1, y)
    elif direction == 'ne':
        return (x + add, y + 1)
    elif direction == 'nw':
        return (x - 1 + add, y + 1)
    elif direction == 'se':
        return (x + add, y - 1)
    elif direction == 'sw':
        return (x -1 + add, y - 1)
    print("Unknown direction " + direction)
    return (x, y)

def applyDirections(line, ref = (0,0)):
    unused = [char for char in line]
    (x,y) = ref
    while len(unused) > 0:
        direction = unused.pop(0)
        if direction in ['n','s']: # need to add east/west
            direction += unused.pop(0)
        (x,y) = applyDirection(x,y,direction)
    return (x,y)

def getDirections(line):
    unused = [char for char in line]
    directions = []
    while len(unused) > 0:
        direction = unused.pop(0)
        if direction in ['n','s']: # need to add east/west
            direction += unused.pop(0)
        directions.append(direction)
    return directions

# 1 dir1 + 1 dir2 = 0 net movement
def cancelDirs(directions, dir1, dir2):
    netDirs = []
    diff12 = directions.count(dir1) - directions.count(dir2)
    if diff12 > 0:
        for i in range(diff12):
            netDirs.append(dir1)
    elif diff12 < 0:
        for i in range(-diff12):
            netDirs.append(dir2)
    return netDirs

# 1 dir1 + 1 dir2 = 1 netdir
def combineDirs(directions, dir1, dir2, netdir):
    netDirs = []
    count1 = directions.count(dir1)
    count2 = directions.count(dir2)
    for i in range(min(count1, count2)):
        netDirs.append(netdir)
    # still need to add leftover directions
    diff12 = count1 - count2
    if diff12 > 0:
        for i in range(diff12):
            netDirs.append(dir1)
    elif diff12 < 0:
        for i in range(-diff12):
            netDirs.append(dir2)
    return netDirs

def netDirections(directions):
    # order arguably shouldn't matter?
    netDirs = []
    # ne + sw cancel out?
    netDirs.extend(cancelDirs(directions, 'ne', 'sw'))
    # se + nw cancel out?
    netDirs.extend(cancelDirs(directions, 'se', 'nw'))
    # ne + se is just east?
    addEastDirs = combineDirs(netDirs, 'ne', 'se', 'e')
    # same for nw and sw
    addWestDirs = combineDirs(netDirs, 'nw', 'sw', 'w')
    # e + w cancel out
    eastWestDirs = cancelDirs(directions, 'e', 'w')
    return addEastDirs + addWestDirs + eastWestDirs

def netApplyDirections(line, ref = (0,0)):
    directions = getDirections(line)
    directions = netDirections(directions)
    (x,y) = ref
    for direction in directions:
        (x,y) = applyDirection(x,y,direction)
    return (x,y)

def flipTiles(inputFileName):
    flippedTiles = set()
    with open(inputFileName) as f:
        for line in f:
            (x,y) = netApplyDirections(line.strip())
            if (x,y) in flippedTiles:
                flippedTiles.remove((x,y))
            else:
                flippedTiles.add((x,y))
    print(len(flippedTiles))
    return flippedTiles

"""
print(applyDirections('esew'))
print(netApplyDirections('esew'))
print(applyDirections('nwwswee'))
print(netApplyDirections('nwwswee'))
print(flipTiles('testinput1.txt'))
print(flipTiles('input24.txt'))
"""

def getNeighborTiles(pos):
    neighbors = []
    (x,y) = pos
    dirs = ['e','w','ne','se','nw','sw']
    for d in dirs:
        neighbors.append(applyDirection(x,y,d))
    return neighbors

def tupleToHashStr(pos):
    return '(' + ','.join([str(x) for x in pos]) + ')'

def hashStrToPosTuple(hashstr):
    parts = hashstr[1:-1].split(',')
    return (int(parts[0]), int(parts[1]))

def runDay(startTiles):
    endTiles = set()
    for tile in startTiles:
        endTiles.add(tile)
    # maps a white tile to number of neighboring black tiles
    neighbors = {}
    for tile in startTiles:
        tileNeighbors = getNeighborTiles(tile)
        countBlackTiles = 0
        for neighbor in tileNeighbors:
            if neighbor in startTiles:
                # neighbor is a black tile
                countBlackTiles += 1
            else:
                # neighbor is a white tile (but has this black tile as a neighbor!)
                neighborkey = tupleToHashStr(neighbor)
                if neighborkey not in neighbors:
                    neighbors[neighborkey] = 0
                neighbors[neighborkey] += 1
        if countBlackTiles == 0 or countBlackTiles > 2:
            # flip to white
            endTiles.remove(tile)
    for tilekey in neighbors:
        if neighbors[tilekey] == 2:
            # flip to black
            endTiles.add(hashStrToPosTuple(tilekey))
    return endTiles

"""
start = flipTiles('testinput1.txt')
day = runDay(start)
for i in range(1, 11):
    print(i)
    print(len(day))
    day = runDay(day)
for i in range(11, 101):
    if i%10 == 0:
        print(i)
        print(len(day))
    day = runDay(day)
"""
start = flipTiles('input24.txt')
day = runDay(start) # day 1
for i in range(1, 100): # runs 99x
    day = runDay(day)
print(len(day))
