from typing import Optional, Any, List
from dataclasses import dataclass
from collections.abc import Sequence

class HeapError(Exception):
    """Custom exception for heap operations."""
    pass

class MinHeap:
    """
    A Min Heap implementation with type hints and error handling.
    
    A min heap is a complete binary tree where the value of each node is less than
    or equal to the values of its children.
    """
    
    def __init__(self) -> None:
        """Initialize an empty min heap."""
        self.heap: List[Any] = []
    
    def get_parent_index(self, index: int) -> Optional[int]:
        """
        Get the parent index for a given node index.
        
        Args:
            index: Index of the current node
            
        Returns:
            Optional[int]: Parent index or None if no parent exists
        
        Raises:
            ValueError: If index is negative
        """
        if index < 0:
            raise ValueError("Index cannot be negative")
        if index <= 0:  # Root has no parent
            return None
        return (index - 1) // 2
    
    def get_left_child_index(self, index: int) -> Optional[int]:
        """
        Get the left child index for a given node index.
        
        Args:
            index: Index of the current node
            
        Returns:
            Optional[int]: Left child index or None if no left child exists
            
        Raises:
            ValueError: If index is negative
        """
        if index < 0:
            raise ValueError("Index cannot be negative")
        left_index = 2 * index + 1
        if left_index >= len(self.heap):
            return None
        return left_index
    
    def get_right_child_index(self, index: int) -> Optional[int]:
        """
        Get the right child index for a given node index.
        
        Args:
            index: Index of the current node
            
        Returns:
            Optional[int]: Right child index or None if no right child exists
            
        Raises:
            ValueError: If index is negative
        """
        if index < 0:
            raise ValueError("Index cannot be negative")
        right_index = 2 * index + 2
        if right_index >= len(self.heap):
            return None
        return right_index
    
    def swap(self, i: int, j: int) -> None:
        """
        Swap two elements in the heap.
        
        Args:
            i: First index
            j: Second index
            
        Raises:
            IndexError: If either index is out of bounds
        """
        if i < 0 or j < 0 or i >= len(self.heap) or j >= len(self.heap):
            raise IndexError("Index out of bounds")
        self.heap[i], self.heap[j] = self.heap[j], self.heap[i]
    
    def has_left_child(self, index: int) -> bool:
        """Check if node has a left child."""
        return self.get_left_child_index(index) is not None
    
    def has_right_child(self, index: int) -> bool:
        """Check if node has a right child."""
        return self.get_right_child_index(index) is not None
    
    def get_parent_value(self, index: int) -> Optional[Any]:
        """Get the value of parent node."""
        parent_index = self.get_parent_index(index)
        if parent_index is None:
            return None
        return self.heap[parent_index]
    
    def get_left_child_value(self, index: int) -> Optional[Any]:
        """Get the value of left child node."""
        left_index = self.get_left_child_index(index)
        if left_index is None:
            return None
        return self.heap[left_index]
    
    def get_right_child_value(self, index: int) -> Optional[Any]:
        """Get the value of right child node."""
        right_index = self.get_right_child_index(index)
        if right_index is None:
            return None
        return self.heap[right_index]
    
    def insert(self, value: Any) -> None:
        """
        Insert a new value into the heap.
        
        Args:
            value: Value to insert
        """
        self.heap.append(value)
        self._bubble_up(len(self.heap) - 1)
    
    def _bubble_up(self, index: int) -> None:
        """
        Restore heap property by moving a node up.
        
        Args:
            index: Starting index for bubble up operation
            
        Raises:
            ValueError: If index is negative
        """
        if index < 0:
            raise ValueError("Index cannot be negative")
            
        while index > 0:
            parent_index = self.get_parent_index(index)
            if parent_index is None:
                break
            
            if self.heap[parent_index] > self.heap[index]:
                self.swap(parent_index, index)
                index = parent_index
            else:
                break
    
    def remove_min(self) -> Optional[Any]:
        """
        Remove and return the minimum element from the heap.
        
        Returns:
            Optional[Any]: The minimum element or None if heap is empty
        """
        if not self.heap:
            return None
            
        min_value = self.heap[0]
        
        if len(self.heap) == 1:
            self.heap.pop()
            return min_value
            
        self.heap[0] = self.heap[-1]
        self.heap.pop()
        self._bubble_down(0)
        
        return min_value
    
    def _bubble_down(self, index: int) -> None:
        """
        Restore heap property by moving a node down.
        
        Args:
            index: Starting index for bubble down operation
            
        Raises:
            ValueError: If index is negative or beyond heap size
        """
        if index < 0 or index >= len(self.heap):
            raise ValueError("Invalid index")
            
        while True:
            smallest = index
            left_index = self.get_left_child_index(index)
            right_index = self.get_right_child_index(index)
            
            if left_index is not None and self.heap[left_index] < self.heap[smallest]:
                smallest = left_index
            
            if right_index is not None and self.heap[right_index] < self.heap[smallest]:
                smallest = right_index
            
            if smallest == index:
                break
                
            self.swap(index, smallest)
            index = smallest
    
    def peek(self) -> Optional[Any]:
        """Return the minimum element without removing it."""
        return None if not self.heap else self.heap[0]
    
    def size(self) -> int:
        """Return the number of elements in the heap."""
        return len(self.heap)
    
    def is_empty(self) -> bool:
        """Check if the heap is empty."""
        return len(self.heap) == 0
    
    def __str__(self) -> str:
        """String representation of the heap."""
        return str(self.heap)
    
    def __len__(self) -> int:
        """Return the size of the heap."""
        return len(self.heap)
      
      
