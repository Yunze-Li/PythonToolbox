from typing import List


class Solution:
    def findJudge(self, N: int, trust: List[List[int]]) -> int:
        candidates = [True] * N
        count = [0] * N
        for trust_link in trust:
            candidates[trust_link[0] - 1] = False
            count[trust_link[1] - 1] += 1
        for i in range(N):
            if candidates[i] == True and count[i] == N - 1:
                return i + 1
        return -1


if __name__ == '__main__':
    print(Solution().findJudge(4, [[1, 3], [1, 4], [2, 3], [2, 4], [4, 3]]))
