# Stack Data Structure - Complete Guide

## Table of Contents
- [Introduction](#introduction)
- [Implementation](#implementation)
- [Core Operations](#core-operations)
- [Common Applications](#common-applications)
- [Interview Problems](#interview-problems)
- [Time Complexity](#time-complexity)
- [Best Practices & Tips](#best-practices--tips)

## Introduction

A stack is a linear data structure that follows the Last-In-First-Out (LIFO) principle. Think of it like a stack of plates - you can only add or remove plates from the top.

### Key Characteristics:
- Elements are added to the top (push)
- Elements are removed from the top (pop)
- Only the top element is accessible at any time
- Perfect for tracking state that needs to be unwound

## Implementation

### Basic Stack Implementation using List

```python
class Stack:
    def __init__(self):
        self.items = []
    
    def push(self, item):
        self.items.append(item)
    
    def pop(self):
        if not self.is_empty():
            return self.items.pop()
        raise IndexError("Pop from empty stack")
    
    def peek(self):
        if not self.is_empty():
            return self.items[-1]
        raise IndexError("Peek at empty stack")
    
    def is_empty(self):
        return len(self.items) == 0
    
    def size(self):
        return len(self.items)
```

### Stack Implementation using Linked List (More Memory Efficient)

```python
class Node:
    def __init__(self, value):
        self.value = value
        self.next = None

class LinkedStack:
    def __init__(self):
        self.head = None
        self._size = 0
    
    def push(self, value):
        new_node = Node(value)
        new_node.next = self.head
        self.head = new_node
        self._size += 1
    
    def pop(self):
        if self.is_empty():
            raise IndexError("Pop from empty stack")
        value = self.head.value
        self.head = self.head.next
        self._size -= 1
        return value
    
    def peek(self):
        if self.is_empty():
            raise IndexError("Peek at empty stack")
        return self.head.value
    
    def is_empty(self):
        return self.head is None
    
    def size(self):
        return self._size
```

## Core Operations

1. **push(item)**: Add an element to the top
   ```python
   stack.push(5)  # stack: [5]
   stack.push(10) # stack: [5, 10]
   ```

2. **pop()**: Remove and return the top element
   ```python
   value = stack.pop() # Returns 10, stack: [5]
   ```

3. **peek()**: View the top element without removing it
   ```python
   top = stack.peek() # Returns 5, stack unchanged
   ```

4. **is_empty()**: Check if stack is empty
   ```python
   empty = stack.is_empty() # Returns False
   ```

## Common Applications

### 1. Parentheses Matching
```python
def is_valid_parentheses(s: str) -> bool:
    stack = []
    pairs = {')': '(', '}': '{', ']': '['}
    
    for char in s:
        if char in '({[':
            stack.append(char)
        elif char in ')}]':
            if not stack or stack.pop() != pairs[char]:
                return False
    
    return len(stack) == 0

# Example usage:
print(is_valid_parentheses("(){}[]"))  # True
print(is_valid_parentheses("({)}"))    # False
```

### 2. Expression Evaluation
```python
def evaluate_postfix(expression: str) -> int:
    stack = []
    operators = {'+', '-', '*', '/'}
    
    for token in expression.split():
        if token in operators:
            b = stack.pop()
            a = stack.pop()
            if token == '+': stack.append(a + b)
            elif token == '-': stack.append(a - b)
            elif token == '*': stack.append(a * b)
            elif token == '/': stack.append(a // b)
        else:
            stack.append(int(token))
    
    return stack.pop()

# Example usage:
print(evaluate_postfix("5 3 + 2 *"))  # Output: 16
```

### 3. Undo Operation
```python
class TextEditor:
    def __init__(self):
        self.text = ""
        self.undo_stack = []
    
    def add_text(self, text):
        self.undo_stack.append(self.text)
        self.text += text
    
    def delete_last(self):
        if self.text:
            self.undo_stack.append(self.text)
            self.text = self.text[:-1]
    
    def undo(self):
        if self.undo_stack:
            self.text = self.undo_stack.pop()
```

## Interview Problems

### 1. Min Stack
Design a stack that supports push, pop, top, and retrieving the minimum element in constant time.

```python
class MinStack:
    def __init__(self):
        self.stack = []
        self.min_stack = []
    
    def push(self, val: int) -> None:
        self.stack.append(val)
        if not self.min_stack or val <= self.min_stack[-1]:
            self.min_stack.append(val)
    
    def pop(self) -> None:
        if self.stack:
            if self.stack.pop() == self.min_stack[-1]:
                self.min_stack.pop()
    
    def top(self) -> int:
        return self.stack[-1] if self.stack else None
    
    def getMin(self) -> int:
        return self.min_stack[-1] if self.min_stack else None
```

### 2. Next Greater Element
Find the next greater element for each element in an array.

```python
def next_greater_element(arr):
    n = len(arr)
    result = [-1] * n
    stack = []
    
    for i in range(n-1, -1, -1):
        while stack and stack[-1] <= arr[i]:
            stack.pop()
        
        if stack:
            result[i] = stack[-1]
        
        stack.append(arr[i])
    
    return result

# Example usage:
print(next_greater_element([4, 5, 2, 10]))  # [5, 10, 10, -1]
```

## Time Complexity

Operation | Array-based | Linked List-based
----------|------------|------------------
Push      | O(1)*      | O(1)
Pop       | O(1)       | O(1)
Peek      | O(1)       | O(1)
IsEmpty   | O(1)       | O(1)
Size      | O(1)       | O(1)

* Note: Array-based implementation might need O(n) for resizing, but this is amortized to O(1)

## Best Practices & Tips

### 1. Implementation Choices
- Use array-based implementation when:
  - Maximum size is known
  - Memory is not a constraint
  - Need cache-friendly operations
- Use linked list-based implementation when:
  - Size is unknown
  - Memory efficiency is important
  - Frequent push/pop operations

### 2. Common Pitfalls
- Not handling empty stack cases
- Not considering stack overflow
- Forgetting to update size counter
- Not cleaning up references in pop operations

### 3. Interview Tips
1. Always clarify:
   - Expected behavior for edge cases
   - Whether there are size constraints
   - If optimization is needed for space/time

2. Think about:
   - Can the problem be solved by tracking "last seen" elements?
   - Is there a need to maintain additional state?
   - Would multiple stacks help?

3. Common Stack Patterns:
   - Matching pairs (parentheses, tags)
   - Tracking maxima/minima
   - Monotonic sequences
   - Backtracking
   - Undo operations

### 4. Memory Management
```python
def clean_pop(self):
    if self.is_empty():
        raise IndexError("Pop from empty stack")
    value = self.items[-1]
    self.items[-1] = None  # Clean reference
    self.items.pop()
    return value
```

### 5. Testing Your Implementation
```python
def test_stack():
    stack = Stack()
    
    # Test empty stack
    assert stack.is_empty() == True
    
    # Test push
    stack.push(1)
    assert stack.peek() == 1
    
    # Test multiple operations
    stack.push(2)
    stack.push(3)
    assert stack.pop() == 3
    assert stack.peek() == 2
    assert stack.size() == 2
```

Remember:
- Stack operations should be O(1)
- Always handle edge cases
- Consider memory implications
- Think about thread safety if relevant
- Keep track of size explicitly if needed
