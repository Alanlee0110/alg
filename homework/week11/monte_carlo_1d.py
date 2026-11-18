"""
用蒙地卡羅法算單變數積分

在 [a, b] 均勻亂撒 n 個點 x_i，
    ∫_a^b f(x) dx ≈ (b - a) * 平均(f(x_i))
誤差大約跟 1/sqrt(n) 成正比：點數變 100 倍，誤差才縮小 10 倍。
"""
import math
import random
import sys

sys.stdout.reconfigure(encoding="utf-8")


def mc_integral(f, a, b, n=100_000):
    total = sum(f(random.uniform(a, b)) for _ in range(n))
    return (b - a) * total / n


# ---------------- 測試 ----------------

def test_mc_integral():
    random.seed(0)
    # 蒙地卡羅有隨機誤差，所以容許度要放寬到 1e-2 等級
    assert abs(mc_integral(lambda x: x ** 2, 0, 1) - 1 / 3) < 1e-2
    assert abs(mc_integral(math.sin, 0, math.pi) - 2) < 2e-2
    assert abs(mc_integral(math.exp, 0, 1) - (math.e - 1)) < 1e-2
    assert abs(mc_integral(lambda x: 5, 2, 4) - 10) < 1e-12     # 常數函數沒有變異數，一定精確


if __name__ == "__main__":
    test_mc_integral()
    print("所有測試通過\n")

    random.seed(42)
    print("=== 蒙地卡羅積分（n = 100000）===")
    cases = [
        ("∫0^1 x^2 dx  ", lambda x: x ** 2, 0, 1, 1 / 3),
        ("∫0^π sin x dx", math.sin, 0, math.pi, 2),
        ("∫0^1 e^x dx  ", math.exp, 0, 1, math.e - 1),
    ]
    for name, f, a, b, exact in cases:
        v = mc_integral(f, a, b)
        print(f"{name}: 數值 = {v:.6f}  正確 = {exact:.6f}  誤差 = {abs(v - exact):.2e}")

    print("\n=== 點數 vs 誤差：∫0^1 x^2 dx ===")
    for n in [100, 10_000, 1_000_000]:
        v = mc_integral(lambda x: x ** 2, 0, 1, n)
        print(f"n = {n:>7}: {v:.6f}  誤差 = {abs(v - 1 / 3):.2e}")
