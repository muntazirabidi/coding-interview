# Common Linked List Patterns Guide

## Table of Contents

1. [Two-Pointer Technique](#two-pointer-technique)
2. [Reverse Linked List Pattern](#reverse-linked-list-pattern)
3. [Merge Lists Pattern](#merge-lists-pattern)
4. [Find Middle Pattern](#find-middle-pattern)
5. [Remove Nth Node Pattern](#remove-nth-node-pattern)
6. [Intersection Point Pattern](#intersection-point-pattern)
7. [Add Numbers Pattern](#add-numbers-pattern)
8. [Common Tips & Edge Cases](#common-tips--edge-cases)

## Two-Pointer Technique

Used for cycle detection, finding middle elements, etc.

### Floyd's Cycle Detection

```python
def hasCycle(head):
    slow = fast = head
    while fast and fast.next:
        slow = slow.next         # Move one step
        fast = fast.next.next    # Move two steps
        if slow == fast:         # Cycle detected
            return True
    return False
```

### Find Cycle Start Point

```python
def detectCycle(head):
    slow = fast = head
    while fast and fast.next:
        slow = slow.next
        fast = fast.next.next
        if slow == fast:
            slow = head
            while slow != fast:
                slow = slow.next
                fast = fast.next
            return slow
    return None
```

## Reverse Linked List Pattern

Used in many problems requiring list manipulation.

### Iterative Approach

```python
def reverse(head):
    prev = None
    curr = head
    while curr:
        next_temp = curr.next    # Store next
        curr.next = prev         # Reverse arrow
        prev = curr             # Move prev
        curr = next_temp        # Move curr
    return prev
```

### Recursive Approach

```python
def reverse(head):
    if not head or not head.next:
        return head
    new_head = reverse(head.next)
    head.next.next = head
    head.next = None
    return new_head
```

## Merge Lists Pattern

Common in problems involving multiple lists.

### Merge Two Sorted Lists

```python
def mergeLists(l1, l2):
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

    curr.next = l1 or l2
    return dummy.next
```

## Find Middle Pattern

Essential for many divide-and-conquer approaches.

```python
def findMiddle(head):
    slow = fast = head
    while fast and fast.next:
        slow = slow.next
        fast = fast.next.next
    return slow
```

## Remove Nth Node Pattern

Useful for removal operations with specific conditions.

```python
def removeNth(head, n):
    dummy = ListNode(0)
    dummy.next = head
    first = second = dummy

    # Advance first pointer by n+1 steps
    for _ in range(n + 1):
        first = first.next

    # Move both pointers until first reaches end
    while first:
        first = first.next
        second = second.next

    # Remove nth node
    second.next = second.next.next
    return dummy.next
```

## Intersection Point Pattern

Finding common nodes between lists.

```python
def getIntersection(headA, headB):
    if not headA or not headB:
        return None

    a = headA
    b = headB

    while a != b:
        a = a.next if a else headB
        b = b.next if b else headA

    return a
```

## Add Numbers Pattern

Used when working with numbers represented as linked lists.

```python
def addTwoNumbers(l1, l2):
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

## Common Tips & Edge Cases

### Essential Operations

```python
# Insert node
new_node.next = curr.next
curr.next = new_node

# Delete node
curr.next = curr.next.next

# Get length
def getLength(head):
    length = 0
    while head:
        length += 1
        head = head.next
    return length
```

### Edge Cases to Consider

1. Empty list (`head = None`)
2. Single node list
3. Two node list
4. Lists with cycles
5. Lists of different lengths
6. Operation at list head
7. Operation at list tail

### Best Practices

1. Always handle null pointer cases first
2. Use dummy nodes when modifying the head
3. Draw out pointer movements for complex operations
4. Test with edge cases
5. Consider using helper functions for common operations

### Common Mistakes to Avoid

1. Forgetting to update pointers
2. Incorrect order of pointer updates
3. Not handling edge cases
4. Memory leaks in languages without garbage collection
5. Not preserving important pointers

### Time/Space Complexity

Most linked list operations should aim for:

- Time Complexity: O(n) or better
- Space Complexity: O(1) for iterative solutions

Remember to analyze both time and space complexity when choosing between recursive and iterative approaches.
