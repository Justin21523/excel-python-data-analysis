# INDEX: Week 6 完整題目索引

## 📋 總覽

| 部分 | 文件 | 題目 | 難度 | 總計 |
|------|------|------|------|------|
| Exercise 10 | Memory | 8 | 🟢🟡🔴 | 8 |
| Exercise 11 | Vectorization | 10 | 🟢🟡🔴 | 10 |
| Exercise 12 | Merge | 14 | 🟢🟡🔴 | 14 |
| **合計** | - | 32 | - | **32** |

---

## Exercise 10: 記憶體優化 (8 題)

### 🟢 入門題 (Easy) - 3 題

| # | 題目 | 文件 | 內容 |
|---|------|------|------|
| E10-1 | 分析 orders 表的記憶體使用 | Exercise_10_Memory_8_Questions.md | 使用 memory_usage(deep=True) 分析，找出最耗記憶體的列 |
| E10-2 | 簡單的 Dtype 轉換 | Exercise_10_Memory_8_Questions.md | 時間戳優化（object → datetime64），計算優化百分比 |
| E10-3 | 識別應該使用 category 的列 | Exercise_10_Memory_8_Questions.md | 掃描所有列，找出適合轉為 category 的列 |

**入門技能：**
- ✓ memory_usage(deep=True) 使用
- ✓ Dtype 基本轉換
- ✓ 記憶體分析

---

### 🟡 進階題 (Medium) - 3 題

| # | 題目 | 文件 | 內容 |
|---|------|------|------|
| E10-4 | 完整的 DataFrame 優化 | Exercise_10_Memory_8_Questions.md | 編寫 optimize_dataframe() 函數，自動優化任何 DataFrame |
| E10-5 | 整數類型縮小 | Exercise_10_Memory_8_Questions.md | 分析 int64 列，選擇最小的合適整數類型 |
| E10-6 | Chunking 處理大文件 | Exercise_10_Memory_8_Questions.md | 分塊讀取，計算記憶體節省效果 |

**進階技能：**
- ✓ downcast_integer 實現
- ✓ Chunking 讀取
- ✓ 函數抽象

---

### 🔴 高級題 (Hard) - 2 題

| # | 題目 | 文件 | 內容 |
|---|------|------|------|
| E10-7 | 並行優化 + 記憶體監控 | Exercise_10_Memory_8_Questions.md | 完整的 Pipeline，多個表的批量優化 + 峰值監控 |
| E10-8 | 大文件處理 + 即時分析 | Exercise_10_Memory_8_Questions.md | 流式處理，分塊讀取、優化、實時統計 |

**高級技能：**
- ✓ Pipeline 設計
- ✓ 實時監控 (psutil)
- ✓ 流式處理

---

## Exercise 11: 向量化操作 (10 題)

### 🟢 入門題 (Easy) - 3 題

| # | 題目 | 文件 | 內容 |
|---|------|------|------|
| E11-1 | 基礎 np.where - 價格分類 | Exercise_11_Vectorization_10_Questions.md | 簡單的 3 層分類，計算統計信息 |
| E11-2 | np.where 應用 - 評分狀態 | Exercise_11_Vectorization_10_Questions.md | 4 層分類（含 NaN 處理），統計各類別 |
| E11-3 | pd.cut - 等寬分箱 | Exercise_11_Vectorization_10_Questions.md | 5 個等寬區間，計算訂單數、平均價格、銷售額 |

**入門技能：**
- ✓ np.where 基本使用
- ✓ pd.cut 基本使用
- ✓ NaN 處理

---

### 🟡 進階題 (Medium) - 3 題

| # | 題目 | 文件 | 內容 |
|---|------|------|------|
| E11-4 | np.select - 複雜條件 | Exercise_11_Vectorization_10_Questions.md | 5 級優先級分配（多條件），統計分佈 |
| E11-5 | 向量化計算 - 動態定價 | Exercise_11_Vectorization_10_Questions.md | 條件加減價格，計算銷售額變化 |
| E11-6 | pd.qcut - 等頻分箱 + 客戶分層 | Exercise_11_Vectorization_10_Questions.md | 四分位分層，計算客戶統計 (平均訂單值、評分、回購率) |

**進階技能：**
- ✓ np.select 使用
- ✓ pd.qcut 使用
- ✓ 向量化計算

---

### 🔴 高級題 (Hard) - 4 題

| # | 題目 | 文件 | 內容 |
|---|------|------|------|
| E11-7 | 複雜業務規則 - np.select + 計算 | Exercise_11_Vectorization_10_Questions.md | 多層折扣邏輯（基礎 + 額外 + 上限），統計效果 |
| E11-8 | 性能測試 - For Loop vs Vectorization | Exercise_11_Vectorization_10_Questions.md | 對比三種方法 (for loop, np.where, np.select) |
| E11-9 | 多維度向量化特徵工程 | Exercise_11_Vectorization_10_Questions.md | 創建 10 個向量化特徵 (分類、分箱、計算等) |
| E11-10 | 完整的分析 Pipeline (向量化版) | Exercise_11_Vectorization_10_Questions.md | 數據準備 → 特徵工程 → 分析 → 報告 |

