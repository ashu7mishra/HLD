class LRUCache:

    # @param capacity, an integer
    def __init__(self, capacity):
        self.capacity = capacity
        self.LRU = {}
        self.count = 0

        # @return an integer

    def get(self, key):
        if key in self.LRU:
            return self.LRU[key][0]
        return -1

    # @param key, an integer
    # @param value, an integer
    # @return nothing
    def set(self, key, value):
        if self.count < self.capacity:
            self.LRU[key] = [value, self.count]
            self.count += 1
        else:
            for old_key in self.LRU:
                if self.LRU[old_key][1] == self.count:
                    break
            del self.LRU[old_key]
            # for old_key in self.LRU:
            #     if self.LRU[old_key][1] != self.count:
            #         self.LRU[old_key][1] += 1
            self.LRU[key] = [value, self.count]


obj = LRUCache(2)

obj.set(1, 10)
obj.set(5, 12)
print(obj.get(5))
print(obj.get(1))
print(obj.get(10))
obj.set(6, 14)
print(obj.get(5))
print(obj.LRU)
obj.set(7, 18)
print(obj.LRU)