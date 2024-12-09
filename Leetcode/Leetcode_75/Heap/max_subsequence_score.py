import heapq
from typing import List, Tuple

class Solution:
    """
    This class provides a solution to calculate the maximum subsequence score.
    
    Given two integer arrays nums1 and nums2 of equal length and a positive integer k,
    the goal is to select k indices such that the score is maximized. The score is defined as:
    score = sum(nums1[selected indices]) * min(nums2[selected indices])
    
    Example:
        nums1 = [1, 3, 3, 2], nums2 = [2, 1, 3, 4], k = 3
        If we select indices [0, 2, 3]:
        sum = nums1[0] + nums1[2] + nums1[3] = 1 + 3 + 2 = 6
        min = min(nums2[0], nums2[2], nums2[3]) = min(2, 3, 4) = 2
        score = 6 * 2 = 12
    """
    
    def maxScore(self, nums1: List[int], nums2: List[int], k: int) -> int:
        """
        Calculates the maximum score by selecting k indices based on nums1 and nums2.
        
        The algorithm works by:
        1. Sorting pairs (nums2, nums1) by nums2 in descending order
        2. Maintaining a min heap of k nums1 values
        3. For each nums2 value (potential minimum), finding the maximum possible sum
           from nums1 using the heap
        
        Args:
            nums1: First array, where selected indices contribute to the sum
            nums2: Second array, where selected indices contribute to the minimum value
            k: Number of indices to select
            
        Returns:
            The maximum possible score based on the given arrays and constraints
            
        Raises:
            ValueError: If inputs are invalid (empty arrays, k > length, etc.)
        """
        # Input validation
        if not nums1 or not nums2 or k <= 0:
            raise ValueError("Arrays cannot be empty and k must be positive")
        if len(nums1) != len(nums2):
            raise ValueError("Arrays must have equal length")
        if k > len(nums1):
            raise ValueError("k cannot be larger than array length")
            
        # Sort pairs by nums2 in descending order
        pairs: List[Tuple[int, int]] = sorted(zip(nums2, nums1), reverse=True)
        min_heap: List[int] = []
        current_sum: int = 0
        max_score: int = 0
        
        # Process each pair
        for multiplier, value in pairs:
            heapq.heappush(min_heap, value)
            current_sum += value
            
            # If heap size exceeds k, remove smallest value
            if len(min_heap) > k:
                current_sum -= heapq.heappop(min_heap)
            
            # Calculate score when we have exactly k elements
            if len(min_heap) == k:
                max_score = max(max_score, current_sum * multiplier)
                
        return max_score


def test_solution():
    """
    Comprehensive test suite for the maxScore solution.
    Tests various scenarios including edge cases and error conditions.
    """
    solution = Solution()
    
    def run_test(test_name: str, nums1: List[int], nums2: List[int], k: int, expected: int) -> None:
        """Helper function to run individual tests with proper error messages"""
        try:
            result = solution.maxScore(nums1, nums2, k)
            assert result == expected, f"{test_name} failed: expected {expected}, got {result}"
            print(f"{test_name} passed!")
        except Exception as e:
            print(f"{test_name} failed with error: {str(e)}")
            raise
    
    # Test case 1: Basic example
    run_test(
        "Basic example",
        nums1=[1, 3, 3, 2],
        nums2=[2, 1, 3, 4],
        k=3,
        expected=12
    )
    
    # Test case 2: All values identical
    run_test(
        "Identical values",
        nums1=[5, 5, 5],
        nums2=[3, 3, 3],
        k=2,
        expected=30
    )
    
    # Test case 3: k equals array length
    run_test(
        "Full array selection",
        nums1=[7, 6, 5],
        nums2=[2, 4, 1],
        k=3,
        expected=18
    )
    
    # Test case 4: Minimal array
    run_test(
        "Single element",
        nums1=[10],
        nums2=[5],
        k=1,
        expected=50
    )
    
    # Test case 5: Complex scenario
    run_test(
        "Complex scenario",
        nums1=[9, 7, 5, 3],
        nums2=[1, 2, 3, 4],
        k=2,
        expected=24
    )
    
    # Test error cases
    def test_error_cases():
        """Test various error conditions"""
        try:
            solution.maxScore([], [], 1)
            assert False, "Should raise error for empty arrays"
        except ValueError:
            print("Empty array test passed!")
            
        try:
            solution.maxScore([1, 2], [1], 1)
            assert False, "Should raise error for unequal array lengths"
        except ValueError:
            print("Unequal lengths test passed!")
            
        try:
            solution.maxScore([1], [1], 2)
            assert False, "Should raise error for k > array length"
        except ValueError:
            print("Invalid k test passed!")
    
    # Run error cases
    test_error_cases()
    print("All tests completed successfully!")


if __name__ == '__main__':
    test_solution()