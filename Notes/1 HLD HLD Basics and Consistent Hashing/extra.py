answers = []
locationToServerMapping = {}
serverToKeyMappings = {}

def userHash(username, hashKey):
    p = hashKey
    n = 360
    hashCode = 0
    p_pow = 1
    for character in username:
        hashCode = (hashCode + (ord(character) - ord('A') + 1) * p_pow) % n
        p_pow = (p_pow * p) % n
    return hashCode

def assignRequest(keyname, hashKey):
    global locationToServerMapping, serverToKeyMappings
    if not locationToServerMapping:
        return 1000
    keyLocation = userHash(keyname, hashKey)
    serverLocations = sorted(locationToServerMapping.keys())
    for loc in serverLocations:
        if loc >= keyLocation:
            serverID = locationToServerMapping[loc]
            if serverID not in serverToKeyMappings:
                serverToKeyMappings[serverID] = []
            serverToKeyMappings[serverID].append((keyname, hashKey))
            return loc
    serverID = locationToServerMapping[serverLocations[0]]
    if serverID not in serverToKeyMappings:
        serverToKeyMappings[serverID] = []
    serverToKeyMappings[serverID].append((keyname, hashKey))
    return serverLocations[0]

def findRequestsToServe(serverLocation):
    global locationToServerMapping, serverToKeyMappings
    if not serverToKeyMappings:
        return
    serverLocations = sorted(locationToServerMapping.keys())
    for loc in serverLocations:
        if loc > serverLocation:
            serverID = locationToServerMapping[loc]
            keynames = serverToKeyMappings.get(serverID, [])
            serverToKeyMappings[serverID] = []
            for keyname, hashKey in keynames:
                assignRequest(keyname, hashKey)
            return
    serverID = locationToServerMapping[serverLocations[0]]
    keynames = serverToKeyMappings.get(serverID, [])
    serverToKeyMappings[serverID] = []
    for keyname, hashKey in keynames:
        assignRequest(keyname, hashKey)

def addServer(serverID, hashKey):
    global locationToServerMapping, serverToKeyMappings
    firstLocation = userHash(serverID, hashKey)
    locationToServerMapping[firstLocation] = serverID
    findRequestsToServe(firstLocation)
    return len(serverToKeyMappings.get(serverID, []))

def removeServer(serverID):
    global locationToServerMapping, serverToKeyMappings
    for loc, server in locationToServerMapping.items():
        if server == serverID:
            locationToServerMapping.pop(loc)
            break
    keynamesToReassign = serverToKeyMappings.get(serverID, [])
    if serverID in serverToKeyMappings:
        del serverToKeyMappings[serverID]
    for keyname, hashKey in keynamesToReassign:
        assignRequest(keyname, hashKey)
    return len(keynamesToReassign)

def performOperation(A, B, C):
    global answers
    operation = A
    if operation == "ADD":
        serverID = B
        answers.append(addServer(serverID, C))
    elif operation == "REMOVE":
        serverID = B
        answers.append(removeServer(serverID))
    elif operation == "ASSIGN":
        keyname = B
        answers.append(assignRequest(keyname, C))

class Solution:
    # @param A : list of strings
    # @param B : list of strings
    # @param C : list of integers
    # @return a list of integers
    def solve(self, A, B, C):
        global answers, serverToKeyMappings, locationToServerMapping
        serverToKeyMappings.clear()
        locationToServerMapping.clear()
        answers = []
        for i in range(len(A)):
            performOperation(A[i], B[i], C[i])
        return answers