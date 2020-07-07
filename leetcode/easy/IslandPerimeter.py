from typing import List


class Solution:
    def islandPerimeter(self, grid: List[List[int]]) -> int:
        row, column, result = len(grid), len(grid[0]), 0
        for row_index in range(row):
            for column_index in range(column):
                if grid[row_index][column_index] == 1:
                    result += self.calculate(grid, row_index, column_index)
        return result

    def calculate(self, grid: List[List[int]], current_row: int, current_column: int):
        row, column, count = len(grid), len(grid[0]), 0
        row_step, column_step = [-1, 1, 0, 0], [0, 0, -1, 1]
        for index in range(4):
            next_row = current_row + row_step[index]
            next_column = current_column + column_step[index]
            if row > next_row >= 0 and 0 <= next_column < xcolumn and grid[next_row][next_column] == 0:
                count += 1
            elif next_row < 0 or next_row >= row or next_column < 0 or next_column >= column:
                count += 1
        return count


if __name__ == '__main__':
    print(Solution().islandPerimeter([[0, 1, 0, 0], [1, 1, 1, 0], [0, 1, 0, 0], [1, 1, 0, 0]]))
