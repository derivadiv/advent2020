readfilename = 'input2.txt'

def valid(minchar, maxchar, repchar, password):
    n = password.count(repchar)
    if n >= minchar and n <= maxchar:
        return 1
    return 0

def part1(filename):
    rows = []
    validcount = 0
    with open(filename, 'r') as f:
        for line in f:
            parts = line.strip().split(' ')
            (minchar, maxchar) = parts[0].split('-')
            minchar = int(minchar)
            maxchar = int(maxchar)
            repchar = parts[1][0]
            password = parts[2]
            validcount += valid(minchar, maxchar, repchar, password)
    return validcount

#print(part1(readfilename))

def valid2(minchar, maxchar, repchar, password):
    if password[minchar] == repchar and password[maxchar] == repchar:
        return 0
    if password[minchar] != repchar and password[maxchar] != repchar:
        return 0
    return 1

def part2(filename):
    rows = []
    validcount = 0
    with open(filename, 'r') as f:
        for line in f:
            parts = line.strip().split(' ')
            (minchar, maxchar) = parts[0].split('-')
            minchar = int(minchar) - 1 # less index confusion later
            maxchar = int(maxchar) - 1
            repchar = parts[1][0]
            password = parts[2]
            validcount += valid2(minchar, maxchar, repchar, password)
    return validcount

print(part2(readfilename))

