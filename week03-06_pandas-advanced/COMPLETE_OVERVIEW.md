# 🎓 Week 3-6: pandas 進階實戰完整系統總覽

> ✅ **系統狀態：100% 就緒！**
>
> 📦 **總檔案：** 28 個 Notebook + 108+ 練習題 + 5 個整合專案
>
> ⏱️ **總時數：** 80-100 小時（密集訓練 4 週）
>
> 📊 **資料集：** Olist 電商 121MB（9 張表，100K 訂單）

---

## 📋 系統架構概覽

```
Week 3-6 pandas 進階實戰系統
├── Week 3 (20-25h): MultiIndex & 複雜 GroupBy
│   ├── 7 個 Notebook
│   ├── 37 個練習題
│   └── 1 個整合專案（5-7h）
│
├── Week 4 (20-25h): 時間序列 & 視窗函數
│   ├── 7 個 Notebook
│   ├── 32 個練習題
│   └── 1 個整合專案（5-7h）
│
├── Week 5 (20-25h): Apply/Transform/Agg 深度應用
│   ├── 7 個 Notebook
│   ├── 37 個練習題
│   └── 1 個整合專案（3-5h）
│
├── Week 6 (20-25h): 效能優化 & 合併策略
│   ├── 7 個 Notebook
│   ├── 32 個練習題
│   └── 1 個整合專案（3-5h）
│
└── Capstone Project (10-15h): 端到端電商分析系統
    ├── 資料載入與清洗
    ├── 多表整合（9 張表）
    ├── 多維度分析（MultiIndex + GroupBy + Pivot）
    ├── 時間序列分析（Resample + Rolling + MoM/YoY）
    ├── 客戶分析（RFM + Apply/Transform/Agg）
    └── 效能優化與報表輸出
```

---

## 🗂️ 完整檔案清單

### 📁 核心文檔（5 個）
1. **START_HERE.md** (17KB) - ⭐ 快速啟動指南
2. **COMPLETE_OVERVIEW.md** (本文件) - 完整系統總覽
3. **DATASET_GUIDE.md** - Olist 資料集使用指南
4. **QUICK_REFERENCE.md** - pandas 進階速查表
5. **GLOSSARY.md** - 術語表（Excel → pandas）

### 📁 Week 3: MultiIndex & 複雜 GroupBy（15 個檔案）

#### 🔵 教學文檔（4 個）
1. **Day01_MultiIndex_Complete_Guide.md** (25KB) - ⭐ MultiIndex 完全掌握
2. **Day02_GroupBy_Advanced_Guide.md** (22KB) - GroupBy 進階聚合
3. **Day03_Pivot_Reshape_Guide.md** (20KB) - 透視表與重塑
4. **Day04_Practice_Integration.md** (18KB) - 整合練習指南

#### 🟢 Notebook（7 個）
1. **01_multiindex_basics.ipynb** ⭐ - MultiIndex 基礎（2h）
2. **02_multiindex_slicing_advanced.ipynb** - 進階切片（2h）
3. **03_groupby_aggregation.ipynb** ⭐ - GroupBy 聚合（2h）
4. **04_groupby_transform_filter.ipynb** - Transform & Filter（2h）
5. **05_pivot_stack_unstack.ipynb** ⭐ - 透視表（2h）
6. **06_melt_wide_to_long.ipynb** - Melt 轉換（2h）
7. **07_week03_final_project.ipynb** - 整合專案（5-7h）

#### 🟡 練習題（4 個）
1. **Exercise_01_MultiIndex_12_Questions.md** - 12 題（基礎 6 + 進階 6）
2. **Exercise_02_GroupBy_15_Questions.md** - 15 題（基礎 5 + 進階 5 + 挑戰 5）
3. **Exercise_03_Pivot_10_Questions.md** - 10 題（基礎 4 + 進階 4 + 挑戰 2）
4. **Solutions_Complete.md** - 完整解答

---

### 📁 Week 4: 時間序列 & 視窗函數（15 個檔案）

#### 🔵 教學文檔（4 個）
1. **Day05_DateTime_Mastery_Guide.md** (23KB) - DateTime 完全掌握
2. **Day06_Resample_Rolling_Guide.md** (24KB) - 重採樣與移動視窗
3. **Day07_Time_Comparison_Guide.md** (21KB) - 時間比較（MoM/YoY）
4. **Day08_Practice_Integration.md** (19KB) - 整合練習指南

#### 🟢 Notebook（7 個）
1. **08_datetime_fundamentals.ipynb** ⭐ - DateTime 基礎（2h）
2. **09_timedelta_dateoffset.ipynb** - 時間差與偏移（2h）
3. **10_resample_frequency.ipynb** ⭐ - 重採樣（2h）
4. **11_rolling_windows.ipynb** - 移動視窗（2.5h）
5. **12_time_comparison_yoy_mom.ipynb** ⭐ - 同期比較（2h）
6. **13_seasonal_decomposition.ipynb** - 季節性分解（2.5h）
7. **14_week04_final_project.ipynb** - 整合專案（5-7h）

#### 🟡 練習題（4 個）
1. **Exercise_04_DateTime_10_Questions.md** - 10 題
2. **Exercise_05_Resample_Rolling_12_Questions.md** - 12 題
3. **Exercise_06_Time_Comparison_10_Questions.md** - 10 題
4. **Solutions_Complete.md** - 完整解答

---

### 📁 Week 5: Apply/Transform/Agg 深度應用（15 個檔案）

#### 🔵 教學文檔（4 個）
1. **Day09_Apply_Deep_Dive_Guide.md** (26KB) - Apply 深度探索
2. **Day10_Transform_Guide.md** (23KB) - Transform 組內計算
3. **Day11_Agg_Named_Guide.md** (22KB) - Agg 命名聚合
4. **Day12_Practice_Integration.md** (18KB) - 整合練習指南

#### 🟢 Notebook（7 個）
1. **15_apply_series_dataframe.ipynb** ⭐ - Apply 基礎（2h）
2. **16_apply_performance.ipynb** - Apply 效能優化（2h）
3. **17_transform_group_calc.ipynb** ⭐ - Transform 組內計算（2h）
4. **18_agg_named_aggregation.ipynb** ⭐ - 命名聚合（2h）
5. **19_custom_aggregation.ipynb** - 自訂聚合函數（2h）
6. **20_rfm_analysis.ipynb** - RFM 客戶分析（3h）
7. **21_week05_final_project.ipynb** - 整合專案（3-5h）

