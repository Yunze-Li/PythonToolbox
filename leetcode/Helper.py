# Definition for singly-linked list.
from typing import List


class ListNode:
    def __init__(self, x):
        self.val = x
        self.next = None


def createLinkedList(nums: List) -> ListNode:
    head = ListNode(nums[0])
    current = head
    for i in range(1, len(nums)):
        current.next = ListNode(nums[i])
        current = current.next
    return head


class TreeNode:
    def __init__(self, x):
        self.val = x
        self.left = None
        self.right = None


def createTree(nums: List) -> TreeNode:
    if len(nums) == 0: return None
    root = TreeNode(nums[0])
    queue = [root]
    current = 1
    while current < len(nums) - 1:
        temp = queue.pop(0)
        left = TreeNode(nums[current])
        right = TreeNode(nums[current + 1])
        temp.left = left
        temp.right = right
        queue.append(left)
        queue.append(right)
        current += 2
    if current == len(nums) - 1:
        temp = queue.pop(0)
        temp.left = TreeNode(nums[current])
    return root


def printTree(root: TreeNode):
    if root is not None:
        print(root.val)
    if root.left is not None:
        printTree(root.left)
    if root.right is not None:
        printTree(root.right)


def compareTree(root1: TreeNode, root2: TreeNode) -> bool:
    return True
