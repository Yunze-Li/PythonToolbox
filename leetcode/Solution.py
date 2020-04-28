class Solution:
    def rangeBitwiseAnd(self, m: int, n: int) -> int:
        result = m
        for num in range(m + 1, n):
            result = result & num
        return result

if __name__ == '__main__':
    print(Solution().rangeBitwiseAnd(5, 7))
