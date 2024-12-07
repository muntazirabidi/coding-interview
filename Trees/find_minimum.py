from node import Node 

def build_sample_tree():
    """
    Creates and returns a sample binary tree for testing.

    Returns:
        Node: The root node of the binary tree.
    """
    # Create nodes
    a = Node(3)
    b = Node(11)
    c = Node(4)
    d = Node(4)
    e = Node(2)
    f = Node(10)

    # Establish relationships
    a.left = b
    a.right = c
    b.left = d
    b.right = e
    c.right = f

    return a

def find_minimum(root):
  if root is not None and not isinstance(root, Node):
    raise TypeError("The root must be an instance of Node or None.")
  
  if root is None: return float('inf')
    
  left = find_minimum(root.left)
  right = find_minimum(root.right)
    
  return min(root.data, left, right)



if __name__ == '__main__':
  try:
    # Build the sample tree and perform depth-first traversal
    root_node = build_sample_tree()
    find_minimum(root_node)
    print(f"Minimum value in the tree = {find_minimum(root_node)}")
  except Exception as e:
    print(e)
    