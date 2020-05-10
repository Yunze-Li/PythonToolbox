class ListNode:
    def __init__(self, key: int, value: int):
        self.key = key
        self.value = value
        self.prev = None
        self.next = None


class LRUCache:

    def __init__(self, capacity: int):
        self.capacity = capacity
        self.head = ListNode(0, 0)
        self.tail = ListNode(0, 0)
        self.head.next = self.tail
        self.tail.prev = self.head
        self.node_map = {}

    def get(self, key: int) -> int:
        if key in self.node_map.keys():
            self.updateNode(key)
            return self.node_map[key].value
        else:
            return -1

    def put(self, key: int, value: int) -> None:
        new_node = ListNode(key, value)
        if key in self.node_map:
            old_node = self.node_map[key]
            self.removeNode(old_node)
        elif len(self.node_map) == self.capacity:
            self.removeLastNode()
        self.node_map[key] = new_node
        self.insertNewNode(new_node)

    def removeLastNode(self):
        target = self.tail.prev
        self.removeNode(target)
        self.node_map.pop(target.key, None)

    def updateNode(self, key: int):
        target = self.node_map[key]
        self.removeNode(target)
        self.insertNewNode(target)

    def insertNewNode(self, new_node: ListNode):
        temp = self.head.next
        self.head.next = new_node
        new_node.prev = self.head
        new_node.next = temp
        temp.prev = new_node

    def removeNode(self, node: ListNode):
        previous_node = node.prev
        next_node = node.next
        previous_node.next = next_node
        next_node.prev = previous_node
        node.prev = None
        node.next = None


if __name__ == '__main__':
    cache = LRUCache(2)
    print(cache.put(1, 1))
    print(cache.put(2, 2))
    print(cache.get(1))
    print(cache.put(3, 3))
    print(cache.get(2))
    print(cache.put(4, 4))
    print(cache.get(1))
    print(cache.get(3))
    print(cache.get(4))
