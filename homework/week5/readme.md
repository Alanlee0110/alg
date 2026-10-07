# Week 5 作業

執行方式（Windows 直接用 `python`）：

```bash
python week5/hanoi.py
python week5/sym_diff.py
python week5/bubble_sort.py
```

## 1. 河內塔：遞迴與禁止遞迴 [hanoi.py]

- 遞迴解：`hanoi_recursive(n, src, dst, aux)`，先搬 n-1 層到中柱、搬自己、再把 n-1 層搬到終點。
- 禁止遞迴解：`hanoi_iterative` 用 list 當顯式堆疊，狀態為 `(盤數, 起點, 終點, 輔助柱, 是否展開)`，以「先壓第三步、再壓標記、最後壓第一步」的順序模擬後序走訪。
- 驗證：n=4 兩解 15 步完全相同；n=12 兩解 4095 步完全相同，並用三根柱子的模擬確認每步都合法、終點是完整的塔。

## 2. 符號微分 sym_diff(expr) [sym_diff.py]

表達式以樹狀 tuple 表示（`("+" , a, b)`、`("^", a, n)`、`("sin", a)` 等），
`sym_diff` 遞迴套用：

- 加減：各項分別微分
- 乘法：乘法法則 `(uv)' = u'v + uv'`
- 除法：商法則 `(u/v)' = (u'v - uv') / v^2`
- 幂次：`(u^n)' = n u^(n-1) u'`，`a^b` 一般式走 `e^(b ln a)`
- 連鎖律：`(sin u)' = cos u · u'`

另有遞迴的 `simplify` 化簡與 `eval_expr` 求值，
用中心差分的數值微分交叉驗證，五組測試誤差皆 < 1e-9。

## 3. 自製 map/filter/reduce + 禁止迴圈的泡沫排序 [bubble_sort.py]

- `my_map` / `my_filter` / `my_reduce` 全部以遞迴實作（遞迴定義就是函式語言的原始定義）。
- 泡沫排序：`bubble_pass(a, i, limit)` 由左往右遞迴做一輪相鄰交換（大值下沉），
  `bubble_sort(a, n)` 每輪處理完就把最大值固定在末端，再遞迴處理前 n-1 個。
- 整份程式沒有任何 `for` / `while`，測資（含 5 組隨機清單）也用 `my_map` 產生，
  全部與 `sorted` 比對通過。
