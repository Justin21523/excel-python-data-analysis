# 🚀 Week 3-6: pandas 進階實戰 - 快速啟動指南

## 📋 系統總覽

恭喜你完成 Week 1-2 Excel 進階學習！現在進入 **pandas 進階實戰密集訓練**。

**訓練期程：** 4 週（80-100 小時）
**學習模式：** 大量實戰案例 + 真實電商資料
**目標：** 掌握企業級 pandas 進階技能

---

## 🎯 Week 3-6 學習地圖

```
Week 3 (20-25h)          Week 4 (20-25h)          Week 5 (20-25h)          Week 6 (20-25h)
MultiIndex & GroupBy  →  時間序列 & 視窗函數  →  Apply/Transform/Agg  →  效能優化 & Merge
├─ MultiIndex 完全掌握    ├─ DateTime 完全掌握      ├─ Apply 深度探索      ├─ 記憶體優化
├─ GroupBy 進階聚合       ├─ Resample & Rolling     ├─ Transform 組內計算   ├─ 向量化運算
├─ 透視表與重塑           ├─ 時間比較 (YoY/MoM)     ├─ Agg 命名聚合        ├─ Merge 策略
└─ 整合練習 (5-7h)        └─ 整合練習 (5-7h)        └─ 整合練習 (3-5h)     └─ 整合練習 (3-5h)

                              ↓
                     Capstone Project (10-15h)
                  端到端電商分析系統（整合所有技能）
```

---

## 🚦 快速啟動（3 步驟）

### Step 1: 啟動 Jupyter Lab

```bash
cd /home/justin/web-projects/excel-python-data-analysis/week03-06_pandas-advanced

# 如果 Jupyter Lab 未運行，啟動它
source ~/miniconda3/etc/profile.d/conda.sh
conda activate data_env
jupyter lab --no-browser --port=8888 --ip=0.0.0.0
```

**訪問：** http://localhost:8888/lab?token=<your_token>

---

### Step 2: 選擇你的學習路徑

#### 🟢 路徑 A：完整學習（推薦）- 90-100h
**適合：** 想要全面掌握 pandas 進階技能
- 完成所有 28 個 Notebook
- 完成所有 108+ 練習題
- 完成 5 個週末整合專案
- 完成 Capstone 專案

**開始：**
```bash
cd week03_multiindex_groupby
cat Day01_MultiIndex_Complete_Guide.md
jupyter lab notebooks/01_multiindex_basics.ipynb
```

---

#### 🟡 路徑 B：快速學習 - 50-60h
**適合：** 時間有限，聚焦核心技能
- 完成核心 Notebook（標記 ⭐）
- 完成基礎 + 進階練習（70%）
- 完成週末整合專案
- 簡化版 Capstone

**核心 Notebook 清單（18 個）：**
```
Week 3: 01, 03, 05 (MultiIndex, GroupBy, Pivot)
Week 4: 08, 10, 12 (DateTime, Resample, Time Compare)
Week 5: 15, 17, 18 (Apply, Transform, Agg)
Week 6: 22, 23, 25, 26 (Memory, Categorical, Vectorization, Merge)
```

---

#### 🔴 路徑 C：工作導向 - 30-40h
**適合：** 立即應用到工作，邊學邊用
- 完成最常用的 10 個技能模組
- 聚焦你工作中的應用場景
- 建立可重用的代碼庫

**工作常用 Top 10：**
1. GroupBy 聚合與命名（Week 3）
2. 時間序列重採樣（Week 4）
3. MoM/YoY 成長率計算（Week 4）
4. Transform 組內計算（Week 5）
5. Agg 建立報表（Week 5）
6. Merge 多表整合（Week 6）
7. 記憶體優化（Week 6）
8. 向量化運算（Week 6）
9. Pivot_table 交叉分析（Week 3）
10. Rolling 移動平均（Week 4）

---

### Step 3: 載入練習資料集

**主要資料集：Olist Brazilian E-Commerce（121MB）**

