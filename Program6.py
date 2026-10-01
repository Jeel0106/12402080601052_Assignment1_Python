import heapq


def find_cycle(graph):
    state = {}
    parent = {}

    for node in graph:
        state[node] = 0

    def dfs(node):
        state[node] = 1

        for next_node in graph[node]:
            if state[next_node] == 0:
                parent[next_node] = node
                result = dfs(next_node)
                if result:
                    return result

            elif state[next_node] == 1:
                cycle = [next_node]
                current = node

                while current != next_node:
                    cycle.append(current)
                    current = parent[current]

                cycle.append(next_node)
                cycle.reverse()
                return cycle

        state[node] = 2
        return None

    for node in sorted(graph):
        if state[node] == 0:
            result = dfs(node)
            if result:
                return result

    return []


def main():
    try:
        n, e = map(int, input().split())
        graph = {}

        for i in range(n):
            name = input().strip()
            graph[name] = set()

        for i in range(e):
            first, second = input().split()
            graph[second].add(first)

        indegree = {}

        for node in graph:
            indegree[node] = 0

        for node in graph:
            for next_node in graph[node]:
                indegree[next_node] += 1

        heap = []

        for node in graph:
            if indegree[node] == 0:
                heapq.heappush(heap, node)

        order = []

        while heap:
            node = heapq.heappop(heap)
            order.append(node)

            for next_node in graph[node]:
                indegree[next_node] -= 1

                if indegree[next_node] == 0:
                    heapq.heappush(heap, next_node)

        if len(order) == n:
            print(" ".join(order))
        else:
            cycle = find_cycle(graph)
            print("CYCLE")
            print(" ".join(cycle))

    except Exception:
        print("INVALID")


if __name__ == "__main__":
    main()
