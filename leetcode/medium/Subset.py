from typing import List


class Solution:
    def __init__(self):
        self.result = []

    def subsets(self, nums: List[int]) -> List[List[int]]:
        if len(nums) == 0:
            return []
        self.helper([], nums, 0)
        return self.result

    def helper(self, current: List[int], nums: List[int], current_index: int):
        self.result.append(current.copy())
        visited = []
        for index in range(current_index, len(nums)):
            if nums[index] not in visited:
                current.append(nums[index])
                self.helper(current, nums, index + 1)
                visited.append(nums[index])
                current.pop()


if __name__ == '__main__':
    print(Solution().subsets([1, 1, 2, 3]))
