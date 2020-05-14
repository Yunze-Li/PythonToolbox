class MinStack:

    def __init__(self):
        """
        initialize your data structure here.
        """
        self.stack = []
        self.minimum = []

    def push(self, x: int) -> None:
        self.stack.append(x)
        if len(self.minimum) == 0:
            self.minimum.append(x)
        elif self.minimum[len(self.minimum) - 1]  >= x:
            self.minimum.append(x)

    def pop(self) -> None:
        temp = self.stack.pop()
        if len(self.minimum) > 0 and self.minimum[len(self.minimum) - 1] == temp:
            self.minimum.pop()

    def top(self) -> int:
        if len(self.stack) > 0:
            return self.stack[len(self.stack) - 1]
        else:
            return None

    def getMin(self) -> int:
        if len(self.minimum) > 0:
            return self.minimum[len(self.minimum) - 1]
        else:
            return None


if __name__ == '__main__':
    minStack = MinStack()
    print(minStack.push(-2))
    print(minStack.push(0))
    print(minStack.push(-3))
    print(minStack.getMin())
    print(minStack.pop())
    print(minStack.top())
    print(minStack.getMin())
