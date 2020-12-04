# right 3 and down 1. (first at 3,1; second at 6,2)

def get_tree_count_1(filehandle):
    row = 0
    trees = 0
    poslist = []
    for line in filehandle:
        charsrow= line.strip()
        treesearch = (row*3) % len(charsrow)
        if charsrow[treesearch] == '#':
            trees += 1
        row += 1
    return trees

with open('input3.txt', 'r') as f:
    print(get_tree_count_1(f))

def get_tree_count_2(filehandle, rightsteps, downsteps):
    row = 0
    trees = 0
    poslist = []
    rowsteps = 0
    for line in filehandle:
        if rowsteps == 0:
            charsrow = line.strip()
            treesearch = (row*rightsteps) % len(charsrow)
            if charsrow[treesearch] == '#':
                trees += 1
            row += 1
        rowsteps = (rowsteps + 1) % downsteps
    return trees

filename = 'input3.txt'
with open(filename, 'r') as f:
    a = get_tree_count_2(f, 1, 1)
with open(filename, 'r') as f:
    b = get_tree_count_2(f, 3, 1)
with open(filename, 'r') as f:
    c = get_tree_count_2(f, 5, 1)
with open(filename, 'r') as f:
    d = get_tree_count_2(f, 7, 1)
with open(filename, 'r') as f:
    e = get_tree_count_2(f, 1, 2)

print(a,b,c,d,e,a*b*c*d*e)
