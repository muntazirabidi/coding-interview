# Linked List - Complete Python Guide

## Table of Contents
- [Basic Concepts](#basic-concepts)
- [Implementation](#implementation)
- [Common Operations](#common-operations)
- [Common Patterns](#common-patterns)
- [Interview Problems](#interview-problems)
- [Best Practices](#best-practices)

## Basic Concepts

### Node Structure
```python
class ListNode:
    def __init__(self, val=0, next=None):
        self.val = val
        self.next = next
```

### Types of Linked Lists
1. Singly Linked List: Each node points to next node
2. Doubly Linked List: Each node points to both next and previous nodes
3. Circular Linked List: Last node points back to first node

## Implementation

### 1. Singly Linked List
```python
class SinglyLinkedList:
    def __init__(self):
        self.head = None
        self.size = 0
    
    def insert_at_beginning(self, val):
        new_node = ListNode(val)
        new_node.next = self.head
        self.head = new_node
        self.size += 1
    
    def insert_at_end(self, val):
        new_node = ListNode(val)
        if not self.head:
            self.head = new_node
            self.size += 1
            return
        
        curr = self.head
        while curr.next:
            curr = curr.next
        curr.next = new_node
        self.size += 1
    
    def delete_at_beginning(self):
        if not self.head:
            return None
        
        val = self.head.val
        self.head = self.head.next
        self.size -= 1
        return val
    
    def delete_at_end(self):
        if not self.head:
            return None
        
        if not self.head.next:
            val = self.head.val
            self.head = None
            self.size -= 1
            return val
        
        curr = self.head
        while curr.next.next:
            curr = curr.next
        
        val = curr.next.val
        curr.next = None
        self.size -= 1
        return val
    
    def print_list(self):
        curr = self.head
        while curr:
            print(curr.val, end=" -> ")
            curr = curr.next
        print("None")
```

### 2. Doubly Linked List
```python
class DoublyNode:
    def __init__(self, val=0, next=None, prev=None):
        self.val = val
        self.next = next
        self.prev = prev

class DoublyLinkedList:
    def __init__(self):
        self.head = None
        self.tail = None
        self.size = 0
    
    def insert_at_beginning(self, val):
        new_node = DoublyNode(val)
        if not self.head:
            self.head = self.tail = new_node
        else:
            new_node.next = self.head
            self.head.prev = new_node
            self.head = new_node
        self.size += 1
    
    def insert_at_end(self, val):
        new_node = DoublyNode(val)
        if not self.tail:
            self.head = self.tail = new_node
        else:
            new_node.prev = self.tail
            self.tail.next = new_node
            self.tail = new_node
        self.size += 1
    
    def delete_at_beginning(self):
        if not self.head:
            return None
        
        val = self.head.val
        self.head = self.head.next
        if self.head:
            self.head.prev = None
        else:
            self.tail = None
        self.size -= 1
        return val
    
    def delete_at_end(self):
        if not self.tail:
            return None
        
        val = self.tail.val
        self.tail = self.tail.prev
        if self.tail:
            self.tail.next = None
        else:
            self.head = None
        self.size -= 1
        return val
```

## Common Operations

### 1. Find Middle of Linked List
```python
def find_middle(head):
    if not head or not head.next:
        return head
    
    slow = fast = head
    while fast and fast.next:
        slow = slow.next
        fast = fast.next.next
    
    return slow
```

### 2. Reverse Linked List
```python
def reverse_iterative(head):
    prev = None
    curr = head
    
    while curr:
        next_temp = curr.next
        curr.next = prev
        prev = curr
        curr = next_temp
    
    return prev

def reverse_recursive(head):
    if not head or not head.next:
        return head
    
    new_head = reverse_recursive(head.next)
    head.next.next = head
    head.next = None
    
    return new_head
```

### 3. Detect Cycle
```python
def has_cycle(head):
    if not head or not head.next:
        return False
    
    slow = fast = head
    while fast and fast.next:
        slow = slow.next
        fast = fast.next.next
        if slow == fast:
            return True
    
    return False
```

## Common Patterns

### 1. Fast and Slow Pointers
```python
def find_cycle_start(head):
    if not head or not head.next:
        return None
    
    # Find meeting point
    slow = fast = head
    while fast and fast.next:
        slow = slow.next
        fast = fast.next.next
        if slow == fast:
            break
    else:
        return None
    
    # Find cycle start
    slow = head
    while slow != fast:
        slow = slow.next
        fast = fast.next
    
    return slow
```

### 2. Multiple Pointers
```python
def remove_nth_from_end(head, n):
    dummy = ListNode(0)
    dummy.next = head
    first = dummy
    second = dummy
    
    # Advance first pointer by n+1 steps
    for _ in range(n + 1):
        first = first.next
    
    # Move both pointers until first reaches end
    while first:
        first = first.next
        second = second.next
    
    second.next = second.next.next
    return dummy.next
```

## Interview Problems

### 1. Merge Two Sorted Lists
```python
def merge_sorted_lists(l1, l2):
    dummy = ListNode(0)
    curr = dummy
    
    while l1 and l2:
        if l1.val <= l2.val:
            curr.next = l1
            l1 = l1.next
        else:
            curr.next = l2
            l2 = l2.next
        curr = curr.next
    
    curr.next = l1 if l1 else l2
    return dummy.next
```

### 2. Add Two Numbers
```python
def add_two_numbers(l1, l2):
    dummy = ListNode(0)
    curr = dummy
    carry = 0
    
    while l1 or l2 or carry:
        val1 = l1.val if l1 else 0
        val2 = l2.val if l2 else 0
        
        total = val1 + val2 + carry
        carry = total // 10
        curr.next = ListNode(total % 10)
        
        curr = curr.next
        l1 = l1.next if l1 else None
        l2 = l2.next if l2 else None
    
    return dummy.next
```

### 3. Intersection of Two Lists
```python
def get_intersection_node(headA, headB):
    if not headA or not headB:
        return None
    
    ptrA = headA
    ptrB = headB
    
    while ptrA != ptrB:
        ptrA = ptrA.next if ptrA else headB
        ptrB = ptrB.next if ptrB else headA
    
    return ptrA
```

## Best Practices

### Time Complexity Analysis
Operation | Time Complexity | Space Complexity
----------|----------------|------------------
Insert at beginning | O(1) | O(1)
Insert at end | O(n) | O(1)
Delete at beginning | O(1) | O(1)
Delete at end | O(n) | O(1)
Search | O(n) | O(1)
Access | O(n) | O(1)

### Tips for Interviews
1. Always check for null/empty lists
2. Handle edge cases:
   - Empty list
   - Single node
   - Two nodes
   - Circular lists
   
3. Common techniques:
   - Use dummy nodes for simplification
   - Fast/slow pointers for cycle detection
   - Multiple pointers for distance-based problems
   - Stack for palindrome verification

4. Optimization strategies:
   - Consider in-place solutions
   - Use two-pointer technique when applicable
   - Leverage dummy nodes for cleaner code
   - Think about space-time tradeoffs

5. Problem-solving steps:
   - Draw the list and visualize changes
   - Start with brute force approach
   - Look for optimization opportunities
   - Test with example cases
   - Verify edge cases

Remember:
- Keep track of null pointers
- Consider using dummy nodes
- Watch for cycles
- Think about maintaining references
- Consider both iterative and recursive solutions
