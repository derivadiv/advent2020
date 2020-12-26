
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
print(move('389125467', moves = 10))
print(move('389125467', moves = 100))
print(move('463528179', moves = 100))

def moveMillion(inputstr, moves = 100):
    cups = []
    for char in inputstr:
        cups.append(int(char))
    maxCups = max(cups)
    for i in range(maxCups + 1, 1000001):
        cups.append(i)
    for i in range(moves):
        cups = crabMove(cups)
    start = cups.index(1)
    nextCup = (start + 1) % len(cups)
    secondCup = (start + 2) % len(cups)
    return cups[nextCup] * cups[secondCup]

print(moveMillion('389125467'))
