# Heap Data Structures:

## Introduction

A heap is a specialized tree-based data structure that satisfies the heap property. Understanding heaps is fundamental for efficient priority queue implementations and sorting algorithms. This guide explains heaps from the ground up, starting with their foundational concepts.

## Table of Contents

1. [Binary Tree Array Representation](#binary-tree-array-representation)
2. [Complete Binary Trees](#complete-binary-trees)
3. [Heaps](#heaps)
4. [Heapify](#heapify)
5. [Heap Sort](#heap-sort)
6. [Priority Queue](#priority-queue)
7. [Time Complexities](#time-complexities)

## Binary Tree Array Representation

### Understanding Array-Based Trees

When we represent a binary tree using an array, we maintain two crucial aspects:

1. The element values themselves
2. Parent-child relationships between nodes

For any node at index `i` in the array:

- Its left child is located at index: `2i`
- Its right child is located at index: `2i + 1`
- Its parent is located at index: `floor(i/2)`

### Implementation

Here's how we can implement this array representation in Python:

```python
class BinaryTreeArray:
    def __init__(self, size):
        # Index 0 remains unused to simplify parent-child calculations
        self.arr = [None] * (size + 1)
        self.size = size

    def set_node(self, index, value):
        # Ensure index is within valid range
        if 1 <= index <= self.size:
            self.arr[index] = value

    def get_left_child_index(self, index):
        left_index = 2 * index
        return left_index if left_index <= self.size else None

    def get_right_child_index(self, index):
        right_index = 2 * index + 1
        return right_index if right_index <= self.size else None

    def get_parent_index(self, index):
        # Root node (index 1) has no parent
        return index // 2 if index > 1 else None
```

## Complete Binary Trees

### Key Properties

A complete binary tree must satisfy two essential conditions:

1. All levels, except possibly the last one, must be completely filled
2. Nodes in the last level must be as far left as possible

This means there should be no gaps between nodes when represented in an array.

### Verification Implementation

Here's how we can verify if a binary tree is complete:

```python
def is_complete_binary_tree(arr):
    """
    Verifies if an array represents a complete binary tree

    Parameters:
        arr: Array representation of the tree (index 0 unused)
    Returns:
        bool: True if tree is complete, False otherwise
    """
    if not arr or len(arr) < 2:
        return True

    # Find last non-empty node
    last_index = len(arr) - 1
    while last_index > 0 and arr[last_index] is None:
        last_index -= 1

    # Check for gaps before last_index
    for i in range(1, last_index + 1):
        if arr[i] is None:
            return False

    return True
```

## Heaps

### Types of Heaps

A heap is a complete binary tree that satisfies the heap property. There are two main types:

1. **Max Heap**: Parent nodes are greater than or equal to their children
2. **Min Heap**: Parent nodes are less than or equal to their children

### Max Heap Implementation

Here's a complete implementation of a max heap:

```python
class MaxHeap:
    def __init__(self):
        # Start with [None] to maintain 1-based indexing
        self.heap = [None]

    def parent(self, i):
        return i // 2

    def left_child(self, i):
        return 2 * i

    def right_child(self, i):
        return 2 * i + 1

    def swap(self, i, j):
        self.heap[i], self.heap[j] = self.heap[j], self.heap[i]

    def insert(self, key):
        """
        Insert a new key into the heap
        Time Complexity: O(log n)
        """
        self.heap.append(key)
        self._bubble_up(len(self.heap) - 1)

    def _bubble_up(self, i):
        """
        Restore heap property by moving a node up
        """
        parent = self.parent(i)
        if i > 1 and self.heap[i] > self.heap[parent]:
            self.swap(i, parent)
            self._bubble_up(parent)

    def extract_max(self):
        """
        Remove and return the maximum element
        Time Complexity: O(log n)
        """
        if len(self.heap) < 2:
            return None

        max_val = self.heap[1]
        self.heap[1] = self.heap[-1]
        self.heap.pop()

        if len(self.heap) > 1:
            self._bubble_down(1)

        return max_val

    def _bubble_down(self, i):
        """
        Restore heap property by moving a node down
        """
        largest = i
        left = self.left_child(i)
        right = self.right_child(i)

        if left < len(self.heap) and self.heap[left] > self.heap[largest]:
            largest = left

        if right < len(self.heap) and self.heap[right] > self.heap[largest]:
            largest = right

        if largest != i:
            self.swap(i, largest)
            self._bubble_down(largest)
```

## Heapify

### Understanding Heapify

Heapify is an efficient algorithm that converts an array into a heap in-place. It works bottom-up, which is more efficient than inserting elements one by one.

### Implementation

```python
def heapify(arr):
    """
    Convert an array into a max heap in-place
    Time Complexity: O(n)
    """
    # Start from last non-leaf node
    for i in range(len(arr) // 2, -1, -1):
        _bubble_down(arr, i, len(arr))

def _bubble_down(arr, i, n):
    """
    Helper function to maintain heap property
    """
    largest = i
    left = 2 * i + 1
    right = 2 * i + 2

    if left < n and arr[left] > arr[largest]:
        largest = left

    if right < n and arr[right] > arr[largest]:
        largest = right

    if largest != i:
        arr[i], arr[largest] = arr[largest], arr[i]
        _bubble_down(arr, largest, n)
```

## Heap Sort

### Algorithm Description

Heap sort leverages the properties of a max heap to sort an array:

1. First, build a max heap from the input array
2. Repeatedly extract the maximum element and place it at the end

### Implementation

```python
def heap_sort(arr):
    """
    Sort an array using heap sort
    Time Complexity: O(n log n)
    """
    # Build initial max heap
    heapify(arr)

    # Extract elements one by one
    for i in range(len(arr) - 1, 0, -1):
        # Move current root to end
        arr[0], arr[i] = arr[i], arr[0]
        # Restore heap property for remaining elements
        _bubble_down(arr, 0, i)

    return arr
```

## Priority Queue

### Overview

A priority queue is an abstract data type where elements have priorities attached to them. Heaps provide an efficient implementation of priority queues.

### Implementation

```python
class PriorityQueue:
    def __init__(self, is_min_heap=False):
        """
        Initialize priority queue
        is_min_heap: If True, creates a min heap (minimum priority first)
                    If False, creates a max heap (maximum priority first)
        """
        self.heap = MaxHeap() if not is_min_heap else MinHeap()

    def enqueue(self, item):
        """Add an item to the priority queue"""
        self.heap.insert(item)

    def dequeue(self):
        """Remove and return the highest priority item"""
        return self.heap.extract_max()  # or extract_min for min heap

    def peek(self):
        """View the highest priority item without removing it"""
        return self.heap.heap[1] if len(self.heap.heap) > 1 else None

    def is_empty(self):
        """Check if the priority queue is empty"""
        return len(self.heap.heap) <= 1
```

## Time Complexities

Here are the time complexities for various heap operations:

| Operation           | Time Complexity | Description                 |
| ------------------- | --------------- | --------------------------- |
| Insertion           | O(log n)        | Adding a new element        |
| Deletion            | O(log n)        | Removing the root element   |
| Get Maximum/Minimum | O(1)            | Viewing the root element    |
| Heapify             | O(n)            | Converting an array to heap |
| Heap Sort           | O(n log n)      | Sorting using heap          |

### Space Complexity

Heap sort can be performed in-place, requiring O(1) additional space, making it space-efficient compared to some other sorting algorithms.

## Conclusion

Heaps are powerful data structures that provide efficient implementations for priority queues and sorting. Their logarithmic time complexity for most operations makes them particularly useful in scenarios requiring frequent access to maximum/minimum elements or priority-based processing.

Ref: https://www.youtube.com/watch?v=HqPJF2L5h9U&t=18s