**高級技能：**
- ✓ 複雜條件邏輯
- ✓ 性能對比測試
- ✓ 完整 Pipeline 設計

---

## Exercise 12: Merge 策略 (14 題)

### 🟢 入門題 (Easy) - 3 題

| # | 題目 | 文件 | 內容 |
|---|------|------|------|
| E12-1 | Left Join - 訂單 + 客戶 | Exercise_12_Merge_14_Questions.md | 基本 LEFT JOIN，驗證行數和缺失值 |
| E12-2 | Inner Join - 僅保留完整記錄 | Exercise_12_Merge_14_Questions.md | INNER JOIN，計算篩選率 |
| E12-3 | Outer Join - 查找不匹配的記錄 | Exercise_12_Merge_14_Questions.md | OUTER JOIN with indicator，統計 both/left_only/right_only |

**入門技能：**
- ✓ 3 種基本 Join
- ✓ indicator 使用
- ✓ 數據驗證

---

### 🟡 進階題 (Medium) - 3 題

| # | 題目 | 文件 | 內容 |
|---|------|------|------|
| E12-4 | 多表連續合併 | Exercise_12_Merge_14_Questions.md | 4 個表的順序合併，追蹤行數變化 |
| E12-5 | 處理列名衝突 (suffixes) | Exercise_12_Merge_14_Questions.md | 使用 suffixes 處理重複列名 |
| E12-6 | 使用 indicator 驗證匹配 | Exercise_12_Merge_14_Questions.md | OUTER JOIN + indicator，驗證數據完整性 |

**進階技能：**
- ✓ 多表合併
- ✓ suffixes 參數
- ✓ 驗證策略

---

### 🔴 高級題 (Hard) - 8 題

| # | 題目 | 文件 | 內容 |
|---|------|------|------|
| E12-7 | 多鍵合併 | Exercise_12_Merge_14_Questions.md | 使用多個鍵進行合併，使用 validate 檢查關係 |
| E12-8 | Anti Join - 查找缺失配對 | Exercise_12_Merge_14_Questions.md | OUTER JOIN + 篩選，找無評論訂單和無銷售產品 |
| E12-9 | validate 參數 - 檢查關係完整性 | Exercise_12_Merge_14_Questions.md | 驗證 1:1, 1:m, m:1, m:m 關係 |
| E12-10 | Concat - 垂直堆疊 + 水平連接 | Exercise_12_Merge_14_Questions.md | concat axis=0 和 axis=1 的應用 |
| E12-11 | 自連接 (Self-join) - 查找重複購買客戶 | Exercise_12_Merge_14_Questions.md | 表與自己合併，找出重複購買配對 |
| E12-12 | 複雜的多表合併 Pipeline | Exercise_12_Merge_14_Questions.md | 6 表整合 Pipeline，完整驗證和報告 |
| E12-13 | 多層次 Merge 優化 | Exercise_12_Merge_14_Questions.md | 優化合併順序和方法，監控記憶體和性能 |
| E12-14 | 超大規模合併 + 流式處理 | Exercise_12_Merge_14_Questions.md | 分塊讀取 + 增量合併 + 聚合統計 |

**高級技能：**
- ✓ Anti Join 實現
- ✓ validate 驗證
- ✓ 自連接
- ✓ Concat 應用
- ✓ Pipeline 設計
- ✓ 流式處理

---

## 🎯 按難度分類

### 所有 🟢 入門題 (9 題)

1. E10-1: 分析記憶體使用
2. E10-2: Dtype 轉換
3. E10-3: Category 識別
4. E11-1: np.where 價格分類
5. E11-2: np.where 評分狀態
6. E11-3: pd.cut 等寬分箱
7. E12-1: Left Join
8. E12-2: Inner Join
9. E12-3: Outer Join

**預計耗時：** 6-8 小時
**適合：** 初學者快速掌握基礎

---

### 所有 🟡 進階題 (9 題)

1. E10-4: 完整 DataFrame 優化
2. E10-5: 整數類型縮小
3. E10-6: Chunking 處理
4. E11-4: np.select 複雜條件
5. E11-5: 向量化計算
6. E11-6: pd.qcut 分層
7. E12-4: 多表連續合併
8. E12-5: 列名衝突處理
9. E12-6: indicator 驗證

**預計耗時：** 8-10 小時
**適合：** 掌握進階技術

---

### 所有 🔴 高級題 (14 題)

1. E10-7: 並行優化 + 監控
2. E10-8: 流式處理 + 實時分析
3. E11-7: 複雜業務規則
4. E11-8: 性能測試對比
5. E11-9: 多維度特徵工程
6. E11-10: 完整分析 Pipeline
7. E12-7: 多鍵合併
8. E12-8: Anti Join
9. E12-9: validate 驗證
10. E12-10: Concat 應用
11. E12-11: 自連接
12. E12-12: 6 表整合
13. E12-13: Merge 優化
14. E12-14: 流式合併

**預計耗時：** 12-15 小時
**適合：** 實現完整的實戰應用

