from typing import List


class Solution:

    def __init__(self):
        self.result = float("inf")

    def findMin(self, nums: List[int]) -> int:
        self.bin_dfs(nums, 0, len(nums) - 1)
        return self.result

    def bin_dfs(self, nums, start, end):
        if end - start <= 1:
            self.result = min(nums[start], nums[end], self.result)
            return

        mid = (start + end) // 2
        if nums[end] <= nums[mid]:
            self.bin_dfs(nums, mid + 1, end)
        if nums[end] >= nums[mid]:
            self.bin_dfs(nums, start, mid)


if __name__ == '__main__':
    print(Solution().findMin([4, 5, 6, 7, 7, 0, 0, 1, 2]))
