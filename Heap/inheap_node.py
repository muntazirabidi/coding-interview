from typing import Optional, Any
from dataclasses import dataclass

@dataclass
class Node:
    value: Any
    left: Optional['Node'] = None
    right: Optional['Node'] = None
    parent: Optional['Node'] = None

class HeapError(Exception):
    """Custom exception for heap operations."""
    pass

class MinHeap:
    """
    A Min Heap implementation using nodes for a tree-like structure.
    """

    def __init__(self):
        """Initialize an empty min heap."""
        self.root: Optional[Node] = None
        self.size = 0

    def insert(self, value: Any) -> None:
        """Insert a new value into the heap."""
        new_node = Node(value)
        self.size += 1

        if not self.root:
            self.root = new_node
            return

        # Find the correct place to insert the new node
        current = self.root
        queue = [current]
        while queue:
            node = queue.pop(0)
            if not node.left:
                node.left = new_node
                new_node.parent = node
                self._bubble_up(new_node)
                return
            elif not node.right:
                node.right = new_node
                new_node.parent = node
                self._bubble_up(new_node)
                return
            else:
                queue.append(node.left)
                if node.right:
                    queue.append(node.right)

    def _bubble_up(self, node: Node) -> None:
        """Move the node up the heap to maintain min-heap property."""
        parent = node.parent
        while parent and node.value < parent.value:
            node.value, parent.value = parent.value, node.value
            node = parent
            parent = node.parent

    def remove_min(self) -> Optional[Any]:
        """Remove and return the minimum element from the heap."""
        if not self.root:
            return None
        
        min_value = self.root.value
        if not self.root.left:
            self.root = None
        else:
            # Find the last node in the heap
            last_node = self._find_last_node()
            # Replace root's value with last node's value
            self.root.value = last_node.value
            # Remove the last node
            self._remove_last_node(last_node)
            # Bubble down from root
            self._bubble_down(self.root)
        self.size -= 1
        return min_value

    def _find_last_node(self) -> Node:
        """Find the last node in the heap (level order)."""
        if not self.root:
            raise HeapError("Heap is empty")
        
        queue = [self.root]
        while queue:
            node = queue.pop(0)
            if not node.left or not node.right:
                if node.right:
                    return node.right
                elif node.left:
                    return node.left
            queue.extend([child for child in (node.left, node.right) if child])

    def _remove_last_node(self, node: Node) -> None:
        """Remove the last node from the heap."""
        parent = node.parent
        if parent:
            if parent.right == node:
                parent.right = None
            else:  # node is left child
                parent.left = None

    def _bubble_down(self, node: Node) -> None:
        """Move the node down the heap to maintain min-heap property."""
        while True:
            smallest = node
            if node.left and node.left.value < smallest.value:
                smallest = node.left
            if node.right and node.right.value < smallest.value:
                smallest = node.right

            if smallest == node:
                break

            node.value, smallest.value = smallest.value, node.value
            node = smallest

    def peek(self) -> Optional[Any]:
        """Return the minimum element without removing it."""
        return self.root.value if self.root else None

    def is_empty(self) -> bool:
        """Check if the heap is empty."""
        return self.size == 0

    def __len__(self) -> int:
        """Return the size of the heap."""
        return self.size