# Week 6: 效能優化 & Merge 策略 完整教學系統

## 📚 系統概覽

一個包含完整教學、實踐案例、練習題和解答的 Week 6 學習體系。

**核心目標：**
- 實現 60%+ 記憶體優化
- 達成 100x+ 性能提升
- 掌握複雜的多表整合

---

## 📖 課程結構

### 第 1 部分：教學指南 (4 個文件)

#### Day 13: 記憶體優化完全指南 (28-32 KB)
**文件：** `Day13_Memory_Optimization_Guide.md`

涵蓋內容：
- Part 1: 記憶體分析 (2h) - info(), memory_usage(), 瓶頸識別
- Part 2: Dtype 優化 (2-3h) - downcasting, Categorical, 優化策略
- Part 3: Sparse 與 Chunking (2h) - SparseArray, chunksize 讀取
- 8 個實戰案例 - 記憶體減少 60%+ 實例
- 優化前後對比數據

**關鍵概念：**
- `df.memory_usage(deep=True)` 精確測量
- 時間戳優化：object → datetime64 (90% 減少)
- Category 轉換：唯一值 < 50 時 (80-98% 減少)
- Chunking 讀取大文件（避免內存溢出）

---

#### Day 14: 向量化完全指南 (28-32 KB)
**文件：** `Day14_Vectorization_Guide.md`

涵蓋內容：
- Part 1: 向量化基礎 (2h) - 避免迴圈、np.where
- Part 2: np.select 多條件 (2h) - 複雜邏輯向量化
- Part 3: 分箱與離散化 (2-3h) - pd.cut, pd.qcut
- 10 個實戰案例 - 速度提升 100x+ 實例
- for loop vs vectorization 效能對比

**關鍵概念：**
- `np.where(condition, value_if_true, value_if_false)` 簡單條件
- `np.select(conditions, choices, default)` 複雜條件
- `pd.cut()` 等寬分箱
- `pd.qcut()` 等頻分箱
- 性能提升：633x - 8897x

---

#### Day 15: Merge 策略完全指南 (25-28 KB)
**文件：** `Day15_Merge_Strategies_Guide.md`

涵蓋內容：
- Part 1: Merge 基礎 (2h) - 4 種 Join（inner/left/outer/cross）
- Part 2: Merge 進階技巧 (2h) - indicator, validate, suffixes
- Part 3: Concat 策略 (1-2h) - 垂直/水平合併
- 14 個實戰案例 - Olist 9 張表整合
- Excel 對照：VLOOKUP vs merge

**關鍵概念：**
- 4 種 Join：Inner, Left, Outer, Cross
- `indicator=True` 驗證匹配
- `validate='m:1'` 檢查關係
- `suffixes` 處理列名衝突
- Concat vs Merge 的區別

---

#### Day 16: 實踐整合 (20-25 KB)
**文件：** `Day16_Practice_Integration.md`

挑戰 & 項目：
- **挑戰 1**: 大文件記憶體優化 - 4GB 內處理 13.7GB 數據
- **挑戰 2**: 向量化操作 100x - 複雜商業規則
- **挑戰 3**: 高效多表合併 - Olist 9 張表整合
- **完整 Pipeline**: 實際應用示例

**實際技能：**
- 分塊讀取和即時優化
- 複雜向量化邏輯
- 多表高效合併
- 性能監控

---

### 第 2 部分：練習題系統 (4 個文件)

#### Exercise 10: 記憶體優化 - 8 題
**文件：** `exercises/Exercise_10_Memory_8_Questions.md`

- 🟢 入門題 (3 題)：分析、基礎轉換、識別 category
- 🟡 進階題 (3 題)：完整優化、整數縮小、Chunking
- 🔴 高級題 (2 題)：並行優化、流式處理

**技能驗證：**
- 正確分析記憶體使用
- 實現 80%+ 優化效果
- 處理大文件

---

#### Exercise 11: 向量化操作 - 10 題
**文件：** `exercises/Exercise_11_Vectorization_10_Questions.md`

- 🟢 入門題 (3 題)：np.where, pd.cut/qcut 基礎
- 🟡 進階題 (3 題)：np.select, 動態定價、性能對比
- 🔴 高級題 (4 題)：複雜規則、性能測試、完整 Pipeline

**技能驗證：**
- 掌握多種向量化方法
- 實現 100x+ 性能提升
- 避免使用 for 迴圈

---

#### Exercise 12: Merge 策略 - 14 題
**文件：** `exercises/Exercise_12_Merge_14_Questions.md`

- 🟢 入門題 (3 題)：Left/Inner/Outer Join
- 🟡 進階題 (3 題)：多表、衝突處理、驗證
- 🔴 高級題 (8 題)：Anti Join、自連接、流式合併、優化策略