```python
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns

# 設定視覺化風格
plt.style.use('seaborn-v0_8')
sns.set_palette("husl")

# 載入 Olist 資料集
DATA_PATH = '/mnt/data/datasets/ecommerce/olist/'

# 9 張表
df_orders = pd.read_csv(f'{DATA_PATH}olist_orders_dataset.csv')
df_order_items = pd.read_csv(f'{DATA_PATH}olist_order_items_dataset.csv')
df_products = pd.read_csv(f'{DATA_PATH}olist_products_dataset.csv')
df_customers = pd.read_csv(f'{DATA_PATH}olist_customers_dataset.csv')
df_sellers = pd.read_csv(f'{DATA_PATH}olist_sellers_dataset.csv')
df_payments = pd.read_csv(f'{DATA_PATH}olist_order_payments_dataset.csv')
df_reviews = pd.read_csv(f'{DATA_PATH}olist_order_reviews_dataset.csv')
df_geolocation = pd.read_csv(f'{DATA_PATH}olist_geolocation_dataset.csv')
df_category_translation = pd.read_csv(f'{DATA_PATH}product_category_name_translation.csv')

print(f"✅ 資料載入完成！")
print(f"訂單數：{len(df_orders):,}")
print(f"訂單明細數：{len(df_order_items):,}")
print(f"產品數：{len(df_products):,}")
print(f"客戶數：{len(df_customers):,}")
```

**預期輸出：**
```
✅ 資料載入完成！
訂單數：99,441
訂單明細數：112,650
產品數：32,951
客戶數：99,441
```

---

## 📚 Week 3-6 詳細內容

### **Week 3: MultiIndex & 複雜 GroupBy（20-25h）**

**學習目標：**
- 掌握階層式索引（MultiIndex）的建立與操作
- 熟練 GroupBy 的進階聚合（命名聚合、自訂函數）
- 實現透視表轉換（pivot_table, stack/unstack, melt）

**Day 01: MultiIndex 完全掌握（5-6h）** ⭐
- Part 1: MultiIndex 基礎（2h）
- Part 2: MultiIndex 切片進階（2h）
- Part 3: MultiIndex 重塑（2h）
- **實戰案例：** 12 個（建立、切片、重組）
- **Excel 對照：** 樞紐表多列標籤 → MultiIndex

**Day 02: GroupBy 進階聚合（5-6h）** ⭐
- Part 1: GroupBy 基礎回顧（1h）
- Part 2: 命名聚合（Named Aggregation）（2h）
- Part 3: Transform vs Aggregate（2h）
- **實戰案例：** 15 個（聚合、轉換、篩選）
- **Excel 對照：** 樞紐表計算欄位 → agg/transform

**Day 03: 透視表與重塑（5-6h）** ⭐
- Part 1: pivot_table 完全掌握（2h）
- Part 2: stack / unstack 深度理解（2h）
- Part 3: melt - 寬表變長表（2h）
- **實戰案例：** 10 個（透視、堆疊、融化）
- **Excel 對照：** 樞紐表 → pivot_table, Power Query Unpivot → melt

**Day 04: Week 3 整合練習（5-7h）**
- **最終專案：** Olist 多維度分析系統
- 整合 MultiIndex + GroupBy + Pivot
- 輸出 3 個報表（月度類別表現、地區類別矩陣、Top 產品排行）

**檔案位置：**
```
week03_multiindex_groupby/
├── Day01_MultiIndex_Complete_Guide.md         (教學指南)
├── Day02_GroupBy_Advanced_Guide.md            (教學指南)
├── Day03_Pivot_Reshape_Guide.md               (教學指南)
├── Day04_Practice_Integration.md              (整合練習)
├── notebooks/
│   ├── 01_multiindex_basics.ipynb             ⭐ 核心
│   ├── 02_multiindex_slicing_advanced.ipynb
│   ├── 03_groupby_aggregation.ipynb           ⭐ 核心
│   ├── 04_groupby_transform_filter.ipynb
│   ├── 05_pivot_stack_unstack.ipynb           ⭐ 核心
│   ├── 06_melt_wide_to_long.ipynb
│   └── 07_week03_final_project.ipynb          (整合專案)
└── exercises/
    ├── Exercise_01_MultiIndex_12_Questions.md
    ├── Exercise_02_GroupBy_15_Questions.md
    ├── Exercise_03_Pivot_10_Questions.md
    └── Solutions_Complete.md
```

---

### **Week 4: 時間序列 & 視窗函數（20-25h）**

