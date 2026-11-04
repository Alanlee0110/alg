# 遞迴關係式求解
# 對每一個遞迴式：
#   1. 直接照遞迴定義算出 T(n)
#   2. 用推導出來的封閉公式 (closed form) 算出 T(n)，驗證兩者相同
#   3. 輸出 Big O
#
# (1) T(n) = T(n-1) + 8,    T(1) = 1  →  T(n) = 8n - 7         →  O(n)
# (2) T(n) = 2T(n-1) + 9,   T(1) = 1  →  T(n) = 5·2^n - 9      →  O(2^n)
# (3) T(n) = 2T(n/2) + 1,   T(1) = 1  →  T(n) = 2n - 1         →  O(n)
# (4) T(n) = T(n/2) + 1,    T(1) = 1  →  T(n) = log2(n) + 1    →  O(log n)
# (3)(4) 的 n/2 只在 n 為 2 的次方時能整除，所以這兩題取 n = 1, 2, 4, 8, ...

from functools import lru_cache
from math import log2


@lru_cache(maxsize=None)
def T1(n):
    return 1 if n == 1 else T1(n - 1) + 8


@lru_cache(maxsize=None)
def T2(n):
    return 1 if n == 1 else 2 * T2(n - 1) + 9


@lru_cache(maxsize=None)
def T3(n):
    return 1 if n == 1 else 2 * T3(n // 2) + 1


@lru_cache(maxsize=None)
def T4(n):
    return 1 if n == 1 else T4(n // 2) + 1


PROBLEMS = [
    {
        "title": "T(n) = T(n-1) + 8, T(1) = 1",
        "f": T1,
        "closed": lambda n: 8 * n - 7,
        "formula": "8n - 7",
        "bigO": "O(n)",
        "ns": [1, 2, 3, 4, 5, 10, 20, 100],
        "why": [
            "每往下一層就加 8，從 T(1) 到 T(n) 共加了 (n-1) 次",
            "T(n) = T(1) + 8(n-1) = 1 + 8n - 8 = 8n - 7",
        ],
    },
    {
        "title": "T(n) = 2T(n-1) + 9, T(1) = 1",
        "f": T2,
        "closed": lambda n: 5 * 2**n - 9,
        "formula": "5·2^n - 9",
        "bigO": "O(2^n)",
        "ns": [1, 2, 3, 4, 5, 10, 20, 30],
        "why": [
            "兩邊同加 9：T(n) + 9 = 2T(n-1) + 18 = 2(T(n-1) + 9)",
            "令 S(n) = T(n) + 9，則 S(n) = 2S(n-1)，S(1) = 10 → S(n) = 10·2^(n-1) = 5·2^n",
            "T(n) = 5·2^n - 9",
        ],
    },
    {
        "title": "T(n) = 2T(n/2) + 1, T(1) = 1",
        "f": T3,
        "closed": lambda n: 2 * n - 1,
        "formula": "2n - 1",
        "bigO": "O(n)",
        "ns": [1, 2, 4, 8, 16, 32, 1024, 2**20],
        "why": [
            "遞迴樹：第 k 層有 2^k 個子問題，每個貢獻 1，共 log2(n)+1 層",
            "T(n) = 1 + 2 + 4 + ... + n = 2n - 1",
            "主定理：a=2, b=2, f(n)=1，n^(log_b a) = n 比 f(n) 大 → O(n)",
        ],
    },
    {
        "title": "T(n) = T(n/2) + 1, T(1) = 1",
        "f": T4,
        "closed": lambda n: int(log2(n)) + 1,
        "formula": "log2(n) + 1",
        "bigO": "O(log n)",
        "ns": [1, 2, 4, 8, 16, 32, 1024, 2**20],
        "why": [
            "每次 n 減半並加 1，從 n 減半到 1 需要 log2(n) 次",
            "T(n) = T(1) + log2(n) = log2(n) + 1（就像二分搜尋）",
            "主定理：a=1, b=2, f(n)=1，n^(log_b a) = 1 與 f(n) 同階 → O(log n)",
        ],
    },
]


if __name__ == "__main__":
    for i, p in enumerate(PROBLEMS, 1):
        print(f"({i}) {p['title']}")
        print("    推導：")
        for line in p["why"]:
            print(f"      {line}")
        print(f"    {'n':>9} | {'遞迴計算 T(n)':>14} | {'公式 ' + p['formula']:>14} | 相同?")
        all_ok = True
        for n in p["ns"]:
            a, b = p["f"](n), p["closed"](n)
            all_ok &= a == b
            print(f"    {n:>9} | {a:>14} | {b:>14} | {'✔' if a == b else '✘'}")
        print(f"    封閉公式：T(n) = {p['formula']}   {'(全部驗證通過)' if all_ok else '(驗證失敗!)'}")
        print(f"    Big O   ：{p['bigO']}")
        print()

    print("總結：")
    for i, p in enumerate(PROBLEMS, 1):
        print(f"  ({i}) {p['title']:<30} → T(n) = {p['formula']:<12} → {p['bigO']}")
