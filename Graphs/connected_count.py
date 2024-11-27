from typing import Dict, List, Set, Union


def connected_count(graph: Dict[Union[str, int], List[Union[str, int]]]) -> int:
    """
    Counts the number of connected components in an undirected graph.

    Args:
        graph (Dict[Union[str, int], List[Union[str, int]]]): The adjacency list representation of the graph.

    Returns:
        int: The number of connected components in the graph.
    """
    visited: Set[Union[str, int]] = set()
    count: int = 0

    for node in graph:
        if explore(graph, node, visited):
            count += 1

    return count


def explore(graph: Dict[Union[str, int], List[Union[str, int]]], current: Union[str, int], visited: Set[Union[str, int]]) -> bool:
    """
    Explores all nodes connected to the current node using Depth-First Search (DFS).

    Args:
        graph (Dict[Union[str, int], List[Union[str, int]]]): The adjacency list representation of the graph.
        current (Union[str, int]): The node currently being explored.
        visited (Set[Union[str, int]]): A set to track visited nodes.

    Returns:
        bool: True if the current node is part of a new connected component, False otherwise.
    """
    if current in visited:
        return False

    visited.add(current)

    for neighbor in graph[current]:
        explore(graph, neighbor, visited)

    return True


# Test cases for the connected_count function
def test_connected_count():
    # Test Case 1: Graph with three connected components (string keys)
    graph1 = {
        'a': ['b'],
        'b': ['a'],
        'c': ['d'],
        'd': ['c'],
        'e': []
    }
    assert connected_count(graph1) == 3, "Test Case 1 Failed"

    # Test Case 2: Fully connected graph (string keys)
    graph2 = {
        'a': ['b', 'c'],
        'b': ['a', 'c'],
        'c': ['a', 'b']
    }
    assert connected_count(graph2) == 1, "Test Case 2 Failed"

    # Test Case 3: Graph with integer keys
    graph3 = {
        1: [2],
        2: [1],
        3: [4],
        4: [3],
        5: []
    }
    assert connected_count(graph3) == 3, "Test Case 3 Failed"

    # Test Case 4: Single-node graph (integer key)
    graph4 = {
        1: []
    }
    assert connected_count(graph4) == 1, "Test Case 4 Failed"

    # Test Case 5: Mixed type keys (string and integer)
    graph5 = {
        'a': [1],
        1: ['a', 2],
        2: [1]
    }
    assert connected_count(graph5) == 1, "Test Case 5 Failed"

    # Test Case 6: Empty graph
    graph6 = {}
    assert connected_count(graph6) == 0, "Test Case 6 Failed"

    print("All test cases passed!")


# Example Usage and Test Cases
if __name__ == "__main__":
    test_connected_count()
    
    graph = {
        'a': ['b'],
        'b': ['a'],
        'c': ['d'],
        'd': ['c'],
        'e': []
    }

    print(connected_count(graph))  # Expected Output: 3