**學習目標：**
- 掌握 pandas 的 datetime 體系
- 使用 resample 進行頻率轉換
- 實現 rolling/expanding 移動指標
- 計算 YoY, MoM, WoW 成長率

**Day 05: DateTime 完全掌握（5-6h）** ⭐
- Part 1: DateTime 基礎（2h）
- Part 2: Timedelta & DateOffset（2h）
- Part 3: Period vs Timestamp（2h）
- **實戰案例：** 10 個
- **Excel 對照：** YEAR/MONTH/EOMONTH/DATEDIF → dt accessor

**Day 06: Resample & Rolling（5-6h）** ⭐
- Part 1: Resample 重採樣（2h）
- Part 2: Rolling 移動視窗（2.5h）
- Part 3: Expanding 累計（1.5h）
- **實戰案例：** 12 個
- **Excel 對照：** 樞紐表按月分組 → resample

**Day 07: 時間比較（5-6h）** ⭐
- Part 1: shift 時間平移（2h）
- Part 2: pct_change & diff（2h）
- Part 3: 同期比較實戰（2h）
- **實戰案例：** 10 個
- **Excel 對照：** 樞紐表「顯示值方式」→ pct_change

**Day 08: Week 4 整合練習（5-7h）**
- **最終專案：** 時間序列分析儀表板
- 日/週/月度趨勢 + 移動平均 + YTD + MoM/YoY

**檔案位置：**
```
week04_timeseries_windows/
├── Day05_DateTime_Mastery_Guide.md
├── Day06_Resample_Rolling_Guide.md
├── Day07_Time_Comparison_Guide.md
├── Day08_Practice_Integration.md
└── notebooks/ (7 個 Notebook + 整合專案)
```

---

### **Week 5: Apply/Transform/Agg 深度應用（20-25h）**

**學習目標：**
- 理解 apply 的運作機制與優化
- 掌握 transform 的「保持形狀」特性
- 使用命名聚合建立清晰報表

**Day 09: Apply 深度探索（6-7h）** ⭐
- Part 1: Series.apply（2h）
- Part 2: DataFrame.apply（2h）
- Part 3: Apply vs 向量化（2-3h）
- **實戰案例：** 15 個
- **效能對比：** apply vs vectorization (10x+ 差異)

**Day 10: Transform 組內計算（6-7h）** ⭐
- Part 1: Transform 基礎（2h）
- Part 2: 組內標準化與排名（2h）
- Part 3: 組內百分比計算（2-3h）
- **實戰案例：** 10 個
- **Excel 對照：** AVERAGEIF 廣播 → transform

**Day 11: Agg 命名聚合（5-6h）** ⭐
- Part 1: 命名聚合基礎（2h）
- Part 2: 自訂聚合函數（2h）
- Part 3: 建立完整報表（1-2h）
- **實戰案例：** 12 個

**Day 12: Week 5 整合練習（3-5h）**
- **最終專案：** 客戶分析系統（RFM 分析）

**檔案位置：**
```
week05_apply_transform_agg/
├── Day09_Apply_Deep_Dive_Guide.md
├── Day10_Transform_Guide.md
├── Day11_Agg_Named_Guide.md
├── Day12_Practice_Integration.md
└── notebooks/ (7 個 Notebook + 整合專案)
```

---

### **Week 6: 效能優化 & 合併策略（20-25h）**

**學習目標：**
- 記憶體優化（Categorical, downcasting）
- 向量化運算取代迴圈
- 掌握 4 種 Join 類型與驗證

**Day 13: 記憶體優化（6-7h）** ⭐
- Part 1: 記憶體分析（2h）
- Part 2: Dtype 優化（2-3h）
- Part 3: Sparse 與 Chunking（2h）
- **實戰案例：** 8 個
- **目標：** 記憶體減少 60%+

**Day 14: 向量化運算（6-7h）** ⭐
- Part 1: 向量化基礎（2h）
- Part 2: np.select 多條件（2h）
- Part 3: 分箱與離散化（2-3h）
- **實戰案例：** 10 個
- **效能對比：** for loop vs vectorization (100x+ 差異)

**Day 15: Merge 與 Concat 策略（5-6h）** ⭐
- Part 1: Merge 基礎（2h）
- Part 2: Merge 進階技巧（2h）
- Part 3: Concat 策略（1-2h）
- **實戰案例：** 14 個
- **Excel 對照：** VLOOKUP → merge, Power Query Merge → merge