#### 🟡 練習題（4 個）
1. **Exercise_07_Apply_15_Questions.md** - 15 題
2. **Exercise_08_Transform_12_Questions.md** - 12 題
3. **Exercise_09_Agg_10_Questions.md** - 10 題
4. **Solutions_Complete.md** - 完整解答

---

### 📁 Week 6: 效能優化 & 合併策略（15 個檔案）

#### 🔵 教學文檔（4 個）
1. **Day13_Memory_Optimization_Guide.md** (24KB) - 記憶體優化
2. **Day14_Vectorization_Guide.md** (25KB) - 向量化運算
3. **Day15_Merge_Strategies_Guide.md** (23KB) - Merge 策略
4. **Day16_Practice_Integration.md** (19KB) - 整合練習指南

#### 🟢 Notebook（7 個）
1. **22_memory_profiling.ipynb** ⭐ - 記憶體分析（2h）
2. **23_dtype_optimization.ipynb** ⭐ - Dtype 優化（2h）
3. **24_vectorization_basics.ipynb** - 向量化基礎（2h）
4. **25_np_select_where.ipynb** ⭐ - np.select/where（2h）
5. **26_merge_join_types.ipynb** ⭐ - Merge 類型（2h）
6. **27_merge_validation.ipynb** - Merge 驗證（2h）
7. **28_week06_final_project.ipynb** - 整合專案（3-5h）

#### 🟡 練習題（4 個）
1. **Exercise_10_Memory_10_Questions.md** - 10 題
2. **Exercise_11_Vectorization_12_Questions.md** - 12 題
3. **Exercise_12_Merge_10_Questions.md** - 10 題
4. **Solutions_Complete.md** - 完整解答

---

### 📁 Capstone Project（5 個檔案）

1. **PROJECT_GUIDE.md** (30KB) - 專案完整指南
2. **capstone_sales_analytics_system.ipynb** - 主 Notebook
3. **requirements.md** - 需求文檔
4. **evaluation_rubric.md** - 評估標準（自評 + 同儕評估）
5. **sample_report.md** - 範例分析報告

---

### 📁 工具函數庫（utils/ 目錄）

1. **data_loader.py** - 資料載入工具
2. **performance_profiler.py** - 效能分析工具
3. **plotting_helpers.py** - 視覺化輔助
4. **validation_helpers.py** - 資料驗證工具
5. **excel_exporter.py** - Excel 報表輸出

---

## 🎯 28 個 Notebook 設計綱要

### **Week 3: MultiIndex & GroupBy（7 個 Notebook）**

#### Notebook 01: MultiIndex 基礎（2h）⭐
**學習目標：**
- 理解 MultiIndex 的概念與優勢
- 掌握 4 種建立 MultiIndex 的方法
- 熟悉 MultiIndex 的屬性與方法

**核心內容：**
1. 什麼是 MultiIndex（10min）
2. 建立 MultiIndex（30min）
   - `from_tuples()`
   - `from_arrays()`
   - `from_product()`
   - `set_index()` 多欄位
3. MultiIndex 屬性（20min）
   - `levels`, `codes`, `names`
   - `nlevels`, `levshape`
4. 基礎選取（40min）
   - 單層選取
   - 多層選取
   - 部分索引
5. 實戰案例（20min）
   - Olist 訂單：按地區 + 類別建立 MultiIndex

**Excel 對照：**
- Excel 樞紐表多列標籤 → pandas MultiIndex

---

#### Notebook 02: MultiIndex 切片進階（2h）
**學習目標：**
- 掌握 `loc` 的多層切片語法
- 使用 `xs` 跨層選取
- 理解 `IndexSlice` 的威力

**核心內容：**
1. loc 多層切片（40min）
   - 單層選取：`df.loc['level0']`
   - 雙層選取：`df.loc[('level0', 'level1')]`
   - 部分索引：`df.loc[('level0', slice(None))]`
2. xs 跨層選取（30min）
   - `df.xs('key', level=1)`
   - 跨多層選取
3. IndexSlice 進階（30min）
   - 建立 IndexSlice 物件
   - 範圍切片
   - 多維切片
4. 實戰案例（20min）
   - 選取特定地區的所有類別
   - 選取所有地區的特定類別

---

#### Notebook 03: GroupBy 聚合（2h）⭐
**學習目標：**
- 掌握命名聚合（Named Aggregation）
- 使用多函數聚合
- 自訂聚合函數

**核心內容：**
1. GroupBy 基礎回顧（20min）
2. 命名聚合（50min）
   - 語法：`agg(新名稱=('欄位', '函數'))`
   - 多函數多欄位
   - 重新命名輸出
3. 常用聚合函數（30min）
   - 統計：sum, mean, median, std, count
   - 位置：first, last, nth
   - 自訂：lambda, 自訂函數
4. 實戰案例（20min）
   - 計算每個類別的訂單統計
   - 計算每個地區的營收指標

**Excel 對照：**
- 樞紐表值欄位 → agg 函數
- 樞紐表計算欄位 → 自訂聚合函數

---

#### Notebook 04: GroupBy Transform & Filter（2h）
**學習目標：**
- 理解 transform 的「保持形狀」特性
- 使用 filter 篩選群組
- 區分 agg vs transform vs filter

**核心內容：**
1. Transform 基礎（40min）
   - 保持原始 DataFrame 形狀
   - 常用場景：組內標準化、組內排名
2. Filter 群組篩選（30min）
   - 篩選符合條件的群組
   - 與 transform 結合
3. 三者對比（30min）
   - agg：聚合（縮小）
   - transform：保持形狀（廣播）
   - filter：篩選群組
4. 實戰案例（20min）
   - 計算每個產品的銷售額佔比
   - 篩選訂單數 > 100 的類別

---

#### Notebook 05: Pivot & Stack/Unstack（2h）⭐
**學習目標：**
- 掌握 pivot_table 完整語法
- 理解 stack/unstack 轉換
- 實現多維度透視

**核心內容：**
1. pivot_table 完整語法（50min）
   - index, columns, values, aggfunc
   - margins（小計與總計）
   - fill_value（填充缺失值）
