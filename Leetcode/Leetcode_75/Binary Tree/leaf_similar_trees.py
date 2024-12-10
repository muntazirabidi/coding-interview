'''
Consider all the leaves of a binary tree, from left to right order, the values of those leaves form a leaf value sequence.
'''

from typing import Optional, List

class TreeNode:
    def __init__(self, val: int = 0, left: Optional['TreeNode'] = None, right: Optional['TreeNode'] = None):
        self.val = val
        self.left = left
        self.right = right

class Solution:
    def leafSimilar(self, root1: Optional[TreeNode], root2: Optional[TreeNode]) -> bool:
        def get_leaves(root: Optional[TreeNode], leaves: List[int]) -> None:
            if not root:
                return
            
            if not root.left and not root.right:
                leaves.append(root.val)
                return
            
            get_leaves(root.left, leaves)
            get_leaves(root.right, leaves)
        
        leaves1: List[int] = []
        leaves2: List[int] = []
        get_leaves(root1, leaves1)
        get_leaves(root2, leaves2)
        
        return leaves1 == leaves2