class MaxHeap:
    def __init__(self):
        self.min_heap = MinHeap()
    
    def insert(self, value):
        # Insert negative value into min heap
        self.min_heap.insert(-value)
    
    def remove_max(self):
        # Remove minimum (which is negative of our maximum) and negate it
        min_val = self.min_heap.remove_min()
        return -min_val if min_val is not None else None
    
    def peek_max(self):
        # Look at minimum (which is negative of our maximum) and negate it
        min_val = self.min_heap.peek()
        return -min_val if min_val is not None else None


      

      
def test_min_heap():
    # Create a new heap
    heap = MinHeap()
    
    # Test 1: Empty heap operations
    print("\nTest 1: Empty heap operations")
    print(f"Is empty? {heap.is_empty()}")  # Should be True
    print(f"Size: {len(heap)}")  # Should be 0
    print(f"Peek: {heap.peek()}")  # Should be None
    print(f"Remove min from empty heap: {heap.remove_min()}")  # Should be None
    
    # Test 2: Insertions
    print("\nTest 2: Insertions")
    values = [5, 3, 7, 1, 4, 6, 2]
    print(f"Inserting values: {values}")
    for value in values:
        heap.insert(value)
    print(f"Heap after insertions: {heap}")  # Should be ordered as min heap
    print(f"Size after insertions: {len(heap)}")  # Should be 7
    
    # Test 3: Peek and Remove operations
    print("\nTest 3: Peek and Remove operations")
    print(f"Peek at minimum: {heap.peek()}")  # Should be 1
    removed_values = []
    while not heap.is_empty():
        removed_values.append(heap.remove_min())
    print(f"Values removed in order: {removed_values}")  # Should be sorted
    
    # Test 4: Edge cases
    print("\nTest 4: Edge cases")
    try:
        heap.get_parent_index(-1)
    except ValueError as e:
        print(f"Caught expected error for negative index: {e}")
        
    try:
        heap.get_left_child_index(-1)
    except ValueError as e:
        print(f"Caught expected error for negative index: {e}")
    
    # Test 5: Duplicate values
    print("\nTest 5: Duplicate values")
    heap = MinHeap()
    values = [3, 3, 1, 1, 2, 2]
    for value in values:
        heap.insert(value)
    print(f"Heap with duplicates: {heap}")
    removed_values = []
    while not heap.is_empty():
        removed_values.append(heap.remove_min())
    print(f"Removed values with duplicates: {removed_values}")
    
    # Test 6: Large number of elements
    print("\nTest 6: Large number of elements")
    heap = MinHeap()
    import random
    values = random.sample(range(1000), 20)  # 20 random numbers
    for value in values:
        heap.insert(value)
    print(f"Original random values: {sorted(values)}")
    removed_values = []
    while not heap.is_empty():
        removed_values.append(heap.remove_min())
    print(f"Heap sorted values: {removed_values}")
    print(f"Correctly sorted? {removed_values == sorted(values)}")

# Run the tests
if __name__ == "__main__":
    test_min_heap()
    
    # Usage example
    max_heap = MaxHeap()
    values = [5, 3, 7, 1, 4]
    print("Inserting:", values)

    for value in values:
        max_heap.insert(value)

    # Remove all values (should come out in descending order)
    while True:
        max_val = max_heap.remove_max()
        if max_val is None:
            break
        print(f"Removed max: {max_val}")