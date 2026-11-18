"""
單變數的數值微分與數值積分

- diff(f, x)          : 中心差分  f'(x) ≈ (f(x+h) - f(x-h)) / 2h
- integral(f, a, b)   : 黎曼和（取每個小區間的中點）
                        ∫f ≈ Σ f(中點) * dx
"""
import math
import sys

sys.stdout.reconfigure(encoding="utf-8")


def diff(f, x, h=1e-5):
    """中心差分：誤差 O(h^2)，比前向差分 (f(x+h)-f(x))/h 的 O(h) 準。"""
    return (f(x + h) - f(x - h)) / (2 * h)


def integral(f, a, b, n=100_000):
    """中點黎曼和：把 [a, b] 切成 n 等分，每段用中點的高度當矩形高。"""
    dx = (b - a) / n
    return sum(f(a + (i + 0.5) * dx) for i in range(n)) * dx


# ---------------- 測試 ----------------

def test_diff():
    assert abs(diff(lambda x: x ** 2, 3) - 6) < 1e-6          # (x^2)' = 2x
    assert abs(diff(lambda x: x ** 3, 2) - 12) < 1e-6         # (x^3)' = 3x^2
    assert abs(diff(math.sin, 0) - 1) < 1e-6                  # sin'(0) = cos(0)
    assert abs(diff(math.exp, 1) - math.e) < 1e-6             # (e^x)' = e^x


def test_integral():
    assert abs(integral(lambda x: x ** 2, 0, 1) - 1 / 3) < 1e-8
    assert abs(integral(math.sin, 0, math.pi) - 2) < 1e-8
    assert abs(integral(math.exp, 0, 1) - (math.e - 1)) < 1e-8
    assert abs(integral(lambda x: 1 / x, 1, math.e) - 1) < 1e-8   # ln e = 1


if __name__ == "__main__":
    test_diff()
    test_integral()
    print("所有測試通過\n")

    print("=== 數值微分（中心差分）===")
    cases = [
        ("x^2   在 x=3", lambda x: x ** 2, 3, 6),
        ("x^3   在 x=2", lambda x: x ** 3, 2, 12),
        ("sin x 在 x=0", math.sin, 0, 1),
        ("e^x   在 x=1", math.exp, 1, math.e),
    ]
    for name, f, x, exact in cases:
        d = diff(f, x)
        print(f"{name}: 數值 = {d:.10f}  正確 = {exact:.10f}  誤差 = {abs(d - exact):.2e}")

    print("\n=== 數值積分（中點黎曼和，n = 100000）===")
    cases = [
        ("∫0^1 x^2 dx  ", lambda x: x ** 2, 0, 1, 1 / 3),
        ("∫0^π sin x dx", math.sin, 0, math.pi, 2),
        ("∫0^1 e^x dx  ", math.exp, 0, 1, math.e - 1),
        ("∫1^e 1/x dx  ", lambda x: 1 / x, 1, math.e, 1),
    ]
    for name, f, a, b, exact in cases:
        v = integral(f, a, b)
        print(f"{name}: 數值 = {v:.10f}  正確 = {exact:.10f}  誤差 = {abs(v - exact):.2e}")

    print("\n=== 切越細越準：∫0^1 x^2 dx ===")
    for n in [10, 100, 1000, 10000]:
        v = integral(lambda x: x ** 2, 0, 1, n)
        print(f"n = {n:>5}: {v:.10f}  誤差 = {abs(v - 1 / 3):.2e}")
