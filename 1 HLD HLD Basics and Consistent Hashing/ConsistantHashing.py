answers = []
serverToKeyMapping = {}
locationToServerMapping = {}

def userHash(serverId, hashKey):
    p = hashKey
    n = 360
    hashCode = 0
    p_pow = 1
    for character in serverId:
        hashCode = (hashCode + (ord(character) - ord('A') + 1) * p_pow) % n
        p_pow = (p_pow * p) % n
    return hashCode

def findRequestsToServer(serverLocation):
    global locationToServerMapping, serverToKeyMapping
    if not serverToKeyMapping:
        return

    serverLocation = sorted(locationToServerMapping.keys())

    for loc in serverLocation:
        if loc > serverLocation:
            serverId = locationToServerMapping[loc]
            keynames = serverToKeyMapping.get(serverId, [])
            serverToKeyMapping[serverId] = []
            for keyname, hashKey in keynames:
                assignRequest(keyname, hashKey)
            return
    serverId = locationToServerMapping[serverLocation[0]]
    keynames = serverToKeyMapping.get(serverId, [])
    serverToKeyMapping[serverId] = []
    for keyname, hashKey in keynames:
        assignRequest(keyname, hashKey)
def addServer(serverId, hashKey):
    global locationToServerMapping, serverToKeyMapping
    firstLocation = userHash(serverId, hashKey)
    locationToServerMapping[firstLocation] = serverId
    findRequestsToServer(firstLocation)
    return len(serverToKeyMapping.get(serverId, []))
def performOperation(operation, keyOrServer, hashKey):
    global answers

    if operation == "ADD":
        answers.append(addServer(keyOrServer, hashKey))
    elif operation == "REMOVE":
        answers.append(removeServer(keyOrServer))
    elif operation == "ASSIGN":
        answers.append(assignRequest(keyOrServer, hashKey))

class Solution:
    # @param A : list of strings
    # @param B : list of strings
    # @param C : list of integers
    # @return a list of integers
    def solve(self, A, B, C):
        global answer, serverToKeyMapping, locationToServerMapping
        answers = []
        serverToKeyMapping.clear()
        locationToServerMapping.clear()

        for i in range(len(A)):
            performOperation(A[i], B[i], C[i])
        return answers

