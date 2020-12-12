import math

DEGREE_DIRECTIONS = {'N': 0, 'E': 90, 'S': 180, 'W': 270}

# leftDegrees is just -rightDegrees)
def adjustDegrees(curDegrees, rightDegrees):
    return (curDegrees + rightDegrees) % 360

def newPosForward(curXY, curDegrees, forwardUnits):
    (x, y) = curXY
    diffx = round(math.sin(math.radians(curDegrees)), 5) * forwardUnits
    diffy = round(math.cos(math.radians(curDegrees)), 5) * forwardUnits
    return (x + diffx, y + diffy)

"""
Ran all of these to verify output:
print(newPos((0,0), 0, 10))
print(newPos((0,0), 45, 10))
print(newPos((0,0), 90, 10))
print(newPos((0,0), 135, 10))
print(newPos((0,0), 180, 10))
print(newPos((0,0), 225, 10))
print(newPos((0,0), 270, 10))
print(newPos((0,0), 315, 10))
print(newPos((0,0), 360, 10))
"""

def afterInstruction(instruction, curPos, curDegrees):
    action = instruction[0]
    value = int(instruction[1:])
    newDegrees = curDegrees
    newPos = curPos
    if action in DEGREE_DIRECTIONS:
        # DO NOT CHANGE following degrees. Only applies to this action.
        actionDegrees = DEGREE_DIRECTIONS[action]
        newPos = newPosForward(curPos, actionDegrees, value)
    elif action == 'R':
        newDegrees = adjustDegrees(curDegrees, value)
    elif action == 'L':
        newDegrees = adjustDegrees(curDegrees, -value)
    elif action == 'F':
        newPos = newPosForward(curPos, curDegrees, value)
    return (newPos, newDegrees)

def manhattanDistance(fromXY, toXY):
    diffx = abs(toXY[0] - fromXY[0])
    diffy = abs(toXY[1] - fromXY[1])
    return diffx + diffy

def distAfterFileInstructions(filename, startPos, startDegrees):
    curPos = startPos
    curDegrees = startDegrees
    with open(filename, 'r') as f:
        for line in f:
            (curPos, curDegrees) = afterInstruction(line.strip(), curPos, curDegrees)
    return manhattanDistance(startPos, curPos)

# print(distAfterFileInstructions('testinput1.txt', (0,0), 90))
# print(distAfterFileInstructions('input12.txt', (0,0), 90))

# Part 2:
# F moves toward the waypoint, but *x. waypoint always relative to ship?
# NESW moves waypoint but otherwise as expected
# RL rotates waypoint around ship

def forwardToWaypoint(shipPos, waypointPos, times):
    diffx = waypointPos[0] - shipPos[0]
    diffy = waypointPos[1] - shipPos[1]
    newShipPos = (shipPos[0] + (diffx * times), shipPos[1] + (diffy * times))
    newWaypointPos = (newShipPos[0] + diffx, newShipPos[1] + diffy)
    return (newShipPos, newWaypointPos)

def calcAngle(diffx, diffy):
    # tan(angle) = diffy/diffx?
    return (90 - round(math.degrees(math.atan2(diffy,diffx)), 3)) % 360

"""
# Tested with following:
print(calcAngle(0,10)) # expect N, angle 0
print(calcAngle(5,5)) # expect NE, angle 45
print(calcAngle(10,0)) # E
print(calcAngle(5,-5)) # SE
print(calcAngle(0,-10)) # S
print(calcAngle(-5,-5)) # SW
print(calcAngle(-10,0)) # W
print(calcAngle(-5,5)) # NW
print(calcAngle(0,10))  # back to N
"""

def euclideanDistance(diffx, diffy):
    return math.sqrt(diffx**2 + diffy**2)

# keep value sign for R, add - for L
def rotateWaypointClockwise(shipPos, waypointPos, degrees):
    diffx = waypointPos[0] - shipPos[0]
    diffy = waypointPos[1] - shipPos[1]
    waypointDegreesFromShip = calcAngle(diffx, diffy)
    newWaypointDegrees = (waypointDegreesFromShip + degrees) % 360
    waypointDistance = euclideanDistance(diffx, diffy)
    newWaypointPos = newPosForward(shipPos, newWaypointDegrees, waypointDistance)
    return newWaypointPos

def afterInstruction2(instruction, shipPos, waypointPos):
    action = instruction[0]
    value = int(instruction[1:])
    newShipPos = shipPos
    newWaypointPos = waypointPos
    if action in DEGREE_DIRECTIONS:
        # move the waypoint in that dir
        actionDegrees = DEGREE_DIRECTIONS[action]
        newWaypointPos = newPosForward(waypointPos, actionDegrees, value)
    elif action == 'R':
        newWaypointPos = rotateWaypointClockwise(shipPos, waypointPos, value)
    elif action == 'L':
        newWaypointPos = rotateWaypointClockwise(shipPos, waypointPos, -value)
    elif action == 'F':
        (newShipPos, newWaypointPos) = forwardToWaypoint(shipPos, waypointPos, value)
    return (newShipPos, newWaypointPos)

def distAfterFileInstructions2(filename, shipPos, waypointPos):
    curShipPos = shipPos
    curWaypointPos = waypointPos
    with open(filename, 'r') as f:
        for line in f:
            (curShipPos, curWaypointPos) = afterInstruction2(line.strip(), curShipPos, curWaypointPos)
    return round(manhattanDistance(shipPos, curShipPos), 2)

print(distAfterFileInstructions2('testinput1.txt', (0,0), (10,1)))
print(distAfterFileInstructions2('input12.txt', (0,0), (10,1)))
