# NPC 搜尋玩家問題
# 遊戲地圖上有牆壁、草地(移動成本 1)、沼澤(移動成本 5)，NPC 要以最小成本走到玩家身邊。
#
# 1. 用 A* 搜尋：f(n) = g(n) 已走成本 + h(n) 曼哈頓距離估計
# 2. 和其他方法比較，看看 A* 是不是最優、效率如何：
#    - Greedy Best-First：只看 h(n)，快但「不保證最優」
#    - Dijkstra：只看 g(n)，保證最優但展開節點很多
#    - A*：只要 h(n) 不高估（admissible），就保證最優，且展開節點比 Dijkstra 少

import heapq

# N = NPC, P = 玩家, # = 牆, ~ = 沼澤(成本 5), . = 草地(成本 1)
MAP = [
    "....................",
    "......#####.........",
    "......#####.........",
    "N.....~~~~~.......P.",
    "......#####.........",
    "......#####.........",
    "....................",
]
COST = {".": 1, "~": 5, "N": 1, "P": 1}


def find(ch):
    for r, row in enumerate(MAP):
        if ch in row:
            return r, row.index(ch)


START, GOAL = find("N"), find("P")


def neighbors(r, c):
    for dr, dc in ((0, 1), (1, 0), (0, -1), (-1, 0)):
        nr, nc = r + dr, c + dc
        if 0 <= nr < len(MAP) and 0 <= nc < len(MAP[0]) and MAP[nr][nc] != "#":
            yield (nr, nc), COST[MAP[nr][nc]]


def manhattan(a, b):
    return abs(a[0] - b[0]) + abs(a[1] - b[1])


def search(mode):
    """mode = 'astar' | 'dijkstra' | 'greedy'，用同一套優先佇列框架"""
    def priority(g, pos):
        h = manhattan(pos, GOAL)
        return {"astar": g + h, "dijkstra": g, "greedy": h}[mode]

    g_cost = {START: 0}
    parent = {START: None}
    heap = [(priority(0, START), 0, START)]
    closed = set()
    while heap:
        _, g, pos = heapq.heappop(heap)
        if pos in closed:
            continue
        closed.add(pos)
        if pos == GOAL:
            break
        for nxt, step in neighbors(*pos):
            ng = g + step
            if nxt not in g_cost or ng < g_cost[nxt]:
                g_cost[nxt] = ng
                parent[nxt] = pos
                heapq.heappush(heap, (priority(ng, nxt), ng, nxt))

    path, p = [], GOAL
    while p is not None:
        path.append(p)
        p = parent[p]
    return path[::-1], g_cost[GOAL], len(closed)


def show(path):
    on = set(path)
    for r, row in enumerate(MAP):
        print("  " + "".join(
            ch if ch in "NP#" else ("*" if (r, c) in on else ch)
            for c, ch in enumerate(row)))


if __name__ == "__main__":
    results = {}
    for mode, name in (("astar", "A*"), ("greedy", "Greedy Best-First"), ("dijkstra", "Dijkstra")):
        path, cost, expanded = search(mode)
        results[mode] = cost
        print(f"[{name}] 總成本 = {cost}，路徑格數 = {len(path) - 1}，展開節點 = {expanded}")
        show(path)
        print()

    print("結論：")
    print(f"  A* 成本 {results['astar']} == Dijkstra 成本 {results['dijkstra']}"
          f" → A* 找到的就是最優解" if results["astar"] == results["dijkstra"] else "  A* 與 Dijkstra 不同！")
    if results["greedy"] > results["astar"]:
        print(f"  Greedy 成本 {results['greedy']} 比最優解多 {results['greedy'] - results['astar']}，"
              "它直直衝向玩家結果踩進沼澤 → 不保證最優")
