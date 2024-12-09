import heapq
from typing import List, Set

class SmallestInfiniteSet:
    """
    A class to represent an infinite set containing all positive integers [1, 2, 3, 4, ...].
    Allows removal of the smallest number and adding a number back to the set.

    Methods:
    --------
    __init__():
        Initializes the set.
    popSmallest() -> int:
        Removes and returns the smallest integer in the set.
    addBack(num: int) -> None:
        Adds a positive integer back to the set if not already present.
    """

    def __init__(self) -> None:
        """
        Initializes the SmallestInfiniteSet object. 
        Starts with the smallest number set to 1 and an empty heap for storing returned numbers.
        """
        self.heap: List[int] = []  # Min-heap to store numbers added back
        self.in_heap: Set[int] = set()  # Set to track elements in the heap
        self.current: int = 1  # Counter for the next smallest number not yet popped

    def popSmallest(self) -> int:
        """
        Removes and returns the smallest integer from the set.
        If there are numbers in the heap, the smallest among them is removed and returned.
        Otherwise, the next smallest number from the infinite set is returned.

        Returns:
        --------
        int:
            The smallest integer currently in the set.
        """
        if self.heap:
            smallest = heapq.heappop(self.heap)
            self.in_heap.remove(smallest)  # Remove from the set to avoid duplicates
            return smallest
        else:
            self.current += 1
            return self.current - 1

    def addBack(self, num: int) -> None:
        """
        Adds a number back to the set if it was previously removed and not already present.
        The number is only added if it is less than the current smallest number in the infinite set.

        Parameters:
        -----------
        num : int
            The positive integer to add back to the set.
        """
        if num < self.current and num not in self.in_heap:
            heapq.heappush(self.heap, num)
            self.in_heap.add(num)


# Example Usage:
# obj = SmallestInfiniteSet()
# param_1 = obj.popSmallest()
# obj.addBack(num)
