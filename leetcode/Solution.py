from typing import List


class Solution:
    def kClosest(self, points: List[List[int]], K: int) -> List[List[int]]:
        result = sorted(points, key=lambda item: item[0] * item[0] + item[1] * item[1])
        return result[:K]


if __name__ == '__main__':
    print(Solution().kClosest([[3, 3], [5, -1], [-2, 4]], 2))
