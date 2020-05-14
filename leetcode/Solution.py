class Solution:
    def removeKdigits(self, num: str, k: int) -> str:
        current = num
        for i in range(k):
            current = self.helper(current)
            while current.startswith('0'):
                current = current[1:]
        if len(current) == 0:
            return '0'
        else:
            return current

    def helper(self, num: str) -> str:
        if len(num) > 1 and num[1] == '0':
            return num[1:]
        for index in range(1, len(num)):
            if ord(num[index]) > ord(num[index - 1]):
                num = num[:index] + num[index + 1:]
                return num
        num = num[1:]
        return num


if __name__ == '__main__':
    print(Solution().removeKdigits("10200", 2))
