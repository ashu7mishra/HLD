class Solution:
    # @param A : list of strings
    # @param B : list of strings
    # @param C : list of integers
    # @return a list of integers
    def __init__(self):
        self.consistentHash = [None]*360
        self.out = [0]
    
    def userHash(self, username, hashKey):
        p = hashKey
        n = 360
        hashCode = 0
        p_pow = 1
        for i in range(len(username)):
            character = username[i]
            hashCode = (hashCode + (ord(character) - ord('A') + 1) * p_pow) % n
            p_pow = (p_pow * p) % n
        return hashCode
    
    def addServer(self, hashCode):
        self.consistentHash[hashCode%len(self.consistentHash)] = 0
        self.out.append(hashCode)
        
    def assignServer(self, hashCode):
        i = hashCode
        while True:
            if self.consistentHash[i%len(self.consistentHash)] is not None:
                self.consistentHash[i%len(self.consistentHash)] += 1
                self.out.append(1)
                break
            i %= len(self.consistentHash)
            i += 1
            if i%len(self.consistentHash) == hashCode:
                break
    
    def removeServer(self, serverLocation):
        i = serverLocation+1
        while True:
            if self.consistentHash[i%len(self.consistentHash)] is not None:
                self.consistentHash[i%len(self.consistentHash)] += self.consistentHash[serverLocation]
                self.out.append(self.consistentHash[serverLocation])
                self.consistentHash[serverLocation] = None
                break
            i %= len(self.consistentHash)
            i += 1
            if i%len(self.consistentHash) == serverLocation:
                break
            
    
    def solve(self, A, B, C):
        serverLocation = {}
        for i in range(len(A)):
            if A[i] != 'REMOVE':
                hashCode = self.userHash(B[i], C[i])
            if A[i] == 'ADD':
                self.addServer(hashCode)
                serverLocation[B[i]] = hashCode
            elif A[i] == 'ASSIGN':
                self.assignServer(hashCode)
            else:
                self.removeServer(serverLocation[B[i]])
                del serverLocation[B[i]]
            print('*****serverLocation: ', serverLocation)
            print('=====consistentHash: ', [(i, idx) for idx, i in enumerate(self.consistentHash) if i is not None])
        return self.out
                
A = ['ADD', 'ASSIGN', 'ADD', 'ASSIGN', 'REMOVE', 'ASSIGN']
B = ['INDIA', 'NWFJ', 'RUSSIA', 'OYVL', 'INDIA', 'IGAX']
C = [7, 3, 5, 13, -1, 17 ]  
obj = Solution()
print(obj.solve(A, B, C))
# out = 0 31 1 203 0 203


