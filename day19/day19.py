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
                print(rules[0])
                rule0 = re.compile(rules[0])
            elif not endRules:
                (indexRule, value) = parserule(line.strip())
                rules[indexRule] = value
            else:
                # individual messages to test
                if rule0.fullmatch(line.strip()):                
                    numMatch += 1
    return numMatch
print(parsefile('testinput1.txt'))
print(parsefile('testinput0.txt'))
print(parsefile('input19.txt'))

"""
Gonna do part 2 manually: I think regex can handle this nicely.
"""
# rules[indexSub] must be a string
def updaterules2(rules, indexSub):
    if indexSub == 8:
        # 8: 42 -> 8: 42 | 42 8  -> basically (42)+
        rules[8] = r'(' + rules[42] + r')+'
    elif indexSub == 11:
        # 11: 42 31  -> 11: 42 31 | 42 11 31 -> basically 42 (42 31)* 31
        # 42 and 31 were already string'ed, but 11 hasn't been used yet
        rules[11] = rules[42] + r'(' + rules[42] + rules[31] + r')*' + rules[31]
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

def allowLoop(inputfilename):
    endRules = False
    rules = {}
    rule0 = None
    numMatch = 0
    with open(inputfilename) as f:
        for line in f:
            if len(line.strip()) == 0:
                endRules = True
                # recalc rules
                updatedrules = []
                while len(updatedrules) < len(rules):
                    stringrules = findstringrules(rules)
                    for s in stringrules:
                        if s not in updatedrules:
                            rules = updaterules2(rules, s)
                            rules = condensestrings(rules)
                            updatedrules.append(s)
                print(rules[8])
                print(rules[11])
                print(rules[0])
                rule0 = re.compile(rules[0])
            elif not endRules:
                (indexRule, value) = parserule(line.strip())
                rules[indexRule] = value
            else:
                # individual messages to test
                if rule0.fullmatch(line.strip()):                
                    numMatch += 1
    return numMatch

print(parsefile('testinput2.txt'))
print(allowLoop('testinput2.txt'))
# print(allowLoop('input19.txt'))
