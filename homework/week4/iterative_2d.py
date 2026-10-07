# 二維不動點迭代法：同一組方程，四種拆法，三收斂一發散

import cmath
import math

TOL = 1e-6
MAX_ITER = 200
BLOWUP = 1e3
TARGET = (4.0, 3.0)

R1 = lambda x, y: x * x + y * y - 25
R2 = lambda x, y: x - y - 1


def iterate(f, g, x0, y0, sequential, tol=TOL, max_iter=MAX_ITER):
    x, y = x0, y0
    for n in range(1, max_iter + 1):
        xn = f(x, y)
        yn = g(xn, y) if sequential else g(x, y)
        err = max(abs(xn - x), abs(yn - y))
        x, y = xn, yn
        if err < tol:
            return "收斂", n, x, y, err
        if max(abs(x), abs(y)) > BLOWUP:
            return "發散", n, x, y, err
    return "步數用盡", max_iter, x, y, err


def spectral_radius(f, g, x, y, h=1e-6):
    a = (f(x + h, y) - f(x - h, y)) / (2 * h)
    b = (f(x, y + h) - f(x, y - h)) / (2 * h)
    c = (g(x + h, y) - g(x - h, y)) / (2 * h)
    d = (g(x, y + h) - g(x, y - h)) / (2 * h)
    gap = cmath.sqrt((a - d) ** 2 / 4 + b * c)
    half = (a + d) / 2
    return max(abs(half + gap), abs(half - gap))


def show(title, f, g, x0, y0, sequential, rounds):
    rho = spectral_radius(f, g, *TARGET)
    print(f"\n{title}")
    print(f"  譜半徑 rho = {rho:.4f}  ->  {'收斂' if rho < 1 else '發散'}")
    x, y = x0, y0
    print(f"  {'n':<4}{'x':>18}{'y':>18}")
    for n in range(1, rounds + 1):
        xn = f(x, y)
        yn = g(xn, y) if sequential else g(x, y)
        x, y = xn, yn
        print(f"  {n:<4}{x:>18.6f}{y:>18.6f}")
        if max(abs(x), abs(y)) > BLOWUP:
            print("  ... 已經爆走，停止")
            break
    status, n, fx, fy, err = iterate(f, g, x0, y0, sequential)
    print(f"  => {status}：{n} 步，末次變化 {err:.2e}，末值 ({fx:.4f}, {fy:.4f})")


CASES = [
    (
        "拆法 A  x = sqrt(25 - y^2),  y = x - 1        （Jacobi：兩式都用舊值）",
        lambda x, y: math.sqrt(25 - y * y),
        lambda x, y: x - 1,
        5.0, 1.0, False, 6,
    ),
    (
        "拆法 A' 同上，但 y 用剛更新好的 x            （Gauss-Seidel）",
        lambda x, y: math.sqrt(25 - y * y),
        lambda x, y: x - 1,
        5.0, 1.0, True, 6,
    ),
    (
        "拆法 B  x = 1 + 12/x,  y = x - 1             （代數化成單一未知數）",
        lambda x, y: 1 + 12 / x,
        lambda x, y: x - 1,
        5.0, 1.0, False, 6,
    ),
    (
        "拆法 C  x = x + R1 + R2,  y = y + R1 - R2   （殘差直接加回去）",
        lambda x, y: x + R1(x, y) + R2(x, y),
        lambda x, y: y + R1(x, y) - R2(x, y),
        5.0, 1.0, False, 6,
    ),
]

print("要解： x^2 + y^2 = 25   與   x - y = 1")
print("正解為 (4, 3) 與 (-3, -4)；起點一律用 (5, 1)")

for case in CASES:
    show(*case)
