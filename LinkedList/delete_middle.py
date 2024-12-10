'''
You are given the head of a linked list. Delete the middle node, and return the head of the modified linked list.

The middle node of a linked list of size n is the ⌊n / 2⌋th node from the start using 0-based indexing, where ⌊x⌋ denotes the largest integer less than or equal to x.

For n = 1, 2, 3, 4, and 5, the middle nodes are 0, 1, 1, 2, and 2, respectively.
'''

from typing import Optional

# Definition for singly-linked list.
class ListNode:
    def __init__(self, val=0, next=None):
        self.val = val
        self.next = next

class Solution:
    def deleteMiddle(self, head: Optional[ListNode]) -> Optional[ListNode]:
        # Edge case: if list is empty or has only one node
        if not head or not head.next:
            return None
            
        # Use two pointers: slow and fast
        # prev will keep track of node before slow
        slow = fast = head
        prev = None
        
        while fast and fast.next:
            fast = fast.next.next
            prev = slow
            slow = slow.next
        
        # Now slow is at the middle node
        prev.next = slow.next
        
        return head

def createLinkedList(arr):
    if not arr:
        return None
    head = ListNode(arr[0])
    current = head
    for val in arr[1:]:
        current.next = ListNode(val)
        current = current.next
    return head

# Helper function to convert linked list to array (for testing)
def linkedListToArray(head):
    result = []
    current = head
    while current:
        result.append(current.val)
        current = current.next
    return result

# Test cases
def test_solution():
    solution = Solution()
    
    # Test case 1: [1,3,4,7,1,2,6]
    test1 = createLinkedList([1,3,4,7,1,2,6])
    result1 = solution.deleteMiddle(test1)
    assert linkedListToArray(result1) == [1,3,4,1,2,6]
    
    # Test case 2: [1,2,3,4]
    test2 = createLinkedList([1,2,3,4])
    result2 = solution.deleteMiddle(test2)
    assert linkedListToArray(result2) == [1,2,4]
    
    # Test case 3: [2,1]
    test3 = createLinkedList([2,1])
    result3 = solution.deleteMiddle(test3)
    assert linkedListToArray(result3) == [2]
    
    # Test case 4: [1]
    test4 = createLinkedList([1])
    result4 = solution.deleteMiddle(test4)
    assert result4 == None
    
    print("All test cases passed!")

# Run tests
test_solution()