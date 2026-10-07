# 符號微分 sym_diff(expr)：遞迴處理表達式樹，並用數值微分交叉驗證

import math

# 表達式樹的表示方式：
#   數字        -> 1.5
#   變數        -> "x"
#   二元運算    -> ("+", a, b) / ("-", a, b) / ("*", a, b) / ("/", a, b) / ("^", a, b)
#   一元函數    -> ("sin", a) / ("cos", a) / ("ln", a)


def sym_diff(expr):
    if isinstance(expr, (int, float)):
        return 0.0
    if expr == "x":
        return 1.0

    op = expr[0]
    if op in ("+", "-"):
        a, b = expr[1], expr[2]
        return (op, sym_diff(a), sym_diff(b))

    if op == "*":
        a, b = expr[1], expr[2]
        return ("+", ("*", sym_diff(a), b), ("*", a, sym_diff(b)))  # 乘法法則

    if op == "/":
        a, b = expr[1], expr[2]
        # 商法則 (u/v)' = (u'v - uv') / v^2
        return ("/", ("-", ("*", sym_diff(a), b), ("*", a, sym_diff(b))),
                ("*", b, b))

    if op == "^":
        a, b = expr[1], expr[2]
        if isinstance(b, (int, float)):  # 幂次法則 (u^n)' = n u^(n-1) u'
            return ("*", ("*", float(b), ("^", a, b - 1)), sym_diff(a))
        # 一般情況 a^b = e^(b ln a)，用乘法/對數法則推導
        return ("*", expr, ("+", ("*", sym_diff(b), ("ln", a)),
                            ("*", b, ("/", sym_diff(a), a))))

    if op == "sin":
        return ("*", ("cos", expr[1]), sym_diff(expr[1]))  # 連鎖律
    if op == "cos":
        return ("*", ("*", -1.0, ("sin", expr[1])), sym_diff(expr[1]))
    if op == "ln":
        return ("*", ("/", 1.0, expr[1]), sym_diff(expr[1]))

    raise ValueError("不支援的運算子：" + str(op))


def to_str(expr):
    if isinstance(expr, (int, float)):
        return ("%g" % expr)
    if expr == "x":
        return "x"
    op = expr[0]
    if op in ("+", "-", "*"):
        sep = {"+": " + ", "-": " - ", "*": " * "}[op]
        return "(" + to_str(expr[1]) + sep + to_str(expr[2]) + ")"
    if op == "/":
        return "(" + to_str(expr[1]) + " / " + to_str(expr[2]) + ")"
    if op == "^":
        return "(" + to_str(expr[1]) + ")^" + to_str(expr[2])
    return op + "(" + to_str(expr[1]) + ")"


def simplify(expr):
    # 遞迴化簡：先化簡子樹，再合併數字、消掉單位元
    if isinstance(expr, (int, float)) or expr == "x":
        return expr
    op = expr[0]
    a, b = simplify(expr[1]), (simplify(expr[2]) if len(expr) > 2 else None)

    def isnum(v):
        return isinstance(v, (int, float))

    if op in ("+", "-", "*") and isnum(a) and isnum(b):
        return {"+": a + b, "-": a - b, "*": a * b}[op]
    if op == "*" and (a == 0 or b == 0):
        return 0.0
    if op == "*" and isnum(a) and a == 1:
        return b
    if op == "*" and isnum(b) and b == 1:
        return a
    if op == "+" and a == 0:
        return b
    if op == "+" and b == 0:
        return a
    if op == "-" and b == 0:
        return a
    if op == "^" and isnum(b) and b == 1:
        return a
    if op == "^" and isnum(b) and b == 0:
        return 1.0
    if op == "^" and isnum(a) and a == 1:
        return 1.0
    return (op, a, b)


def eval_expr(expr, x):
    if isinstance(expr, (int, float)):
        return float(expr)
    if expr == "x":
        return x
    op = expr[0]
    if op == "sin":
        return math.sin(eval_expr(expr[1], x))
    if op == "cos":
        return math.cos(eval_expr(expr[1], x))
    if op == "ln":
        return math.log(eval_expr(expr[1], x))
    a, b = eval_expr(expr[1], x), eval_expr(expr[2], x)
    return {"+": a + b, "-": a - b, "*": a * b, "/": a / b, "^": a ** b}[op]


def numeric_diff(expr, x, h=1e-6):
    return (eval_expr(expr, x + h) - eval_expr(expr, x - h)) / (2 * h)


CASES = [
    ("x^2 + 3x + 5", ("+", ("+", ("^", "x", 2), ("*", 3, "x")), 5), 1.3),
    ("x^3 - 2x", ("-", ("^", "x", 3), ("*", 2, "x")), 0.7),
    ("(x+1)/(x-1)", ("/", ("+", "x", 1), ("-", "x", 1)), 2.5),
    ("sin(x^2)", ("sin", ("^", "x", 2)), 0.9),
    ("x^x", ("^", "x", "x"), 1.8),
]

print("%-14s %-34s %-34s %s" % ("表達式", "sym_diff 結果", "化簡後", "數值微分檢查"))
for name, expr, x in CASES:
    d = simplify(sym_diff(expr))
    symbolic = eval_expr(d, x)
    numeric = numeric_diff(expr, x)
    diff = abs(symbolic - numeric)
    print("%-14s %-34s %-34s x=%s  符號=%+.6f 數值=%+.6f  誤差=%.2e %s"
          % (name, to_str(sym_diff(expr)), to_str(d), x, symbolic, numeric,
             diff, "OK" if diff < 1e-5 else "FAIL"))

print("\nd/dx 純常數 =", sym_diff(7))
print("d/dx x     =", sym_diff("x"))
