from typing import List


class Solution:
    def calculateMinimumHP(self, dungeon: List[List[int]]) -> int:
        row, column = len(dungeon), len(dungeon[0])
        dp = [[0] * (column + 1) for _ in range(row + 1)]

        dp[row - 1][column], dp[row][column - 1] = 1, 1
        for i in range(row - 1): dp[i][column] = float('inf')
        for i in range(column - 1): dp[row][i] = float('inf')
        for i in range(row - 1, -1, -1):
            for j in range(column - 1, -1, -1):
                dp[i][j] = max(1, min(dp[i + 1][j], dp[i][j + 1]) - dungeon[i][j])
        return dp[0][0]


if __name__ == '__main__':
    print(Solution().calculateMinimumHP([[-2, -3, 3], [-5, -10, 1], [10, 30, -5]]))
