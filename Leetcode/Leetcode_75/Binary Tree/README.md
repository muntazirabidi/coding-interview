# Solving Tree-Based Problems

## 1. Core Tree Traversal Patterns

### DFS (Depth-First Search) Traversals

#### Preorder (Root -> Left -> Right)

```python
def preorder(root):
    if not root:
        return
    print(root.val)      # Process root
    preorder(root.left)  # Process left subtree
    preorder(root.right) # Process right subtree
```

#### Inorder (Left -> Root -> Right)

```python
def inorder(root):
    if not root:
        return
    inorder(root.left)   # Process left subtree
    print(root.val)      # Process root
    inorder(root.right)  # Process right subtree
```

#### Postorder (Left -> Right -> Root)

```python
def postorder(root):
    if not root:
        return
    postorder(root.left)  # Process left subtree
    postorder(root.right) # Process right subtree
    print(root.val)       # Process root
```

### BFS (Breadth-First Search)

```python
from collections import deque

def levelOrder(root):
    if not root:
        return
    queue = deque([root])
    while queue:
        node = queue.popleft()
        print(node.val)
        if node.left:
            queue.append(node.left)
        if node.right:
            queue.append(node.right)
```

## 2. Problem-Solving Approaches

### A. Top-Down Approach

- Similar to preorder traversal
- Passes information from parent to children
- Good for path-related problems

```python
def top_down(root, params):
    if not root:
        return

    # Process current node using parameters from parent
    process_node(root, params)

    # Pass updated parameters to children
    top_down(root.left, new_params)
    top_down(root.right, new_params)
```

### B. Bottom-Up Approach

- Similar to postorder traversal
- Collects information from children first
- Good for subtree-related problems

```python
def bottom_up(root):
    if not root:
        return result

    # Get results from children
    left_result = bottom_up(root.left)
    right_result = bottom_up(root.right)

    # Process current node using children's results
    return process_results(left_result, right_result, root)
```

## 3. Common Problem-Solving Patterns

### Path Tracking

```python
def find_paths(root):
    def dfs(node, current_path):
        if not node:
            return

        current_path.append(node.val)

        # Process path at leaf
        if not node.left and not node.right:
            process_path(current_path)

        dfs(node.left, current_path)
        dfs(node.right, current_path)
        current_path.pop()  # Backtrack

    dfs(root, [])
```

### Level Processing

```python
def process_levels(root):
    if not root:
        return
    queue = deque([(root, 0)])  # (node, level)

    while queue:
        node, level = queue.popleft()
        process_node_at_level(node, level)

        if node.left:
            queue.append((node.left, level + 1))
        if node.right:
            queue.append((node.right, level + 1))
```

### Global State Management

```python
def tree_problem(root):
    results = []  # or other data structure

    def dfs(node):
        if not node:
            return
        # Process and update results
        results.append(node.val)
        dfs(node.left)
        dfs(node.right)

    dfs(root)
    return results
```

## 4. Key Considerations

### Base Cases

- Empty node (`if not root: return`)
- Leaf node (`if not root.left and not root.right`)
- Single child (`if not root.left or not root.right`)

### Time/Space Complexity

- Most tree solutions:
  - Time: O(n) where n is number of nodes
  - Space: O(h) where h is height of tree
- BFS Space: O(w) where w is maximum width of tree
- Path collection: Space O(n) in worst case

### Common Pitfalls

1. Forgetting to handle empty trees
2. Not considering single-child cases
3. Improper backtracking in path problems
4. Modifying global state without resetting
5. Not handling negative values when relevant

## 5. Problem Categories and Approaches

### Path Problems

- Use DFS with path tracking
- Consider backtracking when necessary
- Track running sums/conditions

### Structure Problems

- Use Bottom-up approach
- Compare left and right subtrees
- Consider symmetry cases

### Level-based Problems

- Use BFS
- Track level information
- Consider level-specific operations

### Search Problems

- Choose between DFS/BFS based on tree shape
- Consider BST properties if applicable
- Use early termination when possible

## 6. Testing Strategy

1. Test cases should include:

   - Empty tree
   - Single node
   - Left/right skewed trees
   - Perfect binary trees
   - Unbalanced trees
   - Negative values (if applicable)

2. Edge cases to consider:
   - Maximum/minimum values
   - Duplicate values
   - Deep trees
   - Wide trees
   - Single-child nodes
