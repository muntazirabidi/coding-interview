# Memoization in Dynamic Programming (Python Implementation)

## Introduction
Memoization is an optimization technique that speeds up programs by storing the results of expensive function calls and returning the cached result when the same inputs occur again. In Python, we can implement memoization using dictionaries.

## Core Concepts
1. Cache results in a dictionary
2. Check cache before computation
3. Store results after computation
4. Uses recursion with optimization

## Basic Example: Fibonacci Sequence

### Without Memoization
```python
def fib(n):
    if n <= 2:
        return 1
    return fib(n - 1) + fib(n - 2)
```
Time Complexity: O(2^n)
Space Complexity: O(n)

### With Memoization
```python
def fib(n, memo=None):
    if memo is None:
        memo = {}
    
    # check if in memo
    if n in memo:
        return memo[n]
    
    # base cases
    if n <= 2:
        return 1
    
    # store result in memo
    memo[n] = fib(n - 1, memo) + fib(n - 2, memo)
    return memo[n]

# Example usage:
print(fib(6))   # 8
print(fib(50))  # 12586269025

# Using Python's built-in memoization decorator
from functools import lru_cache

@lru_cache(maxsize=None)
def fib_cached(n):
    if n <= 2:
        return 1
    return fib_cached(n - 1) + fib_cached(n - 2)
```

## Grid Traveler Problem
**Problem**: Given a grid of m×n dimensions, find the number of ways to travel from top-left to bottom-right if you can only move right or down.

```python
def grid_traveler(m, n, memo=None):
    if memo is None:
        memo = {}
    
    # create a key for memo
    key = f"{m},{n}"
    
    # check if in memo
    if key in memo:
        return memo[key]
    
    # base cases
    if m == 1 and n == 1:
        return 1
    if m == 0 or n == 0:
        return 0
    
    # store result in memo
    memo[key] = grid_traveler(m - 1, n, memo) + grid_traveler(m, n - 1, memo)
    return memo[key]

# Example usage:
print(grid_traveler(2, 3))    # 3
print(grid_traveler(18, 18))  # 2333606220
```

## Sum Problems

### 1. canSum - Decision Problem
**Problem**: Given a target sum and a list of numbers, return boolean indicating if it's possible to generate target sum using numbers from the list.

```python
def can_sum(target_sum, numbers, memo=None):
    if memo is None:
        memo = {}
    
    if target_sum in memo:
        return memo[target_sum]
    
    if target_sum == 0:
        return True
    if target_sum < 0:
        return False
    
    for num in numbers:
        remainder = target_sum - num
        if can_sum(remainder, numbers, memo):
            memo[target_sum] = True
            return True
    
    memo[target_sum] = False
    return False

# Example usage:
print(can_sum(7, [2, 3]))         # True
print(can_sum(7, [5, 3, 4, 7]))   # True
print(can_sum(7, [2, 4]))         # False
```

### 2. howSum - Combinatoric Problem
**Problem**: Return a list containing any combination of numbers that add up to exactly the targetSum.

```python
def how_sum(target_sum, numbers, memo=None):
    if memo is None:
        memo = {}
    
    if target_sum in memo:
        return memo[target_sum]
    
    if target_sum == 0:
        return []
    if target_sum < 0:
        return None
    
    for num in numbers:
        remainder = target_sum - num
        remainder_result = how_sum(remainder, numbers, memo)
        if remainder_result is not None:
            memo[target_sum] = remainder_result + [num]
            return memo[target_sum]
    
    memo[target_sum] = None
    return None

# Example usage:
print(how_sum(7, [2, 3]))         # [3, 2, 2]
print(how_sum(7, [5, 3, 4, 7]))   # [4, 3]
print(how_sum(7, [2, 4]))         # None
```

### 3. bestSum - Optimization Problem
**Problem**: Return a list containing the shortest combination of numbers that add up to exactly the targetSum.

