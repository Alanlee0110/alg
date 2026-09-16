# AGENTS.md

陳鍾誠《演算法》課程教材（115 學年下），內容為繁體中文。沒有 build / test / lint 工具鏈；程式都是直接執行的教學腳本（`python3 xxx.py`）。

## 兩大區域

- `01-複雜度` `02-方法` `03-領域` `04-理論` — 教科書章節（Markdown + 教學 Python）。
- `_wiki/` — 演算法故事 Wiki（目前主要維護對象）；`_more/` 是其創作源料（`story/chat.md`、`story/list.md`）與舊內容。
- `04-理論/02-數學/_ai/*` 等子專案自帶 `AGENTS.md`，勿混入本區規範。

## `_wiki/` 結構

- `algorithms/` — 92 篇故事頁（每演算法/事故一頁）
- `concepts/` — 概念頁；`categories/` — 主題分類頁（`history.md` 依時代分組）
- `index.md` — 主索引（分類表 + 全部分組清單）、`log.md` — 變更日誌

## `_wiki/` 寫作規則

- 筆法要「趣味點」優先、像說故事，不要寫成教科書定義。
- **禁止 Obsidian `[[wikilinks]]`**；一律用 GitHub 相容的相對 Markdown 連結：
  - `algorithms/` 內互連：`[文字](sibling.md)`
  - 到概念/分類：`[文字](../concepts/xxx.md)`、`[文字](../categories/xxx.md)`
  - 從 `categories/` 到故事：`[文字](../algorithms/xxx.md)`
  - 目標必須存在；禁止 `](..)`、`](.)` 指到目錄本身
- 每頁格式：`# 標題` 後接 `**領域**：[..](../categories/xxx.md) | **年代**：yyyy`（`**趣味點**` 為可選）。
- 新增故事頁必須同步更新 `index.md` 與 `log.md`（每次 ingest 一筆）。

## 驗證：修改後必跑

```bash
cd _wiki && python3 - <<'EOF'
import os, re, glob
bad = []
for f in glob.glob("**/*.md", recursive=True):
    base = os.path.dirname(f)
    for m in re.finditer(r"\[[^\]]*\]\(([^)]+)\)", open(f, encoding="utf-8").read()):
        t = m.group(1).strip()
        if t.startswith("http") or t.startswith("#"):
            continue
        if not os.path.exists(os.path.normpath(os.path.join(base, t))):
            bad.append((f, t))
print("All relative links OK" if not bad else "\n".join(f"BROKEN: {f} -> {t}" for f, t in bad))
EOF
```

## 注意

- `_more/story/AGENTS.md` 是舊版規範（路徑仍寫 `wiki/`），實際成品位於根目錄 `_wiki/`，以其出入為準。
- 已知不一致：`_wiki/index.md` 目前未收錄 `algorithms/dartmouth-ai.md`。