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

def assignRequest(keyname, hashkey):
    global locationToServerMapping, serverToKeyMapping
    if not locationToServerMapping:
        return 1000
    keyLocation = userHash(keyname, hashkey)
    serverLocations = sorted(locationToServerMapping.keys())
    for loc in serverLocations:
        if loc >= keyLocation:
            serverId = locationToServerMapping[loc]
            if serverId not in serverToKeyMapping:
                serverToKeyMapping[serverId] = []
            serverToKeyMapping[serverId].append((keyname, hashkey))
            return loc
    serverId = locationToServerMapping[serverLocations[0]]
    if serverId not in serverToKeyMapping:
        serverToKeyMapping[serverId] = []
    serverToKeyMapping[serverId].append((keyname, hashkey))
    return serverLocations[0]


def findRequestsToServer(serverLocation):
    global locationToServerMapping, serverToKeyMapping
    if not serverToKeyMapping:
        return

    serverLocations = sorted(locationToServerMapping.keys())

    for loc in serverLocations:
        if loc > serverLocation:
            serverId = locationToServerMapping[loc]
            keynames = serverToKeyMapping.get(serverId, [])
            serverToKeyMapping[serverId] = []
            for keyname, hashKey in keynames:
                assignRequest(keyname, hashKey)
            return
    serverId = locationToServerMapping[serverLocations[0]]
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

def removeServer(serverId):
    global locationToServerMapping, serverToKeyMapping
    for loc, server in locationToServerMapping.items():
        if server == serverId:
            locationToServerMapping.pop(loc)
            break
    keynamesToReassign = serverToKeyMapping.get(serverId, [])
    if serverId in serverToKeyMapping:
        del serverToKeyMapping[serverId]
    for keyname, hashkey in keynamesToReassign:
        assignRequest(keyname, hashkey)
    return len(keynamesToReassign)

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
        global answers, serverToKeyMapping, locationToServerMapping
        answers = []
        serverToKeyMapping.clear()
        locationToServerMapping.clear()

        for i in range(len(A)):
            performOperation(A[i], B[i], C[i])
        return answers

obj = Solution()

A = ["ADD", "ASSIGN", "ADD", "ASSIGN", "REMOVE", "ASSIGN"]
B = ["INDIA", "NWFJ", "RUSSIA", "OYVL", "INDIA", "IGAX"]
C = [7, 3, 5, 13, -1, 17 ]

out = obj.solve(A, B, C)
print(out)

A = ['ADD', 'ASSIGN', 'ASSIGN', 'ADD', 'ASSIGN', 'ASSIGN', 'REMOVE', 'ASSIGN']
B = ['INDIA', 'IRYA', 'RGJK', 'RUSSIA', 'BGVH', 'SUKJ', 'INDIA', 'RBRF']
C = [11, 31, 7, 3, 5, 13, -1, 17]

out = obj.solve(A, B, C)
print(out)

