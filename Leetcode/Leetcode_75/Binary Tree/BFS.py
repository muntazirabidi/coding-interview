from collections import deque

def bfs(root):
    if not root:
        return []
        
    result = []
    queue = deque([root])
    
    while queue:
        node = queue.popleft()  # Get next node
        result.append(node.val)  # Process node
        
        # Add children to queue
        if node.left:
            queue.append(node.left)
        if node.right:
            queue.append(node.right)
            
    return result