2. stack/unstack（40min）
   - stack：欄位變索引（寬→長）
   - unstack：索引變欄位（長→寬）
   - 指定層級轉換
3. 實戰案例（30min）
   - 地區 × 類別 營收交叉表
   - 月份 × 產品 銷售趨勢表

**Excel 對照：**
- Excel 樞紐表 → pivot_table
- Power Query Pivot Column → unstack
- Power Query Unpivot → stack/melt

---

#### Notebook 06: Melt - 寬表變長表（2h）
**學習目標：**
- 理解 melt 的概念
- 掌握 id_vars, value_vars, var_name, value_name
- 實現複雜的寬長轉換

**核心內容：**
1. Melt 基礎（40min）
   - 寬表 vs 長表
   - melt 基本語法
2. 參數詳解（40min）
   - id_vars：保持不變的欄位
   - value_vars：要融化的欄位
   - var_name, value_name：新欄位名稱
3. 進階技巧（20min）
   - 部分融化
   - 多次 melt
4. 實戰案例（20min）
   - 將月度銷售寬表轉成長表

---

#### Notebook 07: Week 3 整合專案（5-7h）
**專案名稱：** Olist 多維度分析系統

**需求：**
1. 建立地區 × 類別 MultiIndex 結構
2. 計算每個組合的關鍵指標（訂單數、營收、平均客單價、評分）
3. 使用 pivot_table 產生交叉分析表
4. 輸出 3 個報表：
   - 月度類別表現（時間 × 類別）
   - 地區類別矩陣（地區 × 類別）
   - Top 產品排行（MultiIndex：類別 + 產品）

**評估標準：**
- 代碼正確性（40%）
- 報表完整性（30%）
- 代碼可讀性（20%）
- 洞察分析（10%）

---

### **Week 4: 時間序列 & 視窗函數（7 個 Notebook）**

#### Notebook 08: DateTime 基礎（2h）⭐
**學習目標：**
- 掌握 pandas 的 datetime 體系
- 使用 dt accessor 提取時間元件
- 處理時區與格式轉換

**核心內容：**
1. DateTime 基礎（30min）
   - `pd.to_datetime()`
   - Timestamp vs datetime
2. dt accessor（40min）
   - 提取：year, month, day, hour, dayofweek
   - 計算：quarter, week, dayofyear
   - 中文：weekday_name（需映射）
3. 時區處理（30min）
   - tz_localize, tz_convert
4. 實戰案例（20min）
   - 提取訂單的年/月/季度/星期
   - 計算營業日（排除週末）

**Excel 對照：**
- YEAR/MONTH/DAY → dt.year/month/day
- WEEKDAY() → dt.dayofweek
- EOMONTH() → dt.to_period('M').to_timestamp('M')

---

#### Notebook 09: Timedelta & DateOffset（2h）
**學習目標：**
- 理解 Timedelta vs DateOffset
- 計算時間差與時間偏移
- 使用 Period 處理月度/季度資料

**核心內容：**
1. Timedelta（40min）
   - 建立 Timedelta
   - 時間運算
2. DateOffset（40min）
   - MonthEnd, QuarterEnd, YearEnd
   - BusinessDay
3. Period（20min）
   - Period vs Timestamp
   - Period 運算
4. 實戰案例（20min）
   - 計算訂單處理時長
   - 計算配送天數

**Excel 對照：**
- DATE 運算 → Timedelta
- EOMONTH → MonthEnd
- WORKDAY → BusinessDay

---

#### Notebook 10: Resample 重採樣（2h）⭐
**學習目標：**
- 掌握 resample 頻率轉換
- 理解 Upsampling vs Downsampling
- 使用 agg 進行多指標聚合

**核心內容：**
1. Resample 基礎（40min）
   - 設定 DatetimeIndex
   - 常用頻率：D, W, M, Q, Y
2. Downsampling（30min）
   - 降採樣（高頻→低頻）
   - agg 函數：sum, mean, count
3. Upsampling（20min）
   - 升採樣（低頻→高頻）
   - 填充方法：ffill, bfill, interpolate
4. 實戰案例（30min）
   - 日訂單數 → 週訂單數
   - 日營收 → 月營收

**Excel 對照：**
- 樞紐表按月分組 → resample('M')
- 樞紐表按季分組 → resample('Q')

---

#### Notebook 11: Rolling 移動視窗（2.5h）
**學習目標：**
- 掌握 rolling 移動視窗
- 計算移動平均（SMA, EMA）
- 使用 expanding 計算累計指標

**核心內容：**
1. Rolling 基礎（40min）
   - window 參數
   - min_periods
2. 常用函數（50min）
   - mean, sum, std
   - apply 自訂函數
3. Expanding（30min）
   - 累計平均
   - 累計總和（YTD）
4. 實戰案例（30min）
   - 7 日移動平均
   - 30 日移動平均
   - YTD 累計營收

**Excel 對照：**
- AVERAGE(A1:A7) 拖曳 → rolling(7).mean()

---

#### Notebook 12: 時間比較（MoM/YoY）（2h）⭐
**學習目標：**
- 使用 shift 進行時間平移
- 計算 MoM, YoY, WoW 成長率
- 實現同期比較

**核心內容：**
1. shift 時間平移（30min）
   - 正向/反向平移
   - freq 參數
2. pct_change & diff（40min）
   - pct_change：百分比變化
   - diff：絕對差異
3. 同期比較（30min）
   - MoM（月成長率）
   - YoY（年成長率）
   - WoW（週成長率）
4. 實戰案例（20min）
   - 計算每月營收 MoM
   - 計算每月營收 YoY

**Excel 對照：**
- 樞紐表「顯示值方式」→「差異百分比」→ pct_change
- 樞紐表「顯示值方式」→「Running Total」→ expanding().sum()

---

#### Notebook 13: 季節性分解（2.5h）
**學習目標：**
- 理解時間序列的組成（趨勢 + 季節性 + 殘差）
- 使用 statsmodels 分解
- 識別季節性模式

**核心內容：**
1. 時間序列分解理論（30min）
2. statsmodels.tsa.seasonal_decompose（60min）
3. 視覺化與解讀（40min）
4. 實戰案例（20min）
   - 分解每日訂單量

---

#### Notebook 14: Week 4 整合專案（5-7h）
**專案名稱：** 時間序列分析儀表板

