class TrieNode:
    def __init__(self, isWord):
        self.isWord = isWord
        self.children = [None] * 26


class Trie:
    root = None

    def __init__(self):
        """
        Initialize your data structure here.
        """
        self.root = TrieNode(False)

    def insert(self, word: str) -> None:
        """
        Inserts a word into the trie.
        """
        current_node = self.root
        for character in word:
            index = ord(character) - ord('a')
            next_node = current_node.children[index]
            if next_node is None:
                next_node = TrieNode(False)
                current_node.children[index] = next_node
            current_node = next_node
        current_node.isWord = True

    def search(self, word: str) -> bool:
        """
        Returns if the word is in the trie.
        """
        current_node = self.root
        for character in word:
            next_node = current_node.children[ord(character) - ord('a')]
            if next_node is None:
                return False
            current_node = next_node
        return current_node.isWord

    def startsWith(self, prefix: str) -> bool:
        """
        Returns if there is any word in the trie that starts with the given prefix.
        """
        current_node = self.root
        for character in prefix:
            next_node = current_node.children[ord(character) - ord('a')]
            if next_node is None:
                return False
            current_node = next_node
        return True


# Your Trie object will be instantiated and called as such:
# obj = Trie()
# obj.insert(word)
# param_2 = obj.search(word)
# param_3 = obj.startsWith(prefix)

if __name__ == '__main__':
    trie = Trie()
    trie.insert("apple")
    print(trie.startsWith("apple"))
    print(trie.search("apple"))
