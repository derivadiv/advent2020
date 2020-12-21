import re

# base eval no parens, L to R
def evalnoparens(line):
    parts = line.strip().split(' ')
    # number (op number)*
    curtot = int(parts[0])
    i = 1
    while i < len(parts):
        op = parts[i]
        if op == '+':
            curtot += int(parts[i+1])
        elif op == '*':
            curtot *= int(parts[i+1])
        i += 2
    return curtot
# print(evalnoparens('1 + 2 * 3 + 4 * 5 + 6'))

# startindex = index (, endindex = index ), no inner parens.
def replaceparen(line, startindex, endindex):
    innerexp = line[startindex+1:endindex]
    innerval = evalnoparens(innerexp)
    return line[:startindex] + str(innerval) + line[endindex + 1:]

# returns start and end index of first closed parens
def findfirstinnerparens(line):
    startp = None
    endp = None
    for i in range(len(line)):
        if line[i] == '(':
            startp = i
        elif line[i] == ')':
            # parens have closed
            endp = i
            return (startp, endp)
    # no proper parens
    return None

def transformparens(line):
    noparenline = line
    parenIndices = findfirstinnerparens(noparenline)
    while parenIndices is not None:
        noparenline = replaceparen(noparenline, parenIndices[0], parenIndices[1])
        parenIndices = findfirstinnerparens(noparenline)
    return noparenline

def evaluate(line):
    return evalnoparens(transformparens(line))

"""
print(evaluate('1 + (2 * 3) + (4 * (5 + 6))'))            
print(evaluate('2 * 3 + (4 * 5)'))        
print(evaluate('5 + (8 * 3 + 9 + 3 * 4 * 3)'))        
print(evaluate('5 * 9 * (7 * 3 * 3 + 9 * 3 + (8 + 6 * 4))'))        
print(evaluate('((2 + 4 * 9) * (6 + 9 * 8 + 6) + 6) + 2 + 4 * 2'))        
"""

def run1(inputfilename):
    sumTot = 0
    with open(inputfilename) as f:
        for line in f:
            val = evaluate(line.strip())
            sumTot += val
    return sumTot

#print(run1('input18.txt'))

ADD_PATTERN = r'(?P<first>\d+) \+ (?P<second>\d+)'
ADD_COMPILE = re.compile(ADD_PATTERN)

# base eval no parens, addition precedence
# same as if we had put parens around every inner addition
def transformaddnoparens(line):
    newline = line
    match = ADD_COMPILE.search(newline)
    while match is not None:
        exprval = int(match.group('first')) + int(match.group('second'))
        (start, end) = match.span() # this end index is non-inclusive
        newline = newline[:start] + str(exprval) + newline[end:]
        match = ADD_COMPILE.search(newline)
    return newline

# base eval no parens, add first
def evaladdfirst(line):
    newline = transformaddnoparens(line)
    # all leftover ops are now *
    parts = newline.strip().split(' * ')
    curtot = int(parts[0])
    i = 1
    while i < len(parts):
        curtot *= int(parts[i])
        i += 1
    return curtot

# startindex = index (, endindex = index ), no inner parens.
def replaceparen2(line, startindex, endindex):
    innerexp = line[startindex+1:endindex]
    innerval = evaladdfirst(innerexp)
    return line[:startindex] + str(innerval) + line[endindex + 1:]

def transformparens2(line):
    noparenline = line
    parenIndices = findfirstinnerparens(noparenline)
    while parenIndices is not None:
        noparenline = replaceparen2(noparenline, parenIndices[0], parenIndices[1])
        parenIndices = findfirstinnerparens(noparenline)
    return noparenline

def eval2(line):
    return evaladdfirst(transformparens2(line))

"""
print(eval2('1 + (2 * 3) + (4 * (5 + 6))'))
print(eval2('2 * 3 + (4 * 5)'))
print(eval2('5 + (8 * 3 + 9 + 3 * 4 * 3)'))
print(eval2('5 * 9 * (7 * 3 * 3 + 9 * 3 + (8 + 6 * 4))'))
print(eval2('((2 + 4 * 9) * (6 + 9 * 8 + 6) + 6) + 2 + 4 * 2'))
"""

def run2(inputfilename):
    sumTot = 0
    with open(inputfilename) as f:
        for line in f:
            val = eval2(line.strip())
            sumTot += val
    return sumTot

print(run2('input18.txt'))
