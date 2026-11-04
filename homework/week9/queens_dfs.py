# 八皇后問題
# 在 8x8 棋盤放 8 個皇后，彼此不能同列、同行、同斜線。
#
# 1. 用 DFS + 回溯（backtracking）逐列放皇后，找出全部 92 組解
# 2. 八皇后沒有「距離」可比，所以「最優」指的是「搜尋得更有效率」：
#    改用位元運算（bitmask）做剪枝，O(1) 判斷衝突，並比較兩者的速度
# 3. 再利用棋盤的對稱性（旋轉、翻轉）把 92 組解歸納成 12 組本質不同的解

from datetime import datetime

N = 8


# ---------- 方法一：基本 DFS 回溯 ----------
def solve_dfs(n):
    solutions, cols = [], []
    nodes = [0]

    def safe(row, col):
        for r, c in enumerate(cols):
            if c == col or abs(c - col) == abs(r - row):   # 同行 或 同斜線
                return False
        return True

    def dfs(row):
        nodes[0] += 1
        if row == n:
            solutions.append(cols.copy())
            return
        for col in range(n):
            if safe(row, col):
                cols.append(col)
                dfs(row + 1)
                cols.pop()                                  # 回溯

    dfs(0)
    return solutions, nodes[0]


# ---------- 方法二：DFS + 位元剪枝 ----------
def solve_bitmask(n):
    solutions, cols = [], []
    full = (1 << n) - 1
    nodes = [0]

    # colmask: 已被佔用的行
    # diag1  : 左上→右下斜線的攻擊範圍（往下一列時左移）
    # diag2  : 右上→左下斜線的攻擊範圍（往下一列時右移）
    def dfs(colmask, diag1, diag2):
        nodes[0] += 1
        if colmask == full:
            solutions.append(cols.copy())
            return
        free = full & ~(colmask | diag1 | diag2)            # 這一列還能放的位置
        while free:
            bit = free & -free                              # 取最低位的 1
            free ^= bit
            cols.append(bit.bit_length() - 1)
            dfs(colmask | bit, ((diag1 | bit) << 1) & full, (diag2 | bit) >> 1)
            cols.pop()

    dfs(0, 0, 0)
    return solutions, nodes[0]


# ---------- 對稱性：找出本質不同的解 ----------
def symmetries(sol):
    n = len(sol)
    board = sol
    result = []
    for _ in range(4):
        # 旋轉 90 度：原本 (r, c) → (c, n-1-r)
        rotated = [0] * n
        for r, c in enumerate(board):
            rotated[c] = n - 1 - r
        board = rotated
        result.append(tuple(board))
        result.append(tuple(n - 1 - c for c in board))      # 左右翻轉
    return result


def unique_solutions(solutions):
    seen, unique = set(), []
    for s in solutions:
        key = min(symmetries(s))
        if key not in seen:
            seen.add(key)
            unique.append(s)
    return unique


def show(sol):
    for c in sol:
        print("  " + " ".join("Q" if i == c else "." for i in range(len(sol))))


def timed(f, *args):
    t = datetime.now()
    r = f(*args)
    return r, datetime.now() - t


if __name__ == "__main__":
    (sols1, nodes1), t1 = timed(solve_dfs, N)
    print(f"[DFS 回溯]   解的數量 = {len(sols1)}，搜尋節點 = {nodes1}，時間 = {t1}")
    print("第一組解：")
    show(sols1[0])

    (sols2, nodes2), t2 = timed(solve_bitmask, N)
    print(f"\n[DFS + 位元] 解的數量 = {len(sols2)}，搜尋節點 = {nodes2}，時間 = {t2}")
    print("兩種方法的解集合是否相同：", sorted(sols1) == sorted(sols2))

    uniq = unique_solutions(sols1)
    print(f"\n[對稱性化簡] 92 組解中，本質不同的解只有 {len(uniq)} 組")

    # 位元版本在較大的 n 上優勢更明顯
    for n in (10, 12):
        (_, _), ta = timed(solve_dfs, n)
        (s, _), tb = timed(solve_bitmask, n)
        print(f"n = {n:2d}: 解 {len(s):5d} 組 | 基本 DFS {ta} | 位元 DFS {tb}")
