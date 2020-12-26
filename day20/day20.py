import re

TILE_CMP = re.compile(r'Tile (\d+):')

def getTilesFromFile(input_filename):
    lastTile = None
    tiles = {}
    with open(input_filename) as f:
        for line in f:
            m = TILE_CMP.match(line.strip())
            if m:
                print(m.group(1))
                lastTile = int(m.group(1))
                tiles[lastTile] = []
            elif len(line.strip()) > 0:
                tiles[lastTile].append(line.strip())
    return tiles

# returns borders: top, right down, lower reverse, left up
def getClockwiseBordersFromTile(list_strs):
    rightdown = ''
    leftup = ''
    lower = list_strs[-1][::-1]
    for row in list_strs:
        rightdown = rightdown + row[-1]
        leftup = row[0] + leftup
    return [list_strs[0], rightdown, lower, leftup]

# first row is last column, and onwards.
# last row is first column
def rotateTileClockwise(list_strs):
    numrows = len(list_strs)
    numcols = len(list_strs[0])
    newTile = ['' for i in range(numcols)]
    for r in range(numrows):
        for c in range(numcols):
            newTile[c] += list_strs[numrows-r-1][c]
    return newTile

# first low is last row
def flipTileHorizontal(list_strs):
    newTile = []
    numrows = len(list_strs) 
    for r in range(numrows):
        newTile.append(list_strs[numrows - r - 1])
    return newTile

def betterTilePrint(tile):
    for row in tile:
        print(row)
    print()

def getSharedBorders(tiles):
    borders = {} # stores border : tiles that match any direction.
    for tile in tiles:
        for border in getClockwiseBordersFromTile(tiles[tile]):
            if border in borders:
                borders[border].append(tile)
            elif border[::-1] in borders:
                # include flips (tbd whether it needs a different dictionary)
                borders[border[::-1]].append(tile)
            else:
                borders[border] = [tile]
    return borders

# 4 corner tiles: 2 unmatched borders, 2 matched borders
# (rows + cols -4)*2 inner edge tiles: 1 unmatched border, 3 matched
# (rows - 1)*(cols-1) innermost tiles, all matched borders

def getCornerTiles(tiles, borders):
    cornerTiles = set()
    numUnmatchedBorders = {}
    for t in tiles:
        numUnmatchedBorders[t] = 0
    for b in borders:
        if len(borders[b]) == 1:
            numUnmatchedBorders[borders[b][0]] += 1
    for n in numUnmatchedBorders:
        if numUnmatchedBorders[n] == 2:
            cornerTiles.add(n)
    
    return cornerTiles

tiles = getTilesFromFile('input20.txt')

# betterTilePrint(tiles[2311])
print()
borders = getSharedBorders(tiles)
print(getCornerTiles(tiles, borders))