**需求：**
1. 每日/週/月訂單趨勢
2. 7 日/30 日移動平均
3. MoM/YoY 成長率
4. YTD 累計營收
5. 季節性分析

**交付物：**
- 1 個完整 Notebook
- 5 個視覺化圖表
- 1 份時間序列分析報告

---

### **Week 5: Apply/Transform/Agg 深度應用（7 個 Notebook）**

#### Notebook 15: Apply 基礎（2h）⭐
**學習目標：**
- 理解 Series.apply vs DataFrame.apply
- 掌握 axis 參數
- 學會何時使用 apply

**核心內容：**
1. Series.apply（40min）
   - 單欄位函數應用
   - lambda vs 自訂函數
2. DataFrame.apply（50min）
   - axis=0 vs axis=1
   - 多欄位計算
3. 注意事項（10min）
   - apply 效能問題
4. 實戰案例（20min）
   - 計算複雜的分類邏輯
   - 計算多欄位組合指標

---

#### Notebook 16: Apply 效能優化（2h）
**學習目標：**
- 測量 apply 效能
- 學會替代方案（向量化）
- 理解何時避免 apply

**核心內容：**
1. 效能基準測試（40min）
   - %%timeit 測量
   - apply vs vectorization 對比
2. 替代方案（60min）
   - 向量化運算
   - np.where, np.select
   - 內建方法
3. 實戰案例（20min）
   - 優化前後對比（10x-100x 差異）

---

#### Notebook 17: Transform 組內計算（2h）⭐
**學習目標：**
- 掌握 transform 的「保持形狀」特性
- 計算組內百分比
- 實現組內排名

**核心內容：**
1. Transform 基礎（30min）
   - 保持 DataFrame 形狀
   - 與 agg 對比
2. 常用場景（60min）
   - 組內標準化：`(x - mean) / std`
   - 組內百分比：`x / sum(x)`
   - 組內排名：`rank()`
3. 實戰案例（30min）
   - 計算每個產品在其類別的銷售額佔比
   - 計算每個客戶在其地區的消費排名

**Excel 對照：**
- AVERAGEIF 廣播 → transform('mean')
- SUMIF 廣播 → transform('sum')

---

#### Notebook 18: Agg 命名聚合（2h）⭐
**學習目標：**
- 掌握命名聚合語法
- 建立清晰的報表結構
- 使用多函數多欄位聚合

**核心內容：**
1. 命名聚合基礎（40min）
   - 語法結構
   - 重新命名輸出欄位
2. 進階技巧（50min）
   - 多函數應用於多欄位
   - 混合使用內建函數與自訂函數
3. 實戰案例（30min）
   - 建立客戶分析報表
   - 建立產品類別報表

---

#### Notebook 19: 自訂聚合函數（2h）
**學習目標：**
- 編寫自訂聚合函數
- 實現複雜的業務邏輯
- 使用 NamedAgg

**核心內容：**
1. 自訂函數基礎（40min）
2. 複雜聚合（50min）
   - 計算範圍（max - min）
   - 計算變異係數（CV）
   - 計算加權平均
3. 實戰案例（30min）
   - 計算客戶購買週期
   - 計算產品價格穩定性

---

#### Notebook 20: RFM 客戶分析（3h）
**學習目標：**
- 理解 RFM 模型
- 實現 RFM 計算
- 進行客戶分群

**核心內容：**
1. RFM 理論（30min）
   - Recency（最近購買）
   - Frequency（購買頻率）
   - Monetary（購買金額）
2. RFM 計算（90min）
   - 使用 transform 計算 R, F, M
   - 分箱與評分
   - 客戶分群
3. 實戰案例（60min）
   - Olist 客戶 RFM 分析
   - 輸出客戶分群報表

---

#### Notebook 21: Week 5 整合專案（3-5h）
**專案名稱：** 客戶分析系統

**需求：**
1. RFM 分析與分群
2. 客戶生命週期價值（CLV）
3. 複購率分析
4. 客戶流失預警

**交付物：**
- 1 個完整 Notebook
- 客戶分群報表
- 3 個視覺化圖表

---

### **Week 6: 效能優化 & 合併策略（7 個 Notebook）**

#### Notebook 22: 記憶體分析（2h）⭐
**學習目標：**
- 分析 DataFrame 記憶體使用
- 理解不同 dtype 的記憶體佔用
- 使用 memory_usage() 分析

**核心內容：**
1. 記憶體分析工具（40min）
   - `df.info(memory_usage='deep')`
   - `df.memory_usage(deep=True)`
2. Dtype 記憶體對比（50min）
   - int64 vs int32 vs int8
   - object vs category
3. 實戰案例（30min）
   - 分析 Olist 資料集記憶體

---

#### Notebook 23: Dtype 優化（2h）⭐
**學習目標：**
- 使用 Categorical dtype
- Downcast 數值型態
- 實現 60%+ 記憶體節省

**核心內容：**
1. Categorical dtype（50min）
   - 何時使用 category
   - ordered vs unordered
2. Downcast（40min）
   - pd.to_numeric(downcast='integer')
   - 自動偵測最小 dtype
3. 實戰案例（30min）
   - 優化 Olist 資料集
   - 前後對比

---

#### Notebook 24: 向量化基礎（2h）
**學習目標：**
- 理解向量化 vs 迴圈
- 使用內建向量化方法
- 測量效能差異

**核心內容：**
1. 向量化概念（30min）
2. 常用向量化方法（60min）
   - 算數運算
   - 比較運算
   - 邏輯運算
3. 效能對比（30min）
   - for loop vs vectorization（100x+ 差異）

---

#### Notebook 25: np.select & np.where（2h）⭐
**學習目標：**
- 使用 np.where 雙條件
- 使用 np.select 多條件
- 取代 apply 提升效能

**核心內容：**
1. np.where（40min）
   - 基礎語法：`np.where(condition, true_val, false_val)`
   - 巢狀 where
2. np.select（50min）
   - 多條件語法
   - 條件列表與值列表
3. 實戰案例（30min）
   - 會員等級分類
   - 訂單狀態標籤

---

#### Notebook 26: Merge 類型（2h）⭐
**學習目標：**
- 掌握 4 種 Join 類型
- 理解 left/inner/outer/cross join
- 使用 indicator 驗證

