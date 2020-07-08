from typing import List


class Solution:
    def threeSum(self, nums: List[int]) -> List[List[int]]:
        if len(nums) <= 2:
            return []
        nums = sorted(nums)
        result = []
        for index in range(len(nums) - 2):
            if index > 0 and nums[index] == nums[index - 1]:
                continue
            target = -nums[index]
            left = index + 1
            right = len(nums) - 1
            while left < right:
                if nums[left] + nums[right] == target:
                    result.append([nums[index], nums[left], nums[right]])
                    left += 1
                    while left < right and nums[left] == nums[left - 1]:
                        left += 1
                elif nums[left] + nums[right] < target:
                    left += 1
                    while left < right and nums[left] == nums[left - 1]:
                        left += 1
                else:
                    right -= 1
                    while left < right and nums[right] == nums[right + 1]:
                        right -= 1
        return result


if __name__ == '__main__':
    print(Solution().threeSum([0, 0, 0, 0]))
