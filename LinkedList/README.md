# Linked List Data Structure

## Table of Contents
- [Introduction](#introduction)
- [Types of Linked Lists](#types-of-linked-lists)
- [Basic Operations](#basic-operations)
- [Common Problems](#common-problems)
- [Implementation](#implementation)
- [Time Complexity](#time-complexity)
- [Interview Tips](#interview-tips)
- [Common Patterns](#common-patterns)

## Introduction
A linked list is a linear data structure where elements are not stored in contiguous memory locations. Each element (node) contains data and a reference (link) to the next node in the sequence.

### Why Linked Lists?
- Dynamic size
- Ease of insertion/deletion
- No memory wastage
- Can grow or shrink during runtime

## Types of Linked Lists

### 1. Singly Linked List
- Each node has data and a pointer to the next node
- Last node points to null
```javascript
class Node {
    constructor(val) {
        this.val = val;
        this.next = null;
    }
}
```

### 2. Doubly Linked List
- Each node has data and pointers to both next and previous nodes
```javascript
class Node {
    constructor(val) {
        this.val = val;
        this.next = null;
        this.prev = null;
    }
}
```

### 3. Circular Linked List
- Last node points back to first node
- Can be singly or doubly linked

## Basic Operations

### 1. Traversal
```javascript
function traverse(head) {
    let current = head;
    while (current !== null) {
        console.log(current.val);
        current = current.next;
    }
}
```

### 2. Insertion
```javascript
// Insert at beginning
function insertHead(head, val) {
    const newNode = new Node(val);
    newNode.next = head;
    return newNode;
}

// Insert at end
function insertTail(head, val) {
    if (!head) return new Node(val);
    
    let current = head;
    while (current.next !== null) {
        current = current.next;
    }
    current.next = new Node(val);
    return head;
}
```

### 3. Deletion
```javascript
// Delete first occurrence of value
function deleteValue(head, val) {
    if (!head) return null;
    if (head.val === val) return head.next;
    
    let current = head;
    while (current.next !== null) {
        if (current.next.val === val) {
            current.next = current.next.next;
            break;
        }
        current = current.next;
    }
    return head;
}
```

## Common Problems

### 1. Reverse a Linked List
```javascript
function reverse(head) {
    let prev = null;
    let current = head;
    
    while (current !== null) {
        const next = current.next;
        current.next = prev;
        prev = current;
        current = next;
    }
    
    return prev;
}
```

### 2. Find Middle Node
```javascript
function findMiddle(head) {
    let slow = head;
    let fast = head;
    
    while (fast !== null && fast.next !== null) {
        slow = slow.next;
        fast = fast.next.next;
    }
    
    return slow;
}
```

### 3. Detect Cycle
```javascript
function hasCycle(head) {
    let slow = head;
    let fast = head;
    
    while (fast !== null && fast.next !== null) {
        slow = slow.next;
        fast = fast.next.next;
        if (slow === fast) return true;
    }
    
    return false;
}
```

## Time Complexity

| Operation | Time Complexity |
|-----------|----------------|
| Access    | O(n)           |
| Search    | O(n)           |
| Insertion | O(1)*          |
| Deletion  | O(1)*          |

\* When position is known, otherwise O(n) to find position

## Interview Tips

1. **Edge Cases**
   - Empty list
   - Single node
   - Two nodes
   - Many nodes
   - Cycles (if applicable)

2. **Common Techniques**
   - Two-pointer technique (slow/fast)
   - Dummy head node
   - Hash table for O(1) lookups
   - Recursion for elegant solutions

3. **Remember**
   - Always check for null pointers
   - Update pointers carefully
   - Consider both previous and next nodes
   - Draw the list and manipulations

## Common Patterns

### 1. Fast & Slow Pointers
Used for:
- Finding middle element
- Detecting cycles
- Finding cycle start
- Finding kth element from end

### 2. Dummy Head
Used for:
- Simplifying insertion at head
- Merging lists
- Removing elements

### 3. Multiple Passes
Used for:
- Finding length
- Reversing
- Reordering

## Best Practices

1. **Always Test For**:
   - Null input
   - Single element
   - Even vs odd length
   - Cycle presence

2. **Implementation Tips**:
   - Use meaningful variable names
   - Comment complex pointer manipulations
   - Draw pointer changes before coding
   - Test with small examples first

3. **Optimization**:
   - Space complexity: Can you solve in O(1)?
   - Time complexity: Is one pass possible?
   - Code clarity: Is it readable and maintainable?

## Debugging Tips

1. **Common Issues**:
   - Lost pointers
   - Infinite loops
   - Not handling null
   - Off-by-one errors

2. **Verification**:
   - Print list after each operation
   - Check next pointers
   - Verify list length
   - Test boundary conditions

## Resources

1. **Practice Problems**:
   - LeetCode Linked List section
   - HackerRank Data Structures
   - GeeksforGeeks Linked Lists

2. **Visual Learning**:
   - [Visualgo - Linked List Visualization](https://visualgo.net/en/list)
   - [CS50 Linked List Visualization](https://www.youtube.com/watch?v=5nsKtQuT6E8)

## Contributing
Feel free to submit pull requests to improve this guide. Please include:
- Clear explanation of changes
- Updated code examples if applicable
- Any additional helpful diagrams or explanations
