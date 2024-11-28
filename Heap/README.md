# Heap Data Structure & Priority Queue in Python

## Table of Contents
- [Introduction](#introduction)
- [Implementation](#implementation)
- [Built-in Heapq Module](#built-in-heapq-module)
- [Common Operations](#common-operations)
- [Advanced Usage](#advanced-usage)
- [Common Problems](#common-problems)
- [Interview Tips](#interview-tips)

## Introduction

A heap is a specialized tree-based data structure that satisfies the heap property. Python's built-in `heapq` module implements a min heap.

### Key Properties
- Complete Binary Tree
- Parent is always smaller (min-heap) or larger (max-heap) than children
- Root is always the minimum (min-heap) or maximum (max-heap) element
- Height is O(log n)

## Implementation

### Basic Min Heap Implementation
```python
class MinHeap:
    def __init__(self):
        self.heap = []
        
    def parent(self, i):
        return (i - 1) // 2
        
    def left_child(self, i):
        return 2 * i + 1
        
    def right_child(self, i):
        return 2 * i + 2
        
    def swap(self, i, j):
        self.heap[i], self.heap[j] = self.heap[j], self.heap[i]
        
    def insert(self, key):
        self.heap.append(key)
        self._sift_up(len(self.heap) - 1)
        
    def _sift_up(self, i):
        parent = self.parent(i)
        if i > 0 and self.heap[i] < self.heap[parent]:
            self.swap(i, parent)
            self._sift_up(parent)
            
    def extract_min(self):
        if not self.heap:
            return None
            
        if len(self.heap) == 1:
            return self.heap.pop()
            
        min_val = self.heap[0]
        self.heap[0] = self.heap.pop()
        self._sift_down(0)
        
        return min_val
        
    def _sift_down(self, i):
        min_index = i
        l = self.left_child(i)
        r = self.right_child(i)
        
        if l < len(self.heap) and self.heap[l] < self.heap[min_index]:
            min_index = l
        if r < len(self.heap) and self.heap[r] < self.heap[min_index]:
            min_index = r
            
        if i != min_index:
            self.swap(i, min_index)
            self._sift_down(min_index)
```

## Built-in Heapq Module

Python's `heapq` module provides an efficient implementation of a min heap.

### Basic Operations
```python
import heapq

# Create heap from list
nums = [3, 1, 4, 1, 5, 9, 2, 6, 5, 3]
heapq.heapify(nums)  # Convert list into heap in-place

# Push element
heapq.heappush(nums, 0)

# Pop smallest element
smallest = heapq.heappop(nums)

# Push and pop in one operation
next_smallest = heapq.heappushpop(nums, 4)

# Replace (pop and push) in one operation
replaced = heapq.heapreplace(nums, 8)

# Get n smallest elements
n_smallest = heapq.nsmallest(3, nums)

# Get n largest elements
n_largest = heapq.nlargest(3, nums)
```

### Max Heap Using Heapq
```python
class MaxHeap:
    def __init__(self):
        self.heap = []
        
    def push(self, val):
        heapq.heappush(self.heap, -val)
        
    def pop(self):
        return -heapq.heappop(self.heap)
        
    def peek(self):
        return -self.heap[0] if self.heap else None
```

## Common Operations

### 1. Priority Queue Implementation
```python
from dataclasses import dataclass
import heapq

@dataclass
class PriorityItem:
    priority: int
    data: any
    
    def __lt__(self, other):
        return self.priority < other.priority

class PriorityQueue:
    def __init__(self):
        self.queue = []
        
    def push(self, item, priority):
        heapq.heappush(self.queue, PriorityItem(priority, item))
        
    def pop(self):
        if not self.queue:
            return None
        return heapq.heappop(self.queue).data
        
    def peek(self):
        if not self.queue:
            return None
        return self.queue[0].data
```

### 2. Merge K Sorted Lists
```python
def merge_k_sorted_lists(lists):
    heap = []
    result = []
    
    # Add first element from each list
    for i, lst in enumerate(lists):
        if lst:
            heapq.heappush(heap, (lst[0], i, 0))
            
    while heap:
        val, list_idx, elem_idx = heapq.heappop(heap)
        result.append(val)
        
        if elem_idx + 1 < len(lists[list_idx]):
            next_val = lists[list_idx][elem_idx + 1]
            heapq.heappush(heap, (next_val, list_idx, elem_idx + 1))
            
    return result
```

### 3. K-th Largest Element
```python
def find_kth_largest(nums, k):
    # Using min heap
    heap = []
    for num in nums:
        heapq.heappush(heap, num)
        if len(heap) > k:
            heapq.heappop(heap)
    return heap[0]
```

## Advanced Usage

### 1. Custom Comparators
```python
from dataclasses import dataclass
import heapq

@dataclass
class Task:
    name: str
    priority: int
    timestamp: float
    
    def __lt__(self, other):
        if self.priority != other.priority:
            return self.priority < other.priority
        return self.timestamp < other.timestamp
```

### 2. Dijkstra's Algorithm
```python
def dijkstra(graph, start):
    distances = {node: float('infinity') for node in graph}
    distances[start] = 0
    heap = [(0, start)]
    visited = set()
    
    while heap:
        current_distance, current_node = heapq.heappop(heap)
        
        if current_node in visited:
            continue
            
        visited.add(current_node)
        
        for neighbor, weight in graph[current_node].items():
            distance = current_distance + weight
            
            if distance < distances[neighbor]:
                distances[neighbor] = distance
                heapq.heappush(heap, (distance, neighbor))
                
    return distances
```

## Time Complexity

| Operation       | Time Complexity |
|----------------|----------------|
| Push           | O(log n)       |
| Pop            | O(log n)       |
| Peek           | O(1)           |
| Heapify        | O(n)          |
| Build Heap     | O(n)          |

## Interview Tips

1. **Built-in vs Custom Implementation**
   - Use `heapq` for standard problems
   - Implement custom heap for special requirements
   - Know how to modify for max heap

2. **Common Patterns**
   - K-th element problems
   - Merge K sorted arrays/lists
   - Priority scheduling
   - Graph algorithms

3. **Edge Cases**
   - Empty heap
   - Single element
   - Duplicate elements
   - Equal priorities

4. **Optimization Tips**
   - Use tuple comparison for multiple keys
   - Leverage heappushpop/heapreplace
   - Consider memory vs time tradeoffs

## Common Mistakes to Avoid

1. Forgetting heap is min heap by default
2. Not handling empty heap cases
3. Incorrect custom comparators
4. Modifying elements after insertion
5. Not considering duplicate priorities

## Debugging Tips

1. Print heap array to verify structure
2. Check heap property at each level
3. Verify size after operations
4. Test with small examples first

## Resources

1. [Python heapq documentation](https://docs.python.org/3/library/heapq.html)
2. [Time Complexity Analysis](https://wiki.python.org/moin/TimeComplexity)
3. [Visualgo - Heap Visualization](https://visualgo.net/en/heap)

## Practice Problems

1. Top K Frequent Elements
2. Merge K Sorted Lists
3. Find Median from Data Stream
4. Task Scheduler
5. Minimum Cost to Connect Sticks
