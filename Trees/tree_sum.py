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
    f = Node(1)

    # Establish relationships
    a.left = b
    a.right = c
    b.left = d
    b.right = e
    c.right = f

    return a

def tree_sum(root):
  if root is None: return 0
  
  left = tree_sum(root.left)
  right = tree_sum(root.right)
  
  return root.data + left + right



if __name__ == '__main__':
    # Build the sample tree and perform depth-first traversal
    root_node = build_sample_tree()
    result = tree_sum(root_node)
    print(f"Total Sum  = {result}")