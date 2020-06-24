from leetcode import Helper
from leetcode.Helper import TreeNode


class Solution:
    def countNodes(self, root: TreeNode) -> int:
        if root is None:
            return 0
        queue, result = [root], 0
        while len(queue) > 0:
            current = queue.pop(0)
            result += 1
            if current.left is not None:
                queue.append(current.left)
            if current.right is not None:
                queue.append(current.right)
        return result


if __name__ == '__main__':
    tree = Helper.createTree([1, 2, 3, 4, 5, 6])
    print(Solution().countNodes(tree))
