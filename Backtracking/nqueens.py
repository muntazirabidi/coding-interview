from typing import List, Set, Optional
from dataclasses import dataclass

@dataclass
class ChessBoard:
    """Represents a chess board configuration for the N-Queens problem."""
    size: int
    board: List[List[str]]

class NQueensError(Exception):
    """Custom exception for N-Queens problem-specific errors."""
    pass

class Solution:
    """
    A solution class for solving the N-Queens problem using backtracking.
    
    The N-Queens problem involves placing N chess queens on an N×N chessboard 
    such that no two queens threaten each other, meaning no two queens share 
    the same row, column, or diagonal.
    """
    
    def solveNQueens(self, n: int) -> List[List[str]]:
        """
        Finds all valid solutions for placing N queens on an N×N chessboard.
        
        Args:
            n (int): The size of the board and number of queens to place.
            
        Returns:
            List[List[str]]: A list of all valid board configurations, where each
                            configuration is represented as a list of strings.
                            Each string represents a row, with '.' for empty squares
                            and 'Q' for queens.
                            
        Raises:
            NQueensError: If n is less than 1.
            ValueError: If n is not an integer.
        """
        if not isinstance(n, int):
            raise ValueError("Board size must be an integer")
        if n < 1:
            raise NQueensError("Board size must be at least 1")
            
        # Initialize sets to track occupied positions
        columns: Set[int] = set()
        positive_diagonal: Set[int] = set()  # (r + c)
        negative_diagonal: Set[int] = set()  # (r - c)
        result: List[List[str]] = []
        board: List[List[str]] = [['.']*n for _ in range(n)]
        
        def backtrack(row: int) -> None:
            """
            Recursive helper function that implements the backtracking algorithm.
            
            Args:
                row (int): The current row being processed.
                
            Side Effects:
                Modifies the result list by adding valid solutions when found.
                Modifies the board and tracking sets during exploration.
            """
            # Base case: if we've placed queens in all rows, we've found a solution
            if row == n:
                # Create a deep copy of the current valid solution
                copy: List[str] = [''.join(row) for row in board]
                result.append(copy)
                return
            
            # Try placing a queen in each column of the current row
            for col in range(n):
                # Calculate diagonal positions
                curr_positive_diagonal: int = row + col
                curr_negative_diagonal: int = row - col
                
                # Check if current position is under attack
                if (col in columns or 
                    curr_positive_diagonal in positive_diagonal or 
                    curr_negative_diagonal in negative_diagonal):
                    continue
                
                try:
                    # Place queen and update tracking sets
                    columns.add(col)
                    positive_diagonal.add(curr_positive_diagonal)
                    negative_diagonal.add(curr_negative_diagonal)
                    board[row][col] = 'Q'
                    
                    # Recurse to next row
                    backtrack(row + 1)
                    
                finally:
                    # Backtrack: remove queen and clean up tracking sets
                    columns.remove(col)
                    positive_diagonal.remove(curr_positive_diagonal)
                    negative_diagonal.remove(curr_negative_diagonal)
                    board[row][col] = '.'
        
        # Start backtracking from the first row
        backtrack(0)
        return result