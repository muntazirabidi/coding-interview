from typing import Dict, List, Set, Union


def largestComponent(graph: Dict[Union[str, int], List[Union[str, int]]]) -> int:
    """
    Finds the size of the largest connected component in an undirected graph.

    Args:
        graph (Dict[Union[str, int], List[Union[str, int]]]): The adjacency list representation of the graph.

    Returns:
        int: The size of the largest connected component in the graph.
    """
    visited: Set[Union[str, int]] = set()
    max_size: int = 0

    for node in graph:
        size = explore(graph, node, visited)  # Corrected argument order
        if size > max_size:
            max_size = size

    return max_size


def explore(graph: Dict[Union[str, int], List[Union[str, int]]], current: Union[str, int], visited: Set[Union[str, int]]) -> int:
    """
    Explores all nodes connected to the current node using Depth-First Search (DFS).

    Args:
        graph (Dict[Union[str, int], List[Union[str, int]]]): The adjacency list representation of the graph.
        current (Union[str, int]): The node currently being explored.
        visited (Set[Union[str, int]]): A set to track visited nodes.

    Returns:
        int: The size of the connected component containing the current node.
    """
    if current in visited:
        return 0

    visited.add(current)

    size: int = 1

    for neighbor in graph[current]:
        size += explore(graph, neighbor, visited)

    return size


if __name__ == "__main__":
    # Test Case 1: Standard graph with two components
    graph1 = {
        0: [8, 1, 5],
        1: [0],
        5: [0, 8],
        8: [0, 5],
        2: [3, 4],
        3: [2, 4],
        4: [3, 2]
    }
    print(largestComponent(graph1))  # Expected Output: 4 (Component: {0, 1, 5, 8})

    # Test Case 2: Graph with isolated nodes
    graph2 = {
        0: [1],
        1: [0],
        2: [],
        3: [],
        4: [5],
        5: [4]
    }
    print(largestComponent(graph2))  # Expected Output: 2 (Component: {4, 5})

    # Test Case 3: Fully connected graph
    graph3 = {
        0: [1, 2, 3],
        1: [0, 2, 3],
        2: [0, 1, 3],
        3: [0, 1, 2]
    }
    print(largestComponent(graph3))  # Expected Output: 4 (Component: {0, 1, 2, 3})

    # Test Case 4: Empty graph
    graph4 = {}
    print(largestComponent(graph4))  # Expected Output: 0 (No components)

    # Test Case 5: Single-node graph
    graph5 = {0: []}
    print(largestComponent(graph5))  # Expected Output: 1 (Component: {0})
