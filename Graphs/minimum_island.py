from typing import List, Set, Tuple


def minimumIsland(grid: List[List[str]]) -> int:
    """
    Finds the size of the smallest island (connected land component) in a 2D grid.

    Args:
        grid (List[List[str]]): A 2D grid where 'L' represents land and 'W' represents water.

    Returns:
        int: The size of the smallest island. If no islands are present, returns 0.
    """
    visited: Set[Tuple[int, int]] = set()
    min_size: int = float('inf')  # Start with infinity to find the smallest island

    for row in range(len(grid)):
        for col in range(len(grid[0])):
            # If the cell is 'L' and not visited, it's a new island
            if grid[row][col] == 'L' and (row, col) not in visited:
                current_size = explore(grid, row, col, visited)
                if current_size < min_size:
                    min_size = current_size

    # If no islands were found, return 0 instead of infinity
    return min_size if min_size != float('inf') else 0


def explore(grid: List[List[str]], row: int, col: int, visited: Set[Tuple[int, int]]) -> int:
    """
    Explores all connected land cells ('L') in the grid using Depth-First Search (DFS).

    Args:
        grid (List[List[str]]): The 2D grid.
        row (int): Current row index.
        col (int): Current column index.
        visited (Set[Tuple[int, int]]): Set of visited cells.

    Returns:
        int: The size of the connected component (island).
    """
    # Check bounds and if the cell is water or already visited
    if row < 0 or row >= len(grid) or col < 0 or col >= len(grid[0]):
        return 0
    if grid[row][col] == 'W' or (row, col) in visited:
        return 0

    visited.add((row, col))  # Mark the cell as visited

    size: int = 1  # Start counting the current cell as part of the island

    # Recursively explore all neighboring cells
    size += explore(grid, row - 1, col, visited)  # Up
    size += explore(grid, row + 1, col, visited)  # Down
    size += explore(grid, row, col - 1, visited)  # Left
    size += explore(grid, row, col + 1, visited)  # Right

    return size


# Test cases
if __name__ == "__main__":
    # Example Grid
    grid: List[List[str]] = [
        ['W', 'L', 'W', 'W', 'W'],
        ['W', 'L', 'W', 'W', 'W'],
        ['W', 'W', 'W', 'L', 'W'],
        ['W', 'W', 'L', 'L', 'W'],
        ['L', 'W', 'W', 'L', 'L'],
        ['L', 'L', 'W', 'W', 'W'],
    ]

    print(minimumIsland(grid))  # Expected Output: 2


    # Additional Test Cases
    test_grids = [
        ([
            ['W', 'W', 'W'],
            ['W', 'L', 'W'],
            ['W', 'W', 'W']
        ], 1),  # Single land cell

        ([
            ['W', 'W', 'W'],
            ['W', 'W', 'W'],
            ['W', 'W', 'W']
        ], 0),  # No islands

        ([
            ['L', 'L', 'W'],
            ['L', 'L', 'W'],
            ['W', 'W', 'L']
        ], 1),  # Smallest island is size 1

        ([
            ['L', 'W', 'W'],
            ['W', 'L', 'W'],
            ['W', 'W', 'L']
        ], 1),  # Three separate islands, each size 1
    ]

    for idx, (test_grid, expected) in enumerate(test_grids, 1):
        result = minimumIsland(test_grid)
        assert result == expected, f"Test Case {idx} Failed: Expected {expected}, Got {result}"
        print(f"Test Case {idx} Passed!")
