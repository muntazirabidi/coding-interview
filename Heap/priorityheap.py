from typing import Any
from minheap import MinHeap

class PriorityHeap(MinHeap):
    """Heap for any values with explicit priorities"""
    def __init__(self):
        super().__init__()
    
    def insert(self, priority: int, value: Any):
        # Store (priority, value) tuple
        self.heap.append((priority, value))
        self._bubble_up(len(self.heap) - 1)

# Example usage
priority_heap = PriorityHeap()
# Insert (priority, value) pairs
priority_heap.insert(3, "Medium task")
priority_heap.insert(1, "Urgent task")
priority_heap.insert(5, "Low priority task")