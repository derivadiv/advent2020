# grid is 2D array OR array of Strings.
# seatrow is outer grid index, seatcol is inner grid index
def adjacentToSeat(grid, seatrow, seatcol):
    adj = []
    r = len(grid)
    # assume all rows are same width (same num of columns)
    c = len(grid[seatrow])
    # also assume seatrow and seatcol are valid within grid
    if (seatrow - 1) >= 0:
        if (seatcol - 1) >= 0:
            adj.append(grid[seatrow-1][seatcol-1])
        adj.append(grid[seatrow-1][seatcol])
        if (seatcol + 1) < c:
            adj.append(grid[seatrow-1][seatcol + 1])
    if (seatcol - 1) >= 0:
        adj.append(grid[seatrow][seatcol-1])
    if (seatcol + 1) < c:
        adj.append(grid[seatrow][seatcol + 1])
    if (seatrow + 1) < r:
        if (seatcol - 1) >= 0:
            adj.append(grid[seatrow+1][seatcol-1])
        adj.append(grid[seatrow+1][seatcol])
        if (seatcol + 1) < c:
            adj.append(grid[seatrow+1][seatcol + 1])
    return adj

def newState(seat, adjseats):
    numOccupied = adjseats.count('#')
    if seat == 'L' and numOccupied == 0:
        # seat becomes occupied
        return '#'
    if seat == '#' and numOccupied >= 4:
        # seat becomes empty
        return 'L'
    # assume no change otherwise
    return seat

def newRound(grid):
    isSameGrid = True
    newgrid = []
    for r in range(len(grid)):
        newrow = []
        for c in range(len(grid[r])):
            adj = adjacentToSeat(grid, r, c)
            state = newState(grid[r][c], adj)
            if grid[r][c] != state:
                isSameGrid = False
            newrow.append(state)
        newgrid.append(newrow)
    return (isSameGrid, newgrid)

def firstGrid(filename):
    grid = []
    with open(filename, 'r') as f:
        for line in f:
            line = line.strip()
            if len(line) > 0:
                grid.append([x for x in line])
    return grid

def numOccupiedInGrid(grid):
    occupiedCount = 0
    for row in grid:
        occupiedCount += row.count('#')
    return occupiedCount

def iterateUntilStable(filename, maxn = 100):
    grid = firstGrid(filename)
    i = 0
    while i < maxn:
        (isSameGrid, newgrid) = newRound(grid)
        if isSameGrid:
            return numOccupiedInGrid(newgrid)
        grid = newgrid
        i += 1
    return "No luck after " + str(i) + " iterations"

print(iterateUntilStable('testinput1.txt'))
# print(iterateUntilStable('input11.txt'))

# Part 2: first visible seat in any direction

# upstep can be (-1, 0, 1) and rightstep can be (-1, 0, 1).
# all combos allowed except (upstep, rightstep) = (0,0)

ALLOWED_STEPS = [(-1,-1), (-1,0), (-1,1), (0,-1), (0,1), (1,-1), (1,0), (1,1)]

def checkDirection(grid, startrow, startcol, upstep, rightstep):
    assert not (upstep == 0 and rightstep == 0)
    r = startrow + upstep
    c = startcol + rightstep
    while (r >= 0 and r < len(grid)) and (c >= 0 and c < len(grid[r])):
        adjseat = grid[r][c]
        # the floor ain't lava
        if adjseat != '.':    
            return adjseat
        r += upstep
        c += rightstep
    return ''

def visibleToSeat(grid, seatrow, seatcol):
    adj = []
    r = len(grid)
    # assume all rows are same width (same num of columns)
    c = len(grid[seatrow])
    for (up, right) in ALLOWED_STEPS:
        adjseat = checkDirection(grid, seatrow, seatcol, up, right)
        if len(adjseat) == 1:
            adj.append(adjseat)
    return adj

def updatedState(seat, adjseats):
    numOccupied = adjseats.count('#')
    if seat == 'L' and numOccupied == 0:
        # seat becomes occupied
        return '#'
    if seat == '#' and numOccupied >= 5:
        # seat becomes empty
        return 'L'
    # assume no change otherwise
    return seat

def updatedRound(grid):
    isSameGrid = True
    newgrid = []
    for r in range(len(grid)):
        newrow = []
        for c in range(len(grid[r])):
            adj = visibleToSeat(grid, r, c)
            state = updatedState(grid[r][c], adj)
            if grid[r][c] != state:
                isSameGrid = False
            newrow.append(state)
        newgrid.append(newrow)
    return (isSameGrid, newgrid)

def updatedIterateUntilStable(filename, maxn = 100):
    grid = firstGrid(filename)
    i = 0
    while i < maxn:
        (isSameGrid, newgrid) = updatedRound(grid)
        if isSameGrid:
            return numOccupiedInGrid(newgrid)
        grid = newgrid
        i += 1
    return "No luck after " + str(i) + " iterations"

print(updatedIterateUntilStable('testinput1.txt'))
print(updatedIterateUntilStable('input11.txt'))