```python
def best_sum(target_sum, numbers, memo=None):
    if memo is None:
        memo = {}
    
    if target_sum in memo:
        return memo[target_sum]
    
    if target_sum == 0:
        return []
    if target_sum < 0:
        return None
    
    shortest_combination = None
    
    for num in numbers:
        remainder = target_sum - num
        remainder_combination = best_sum(remainder, numbers, memo)
        if remainder_combination is not None:
            combination = remainder_combination + [num]
            if shortest_combination is None or len(combination) < len(shortest_combination):
                shortest_combination = combination
    
    memo[target_sum] = shortest_combination
    return shortest_combination

# Example usage:
print(best_sum(7, [5, 3, 4, 7]))  # [7]
print(best_sum(8, [2, 3, 5]))     # [3, 5]
print(best_sum(8, [1, 4, 5]))     # [4, 4]
```

## String Construction Problems

### 1. canConstruct
**Problem**: Return boolean indicating if target can be constructed by concatenating elements of word_bank.

```python
def can_construct(target, word_bank, memo=None):
    if memo is None:
        memo = {}
    
    if target in memo:
        return memo[target]
    
    if target == '':
        return True
    
    for word in word_bank:
        if target.startswith(word):
            suffix = target[len(word):]
            if can_construct(suffix, word_bank, memo):
                memo[target] = True
                return True
    
    memo[target] = False
    return False

# Example usage:
print(can_construct("abcdef", ["ab", "abc", "cd", "def", "abcd"]))  # True
print(can_construct("skateboard", ["bo", "rd", "ate", "t", "ska", "sk", "boar"]))  # False
```

## Python-Specific Memoization Techniques

### 1. Using functools.lru_cache
```python
from functools import lru_cache

@lru_cache(maxsize=None)
def fibonacci(n):
    if n <= 2:
        return 1
    return fibonacci(n-1) + fibonacci(n-2)
```

### 2. Creating a Memoization Decorator
```python
def memoize(func):
    cache = {}
    def memoized(*args):
        if args not in cache:
            cache[args] = func(*args)
        return cache[args]
    return memoized

@memoize
def fibonacci(n):
    if n <= 2:
        return 1
    return fibonacci(n-1) + fibonacci(n-2)
```

## Debugging Memoized Solutions in Python

```python
def debug_fib(n, memo=None, depth=0):
    if memo is None:
        memo = {}
    
    indent = "  " * depth
    print(f"{indent}Calculate fib({n})")
    print(f"{indent}Current memo:", memo)
    
    if n in memo:
        print(f"{indent}Found in memo: fib({n}) = {memo[n]}")
        return memo[n]
    
    if n <= 2:
        return 1
    
    memo[n] = debug_fib(n - 1, memo, depth + 1) + debug_fib(n - 2, memo, depth + 1)
    print(f"{indent}Stored in memo: fib({n}) = {memo[n]}")
    return memo[n]
```

## Python-Specific Tips

1. **Use None as Default Mutable Parameter**
```python
# Wrong
def recursive_func(n, memo={}):  # Mutable default parameter!
    pass

# Right
def recursive_func(n, memo=None):
    if memo is None:
        memo = {}
```

2. **Tuple Keys for Multiple Parameters**
```python
def memoized_func(x, y, memo=None):
    if memo is None:
        memo = {}
    
    key = (x, y)  # Tuples are immutable and hashable
    if key in memo:
        return memo[key]
```

3. **Using dataclasses for Complex Memoization**
```python
from dataclasses import dataclass
from typing import Dict, Any

@dataclass(frozen=True)
class MemoKey:
    param1: Any
    param2: Any

def complex_memoized_func(param1, param2, memo=None):
    if memo is None:
        memo = {}
    
    key = MemoKey(param1, param2)
    if key in memo:
        return memo[key]
```

Remember: Python's built-in memoization tools like `@lru_cache` are often the best choice for simple cases, but custom memoization is necessary when you need more control over the caching behavior or need to cache mutable data structures.