**技能驗證：**
- 4 種 Join 類型
- 複雜多表整合
- 數據完整性驗證

---

#### Solutions: 前 5 題詳細解答
**文件：** `exercises/Solutions_Complete.md`

- Exercise 10 第 1-3 題完整解答
- Exercise 11 第 1-2 題完整解答
- 代碼 + 結果 + 解釋
- 常見錯誤與修正

---

### 第 3 部分：輔助文件 (3 個文件)

#### README.md (本文件)
系統總覽和使用指南

#### QUICK_START.md
快速開始 - 5 分鐘上手

#### INDEX.md
所有 32 題的分類索引

---

## 🎯 學習路徑

### 新手路徑 (2-3 天)

**第 1 天：記憶體優化 (Day 13)**
1. 閱讀 Part 1-2（~4 小時）
2. 完成 Exercise 10 題目 1-3（~1.5 小時）
3. 實踐案例 1-3（~1 小時）

**第 2 天：向量化操作 (Day 14)**
1. 閱讀 Part 1-2（~4 小時）
2. 完成 Exercise 11 題目 1-3（~1.5 小時）
3. 實踐案例 1-3（~1 小時）

**第 3 天：Merge 策略 & 整合 (Day 15-16)**
1. 閱讀 Day 15（~4 小時）
2. 完成 Exercise 12 題目 1-3（~1.5 小時）
3. 完成 Day 16 挑戰（~2 小時）

---

### 進階路徑 (1 周)

**週一：深入記憶體優化**
- Day 13 全部 + Exercise 10 全部（8 小時）

**週二：精通向量化**
- Day 14 全部 + Exercise 11 全部（8 小時）

**週三：掌握 Merge**
- Day 15 全部 + Exercise 12 全部（8 小時）

**週四：實踐整合**
- Day 16 + 完整 Pipeline 項目（8 小時）

**週五：複習 + 優化**
- 解答所有習題 + 性能調優（8 小時）

---

## 📊 教學數據

### 記憶體優化效果
| 表名 | 優化前 | 優化後 | 減少幅度 |
|------|-------|--------|--------|
| orders | 49.97 MB | 3.82 MB | 92.4% |
| customers | 6.18 MB | 4.95 MB | 19.9% |
| order_items | 8.43 MB | 1.54 MB | 81.7% |
| order_reviews | 12.56 MB | 2.18 MB | 82.6% |
| **合計** | **77.14 MB** | **12.49 MB** | **83.8%** |

### 向量化性能提升
| 操作 | For Loop | np.where | pd.cut | 倍數 |
|------|---------|---------|--------|------|
| 簡單分類 | 28.47s | 0.0045s | 0.0032s | 633x-8897x |
| 複雜條件 | N/A | 0.0078s | 0.0062s | 1200x+ |

### Merge 性能
| 操作 | 行數 | 耗時 | 結果 |
|------|------|------|------|
| orders + customers | 99,441 | 0.01s | ✓ |
| +order_items | 112,650 | 0.05s | ✓ |
| +reviews | 112,650 | 0.08s | ✓ |
| +products | 112,650 | 0.10s | ✓ |

---

## 📁 文件清單

### 教學文件 (4 個)
```
/week06_performance_merge/
├── Day13_Memory_Optimization_Guide.md      [31 KB]
├── Day14_Vectorization_Guide.md            [32 KB]
├── Day15_Merge_Strategies_Guide.md         [28 KB]
└── Day16_Practice_Integration.md           [24 KB]
                                    總計: 115 KB
```

### 練習文件 (4 個)
```
/week06_performance_merge/exercises/
├── Exercise_10_Memory_8_Questions.md       [18 KB]
├── Exercise_11_Vectorization_10_Questions.md [22 KB]
├── Exercise_12_Merge_14_Questions.md       [28 KB]
└── Solutions_Complete.md                   [15 KB]
                                    總計: 83 KB
```

### 輔助文件 (3 個)
```
/week06_performance_merge/
├── README.md (本文件)
├── QUICK_START.md
└── INDEX.md
                                    總計: ~20 KB
```

---

## 🚀 快速開始

### 安裝要求
```bash
# 必需
pandas >= 1.3.0
numpy >= 1.21.0

# 可選
psutil >= 5.8.0  # 監控記憶體
memory-profiler >= 0.60.0  # 詳細內存分析
```

### 驗證環境
```python
import pandas as pd
import numpy as np

print(f"Pandas: {pd.__version__}")
print(f"NumPy: {np.__version__}")

# 檢查 Olist 數據
import os
data_path = '/home/justin/web-projects/excel-python-data-analysis/week03-06_pandas-advanced/data/'
files = os.listdir(data_path)
print(f"找到 {len(files)} 個數據文件")
```

