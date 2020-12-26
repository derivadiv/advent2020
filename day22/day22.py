
def playRound(player1, player2):
    top1 = player1.pop(0)
    top2 = player2.pop(0)
    if top1 > top2:
        # cards at bottom of own deck
        player1.append(top1)
        player1.append(top2)
    elif top2 > top1:
        # winning card above other card
        player2.append(top2)
        player2.append(top1)
    else:
        # they didn't talk about draws; assuming
        # both players keep cards
        player1.append(top1)
        player2.append(top2)
    return (player1, player2)

def startingDecks(inputfilename):
    player1 = []
    player2 = []
    onPlayer1 = False
    onPlayer2 = False
    with open(inputfilename) as f:
        for line in f:
            if 'Player 1' in line:
                onPlayer1 = True
            elif 'Player 2' in line:
                onPlayer2 = True
                onPlayer1 = False
            elif len(line.strip()) == 0:
                onPlayer1 = False
                onPlayer2 = False
            else:
                card = int(line.strip())
                if onPlayer1:
                    player1.append(card)
                elif onPlayer2:
                    player2.append(card)
                else:
                    print('Warning with card ' + str(card))
    return (player1, player2)

def winningScore(player):
    n = len(player)
    score = 0
    for i in range(n):
        score += (n-i)*player[i]
    return score

def play(player1, player2, maxRounds = 10000):
    rounds = 0
    while rounds < maxRounds:
        (player1, player2) = playRound(player1, player2)
        rounds += 1
        if len(player1) == 0:
            return winningScore(player2)
        elif len(player2) == 0:
            return winningScore(player1)
    return None

# (player1, player2) = startingDecks('input22.txt')
# print(play(player1, player2))

def doRecurse(top1, player1, top2, player2):
    return len(player1) >= top1 and len(player2) >= top2

def hash4cache(player1,player2):
    return ','.join([str(x) for x in player1]) + ':' + ','.join(
        [str(x) for x in player2])

cache = {}

def playRecurseRound(player1, player2, history1, history2):
    for i in range(len(history1)):
        if history1[i] == player1 and history2[i] == player2:
            # make player 1 win, not sure what happens with
            # player 2's cards
            # player1.extend(player2)
            return (player1, [], history1, history2)
    # add to game's history, otherwise
    history1.append([x for x in player1])
    history2.append([x for x in player2])

    # seeing if a cache helps with memory
    cachekey = hash4cache(player1, player2)
    if cachekey in cache:
        print('cache hit, yay')
        # should be at winning level: rest of history doesn't matter
        (player1, player2) = cache[cachekey]
        return (player1, player2, history1, history2)
    
    top1 = player1.pop(0)
    top2 = player2.pop(0)
    if doRecurse(top1, player1, top2, player2):
        # subgame with new history until a winner
        player1Copy = [x for x in player1]
        history1Copy = []
        player2Copy = [x for x in player2]
        history2Copy = []
        maxRounds = 10000
        rounds = 0
        while rounds < maxRounds:
            (player1Copy, player2Copy, history1Copy,
             history2Copy) = playRecurseRound(
                player1Copy, player2Copy, history1Copy, history2Copy)
            if len(player1Copy) == 0:
                # player 2 wins parent game too
                player2.append(top2)
                player2.append(top1)
                cache[cachekey] = (player1, player2)
                return (player1, player2, history1, history2)
            elif len(player2Copy) == 0:
                player1.append(top1)
                player1.append(top2)
                cache[cachekey] = (player1, player2)
                return (player1, player2, history1, history2)
            rounds += 1
        print('oh no, we got to max rounds')
    elif top1 > top2:
        # cards at bottom of own deck
        player1.append(top1)
        player1.append(top2)
    elif top2 > top1:
        # winning card above other card
        player2.append(top2)
        player2.append(top1)
    else:
        # they didn't talk about draws; assuming
        # both players keep cards
        player1.append(top1)
        player2.append(top2)
    cache[cachekey] = (player1, player2)
    return (player1, player2, history1, history2)

def playRecurse(player1, player2, maxRounds = 10000):
    rounds = 0
    history1 = []
    history2 = []
    while rounds < maxRounds:
        (player1, player2, history1, history2) = playRecurseRound(
            player1, player2, history1, history2)
        rounds += 1
        if len(player1) == 0:
            return winningScore(player2)
        elif len(player2) == 0:
            return winningScore(player1)
    return None

(player1, player2) = startingDecks('input22.txt')
print(playRecurse(player1, player2))
