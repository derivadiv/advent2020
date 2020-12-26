def transform(subjectNumber, loopSize, value = 1):
    for i in range(loopSize):
        value = (value * subjectNumber) % 20201227
    # since starting from 1, value = subjectNumber ^ loopSize % 20201227
    return value

def handshake(cardLoop, doorLoop):
    cardPublic = transform(7, cardLoop)
    doorPublic = transform(7, doorLoop)
    return (cardPublic, doorPublic)

def cardEncryptionKey(cardLoop, doorPublic):
    return transform(doorPublic, cardLoop)

# same result as card encryption key
def doorEncryptionKey(doorLoop, cardPublic):
    return transform(cardPublic, doorLoop)

def getLoopSize(publicKey, subjectNumber = 7):
    value = 1
    loops = 0
    while value != publicKey:
        value = (value * subjectNumber) % 20201227
        loops += 1
    return loops

def getEncryptionKey(doorPublic, cardPublic):
    # doorPublic = 7 ^ doorSecret % 20201227
    # doorSecret = log(doorPublic + 20201227n, 7)
    doorSecret = getLoopSize(doorPublic)
    # cardSecret = log(cardPublic + 20201227k, 7)
    cardSecret = getLoopSize(cardPublic)
    # key1 = doorPublic ^ cardSecret % 20201227
    #      = (7^doorSecret % 20201227) ^ cardSecret
    key1 = transform(doorPublic, cardSecret)
    key2 = transform(cardPublic, doorSecret)
    assert key1 == key2
    return key1

print(getEncryptionKey(12320657, 9659666))
