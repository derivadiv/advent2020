
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

# (player1, player2) = startingDecks('input22.txt')
# print(play(player1, player2))
"""
Part 2:
Naive implementation is too slow.
Full input: Each player has 25 cards, so 50 total.
  - Many combos, but not too long a key.
"""

def doRecurse(top1, player1, top2, player2):
    return len(player1) >= top1 and len(player2) >= top2

def hash4cache(player1,player2):
    return ','.join([str(x) for x in player1]) + ':' + ','.join(
        [str(x) for x in player2])

cache = {} # map of starting game cards to ?

def replayRound(player1, player2):
    # seeing if a cache helps with memory
    cachekey = hash4cache(player1, player2)
    cachekeyreverse = hash4cache(player2, player1)
    if cachekey in cache:
        # should be at winning level: rest of history doesn't matter
        (player1, player2) = cache[cachekey]
        return (player1, player2)
    elif cachekeyreverse in cache:
        # again, winning level, skip rest of history
        (player2, player1) = cache[cachekeyreverse]
        return (player1, player2)

    top1 = player1.pop(0)
    top2 = player2.pop(0)
    if doRecurse(top1, player1, top2, player2):
        # copy that many cards in their deck for a subgame
        (subgame1, subgame2) = replayRecurse(player1[:top1], player2[:top2])
        if len(subgame1) > len(subgame2):
            # player 1 won and gets this top card
            player1.append(top1)
            player1.append(top2)
        else:
            # assume player 2 won
            player2.append(top2)
            player2.append(top1)
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
    return (player1, player2)

def replayRecurse(player1, player2, maxRounds = 10000):
    rounds = 0
    gameHistory = set()
    while rounds < maxRounds:
        cachekey = hash4cache(player1, player2)
        if cachekey in gameHistory:
            # avoid history repeating itself, but
            # what happens with player 2's cards??
            return (player1 + player2, [])
        (player1, player2) = replayRound(player1, player2)
        rounds += 1
        gameHistory.add(cachekey)
        if len(player1) == 0 or len(player2) == 0:
            # game ends; add winningScore separately
            return (player1, player2)

def gameWinningScore(player1, player2):
    if len(player1) == 0:
        return winningScore(player2)
    return winningScore(player1)

(player1, player2) = startingDecks('input22.txt')
(player1, player2) = replayRecurse(player1, player2)
print(gameWinningScore(player1, player2))
