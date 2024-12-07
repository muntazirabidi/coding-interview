# Comprehensive Binary Tree Problems Guide

## Basic Setup

```python
from node import Node

def build_sample_tree():
    """
    Creates and returns a sample binary tree for testing.
    Returns:
        Node: The root node of the binary tree.
    """
    # Create nodes
    a = Node('a')
    b = Node('b')
    c = Node('c')
    d = Node('d')
    e = Node('e')
    f = Node('f')

    # Establish relationships
    a.left = b
    a.right = c
    b.left = d
    b.right = e
    c.right = f

    return a
```

## 1. Tree Height

The height of a tree is the length of the longest path from root to leaf. This is a fundamental problem that appears in many tree-related questions.

```python
def tree_height(root):
    """
    Calculates the height of a binary tree.
    Args:
        root (Node): The root node of the binary tree.
    Returns:
        int: The height of the tree (empty tree has height -1).
    """
    if root is None:
        return -1

    left_height = tree_height(root.left)
    right_height = tree_height(root.right)

    # Height is the maximum path length from root to leaf
    return 1 + max(left_height, right_height)
```

## 2. Level Width

Finding the width at each level helps us understand the tree's structure and is crucial for problems involving tree visualization.

```python
def level_width(root):
    """
    Calculates the width of each level in the binary tree.
    Args:
        root (Node): The root node of the binary tree.
    Returns:
        list: A list where each element is the width of that level.
    """
    if root is None:
        return []

    widths = []
    level = [root, None]  # None marks end of level
    current_width = 0

    while len(level) > 1:  # While more than just the level marker
        current = level.pop(0)

        if current is None:
            widths.append(current_width)
            current_width = 0
            level.append(None)
            continue

        current_width += 1

        if current.left:
            level.append(current.left)
        if current.right:
            level.append(current.right)

    widths.append(current_width)  # Append the last level
    return widths
```

## 3. Bottom View

The bottom view shows what you'd see looking at the tree from below. This tests understanding of vertical alignment in trees.

```python
def bottom_view(root):
    """
    Returns the bottom view of the binary tree.
    Args:
        root (Node): The root node of the binary tree.
    Returns:
        list: Values visible from bottom, left to right.
    """
    if root is None:
        return []

    # Dictionary to store the bottommost node at each horizontal distance
    hd_map = {}  # horizontal distance -> node value
    queue = [(root, 0)]  # (node, horizontal distance)
    min_hd = max_hd = 0

    while queue:
        node, hd = queue.pop(0)

        # Update horizontal distance bounds
        min_hd = min(min_hd, hd)
        max_hd = max(max_hd, hd)

        # Update value for this horizontal distance
        hd_map[hd] = node.data

        if node.left:
            queue.append((node.left, hd - 1))
        if node.right:
            queue.append((node.right, hd + 1))

    # Construct result from left to right
    return [hd_map[i] for i in range(min_hd, max_hd + 1)]
```

## 4. Cousins in Binary Tree

Two nodes are cousins if they have the same depth but different parents. This problem tests both level tracking and parent relationships.

```python
def find_cousins(root, target):
    """
    Finds all cousins of a target node in the binary tree.
    Args:
        root (Node): The root node of the binary tree.
        target: The value to find cousins for.
    Returns:
        list: Values of all cousin nodes.
    """
    if root is None:
        return []

    queue = [(root, None, 0)]  # (node, parent, level)
    target_level = -1
    target_parent = None
    cousins = []

    # First find target's level and parent
    while queue and target_level == -1:
        node, parent, level = queue.pop(0)

        if node.data == target:
            target_level = level
            target_parent = parent
            continue

        if node.left:
            queue.append((node.left, node, level + 1))
        if node.right:
            queue.append((node.right, node, level + 1))

    if target_level == -1:  # Target not found
        return []

    # Find all nodes at target_level with different parent
    queue = [(root, None, 0)]
    while queue:
        node, parent, level = queue.pop(0)

        if level == target_level and parent != target_parent:
            cousins.append(node.data)

        if level < target_level:
            if node.left:
                queue.append((node.left, node, level + 1))
            if node.right:
                queue.append((node.right, node, level + 1))

    return cousins
```

