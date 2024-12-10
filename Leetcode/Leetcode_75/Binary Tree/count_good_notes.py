'''
Given a binary tree root, a node X in the tree is named good if in the path from root to X there are no nodes with a value greater than X.

Return the number of good nodes in the binary tree.

'''

# Definition for a binary tree node.
class TreeNode:
    def __init__(self, val=0, left=None, right=None):
        self.val = val
        self.left = left
        self.right = right
        
class Solution:
    def goodNodes(self, root: TreeNode) -> int:
        def count_good_nodes(node: Optional[TreeNode], max_so_far: int) -> int:
            if not node: return 0

            current_count = 1 if node.val >= max_so_far else 0

            new_max = max(max_so_far, node.val)

            left_count = count_good_nodes(node.left, new_max)
            right_count = count_good_nodes(node.right, new_max)

            return current_count + left_count + right_count

        return count_good_nodes(root, root.val)


        