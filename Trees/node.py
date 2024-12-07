class Node:
    """
    Represents a node in a binary tree.

    Attributes:
        data: The value or data stored in the node.
        left (Node): The left child node.
        right (Node): The right child node.
    """

    def __init__(self, data):
        """
        Initializes a new Node.

        Args:
            data: The value or data to be stored in the node.
        """
        self.data = data
        self.left = None
        self.right = None


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
