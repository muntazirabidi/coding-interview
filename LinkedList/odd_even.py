'''
Given the head of a singly linked list, group all the nodes with odd indices together followed by the nodes with even indices, and return the reordered list.

The first node is considered odd, and the second node is even, and so on.

Note that the relative order inside both the even and odd groups should remain as it was in the input.

You must solve the problem in O(1) extra space complexity and O(n) time complexity.
'''
from typing import Optional

# Definition for singly-linked list.
class ListNode:
    def __init__(self, val=0, next=None):
        self.val = val
        self.next = next

class Solution:
    def oddEvenList(self, head: Optional[ListNode]) -> Optional[ListNode]:
        if not head or not head.next:
            return head
            
        # Initialize pointers
        odd = head  # First node (1-indexed)
        even = head.next  # Second node
        evenHead = even  # Save the head of even list
        
        # Rearrange nodes
        while even and even.next:
            # Connect odd nodes
            odd.next = even.next
            odd = odd.next
            
            # Connect even nodes
            even.next = odd.next
            even = even.next
        
        # Connect the end of odd list to the head of even list
        odd.next = evenHead
        
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
    
    # Test case 1: [1,2,3,4,5]
    test1 = createLinkedList([1,2,3,4,5])
    result1 = solution.oddEvenList(test1)
    assert linkedListToArray(result1) == [1,3,5,2,4]
    
    # Test case 2: [2,1,3,5,6,4,7]
    test2 = createLinkedList([2,1,3,5,6,4,7])
    result2 = solution.oddEvenList(test2)
    assert linkedListToArray(result2) == [2,3,6,7,1,5,4]
    
    # Test case 3: [1,2]
    test3 = createLinkedList([1,2])
    result3 = solution.oddEvenList(test3)
    assert linkedListToArray(result3) == [1,2]
    
    # Test case 4: [1]
    test4 = createLinkedList([1])
    result4 = solution.oddEvenList(test4)
    assert linkedListToArray(result4) == [1]
    
    print("All test cases passed!")

# Run tests
test_solution()
        