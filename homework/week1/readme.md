# 使用claude
# Week 1：計算 2^n 的五種方法

本週作業用五種不同的方法計算 2 的 n 次方，並用 `datetime` 記錄執行時間，用來比較不同演算法的時間複雜度。

每個程式的結構相同：定義一個函式，設定 `n = 100`，印出計算結果和花費的時間。

## 檔案說明

| 檔案 | 函式 | 方法 | 時間複雜度 |
|------|------|------|-----------|
| [power2n.py](power2n.py) | `power2n(n)` | 直接使用 Python 的次方運算子 `2**n` | 約 O(log n)（由直譯器實作） |
| [power2n_shift.py](power2n_shift.py) | `power2n_shift(n)` | 位元左移 `1 << n`，把 1 往左移 n 位就等於 2^n | O(1)～O(n)（取決於大數位元長度） |
| [power2n_a.py](power2n_a.py) | `power2n_2a(n)` | 遞迴：`2^n = 2^(n-1) + 2^(n-1)`，每層呼叫自己**兩次** | **O(2^n)** |
| [power2n_b.py](power2n_b.py) | `power2n_2b(n)` | 遞迴：`2^n = 2 * 2^(n-1)`，每層只呼叫自己一次 | O(n) |
| [power2n_3.py](power2n_3.py) | `power2n_3(n)` | 與 `power2n_a` 相同的遞迴式，但加上**查表（memoization）**，把算過的結果存在 `pow` 陣列中 | O(n) |

### power2n.py
最直接的寫法，使用內建的 `**` 運算子。

### power2n_shift.py
利用二進位特性：`1 << n` 的結果就是 2^n，速度非常快。

### power2n_a.py
樸素的雙重遞迴。因為 `power2n_2a(n-1)` 被重複計算兩次，總呼叫次數約為 2^(n+1)，呈指數成長。
> ⚠️ 當 `n = 100` 時需要約 2^101 次函式呼叫，實際上**跑不完**。想觀察執行時間請把 `n` 改小（例如 20～25）。

### power2n_b.py
把兩次遞迴呼叫合併成 `2 * power2n_2b(n-1)`，只需 n 次呼叫，變成線性時間。
> 注意：遞迴深度為 n，若 n 超過 Python 預設遞迴上限（約 1000）會發生 `RecursionError`。

### power2n_3.py
保留 `power2n_a` 的遞迴式，但用陣列 `pow`（大小 10000）記住已算過的值，`pow[0] = 1`、`pow[1] = 2` 為初始值。每個 `n` 只會真正計算一次，因此從指數時間降為線性時間。這是**動態規劃（Dynamic Programming）**中「記憶化」的概念。
> 注意：同樣受遞迴深度限制，且 n 不可超過 9999（陣列大小）。

## 重點結論

- 同樣的數學式子，寫法不同，效率可能從 O(n) 變成 O(2^n)。
- 重複計算是指數時間的主因，**查表／記憶化**可以消除重複計算。
- 實務上直接用 `2**n` 或 `1 << n` 最快。

## 執行方式

```bash
python power2n.py
python power2n_shift.py
python power2n_b.py
python power2n_3.py
python power2n_a.py   # n=100 會跑不完，請先改小 n
```
