# 5-Step Approach to Solving DP Problems

## Introduction
Dynamic Programming (DP) is a powerful algorithmic technique that solves complex problems by breaking them down into simpler subproblems. The solution to the larger problem is constructed by combining solutions to these subproblems in a systematic way.

### 1. Visualization
- Create visual representations of the problem
- Use diagrams to identify patterns
- Common visualization technique: Directed Acyclic Graphs (DAG)
  - Nodes represent states/values
  - Edges represent valid transitions/relationships
  - Paths in the graph often represent solutions

### 2. Identify Subproblems
- Find smaller, simpler versions of the main problem
- Common subproblem patterns:
  1. Sequence of length n → subproblems with length i
  2. Sorted sequence → i-length subsequences
  3. Two sequences → subsequences of each
  4. Middle-out expansion → grow from center
  5. 2D array → smaller sub-matrices

### 3. Find Relationships Among Subproblems
- Determine how subproblems connect to each other
- Ask: "What subproblems do I need to solve the current one?"
- Establish clear mathematical relationships
- Look for patterns in how solutions build up

### 4. Generalize the Relationship
- Create a formula/rule that works for any instance
- Express the solution to a problem in terms of its subproblems
- Consider edge cases and base conditions

### 5. Implementation
- Solve subproblems in the correct order
- Ensure prerequisites are solved before dependent problems
- Use appropriate data structures (arrays, hash maps)
- Consider optimization techniques (memoization/tabulation)

## Case Study 1: Longest Increasing Subsequence (LIS)

### Problem Definition
- Given: Sequence of n elements
- Goal: Find length of longest increasing subsequence
- Constraint: Each element must be larger than previous elements

### Example
```
Input: [1, 2, 4, 3]
LIS: [1, 2, 4]
Length: 3
```

### Solution Approach
1. **Visualization**
   - Create DAG where edges connect smaller to larger values
   - Each path represents a valid increasing subsequence

2. **Subproblem**
   - LIS[k] = Length of longest increasing subsequence ending at index k

3. **Relationship**
   - LIS[n] = 1 + max(LIS[k]) for all k < n where value[k] < value[n]

4. **Implementation**
```python
def longest_increasing_subsequence(arr):
    if not arr:
        return 0
        
    # Initialize LIS array with 1 (minimum length)
    lengths = [1] * len(arr)
    
    # Compute LIS values for all indexes
    for i in range(1, len(arr)):
        for j in range(i):
            if arr[i] > arr[j]:
                lengths[i] = max(lengths[i], lengths[j] + 1)
    
    # Return maximum value in lengths array
    return max(lengths)
```

## Case Study 2: Box Stacking Problem

### Problem Definition
- Given: n boxes with length, width, height
- Goal: Find height of tallest possible stack
- Constraints: 
  - Box can only be stacked if length and width are smaller than box below
  - No rotation allowed

### Solution Approach
1. **Visualization**
   - Create DAG where edges represent valid stacking relationships
   - Each path represents a possible stack

2. **Subproblem**
   - MaxHeight[box] = Maximum height of stack with 'box' as the base

3. **Relationship**
   - MaxHeight[current] = height[current] + max(MaxHeight[box]) for all boxes that can be stacked on current

4. **Implementation**
```python
class Box:
    def __init__(self, length, width, height):
        self.length = length
        self.width = width
        self.height = height

def max_stack_height(boxes):
    # Sort boxes by base area (length * width) in descending order
    boxes.sort(key=lambda x: x.length * x.width, reverse=True)
    
    # Initialize maximum heights with box heights
    max_heights = [box.height for box in boxes]
    
    # Compute maximum heights for each box as base
    for i in range(1, len(boxes)):
        for j in range(0, i):
            if can_be_stacked(boxes[i], boxes[j]):
                max_heights[i] = max(max_heights[i], 
                                   max_heights[j] + boxes[i].height)
    
    return max(max_heights)

def can_be_stacked(top, bottom):
    return (top.length < bottom.length and 
            top.width < bottom.width)
```

## Common DP Patterns and Tips

### Subproblem Patterns
1. **Linear Sequence**
   - Input: Array/string of length n
   - Subproblem: Consider first/last i elements

2. **Two-Dimensional Grid**
   - Input: Matrix or 2D array
   - Subproblem: Sub-matrix or region

3. **String Transformations**
   - Input: One or more strings
   - Subproblem: Prefixes or suffixes

4. **Optimization Problems**
   - Input: Set of choices with values
   - Subproblem: Optimal solution for subset

### Implementation Tips
1. **Memoization Technique**
   ```python
   def solve_with_memo(params, memo=None):
       if memo is None:
           memo = {}
       
       # Check if already solved
       if key in memo:
           return memo[key]
           
       # Base cases
       
       # Recursive cases with memoization
       memo[key] = calculated_value
       return memo[key]
   ```

2. **Tabulation Technique**
   ```python
   def solve_with_table(params):
       # Initialize table
       dp = [initial_values]
       
       # Fill table iteratively
       for i in range(appropriate_range):
           dp[i] = calculate_from_previous(dp)
           
       return dp[final_index]
   ```

### Common Mistakes to Avoid
1. Not identifying overlapping subproblems
2. Incorrect subproblem definition
3. Missing base cases
4. Wrong order of solving subproblems
5. Not considering all dependencies

## Problem-Solving Checklist
1. [ ] Can I visualize the problem?
2. [ ] What are the smallest subproblems?
3. [ ] How do subproblems relate to each other?
4. [ ] What's the recurrence relation?
5. [ ] What's the optimal order to solve subproblems?
6. [ ] Have I handled all edge cases?

## Practice Strategy
1. Start with simple problems
2. Draw out examples and solutions
3. Focus on subproblem identification
4. Practice both memoization and tabulation
5. Analyze time and space complexity
6. Review and optimize solutions

Remember: The key to mastering dynamic programming is practice and pattern recognition. Start with simpler problems and gradually work your way up to more complex ones.
