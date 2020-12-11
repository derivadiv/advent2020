# Part 1
def parseAndDo(commandLine, accumulator, instructionIndex):
    parts = commandLine.strip().split(' ')
    comm = parts[0]
    num = int(parts[1])
    if comm == 'jmp':
        instructionIndex += num
    elif comm == 'acc':
        accumulator += num
        instructionIndex += 1
    elif comm == 'nop':
        instructionIndex += 1
    return (accumulator, instructionIndex)

def parseFile(inputFileName):
    with open(inputFileName, 'r') as f:
        return f.readlines()

def runWithMax1Loop(lines):
    repNums = 0
    instructionIndex = 0
    accumulator = 0
    pastInstructions = []
    while(repNums < 1) and instructionIndex < len(lines):
        pastInstructions.append(instructionIndex)
        (accumulator, instructionIndex) = parseAndDo(
            lines[instructionIndex], accumulator, instructionIndex)
        if instructionIndex in pastInstructions:
            repNums += 1
    return (accumulator, instructionIndex)

# lines = parseFile('input8.txt')
# print(runWithMax1Loop(lines))

# Part 2

def nop_jmp_indices(lines):
    nops = []
    jmps = []
    for i in range(len(lines)):
        command = lines[i][:3]
        if command == 'nop':
            nops.append(i)
        elif command == 'jmp':
            jmps.append(i)
    return (nops, jmps)

def switchNopJmp(lines, indexSwitch):
    command = lines[indexSwitch][:3]
    newline = ''
    if command == 'nop':
        newline = 'jmp' + lines[indexSwitch][3:]
    elif command == 'jmp':
        newline = 'nop' + lines[indexSwitch][3:]
    return lines[:indexSwitch] + [newline] + lines[indexSwitch+1:]

def runMutateTerm(filename):
    sourceLines = parseFile(filename)
    terminated = len(sourceLines)
    (nops, jmps) = nop_jmp_indices(sourceLines)
    switchIndices = nops + jmps
    for s in switchIndices:
        lines = switchNopJmp(sourceLines, s)
        (accumulator, instructionIndex) = runWithMax1Loop(lines)
        if instructionIndex == terminated:
            return accumulator
    return None

print(runMutateTerm('input8.txt'))