**Day 16: Week 6 整合練習（3-5h）**
- **最終專案：** 大數據處理 Pipeline
- 挑戰：處理 eCommerce Behavior（13.7GB），記憶體 < 4GB

**檔案位置：**
```
week06_performance_merge/
├── Day13_Memory_Optimization_Guide.md
├── Day14_Vectorization_Guide.md
├── Day15_Merge_Strategies_Guide.md
├── Day16_Practice_Integration.md
└── notebooks/ (7 個 Notebook + 整合專案)
```

---

### **Capstone Project: 端到端電商分析系統（10-15h）**

**整合 Week 3-6 所有技能**

**6 大功能模組：**
1. 資料載入與清洗（2h）- 記憶體優化
2. 多表整合（2h）- Merge 驗證
3. 多維度分析（3h）- MultiIndex + GroupBy + Pivot
4. 時間序列分析（3h）- Resample + Rolling + MoM/YoY
5. 客戶分析（3h）- RFM + Apply/Transform/Agg
6. 效能優化與報表（2h）- 向量化 + 輸出 5 個報表

**交付物：**
- 1 個主 Notebook（完整分析流程）
- 5 個報表 CSV/Excel
- 10+ 個視覺化圖表
- 1 份分析報告（Markdown）

**檔案位置：**
```
capstone_project/
├── PROJECT_GUIDE.md                        (專案指南)
├── capstone_sales_analytics_system.ipynb  (主 Notebook)
├── requirements.md                         (需求文檔)
└── evaluation_rubric.md                    (評估標準)
```

---

## 📊 學習資源

### 資料集

**主要資料集（Olist）：**
- **位置：** `/mnt/data/datasets/ecommerce/olist/`
- **大小：** 121MB
- **表數：** 9 張表
- **訂單數：** 99,441
- **時間範圍：** 2016-2018

**資料集關係：**
```
orders (99K)
  ├─ order_items (112K) → products (33K)
  ├─ payments (103K)
  ├─ reviews (99K)
  └─ customers (99K)

sellers (3K)
  └─ geolocation (1M)

category_translation (71)
```

**其他資料集：**
- Amazon Reviews 2023（88GB）- 進階使用
- eCommerce Behavior（13.7GB）- Week 6 效能挑戰

---

### 文檔與工具