### 第一個練習
```python
# 執行第一個練習 (Exercise 10, 題目 1)
import pandas as pd

orders = pd.read_csv(
    '/home/justin/web-projects/excel-python-data-analysis/week03-06_pandas-advanced/data/olist_orders_dataset.csv'
)

memory = orders.memory_usage(deep=True).sum() / 1024**2
print(f"記憶體使用: {memory:.2f} MB")
```

---

## 💡 學習建議

### 1. 按順序學習
- **不要跳過** Day 13-15，它們是基礎
- Day 16 需要 Day 13-15 的知識

### 2. 邊讀邊練
- 讀完每個 Part（1-2h）立即做練習（30 分鐘）
- 不要一次讀完整個教學

### 3. 重點掌握
- **Day 13**：memory_usage(deep=True) + Dtype 轉換
- **Day 14**：np.where + np.select (避免 for 迴圈)
- **Day 15**：4 種 Join + indicator/validate
- **Day 16**：完整 Pipeline 設計

### 4. 實踐很關鍵
- 在自己的數據上應用技術
- 對比優化前後
- 寫下性能數據

### 5. 性能測試
```python
import time

# 測試你的優化
start = time.time()
# 你的代碼
result = your_function(data)
elapsed = time.time() - start

print(f"耗時: {elapsed:.4f}s")
```

---

## ❓ 常見問題

### Q: 我應該從哪裡開始？
**A:** 從 QUICK_START.md 開始（5 分鐘），然後按順序完成 Day 13-16。

### Q: 需要多長時間完成？
**A:**
- 快速通過：2-3 天
- 深度學習：1 周
- 完全掌握：2 周（包括自己的項目實踐）

### Q: 練習題有答案嗎？
**A:** 是的！Solutions_Complete.md 包含前 5 題的完整解答。其他題目的解答可查看每個教學文件的案例。

### Q: 我可以跳過某個部分嗎？
**A:** 不建議。但如果時間緊張：
- 最少：Day 13 + Day 14（必須）
- 推薦：Day 13-15（完整）
- 最優：Day 13-16（最全面）

### Q: 這個課程對我有幫助嗎？
**A:** 如果你：
- ✓ 處理 GB 級數據
- ✓ 需要優化代碼性能
- ✓ 要整合多個數據源
- ✓ 想成為 Pandas 專家

那麼是的，非常有幫助！

---

## 📈 進度跟踪

### 完成檢查清單

**Day 13: 記憶體優化**
- [ ] 理解 memory_usage(deep=True)
- [ ] 掌握 Dtype 轉換
- [ ] 實現 80%+ 優化
- [ ] 完成 Exercise 10

**Day 14: 向量化**
- [ ] 掌握 np.where
- [ ] 掌握 np.select
- [ ] 掌握 pd.cut/qcut
- [ ] 完成 Exercise 11
- [ ] 達成 100x+ 性能提升

**Day 15: Merge 策略**
- [ ] 掌握 4 種 Join
- [ ] 使用 indicator/validate
- [ ] 處理列名衝突
- [ ] 完成 Exercise 12

**Day 16: 實踐整合**
- [ ] 完成挑戰 1（記憶體優化）
- [ ] 完成挑戰 2（向量化操作）
- [ ] 完成挑戰 3（多表合併）
- [ ] 運行完整 Pipeline

---

## 🔗 相關資源

### Pandas 官方文檔
- [Memory Usage](https://pandas.pydata.org/docs/reference/api/pandas.DataFrame.memory_usage.html)
- [Data Types](https://pandas.pydata.org/docs/user_guide/basics.html#dtypes)
- [Merge Join Concat](https://pandas.pydata.org/docs/user_guide/merging.html)

### NumPy 文檔
- [numpy.where](https://numpy.org/doc/stable/reference/generated/numpy.where.html)
- [numpy.select](https://numpy.org/doc/stable/reference/generated/numpy.select.html)

### 性能分析工具
- [memory-profiler](https://pypi.org/project/memory-profiler/)
- [line-profiler](https://pypi.org/project/line-profiler/)
- [cProfile](https://docs.python.org/3/library/profile.html)

---

## 📞 支持

有問題？查看：
1. 每個教學文件的"常見陷阱"部分
2. Solutions_Complete.md 的錯誤修正
3. Exercise 的評分標準和示例

---

## ⭐ 致謝

本教學系統基於 Olist 真實電商數據集，包含完整的實際應用場景。

**最後更新：** 2025-12-11
**版本：** 1.0
**狀態：** ✓ 完成

---

**準備好開始了嗎？👉 [進入 QUICK_START.md](QUICK_START.md)**
