# 100 個字母的大測資：動態規劃 vs 暴力遞迴（實測 + 超時中止 + 指數外插）
# 暴力遞迴在 n=100 絕對跑不完，所以作法是：
#   1. DP 直接跑出答案並計時
#   2. 暴力遞迴給 3 秒死限，證明它中途就放棄
#   3. 用前綴（n = 6~16）實測指數成長，外插回 n = 100 估算它「本來」要多久
# 跑法：python3 big100.py

import math
import random
from time import perf_counter

from dp import bench, edit_table, lcs_table

N = 100
SEED = 7
DEADLINE = 3.0
PREFIX_NS = (6, 8, 10, 12, 14, 16)
ALPHA = "abcdefghijklmnopqrstuvwxyz"


class GiveUp(Exception):
    pass


# ---------- 暴力遞迴（可選死限，超過就中止） ----------
def edit_brute(a, b, i, j, stat, deadline=None):
    stat["calls"] += 1
    if deadline and stat["calls"] % 4096 == 0 and perf_counter() > deadline:
        raise GiveUp
    if i == len(a):
        return len(b) - j
    if j == len(b):
        return len(a) - i
    if a[i] == b[j]:
        return edit_brute(a, b, i + 1, j + 1, stat, deadline)
    return 1 + min(
        edit_brute(a, b, i + 1, j + 1, stat, deadline),
        edit_brute(a, b, i + 1, j, stat, deadline),
        edit_brute(a, b, i, j + 1, stat, deadline),
    )


def lcs_brute(a, b, i, j, stat, deadline=None):
    stat["calls"] += 1
    if deadline and stat["calls"] % 4096 == 0 and perf_counter() > deadline:
        raise GiveUp
    if i == len(a) or j == len(b):
        return 0
    if a[i] == b[j]:
        return 1 + lcs_brute(a, b, i + 1, j + 1, stat, deadline)
    return max(
        lcs_brute(a, b, i + 1, j, stat, deadline),
        lcs_brute(a, b, i, j + 1, stat, deadline),
    )


# ---------- 最小平方擬合 ln(calls) = k*n + c，用來外插 ----------
def fit(ns, counts):
    ys = [math.log(c) for c in counts]
    mx = sum(ns) / len(ns)
    my = sum(ys) / len(ys)
    k = sum((x - mx) * (y - my) for x, y in zip(ns, ys)) / sum((x - mx) ** 2 for x in ns)
    return k, my - k * mx


def fmt_time(seconds):
    if seconds < 1:
        return "%.4f 秒" % seconds
    if seconds < 3600:
        return "%.1f 分鐘" % (seconds / 60)
    if seconds < 86400 * 365:
        return "%.1f 小時" % (seconds / 3600)
    years = seconds / (86400 * 365)
    if years < 1e8:
        return "%s 年" % ("{:,.0f}".format(years))
    return "%e 年（宇宙年齡約 1.4e+10 年）" % years


