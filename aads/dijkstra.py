"""
AADS Module — Dijkstra's Algorithm
Finds shortest route between farm zones for drone/tractor navigation.
Graph: weighted adjacency dict  {zone: {neighbour: distance_metres}}
Time Complexity: O((V+E) log V)
"""
import heapq


def dijkstra(graph: dict, source: str):
    dist = {v: float("inf") for v in graph}
    prev = {v: None for v in graph}
    dist[source] = 0
    pq = [(0, source)]

    while pq:
        d, u = heapq.heappop(pq)
        if d > dist[u]:
            continue                          # stale entry
        for v, weight in graph[u].items():
            alt = dist[u] + weight
            if alt < dist[v]:
                dist[v] = alt
                prev[v] = u
                heapq.heappush(pq, (alt, v))

    return dist, prev


def reconstruct_path(prev: dict, target: str):
    path, u = [], target
    while u is not None:
        path.append(u)
        u = prev[u]
    return list(reversed(path))


# Farm zone graph (distances in metres)
FARM_GRAPH = {
    "ZoneA": {"ZoneB": 150, "ZoneC": 300},
    "ZoneB": {"ZoneA": 150, "ZoneD": 200},
    "ZoneC": {"ZoneA": 300, "ZoneD": 250},
    "ZoneD": {"ZoneB": 200, "ZoneC": 250},
}


# ── Quick demo ──────────────────────────────────────────────────────────────
if __name__ == "__main__":
    dist, prev = dijkstra(FARM_GRAPH, "ZoneA")
    for target in ["ZoneB", "ZoneC", "ZoneD"]:
        path = reconstruct_path(prev, target)
        print(f"ZoneA → {target}: {dist[target]}m  |  path: {' → '.join(path)}")
