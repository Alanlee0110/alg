# 河內塔：遞迴版 與 禁止遞迴版（顯式堆疊），兩者結果必須完全相同

SRC, DST, AUX = 0, 1, 2
NAME = {0: "A", 1: "B", 2: "C"}


# ---------- 1. 遞迴解 ----------
def hanoi_recursive(n, src, dst, aux, moves):
    if n == 0:
        return moves
    hanoi_recursive(n - 1, src, aux, dst, moves)
    moves.append((n, src, dst))
    hanoi_recursive(n - 1, aux, dst, src, moves)
    return moves


# ---------- 2. 禁止遞迴解（自己用 list 當堆疊） ----------
def hanoi_iterative(n, src, dst, aux):
    moves = []
    stack = [(n, src, dst, aux, False)]  # False = 還沒展開這層
    while stack:
        k, s, d, a, expanded = stack.pop()
        if k == 1:
            moves.append((1, s, d))
        elif expanded:
            moves.append((k, s, d))  # 中間那一步：搬第 k 個盤子
        else:
            stack.append((k - 1, a, d, s, False))  # 第三步：aux -> dst
            stack.append((k, s, d, a, True))  # 第二步：標記，之後就搬自己
            stack.append((k - 1, s, a, d, False))  # 第一步：src -> aux
    return moves


# ---------- 模擬搬運，驗證盤子永遠大盤在下 ----------
def simulate(moves, n):
    towers = [list(range(n, 0, -1)), [], []]  # towers[0] = A，底在左邊
    for disk, src, dst in moves:
        if not towers[src] or towers[src][-1] != disk:
            return False, "非法移動：盤子 %d 不在 %s 頂端" % (disk, NAME[src])
        if towers[dst] and towers[dst][-1] < disk:
            return False, "非法移動：大盤 %d 壓到小盤" % disk
        towers[dst].append(towers[src].pop())
    if towers[DST] != list(range(n, 0, -1)):
        return False, "終點不是完整的塔"
    return True, towers


def show(title, moves, n):
    print("\n%s（共 %d 步，理論最少 %d 步）" % (title, len(moves), 2 ** n - 1))
    print("  %4s  %-8s" % ("步", "動作"))
    step = [0]
    print_moves(moves, step)


def print_moves(moves, step):
    if not moves:
        return
    disk, src, dst = moves[0]
    step[0] += 1
    print("  %4d  %d 號盤：%s -> %s" % (step[0], disk, NAME[src], NAME[dst]))
    print_moves(moves[1:], step)  # 用遞迴印，避免迴圈（這個檔案只有 Hanoi 的 2 個迴圈）


N = 4
rec = hanoi_recursive(N, SRC, DST, AUX, [])
itv = hanoi_iterative(N, SRC, DST, AUX)

print("河內塔 n = %d：塔 A(大->小) -> 塔 C" % N)
show("遞迴解", rec, N)
show("禁止遞迴解（顯式堆疊）", itv, N)

print("\n兩種解法步驟完全相同？", rec == itv)
print("模擬驗證（遞迴）：", simulate(rec, N))
print("模擬驗證（迭代）：", simulate(itv, N))

BIG = 12
same = hanoi_recursive(BIG, SRC, DST, AUX, []) == hanoi_iterative(BIG, SRC, DST, AUX)
ok, _ = simulate(hanoi_iterative(BIG, SRC, DST, AUX), BIG)
print("n = %d 大量驗證：步數 %d，兩解相同 %s，模擬合法 %s" % (BIG, 2 ** BIG - 1, same, ok))
