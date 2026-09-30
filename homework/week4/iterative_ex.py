# 牛頓迭代的公式
sqrt_2_iter = lambda x: 0.5 * (x + 2 / x)

x = 1.0
print(f"初始猜測: x = {x}")

for i in range(1, 6):
    x = sqrt_2_iter(x)
    print(f"第 {i} 次迭代: x = {x}")