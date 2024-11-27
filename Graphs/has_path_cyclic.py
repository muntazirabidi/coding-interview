from typing import Dict, List, Set

# Define the graph as a dictionary where keys are nodes and values are lists of connected nodes
edges: List[List[str]] = [
    ['i', 'j'], 
    ['k', 'i'],
    ['m', 'k'],
    ['k', 'l'],
    ['o', 'n']
]

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
        if a not in graph: graph[a] = []
        if b not in graph: graph[b] = []
        graph[a].append(b)
        graph[b].append(a)
        
    return graph

def has_path(graph: Dict[str, List[str]], start: str, end: str, visited: Set[str] = None) -> bool:
    """
    Determines if there is a path between two nodes in an undirected graph.

    This function implements a depth-first search (DFS) to check if a path exists 
    from the start node to the end node.

    Args:
        graph (Dict[str, List[str]]): An undirected graph represented as an adjacency list.
                                      Each key is a node, and its value is a list of nodes it connects to.
        start (str): The starting node of the path.
        end (str): The target node of the path.
        visited (Set[str], optional): A set to track visited nodes to prevent revisiting.

    Returns:
        bool: True if a path exists from start to end, False otherwise.
    """
    if start not in graph or end not in graph:
        raise ValueError("Start or end node not found in graph")
    
    # Base case: if the start and end nodes are the same, a path exists
    if start == end: return True
    
    if visited is None: visited = set()
    
    if start in visited: return False
    
    visited.add(start)

    # Recursively explore each neighbor of the start node
    for neighbor in graph[start]:
        if has_path(graph, neighbor, end, visited):
            return True

    return False

def undirectedPath(edges: List[List[str]], nodeA: str, nodeB: str) -> bool:
    """
    Determines if a path exists between two nodes in an undirected graph.

    Args:
        edges (List[List[str]]): A list of edges representing the graph.
        nodeA (str): The starting node.
        nodeB (str): The target node.

    Returns:
        bool: True if a path exists between nodeA and nodeB, False otherwise.
    """
    graph = buildGraph(edges)
    return has_path(graph, nodeA, nodeB, set())

# Example Usage and Testing
if __name__ == "__main__":
    print(buildGraph(edges))  # Prints the adjacency list representation of the graph

    # Test undirectedPath
    print(undirectedPath(edges, 'i', 'l'))  # Expected: True
    print(undirectedPath(edges, 'i', 'o'))  # Expected: False
    print(undirectedPath(edges, 'k', 'm'))  # Expected: True
    print(undirectedPath(edges, 'n', 'o'))  # Expected: True
