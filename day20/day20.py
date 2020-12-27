import re
import math

TILE_CMP = re.compile(r'Tile (\d+):')

def getTilesFromFile(input_filename):
    lastTile = None
    tiles = {}
    with open(input_filename) as f:
        for line in f:
            m = TILE_CMP.match(line.strip())
            if m:
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

# (rows - 1)*(cols-1) innermost tiles, all matched borders
# (rows + cols -4)*2 inner edge tiles: 1 unmatched border, 3 matched

"""
A bit of a shortcut for part 1; did not pay off for part 2
"""
# 4 corner tiles: 2 unmatched borders, 2 matched borders
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

"""
tiles = getTilesFromFile('input20.txt')

# betterTilePrint(tiles[2311])
print()
borders = getSharedBorders(tiles)
corners = getCornerTiles(tiles, borders)
"""

"""
Onwards is part 2 only.

Corners have distinct unmatched borders, but any of the
tiles could be either via rotation. Could find edge neighbors, graph search..
    uB2
    |
uB1-T1-mB1-T7?-...mB9-T10
    |      |
    mB2
    ...
    |
uB3-T3-              -T30
    |
    uB4

One of the corners can be the root node, and we can expand from there.
But it's not actually a tree, so we may end up in a loop.

Prereq will be figuring out how to handle matches - orienting tiles right.
T1 - B1 vs T2 - B1;  T2 will have to flip and rotate to match T1.

Keep one tile fixed, and transform everything else to match relative to that tile.
"""

# Keeps tile1 unchanged, and rotates/flips tile2 to match.
# They match when borders are in reverse order and opposite sides
# Returns transformed tile2 and index of matching border
def matchTilesAtBorder(tile1, tile2, border):
    # they can have max. 1 shared border anyway, but where is it?
    borders1 = getClockwiseBordersFromTile(tile1)
    if border not in borders1:
        # flip border to match tile1 orientation
        border = border[::-1]
        borders1 = getClockwiseBordersFromTile(tile1)
        assert border in borders1
    copy2 = [row for row in tile2]
    borders2 = getClockwiseBordersFromTile(tile2)
    if border in borders2:
        # flip tile2 to fit the reverse border
        copy2 = flipTileHorizontal(copy2)
        borders2 = getClockwiseBordersFromTile(copy2)
        assert border not in borders2
    # perfect match would be exact opposite (L and R, or Up and Down),
    loc1 = borders1.index(border)
    loc2 = borders2.index(border[::-1])
    # i.e. since there are 4 borders, loc1-loc2 % 4 = 2
    desiredLoc2 = (loc1 + 2) % 4
    while loc2 != desiredLoc2:
        # rotate it clockwise til it fits
        copy2 = rotateTileClockwise(copy2)
        borders2 = getClockwiseBordersFromTile(copy2)
        loc2 = borders2.index(border[::-1])
    return (copy2, loc2)

def orientTopLeft(tile, unmatchedBorder1, unmatchedBorder2):
    # make tile the top left corner, so unmatched borders are
    # up (0 in borders) and left (3 in borders)
    borders = getClockwiseBordersFromTile(tile)
    if unmatchedBorder1 not in borders:
        unmatchedBorder1.reverse()
    if unmatchedBorder2 not in borders:
        unmatchedBorder2.reverse()
    unmatchIndices = sorted([borders.index(unmatchedBorder1), borders.index(unmatchedBorder2)])
    i = 0
    while unmatchIndices != [0,3] or i < 4:
        # rotate clockwise until borders are in the right place
        tile = rotateTileClockwise(tile)
        borders = getClockwiseBordersFromTile(tile)
        unmatchIndices = sorted([borders.index(unmatchedBorder1), borders.index(unmatchedBorder2)])
        i += 1
    if i == 4:
        print('Error: top left start corner did not work')
    return tile # we can infer border changes if need be, TBD

def getMatchingBorderTileIds(refTileId, borders):
    borderTileTuples = []
    for b in borders:
        if refTileId in borders[b]:
            for tilenum in borders[b]:
                if tilenum != refTileId:
                    borderTileTuples.append((b, tilenum))
    return borderTileTuples

def findIn2dArray(array, searchVal):
    for i in range(len(array)):
        for j in range(len(array[i])):
            if array[i][j] == searchVal:
                return (i,j)
    return False

# startIndex (tuple) guaranteed to be present + workable in innerMap and tiles
def bfs1Level(tiles, borders, innerMap, startIndex):
    (row,col) = startIndex
    chosenId = innerMap[row][col]
    chosenTile = tiles[chosenId]
    borderTileTuples = getMatchingBorderTileIds(chosenId, borders)
    newNeighbors = []
    for (border, neighborTileId) in borderTileTuples:
        if not findIn2dArray(innerMap, neighborTileId):
            neighborTile = tiles[neighborTileId]
            # update neighborTile to fit, and get transformed border+index
            (neighborTile, borderNeighborIndex) = matchTilesAtBorder(
                chosenTile, neighborTile, border)
            tiles[neighborTileId] = neighborTile
            newNeighborRow = row
            newNeighborCol = col
            if borderNeighborIndex == 0:
                # neighbor's top border matches chosen tile's bottom border,
                # so neighbor is one row below chosen tile
                newNeighborRow += 1
            elif borderNeighborIndex == 1:
                # neighbor's right border matches chosen's left border,
                # so neighbor is one to the left of chosen tile
                newNeighborCol -= 1
            elif borderNeighborIndex == 2:
                # neighbor's bottom border: neighbor is one above chosen
                newNeighborRow -= 1
            elif borderNeighborIndex == 3:
                # neighbor's left border: neighbor is one right of chosen
                newNeighborCol += 1
            else:
                print('Unexpected border neighbor index ' + str(borderNeighborIndex))
            if newNeighborCol < 0 or newNeighborRow < 0:
                print('Something went wrong - got negative index: ' + str((newNeighborRow, newNeighborCol)))
            innerMap[newNeighborRow][newNeighborCol] = neighborTileId
            newNeighbors.append((newNeighborRow, newNeighborCol))
    # return transformed tiles, updated innerMap, and list of new neighbor indices
    return (tiles, innerMap, newNeighbors)

