import re

RULE_PATTERN = r'(?P<field>(\w|\s)+): (?P<low1>\d+)\-(?P<high1>\d+) or (?P<low2>\d+)\-(?P<high2>\d+)'
RULE_COMPILE = re.compile(RULE_PATTERN)
YOURS = "your ticket:"
NEARBY = "nearby tickets:"

m = RULE_COMPILE.match("row: 6-11 or 33-44")

def unionValid(fieldRanges, maxN = 1000):
    validRange = [False for i in range(maxN)]
    for ranges in fieldRanges:
        for (low, high) in ranges:
            for val in range(low, high + 1):
                validRange[val] = True
    return validRange                

def run1(inputfilename, maxN = 1000):
    finishedRules = False
    startedNearby = False
    # don't see a ticket value bigger than 1000, so getting the overall
    # valid range is relatively storage-friendly
    validRange = [False for i in range(maxN)]
    invalidVals = []
    with open(inputfilename) as f:
        for line in f:
            if line.strip() == NEARBY:
                startedNearby = True
            elif not finishedRules:
                if len(line.strip()) == 0:
                    finishedRules = True
                else:
                    # process new rule
                    m = RULE_COMPILE.match(line.strip())
                    for val in range(int(m.group('low1')), int(m.group('high1')) + 1):
                        validRange[val] = True
                    for val in range(int(m.group('low2')), int(m.group('high2')) + 1):
                        validRange[val] = True
            elif startedNearby:
                ticketVals = [int(x) for x in line.strip().split(',')]
                for val in ticketVals:
                    if val >= maxN:
                        print('Error with assumption:')
                        print(val)
                    elif not validRange[val]:
                        invalidVals.append(val)
    return sum(invalidVals)            

print(run1('testinput1.txt', 100))
print(run1('input16.txt', 1000))

def run2(inputfilename, maxN = 1000):
    finishedRules = False
    startedNearby = False
    startedYours = False
    # this time store all fields that are valid in range
    validRange = [[] for i in range(maxN)]
    allowedFieldOrder = []
    yourTicket = []
    with open(inputfilename) as f:
        for line in f:
            if line.strip() == NEARBY:
                startedNearby = True
            elif line.strip() == YOURS:
                startedYours = True
            elif not finishedRules:
                if len(line.strip()) == 0:
                    finishedRules = True
                else:
                    # process new rule
                    m = RULE_COMPILE.match(line.strip())
                    for val in range(int(m.group('low1')), int(m.group('high1')) + 1):
                        validRange[val].append(m.group('field'))
                    for val in range(int(m.group('low2')), int(m.group('high2')) + 1):
                        validRange[val].append(m.group('field'))
            elif startedYours and len(yourTicket) == 0:
                yourTicket = [int(x) for x in line.strip().split(',')]
                # assuming your ticket is valid, we can narrow down field order
                for val in yourTicket:
                    allowedFieldOrder.append(validRange[val])
            elif startedNearby:
                ticketVals = [int(x) for x in line.strip().split(',')]
                # filter out invalid tickets
                validTicket = True
                for val in ticketVals:
                    if val >= maxN:
                        print('Error with assumption:')
                        print(val)
                        validTicket = False
                    elif not validRange[val]:
                        validTicket = False
                if validTicket:
                    # narrow down possible field order from valid tickets
                    for i in range(len(ticketVals)):
                        prevFields = allowedFieldOrder[i]
                        ticketFields = validRange[ticketVals[i]]
                        # narrow down to union of two field sets
                        allowedFieldOrder[i] = [f for f in prevFields if f in ticketFields]
    # remove dupes in allowed fields
    while max([len(x) for x in allowedFieldOrder]) > 1:
        singleFields = []
        for x in allowedFieldOrder:
            if len(x) == 1:
                singleFields.append(x[0])
        for i in range(len(allowedFieldOrder)):
            if len(allowedFieldOrder[i]) > 1:
                allowedFieldOrder[i] = [x for x in allowedFieldOrder[i] if x not in singleFields]
    # your ticket is in the same order as allowed field order
    yourTicketFields = {}
    for i in range(len(allowedFieldOrder)):
        yourTicketFields[allowedFieldOrder[i][0]] = yourTicket[i]
    return yourTicketFields

print(run2('testInput2.txt', 20))
yourTicket = run2('input16.txt', 1000)
print(yourTicket)
departureProduct = 1
for field in yourTicket:
    if field[:9] == 'departure':
        departureProduct *= yourTicket[field]
print(departureProduct)


