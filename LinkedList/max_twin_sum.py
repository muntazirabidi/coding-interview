'''
Medium

Topics

Companies

Hint
In a linked list of size n, where n is even, the ith node (0-indexed) of the linked list is known as the twin of the (n-1-i)th node, if 0 <= i <= (n / 2) - 1.

For example, if n = 4, then node 0 is the twin of node 3, and node 1 is the twin of node 2. These are the only nodes with twins for n = 4.
The twin sum is defined as the sum of a node and its twin.

Given the head of a linked list with even length, return the maximum twin sum of the linked list.

'''
from typing import Optional, List
import unittest

class ListNode:
    def __init__(self, val=0, next=None):
        self.val = val
        self.next = next

class Solution:
    def pairSum(self, head: Optional[ListNode]) -> int:
        if not head or not head.next:
            return None
            
        # Step 1: Find middle
        slow, fast = head, head
        while fast and fast.next:
            slow = slow.next
            fast = fast.next.next
            
        # Step 2: Reverse second half
        prev = None
        curr = slow
        while curr:
            next_temp = curr.next
            curr.next = prev
            prev = curr
            curr = next_temp
            
        # Step 3: Find maximum twin sum
        max_sum = 0
        first = head
        second = prev
        while second:
            curr_sum = first.val + second.val
            max_sum = max(max_sum, curr_sum)
            first = first.next
            second = second.next
        return max_sum

class TestTwinSum(unittest.TestCase):
    def create_linked_list(self, values: List[int]) -> Optional[ListNode]:
        if not values:
            return None
        head = ListNode(values[0])
        current = head
        for val in values[1:]:
            current.next = ListNode(val)
            current = current.next
        return head
        
    def linked_list_to_array(self, head: Optional[ListNode]) -> List[int]:
        result = []
        current = head
        while current:
            result.append(current.val)
            current = current.next
        return result

    def test_basic_cases(self):
        solution = Solution()
        
        # Test case 1: Basic even-length list
        test1 = self.create_linked_list([5, 4, 2, 1])
        self.assertEqual(solution.pairSum(test1), 6, "Failed with basic list [5,4,2,1]")
        
        # Test case 2: Two elements only
        test2 = self.create_linked_list([1, 2])
        self.assertEqual(solution.pairSum(test2), 3, "Failed with two elements [1,2]")
        
        # Test case 3: All same values
        test3 = self.create_linked_list([1, 1, 1, 1])
        self.assertEqual(solution.pairSum(test3), 2, "Failed with same values [1,1,1,1]")

    

    def test_longer_lists(self):
        solution = Solution()
        
        # Test case 7: Longer list with ascending values
        test7 = self.create_linked_list([1, 2, 3, 4, 5, 6])
        self.assertEqual(solution.pairSum(test7), 7, "Failed with longer ascending list")
        
        # Test case 8: Longer list with descending values
        test8 = self.create_linked_list([6, 5, 4, 3, 2, 1])
        self.assertEqual(solution.pairSum(test8), 7, "Failed with longer descending list")
        
        # Test case 9: Alternating values
        test9 = self.create_linked_list([1, 10, 2, 9, 3, 8])
        self.assertEqual(solution.pairSum(test9), 13, "Failed with alternating values")

def run_tests():
    unittest.main(argv=[''], exit=False)

if __name__ == '__main__':
    run_tests()