**核心內容：**
1. Merge 基礎（30min）
   - on, left_on, right_on
   - how 參數
2. 4 種 Join 類型（60min）
   - inner：交集
   - left：左表全保留
   - outer：聯集
   - cross：笛卡爾積
3. 實戰案例（30min）
   - Olist 9 張表整合

**Excel 對照：**
- VLOOKUP → merge (how='left')
- Power Query Merge → merge

---

#### Notebook 27: Merge 驗證（2h）
**學習目標：**
- 使用 validate 驗證關係
- 使用 indicator 追蹤來源
- 處理重複 key

**核心內容：**
1. Validate 驗證（40min）
   - one_to_one, one_to_many, many_to_one
2. Indicator 追蹤（40min）
   - 檢查未匹配資料
3. 實戰案例（40min）
   - 驗證 Olist 多表合併

---

#### Notebook 28: Week 6 整合專案（3-5h）
**專案名稱：** 大數據處理 Pipeline

**需求：**
1. 載入大數據集（eCommerce Behavior 13.7GB）
2. 記憶體優化（< 4GB）
3. 向量化計算
4. 輸出最終報表

**挑戰：**
- 使用 chunking 分批讀取
- Dtype 優化
- 向量化運算

---

## 📊 108+ 練習題結構

### Week 3: MultiIndex & GroupBy（37 題）

#### Exercise_01_MultiIndex_12_Questions.md

**基礎題（6 題）：**
1. 使用 `from_tuples()` 建立地區 + 類別 MultiIndex
2. 使用 `set_index()` 建立雙欄位索引
3. 選取特定地區的所有資料
4. 使用 `xs()` 選取特定類別
5. 重設索引為單層索引
6. 查看 MultiIndex 的層級數

**進階題（6 題）：**
7. 使用 IndexSlice 選取多個地區的特定類別
8. 交換 MultiIndex 層級順序
9. 對 MultiIndex 進行排序
10. 使用 `loc` 進行範圍切片
11. 建立 3 層 MultiIndex（地區 + 類別 + 月份）
12. 對 MultiIndex 重新命名層級

---

#### Exercise_02_GroupBy_15_Questions.md

**基礎題（5 題）：**
1. 按類別分組，計算總營收
2. 按地區分組，計算平均訂單金額
3. 按月份分組，計算訂單數
4. 按類別 + 地區雙重分組
5. 計算每個類別的訂單數與總營收（命名聚合）

**進階題（5 題）：**
6. 使用 transform 計算每個產品在其類別的銷售額佔比
7. 使用 filter 篩選訂單數 > 100 的類別
8. 計算每個類別的 Top 3 產品
9. 自訂聚合函數：計算銷售額範圍（max - min）
10. 計算每個地區的營收累計佔比

**挑戰題（5 題）：**
11. 建立完整的類別分析報表（10+ 指標）
12. 計算每個類別的月度成長率
13. 找出每個地區銷售額增長最快的類別
14. 使用 agg + transform 結合計算組內排名
15. 實現複雜的條件聚合（不同類別使用不同聚合函數）

---

#### Exercise_03_Pivot_10_Questions.md

**基礎題（4 題）：**
1. 建立地區 × 類別營收交叉表
2. 建立月份 × 類別訂單數交叉表
3. 使用 margins 顯示小計與總計
4. 使用 fill_value 填充缺失值

**進階題（4 題）：**
5. 使用 stack 將寬表轉成長表
6. 使用 unstack 將長表轉成寬表
7. 使用 melt 融化多個欄位
8. 建立 3 維透視表（index + columns 都有多層）

**挑戰題（2 題）：**
9. 實現複雜的透視表（多值欄位 + 多聚合函數）
10. 將透視表結果轉換回 MultiIndex DataFrame

---

### Week 4: 時間序列 & 視窗函數（32 題）

#### Exercise_04_DateTime_10_Questions.md
1-5. 基礎：datetime 轉換、屬性提取、格式化
6-10. 進階：時區處理、時間差計算、Period 使用

#### Exercise_05_Resample_Rolling_12_Questions.md
1-6. 基礎：resample 頻率轉換、agg 聚合
7-12. 進階：rolling 移動平均、expanding 累計指標

#### Exercise_06_Time_Comparison_10_Questions.md
1-5. 基礎：shift, pct_change, diff
6-10. 進階：MoM/YoY/WoW 成長率、同期比較

---

### Week 5: Apply/Transform/Agg（37 題）

#### Exercise_07_Apply_15_Questions.md
1-5. 基礎：Series.apply、DataFrame.apply
6-10. 進階：axis 參數、自訂函數
11-15. 挑戰：效能優化、替代方案

#### Exercise_08_Transform_12_Questions.md
1-6. 基礎：transform 基礎、組內標準化
7-12. 進階：組內百分比、組內排名

#### Exercise_09_Agg_10_Questions.md
1-5. 基礎：命名聚合、多函數聚合
6-10. 進階：自訂聚合函數、複雜報表

---

### Week 6: 效能優化 & Merge（32 題）

#### Exercise_10_Memory_10_Questions.md
1-5. 基礎：記憶體分析、dtype 查看
6-10. 進階：Categorical 優化、downcast

#### Exercise_11_Vectorization_12_Questions.md
1-6. 基礎：向量化基本運算、np.where
7-12. 進階：np.select、效能對比

#### Exercise_12_Merge_10_Questions.md
1-5. 基礎：4 種 Join 類型、on 參數
6-10. 進階：validate 驗證、indicator 追蹤

---

## ⏱️ 時間估算與評估標準

### 時間估算（總計：80-100 小時）

#### Week 3: MultiIndex & GroupBy（20-25h）
- **Day 01（5-6h）：** MultiIndex 完全掌握
  - Notebook 01: 2h
  - Notebook 02: 2h
  - 練習 12 題：1-2h
- **Day 02（5-6h）：** GroupBy 進階聚合
  - Notebook 03: 2h
  - Notebook 04: 2h
  - 練習 15 題：1-2h
- **Day 03（5-6h）：** 透視表與重塑
  - Notebook 05: 2h
  - Notebook 06: 2h
  - 練習 10 題：1-2h
- **Day 04（5-7h）：** Week 3 整合專案
  - Notebook 07: 5-7h

---

