# 使用opencode
# Week 6 作業：Lambda Calculus 解譯器

這是一個**無型別 Lambda Calculus 解譯器**，會把每一步 β 化簡（beta reduction）完整印出來，
並自動辨識結果是不是 Church 數字或 Church 布林。

採用「**有名稱**」版本（`\x.\y.x`）

## 檔案

- `lambda.py` — 解譯器本體（Lexer / Parser / 化簡器 / 輸出）
- `math.lc` — 數學運算程式（加減乘除、次方、前趨、判斷為零）
- `logic.lc` — 布林邏輯與條件式程式

## 執行方式（Windows 直接用 `python`）

```bash
python lambda.py            # 跑內建示範
python lambda.py math.lc    # 跑數學運算程式
python lambda.py logic.lc   # 跑布林邏輯程式
```

## 語法

| 語法 | 意義 |
| --- | --- |
| `\x.M` / `λx.M` | 抽象（函數），可用 `->` 代替 `.` |
| `\x y.M` | 多參數語法糖，等於 `\x.\y.M` |
| `M N` | 應用（左結合） |
| `(M)` | 括號 |
| `NAME = M` | 具名定義（巨集展開，之後可用 `NAME`） |
| `# ...` | 註解 |
| 單獨一行 `M` | 求值並印出完整化簡過程 |

## 運作原理

1. **Lexer/Parser**：遞迴下降，建出 `Var` / `Abs` / `App` 三種節點。
2. **巨集展開**：把 `NAME` 代換成它的定義（會避開被 lambda 綁定的同名變數）。
3. **化簡**：採 **normal order（leftmost-outermost）** 逐步做一次 β 化簡，每步都印出整個 term。
4. **捕獲避免**：代入時若參數名會與自由變數衝突，自動改名（例如 `x` → `x1`）。
5. **結果辨識**：
   - Church 數字 `\f.\x.f (f (...x))` → 印出整數
   - `TRUE` / `FALSE` → 印出布林值

## 範例輸出（節錄）

```
================================================================
程式: PLUS TWO THREE
================================================================
[起始項]
    (\m.\n.\f.\x.m f (n f x)) (\f.\x.f (f x)) (\f.\x.f (f (f x)))
[β 化簡]
    1. (\n.\f.\x.(\f.\x.f (f x)) f (n f x)) (\f.\x.f (f (f x)))
    ...
    6. \f.\x.f (f (f (f (f x))))
[正規形式] (共 6 步 β 化簡)
    \f.\x.f (f (f (f (f x))))
    => Church 數字 5
```

## 定義的數學運算

| 名稱 | 定義 | 說明 |
| --- | --- | --- |
| `SUCC` | `\n.\f.\x.f (n f x)` | 後繼 S(n) |
| `PLUS` | `\m.\n.\f.\x.m f (n f x)` | 加法 |
| `MULT` | `\m.\n.\f.m (n f)` | 乘法 |
| `POW` | `\b.\e.e b` | 次方 |
| `PRED` | `\n.\f.\x.n (\g.\h.h (g f)) (\u.x) (\u.u)` | 前趨 n-1 |
| `SUB` | `\m.\n.n PRED m` | 減法（0 以下截為 0） |
| `ISZERO` | `\n.n (\x.FALSE) TRUE` | 是否為 0 |

## 驗證結果

執行 `python lambda.py math.lc` 得到的正規形式皆正確：

| 程式 | 結果 |
| --- | --- |
| `SUCC TWO` | 3 |
| `PLUS TWO THREE` | 5 |
| `MULT TWO THREE` | 6 |
| `POW TWO THREE` | 8 |
| `PRED THREE` | 2 |
| `SUB FIVE TWO` | 3 |
| `ISZERO ZERO` | TRUE |
| `ISZERO THREE` | FALSE（註：FALSE 與 Church 0 是同一個 term） |

## 備註

- 目前是「有名稱」版本；若要「無名稱」版本，可改用 de Bruijn index（`Var` 存整數層級），
  化簡時只需調整索引，能完全免除 α 改名，但輸出較不直觀。
- 未內建 Church 對、list 與 Y combinator 的範例；Y combinator 的遞迴（如階乘）
  在 normal order 下中間項會急速膨脹，建議另開示範並限制步數。
