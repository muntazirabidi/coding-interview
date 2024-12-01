# Data Structures and Algorithms Practice Guide

A comprehensive collection of Python implementations for common data structure and algorithm problems, optimized for performance and readability.

## Table of Contents
- [1. Rolling Median Calculator](#1-rolling-median-calculator)
- [2. Top-K Frequent Words](#2-top-k-frequent-words)
- [3. LRU Cache Implementation](#3-lru-cache-implementation)
- [4. Stream Average Calculator](#4-stream-average-calculator)
- [5. Closest Points to Origin](#5-closest-points-to-origin)

## 1. Rolling Median Calculator
Efficiently calculates the rolling median from a stream of numbers using two heaps.

```python
import heapq

class RollingMedianCalculator:
    def __init__(self):
        self.max_heap = []  # Lower half
        self.min_heap = []  # Upper half
    
    def add_number(self, num: float) -> float:
        # Add to max_heap (negative for max heap simulation)
        heapq.heappush(self.max_heap, -num)
        
        # Balance heaps
        if self.max_heap and self.min_heap and \
           -self.max_heap[0] > self.min_heap[0]:
            heapq.heappush(self.min_heap, -heapq.heappop(self.max_heap))
        
        # Keep sizes balanced or max_heap one larger
        if len(self.max_heap) > len(self.min_heap) + 1:
            heapq.heappush(self.min_heap, -heapq.heappop(self.max_heap))
        elif len(self.min_heap) > len(self.max_heap):
            heapq.heappush(self.max_heap, -heapq.heappop(self.min_heap))
        
        return self.get_median()
    
    def get_median(self) -> float:
        if len(self.max_heap) > len(self.min_heap):
            return -self.max_heap[0]
        return (-self.max_heap[0] + self.min_heap[0]) / 2
```

## 2. Top-K Frequent Words
Finds the k most frequent words in a large text file using a hash map and heap.

```python
from collections import Counter
import heapq

def top_k_frequent(words: list[str], k: int) -> list[str]:
    # Count word frequencies
    word_count = Counter(words)
    
    # Create heap of (-freq, word) pairs
    # Using negative frequency for max heap behavior
    heap = [(-freq, word) for word, freq in word_count.items()]
    heapq.heapify(heap)
    
    # Extract top k elements
    return [heapq.heappop(heap)[1] for _ in range(min(k, len(heap)))]

# Process large files in chunks
def process_file(filename: str, k: int, chunk_size: int = 1024*1024) -> list[str]:
    word_count = Counter()
    
    with open(filename, 'r') as file:
        while True:
            chunk = file.read(chunk_size)
            if not chunk:
                break
            words = chunk.split()
            word_count.update(words)
    
    return top_k_frequent(word_count, k)
```

## 3. LRU Cache Implementation
Implements a Least Recently Used (LRU) cache with O(1) time complexity for operations.

```python
class Node:
    def __init__(self, key: int = 0, value: int = 0):
        self.key = key
        self.value = value
        self.prev = None
        self.next = None

class LRUCache:
    def __init__(self, capacity: int):
        self.cache = {}
        self.capacity = capacity
        self.head = Node()
        self.tail = Node()
        self.head.next = self.tail
        self.tail.prev = self.head
    
    def _add_node(self, node: Node):
        node.prev = self.head
        node.next = self.head.next
        self.head.next.prev = node
        self.head.next = node
    
    def _remove_node(self, node: Node):
        prev = node.prev
        new = node.next
        prev.next = new
        new.prev = prev
    
    def get(self, key: int) -> int:
        if key in self.cache:
            node = self.cache[key]
            self._remove_node(node)
            self._add_node(node)
            return node.value
        return -1
    
    def put(self, key: int, value: int):
        if key in self.cache:
            self._remove_node(self.cache[key])
        node = Node(key, value)
        self._add_node(node)
        self.cache[key] = node
        if len(self.cache) > self.capacity:
            lru = self.tail.prev
            self._remove_node(lru)
            del self.cache[lru.key]
```

## 4. Stream Average Calculator
Calculates the running average of the last k elements in a stream with O(1) time complexity.

```python
from collections import deque

class StreamAverageCalculator:
    def __init__(self, window_size: int):
        self.window_size = window_size
        self.window = deque(maxlen=window_size)
        self.window_sum = 0
    
    def add_number(self, num: float) -> float:
        if len(self.window) == self.window_size:
            self.window_sum -= self.window[0]
        self.window.append(num)
        self.window_sum += num
        return self.get_average()
    
    def get_average(self) -> float:
        if not self.window:
            return 0
        return self.window_sum / len(self.window)
```

## 5. Closest Points to Origin
Finds the k closest points to the origin (0,0) using a max heap.

```python
import heapq
from typing import List

def k_closest_points(points: List[List[int]], k: int) -> List[List[int]]:
    def distance(point):
        return point[0]**2 + point[1]**2
    
    # Use max heap with negative distances to keep k smallest
    heap = []
    
    for point in points:
        dist = distance(point)
        if len(heap) < k:
            heapq.heappush(heap, (-dist, point))
        else:
            if -dist > heap[0][0]:
                heapq.heapreplace(heap, (-dist, point))
    
    return [point for _, point in heap]
```

## Usage Examples

```python
# Rolling Median Example
calculator = RollingMedianCalculator()
print(calculator.add_number(5))  # 5.0
print(calculator.add_number(2))  # 3.5
print(calculator.add_number(8))  # 5.0

# Top-K Frequent Words Example
words = ["hello", "world", "hello", "python", "world", "hello"]
print(top_k_frequent(words, 2))  # ['hello', 'world']

# LRU Cache Example
cache = LRUCache(2)
cache.put(1, 1)
cache.put(2, 2)
print(cache.get(1))       # 1
cache.put(3, 3)          # Evicts key 2
print(cache.get(2))       # -1

# Stream Average Example
avg_calc = StreamAverageCalculator(3)
print(avg_calc.add_number(1))  # 1.0
print(avg_calc.add_number(2))  # 1.5
print(avg_calc.add_number(3))  # 2.0
print(avg_calc.add_number(4))  # 3.0

# Closest Points Example
points = [[1,1], [-2,-2], [3,3], [1,-1]]
print(k_closest_points(points, 2))  # [[1,1], [1,-1]]
```

Let me help you understand when to use heaps versus sorted arrays for finding medians, as this is a key decision that can greatly affect your code's performance.
Let's compare both approaches by looking at what happens when we need to find the median in different scenarios:
Scenario 1: One-time Median Calculation
If you just need to find the median once for a fixed set of numbers:
pythonCopy# Using sorted array
numbers = [4, 1, 7, 3, 8, 2]
sorted_nums = sorted(numbers)  # O(n log n)
# Find median
if len(sorted_nums) % 2 == 0:
    median = (sorted_nums[len(sorted_nums)//2 - 1] + sorted_nums[len(sorted_nums)//2]) / 2
else:
    median = sorted_nums[len(sorted_nums)//2]
Scenario 2: Stream of Numbers (Numbers keep coming)
pythonCopy# Using heaps (as shown in previous example)
calculator = RollingMedianCalculator()
calculator.add_number(4)  # O(log n)
calculator.add_number(1)  # O(log n)
calculator.add_number(7)  # O(log n)
Here's why the choice matters:
Sorted Array Approach:

Advantages:

Simpler to understand and implement
Better for one-time calculations
Uses less memory (just one array)


Disadvantages:

Requires O(n log n) time to sort
Very inefficient for streaming data as you need to resort every time



Heap Approach:

Advantages:

Efficient for streaming data: O(log n) per insertion
Maintains running median without resorting
Perfect for interview questions about "running" or "streaming" medians


Disadvantages:

More complex to implement
Uses more memory (two heaps)
Overkill for one-time calculations



So when should you use each? Here's a simple decision guide:

Use Sorted Arrays when:

pythonCopy# One-time median calculation
def find_median_sorted(numbers):
    sorted_nums = sorted(numbers)
    n = len(sorted_nums)
    mid = n // 2
    return sorted_nums[mid] if n % 2 else (sorted_nums[mid-1] + sorted_nums[mid]) / 2

# Example
numbers = [4, 1, 7, 3, 8, 2]
median = find_median_sorted(numbers)

Use Heaps when:

pythonCopy# The question mentions:
# - "Running median"
# - "Streaming data"
# - "Find median after each insertion"
# - "Calculate median as numbers come in"

calculator = RollingMedianCalculator()
stream = [4, 1, 7, 3, 8, 2]
for num in stream:
    median = calculator.add_number(num)
    print(f"After adding {num}, median is {median}")
Here's a practical example to help you recognize when to use each:
pythonCopy# Interview Question 1: "Find the median of this array"
def question1(numbers):
    # Use sorted array - it's simpler and sufficient
    return find_median_sorted(numbers)

# Interview Question 2: "Design a class that finds the median 
# of all numbers seen so far as new numbers are added"
class question2:
    # Use heaps - we need to maintain running median
    def __init__(self):
        self.calculator = RollingMedianCalculator()
    
    def add_number(self, num):
        return self.calculator.add_number(num)
Remember: The key is to look for words like "running", "streaming", or "as numbers come in" in the question. These are strong hints that you should use heaps. If it's just finding the median of a fixed set of numbers, use sorting.

## Contributing
Feel free to contribute by:
1. Forking the repository
2. Creating a new branch for your feature
3. Submitting a pull request