**pandas 官方文檔：**
- [10 Minutes to pandas](https://pandas.pydata.org/docs/user_guide/10min.html)
- [Group By Guide](https://pandas.pydata.org/docs/user_guide/groupby.html)
- [Time Series](https://pandas.pydata.org/docs/user_guide/timeseries.html)

**工具函數庫：**
```python
# 載入工具函數
import sys
sys.path.append('../utils')

from data_loader import load_olist_data
from performance_profiler import profile_memory, profile_time
from plotting_helpers import plot_time_series, plot_heatmap
from validation_helpers import validate_merge, check_duplicates
```

---

## 🎯 學習建議

### 每日學習節奏（推薦）

**平日（週一～五）：** 每天 3-4 小時
- 晚上 19:00-22:00 或早起 6:00-9:00
- 專注完成當日 Notebook

**週末（週六～日）：** 每天 5-6 小時
- 上午：新主題學習
- 下午：整合練習專案
- 晚上：複習與筆記整理

### 學習技巧

1. **先讀 Guide，再開 Notebook**
   - Guide 提供理論與 Excel 對照
   - Notebook 提供實戰代碼

2. **每個案例都要親手實作**
   - 不要只看不做
   - 修改參數、嘗試變化

3. **記錄常用模式**
   - 建立自己的 Snippets 庫
   - 常用模式做成函數

4. **Excel → pandas 對照思考**
   - 利用 Week 1-2 的 Excel 知識
   - 理解概念轉換

5. **效能意識**
   - 總是考慮效能
   - 大數據優先向量化

---

## ✅ 學習檢核表

### Week 3 - MultiIndex & GroupBy
- [ ] 能建立並操作 MultiIndex（4 種方法）
- [ ] 熟練 loc、xs、IndexSlice 切片
- [ ] 掌握命名聚合語法
- [ ] 理解 agg vs transform vs filter 差異
- [ ] 能實現 pivot_table 多維度分析
- [ ] 理解 stack/unstack vs pivot/melt 差異
- [ ] 完成 Week 3 整合專案

### Week 4 - 時間序列 & 視窗函數
- [ ] 掌握 datetime 屬性提取（year, month, day, etc.）
- [ ] 能使用 resample 進行頻率轉換
- [ ] 理解 rolling vs expanding 差異
- [ ] 能計算 MoM, YoY, WoW 成長率
- [ ] 使用 shift 實現時間平移
- [ ] 能識別時間序列異常值
- [ ] 完成 Week 4 整合專案

### Week 5 - Apply/Transform/Agg
- [ ] 理解 apply 的運作機制
- [ ] 知道何時避免 apply（效能）
- [ ] 掌握 transform 的「保持形狀」特性
- [ ] 能使用 transform 計算組內百分比
- [ ] 掌握命名聚合建立報表
- [ ] 能自訂聚合函數
- [ ] 完成 Week 5 整合專案（RFM）

### Week 6 - 效能優化 & Merge
- [ ] 能分析 DataFrame 記憶體使用
- [ ] 掌握 Categorical dtype 優化
- [ ] 理解 downcasting 技巧
- [ ] 能使用 np.where/np.select 向量化
- [ ] 掌握 pd.cut/pd.qcut 分箱
- [ ] 理解 4 種 Join 類型（inner/left/outer/anti）
- [ ] 能使用 indicator 驗證合併
- [ ] 完成 Week 6 整合專案

### Capstone Project
- [ ] 完成資料載入與清洗
- [ ] 完成多表整合（9 張表 → 1 張寬表）
- [ ] 完成多維度分析報表
- [ ] 完成時間序列分析報表
- [ ] 完成客戶分析報表（RFM）
- [ ] 完成效能優化與最終報表
- [ ] 撰寫分析報告

---

## 🆘 獲取幫助

### 常見問題

**Q1: Jupyter Lab token 在哪裡？**
```bash
# 查看終端輸出，找到類似這行：
# http://127.0.0.1:8888/lab?token=4a420be62bb9b055c2cf4839de3a235ba6e9c548b13d8ae3
```

**Q2: 如何重新載入資料集？**
```python
# 使用工具函數
from utils.data_loader import load_olist_data

orders, order_items, products, customers, sellers, payments, reviews = load_olist_data()
```

**Q3: Notebook 運行很慢怎麼辦？**
- 檢查資料量（先用 `.head(1000)` 測試）
- 使用 `%%time` 測量單元格執行時間
- 參考 Week 6 效能優化技巧

**Q4: 如何檢視我的進度？**
```bash
# 查看已完成的 Notebook
ls -lh week03_multiindex_groupby/notebooks/*.ipynb
ls -lh week04_timeseries_windows/notebooks/*.ipynb
# ... 等等
```

---

## 🎓 完成後的下一步

完成 Week 3-6 後，你已具備：
✅ 企業級 pandas 進階技能
✅ 處理百萬級資料的能力
✅ 建立完整分析系統的經驗

**接下來可以選擇：**

### 方向 1：商業分析模型（Week 12-14）
- RFM 分析
- Cohort 留存分析
- CLV 計算
- ABC 分析
- 購物籃分析

### 方向 2：自動化與報表（Week 7-11）
- openpyxl 精美報表
- ETL Pipeline
- 資料品質檢查
- 自動化排程

### 方向 3：機器學習
- scikit-learn 基礎
- 客戶流失預測
- 推薦系統
- 時間序列預測

---

## 🚀 現在就開始吧！

```bash
# 切換到 Week 3 目錄
cd /home/justin/web-projects/excel-python-data-analysis/week03-06_pandas-advanced/week03_multiindex_groupby

# 閱讀第一個教學指南
cat Day01_MultiIndex_Complete_Guide.md

# 啟動 Jupyter Lab（如果尚未啟動）
# 訪問：http://localhost:8888/lab

# 開啟第一個 Notebook
# 在 Jupyter Lab 中：week03_multiindex_groupby/notebooks/01_multiindex_basics.ipynb
```

**祝學習順利！💪**

如有問題，隨時提問。讓我們一起掌握 pandas 進階技能！🎯
