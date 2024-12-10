'''
Given the head of a singly linked list, reverse the list, and return the reversed list.
'''

# Definition for singly-linked list.
class ListNode:
    def __init__(self, val=0, next=None):
        self.val = val  # The value stored in the node
        self.next = next  # Pointer to the next node in the list

class Solution:
    def reverseList(self, head: Optional[ListNode]) -> Optional[ListNode]:
        """
        Given the head of a singly linked list, reverse the list, and return the reversed list.

        Args:
            head (Optional[ListNode]): The head node of the singly linked list.

        Returns:
            Optional[ListNode]: The head of the reversed linked list.
        
        This solution uses a recursive approach to reverse the linked list. The key idea is
        to reverse the list in chunks starting from the tail and moving towards the head.
        """

        # Base Case: If the list is empty or has only one node, it's already reversed.
        if not head or not head.next:
            return head

        # Recursive Case:
        # Reverse the rest of the list starting from the next node.
        # This recursive call will eventually return the new head of the reversed list.
        new_head = self.reverseList(head.next)

        # At this point, the sublist starting from `head.next` has been reversed.
        # We now update the pointers to include the current `head` in the reversed list.

        # Make the next node point back to the current node (reversing the direction).
        head.next.next = head

        # Break the old link to ensure the current node becomes the tail of the reversed list.
        head.next = None

        # Return the new head of the reversed list to the previous recursive call.
        return new_head

# Example Usage:
# Input: 1 -> 2 -> 3 -> 4 -> 5 -> None
# Output: 5 -> 4 -> 3 -> 2 -> 1 -> None

# Step-by-step explanation:
# 1. Recursively reverse the sublist starting from the second node.
# 2. Modify the pointers such that each node points back to its predecessor.
# 3. Continue until the base case is reached (empty list or single node).
# 4. Propagate the new head of the reversed list back up the recursive stack.

