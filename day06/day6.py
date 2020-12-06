def unique_chars(group):
    return set(group)

def group_sum_1(filename):
    curgroup = ''
    groupsum = 0
    with open(filename, 'r') as f:
        for line in f:
            if len(line.strip()) > 0:
                curgroup += line.strip()
            else:
                # boundary between new groups
                groupsum += len(unique_chars(curgroup))
                curgroup = ''
    # catch group at end of file
    if len(curgroup) > 0:
        groupsum += len(unique_chars(curgroup))
    return groupsum

def unanimous_chars(group_members):
    agreedchars = set(group_members[0])
    for member in group_members[1:]:
        shared = set()
        for c in member:
            if c in agreedchars:
                shared.add(c)
        agreedchars = shared
    return agreedchars

def group_sum_2(filename):
    curgroup = []
    groupsum = 0
    with open(filename, 'r') as f:
        for line in f:
            if len(line.strip()) > 0:
                curgroup.append(line.strip())
            else:
                # boundary between new groups
                groupsum += len(unanimous_chars(curgroup))
                curgroup = []
    # catch group at end of file
    if len(curgroup) > 0:
        groupsum += len(unanimous_chars(curgroup))
    return groupsum

print(group_sum_2('input6.txt'))
