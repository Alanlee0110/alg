# 字串問題的「非動態規劃」解：純暴力遞迴（不填表、不記憶化）
# 同樣的轉移式，但每次重算子問題 → 指數成長；用來對照 dp.py 的 O(n*m)
# 跑法：python3 non_dp.py

from dp import bench, edit_table, lcs_table


# ---------- 編輯距離：暴力遞迴 ----------
def edit_brute(a, b, i, j, stat):
    stat["calls"] += 1
    if i == len(a):
        return len(b) - j          # 剩下的全部插入
    if j == len(b):
        return len(a) - i          # 剩下的全部刪除
    if a[i] == b[j]:               # 相同就直接往右下走（不展開三個分支）
        return edit_brute(a, b, i + 1, j + 1, stat)
    return 1 + min(
        edit_brute(a, b, i + 1, j + 1, stat),  # 取代
        edit_brute(a, b, i + 1, j, stat),      # 刪除
        edit_brute(a, b, i, j + 1, stat),      # 插入
    )


# ---------- 最長共同子序列：暴力遞迴 ----------
def lcs_brute(a, b, i, j, stat):
    stat["calls"] += 1
    if i == len(a) or j == len(b):
        return 0
    if a[i] == b[j]:
        return 1 + lcs_brute(a, b, i + 1, j + 1, stat)
    return max(
        lcs_brute(a, b, i + 1, j, stat),
        lcs_brute(a, b, i, j + 1, stat),
    )


CASES = [
    ("kitten", "sitting"),
    ("sunday", "saturday"),
    ("algorithm", "altruistic"),
    ("演算法", "演算術"),
]


def run_case(a, b):
    stat = {"calls": 0}
    dist = edit_brute(a, b, 0, 0, stat)
    edit_calls = stat["calls"]

    stat["calls"] = 0
    lcs_len = lcs_brute(a, b, 0, 0, stat)
    lcs_calls = stat["calls"]

    dp_dist = edit_table(a, b)[len(a)][len(b)]
    dp_lcs = lcs_table(a, b)[len(a)][len(b)]
    ok = (dist == dp_dist) and (lcs_len == dp_lcs)

    t_e_brute = bench(edit_brute, a, b, 0, 0, {"calls": 0})
    t_e_dp = bench(edit_table, a, b)
    t_l_brute = bench(lcs_brute, a, b, 0, 0, {"calls": 0})
    t_l_dp = bench(lcs_table, a, b)

    print("\n%s -> %s" % (a, b))
    print("  編輯距離 = %d" % dist)
    print("     暴力遞迴 %10.4f ms（%d 次呼叫）" % (t_e_brute * 1000, edit_calls))
    print("     動態規劃 %10.4f ms（%d 格）     慢 %6.1f 倍"
          % (t_e_dp * 1000, (len(a) + 1) * (len(b) + 1), t_e_brute / t_e_dp))
    print("  LCS 長度 = %d" % lcs_len)
    print("     暴力遞迴 %10.4f ms（%d 次呼叫）" % (t_l_brute * 1000, lcs_calls))
    print("     動態規劃 %10.4f ms（%d 格）     慢 %6.1f 倍"
          % (t_l_dp * 1000, (len(a) + 1) * (len(b) + 1), t_l_brute / t_l_dp))
    print("  與 dp.py 動態規劃答案相同？ %s" % ok)
    return ok, edit_calls, lcs_calls, t_e_brute + t_l_brute, t_e_dp + t_l_dp


def growth():
    print("\n【暴力 vs DP 的規模成長】")
    print("   %3s  %10s  %9s  %7s  %10s  %9s  %7s"
          % ("n", "編輯暴力", "編輯DP", "慢幾倍", "LCS暴力", "LCS-DP", "慢幾倍"))
    for n in range(2, 9):
        a = "abcdefghij"[:n]
        b = ("z" + a[1:])
        t_eb = bench(edit_brute, a, b, 0, 0, {"calls": 0}) * 1000
        t_ed = bench(edit_table, a, b) * 1000
        t_lb = bench(lcs_brute, a, b, 0, 0, {"calls": 0}) * 1000
        t_ld = bench(lcs_table, a, b) * 1000
        print("   %3d  %8.4f ms  %6.4f ms  %6.1f  %8.4f ms  %6.4f ms  %6.1f"
              % (n, t_eb, t_ed, t_eb / t_ed, t_lb, t_ld, t_lb / t_ld))


if __name__ == "__main__":
    print("【非動態規劃版】字串問題：純暴力遞迴（無表格、無記憶化）")
    print("同一組轉移式，但每個子問題都重算，呼叫次數隨長度指數成長")

    all_ok = True
    te = tl = 0
    t_brute = t_dp = 0.0
    for a, b in CASES:
        ok, ce, cl, tb, td = run_case(a, b)
        all_ok = all_ok and ok
        te += ce
        tl += cl
        t_brute += tb
        t_dp += td

    print("\n四組測資總呼叫次數：編輯距離 %d、LCS %d（DP 只有約 %d 格要填）"
          % (te, tl, sum((len(a) + 1) * (len(b) + 1) for a, b in CASES)))
    print("四組測資總耗時：暴力 %.4f ms ｜ DP %.4f ms ｜ 慢 %.1f 倍"
          % (t_brute * 1000, t_dp * 1000, t_brute / t_dp))
    print("全部與動態規劃答案一致？ %s" % all_ok)

    growth()
