
# current cup is first in list
def crabMove(cups):
    threeClock = cups[1:4]
    cups = cups[:1] + cups[4:]
    destinationValue = cups[0] - 1
    while destinationValue not in cups:
        destinationValue -= 1
        if destinationValue < min(cups):
            destinationValue = max(cups) # should break out of while loop
    # insert 1 R of destination
    destination = cups.index(destinationValue)
    cups = cups[:destination] + [destinationValue] + threeClock + cups[destination+1:]
    # rotate 1 clockwise (R)
    return cups[1:] + cups[:1]

def move(inputstr, moves = 100):
    cups = []
    for char in inputstr:
        cups.append(int(char))
    for i in range(moves):
        cups = crabMove(cups)
    outstr = ''
    start = cups.index(1)
    for cup in cups[start + 1:] + cups[:start]:
        outstr += str(cup)
    
    return outstr
# print(move('389125467', moves = 10))
# print(move('389125467', moves = 100))
# print(move('463528179', moves = 100))

"""
Part 2 must be more efficient. Giwen clockwise str:
- first is current cup
- picks 3 clockwise, "removes" them
- destination label = current cup label - 1, or next lowest,
  wrapping arount to highest (individual ~O(n) search, worst case finding min/max)
- moves 3 clockwise of destination
- new current is 1 clockwise of current

1. track start index in fixed list
2. circular linked list? then change links
3. create on-demand? e.g. store max ns
it still took too long to actually run, probably for finding highest min/max.
maybe we could precalculate that with another link?
   - special case is that the next min is "removed": but can traverse children if needed; actually
   - would just be destination label
"""

class Cup:
    def __init__(self, label):
        self.label = label
        self.clockwiseChild = None
        self.nextMinChild = None

    def setChild(self, value):
        self.clockwiseChild = Cup(value)

    def setClockwiseChildCup(self, cup):
        if cup is not None:
            assert isinstance(cup, Cup)
        self.clockwiseChild = cup

    def setNextMinChildCup(self, cup):
        if cup is not None:
            assert isinstance(cup, Cup)
        self.nextMinChild = cup

    def getClockwise(self):
        return self.clockwiseChild

    def getNextMin(self):
        return self.nextMinChild

    def getLabel(self):
        return self.label

# iterating clockwise: only do this if we can't use nextMinChildCup
def findValueClockwise(currentCup, desiredValue):
    if currentCup.getLabel() == desiredValue:
        return currentCup
    child = currentCup.getClockwise()
    while child.getLabel() != desiredValue:
        if child.getLabel() == currentCup.getLabel():
            # unsuccessful search somehow, looped around
            print('Could not find desired value')
            print(currentCup.getLabel())
            print(desiredValue)
            return None
        child = child.getClockwise()
    return child

def initialize(inputstr, maxN):
    initMax = len(inputstr)
    firstCup = Cup(int(inputstr[0]))
    lastCup = firstCup
    for char in inputstr[1:]:
        lastCup.setChild(int(char))
        lastCup = lastCup.getClockwise()
    # we have len(inputstr) cups with values 1 to initMax, jumbled up
    # set each cup's nextMinChild (except for lowest value, which will wrap around)
    lowestCup = findValueClockwise(firstCup, 1)
    for lowerValue in range(1, initMax): 
        biggerCup = findValueClockwise(firstCup, lowerValue + 1) # range 2 to initMax
        smallerCup = findValueClockwise(firstCup, lowerValue) # range 1 to initMax - 1
        biggerCup.setNextMinChildCup(smallerCup)
    # everything else is in order, so nextMinChildCup is just the previous cup
    oneValueLowerCup = findValueClockwise(firstCup, initMax) # special case for last cup
    for i in range(initMax + 1, maxN + 1):
        nextCup = Cup(i)
        nextCup.setNextMinChildCup(oneValueLowerCup)
        lastCup.setClockwiseChildCup(nextCup)
        oneValueLowerCup = nextCup
        lastCup = nextCup
    # at end, lastCup is Cup(maxN), with its nextMinChild set already to maxN-1. 
    # make this circular.
    lastCup.setClockwiseChildCup(firstCup)
    # make sure lowestCup wraps around to max. value
    lowestCup.setNextMinChildCup(lastCup)
    return firstCup

def oneRound(currentCup, maxN):
    # cups that we need to disassociate: [moveCup, stopCup)
    moveCup = currentCup.getClockwise()
    stopCup = moveCup.getClockwise().getClockwise().getClockwise()
    moveLabels = [
        moveCup.getLabel(),
        moveCup.getClockwise().getLabel(),
        moveCup.getClockwise().getClockwise().getLabel()]
    # find destination, getting around move cups if needed
    destCup = currentCup.getNextMin()
    while destCup.getLabel() in moveLabels:
        destCup = destCup.getNextMin()
    # disassociate three cups clockwise
    moveCup.getClockwise().getClockwise().setClockwiseChildCup(None)
    currentCup.setClockwiseChildCup(stopCup)
    # attach moveCup to destination
    destOrigChild = destCup.getClockwise()
    destCup.setClockwiseChildCup(moveCup)
    moveCup.getClockwise().getClockwise().setClockwiseChildCup(destOrigChild)
    # rotate one clockwise
    return currentCup.getClockwise()

# current cup is first in list
def efficientCrab(inputstr, maxN = 1000000, moves = 10000000):
    firstCup = initialize(inputstr, maxN)
    tmp = firstCup
    for i in range(15):
        print('Cup:' + str(tmp.getLabel()))
        print('Cup clockwise:' + str(tmp.getClockwise().getLabel()))
        print('Cup next min:' + str(tmp.getNextMin().getLabel()))
        print()
        tmp = tmp.getClockwise()
    progress = int(moves/100)
    for i in range(moves):
        firstCup = oneRound(firstCup, maxN)
        if i % progress == 0:
            print(int(i/progress))
    cup1 = findValueClockwise(firstCup, 1)
    val1 = cup1.getClockwise().getLabel()
    val2 = cup1.getClockwise().getClockwise().getLabel()
    print(val1)
    print(val2)
    return val1 * val2

# print(efficientCrab('389125467'))
print(efficientCrab('463528179'))