#### Week 4: 時間序列 & 視窗函數（20-25h）
- **Day 05（5-6h）：** DateTime 完全掌握
  - Notebook 08: 2h
  - Notebook 09: 2h
  - 練習 10 題：1-2h
- **Day 06（6-7h）：** Resample & Rolling
  - Notebook 10: 2h
  - Notebook 11: 2.5h
  - 練習 12 題：1.5-2.5h
- **Day 07（5-6h）：** 時間比較
  - Notebook 12: 2h
  - Notebook 13: 2.5h
  - 練習 10 題：0.5-1.5h
- **Day 08（5-7h）：** Week 4 整合專案
  - Notebook 14: 5-7h

---

#### Week 5: Apply/Transform/Agg（20-25h）
- **Day 09（6-7h）：** Apply 深度探索
  - Notebook 15: 2h
  - Notebook 16: 2h
  - 練習 15 題：2-3h
- **Day 10（6-7h）：** Transform 組內計算
  - Notebook 17: 2h
  - Notebook 18: 2h
  - 練習 12 題：2-3h
- **Day 11（5-6h）：** Agg 命名聚合
  - Notebook 19: 2h
  - Notebook 20: 3h
  - 練習 10 題：0-1h
- **Day 12（3-5h）：** Week 5 整合專案
  - Notebook 21: 3-5h

---

#### Week 6: 效能優化 & Merge（20-25h）
- **Day 13（6-7h）：** 記憶體優化
  - Notebook 22: 2h
  - Notebook 23: 2h
  - 練習 10 題：2-3h
- **Day 14（6-7h）：** 向量化運算
  - Notebook 24: 2h
  - Notebook 25: 2h
  - 練習 12 題：2-3h
- **Day 15（5-6h）：** Merge 策略
  - Notebook 26: 2h
  - Notebook 27: 2h
  - 練習 10 題：1-2h
- **Day 16（3-5h）：** Week 6 整合專案
  - Notebook 28: 3-5h

---

#### Capstone Project（10-15h）
- **Module 1（2h）：** 資料載入與清洗
- **Module 2（2h）：** 多表整合
- **Module 3（3h）：** 多維度分析
- **Module 4（3h）：** 時間序列分析
- **Module 5（3h）：** 客戶分析
- **Module 6（2h）：** 效能優化與報表輸出
- **報告（0-3h）：** 撰寫分析報告（可選）

---

### 評估標準

#### Notebook 練習評估（適用於 Notebook 01-28）

**代碼正確性（50%）**
- [ ] 代碼能正確執行（無錯誤）
- [ ] 輸出結果正確
- [ ] 邏輯清晰

**代碼品質（30%）**
- [ ] 變數命名清晰
- [ ] 適當的註釋
- [ ] 遵循 PEP 8 風格
- [ ] 無冗餘代碼

**理解深度（20%）**
- [ ] 能解釋代碼邏輯
- [ ] 理解為何這樣寫
- [ ] 能舉一反三

---

#### 整合專案評估（適用於 Week 3-6 整合專案）

**功能完整性（40%）**
- [ ] 完成所有需求功能
- [ ] 輸出正確的報表
- [ ] 視覺化清晰

**代碼品質（30%）**
- [ ] 代碼結構清晰
- [ ] 模組化設計
- [ ] 適當的錯誤處理
- [ ] 良好的註釋

**效能優化（20%）**
- [ ] 適當使用向量化
- [ ] 記憶體使用合理
- [ ] 執行時間合理

**洞察分析（10%）**
- [ ] 提供有價值的洞察
- [ ] 報表易讀易懂
- [ ] 包含結論與建議

---

#### Capstone Project 評估

**資料處理（25%）**
- [ ] 正確載入與清洗資料
- [ ] 適當的記憶體優化
- [ ] 資料品質檢查

**多表整合（20%）**
- [ ] 正確合併 9 張表
- [ ] 使用適當的 Join 類型
- [ ] Merge 驗證

**分析深度（30%）**
- [ ] 多維度分析完整
- [ ] 時間序列分析深入
- [ ] 客戶分析有洞察

**報表品質（15%）**
- [ ] 報表結構清晰
- [ ] 視覺化專業
- [ ] 易於理解

**代碼品質（10%）**
- [ ] 代碼可讀性高
- [ ] 適當的模組化
- [ ] 良好的註釋

---

## 🎯 學習路徑建議

### 🟢 路徑 A：完整學習（90-100h）⭐ 推薦

**適合對象：**
- 想要全面掌握 pandas 進階技能
- 時間充裕（每週 20-25h × 4 週）
- 目標成為 pandas 專家

**學習計劃：**
```
Week 3（20-25h）
├── Day 1（週一-週二）：MultiIndex（5-6h）
├── Day 2（週三-週四）：GroupBy（5-6h）
├── Day 3（週五）：Pivot & Reshape（5-6h）
└── Day 4（週末）：整合專案（5-7h）

Week 4（20-25h）
├── Day 5（週一-週二）：DateTime（5-6h）
├── Day 6（週三-週四）：Resample & Rolling（6-7h）
├── Day 7（週五）：Time Comparison（5-6h）
└── Day 8（週末）：整合專案（5-7h）

Week 5（20-25h）
├── Day 9（週一-週二）：Apply（6-7h）
├── Day 10（週三-週四）：Transform & Agg（6-7h）
├── Day 11（週五）：RFM 分析（5-6h）
└── Day 12（週末）：整合專案（3-5h）

Week 6（20-25h）
├── Day 13（週一-週二）：Memory Optimization（6-7h）
├── Day 14（週三-週四）：Vectorization（6-7h）
├── Day 15（週五）：Merge Strategies（5-6h）
└── Day 16（週末）：整合專案（3-5h）

Capstone Project（10-15h）
└── 週末完成（2 天）
```

**完成後能力：**
- ✅ 掌握 pandas 90% 進階技能
- ✅ 能處理百萬級資料
- ✅ 能建立完整分析系統
- ✅ 能優化記憶體與效能
- ✅ 可直接應用於工作

---

### 🟡 路徑 B：快速學習（50-60h）

**適合對象：**
- 時間有限但想學核心技能
- 每週 12-15h × 4 週
- 聚焦最常用的功能

**學習計劃：**
只完成標記 ⭐ 的 Notebook（18 個）
+ 基礎與進階練習（跳過挑戰題）
+ 週末整合專案