## 5. Path with Given Sum

Finding if there exists a root-to-leaf path with a given sum is a classic tree problem combining path tracking and sum calculation.

```python
def has_path_sum(root, target_sum):
    """
    Checks if there exists a root-to-leaf path that sums to target_sum.
    Args:
        root (Node): The root node of the binary tree.
        target_sum (int): The target sum to find.
    Returns:
        bool: True if such a path exists, False otherwise.
    """
    def dfs(node, remaining_sum):
        if node is None:
            return False

        # If it's a leaf node, check if we've reached our target
        if node.left is None and node.right is None:
            return remaining_sum == node.data

        # Try both paths, subtracting current node's value
        return (dfs(node.left, remaining_sum - node.data) or
                dfs(node.right, remaining_sum - node.data))

    return dfs(root, target_sum)
```

## 6. Invert Binary Tree

Inverting a binary tree is a fundamental transformation that tests understanding of tree manipulation.

```python
def invert_tree(root):
    """
    Inverts a binary tree (mirror image).
    Args:
        root (Node): The root node of the binary tree.
    Returns:
        Node: Root of the inverted tree.
    """
    if root is None:
        return None

    # Swap children
    root.left, root.right = root.right, root.left

    # Recursively invert subtrees
    invert_tree(root.left)
    invert_tree(root.right)

    return root
```

## 7. Serialize and Deserialize

This problem tests deep understanding of tree structure and traversal by converting between tree and string formats.

```python
def serialize(root):
    """
    Serializes a binary tree to a string.
    Args:
        root (Node): The root node of the binary tree.
    Returns:
        str: String representation of the tree.
    """
    if root is None:
        return "null"

    return f"{root.data},{serialize(root.left)},{serialize(root.right)}"

def deserialize(data):
    """
    Deserializes a string to a binary tree.
    Args:
        data (str): String representation of the tree.
    Returns:
        Node: The root node of the reconstructed tree.
    """
    def dfs():
        val = next(values)
        if val == "null":
            return None

        node = Node(val)
        node.left = dfs()
        node.right = dfs()
        return node

    values = iter(data.split(','))
    return dfs()
```

## 8. Diameter of Binary Tree

The diameter is the longest path between any two nodes, which may or may not pass through the root.

```python
def tree_diameter(root):
    """
    Calculates the diameter of a binary tree.
    Args:
        root (Node): The root node of the binary tree.
    Returns:
        int: The diameter of the tree.
    """
    max_diameter = 0

    def height(node):
        nonlocal max_diameter
        if node is None:
            return -1

        left_height = height(node.left)
        right_height = height(node.right)

        # Update diameter if path through this node is longer
        max_diameter = max(max_diameter, 2 + left_height + right_height)

        return 1 + max(left_height, right_height)

    height(root)
    return max_diameter
```

## 9. Balanced Binary Tree Check

A balanced tree has the heights of left and right subtrees differing by at most one for all nodes.

```python
def is_balanced(root):
    """
    Checks if a binary tree is height-balanced.
    Args:
        root (Node): The root node of the binary tree.
    Returns:
        bool: True if the tree is balanced, False otherwise.
    """
    def check_height(node):
        if node is None:
            return 0

        left_height = check_height(node.left)
        if left_height == -1:
            return -1

        right_height = check_height(node.right)
        if right_height == -1:
            return -1

        if abs(left_height - right_height) > 1:
            return -1

        return 1 + max(left_height, right_height)

    return check_height(root) != -1
```

## 10. Lowest Common Ancestor

Finding the lowest common ancestor (LCA) of two nodes is crucial for understanding relationships in trees.

