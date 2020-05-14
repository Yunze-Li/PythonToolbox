from typing import List


class ListNode:
    def __init__(self, value: int):
        self.value = value
        self.next = None
        self.prev = None


class FirstUnique:

    def __init__(self, nums: List[int]):
        self.map = {}
        self.head = ListNode(-1)
        self.tail = ListNode(-1)
        self.head.next = self.tail
        self.tail.prev = self.head
        for num in nums:
            self.add(num)

    def showFirstUnique(self) -> int:
        return self.head.next.value

    def add(self, value: int) -> None:
        if value not in self.map:
            new_node = ListNode(value)
            self.map[value] = new_node
            self.insertNewNode(new_node)
        else:
            node = self.map[value]
            if node.prev is not None and node.next is not None:
                self.removeNode(node)

    def insertNewNode(self, node: ListNode):
        temp = self.tail.prev
        temp.next = node
        node.prev = temp
        node.next = self.tail
        self.tail.prev = node

    def removeNode(self, node: ListNode):
        prev_node = node.prev
        next_node = node.next
        prev_node.next = next_node
        next_node.prev = prev_node
        node.prev = None
        node.next = None


if __name__ == '__main__':
    queue = FirstUnique([809])
    print(queue.showFirstUnique())
    print(queue.add(809))
    print(queue.showFirstUnique())