**核心 Notebook（18 個）：**
- Week 3: 01, 03, 05（MultiIndex, GroupBy, Pivot）
- Week 4: 08, 10, 12（DateTime, Resample, Time Compare）
- Week 5: 15, 17, 18（Apply, Transform, Agg）
- Week 6: 22, 23, 25, 26（Memory, Dtype, np.select, Merge）
- 整合專案：4 個（Week 3-6 各 1 個）

**完成後能力：**
- ✅ 掌握 pandas 70% 進階技能
- ✅ 能處理常見資料分析任務
- ✅ 理解核心概念
- ✅ 可在工作中應用

---

### 🔴 路徑 C：工作導向（30-40h）

**適合對象：**
- 立即應用到工作
- 邊學邊用
- 聚焦特定場景

**學習計劃：**
根據工作需求選擇模組

**場景 1：報表自動化（10h）**
- GroupBy 命名聚合（2h）
- Pivot_table 交叉分析（2h）
- Agg 建立報表（2h）
- Merge 多表整合（2h）
- 實戰：建立月度報表系統（2h）

**場景 2：時間序列分析（12h）**
- DateTime 基礎（2h）
- Resample 重採樣（2h）
- Rolling 移動平均（2h）
- MoM/YoY 成長率（2h）
- 實戰：營收趨勢分析（4h）

**場景 3：客戶分析（10h）**
- GroupBy + Transform（2h）
- RFM 分析（3h）
- 客戶分群（2h）
- 實戰：客戶價值分析（3h）

**場景 4：效能優化（8h）**
- 記憶體優化（2h）
- Dtype 優化（2h）
- 向量化運算（2h）
- 實戰：優化現有代碼（2h）

**完成後能力：**
- ✅ 掌握特定領域技能
- ✅ 立即解決工作問題
- ✅ 提升工作效率
- ✅ 可持續擴展學習

---

## 📖 Excel → pandas 核心對照表

### MultiIndex & GroupBy

| Excel 功能 | pandas 對應 | 說明 |
|-----------|------------|------|
| 樞紐表多列標籤 | MultiIndex | 建立階層式索引 |
| 樞紐表值欄位 | `groupby().agg()` | 聚合計算 |
| 樞紐表計算欄位 | 自訂聚合函數 | 複雜計算 |
| 小計與總計 | `margins=True` | 透視表小計 |
| 欄位設定格式 | `aggfunc` 參數 | 聚合函數 |

### 時間序列

| Excel 功能 | pandas 對應 | 說明 |
|-----------|------------|------|
| YEAR/MONTH/DAY | `dt.year/month/day` | 提取時間元件 |
| WEEKDAY() | `dt.dayofweek` | 星期幾 |
| EOMONTH() | `pd.offsets.MonthEnd()` | 月末日期 |
| DATEDIF() | `(date2 - date1).dt.days` | 日期差 |
| 樞紐表按月分組 | `resample('M')` | 時間重採樣 |
| 移動平均（拖曳公式） | `rolling(7).mean()` | 移動視窗 |
| 樞紐表「顯示值方式」差異 | `pct_change()` | 百分比變化 |
| 樞紐表「顯示值方式」Running Total | `expanding().sum()` | 累計 |

### Apply/Transform/Agg

| Excel 功能 | pandas 對應 | 說明 |
|-----------|------------|------|
| IF/IFS 複雜邏輯 | `apply(lambda x: ...)` | 自訂函數 |
| AVERAGEIF 廣播 | `transform('mean')` | 組內計算 |
| SUMIF 廣播 | `transform('sum')` | 組內總和 |
| 樞紐表計算欄位 | 命名聚合 | 多指標報表 |

### 效能 & Merge

| Excel 功能 | pandas 對應 | 說明 |
|-----------|------------|------|
| VLOOKUP | `merge(how='left')` | 左連接 |
| Power Query Merge | `merge()` | 表合併 |
| Power Query Append | `concat()` | 表堆疊 |
| 條件格式資料橫條 | 記憶體優化 | 視覺化 |

---

## ✅ 學習成就系統

### 🥉 初級成就（完成 25%）
- [ ] 完成 Week 3 MultiIndex & GroupBy 核心 Notebook（3 個）
- [ ] 完成 Week 3 基礎練習（20 題）
- [ ] 建立第一個 MultiIndex DataFrame
- [ ] 使用命名聚合建立報表

### 🥈 中級成就（完成 50%）
- [ ] 完成 Week 3-4 所有核心 Notebook（6 個）
- [ ] 完成 Week 3-4 所有練習（70 題）
- [ ] 完成 Week 3-4 整合專案（2 個）
- [ ] 計算 MoM/YoY 成長率

### 🥇 高級成就（完成 75%）
- [ ] 完成 Week 3-6 所有核心 Notebook（18 個）
- [ ] 完成 Week 3-6 所有基礎+進階練習（80+ 題）
- [ ] 完成 Week 3-6 整合專案（4 個）
- [ ] 實現 60%+ 記憶體優化

### 🏆 大師成就（完成 100%）
- [ ] 完成所有 28 個 Notebook
- [ ] 完成所有 108+ 練習題
- [ ] 完成所有 5 個整合專案
- [ ] 完成 Capstone Project
- [ ] 建立個人 pandas 工具庫
- [ ] 在工作中應用並節省時間
- [ ] 教會至少 1 位同事使用

---

## 💡 學習建議

### DO ✅
1. **先讀 Guide，再開 Notebook** - Guide 提供理論與 Excel 對照
2. **每個案例都要親手實作** - 不要只看不做
3. **修改參數、嘗試變化** - 舉一反三
4. **記錄常用模式** - 建立自己的 Snippets 庫
5. **Excel → pandas 對照思考** - 利用已有的 Excel 知識
6. **效能意識** - 總是考慮效能（向量化 > apply）
7. **完成練習題** - 練習是內化的關鍵
8. **完成整合專案** - 整合所有技能

### DON'T ❌
1. **跳過基礎直接學進階** - 基礎紮實才能走遠
2. **只看不練** - 光看無法真正學會
3. **急於求成** - 每週 20-25h 是合理節奏
4. **忽略 Excel 對照** - Excel 知識是寶貴資產
5. **濫用 apply** - 效能殺手，優先向量化
6. **不做練習題** - 練習題設計用於強化概念
7. **跳過整合專案** - 整合專案整合所有技能

