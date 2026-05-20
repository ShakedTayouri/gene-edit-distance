from heapq import heappush, heappop  # library for Priority Queue


class PriorityQueue:

    # Constructor to initialize a Priority Queue
    def __init__(self):
        self.heap = []

    # Inserts a new key 'k'
    def push(self, k):
        heappush(self.heap, k)

    # Method to remove minimum element
    # from Priority Queue
    def pop(self):
        return heappop(self.heap)

    # Method to know if the Queue is empty
    def empty(self):
        return len(self.heap) == 0
