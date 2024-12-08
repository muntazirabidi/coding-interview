import unittest
from typing import List, Set
from nqueens import Solution, NQueensError

class TestNQueensSolution(unittest.TestCase):
    """Test suite for the N-Queens problem solution."""
    
    def setUp(self):
        """Initialize the Solution class before each test."""
        self.solution = Solution()

    def is_valid_solution(self, board: List[str], n: int) -> bool:
        """
        Validate if a given board configuration is a valid N-Queens solution.
        
        Args:
            board (List[str]): The board configuration to validate
            n (int): The size of the board
            
        Returns:
            bool: True if the configuration is valid, False otherwise
        """
        # Convert board strings to 2D list for easier processing
        board_2d = [[char for char in row] for row in board]
        
        # Check number of queens
        queen_count = sum(row.count('Q') for row in board_2d)
        if queen_count != n:
            return False
            
        # Track occupied positions
        columns: Set[int] = set()
        positive_diagonals: Set[int] = set()
        negative_diagonals: Set[int] = set()
        
        # Check each position
        for row in range(n):
            for col in range(n):
                if board_2d[row][col] == 'Q':
                    # Check if queen position conflicts with existing queens
                    if (col in columns or 
                        (row + col) in positive_diagonals or 
                        (row - col) in negative_diagonals):
                        return False
                    
                    # Add queen position to tracking sets
                    columns.add(col)
                    positive_diagonals.add(row + col)
                    negative_diagonals.add(row - col)
        
        return True

    def test_invalid_inputs(self):
        """Test handling of invalid inputs."""
        # Test negative board size
        with self.assertRaises(NQueensError):
            self.solution.solveNQueens(-1)
        
        # Test zero board size
        with self.assertRaises(NQueensError):
            self.solution.solveNQueens(0)
        
        # Test non-integer input
        with self.assertRaises(ValueError):
            self.solution.solveNQueens(3.5)
        
        # Test string input
        with self.assertRaises(ValueError):
            self.solution.solveNQueens("4")

    def test_small_boards(self):
        """Test solutions for small board sizes."""
        # Test 1x1 board
        result = self.solution.solveNQueens(1)
        self.assertEqual(len(result), 1)
        self.assertEqual(result[0], ["Q"])
        
        # Test 2x2 board (no solution possible)
        result = self.solution.solveNQueens(2)
        self.assertEqual(len(result), 0)
        
        # Test 3x3 board (no solution possible)
        result = self.solution.solveNQueens(3)
        self.assertEqual(len(result), 0)

    def test_4x4_board(self):
        """Test the classic 4x4 board case."""
        result = self.solution.solveNQueens(4)
        
        # Verify number of solutions
        self.assertEqual(len(result), 2)
        
        # Verify each solution is valid
        for solution in result:
            self.assertEqual(len(solution), 4)  # Correct number of rows
            self.assertTrue(all(len(row) == 4 for row in solution))  # Correct row lengths
            self.assertTrue(self.is_valid_solution(solution, 4))
            
        # Verify solutions match known patterns
        expected_solutions = [
            [".Q..", "...Q", "Q...", "..Q."],
            ["..Q.", "Q...", "...Q", ".Q.."]
        ]
        self.assertEqual(sorted(result), sorted(expected_solutions))

    def test_large_board(self):
        """Test solution for a larger board (6x6)."""
        result = self.solution.solveNQueens(6)
        
        # Verify solutions exist
        self.assertGreater(len(result), 0)
        
        # Verify each solution is valid
        for solution in result:
            self.assertEqual(len(solution), 6)  # Correct number of rows
            self.assertTrue(all(len(row) == 6 for row in solution))  # Correct row lengths
            self.assertTrue(self.is_valid_solution(solution, 6))
            
        # Known number of solutions for 6x6 board is 4
        self.assertEqual(len(result), 4)

    def test_solution_properties(self):
        """Test general properties that should hold for any valid solution."""
        n = 5
        result = self.solution.solveNQueens(n)
        
        for solution in result:
            # Test row count
            self.assertEqual(len(solution), n)
            
            # Test column count in each row
            for row in solution:
                self.assertEqual(len(row), n)
            
            # Test queen count
            total_queens = sum(row.count('Q') for row in solution)
            self.assertEqual(total_queens, n)
            
            # Test each row has exactly one queen
            for row in solution:
                self.assertEqual(row.count('Q'), 1)
            
            # Test each column has exactly one queen
            for col in range(n):
                queens_in_col = sum(row[col] == 'Q' for row in solution)
                self.assertEqual(queens_in_col, 1)

    def test_solution_uniqueness(self):
        """Test that all returned solutions are unique."""
        for n in range(1, 6):  # Test boards from 1x1 to 5x5
            result = self.solution.solveNQueens(n)
            # Convert solutions to tuples for hashability
            solution_set = set(tuple(solution) for solution in result)
            self.assertEqual(len(solution_set), len(result))

if __name__ == '__main__':
    unittest.main(verbosity=2)