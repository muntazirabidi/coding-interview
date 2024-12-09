from typing import List, Optional
import heapq

class KthLargestFinder:
    """
    A class that finds the kth largest element in an array using a min heap.
    
    This class implements a solution using Python's heapq module to maintain
    a min heap of size k, where the root of the heap will be the kth largest
    element after processing all numbers.
    
    Time Complexity: O(n log k) where n is the length of the input array
    Space Complexity: O(k) to store the heap
    
    Example:
        >>> finder = KthLargestFinder()
        >>> finder.findKthLargest([3,2,1,5,6,4], 2)
        5  # 5 is the 2nd largest element after 6
    """
    
    def findKthLargest(self, nums: List[int], k: int) -> Optional[int]:
        """
        Finds the kth largest element in an array.
        
        Args:
            nums (List[int]): An array of integers
            k (int): The position of the largest element to find (1-based)
                    k=1 means find the largest element
                    k=2 means find the second largest element, etc.
        
        Returns:
            Optional[int]: The kth largest element in the array
                          Returns None if inputs are invalid
        
        Raises:
            ValueError: If k is less than 1 or greater than array length
            ValueError: If the input array is empty
        
        Examples:
            >>> finder = KthLargestFinder()
            >>> finder.findKthLargest([3,2,1,5,6,4], 2)
            5
            >>> finder.findKthLargest([1], 1)
            1
            >>> finder.findKthLargest([1,2,3,4,5], 3)
            3
        """
        # Input validation
        if not nums:
            raise ValueError("Input array cannot be empty")
        if k < 1:
            raise ValueError("k must be at least 1")
        if k > len(nums):
            raise ValueError("k cannot be larger than array length")
            
        # Create a min heap to store k largest elements
        min_heap = []
        

        for num in nums:

            if len(min_heap) < k:
                heapq.heappush(min_heap, num)

            elif num > min_heap[0]:
                heapq.heapreplace(min_heap, num)
                
        return min_heap[0] if min_heap else None


def test_kth_largest_finder():
    """
    Test function to verify the KthLargestFinder implementation.
    Covers various test cases and edge cases.
    """
    finder = KthLargestFinder()
    
    # Test case 1: Normal case
    assert finder.findKthLargest([3,2,1,5,6,4], 2) == 5, "Failed test case 1"
    
    # Test case 2: Array with duplicates
    assert finder.findKthLargest([3,2,3,1,2,4,5,5,6], 4) == 4, "Failed test case 2"
    
    # Test case 3: k = 1 (finding maximum)
    assert finder.findKthLargest([1,2,3,4,5], 1) == 5, "Failed test case 3"
    
    # Test case 4: k = length of array (finding minimum)
    assert finder.findKthLargest([1,2,3,4,5], 5) == 1, "Failed test case 4"
    
    # Test case 5: Single element array
    assert finder.findKthLargest([1], 1) == 1, "Failed test case 5"
    
    # Test case 6: Negative numbers
    assert finder.findKthLargest([-1,-2,-3,-4,-5], 2) == -2, "Failed test case 6"
    
    # Test case 7: Error cases
    try:
        finder.findKthLargest([], 1)
        assert False, "Should raise ValueError for empty array"
    except ValueError:
        pass
        
    try:
        finder.findKthLargest([1,2,3], 0)
        assert False, "Should raise ValueError for k < 1"
    except ValueError:
        pass
        
    try:
        finder.findKthLargest([1,2,3], 4)
        assert False, "Should raise ValueError for k > array length"
    except ValueError:
        pass
    
    print("All test cases passed!")

# Run the tests
if __name__ == "__main__":
    test_kth_largest_finder()