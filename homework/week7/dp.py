# 字串問題的動態規劃解：編輯距離（Edit Distance）與最長共同子序列（LCS）
# 特性：最優子結構 + 重複子問題，自底向上填表，O(n*m)，並回溯出對齊／字串本身
# 跑法：python3 dp.py

from time import perf_counter


# ---------- 計時：重複執行取平均（DP 太快，跑一次讀數不穩） ----------
def bench(fn, *args, target=0.05, limit=500):
    t0 = perf_counter()
    fn(*args)
    one = perf_counter() - t0
    reps = 1 if one <= 0 else max(1, min(limit, int(target / one)))
    t0 = perf_counter()
    for _ in range(reps):
        fn(*args)
    return (perf_counter() - t0) / reps   # 平均每次執行的秒數


# ---------- 編輯距離：轉移式 d[i][j] = min(插入, 刪除, 取代) ----------
def edit_table(a, b):
    n, m = len(a), len(b)
    d = [[0] * (m + 1) for _ in range(n + 1)]
    for i in range(n + 1):
        d[i][0] = i          # 把 a 的前 i 個字全刪掉
    for j in range(m + 1):
        d[0][j] = j          # 把 b 的前 j 個字全插進來
    for i in range(1, n + 1):
        for j in range(1, m + 1):
            cost = 0 if a[i - 1] == b[j - 1] else 1
            d[i][j] = min(
                d[i - 1][j] + 1,        # 刪除 a[i-1]
                d[i][j - 1] + 1,        # 插入 b[j-1]
                d[i - 1][j - 1] + cost, # 取代（相同則 0）
            )
    return d


def edit_ops(a, b, d):
    i, j = len(a), len(b)
    ops = []
    while i > 0 or j > 0:
        if i > 0 and j > 0:
            cost = 0 if a[i - 1] == b[j - 1] else 1
            if d[i][j] == d[i - 1][j - 1] + cost:
                ops.append(("相同" if cost == 0 else "取代", a[i - 1], b[j - 1]))
                i, j = i - 1, j - 1
                continue
        if i > 0 and d[i][j] == d[i - 1][j] + 1:
            ops.append(("刪除", a[i - 1], "-"))
            i -= 1
        else:
            ops.append(("插入", "-", b[j - 1]))
            j -= 1
    ops.reverse()
    return ops


def show_edit(a, b):
    d = edit_table(a, b)
    ops = edit_ops(a, b, d)
    print("\n編輯距離：%s -> %s" % (a, b))
    show_table(a, b, d, "  DP 表（列 = a 的前綴，行 = b 的前綴）")
    top, mid, bot = [], [], []
    for kind, x, y in ops:
        if kind == "相同":
            top.append(x); mid.append("|"); bot.append(y)
        elif kind == "取代":
            top.append(x); mid.append("*"); bot.append(y)
        elif kind == "刪除":
            top.append(x); mid.append("\\"); bot.append("-")
        else:
            top.append("-"); mid.append("/"); bot.append(y)
    print("  對齊（| 相同、* 取代、\\ 刪除、/ 插入）：")
    print("    " + " ".join(top))
    print("    " + " ".join(mid))
    print("    " + " ".join(bot))
    kinds = {k: sum(1 for o in ops if o[0] == k) for k in ("相同", "取代", "刪除", "插入")}
    print("  距離 = %d  （取代 %d、刪除 %d、插入 %d、相同 %d）"
          % (d[len(a)][len(b)], kinds["取代"], kinds["刪除"], kinds["插入"], kinds["相同"]))
    return d[len(a)][len(b)]


# ---------- 最長共同子序列：轉移式 d[i][j] = 相同 ? d[i-1][j-1]+1 : max(上, 左) ----------
def lcs_table(a, b):
    n, m = len(a), len(b)
    d = [[0] * (m + 1) for _ in range(n + 1)]
    for i in range(1, n + 1):
        for j in range(1, m + 1):
            if a[i - 1] == b[j - 1]:
                d[i][j] = d[i - 1][j - 1] + 1
            else:
                d[i][j] = max(d[i - 1][j], d[i][j - 1])
    return d


def lcs_string(a, b, d):
    i, j = len(a), len(b)
    out = []
    while i > 0 and j > 0:
        if a[i - 1] == b[j - 1]:
            out.append(a[i - 1])
            i, j = i - 1, j - 1
        elif d[i - 1][j] >= d[i][j - 1]:
            i -= 1
        else:
            j -= 1
    out.reverse()
    return "".join(out)


def show_lcs(a, b):
    d = lcs_table(a, b)
    s = lcs_string(a, b, d)
    print("\n最長共同子序列：%s vs %s" % (a, b))
    show_table(a, b, d, "  DP 表")
    print("  長度 = %d，LCS = %s" % (d[len(a)][len(b)], s))
    return d[len(a)][len(b)], s


# ---------- 表格排版 ----------
def show_table(a, b, d, title):
    print(title)
    print("      " + "  ".join(["#"] + list(b)))
    for i, row in enumerate(d):
        label = "#" if i == 0 else a[i - 1]
        print("   %s  " % label + "  ".join("%2d" % v for v in row))


CASES = [
    ("kitten", "sitting"),
    ("sunday", "saturday"),
    ("algorithm", "altruistic"),
    ("演算法", "演算術"),
]

if __name__ == "__main__":
    print("【動態規劃版】字串問題：編輯距離 + 最長共同子序列")
    print("填表格數 = (n+1)*(m+1)，時間 O(n*m)，空間 O(n*m)，可回溯出解")

    total = 0
    for a, b in CASES:
        total += show_edit(a, b) + show_lcs(a, b)[0]
    print("\n四組測資的編輯距離與 LCS 長度總和 = %d" % total)

    print("\n【DP 執行時間】（重複執行取平均，單位 ms）")
    print("   %-24s  %12s  %12s" % ("測資", "編輯距離", "LCS"))
    for a, b in CASES:
        t_edit = bench(edit_table, a, b) * 1000
        t_lcs = bench(lcs_table, a, b) * 1000
        print("   %-24s  %10.4f ms  %10.4f ms" % (a + " -> " + b, t_edit, t_lcs))

    print("\n【轉移式】")
    print("  編輯距離 d[i][j] = min( d[i-1][j]+1 刪, d[i][j-1]+1 插, d[i-1][j-1]+cost 代 )")
    print("  LCS       d[i][j] = 相同 ? d[i-1][j-1]+1 : max( d[i-1][j], d[i][j-1] )")
