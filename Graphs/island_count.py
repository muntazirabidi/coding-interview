from typing import List, Set, Tuple


def island_count(grid: List[List[str]]) -> int:
    """
    Counts the number of islands in a grid.

    Args:
        grid (List[List[str]]): A 2D grid of characters representing land ('L') and water ('W').

    Returns:
        int: The number of islands in the grid.
    """
    visited: Set[Tuple[int, int]] = set()  # Keeps track of visited cells
    count: int = 0 

    for row in range(len(grid)):
        for col in range(len(grid[0])):
            # If the cell is 'L' and not visited, it's a new island
            if grid[row][col] == 'L' and (row, col) not in visited:
                if explore(grid, row, col, visited):  # Explore the island
                    count += 1 
    
    return count


def explore(grid: List[List[str]], row: int, col: int, visited: Set[Tuple[int, int]]) -> bool:
    """
    Explores the connected land cells of an island using Depth-First Search (DFS).

    Args:
        grid (List[List[str]]): The grid.
        row (int): Current row index.
        col (int): Current column index.
        visited (Set[Tuple[int, int]]): Set of visited cells.

    Returns:
        bool: True if a new island is found and explored, False otherwise.
    """
    # Check bounds and if the cell is water or already visited
    if row < 0 or row >= len(grid) or col < 0 or col >= len(grid[0]):
        return False
    if grid[row][col] == 'W' or (row, col) in visited:
        return False

    visited.add((row, col))

    explore(grid, row - 1, col, visited)  # Up
    explore(grid, row + 1, col, visited)  # Down
    explore(grid, row, col - 1, visited)  # Left
    explore(grid, row, col + 1, visited)  # Right

    return True  


if __name__ == "__main__":
    grid: List[List[str]] = [
        ['W', 'L', 'W', 'W', 'W'],
        ['W', 'L', 'W', 'W', 'W'],
        ['W', 'W', 'W', 'L', 'W'],
        ['W', 'W', 'L', 'L', 'W'],
        ['L', 'W', 'W', 'L', 'L'],
        ['L', 'L', 'W', 'W', 'W'],
    ]
    
    print(island_count(grid))  # Expected Output: 4
