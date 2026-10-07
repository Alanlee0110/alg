# 使用gemini
https://share.gemini.google/7MRuozXNajwn

# 迭代法

迭代法的定義是從一個初始的猜測值，利用重複的公式去逼進正確答案


## 二維不動點迭代法

用來求解包含兩個變數的非線性聯立方程式

把 F(x,y) = 0、G(x,y) = 0 改寫成 x = f(x,y)、y = g(x,y)，再反覆套用。
同一組方程的不同改寫會決定收斂或發散，收斂與否看 Jacobian 的譜半徑是否小於 1。

範例程式：[iterative_2d.py] 一維對照：[iterative_ex.py]

## 牛頓法