# 自製 map / filter / reduce，且全程禁止迴圈（for/while），
# 用遞迴完成泡沫排序：每輪把最大值「浮」到末端，再處理剩下的 n-1 個


# ---------- 1. 自製函數型工具（內部也用遞迴，不用迴圈） ----------
def my_map(f, seq):
    if not seq:
        return []
    return [f(seq[0])] + my_map(f, seq[1:])


def my_filter(pred, seq):
    if not seq:
        return []
    head = seq[:1] if pred(seq[0]) else []
    return head + my_filter(pred, seq[1:])


def my_reduce(f, seq, init=None):
    if not seq:
        if init is None:
            raise TypeError("空序列且沒有初始值")
        return init
    if init is None:
        return my_reduce(f, seq[1:], seq[0])
    return my_reduce(f, seq[1:], f(init, seq[0]))


# ---------- 2. 禁止迴圈的泡沫排序 ----------
def swap_right(a, i):
    # 比較 a[i] 與 a[i+1]，大的往右邊（往下沉）
    if i + 1 < len(a) and a[i] > a[i + 1]:
        b = list(a)
        b[i], b[i + 1] = a[i + 1], a[i]
        return b
    return a


def bubble_pass(a, i, limit):
    # 一輪：由左往右遞迴比較到 limit-1，把前 limit 個中的最大值推到最右
    if i >= limit - 1:
        return a
    return bubble_pass(swap_right(a, i), i + 1, limit)


def bubble_sort(a, n=None):
    if n is None:
        n = len(a)
    if n <= 1:
        return list(a)
    return bubble_sort(bubble_pass(list(a), 0, n), n - 1)


# ---------- 3. 驗證 ----------
def check(a):
    expected = sorted(a)
    got = bubble_sort(a)
    return got == expected, got, expected


TESTS = [
    [5, 1, 4, 2, 8],
    [3, 2, 1],
    [1, 2, 3],
    [],
    [7],
    [2, 2, 1, 5, 1, 9, 4],
    [9, -3, 0, 7, -3, 12, 5],
]

print("泡沫排序（遞迴、無迴圈）驗證：")
# 隨機測資也用 my_map 產生，整份程式沒有任何 for / while
import random

random.seed(7)
STRESS = my_map(lambda _: my_map(lambda __: random.randint(-50, 50), range(13)), range(5))
results = my_map(check, TESTS + STRESS)
ok_list = my_map(lambda r: r[0], results)
my_map(lambda r: print("  ", r[1], "->", "OK" if r[0] else "FAIL（應為 " + str(r[2]) + "）"),
       results)
print("全部通過？", my_reduce(lambda a, b: a and b, ok_list, True))

demo = [5, 3, 8, 1, 9, 2]
sorted_demo = bubble_sort(demo)
print("\n範例", demo, "->", sorted_demo)

# 展示自製 map / filter / reduce
doubled = my_map(lambda v: v * 2, sorted_demo)
evens = my_filter(lambda v: v % 2 == 0, sorted_demo)
total = my_reduce(lambda a, b: a + b, sorted_demo)
biggest = my_reduce(lambda a, b: a if a > b else b, sorted_demo)
print("my_map(*2)      :", doubled)
print("my_filter(偶數) :", evens)
print("my_reduce(加總) :", total)
print("my_reduce(取最大):", biggest)
print("最大值與 sorted 一致？", biggest == max(sorted_demo))
