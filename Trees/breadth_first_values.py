from node import Node

def breadth_first_values(root):
    """
    Generates a breadth-first sequence of the values in a binary tree.

    Args:
        root (Node): The root node of the binary tree.

    Returns:
        list: The breadth-first sequence of values.
    """
    if root is None: return []

    result = []
    queue = [root]

    while queue: 
      current = queue.pop(0)
      result.append(current.data)
      
      if current.left:
        queue.append(current.left)
      if current.right:
        queue.append(current.right)
        
    return result
        
      
      


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
    print(breadth_first_values(root_node))
