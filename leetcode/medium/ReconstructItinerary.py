from typing import List, Dict


class Solution:
    def __init__(self):
        self.result = []
        self.is_found = False

    def findItinerary(self, tickets: List[List[str]]) -> List[str]:
        ticket_map, in_count, out_count, result_list = {}, {}, {}, []
        for ticket in tickets:
            start, end = ticket[0], ticket[1]
            if start in ticket_map.keys():
                ticket_map[start].append(end)
            else:
                ticket_map[start] = [end]
            in_count[end] = in_count[end] + 1 if end in in_count.keys() else 1
            out_count[start] = out_count[start] + 1 if start in out_count.keys() else 1
        self.helper("JFK", ticket_map, in_count, out_count, len(tickets), result_list)
        return self.result

    def helper(self, current: str, ticket_map: Dict, in_count: Dict, out_count: Dict, total: int,
               result_list: List[str]):
        if self.checkCorrectResult(in_count, out_count, total, result_list):
            temp_list = result_list.copy()
            temp_list.append(current)
            self.result = temp_list
            self.is_found = True
            return

        if current in ticket_map.keys() and not self.is_found:
            next_list = sorted(ticket_map[current])
            for next in next_list:
                if self.is_found:
                    return
                out_count[current] -= 1
                in_count[next] -= 1
                result_list.append(current)
                ticket_map[current].remove(next)
                self.helper(next, ticket_map, in_count, out_count, total, result_list)
                ticket_map[current].append(next)
                result_list.pop(len(result_list) - 1)
                in_count[next] += 1
                out_count[current] += 1

    def checkCorrectResult(self, in_count: Dict, out_count: Dict, total: int, result_list: List[str]) -> bool:
        return len(result_list) == total and all(value == 0 for value in in_count.values()) and all(
            value == 0 for value in out_count.values())


if __name__ == '__main__':
    print(Solution().findItinerary([["JFK", "SFO"], ["JFK", "ATL"], ["SFO", "ATL"], ["ATL", "JFK"], ["ATL", "SFO"]]))
