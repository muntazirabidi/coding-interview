from typing import Dict, List, Union, Set


def buildGraph(edges: List[List[str]]) -> Dict[str, List[str]]:
    """
    Builds a graph from a list of edges.

    Args:
        edges (List[List[str]]): A list of edges where each edge is represented as a pair of nodes.

    Returns:
        Dict[str, List[str]]: An adjacency list representation of the graph.
    """
    graph: Dict[str, List[str]] = {}
    
    for edge in edges:
        a, b = edge
        if a not in graph:
            graph[a] = []
        if b not in graph:
            graph[b] = []
        graph[a].append(b)
        graph[b].append(a)
        
    return graph


def shortestPath(edges: List[List[str]], start: str, end: str) -> int:
    """
    Finds the shortest distance between two nodes in an undirected graph.

    Args:
        edges (List[List[str]]): A list of edges where each edge is represented as a pair of nodes.
        start (str): The starting node.
        end (str): The target node.

    Returns:
        int: The shortest distance between the start and end nodes, or -1 if no path exists.
    """
    graph = buildGraph(edges)
    visited: Set[str] = set()
    queue: List[Union[str, int]] = [[start, 0]]  # Queue stores [node, distance]
    
    while queue:
        node, distance = queue.pop(0)
        
        if node == end:
            return distance
        
        for neighbor in graph[node]:
            if neighbor not in visited:
                visited.add(neighbor)
                queue.append([neighbor, distance + 1])
                
    return -1  # Return -1 if no path exists


if __name__ == '__main__':
    edges = [
        ['w', 'x'],
        ['x', 'y'],
        ['z', 'y'],
        ['z', 'v'],
        ['w', 'v']
    ]

    # Test Cases
    print(shortestPath(edges, 'w', 'z'))  # Expected Output: 2
    print(shortestPath(edges, 'w', 'y'))  # Expected Output: 2
    print(shortestPath(edges, 'z', 'x'))  # Expected Output: 2
    print(shortestPath(edges, 'x', 'v'))  # Expected Output: 1
    print(shortestPath(edges, 'w', 'a'))  # Expected Output: -1 (no path exists)