if __name__ == "__main__":
    random.seed(SEED)
    a = "".join(random.choice(ALPHA) for _ in range(N))
    b_chars = list(a)
    for _ in range(25):
        b_chars[random.randrange(N)] = random.choice(ALPHA)
    b = "".join(b_chars)

    print("【100 個字母的測資】seed=%d，字母 a-z 隨機；b = a 改動 25 個位置" % SEED)
    print("  a = %s ..." % a[:60])
    print("  b = %s ..." % b[:60])

    # ---------- 1. 動態規劃：直接跑 ----------
    dist = edit_table(a, b)[N][N]
    lcs_len = lcs_table(a, b)[N][N]
    t_e = bench(edit_table, a, b) * 1000
    t_l = bench(lcs_table, a, b) * 1000
    print("\n【動態規劃 實測】101*101 = 10201 格")
    print("  編輯距離 = %-3d 耗時 %.4f ms" % (dist, t_e))
    print("  LCS 長度 = %-3d 耗時 %.4f ms" % (lcs_len, t_l))

    # ---------- 2. 暴力遞迴：n=100 給死限 ----------
    print("\n【暴力遞迴 實測】最多允許 %.1f 秒" % DEADLINE)
    for name, fn, ans, t_dp in (("編輯距離", edit_brute, dist, t_e), ("LCS", lcs_brute, lcs_len, t_l)):
        stat = {"calls": 0}
        t0 = perf_counter()
        try:
            got = fn(a, b, 0, 0, stat, perf_counter() + DEADLINE)
            print("  %s = %d，%.2f ms，呼叫 %d 次" % (name, got, (perf_counter() - t0) * 1000, stat["calls"]))
        except GiveUp:
            used = perf_counter() - t0
            print("  %s：跑了 %.2f 秒、呼叫 %d 次還沒算完 → 放棄（DP 只要 %.4f ms）"
                  % (name, used, stat["calls"], t_dp))

    # ---------- 3. 前綴實測，看指數成長 ----------
    print("\n【暴力遞迴 前綴實測】只取兩串的前 n 個字母（n=16 內還跑得完）")
    print("   %3s  %11s  %10s  %11s  %10s" % ("n", "編輯呼叫", "編輯ms", "LCS呼叫", "LCSms"))
    ns, e_calls, l_calls = [], [], []
    e_ms = l_ms = 0.0
    all_ok = True
    for n in PREFIX_NS:
        pa, pb = a[:n], b[:n]
        stat = {"calls": 0}
        got_e = edit_brute(pa, pb, 0, 0, stat)
        ce = stat["calls"]
        stat = {"calls": 0}
        got_l = lcs_brute(pa, pb, 0, 0, stat)
        cl = stat["calls"]
        te = bench(edit_brute, pa, pb, 0, 0, {"calls": 0}) * 1000
        tl = bench(lcs_brute, pa, pb, 0, 0, {"calls": 0}) * 1000
        ok = (got_e == edit_table(pa, pb)[n][n]) and (got_l == lcs_table(pa, pb)[n][n])
        all_ok = all_ok and ok
        ns.append(n)
        e_calls.append(ce)
        l_calls.append(cl)
        e_ms, l_ms = te, tl
        print("   %3d  %11d  %8.4f ms  %11d  %8.4f ms   答案與DP相同 %s" % (n, ce, te, cl, tl, ok))

    # ---------- 4. 外插回 n = 100 ----------
    tail = 3  # 只用最後 3 筆（n 較大、已進入穩定的指數區）擬合
    k_e, c_e = fit(ns[-tail:], e_calls[-tail:])
    k_l, c_l = fit(ns[-tail:], l_calls[-tail:])
    calls_e = math.exp(k_e * N + c_e)
    calls_l = math.exp(k_l * N + c_l)
    per_e = (e_ms / 1000) / e_calls[-1]   # 每次呼叫的秒數（用最大前綴實測）
    per_l = (l_ms / 1000) / l_calls[-1]
    sec_e = calls_e * per_e
    sec_l = calls_l * per_l

    print("\n【外插到 n = 100】（用最後 %d 筆實測 n=%s 的指數成長率推算，僅供估算）"
          % (tail, "~".join(str(x) for x in ns[-tail:])))
    print("  編輯距離暴力：約 %e 次呼叫，需 %s" % (calls_e, fmt_time(sec_e)))
    print("  LCS 暴力    ：約 %e 次呼叫，需 %s" % (calls_l, fmt_time(sec_l)))
    print("  動態規劃    ：%.4f ms / %.4f ms" % (t_e, t_l))
    print("  => 暴力比 DP 慢約 10^%d 倍（編輯距離）、10^%d 倍（LCS）"
          % (math.log10(sec_e / (t_e / 1000)), math.log10(sec_l / (t_l / 1000))))
    print("  全部前綴答案與 DP 一致？ %s" % all_ok)
