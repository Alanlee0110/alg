# 狼羊甘藍菜過河問題
# 農夫要把 狼、羊、甘藍菜 從左岸載到右岸，船上除了農夫最多只能再載一樣東西。
# 農夫不在時：狼會吃羊、羊會吃甘藍菜。
#
# 1. 用 BFS 找出最少渡河次數的解（BFS 第一次碰到終點時就是最少步數）
# 2. 再把 BFS 擴充成「找出所有最優解」，確認最優解有幾種

from collections import deque

ITEMS = ["農夫", "狼", "羊", "菜"]
# 狀態：(農夫, 狼, 羊, 菜) 各自在哪一岸，0 = 左岸，1 = 右岸
START = (0, 0, 0, 0)
GOAL = (1, 1, 1, 1)


def is_safe(state):
    farmer, wolf, goat, cabbage = state
    if wolf == goat != farmer:       # 狼羊同岸、農夫不在
        return False
    if goat == cabbage != farmer:    # 羊菜同岸、農夫不在
        return False
    return True


def next_states(state):
    """農夫自己過河，或帶一樣跟他同岸的東西過河"""
    farmer = state[0]
    for i in range(4):               # i = 0 表示農夫獨自過河
        if state[i] != farmer:
            continue
        s = list(state)
        s[0] = 1 - farmer
        s[i] = 1 - farmer
        s = tuple(s)
        if is_safe(s):
            yield s, i


def describe(prev, cur, item):
    direction = "→ 右岸" if cur[0] == 1 else "← 左岸"
    who = "農夫獨自" if item == 0 else f"農夫帶{ITEMS[item]}"
    return f"{who} {direction}"


def show_state(s):
    left = " ".join(ITEMS[i] for i in range(4) if s[i] == 0) or "(空)"
    right = " ".join(ITEMS[i] for i in range(4) if s[i] == 1) or "(空)"
    return f"左岸[{left:<12}]  ~~河~~  右岸[{right}]"


# ---------- 方法一：BFS 找一個最少步數的解 ----------
def bfs():
    parent = {START: None}
    queue = deque([START])
    while queue:
        s = queue.popleft()
        if s == GOAL:
            break
        for nxt, item in next_states(s):
            if nxt not in parent:
                parent[nxt] = (s, item)
                queue.append(nxt)
    steps, s = [], GOAL
    while parent[s] is not None:
        prev, item = parent[s]
        steps.append((prev, s, item))
        s = prev
    return steps[::-1]


# ---------- 方法二：BFS 分層，找出「所有」最優解 ----------
def bfs_all_optimal():
    dist = {START: 0}
    parents = {START: []}            # 一個狀態可能有多個同樣短的前一步
    queue = deque([START])
    while queue:
        s = queue.popleft()
        for nxt, item in next_states(s):
            if nxt not in dist:
                dist[nxt] = dist[s] + 1
                parents[nxt] = [(s, item)]
                queue.append(nxt)
            elif dist[nxt] == dist[s] + 1:
                parents[nxt].append((s, item))

    def build(s):
        if s == START:
            return [[]]
        result = []
        for prev, item in parents[s]:
            for p in build(prev):
                result.append(p + [(prev, s, item)])
        return result

    return build(GOAL), dist[GOAL]


if __name__ == "__main__":
    steps = bfs()
    print(f"[BFS] 最少需要渡河 {len(steps)} 次")
    print(f"  0. {show_state(START)}")
    for k, (prev, cur, item) in enumerate(steps, 1):
        print(f"  {k}. {describe(prev, cur, item):<12} {show_state(cur)}")

    print()
    all_paths, d = bfs_all_optimal()
    print(f"[所有最優解] 最少步數 = {d}，共有 {len(all_paths)} 種最優解：")
    for n, p in enumerate(all_paths, 1):
        print(f"  解 {n}: " + "，".join(describe(a, b, i) for a, b, i in p))
