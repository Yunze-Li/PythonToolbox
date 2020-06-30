from typing import List


class TrieNode:
    def __init__(self):
        self.children = {}
        self.end_node = 0


class Trie:
    def __init__(self):
        self.root = TrieNode()

    def insert(self, word):
        root = self.root
        for symbol in word:
            dic_to_search = root.children
            if symbol not in dic_to_search:
                dic_to_search[symbol] = TrieNode()
            root.children = dic_to_search
            root = root.children[symbol]
        root.end_node = 1


class Solution1:
    def findWords(self, board, words):
        self.num_words = len(words)
        res, trie = [], Trie()
        for word in words: trie.insert(word)

        for i in range(len(board)):
            for j in range(len(board[0])):
                self.dfs(board, trie.root, i, j, "", res)
        return res

    def dfs(self, board, node, i, j, path, res):
        if self.num_words == 0: return

        if node.end_node:
            res.append(path)
            node.end_node = False
            self.num_words -= 1

        if i < 0 or i >= len(board) or j < 0 or j >= len(board[0]): return
        tmp = board[i][j]
        if tmp not in node.children: return

        board[i][j] = "#"
        for x, y in [[0, -1], [0, 1], [1, 0], [-1, 0]]:
            self.dfs(board, node.children[tmp], i + x, j + y, path + tmp, res)
        board[i][j] = tmp


class Solution2:
    def __init__(self):
        self.result = []

    def findWords(self, board: List[List[str]], words: List[str]) -> List[str]:
        if len(board) == 0 or len(board[0]) == 0:
            return []
        for word in words:
            self.findWord(board, word)
        return self.result

    def findWord(self, board: List[List[str]], word: str):
        row, column = len(board), len(board[0])
        is_visited = [[False for x in range(column)] for y in range(row)]
        for row_index in range(row):
            for column_index in range(column):
                if board[row_index][column_index] == word[0]:
                    is_visited[row_index][column_index] = True
                    self.findHelper(board, is_visited, word, 1, row_index, column_index)
                    is_visited[row_index][column_index] = False

    def findHelper(self, board: List[List[str]], is_visited: List[List[bool]], word: str, current_index: int,
                   current_row: int, current_column: int):
        if current_index == len(word):
            if word not in self.result:
                self.result.append(word)
            return

        row, column = len(board), len(board[0])
        row_step, column_step = [-1, 1, 0, 0], [0, 0, -1, 1]
        for index in range(4):
            next_row = current_row + row_step[index]
            next_column = current_column + column_step[index]
            if 0 <= next_row < row and 0 <= next_column < column and not is_visited[next_row][next_column] \
                    and word[current_index] == board[next_row][next_column]:
                is_visited[next_row][next_column] = True
                self.findHelper(board, is_visited, word, current_index + 1, next_row, next_column)
                is_visited[next_row][next_column] = False


if __name__ == '__main__':
    print(Solution1().findWords([["a", "b"], ["a", "a"]], ["aba", "baa", "bab", "aaab", "aaa", "aaaa", "aaba"]))
