"""
用蒙地卡羅法算 n 變數積分（超體積）

在 [low, high] 這個 n 維方塊裡均勻亂撒 N 個點，
    ∫f ≈ 方塊體積 * 平均(f(x_i))
誤差 ~ 1/sqrt(N)，跟維度 n 無關 —— 所以高維時遠勝黎曼積分。

範例 f(x) = x1^2 + ... + xn^2，low = 0，high = 1，正確答案 = n/3
"""
import math
import random
import sys
import time

sys.stdout.reconfigure(encoding="utf-8")


def integral(f, low, high, samples=100_000):
    n = len(low)
    volume = math.prod(high[i] - low[i] for i in range(n))
    total = 0.0
    for _ in range(samples):
        x = [random.uniform(low[i], high[i]) for i in range(n)]
        total += f(x)
    return volume * total / samples


def f(x):
    return sum(xi * xi for xi in x)


# ---------------- 測試 ----------------

def test_integral():
    random.seed(0)
    # Var(Σ x_i^2) = n * 4/45，標準誤差 = sqrt(n*4/45 / N)，容許 5 倍標準誤差
    for n, N in ((1, 100_000), (2, 100_000), (5, 50_000), (100, 10_000)):
        v = integral(f, [0] * n, [1] * n, N)
        se = math.sqrt(n * 4 / 45 / N)
        assert abs(v - n / 3) < 5 * se, (n, v)
    # 常數函數 1 的積分 = 方塊體積（沒有隨機誤差）
    assert abs(integral(lambda p: 1, [0, 0, 0], [2, 3, 4], 100) - 24) < 1e-9
    # 單位圓面積 = π：在 [-1,1]^2 撒點，落在圓內算 1
    inside = lambda p: 1 if p[0] ** 2 + p[1] ** 2 <= 1 else 0
    assert abs(integral(inside, [-1, -1], [1, 1], 200_000) - math.pi) < 0.02


if __name__ == "__main__":
    test_integral()
    print("所有測試通過\n")

    random.seed(42)
    print("=== 蒙地卡羅積分：f(x) = Σ x_i^2，low = 0，high = 1，正確答案 = n/3 ===")
    for n, N in ((1, 100_000), (2, 100_000), (5, 100_000), (100, 100_000)):
        t = time.time()
        v = integral(f, [0] * n, [1] * n, N)
        print(f"n = {n:>3}, 撒 {N} 點: 積分 = {v:.6f}  正確 = {n / 3:.6f}  "
              f"相對誤差 = {abs(v - n / 3) / (n / 3):.2e}  ({time.time() - t:.2f} 秒)")

    print("\n100 維只要撒 10 萬個點，相對誤差就在 0.1% 左右；")
    print("黎曼積分就算給 100 萬次 f 的預算，100 維也只能每維切 1 段，誤差 25%。")
