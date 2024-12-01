# Data Structures for Statistical Calculations
A comprehensive guide to choosing the right data structures for different statistical operations, with a focus on one-time versus streaming calculations.

## Table of Contents
1. [Understanding the Problem Types](#understanding-the-problem-types)
2. [Calculating Median](#calculating-median)
3. [Other Statistical Measures](#other-statistical-measures)
4. [Best Practices and Decision Guide](#best-practices-and-decision-guide)
5. [Code Examples](#code-examples)

## Understanding the Problem Types

When dealing with statistical calculations, we encounter two main scenarios:

1. **One-time Calculations**: Computing statistics for a fixed set of numbers
   - Data is available all at once
   - No future updates needed
   - Efficiency of memory usage is prioritized over update speed

2. **Streaming Calculations**: Computing statistics as numbers arrive continuously
   - Data arrives one piece at a time
   - Need to maintain running statistics
   - Update speed is prioritized over memory usage

## Calculating Median

### Heap-based Approach (for Streaming)
The heap approach uses two heaps to maintain numbers in a way that allows quick median calculation:

```python
class RollingMedianCalculator:
    def __init__(self):
        self.max_heap = []  # Lower half of numbers
        self.min_heap = []  # Upper half of numbers
    
    def add_number(self, num):
        # Add to heaps and balance them
        heapq.heappush(self.max_heap, -num)
        # Balance heaps...
        return self.get_median()
```

Key characteristics:
- Time Complexity: O(log n) per insertion
- Space Complexity: O(n)
- Perfect for streaming data
- Maintains running median efficiently

### Sorted Array Approach (for One-time)
```python
def calculate_median(numbers):
    sorted_nums = sorted(numbers)
    n = len(sorted_nums)
    mid = n // 2
    return sorted_nums[mid] if n % 2 else (sorted_nums[mid-1] + sorted_nums[mid]) / 2
```

Key characteristics:
- Time Complexity: O(n log n) for sorting
- Space Complexity: O(n)
- Better for one-time calculations
- Simpler to implement

## Other Statistical Measures

### Mean (Average)
For streaming data:
```python
class RunningMean:
    def __init__(self):
        self.total = 0
        self.count = 0
    
    def add_number(self, num):
        self.total += num
        self.count += 1
        return self.total / self.count
```

For one-time calculation:
```python
mean = sum(numbers) / len(numbers)
```

### Mode (Most Frequent Value)
For streaming data:
```python
class RunningMode:
    def __init__(self):
        self.frequency = {}
        self.max_freq = 0
        self.mode = None
    
    def add_number(self, num):
        self.frequency[num] = self.frequency.get(num, 0) + 1
        if self.frequency[num] > self.max_freq:
            self.max_freq = self.frequency[num]
            self.mode = num
        return self.mode
```

For one-time calculation:
```python
from collections import Counter
mode = Counter(numbers).most_common(1)[0][0]
```

### Standard Deviation
For streaming data:
```python
class RunningStdDev:
    def __init__(self):
        self.count = 0
        self.sum = 0
        self.sum_squares = 0
    
    def add_number(self, num):
        self.count += 1
        self.sum += num
        self.sum_squares += num * num
        variance = (self.sum_squares / self.count) - (self.sum / self.count) ** 2
        return variance ** 0.5
```

## Best Practices and Decision Guide

When choosing a data structure for statistical calculations, consider:

1. **Data Access Pattern**
   - Streaming data → Use specialized running calculators
   - One-time calculation → Use simple sorted arrays or built-in functions

2. **Space-Time Tradeoffs**
   - Need fast updates → Use running calculators (more memory)
   - Need minimal memory → Use sorted arrays (slower updates)

3. **Operation Frequency**
   - Frequent updates → Running calculators
   - Rare updates → Simple calculations on demand

## Code Examples

Here's a comprehensive class that handles multiple statistics:

```python
class StatisticsCalculator:
    def __init__(self):
        self.count = 0
        self.total = 0
        self.median_calc = RollingMedianCalculator()
        self.frequency = {}
        self.sum_squares = 0
    
    def add_number(self, num):
        # Update basic counts
        self.count += 1
        self.total += num
        
        # Update median
        current_median = self.median_calc.add_number(num)
        
        # Update mode tracking
        self.frequency[num] = self.frequency.get(num, 0) + 1
        
        # Update standard deviation tracking
        self.sum_squares += num * num
        
        # Return current statistics
        return {
            'mean': self.total / self.count,
            'median': current_median,
            'mode': max(self.frequency.items(), key=lambda x: x[1])[0],
            'std_dev': ((self.sum_squares / self.count) - 
                       (self.total / self.count) ** 2) ** 0.5
        }
```

## Conclusion

The choice of data structure significantly impacts the efficiency of statistical calculations. For streaming data, specialized data structures like heaps and running calculators offer optimal performance. For one-time calculations, simpler approaches using sorted arrays or built-in functions are often more appropriate.

Remember that the best choice depends on your specific use case, considering factors like:
- Whether data is streaming or static
- Update frequency requirements
- Memory constraints
- Performance requirements

This guide serves as a reference for choosing the right approach for your statistical computation needs.