---

## 🚀 快速啟動命令

### 啟動 Jupyter Lab

```bash
cd /home/justin/web-projects/excel-python-data-analysis/week03-06_pandas-advanced

# 如果 Jupyter Lab 未運行
source ~/miniconda3/etc/profile.d/conda.sh
conda activate data_env
jupyter lab --no-browser --port=8888 --ip=0.0.0.0

# 訪問：http://localhost:8888/lab
```

### Week 3 開始

```bash
# 閱讀快速啟動指南（10min）
cat START_HERE.md

# 閱讀資料集指南（10min）
cat DATASET_GUIDE.md

# 開始 Day 1: MultiIndex（5-6h）
cd week03_multiindex_groupby
cat Day01_MultiIndex_Complete_Guide.md

# 在 Jupyter Lab 中開啟：
# week03_multiindex_groupby/notebooks/01_multiindex_basics.ipynb
```

### 載入資料集測試

```python
import pandas as pd
import numpy as np

# 使用工具函數載入
import sys
sys.path.append('../utils')
from data_loader import load_olist_data

# 載入 Olist 資料
orders, order_items, products, customers, sellers, payments, reviews = load_olist_data()

print(f"✅ 資料載入完成！")
print(f"訂單數：{len(orders):,}")
print(f"訂單明細數：{len(order_items):,}")
```

---

## 📊 系統統計

### 檔案統計
```
總檔案數：70+ 個
  核心文檔：5 個
  Week 3：15 個（教學 4 + Notebook 7 + 練習 4）
  Week 4：15 個（教學 4 + Notebook 7 + 練習 4）
  Week 5：15 個（教學 4 + Notebook 7 + 練習 4）
  Week 6：15 個（教學 4 + Notebook 7 + 練習 4）
  Capstone：5 個
  Utils：5 個

總大小：預估 150-200 MB（含資料集）
```

### 內容統計
```
總 Notebook：28 個
  核心 Notebook（⭐）：18 個
  進階 Notebook：10 個

總練習題目：108+ 題
  Week 3：37 題（基礎 15 + 進階 15 + 挑戰 7）
  Week 4：32 題（基礎 15 + 進階 12 + 挑戰 5）
  Week 5：37 題（基礎 15 + 進階 15 + 挑戰 7）
  Week 6：32 題（基礎 15 + 進階 12 + 挑戰 5）

總代碼範例：500+
  Notebook 內：300+
  練習題：108+
  專案：100+
```

### 時間統計
```
總預估時間：80-100 小時
  Week 3：20-25 小時
  Week 4：20-25 小時
  Week 5：20-25 小時
  Week 6：20-25 小時
  Capstone：10-15 小時

快速路徑：50-60 小時（核心 Notebook + 基礎練習）
工作導向：30-40 小時（特定場景模組）
```

---

## 🎓 完成後的下一步

完成 Week 3-6 後，你已具備：
- ✅ 企業級 pandas 進階技能（90%）
- ✅ 處理百萬級資料的能力
- ✅ 建立完整分析系統的經驗
- ✅ 效能優化與記憶體管理能力
- ✅ 多表整合與資料清洗能力

### 方向 1：商業分析模型（Week 12-14）
- RFM 分析深化
- Cohort 留存分析
- CLV（客戶生命週期價值）
- ABC 分析
- 購物籃分析（關聯規則）

### 方向 2：自動化與報表（Week 7-11）
- openpyxl 精美 Excel 報表
- ETL Pipeline 自動化
- 資料品質檢查系統
- 自動化排程（APScheduler）
- Email 報表發送

### 方向 3：視覺化進階
- Plotly 互動式圖表
- Dash 儀表板
- Matplotlib/Seaborn 深化
- 地理視覺化（Folium）

### 方向 4：機器學習
- scikit-learn 基礎
- 客戶流失預測
- 推薦系統
- 時間序列預測（Prophet, ARIMA）

---

## 📚 額外資源

### 官方文件
- [pandas 官方文檔](https://pandas.pydata.org/docs/)
- [pandas 10 Minutes to pandas](https://pandas.pydata.org/docs/user_guide/10min.html)
- [pandas Cookbook](https://pandas.pydata.org/docs/user_guide/cookbook.html)
- [pandas Cheat Sheet](https://pandas.pydata.org/Pandas_Cheat_Sheet.pdf)

### 推薦書籍
- 《Python for Data Analysis》（Wes McKinney - pandas 作者）
- 《Pandas Cookbook》
- 《Effective Pandas》

### 線上課程
- Coursera: Applied Data Science with Python
- DataCamp: pandas Foundations
- Kaggle Learn: pandas

### 社群資源
- Stack Overflow（pandas 標籤）
- Reddit: r/learnpython, r/datascience
- GitHub: awesome-pandas

---

## 🏆 結語

恭喜你！你現在擁有一套完整的 pandas 進階實戰學習系統：

### ✅ 你擁有的資源
- 📚 70+ 個教學文件與 Notebook
- 📝 108+ 個練習題目
- 💻 500+ 個代碼範例
- 📊 Olist 電商完整資料集（9 張表，100K 訂單）
- 🗄️ 103GB 真實電商資料集（備用）
- 🚀 就緒的 Jupyter Lab 環境
- 🛠️ 完整的工具函數庫

### 🎯 你的學習路徑
```
現在位置：Week 3-6 完全就緒 ✅
  ↓
選擇學習路徑（A/B/C）
  ↓
Week 3-6 學習（80-100h / 50-60h / 30-40h）
  ↓
Capstone Project（10-15h）
  ↓
進階方向（商業分析/自動化/視覺化/機器學習）
  ↓
成為 pandas 進階專家 🏆
```

### 💪 立即開始
```bash
# 從 Week 3 開始學習
cd week03-06_pandas-advanced
cat START_HERE.md

# 啟動 Jupyter Lab
jupyter lab

# 開啟第一個 Notebook
# week03_multiindex_groupby/notebooks/01_multiindex_basics.ipynb
```

---

**📅 系統創建時間：** 2024-12-11
**📦 系統版本：** Week 3-6 Complete System v1.0
**🎯 系統目標：** 幫助你從 pandas 基礎使用者進化為 pandas 進階專家

**祝學習順利！Let's GO! 💪🚀**
