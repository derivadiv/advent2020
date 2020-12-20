
def numspoken(starting, n):
    lastTurnSpoken = {}
    # skip last number
    for i in range(len(starting) - 1):
        val = starting[i]
        # always gets most recent turn this way
        lastTurnSpoken[val] = i + 1
    prevnum = starting[-1]
    for j in range(len(starting), n):
        # current turn number = j + 1
        if prevnum not in lastTurnSpoken:
            # then it was most recently spoken the previous turn
            lastTurnSpoken[prevnum] = j
            # and this turn we'd say 0
            prevnum = 0
        else:
            # then it was spoken the previous turn AND the time in
            # lastTurnSpoken
            timeBefore = lastTurnSpoken[prevnum]
            lastTurnSpoken[prevnum] = j
            prevnum = j - timeBefore
    return prevnum

"""
# Part 1:
print(numspoken([0,3,6], 4))
print(numspoken([0,3,6], 5))
print(numspoken([0,3,6], 6))
print(numspoken([0,3,6], 7))
print(numspoken([0,3,6], 8))
print(numspoken([0,3,6], 9))
print(numspoken([0,3,6], 10))
print(numspoken([0,3,6], 2020))
print(numspoken([8,0,17,4,1,12], 2020))
"""

# print(numspoken([0,3,6], 30000000))
print(numspoken([8,0,17,4,1,12], 30000000))
