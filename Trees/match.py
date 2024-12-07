from node import Node


def match(root, target):
    """
    Performs a breadth-first search to determine if the target value exists in the binary tree.

    Args:
        root (Node): The root node of the binary tree.
        target (str): The value to search for in the binary tree.

    Returns:
        bool: True if the target value is found, False otherwise.

    Raises:
        TypeError: If `root` is not an instance of Node or None.
        ValueError: If `target` is not a string.
    """
    # Validate root
    if root is not None and not isinstance(root, Node):
        raise TypeError("The root must be an instance of Node or None.")

    # Validate target
    if not isinstance(target, str):
        raise ValueError("The target must be a string.")

    if not root:
        return False

    queue = [root]

    while queue:
        current = queue.pop(0)

        # Handle potential attribute access issues
        if not hasattr(current, 'data'):
            raise AttributeError(f"Node {current} does not have a 'data' attribute.")

        if current.data == target:
            return True

        if current.left:
            queue.append(current.left)
        if current.right:
            queue.append(current.right)

    return False

def match_recursive(root, target):
  if root is None: return False
  if root.data == target: return True
  
  return match_recursive(root.left, target) or match_recursive(root.right, target)

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


if __name__ == '__main__':
    try:
        # Build the sample tree and search for the target value
        target = 'e'
        root_node = build_sample_tree()
        result = match(root_node, target)
        print(f"BFS: Target '{target}' found in tree: {result}")
        result = match_recursive(root_node, target)
        print(f"DFS: Target '{target}' found in tree: {result}")
    except (TypeError, ValueError, AttributeError) as error:
        print(f"Error: {error}")
