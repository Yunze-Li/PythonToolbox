from collections import deque
from typing import List


class CourseSchedule:
    def canFinish(self, numCourses: int, prerequisites: List[List[int]]):
        in_count, out_count = [[] for _ in range(numCourses)], [0] * numCourses
        for prerequisite in prerequisites:
            out_count[prerequisite[0]] += 1
            in_count[prerequisite[1]].append(prerequisite[0])
        dq = deque()
        for i in range(numCourses):
            if out_count[i] == 0:
                dq.append(i)
        count = 0
        while dq:
            x = dq.popleft()
            count += 1
            for i in in_count[x]:
                out_count[i] -= 1
                if out_count[i] == 0:
                    dq.append(i)
        return count == numCourses


class CourseScheduleII:
    def findOrder(self, numCourses: int, prerequisites: List[List[int]]) -> List[int]:
        in_count, out_count = [[] for _ in range(numCourses)], [0] * numCourses
        for prerequisite in prerequisites:
            out_count[prerequisite[0]] += 1
            in_count[prerequisite[1]].append(prerequisite[0])
        dq = deque()
        result = []
        for i in range(numCourses):
            if out_count[i] == 0:
                dq.append(i)
                result.append(i)
        count = 0
        while dq:
            x = dq.popleft()
            count += 1
            for i in in_count[x]:
                out_count[i] -= 1
                if out_count[i] == 0:
                    dq.append(i)
                    result.append(i)
        return result if count == numCourses else []


if __name__ == '__main__':
    print(CourseScheduleII().findOrder(3, [[1, 0], [1, 2], [0, 1]]))
