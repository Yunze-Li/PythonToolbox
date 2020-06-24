from typing import List, Dict


class Solution:
	def __init__(self):
		self.result = -1

	def findCheapestPrice(self, n: int, flights: List[List[int]], src: int, dst: int, K: int) -> int:
		if K < 0:
			return -1
		graph = {}
		for flight in flights:
			if flight[0] in graph.keys():
				graph[flight[0]].append([flight[1], flight[2]])
			else:
				graph[flight[0]] = [[flight[1], flight[2]]]
		self.helper(graph, src, dst, K + 1, 0)
		return self.result

	def helper(self, graph: Dict, current: int, destination: int, remain_step: int, total_spend: int):
		if current == destination:
			if self.result < 0:
				self.result = total_spend
			else:
				self.result = min(self.result, total_spend)
			return
		elif remain_step <= 0:
			return

		if current in graph.keys():
			next_step_list = graph[current]
			for next_step in next_step_list:
				remain_step -= 1
				total_spend += next_step[1]
				self.helper(graph, next_step[0], destination, remain_step, total_spend)
				remain_step += 1
				total_spend -= next_step[1]


if __name__ == '__main__':
	print(Solution().findCheapestPrice(3, [[0, 1, 100], [1, 2, 100], [0, 2, 500]], 0, 2, 0))
