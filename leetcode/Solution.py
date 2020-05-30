from typing import List


class Solution:
    def canFinish(self, numCourses: int, prerequisites: List[List[int]]) -> bool:
        route, in_count, out_count = {}, [0] * numCourses, [0] * numCourses
        for course in range(numCourses):
            route[course] = []
        for prerequisite in prerequisites:
            in_count[prerequisite[1]] += 1
            out_count[prerequisite[0]] += 1
            route[prerequisite[0]].append(prerequisite[1])
        

if __name__ == '__main__':
    print(Solution().canFinish(5, [0, 1], [1, 2], [1, 4], [2, 3], [4, 3]))
