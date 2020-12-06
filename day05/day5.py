def seat_id(row, col):
    return (row*8) + col

def rangehalf(low, high, newchar):
    diff = (high - low + 1) / 2
    newlow = low + diff
    newhigh = high - diff
    
    if newchar == 'F' or newchar == 'L':
        return (low, newhigh)
    elif newchar == 'B' or newchar == 'R':
        return (newlow, high)
    print("Character '" + newchar + "' not expected for rangehalf()")

def seat_pos(binpart):
    rowlow = 0
    rowhigh = 127
    for r in binpart[:7]:
        (rowlow, rowhigh) = rangehalf(rowlow, rowhigh, r)
    assert rowlow == rowhigh
    collow = 0
    colhigh = 7
    for c in binpart[7:]:
        (collow, colhigh) = rangehalf(collow, colhigh, c)
    assert collow == colhigh
    return (rowlow, collow)

# Part 1
def highestseatid(filename):
    maxid = 0
    with open(filename, 'r') as f:
        for line in f:
            (seatrow, seatcol) = seat_pos(line.strip())
            seatid = seat_id(seatrow, seatcol)
            if seatid > maxid:
                maxid = seatid
    return maxid
            
print(highestseatid('input5.txt'))

# Seat ID range from 0 to 1023
# Your seat ID will be in an almost full row (besides yours)

def unfull_rows(filename):
    seatmap = {}
    for i in range(128):
        seatmap[i] = []
    with open(filename, 'r') as f:
        for line in f:
            (seatrow, seatcol) = seat_pos(line.strip())
            seatmap[seatrow].append(seatcol)
    for i in range(128):
        if len(seatmap[i]) == 8: #full row
            del seatmap[i]
        else:
            # solely for my own benefit
            seatmap[i] = sorted(seatmap[i])
    return seatmap

leftover_rows = unfull_rows('input5.txt')
print(leftover_rows)
for r in leftover_rows:
    for c in leftover_rows[r]:
        print(r, c, seat_id(r,c))

"""
From here on, the output was manually inspected (gasp!).
The missing seat had to be within an unfull row, but its neighboring ID could be in a full
row not on this list. The only row here where the missing seat ID had both neighbors with
full seats was row 74: column 1 was present but column 0 was not, and row 73 is not in
this list because it was full.
3 3.0 27.0
3 4.0 28.0
3 5.0 29.0
3 6.0 30.0
3 7.0 31.0
74 1.0 593.0
74 2.0 594.0
74 3.0 595.0
74 4.0 596.0
74 5.0 597.0
74 6.0 598.0
74 7.0 599.0
120 0 960
120 1.0 961.0
120 2.0 962.0
120 3.0 963.0
"""
