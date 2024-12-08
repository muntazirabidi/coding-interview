import heapq

class PriorityQueue:
    def __init__(self):
        # Use a list as our heap, where each element is a tuple of (priority, item)
        self._queue = []
        self._index = 0  # For stable sorting

    def push(self, item, priority):
        # Negative priority because heapq gives the smallest element first
        heapq.heappush(self._queue, (-priority, self._index, item))
        self._index += 1

    def pop(self):
        if self._queue:
            return heapq.heappop(self._queue)[-1]  # Return just the item
        else:
            raise KeyError('Priority queue is empty')

    def peek(self):
        if self._queue:
            return self._queue[0][-1]  # Return just the item without removing
        else:
            raise KeyError('Priority queue is empty')

    def is_empty(self):
        return len(self._queue) == 0

# Usage
pq = PriorityQueue()
pq.push("Task 1", 3)  # Lower number means higher priority
pq.push("Task 2", 1)
pq.push("Task 3", 2)

print(pq.pop())  # Should print "Task 2"
print(pq.pop())  # Should print "Task 3"
print(pq.peek())  # Should print "Task 1" without removing it
print(pq.pop())  # Should print "Task 1"
print(pq.is_empty())  # Should print True