from node import Node


def depth_first_values(root):
    """
    Performs a depth-first traversal of a binary tree and prints node values.

    Args:
        root (Node): The root node of the binary tree.

    Returns:
        None
    """
    if root is None:
        return

    stack = [root]

    while stack:
        current = stack.pop()
        print(current.data)

        if current.right:
            stack.append(current.right)
        if current.left:
            stack.append(current.left)


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
    # Build the sample tree and perform depth-first traversal
    root_node = build_sample_tree()
    depth_first_values(root_node)