```python
def lowest_common_ancestor(root, p, q):
    """
    Finds the lowest common ancestor of two nodes.
    Args:
        root (Node): The root node of the binary tree.
        p: Value of first node.
        q: Value of second node.
    Returns:
        Node: The lowest common ancestor node.
    """
    if root is None or root.data == p or root.data == q:
        return root

    left = lowest_common_ancestor(root.left, p, q)
    right = lowest_common_ancestor(root.right, p, q)

    if left and right:  # If p and q are in different subtrees
        return root

    return left if left else right  # Return non-null value
```

## 11. Right Side View

The right side view shows what you'd see looking at the tree from the right side.

```python
def right_side_view(root):
    """
    Returns the right side view of the binary tree.
    Args:
        root (Node): The root node of the binary tree.
    Returns:
        list: Values visible from the right side.
    """
    if root is None:
        return []

    result = []
    queue = [(root, 0)]  # (node, level)
    current_level = 0
    current_right = None

    while queue:
        node, level = queue.pop(0)

        # We're still at the same level
        if level == current_level:
            current_right = node.data
        else:
            # We've moved to a new level, add the rightmost node
            # from the previous level
            result.append(current_right)
            current_level = level
            current_right = node.data

        # Add children (left first, so right child processes last)
        if node.left:
            queue.append((node.left, level + 1))
        if node.right:
            queue.append((node.right, level + 1))

    # Add the last level's rightmost node
    result.append(current_right)
    return result
```

## Usage and Testing

```python
if __name__ == '__main__':
    # Build sample tree
    root = build_sample_tree()

    # Test various functions
    print("Tree height:", tree_height(root))
    print("Level widths:", level_width(root))
    print("Bottom view:", bottom_view(root))
    print("Right side view:", right_side_view(root))
    print("Is balanced:", is_balanced(root))
    print("Tree diameter:", tree_diameter(root))

    # Test path sum
    print("Has path sum 10:", has_path_sum(root, 10))

    # Test serialization
    serialized = serialize(root)
    print("Serialized tree:", serialized)
    deserialized_root = deserialize(serialized)
```

## Testing Strategy

When testing these functions, consider:

1. Tree Structures:

   - Empty tree (None)
   - Single node
   - Perfect binary tree
   - Skewed tree (left/right)
   - Unbalanced tree
   - Complete binary tree

2. Values:

   - Positive/negative numbers
   - Duplicate values
   - Different data types
   - Very large values

3. Edge Cases:

   - Maximum/minimum possible values
   - Deep trees (recursion limit)
   - Wide trees (memory constraints)
   - All nodes same value

4. Performance:
   - Time complexity verification
   - Space complexity verification
   - Large input handling

## Essential Concepts for Tree Problems

### Understanding Tree Properties

When working with binary trees, it's essential to understand that every tree problem revolves around a few fundamental properties:

1. Structural Properties
   A binary tree's structure gives us important guarantees that we can use in our solutions. Every node has at most two children, which means:

   - We can always process a node's children in a predictable order
   - The maximum number of nodes at any level L is 2^L
   - A perfect binary tree of height H has 2^(H+1) - 1 nodes

2. Path Properties
   The concept of paths in trees is fundamental to many problems:
   - Every node has exactly one path from the root to reach it
   - The height of a tree is the length of the longest root-to-leaf path
   - Any two nodes have a unique lowest common ancestor (LCA)

### Common Problem-Solving Patterns

When approaching tree problems, look for these common patterns:

1. The Recursive Pattern
   Most tree problems can be solved recursively by following this template:

   ```python
   def solve_tree(root):
       # Base case - usually empty tree or leaf
       if root is None:
           return base_value

       # Process left and right subtrees
       left_result = solve_tree(root.left)
       right_result = solve_tree(root.right)

       # Combine results with current node
       return combine(root.data, left_result, right_result)
   ```

2. The Level-by-Level Pattern
   For problems involving level relationships, use this template:

   ```python
   def process_by_level(root):
       if root is None:
           return result

       queue = [root]
       while queue:
           level_size = len(queue)
           for _ in range(level_size):
               node = queue.pop(0)
               # Process node
               if node.left:
                   queue.append(node.left)
               if node.right:
                   queue.append(node.right)
   ```

