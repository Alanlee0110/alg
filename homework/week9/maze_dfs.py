# 老鼠走迷宮問題
# 1. 先用 DFS（深度優先搜尋）找出「一條」可行路徑
# 2. 再用 BFS（廣度優先搜尋）找出「最短」路徑（最優解），比較兩者差異

from collections import deque

# 0 = 通道, 1 = 牆
MAZE = [
    [0, 0, 0, 0, 0, 0, 0, 1],
    [0, 1, 1, 1, 1, 1, 0, 1],
    [0, 1, 0, 0, 0, 1, 0, 0],
    [0, 1, 0, 1, 0, 1, 1, 0],
    [0, 0, 0, 1, 0, 0, 0, 0],
    [1, 1, 0, 1, 1, 1, 1, 0],
    [0, 0, 0, 0, 0, 0, 1, 0],
    [0, 1, 1, 1, 1, 0, 0, 0],
]
START = (0, 0)
GOAL = (6, 0)
DIRS = [(0, 1), (1, 0), (0, -1), (-1, 0)]  # 右、下、左、上


def neighbors(maze, r, c):
    rows, cols = len(maze), len(maze[0])
    for dr, dc in DIRS:
        nr, nc = r + dr, c + dc
        if 0 <= nr < rows and 0 <= nc < cols and maze[nr][nc] == 0:
            yield nr, nc


# ---------- 方法一：DFS（遞迴 + 回溯） ----------
def dfs(maze, pos, goal, visited, path, counter):
    counter[0] += 1                  # 記錄展開了幾個節點
    path.append(pos)
    visited.add(pos)
    if pos == goal:
        return True
    for nxt in neighbors(maze, *pos):
        if nxt not in visited:
            if dfs(maze, nxt, goal, visited, path, counter):
                return True
    path.pop()                       # 此路不通 → 回溯
    return False


# ---------- 方法二：BFS（保證最短路徑） ----------
def bfs(maze, start, goal):
    parent = {start: None}
    queue = deque([start])
    expanded = 0
    while queue:
        pos = queue.popleft()
        expanded += 1
        if pos == goal:
            break
        for nxt in neighbors(maze, *pos):
            if nxt not in parent:
                parent[nxt] = pos
                queue.append(nxt)
    if goal not in parent:
        return None, expanded
    path, p = [], goal               # 由終點沿 parent 回推路徑
    while p is not None:
        path.append(p)
        p = parent[p]
    return path[::-1], expanded


def show(maze, path):
    on_path = set(path)
    for r, row in enumerate(maze):
        line = ""
        for c, cell in enumerate(row):
            if (r, c) == START:
                line += "S "
            elif (r, c) == GOAL:
                line += "G "
            elif (r, c) in on_path:
                line += "* "
            else:
                line += "█ " if cell else ". "
        print(line)


if __name__ == "__main__":
    path, counter = [], [0]
    dfs(MAZE, START, GOAL, set(), path, counter)
    print(f"[DFS] 路徑長度 = {len(path) - 1} 步，展開節點 = {counter[0]}")
    show(MAZE, path)

    print()
    best, expanded = bfs(MAZE, START, GOAL)
    print(f"[BFS 最優解] 路徑長度 = {len(best) - 1} 步，展開節點 = {expanded}")
    show(MAZE, best)

    print()
    if len(path) > len(best):
        print(f"結論：DFS 找到的不是最短路徑，多走了 {len(path) - len(best)} 步；BFS 才是最優解。")
    else:
        print("結論：這次 DFS 剛好找到最短路徑，但 DFS 並不保證最短；BFS 才保證最優。")
