import re

# rules[indexSub] must be a string
def updaterules(rules, indexSub):
    val = rules[indexSub]
    for i in rules:
        if isinstance(rules[i], list):
            for j in range(len(rules[i])):
                rule = rules[i][j]
                if isinstance(rule, list):
                    for r in range(len(rule)):
                        if rule[r] == indexSub:
                            rule[r] = val
                    rules[i][j] = rule
    return rules

# return list of indices where rule is a String
def findstringrules(rules):
    indices = []
    for i in rules:
        if isinstance(rules[i], str):
            indices.append(i)
    return indices

# rule number: [] <- possibilities with pipes, e.g. [[1,2], [2,1]]
def parserule(line):
    (indexRule, rule) = line.split(': ')
    indexRule = int(indexRule)
    if rule[0] == '"':
        # single character
        return (indexRule, rule[1])
    # references to subrules
    pipes = rule.split('|')
    poss = []
    for p in pipes:
        poss.append([int(i) for i in p.strip().split()])
    return (indexRule, poss)

def islistofstrings(checklist):
    for val in checklist:
        if not isinstance(val, str):
            return False
    return True

def condensestrings(rules):
    for indexRule in rules:
        if isinstance(rules[indexRule], list):
            for i in range(len(rules[indexRule])):
                poss = rules[indexRule][i]
                if isinstance(poss, list) and islistofstrings(poss):
                    poss = ''.join(poss)
                    rules[indexRule][i] = poss
            if islistofstrings(rules[indexRule]):
                if len(rules[indexRule]) == 1:
                    rules[indexRule] = rules[indexRule][0]
                else:
                    rules[indexRule] = '(' + '|'.join(rules[indexRule]) + ')'
    return rules

def parsefile(inputfilename):
    endRules = False
    rules = {}
    rule0 = None
    numMatch = 0
    with open(inputfilename) as f:
        for line in f:
            if len(line.strip()) == 0:
                endRules = True
                # recalc rules
                stringrules = findstringrules(rules)
                while len(stringrules) < len(rules):
                    for s in stringrules:
                        rules = updaterules(rules, s)
                        rules = condensestrings(rules)
                    stringrules = findstringrules(rules)
                rule0 = re.compile(rules[0])
            elif not endRules:
                (indexRule, value) = parserule(line.strip())
                rules[indexRule] = value
            else:
                # individual messages to test
                if rule0.fullmatch(line.strip()):                
                    numMatch += 1
    return numMatch
# print(parsefile('testinput1.txt'))
# print(parsefile('testinput0.txt'))
# print(parsefile('input19.txt'))

"""
Still attempting part 2 with regex
"""

def parsefileLoops(inputfilename):
    endRules = False
    rules = {}
    rule0 = None
    rule42 = None
    rule31 = None
    numMatch = 0
    with open(inputfilename) as f:
        for line in f:
            if len(line.strip()) == 0:
                endRules = True
                # recalc rules
                stringrules = findstringrules(rules)
                while len(stringrules) < len(rules):
                    for s in stringrules:
                        rules = updaterules(rules, s)
                        rules = condensestrings(rules)
                    stringrules = findstringrules(rules)
                # 8: 42 becomes 8: 42 | 42 8  -> basically (42)+
                # 11: 42 31 becomes 11: 42 31 | 42 11 31 -> basically 42 (42 31)* 31
                # 0: 8 11 = 42 42 31 | 42 42 42 31 | 42 42 ... 42 31 |
                          # 42 42 42 31 31  | 42 42 42 42 42 31 31 31 31
                # basically 0 can match any number of 42s followed by
                # a smaller number of 31s... probably 42+ (42 31)+ should do.
                rules[0] = r'(' + rules[42] + r')+(' + rules[42] + rules[31] + r')+'
                rule0 = re.compile(rules[0])
                rule42 = re.compile(rules[42])
                rule31 = re.compile(rules[31])
            elif not endRules:
                (indexRule, value) = parserule(line.strip())
                rules[indexRule] = value
            else:
                # Python implementation is not quite greedy enough...
                doesMatch = False
                endIndices42 = []
                stripline = line.strip()
                match42 = rule42.match(stripline)
                while match42 is not None:
                    endIndex = match42.span()[1]
                    endIndices42.append(endIndex)
                    match42 = rule42.match(stripline, endIndex)
                for endIndex42 in endIndices42:
                    # search for 31 matches from here on: match leftover str
                    # and number of matches < number of 42 matches
                    endIndices31 = []
                    endIndex = endIndex42
                    match31 = rule31.match(stripline, endIndex)
                    while match31 is not None:
                        endIndex = match31.span()[1]
                        endIndices31.append(endIndex)
                        match31 = rule31.match(stripline, endIndex)
                    if endIndex != endIndex42 and endIndex == len(stripline):
                        # made it to end of string, now ensure that fewer 32 than 41 matches
                        if len(endIndices31) <= endIndices42.index(endIndex42):
                            doesMatch = True
                if doesMatch:
                    numMatch += 1
    return numMatch

print(parsefile('testinput2.txt')) # old
print(parsefileLoops('testinput2.txt')) # new
print(parsefileLoops('input19.txt'))
