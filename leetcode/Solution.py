from typing import List


class Solution:
    def plusOne(self, digits: List[int]) -> List[int]:
        add_one = 1
        for index in range(len(digits) - 1, -1, -1):
            current = digits[index] + add_one
            if current < 10:
                digits[index] = current
                add_one = 0
            else:
                digits[index] = 0
                add_one = 1
        if add_one == 1:
            digits.insert(0, add_one)
        return digits


if __name__ == '__main__':
    print(Solution().plusOne([9, 9]))