def betterPuzzlePrint(tiles, innerMap):
    tileRows = len(list(tiles.values())[0])
    for row in innerMap:
        # want to print all rows in row together
        jointRows = ['' for j in range(tileRows)]
        for tileId in row:
            for j in range(tileRows):
                if tileId in tiles:
                    jointRows[j] += tiles[tileId][j] + '  '
                else:
                    jointRows[j] += ' '*(tileRows + 2)
        for row in jointRows:
            print(row)
        print()

def runBfs(filename):
    tiles = getTilesFromFile(filename)
    borders = getSharedBorders(tiles)
    corners = getCornerTiles(tiles, borders)
    # Initialize, starting with "top left" corner as reference
    startCornerId = list(corners)[0]
    unmatchedBorders = [b for b in borders if borders[b] == [startCornerId]]
    tiles[startCornerId] = orientTopLeft(tiles[startCornerId], unmatchedBorders[0], unmatchedBorders[1])
    n = int(math.sqrt(len(tiles))) # square puzzle too, so this gives number of rows
    innerMap = [[None for i in range(n)] for j in range(n)]
    innerMap[0][0] = startCornerId
    # BFS loops
    searchIndices = [(0,0)]
    visitedIndices = []
    while(len(searchIndices) > 0):
        newSearchIndices = []
        for pos in searchIndices:
            if pos not in visitedIndices: # just a safety check
                # updates tiles and innerMap
                (tiles, innerMap, newNeighbors) = bfs1Level(tiles, borders, innerMap, pos)
                # pos is now visited
                visitedIndices.append(pos)
                for neighPos in newNeighbors:
                    # first part is just a safety check; second is possibly an edge case :P
                    if neighPos not in visitedIndices and neighPos not in searchIndices: 
                        newSearchIndices.append(neighPos)
        searchIndices = newSearchIndices
    return (tiles, innerMap)

def getActualImage(tiles, innerMap):
    newTiles = {}
    for tileId in tiles:
        newTile = []
        for row in tiles[tileId][1:-1]:
            newTile.append(row[1:-1])
        newTiles[tileId] = newTile
    tileRows = len(list(newTiles.values())[0])
    jointImage = []
    for row in innerMap:
        # want to print all rows in row together
        jointRows = ['' for j in range(tileRows)]
        for tileId in row:
            for j in range(tileRows):
                if tileId in newTiles:
                    jointRows[j] += newTiles[tileId][j]
                else:
                    # catches errors, if we missed a tile
                    jointRows[j] += ' ' * (tileRows)
        for row in jointRows:
            jointImage.append(row)
    return jointImage


(tiles, innerMap) = runBfs('testinput1.txt')
# betterPuzzlePrint(tiles, innerMap)
actualImage = getActualImage(tiles, innerMap)
# betterTilePrint(actualImage)

SEA_MONSTER = [
    "                  # ",
    "#    ##    ##    ###",
    " #  #  #  #  #  #   "]

def getHashtagIndices(seaMonster):
    seaMonsterHashtags = []
    seaMonsterRows = len(seaMonster)
    seaMonsterCols = max([len(row) for row in seaMonster])
    for r in range(seaMonsterRows):
        for c in range(seaMonsterCols):
            if seaMonster[r][c] == '#':
                seaMonsterHashtags.append((r,c))
    return (seaMonsterRows, seaMonsterCols, seaMonsterHashtags)

# betterTilePrint(rotateTileClockwise(SEA_MONSTER))
# Implementation can rotate + flip either actualImage or SEA_MONSTER;
# latter probably easier, but would need to recalculate hashtag indices

def markPatternInImage(fullImage, hashtagPattern):
    maxRows = len(fullImage)
    maxCols = len(fullImage[0])
    (rows, cols, indices) = getHashtagIndices(hashtagPattern)
    for startRow in range(maxRows - rows + 1):
        for startCol in range(maxCols - cols + 1):
            matchWrtStart = True
            for (x,y) in indices:
                if fullImage[x + startRow][y + startCol] != '#':
                    # not a pattern match (TODO make more efficient if needed)
                    matchWrtStart = False
            if matchWrtStart:
                # matches so mark the pattern
                for (x,y) in indices:
                    origStr = fullImage[x + startRow]
                    replIndex = y + startCol
                    fullImage[x + startRow] = origStr[:replIndex] + '0' + origStr[replIndex + 1:]
    return fullImage

def getRoughness(filename, seaTile):
    (tiles, innerMap) = runBfs(filename)
    actualImage = getActualImage(tiles, innerMap)
    for j in range(2):
        for i in range(4):
            seaTile = rotateTileClockwise(seaTile)
            actualImage = markPatternInImage(actualImage, seaTile)
        seaTile = flipTileHorizontal(seaTile)
    roughness = 0
    for row in actualImage:
        roughness += row.count('#')
    return roughness

print(getRoughness('input20.txt', SEA_MONSTER))
