# Queue Data Structure - Complete Guide

## Table of Contents
- [Introduction](#introduction)
- [Types of Queues](#types-of-queues)
- [Implementation](#implementation)
- [Core Operations](#core-operations)
- [Common Applications](#common-applications)
- [Interview Problems](#interview-problems)
- [Time Complexity](#time-complexity)
- [Best Practices & Tips](#best-practices--tips)

## Introduction

A Queue is a linear data structure that follows the First-In-First-Out (FIFO) principle. Think of it like a line of people waiting - the first person to join the line is the first to leave.

### Key Characteristics:
- Elements are added at the rear/tail (enqueue)
- Elements are removed from the front/head (dequeue)
- First element added is the first to be removed
- Perfect for managing tasks that need to be processed in order

## Types of Queues

### 1. Simple Queue
Basic FIFO queue implementation.

### 2. Circular Queue
```python
class CircularQueue:
    def __init__(self, capacity):
        self.capacity = capacity
        self.queue = [None] * capacity
        self.front = self.rear = -1
        self.size = 0
    
    def enqueue(self, item):
        if self.is_full():
            raise Exception("Queue is full")
        
        if self.front == -1:
            self.front = 0
        self.rear = (self.rear + 1) % self.capacity
        self.queue[self.rear] = item
        self.size += 1
    
    def dequeue(self):
        if self.is_empty():
            raise Exception("Queue is empty")
        
        item = self.queue[self.front]
        self.queue[self.front] = None
        
        if self.front == self.rear:
            self.front = self.rear = -1
        else:
            self.front = (self.front + 1) % self.capacity
        
        self.size -= 1
        return item
    
    def is_empty(self):
        return self.size == 0
    
    def is_full(self):
        return self.size == self.capacity
```

### 3. Priority Queue
```python
import heapq

class PriorityQueue:
    def __init__(self):
        self._queue = []
        self._index = 0
    
    def push(self, item, priority):
        # Lower priority number = higher priority
        heapq.heappush(self._queue, (priority, self._index, item))
        self._index += 1
    
    def pop(self):
        if self._queue:
            return heapq.heappop(self._queue)[-1]
        raise IndexError("pop from empty queue")
    
    def peek(self):
        if self._queue:
            return self._queue[0][-1]
        raise IndexError("peek at empty queue")
```

### 4. Double-ended Queue (Deque)
```python
from collections import deque

class Deque:
    def __init__(self):
        self.items = deque()
    
    def add_front(self, item):
        self.items.appendleft(item)
    
    def add_rear(self, item):
        self.items.append(item)
    
    def remove_front(self):
        return self.items.popleft()
    
    def remove_rear(self):
        return self.items.pop()
    
    def is_empty(self):
        return len(self.items) == 0
```

## Implementation

### Basic Queue Using List
```python
class Queue:
    def __init__(self):
        self.items = []
    
    def enqueue(self, item):
        self.items.append(item)
    
    def dequeue(self):
        if not self.is_empty():
            return self.items.pop(0)
        raise IndexError("dequeue from empty queue")
    
    def front(self):
        if not self.is_empty():
            return self.items[0]
        raise IndexError("front from empty queue")
    
    def is_empty(self):
        return len(self.items) == 0
    
    def size(self):
        return len(self.items)
```

### Queue Using Linked List
```python
class Node:
    def __init__(self, value):
        self.value = value
        self.next = None

class LinkedQueue:
    def __init__(self):
        self.front = None
        self.rear = None
        self._size = 0
    
    def enqueue(self, value):
        new_node = Node(value)
        if self.rear:
            self.rear.next = new_node
            self.rear = new_node
        else:
            self.front = self.rear = new_node
        self._size += 1
    
    def dequeue(self):
        if self.is_empty():
            raise IndexError("dequeue from empty queue")
        
        value = self.front.value
        self.front = self.front.next
        if not self.front:
            self.rear = None
        self._size -= 1
        return value
    
    def is_empty(self):
        return self.front is None
    
    def size(self):
        return self._size
```

## Core Operations

1. **enqueue(item)**: Add an element to the rear
   ```python
   queue.enqueue(5)  # queue: [5]
   queue.enqueue(10) # queue: [5, 10]
   ```

2. **dequeue()**: Remove and return the front element
   ```python
   value = queue.dequeue() # Returns 5, queue: [10]
   ```

3. **front()**: View the front element without removing it
   ```python
   front = queue.front() # Returns 10, queue unchanged
   ```

4. **is_empty()**: Check if queue is empty
   ```python
   empty = queue.is_empty() # Returns False
   ```

## Common Applications

### 1. BFS Implementation
```python
from collections import deque

def bfs(graph, start):
    visited = set()
    queue = deque([start])
    visited.add(start)
    
    while queue:
        vertex = queue.popleft()
        print(vertex, end=' ')
        
        for neighbor in graph[vertex]:
            if neighbor not in visited:
                visited.add(neighbor)
                queue.append(neighbor)

# Example usage:
graph = {
    'A': ['B', 'C'],
    'B': ['A', 'D', 'E'],
    'C': ['A', 'F'],
    'D': ['B'],
    'E': ['B', 'F'],
    'F': ['C', 'E']
}

bfs(graph, 'A')  # Outputs: A B C D E F
```

### 2. Task Scheduling
```python
class TaskScheduler:
    def __init__(self):
        self.task_queue = PriorityQueue()
    
    def add_task(self, task, priority):
        self.task_queue.push(task, priority)
    
    def process_next_task(self):
        if not self.task_queue._queue:
            return None
        return self.task_queue.pop()
```

## Interview Problems

### 1. Implementing Stack using Queues
```python
from collections import deque

class StackUsingQueues:
    def __init__(self):
        self.q1 = deque()
        self.q2 = deque()
    
    def push(self, x):
        # Add to q2
        self.q2.append(x)
        # Move all elements from q1 to q2
        while self.q1:
            self.q2.append(self.q1.popleft())
        # Swap q1 and q2
        self.q1, self.q2 = self.q2, self.q1
    
    def pop(self):
        if self.q1:
            return self.q1.popleft()
        return None
    
    def top(self):
        if self.q1:
            return self.q1[0]
        return None
```

### 2. Sliding Window Maximum
```python
from collections import deque

def max_sliding_window(nums, k):
    result = []
    window = deque()
    
    for i, num in enumerate(nums):
        # Remove indices that are out of window
        while window and window[0] <= i - k:
            window.popleft()
        
        # Remove smaller elements
        while window and nums[window[-1]] < num:
            window.pop()
        
        window.append(i)
        
        if i >= k - 1:
            result.append(nums[window[0]])
    
    return result

# Example usage:
print(max_sliding_window([1,3,-1,-3,5,3,6,7], 3))  # [3,3,5,5,6,7]
```

## Time Complexity

Operation  | Array-based | Linked List-based | Priority Queue
-----------|------------|-------------------|---------------
Enqueue    | O(1)*      | O(1)             | O(log n)
Dequeue    | O(n)       | O(1)             | O(log n)
Front      | O(1)       | O(1)             | O(1)
IsEmpty    | O(1)       | O(1)             | O(1)
Size       | O(1)       | O(1)             | O(1)

* Note: Using a circular array implementation

## Best Practices & Tips

### 1. Implementation Choice Guidelines
- Use array-based implementation when:
  - Fixed size is known
  - Random access is needed
  - Memory locality is important
- Use linked list-based implementation when:
  - Dynamic sizing is needed
  - Constant time operations are crucial
- Use priority queue when:
  - Elements need to be processed based on priority
  - Heap properties are beneficial

### 2. Common Pitfalls
- Not handling empty queue cases
- Forgetting to update front/rear pointers
- Memory leaks in linked implementations
- Not considering circular buffer for array implementation

### 3. Interview Tips
1. Always clarify:
   - FIFO vs Priority requirements
   - Size constraints
   - Threading requirements
   - Performance expectations

2. Consider:
   - Is ordering important?
   - Would a priority queue be more appropriate?
   - Is random access needed?
   - Could a deque solve the problem better?

3. Common Queue Patterns:
   - Level-order traversal
   - BFS implementation
   - Task scheduling
   - Buffer management
   - Producer-consumer problems

### 4. Testing Strategies
```python
def test_queue():
    q = Queue()
    
    # Test empty queue
    assert q.is_empty() == True
    
    # Test enqueue
    q.enqueue(1)
    assert q.front() == 1
    
    # Test multiple operations
    q.enqueue(2)
    q.enqueue(3)
    assert q.dequeue() == 1
    assert q.front() == 2
    assert q.size() == 2
```

Remember:
- Always handle edge cases
- Consider memory management
- Think about thread safety
- Document assumptions
- Test corner cases thoroughly
- Consider using built-in implementations for production code
