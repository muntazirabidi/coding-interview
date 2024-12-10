# Sliding Window Technique Guide

## Introduction

The sliding window technique is a computational method that converts two nested loops into a single loop, reducing time complexity from O(n²) to O(n). It's particularly useful for solving array/string problems involving contiguous sequences.

## Core Concept

A "window" is a subarray or substring that moves from left to right through the data structure. The window can:

- Be fixed-size (e.g., find max sum of k consecutive elements)
- Have variable size (e.g., find longest substring with k distinct characters)
- Grow or shrink based on conditions

## When to Use

Use sliding window when the problem involves:

- Contiguous sequence of elements (subarray/substring)
- Finding min/max/sum/average over all possible subarrays of size k
- Finding longest/shortest substring with certain constraints
- Pattern matching or substring problems

## Common Patterns

### Fixed Window Size

```python
def fixed_window_pattern(arr, k):
    window_sum = sum(arr[:k])  # Initial window
    max_sum = window_sum

    for i in range(k, len(arr)):
        # Remove first element of previous window
        # Add last element of current window
        window_sum = window_sum - arr[i-k] + arr[i]
        max_sum = max(max_sum, window_sum)

    return max_sum
```

### Variable Window Size

```python
def variable_window_pattern(arr, target):
    window_sum = 0
    start = 0
    min_length = float('inf')

    for end in range(len(arr)):
        window_sum += arr[end]

        while window_sum >= target:
            min_length = min(min_length, end - start + 1)
            window_sum -= arr[start]
            start += 1

    return min_length if min_length != float('inf') else 0
```

## Common Interview Problems

### 1. Maximum Sum Subarray of Size K

- **Problem**: Find maximum sum of any contiguous subarray of size k
- **Approach**: Fixed-size window, track sum while sliding
- **Time**: O(n)

### 2. Longest Substring with K Distinct Characters

- **Problem**: Find the longest substring with at most k distinct characters
- **Approach**: Variable-size window with hashmap to track character frequency
- **Time**: O(n)

### 3. Minimum Window Substring

- **Problem**: Find minimum window containing all characters of pattern
- **Approach**: Variable-size window with two hashmaps
- **Time**: O(n)

### 4. Maximum Consecutive Ones III

- **Problem**: Find longest sequence of 1s after flipping at most k 0s
- **Approach**: Variable-size window tracking zeros count
- **Time**: O(n)

## Implementation Tips

### Window Structure

1. Initialize window pointers (start, end)
2. Define window constraints
3. Track window state (sum, count, hashmap)
4. Update result based on window state

### Common Edge Cases

- Empty array/string
- Window size larger than array length
- Negative numbers in sum problems
- Case sensitivity in string problems
- Duplicate elements

## Optimization Techniques

### Space Optimization

- Use variables instead of additional arrays when possible
- Clear hashmap entries when frequency becomes zero
- Use bit manipulation for character tracking when applicable

### Time Optimization

- Avoid nested loops
- Use appropriate data structures (hashmap vs array)
- Pre-compute when possible (prefix sums)

## Common Mistakes to Avoid

1. Forgetting to update window state when shrinking
2. Incorrect window size calculations
3. Not handling edge cases
4. Inefficient data structure choices
5. Missing optimization opportunities

## Problem-Solving Framework

1. **Identify Pattern**

   - Is it about contiguous elements?
   - Are we looking for min/max/sum?
   - Is there a size constraint?

2. **Choose Window Type**

   - Fixed size: k is given
   - Variable size: based on conditions

3. **Select Data Structures**

   - Array/string for window
   - Hashmap for frequency
   - Variables for state tracking

4. **Implement Solution**

   - Initialize window
   - Process elements
   - Update state
   - Track result

5. **Optimize**
   - Remove unnecessary operations
   - Improve space usage
   - Handle edge cases
