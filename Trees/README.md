# Trees - Complete Interview Guide

## Table of Contents
- [Basic Concepts](#basic-concepts)
- [Tree Implementation](#tree-implementation)
- [Tree Traversals](#tree-traversals)
- [Binary Search Trees](#binary-search-trees)
- [Balanced Trees](#balanced-trees)
- [Common Problems](#common-problems)
- [Advanced Tree Concepts](#advanced-tree-concepts)
- [Interview Tips](#interview-tips)

## Basic Concepts

### Tree Node Definition
```python
class TreeNode:
    def __init__(self, val=0, left=None, right=None):
        self.val = val
        self.left = left
        self.right = right
```

### Tree Properties
- Height: Length of path from root to deepest leaf
- Depth: Length of path from node to root
- Balanced: Heights of left and right subtrees differ by at most one
- Complete: All levels filled except possibly last level
- Perfect: All internal nodes have two children and all leaves are at same level

## Tree Traversals

### 1. Depth-First Search (DFS)
```python
def inorder(root):
    """Left -> Root -> Right"""
    if not root:
        return
    inorder(root.left)
    print(root.val)
    inorder(root.right)

def preorder(root):
    """Root -> Left -> Right"""
    if not root:
        return
    print(root.val)
    preorder(root.left)
    preorder(root.right)

def postorder(root):
    """Left -> Right -> Root"""
    if not root:
        return
    postorder(root.left)
    postorder(root.right)
    print(root.val)

# Iterative Inorder Traversal
def inorder_iterative(root):
    stack = []
    curr = root
    result = []
    
    while stack or curr:
        while curr:
            stack.append(curr)
            curr = curr.left
        curr = stack.pop()
        result.append(curr.val)
        curr = curr.right
    
    return result
```

### 2. Breadth-First Search (BFS)
```python
from collections import deque

def level_order(root):
    if not root:
        return []
    
    result = []
    queue = deque([root])
    
    while queue:
        level_size = len(queue)
        current_level = []
        
        for _ in range(level_size):
            node = queue.popleft()
            current_level.append(node.val)
            
            if node.left:
                queue.append(node.left)
            if node.right:
                queue.append(node.right)
        
        result.append(current_level)
    
    return result
```

## Binary Search Trees

### BST Implementation
```python
class BST:
    def __init__(self):
        self.root = None
    
    def insert(self, val):
        if not self.root:
            self.root = TreeNode(val)
            return
        
        curr = self.root
        while True:
            if val < curr.val:
                if not curr.left:
                    curr.left = TreeNode(val)
                    break
                curr = curr.left
            else:
                if not curr.right:
                    curr.right = TreeNode(val)
                    break
                curr = curr.right
    
    def search(self, val):
        curr = self.root
        while curr and curr.val != val:
            curr = curr.left if val < curr.val else curr.right
        return curr
    
    def delete(self, val):
        def find_min(node):
            current = node
            while current.left:
                current = current.left
            return current
        
        def delete_node(root, val):
            if not root:
                return None
            
            if val < root.val:
                root.left = delete_node(root.left, val)
            elif val > root.val:
                root.right = delete_node(root.right, val)
            else:
                if not root.left:
                    return root.right
                elif not root.right:
                    return root.left
                
                # Node with two children
                temp = find_min(root.right)
                root.val = temp.val
                root.right = delete_node(root.right, temp.val)
            
            return root
        
        self.root = delete_node(self.root, val)
```

### BST Validation
```python
def is_valid_bst(root):
    def validate(node, min_val=float('-inf'), max_val=float('inf')):
        if not node:
            return True
            
        if node.val <= min_val or node.val >= max_val:
            return False
            
        return (validate(node.left, min_val, node.val) and
                validate(node.right, node.val, max_val))
    
    return validate(root)
```

## Common Problems

### 1. Lowest Common Ancestor
```python
def lowest_common_ancestor(root, p, q):
    if not root:
        return None
    
    if root.val > p.val and root.val > q.val:
        return lowest_common_ancestor(root.left, p, q)
    if root.val < p.val and root.val < q.val:
        return lowest_common_ancestor(root.right, p, q)
    
    return root
```

### 2. Maximum Path Sum
```python
def max_path_sum(root):
    max_sum = float('-inf')
    
    def max_gain(node):
        nonlocal max_sum
        if not node:
            return 0
        
        left_gain = max(max_gain(node.left), 0)
        right_gain = max(max_gain(node.right), 0)
        
        current_path_sum = node.val + left_gain + right_gain
        max_sum = max(max_sum, current_path_sum)
        
        return node.val + max(left_gain, right_gain)
    
    max_gain(root)
    return max_sum
```

### 3. Serialize and Deserialize Binary Tree
```python
class Codec:
    def serialize(self, root):
        if not root:
            return 'null'
        return f'{root.val},{self.serialize(root.left)},{self.serialize(root.right)}'
    
    def deserialize(self, data):
        def dfs():
            val = next(values)
            if val == 'null':
                return None
            
            node = TreeNode(int(val))
            node.left = dfs()
            node.right = dfs()
            return node
        
        values = iter(data.split(','))
        return dfs()
```

## Advanced Tree Concepts

### 1. AVL Tree Operations
```python
class AVLNode:
    def __init__(self, val):
        self.val = val
        self.left = None
        self.right = None
        self.height = 1

class AVLTree:
    def get_height(self, node):
        if not node:
            return 0
        return node.height
    
    def get_balance(self, node):
        if not node:
            return 0
        return self.get_height(node.left) - self.get_height(node.right)
    
    def right_rotate(self, y):
        x = y.left
        T2 = x.right
        
        x.right = y
        y.left = T2
        
        y.height = max(self.get_height(y.left), self.get_height(y.right)) + 1
        x.height = max(self.get_height(x.left), self.get_height(x.right)) + 1
        
        return x
    
    def left_rotate(self, x):
        y = x.right
        T2 = y.left
        
        y.left = x
        x.right = T2
        
        x.height = max(self.get_height(x.left), self.get_height(x.right)) + 1
        y.height = max(self.get_height(y.left), self.get_height(y.right)) + 1
        
        return y
```

### 2. Red-Black Tree Properties
1. Every node is either red or black
2. Root is black
3. All leaves (NIL) are black
4. If a node is red, its children are black
5. Every path from root to leaves has same number of black nodes

### 3. Segment Tree
```python
class SegmentTree:
    def __init__(self, arr):
        self.n = len(arr)
        self.tree = [0] * (4 * self.n)
        self.build(arr, 0, 0, self.n - 1)
    
    def build(self, arr, node, start, end):
        if start == end:
            self.tree[node] = arr[start]
            return
        
        mid = (start + end) // 2
        self.build(arr, 2*node + 1, start, mid)
        self.build(arr, 2*node + 2, mid + 1, end)
        self.tree[node] = self.tree[2*node + 1] + self.tree[2*node + 2]
    
    def query(self, node, start, end, l, r):
        if r < start or end < l:
            return 0
        
        if l <= start and end <= r:
            return self.tree[node]
        
        mid = (start + end) // 2
        return (self.query(2*node + 1, start, mid, l, r) +
                self.query(2*node + 2, mid + 1, end, l, r))
```

## Interview Tips

### Time Complexity Analysis
Operation | Average | Worst
----------|---------|-------
Insert    | O(log n)| O(n)
Delete    | O(log n)| O(n)
Search    | O(log n)| O(n)
Traversal | O(n)    | O(n)

### Best Practices
1. Tree Traversal:
   - Know all three DFS traversals
   - Understand when to use BFS vs DFS
   - Practice both recursive and iterative solutions

2. Problem Solving:
   - Consider both recursive and iterative approaches
   - Watch for balanced tree requirements
   - Handle edge cases (empty tree, single node)
   - Think about space complexity

3. Common Patterns:
   - Top-down vs Bottom-up recursion
   - Level-order processing
   - Path finding
   - Tree construction

4. Optimization Tips:
   - Use height-balanced trees for better performance
   - Consider iterative solutions for better space complexity
   - Use appropriate tree type (BST, AVL, Red-Black)
   - Implement efficient tree operations

Remember:
- Always validate tree properties
- Consider edge cases
- Think about balanced vs unbalanced scenarios
- Know the trade-offs between different tree types
- Practice tree problems both recursively and iteratively
