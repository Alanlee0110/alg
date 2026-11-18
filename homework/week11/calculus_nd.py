"""
n 變數的數值微分（梯度）與黎曼積分（超體積）

- grad(f, x)              : 對每個座標各做一次中心差分
- integral(f, low, high)  : n 維中點黎曼和，n = len(low)
                            每一維切 k 段，共 k^n 個小方塊，
                            ∫f ≈ Σ f(方塊中心) * 方塊體積

範例 f(x) = x1^2 + ... + xn^2，low = [0]*n，high = [1]*n
正確答案：每一維 ∫0^1 x^2 dx = 1/3，所以總和 = n/3
"""
import itertools
import math
import sys
import time

sys.stdout.reconfigure(encoding="utf-8")


def grad(f, x, h=1e-5):
    g = []
    for i in range(len(x)):
        xp = list(x); xp[i] += h
        xm = list(x); xm[i] -= h
        g.append((f(xp) - f(xm)) / (2 * h))
    return g


def integral(f, low, high, budget=1_000_000):
    """n 維黎曼積分。

    budget 是最多願意算幾次 f，每一維切 k = floor(budget^(1/n)) 段。
    維度越高 k 越小 —— 這就是「維度詛咒」。
    """
    n = len(low)
    k = max(1, int(budget ** (1 / n) + 1e-9))
    dx = [(high[i] - low[i]) / k for i in range(n)]
    # 每一維的 k 個中點
    mids = [[low[i] + (j + 0.5) * dx[i] for j in range(k)] for i in range(n)]
    cell = math.prod(dx)
    total = 0.0
    for p in itertools.product(*mids):   # 走遍 k^n 個小方塊的中心
        total += f(p)
    return total * cell, k


def f(x):
    return sum(xi * xi for xi in x)


# ---------------- 測試 ----------------

def test_grad():
    # f = Σ x_i^2 的梯度 = 2x
    for x in ([1.0], [1.0, -2.0], [0.5, 1, 2, 3, 4], [i / 100 for i in range(100)]):
        g = grad(f, x)
        assert all(abs(g[i] - 2 * x[i]) < 1e-6 for i in range(len(x)))
    # f(x, y) = x^2 * y + sin(y)，梯度 = (2xy, x^2 + cos y)
    h = lambda p: p[0] ** 2 * p[1] + math.sin(p[1])
    g = grad(h, [2.0, 0.0])
    assert abs(g[0] - 0) < 1e-6 and abs(g[1] - 5) < 1e-6


def test_integral():
    # 中點法每一維切 k 段時，∫0^1 x^2 = 1/3 - 1/(12k^2)，所以答案可以算得很精確
    for n in (1, 2, 5):
        v, k = integral(f, [0] * n, [1] * n)
        expect = n * (1 / 3 - 1 / (12 * k * k))
        assert abs(v - expect) < 1e-9
        assert abs(v - n / 3) < 1e-2
    # 常數函數 1 的積分 = 方塊體積
    v, _ = integral(lambda p: 1, [0, 0, 0], [2, 3, 4], budget=1000)
    assert abs(v - 24) < 1e-9


if __name__ == "__main__":
    test_grad()
    test_integral()
    print("所有測試通過\n")

    print("=== 梯度：f(x) = Σ x_i^2，正確答案 = 2x ===")
    for x in ([1.0], [1.0, 2.0], [1.0, 2.0, 3.0, 4.0, 5.0]):
        print(f"x = {x}  grad = {[round(v, 6) for v in grad(f, x)]}")
    x100 = [i / 100 for i in range(100)]
    err = max(abs(gi - 2 * xi) for gi, xi in zip(grad(f, x100), x100))
    print(f"100 維 x = (0, 0.01, ..., 0.99)：最大誤差 = {err:.2e}")

    print("\n=== 黎曼積分：f(x) = Σ x_i^2，low = 0，high = 1，正確答案 = n/3 ===")
    for n in (1, 2, 5, 100):
        t = time.time()
        v, k = integral(f, [0] * n, [1] * n)
        print(f"n = {n:>3}: 每維切 k = {k:>7} 段  積分 = {v:.8f}  正確 = {n / 3:.8f}  "
              f"誤差 = {abs(v - n / 3):.2e}  ({time.time() - t:.2f} 秒)")

    print("\n100 維時，就算每一維只切 2 段，也要算 2^100 ≈ "
          f"{2 ** 100:.2e} 次 f，所以 budget 只夠每維切 1 段，")
    print("只剩正中心一個點 f(0.5, ..., 0.5) = 25，誤差 25%。黎曼積分在高維完全行不通。")
