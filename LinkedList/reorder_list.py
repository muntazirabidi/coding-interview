from typing import Optional

class ListNode:
    def __init__(self, val=0, next=None):
        self.val = val
        self.next = next

class Solution:
    def reorderList(self, head: Optional[ListNode]) -> None:
        """
        Do not return anything, modify head in-place instead.
        """
        if not head or not head.next:
            return

        # 1. Find middle
        slow, fast = head, head.next
        while fast and fast.next:
            slow = slow.next
            fast = fast.next.next

        # 2. Break the list into two halves
        # This is a crucial step that was missing
        second = slow.next
        slow.next = None  # Break the link

        # 3. Reverse the second half
        prev = None
        while second:
            temp = second.next
            second.next = prev
            prev = second
            second = temp

        # 4. Merge two halves
        first, second = head, prev
        while second:
            temp1, temp2 = first.next, second.next
            first.next = second
            second.next = temp1
            first, second = temp1, temp2
            
            
            
def test_reorder():
    # Helper function to create list
    def create_list(arr):
        if not arr: return None
        head = ListNode(arr[0])
        curr = head
        for val in arr[1:]:
            curr.next = ListNode(val)
            curr = curr.next
        return head
    
    # Helper function to convert to array
    def list_to_array(head):
        result = []
        while head:
            result.append(head.val)
            head = head.next
        return result
    
    # Test cases
    test_cases = [
        [1,2,3,4],
        [1,2,3,4,5],
        [1],
        [1,2]
    ]
    
    sol = Solution()
    for arr in test_cases:
        head = create_list(arr)
        sol.reorderList(head)
        result = list_to_array(head)
        print(f"Input: {arr}")
        print(f"Output: {result}\n")

if __name__ == "__main__":
  test_reorder()