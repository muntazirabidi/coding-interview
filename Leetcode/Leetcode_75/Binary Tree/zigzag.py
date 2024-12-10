'''
You are given the root of a binary tree.

A ZigZag path for a binary tree is defined as follow:

Choose any node in the binary tree and a direction (right or left).
If the current direction is right, move to the right child of the current node; otherwise, move to the left child.
Change the direction from right to left or from left to right.
Repeat the second and third steps until you can't move in the tree.
Zigzag length is defined as the number of nodes visited - 1. (A single node has a length of 0).

Return the longest ZigZag path contained in that tree.
'''


from typing import Optional

class TreeNode:
    def __init__(self, val=0, left=None, right=None):
        self.val = val
        self.left = left
        self.right = right

class Solution:
    def longestZigZag(self, root: Optional[TreeNode]) -> int:
        # Initialize max length
        self.max_length = 0
        
        def dfs(node: Optional[TreeNode], going_left: bool, length: int) -> None:
            if not node:
                return
            
            # Update global max length
            self.max_length = max(self.max_length, length)
            
            # If we're going left, we have two choices:
                # 1. Continue zigzag by going right
                # 2. Start new zigzag by going left
            if going_left:
                # Continue zigzag by going right
                dfs(node.right, False, length + 1)
                # Start new zigzag by going left
                dfs(node.left, True, 1)
            else:
                # Continue zigzag by going left
                dfs(node.left, True, length + 1)
                # Start new zigzag by going right
                dfs(node.right, False, 1)
        
        # Start zigzag paths from root in both directions
        if root:
            dfs(root.left, True, 1) 
            dfs(root.right, False, 1) 
        
        return self.max_length