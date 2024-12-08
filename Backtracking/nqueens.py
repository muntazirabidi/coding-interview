class Solution:
    def solveNQueens(self, n: int) -> List[List[str]]:
        # Issue 1: All class methods should be properly indented
        columns = set()
        positive_diagonal = set()  # (r + c)
        negative_diagonal = set()  # (r - c)
        result = []
        board = [['.']*n for i in range(n)]
        
        # Issue 2: The backtrack function needs to be indented as it's inside solveNQueens
        def backtrack(row):
            # Issue 3: 'rown' was a typo - should be 'row'
            if row == n:
                copy = [''.join(row) for row in board]
                result.append(copy)
                return
                
            for col in range(n):
                if col in columns or (row + col) in positive_diagonal or (row - col) in negative_diagonal:
                    continue
                    
                columns.add(col)
                positive_diagonal.add(row + col)
                negative_diagonal.add(row - col)
                board[row][col] = 'Q'
                
                backtrack(row + 1)
                
                columns.remove(col)
                positive_diagonal.remove(row + col)
                negative_diagonal.remove(row - col)
                board[row][col] = '.'
        
        # Issue 4: This line needs to be indented to be part of solveNQueens
        backtrack(0)
        return result