### State Management in Tree Problems

One of the trickier aspects of tree problems is managing state. Here are key approaches:

1. Using Global Variables
   When you need to track information across all recursive calls:

   ```python
   def tree_problem(root):
       result = []  # Global state

       def dfs(node):
           nonlocal result
           if node is None:
               return
           # Update result
           dfs(node.left)
           dfs(node.right)

       dfs(root)
       return result
   ```

2. Passing State Down
   When each recursive call needs its own state:

   ```python
   def tree_problem(root):
       def dfs(node, state):
           if node is None:
               return
           # Modify state for children
           new_state = update_state(state)
           dfs(node.left, new_state)
           dfs(node.right, new_state)

       return dfs(root, initial_state)
   ```

### Space-Time Trade-offs

Understanding space-time trade-offs is crucial for optimizing tree solutions:

1. Recursive vs Iterative Solutions

   - Recursive solutions are often cleaner but use O(h) stack space
   - Iterative solutions might be more complex but can use less space
   - For balanced trees, height h = log(n), but for skewed trees, h = n

2. Memory Usage Patterns
   - DFS uses O(h) space for the recursion stack
   - BFS uses O(w) space where w is the maximum width of the tree
   - For a balanced tree, the maximum width is n/2 at the bottom level

### Binary Search Tree Properties

When working with Binary Search Trees (BST), remember these properties:

1. The BST Property

   - All nodes in left subtree < current node
   - All nodes in right subtree > current node
   - This applies recursively to all subtrees

2. BST Traversal Optimization
   - Inorder traversal gives nodes in sorted order
   - Can often eliminate branches based on value comparisons
   - Search/Insert/Delete operations are O(h) where h is height

### Common Mistakes to Avoid

1. Base Case Handling

   - Always handle null nodes explicitly
   - Consider leaf nodes as a special case
   - Test with empty trees and single-node trees

2. Reference vs Value

   - Be careful when comparing nodes vs values
   - Remember that two nodes might have the same value but be different nodes
   - When storing nodes in collections, consider value equality vs reference equality

3. Recursion Stack
   - Watch out for stack overflow with deep trees
   - Consider iterative solutions for production code
   - Remember that each recursive call adds to memory usage

### Interview Strategy

When solving tree problems in interviews:

1. Analysis First

   - Draw the tree on paper/whiteboard
   - Walk through a small example
   - Consider edge cases before coding

2. Solution Development

   - Start with a recursive solution if possible
   - Optimize only after getting a working solution
   - Explain trade-offs as you make decisions

3. Testing Approach
   - Test with an empty tree
   - Test with a single node
   - Test with a balanced tree
   - Test with a skewed tree
   - Verify special cases mentioned in the problem

### Performance Optimization Tips

1. Early Termination
   When possible, add conditions to stop processing early:

   ```python
   def has_property(root):
       if root is None:
           return True
       if violates_property(root):
           return False  # Early termination
       return has_property(root.left) and has_property(root.right)
   ```

2. Caching Results
   For expensive computations, consider memoization:

   ```python
   def expensive_computation(root):
       cache = {}

       def dfs(node):
           if node in cache:
               return cache[node]
           # Compute result
           cache[node] = result
           return result

       return dfs(root)
   ```

3. Level Processing Optimization
   When processing levels, track size to avoid queue length checks:
   ```python
   def process_levels(root):
       queue = [root]
       while queue:
           size = len(queue)  # Current level size
           for _ in range(size):  # Process exactly one level
               node = queue.pop(0)
               # Process level nodes
   ```

Remember: The key to mastering tree problems is understanding these fundamental concepts and patterns. With practice, you'll start recognizing which approach fits each problem type. Always think about the tree's properties and how they can help you solve the problem more efficiently.

Would you like me to explain any of these concepts in more detail or add additional patterns and tips?
