from typing import List


class Solution:
	def __init__(self):
		self.is_found = False

	def exist(self, board: List[List[str]], word: str) -> bool:
		if len(board) <= 0 or len(board[0]) <= 0:
			return False
		row, column = len(board), len(board[0])
		is_visited = [[False for _ in range(column)] for _ in range(row)]
		for row_index in range(row):
			for column_index in range(column):
				if not self.is_found and board[row_index][column_index] == word[0]:
					is_visited[row_index][column_index] = True
					self.helper(board, word, is_visited, row_index, column_index, 1)
					is_visited[row_index][column_index] = False
		return self.is_found

	def helper(self, board, word, is_visited, current_row, current_column, current_word):
		if current_word == len(word):
			self.is_found = True
			return

		row, column = len(board), len(board[0])
		row_step, column_step = [-1, 1, 0, 0], [0, 0, -1, 1]
		for index in range(4):
			new_row = current_row + row_step[index]
			new_column = current_column + column_step[index]
			if not self.is_found and 0 <= new_row < row and 0 <= new_column < column and board[new_row][new_column] == \
					word[current_word] and not is_visited[new_row][new_column]:
				is_visited[new_row][new_column] = True
				self.helper(board, word, is_visited, new_row, new_column, current_word + 1)
				is_visited[new_row][new_column] = False


if __name__ == '__main__':
	board = [
		['A', 'B', 'C', 'E'],
		['S', 'F', 'C', 'S'],
		['A', 'D', 'E', 'E']
	]
	print(Solution().exist(board, 'ABCCFB'))
