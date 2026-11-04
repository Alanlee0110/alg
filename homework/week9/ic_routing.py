# IC 設計中的電路繞線問題（直接求最優解）
# 在格點晶片上有障礙物(既有元件)，要把多組腳位(net)兩兩接起來，導線之間不能交叉重疊。
#
# 最優解的做法：
# 1. 單一 net：使用 Lee 演算法（BFS 波前擴散），保證找到最短導線；
#    在同樣長度下再以「轉彎數最少」為第二目標（轉彎越少，via/製程問題越少）。
#    → 狀態 = (位置, 方向)，成本 = (長度, 轉彎數)，用 Dijkstra 做字典序最小化。
# 2. 多組 net：先繞的線會擋住後繞的線，繞線順序會影響結果。
#    net 數量少時，直接窮舉所有繞線順序，挑「全部繞通且總長度最短、轉彎最少」的方案。

import heapq
from itertools import permutations

W, H = 12, 8
# 障礙物（晶片上已經存在的元件）
BLOCKS = {(3, c) for c in range(2, 6)} | {(r, 8) for r in range(1, 5)} | {(6, 4), (6, 5)}

# 每組 net：(名稱, 起點腳位, 終點腳位)，座標為 (row, col)
NETS = [
    ("A", (2, 10), (5, 5)),
    ("B", (1, 10), (6, 7)),
    ("C", (4, 4), (5, 10)),
]
DIRS = [(0, 1), (1, 0), (0, -1), (-1, 0)]


def route(src, dst, occupied):
    """在 occupied 以外的格子中，找 (長度, 轉彎數) 字典序最小的路徑"""
    start = (src, -1)                           # -1 代表還沒有方向
    best = {start: (0, 0)}
    parent = {start: None}
    heap = [(0, 0, src, -1)]
    while heap:
        length, bends, pos, d = heapq.heappop(heap)
        if best.get((pos, d)) != (length, bends):
            continue
        if pos == dst:
            path, s = [], (pos, d)
            while s is not None:
                path.append(s[0])
                s = parent[s]
            return path[::-1], length, bends
        for nd, (dr, dc) in enumerate(DIRS):
            nxt = (pos[0] + dr, pos[1] + dc)
            if not (0 <= nxt[0] < H and 0 <= nxt[1] < W):
                continue
            if nxt in BLOCKS or (nxt in occupied and nxt != dst):
                continue
            cost = (length + 1, bends + (d != -1 and nd != d))
            if cost < best.get((nxt, nd), (10**9, 10**9)):
                best[(nxt, nd)] = cost
                parent[(nxt, nd)] = (pos, d)
                heapq.heappush(heap, (*cost, nxt, nd))
    return None, None, None                     # 繞不通


def route_all(order):
    pins = {p for _, a, b in NETS for p in (a, b)}
    occupied = set(pins)                        # 所有腳位都不能被別的線穿過
    paths, total_len, total_bends = {}, 0, 0
    for name, a, b in order:
        path, length, bends = route(a, b, occupied - {a, b})
        if path is None:
            return None, name
        occupied |= set(path)
        paths[name] = path
        total_len += length
        total_bends += bends
    return (paths, total_len, total_bends), None


def show(paths):
    grid = [["." for _ in range(W)] for _ in range(H)]
    for r, c in BLOCKS:
        grid[r][c] = "█"
    for name, path in paths.items():
        for r, c in path:
            grid[r][c] = name.lower()
        for r, c in (path[0], path[-1]):
            grid[r][c] = name                   # 大寫 = 腳位
    for row in grid:
        print("  " + " ".join(row))


if __name__ == "__main__":
    best = None
    for order in permutations(NETS):
        names = "".join(n for n, _, _ in order)
        result, failed = route_all(order)
        if result is None:
            print(f"順序 {names}: 繞線失敗（net {failed} 被擋住）")
            continue
        paths, total_len, total_bends = result
        print(f"順序 {names}: 總長度 = {total_len}，總轉彎 = {total_bends}")
        if best is None or (total_len, total_bends) < best[0]:
            best = ((total_len, total_bends), names, paths)

    if best is None:
        print("\n所有順序都無法完成繞線")
    else:
        (total_len, total_bends), names, paths = best
        print(f"\n[最優解] 繞線順序 {names}，總長度 = {total_len}，總轉彎 = {total_bends}")
        show(paths)
