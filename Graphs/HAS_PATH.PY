from typing import Dict, List

# Define the graph as a dictionary where keys are nodes and values are lists of connected nodes
graph: Dict[str, List[str]] = {
    'f': ['g', 'i'],
    'g': ['h'],
    'h': [],
    'i': ['g', 'k'],
    'j': ['i'],
    'k': []
}

def has_path(graph: Dict[str, List[str]], start: str, end: str) -> bool:
    """
    Determines if there is a path between two nodes in a directed graph.

    This function implements a depth-first search (DFS) to check if a path exists 
    from the start node to the end node.

    Args:
        graph (Dict[str, List[str]]): A directed graph represented as an adjacency list.
                                      Each key is a node, and its value is a list of nodes it points to.
        start (str): The starting node of the path.
        end (str): The target node of the path.

    Returns:
        bool: True if a path exists from start to end, False otherwise.
    """
    # Base case: if the start and end nodes are the same, a path exists
    
    if start not in graph or end not in graph:
      raise ValueError("Start or end node not found in graph")

    if start == end:
        return True

    # Recursively explore each neighbor of the start node
    for neighbor in graph[start]:
        if has_path(graph, neighbor, end):
            return True

    # If no path is found, return False
    return False

# Test cases
if __name__ == "__main__":
    # Test 1: Path exists from 'f' to 'k'
    assert has_path(graph, 'f', 'k') == True, "Test 1 Failed"

    # Test 2: Path does not exist from 'f' to 'j'
    assert has_path(graph, 'f', 'j') == False, "Test 2 Failed"

    # Test 3: Path exists from 'j' to 'k'
    assert has_path(graph, 'j', 'k') == True, "Test 3 Failed"

    # Test 4: Path does not exist from 'k' to 'f' (no reverse path)
    assert has_path(graph, 'k', 'f') == False, "Test 4 Failed"

    # Test 5: Path exists from 'g' to 'h'
    assert has_path(graph, 'g', 'h') == True, "Test 5 Failed"

    # Test 6: Path does not exist from 'h' to any other node
    assert has_path(graph, 'h', 'g') == False, "Test 6 Failed"

    # Test 7: Path exists from a node to itself (trivial case)
    assert has_path(graph, 'f', 'f') == True, "Test 7 Failed"

    print("All tests passed!")