---

## 按主題分類

### 記憶體優化相關 (8 題)
- E10-1: 分析記憶體使用
- E10-2: Dtype 轉換
- E10-3: Category 識別
- E10-4: 完整優化
- E10-5: 整數縮小
- E10-6: Chunking
- E10-7: 並行優化
- E10-8: 流式處理

---

### 向量化相關 (10 題)
- E11-1: np.where 基礎
- E11-2: np.where 應用
- E11-3: pd.cut 分箱
- E11-4: np.select 複雜條件
- E11-5: 向量化計算
- E11-6: pd.qcut 分層
- E11-7: 複雜業務規則
- E11-8: 性能測試
- E11-9: 多維度特徵
- E11-10: 完整 Pipeline

---

### Merge 相關 (14 題)
- E12-1: Left Join
- E12-2: Inner Join
- E12-3: Outer Join
- E12-4: 多表合併
- E12-5: suffixes 處理
- E12-6: indicator 驗證
- E12-7: 多鍵合併
- E12-8: Anti Join
- E12-9: validate 驗證
- E12-10: Concat 應用
- E12-11: 自連接
- E12-12: 6 表整合
- E12-13: Merge 優化
- E12-14: 流式合併

---

## 按時間規劃

### 快速通過 (3 天)

**第 1 天 (Day 13):**
- E10-1, E10-2, E10-3 (3h)
- E10-4, E10-5 (2h)

**第 2 天 (Day 14):**
- E11-1, E11-2, E11-3 (2.5h)
- E11-4, E11-5, E11-6 (3h)

**第 3 天 (Day 15-16):**
- E12-1, E12-2, E12-3, E12-4 (2h)
- E12-5, E12-6, E12-12, E12-14 (4h)

---

### 標準學習 (1 周)

**週一：** E10-1 到 E10-5 (5h)
**週二：** E10-6 到 E10-8, E11-1 到 E11-3 (7h)
**週三：** E11-4 到 E11-6, E11-7 到 E11-10 (8h)
**週四：** E12-1 到 E12-6 (6h)
**週五：** E12-7 到 E12-14 (8h)

---

### 深度掌握 (2 周)

**第 1 周：** 所有入門題 (9h) + 進階題的一半 (4h)
**第 2 周：** 所有進階題 (10h) + 所有高級題 (15h)

---

## 📌 標籤索引

### 按數據量規模

**小規模 (< 10K 行):**
- E10-1, E10-2, E10-3, E12-1, E12-2, E12-3

**中規模 (10K-100K 行):**
- E10-4, E10-5, E11-1 到 E11-6, E12-4 到 E12-11

**大規模 (> 100K 行):**
- E10-6, E10-7, E10-8, E11-10, E12-12, E12-13, E12-14

---

### 按核心技能

**性能提升相關:**
- E11-7, E11-8, E12-13

**記憶體管理相關:**
- E10-4, E10-6, E10-7, E10-8

**數據驗證相關:**
- E12-6, E12-9

**Pipeline 設計相關:**
- E10-7, E11-10, E12-12, E12-14

---

## ✅ 完成標記

### 推薦完成順序

1. **基礎三角**（必做）
   - [ ] E10-1, E10-2, E10-3
   - [ ] E11-1, E11-2, E11-3
   - [ ] E12-1, E12-2, E12-3

2. **進階六角**（強烈推薦）
   - [ ] E10-4, E10-5, E10-6
   - [ ] E11-4, E11-5, E11-6
   - [ ] E12-4, E12-5, E12-6

3. **高級複合**（深度學習）
   - [ ] E10-7, E10-8
   - [ ] E11-7, E11-8, E11-9, E11-10
   - [ ] E12-7, E12-8, E12-9, E12-10, E12-11, E12-12, E12-13, E12-14

---

## 📞 如何使用本索引

1. **找你感興趣的題目** → 查看題號 → 打開對應文件
2. **按難度漸進** → 先做🟢再🟡最後🔴
3. **按主題深入** → 用"按主題分類"快速找相關題
4. **按時間規劃** → 根據你的時間選擇學習路徑

---

## 🎯 學習目標檢查

### 完成所有 32 題後，你應該能夠：

- [ ] 分析和優化任何 DataFrame 的記憶體（60%+ 減少）
- [ ] 編寫完全向量化的代碼（避免所有迴圈）
- [ ] 實現 100x+ 的性能提升
- [ ] 高效整合 5+ 個數據表
- [ ] 驗證和監控 merge 的完整性
- [ ] 設計和實現完整的數據 Pipeline
- [ ] 在 4GB 記憶體內處理 13GB+ 數據
- [ ] 應用複雜的商業邏輯到數據分析

如果都能做到，**恭喜！你已經成為 Pandas 高手！**

---

**開始選擇你的學習路徑：**
- 快速通過？👉 [選擇快速路徑](#快速通過-3-天)
- 深度學習？👉 [選擇深度路徑](#深度掌握-2-周)
- 看推薦順序？👉 [完成標記](#完成標記)

---

**最後更新：** 2025-12-11 | **版本：** 1.0
