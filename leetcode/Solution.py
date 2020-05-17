from typing import List


class Solution:
    def maxSubarraySumCircular(self, A: List[int]) -> int:
        current_max = 0
        total_max = A[0]
        current_min = 0
        total_min = A[0]
        total_sum = 0
        for num in A:
            current_max = max(current_max + num, num)
            total_max = max(total_max, current_max)
            current_min = min(current_min + num, num)
            total_min = min(total_min, current_min)
            total_sum += num
        return max(total_max, total_sum - total_min) if total_max > 0 else total_max


if __name__ == '__main__':
    print(Solution().maxSubarraySumCircular([1, -2, 3, -2]))
