# Arrays and Matrix - Complete Interview Guide

## Table of Contents
- [Array Fundamentals](#array-fundamentals)
- [Common Array Patterns](#common-array-patterns)
- [Matrix Operations](#matrix-operations)
- [Matrix Patterns](#matrix-patterns)
- [Interview Techniques](#interview-techniques)
- [Common Problems with Solutions](#common-problems-with-solutions)
- [Time Complexity Analysis](#time-complexity-analysis)
- [Best Practices](#best-practices)

## Array Fundamentals

### Array Basics
```python
# Array initialization
arr = [1, 2, 3, 4, 5]
arr_2d = [[1, 2, 3], [4, 5, 6]]

# Basic operations
length = len(arr)                # Get length
element = arr[0]                 # Access element
arr.append(6)                    # Add element at end
arr.insert(1, 7)                # Insert at index
arr.pop()                       # Remove last element
arr.remove(3)                   # Remove first occurrence of value
```

### Array Slicing
```python
arr = [0, 1, 2, 3, 4, 5]
subarray = arr[1:4]     # Get elements from index 1 to 3
reversed_arr = arr[::-1] # Reverse array
step_arr = arr[::2]     # Get every second element
```

## Common Array Patterns

### 1. Two Pointer Technique
```python
def two_sum(arr, target):
    left, right = 0, len(arr) - 1
    
    while left < right:
        current_sum = arr[left] + arr[right]
        if current_sum == target:
            return [left, right]
        elif current_sum < target:
            left += 1
        else:
            right -= 1
    return []
```

### 2. Sliding Window
```python
def max_sum_subarray(arr, k):
    if not arr or k <= 0:
        return 0
        
    # Initialize first window
    window_sum = sum(arr[:k])
    max_sum = window_sum
    
    # Slide window
    for i in range(len(arr) - k):
        window_sum = window_sum - arr[i] + arr[i + k]
        max_sum = max(max_sum, window_sum)
        
    return max_sum
```

### 3. Prefix Sum
```python
def prefix_sum_array(arr):
    prefix = [0] * (len(arr) + 1)
    for i in range(len(arr)):
        prefix[i + 1] = prefix[i] + arr[i]
    return prefix

def range_sum(prefix, left, right):
    return prefix[right + 1] - prefix[left]
```

### 4. Binary Search
```python
def binary_search(arr, target):
    left, right = 0, len(arr) - 1
    
    while left <= right:
        mid = (left + right) // 2
        if arr[mid] == target:
            return mid
        elif arr[mid] < target:
            left = mid + 1
        else:
            right = mid - 1
            
    return -1
```

### 5. Dutch National Flag (3-way partitioning)
```python
def sort_colors(nums):
    """
    Sort array with three possible values (0, 1, 2)
    """
    low = mid = 0
    high = len(nums) - 1
    
    while mid <= high:
        if nums[mid] == 0:
            nums[low], nums[mid] = nums[mid], nums[low]
            low += 1
            mid += 1
        elif nums[mid] == 1:
            mid += 1
        else:  # nums[mid] == 2
            nums[mid], nums[high] = nums[high], nums[mid]
            high -= 1
```

## Matrix Operations

### Basic Matrix Operations
```python
# Create matrix
matrix = [[1, 2, 3],
          [4, 5, 6],
          [7, 8, 9]]

# Access elements
element = matrix[row][col]

# Get dimensions
rows = len(matrix)
cols = len(matrix[0])

# Initialize matrix with zeros
matrix = [[0] * cols for _ in range(rows)]
```

### Matrix Traversal
```python
def print_matrix(matrix):
    # Row-wise traversal
    for i in range(len(matrix)):
        for j in range(len(matrix[0])):
            print(matrix[i][j], end=' ')
        print()

def get_neighbors(matrix, row, col):
    """Get valid neighboring cells"""
    rows, cols = len(matrix), len(matrix[0])
    directions = [(0, 1), (1, 0), (0, -1), (-1, 0)]  # right, down, left, up
    
    neighbors = []
    for dx, dy in directions:
        new_row, new_col = row + dx, col + dy
        if 0 <= new_row < rows and 0 <= new_col < cols:
            neighbors.append((new_row, new_col))
    
    return neighbors
```

## Matrix Patterns

### 1. Spiral Traversal
```python
def spiral_order(matrix):
    if not matrix:
        return []
        
    result = []
    top, bottom = 0, len(matrix)
    left, right = 0, len(matrix[0])
    
    while top < bottom and left < right:
        # Traverse right
        for i in range(left, right):
            result.append(matrix[top][i])
        top += 1
        
        # Traverse down
        for i in range(top, bottom):
            result.append(matrix[i][right-1])
        right -= 1
        
        if top < bottom and left < right:
            # Traverse left
            for i in range(right-1, left-1, -1):
                result.append(matrix[bottom-1][i])
            bottom -= 1
            
            # Traverse up
            for i in range(bottom-1, top-1, -1):
                result.append(matrix[i][left])
            left += 1
            
    return result
```

### 2. Diagonal Traversal
```python
def diagonal_traverse(matrix):
    if not matrix:
        return []
        
    rows, cols = len(matrix), len(matrix[0])
    result = []
    
    for d in range(rows + cols - 1):
        temp = []
        # Find row and column for current diagonal
        row = 0 if d < cols else d - cols + 1
        col = d if d < cols else cols - 1
        
        while row < rows and col >= 0:
            temp.append(matrix[row][col])
            row += 1
            col -= 1
            
        if d % 2 == 0:
            result.extend(temp[::-1])
        else:
            result.extend(temp)
            
    return result
```

### 3. DFS in Matrix
```python
def dfs_matrix(matrix, row, col, visited=None):
    if visited is None:
        visited = set()
        
    rows, cols = len(matrix), len(matrix[0])
    
    # Base cases
    if (row < 0 or row >= rows or 
        col < 0 or col >= cols or 
        (row, col) in visited):
        return
        
    visited.add((row, col))
    
    # Process current cell
    print(matrix[row][col])
    
    # Visit neighbors
    directions = [(0, 1), (1, 0), (0, -1), (-1, 0)]
    for dx, dy in directions:
        dfs_matrix(matrix, row + dx, col + dy, visited)
```

### 4. BFS in Matrix
```python
from collections import deque

def bfs_matrix(matrix, start_row, start_col):
    rows, cols = len(matrix), len(matrix[0])
    visited = set([(start_row, start_col)])
    queue = deque([(start_row, start_col)])
    
    while queue:
        row, col = queue.popleft()
        
        # Process current cell
        print(matrix[row][col])
        
        # Visit neighbors
        for new_row, new_col in get_neighbors(matrix, row, col):
            if (new_row, new_col) not in visited:
                visited.add((new_row, new_col))
                queue.append((new_row, new_col))
```

## Common Problems with Solutions

### 1. Search in Sorted Matrix
```python
def search_matrix(matrix, target):
    if not matrix or not matrix[0]:
        return False
        
    rows, cols = len(matrix), len(matrix[0])
    row, col = 0, cols - 1
    
    while row < rows and col >= 0:
        if matrix[row][col] == target:
            return True
        elif matrix[row][col] > target:
            col -= 1
        else:
            row += 1
            
    return False
```

### 2. Rotate Matrix
```python
def rotate_matrix(matrix):
    n = len(matrix)
    
    # Transpose matrix
    for i in range(n):
        for j in range(i, n):
            matrix[i][j], matrix[j][i] = matrix[j][i], matrix[i][j]
    
    # Reverse each row
    for i in range(n):
        matrix[i].reverse()
```

### 3. Islands Count (Connected Components)
```python
def count_islands(grid):
    if not grid:
        return 0
        
    rows, cols = len(grid), len(grid[0])
    islands = 0
    
    def dfs(row, col):
        if (row < 0 or row >= rows or 
            col < 0 or col >= cols or 
            grid[row][col] != '1'):
            return
            
        # Mark as visited
        grid[row][col] = '#'
        
        # Visit all neighbors
        directions = [(0, 1), (1, 0), (0, -1), (-1, 0)]
        for dx, dy in directions:
            dfs(row + dx, col + dy)
    
    for i in range(rows):
        for j in range(cols):
            if grid[i][j] == '1':
                islands += 1
                dfs(i, j)
                
    return islands
```

## Time Complexity Analysis

Operation | Time Complexity | Space Complexity
----------|----------------|------------------
Access    | O(1)           | -
Search    | O(n)           | O(1)
Binary Search | O(log n)    | O(1)
Insert    | O(n)           | O(1)
Delete    | O(n)           | O(1)
Traverse  | O(n)           | O(1)
Matrix Traversal | O(m×n)   | O(1)
DFS/BFS   | O(m×n)         | O(m×n)

## Best Practices

1. Array Manipulation:
   - Always check array bounds
   - Consider edge cases (empty array, single element)
   - Look for sorting requirements
   - Consider using additional data structures

2. Matrix Operations:
   - Verify matrix dimensions
   - Handle empty matrix cases
   - Be careful with row/column indices
   - Consider space optimization

3. Interview Tips:
   - Start with brute force approach
   - Look for patterns (sorting, two pointers, etc.)
   - Consider time/space tradeoffs
   - Test with example inputs
   - Optimize after getting a working solution

4. Common Optimizations:
   - Use two pointers for linear traversal
   - Consider binary search for sorted arrays
   - Use hash tables for O(1) lookup
   - Implement in-place modifications when possible
   - Use prefix sums for range queries
