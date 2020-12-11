import re

BAG_PATTERN = r'(?P<color>(\w|\s)+) bags?'
NUMBER_BAG_PATTERN = r'(?P<number>\d+) ' + BAG_PATTERN
EMPTY_CONTENTS = 'no other bags'
SENTENCE_PATTERN = r'(?P<container>(\w|\s)+) contain (?P<contents>(.*)+)\.\s*'

BAG_COMPILE = re.compile(BAG_PATTERN)
NUM_COMPILE = re.compile(NUMBER_BAG_PATTERN)
SENTENCE_COMPILE = re.compile(SENTENCE_PATTERN)

# Represent as graph: nodes are colors and edges are weights
# for part 1, go in reverse direction: kid to parent

insideToOutside = {}

def addContents(containerColor, insideColor, insideNum):
    if insideColor not in insideToOutside:
        insideToOutside[insideColor] = set()
    if containerColor not in insideToOutside[insideColor]:
        insideToOutside[insideColor].add(containerColor)

def findOutsideColors(insideColor):
    if insideColor not in insideToOutside:
        return set()
    newColors = insideToOutside[insideColor].copy()
    doneColors = set()
    while len(newColors) > 0:
        x = newColors.copy()
        for c in x:
            if c in insideToOutside:
                for k in insideToOutside[c]:
                    if k not in doneColors:
                        newColors.add(k)
            doneColors.add(c)
            newColors.remove(c)
    return doneColors

# returns (container color, [contents]) where contents are tuples of
# (inside bag color, inside number of bags)
def parse(sentence):
    m = SENTENCE_COMPILE.match(sentence)
    l = BAG_COMPILE.match(m.group('container'))

    if m.group('contents') == EMPTY_CONTENTS:
        return (l.group('color'), [])
    # individual bag phrases
    contents = m.group('contents').split(', ')
    bags = []
    for c in contents:
        n = NUM_COMPILE.match(c)
        bags.append((n.group('color'), int(n.group('number'))))
    return (l.group('color'), bags)

# pt. 2: probably need recursion
outsideToInside = {}

def addContents2(containerColor, insideColor, insideNum):
    if containerColor not in outsideToInside:
        outsideToInside[containerColor] = {}
    if insideColor not in outsideToInside[containerColor]:
        outsideToInside[containerColor][insideColor] = insideNum

def countContents(containerColor):
    if containerColor not in outsideToInside:
        return 0
    countBags = 0
    for insideColor in outsideToInside[containerColor]:
        insideNum = outsideToInside[containerColor][insideColor]
        metaInsideNum = countContents(insideColor)
        countBags += (insideNum + (insideNum * metaInsideNum))
    return countBags

inputFileName = 'input7.txt'
with open(inputFileName, 'r') as f:
    for line in f:
        (outsideColor, contents) = parse(line)
        for c in contents:
            addContents2(outsideColor, c[0], c[1])

print(countContents('shiny gold'))
