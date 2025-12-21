# Exercise 11: 向量化操作 - 10 題

## 準備工作

```python
import pandas as pd
import numpy as np
import time

# 載入數據
orders = pd.read_csv('/home/justin/web-projects/excel-python-data-analysis/week03-06_pandas-advanced/data/olist_orders_dataset.csv')
order_items = pd.read_csv('/home/justin/web-projects/excel-python-data-analysis/week03-06_pandas-advanced/data/olist_order_items_dataset.csv')
reviews = pd.read_csv('/home/justin/web-projects/excel-python-data-analysis/week03-06_pandas-advanced/data/olist_order_reviews_dataset.csv')
customers = pd.read_csv('/home/justin/web-projects/excel-python-data-analysis/week03-06_pandas-advanced/data/olist_customers_dataset.csv')

# 合併數據
df = order_items.merge(orders[['order_id', 'order_status']], on='order_id')
df = df.merge(reviews[['order_id', 'review_score']], on='order_id', how='left')
```

---

## 🟢 入門題 (Easy)

### 題目 1: 基礎 np.where - 價格分類

**題目描述：**

使用 np.where 創建一個 'price_category' 列，規則為：
- price < 100: 'Budget'
- 100 <= price < 500: 'Standard'
- price >= 500: 'Premium'

計算每個類別的訂單數量和平均價格。

**預期輸出：**
```
Budget:   45234 訂單, 平均 R$ 38.45
Standard: 62145 訂單, 平均 R$ 234.67
Premium:   5271 訂單, 平均 R$ 742.31
```

---

### 題目 2: np.where 應用 - 評分狀態

**題目描述：**

根據 review_score 創建 'satisfaction' 列：
- score >= 4.5: 'Very_Satisfied'
- 4.0 <= score < 4.5: 'Satisfied'
- score < 4.0: 'Unsatisfied'
- NaN: 'No_Review'

統計各類別的訂單數。

**預期輸出：**
```
Very_Satisfied: 28451 訂單
Satisfied:      22341 訂單
Unsatisfied:    15234 訂單
No_Review:      46574 訂單
```

---

### 題目 3: pd.cut - 等寬分箱

**題目描述：**

使用 pd.cut 將訂單金額分為 5 個等寬區間，標籤為：
'Very_Low', 'Low', 'Medium', 'High', 'Very_High'

計算：
1. 每個區間的訂單數
2. 每個區間的平均價格
3. 每個區間的銷售額

**預期輸出：**
```
          訂單數    平均價格    總銷售額
Very_Low   20134    R$ 26.34    R$ 531,245
Low        24567    R$ 153.45   R$ 3,768,234
Medium     35678    R$ 323.12   R$ 11,534,223
High       23412    R$ 612.45   R$ 14,365,234
Very_High  8859     R$ 1,234.12 R$ 10,923,451
```

---

## 🟡 進階題 (Medium)

### 題目 4: np.select - 複雜條件

**題目描述：**

使用 np.select 創建訂單優先級，規則為：
1. 優先級 1: price > 500 AND review_score >= 4
2. 優先級 2: price > 500 OR review_score >= 4
3. 優先級 3: 100 < price <= 500
4. 優先級 4: price <= 100
5. 優先級 5: 其他（無評分）

計算每個優先級的訂單數和佔比。

**提示：**
使用 np.select(conditions, priorities, default=...)

**預期輸出：**
```
優先級 1: 12345 訂單 (11.0%)
優先級 2: 34567 訂單 (30.8%)
優先級 3: 45678 訂單 (40.6%)
優先級 4: 18234 訂單 (16.2%)
優先級 5:  1826 訂單 ( 1.4%)
```

---

### 題目 5: 向量化計算 - 動態定價

**題目描述：**

實現動態定價邏輯：
- 如果 price < 100 且 review_score >= 4：漲價 10%
- 如果 price > 500 且 review_score < 3：降價 20%
- 其他：不變

創建 'adjusted_price' 列，計算：
1. 平均調整幅度
2. 總銷售額變化
3. 有多少訂單被調整

**預期輸出：**
```
調整統計:
  漲價訂單: 12345 (11.0%)
  降價訂單:  8234 (7.3%)
  不變訂單: 92071 (81.7%)

  原始總銷售額: R$ 4,876,234.50
  調整後銷售額: R$ 4,945,123.45
  銷售額增長: R$ 68,888.95 (1.41%)
```

---

### 題目 6: pd.qcut - 等頻分箱 + 客戶分層

**題目描述：**

根據客戶的訂單總額進行四分位分層：

1. 計算每個客戶的總消費額
2. 使用 pd.qcut 分為 4 層：'Bronze', 'Silver', 'Gold', 'Platinum'
3. 統計每層的：
   - 客戶數
   - 平均訂單金額
   - 平均評分
   - 重複購買率

**預期輸出：**
```
Bronze:     24567 客戶, 平均 R$ 45.23, 評分 3.45, 回購 12.3%
Silver:     24512 客戶, 平均 R$ 156.34, 評分 3.78, 回購 34.5%
Gold:       24534 客戶, 平均 R$ 456.78, 評分 4.01, 回購 67.8%
Platinum:   24567 客戶, 平均 R$ 1234.56, 評分 4.23, 回購 89.2%
```

---

## 🔴 高級題 (Hard)

### 題目 7: 複雜業務規則 - np.select + 計算

**題目描述：**

實現複雜的折扣規則：

**基礎折扣（按優先級）:**
- Premium (price > 500): 5% 折扣
- Standard (100-500): 3% 折扣
- Budget (< 100): 0% 折扣

**額外折扣（按評分）:**
- review_score >= 4.5: +5%
- review_score >= 4.0: +3%
- review_score < 3.0: -2% (沒有折扣，反而加價)

**組合規則:**
- 最大折扣不超過 20%
- 沒有評分的訂單減 2%（默認成本）

計算：
1. 每個訂單的最終折扣
2. 折後價格
3. 總的折扣金額
4. 按優先級統計效果

**預期輸出：**
```
折扣統計:
  平均折扣: 5.34%
  最高折扣: 20.00%
  最低折扣: -2.00%
  總折扣金額: R$ 260,234.56

按優先級:
  Premium 平均折扣: 8.12%
  Standard 平均折扣: 5.34%
  Budget 平均折扣: 2.15%
```

---

### 題目 8: 性能測試 - For Loop vs Vectorization

**題目描述：**

對比 for loop 和向量化的性能：

1. **方法 A**: 使用 for loop 逐行計算（使用 iloc）
2. **方法 B**: 使用 np.where（向量化）
3. **方法 C**: 使用 np.select（向量化）

計算每種方法的耗時，比較性能提升倍數。

任務：將訂單分為 5 個優先級（見題目 4）

**函數簽名：**
```python
def performance_comparison(df, sample_size=10000):
    """
    性能對比測試

    返回:
    - 結果DataFrame
    - 各方法耗時
    - 性能倍數
    """
    pass
```

**預期輸出：**
```
性能對比 (10000 行):
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
方法              耗時       相對速度
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
For Loop         2.847s     1x
np.where         0.0045s    633x ✓
np.select        0.0062s    459x ✓
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

推薦: 使用 np.where 最快！
```

---

### 題目 9: 多維度向量化特徵工程

**題目描述：**

創建 10 個向量化特徵：

1. **price_tier**: pd.cut (5 層)
2. **review_level**: np.select (4 級)
3. **is_premium**: np.where (price > 500)
4. **satisfaction**: np.where (review >= 4)
5. **value_ratio**: (price / 平均價格)
6. **discount_eligible**: np.where (特定條件)
7. **risk_score**: np.select (多條件)
8. **customer_segment**: pd.qcut (4 層，基於訂單總額)
9. **repeat_rate**: 客戶重複購買率
10. **anomaly_score**: 異常檢測 (Z-score)

**預期輸出：**
```
新增特徵統計:
Feature             非空數      唯一值    數據類型
─────────────────────────────────────────────
price_tier          112650         5     category
review_level        112650         4     category
is_premium          112650         2     int
satisfaction        112650         2     int
value_ratio         112650     20000     float32
discount_eligible   112650         2     int
risk_score          112650        50     float32
customer_segment    112650         4     category
repeat_rate         112650       100     float32
anomaly_score       112650     20000     float32

所有特徵向量化完成！✓
```

---

### 題目 10: 完整的分析 Pipeline (向量化版)

**題目描述：**

創建一個完整的向量化分析 Pipeline：

**步驟 1**: 數據準備
- 合併 orders, customers, order_items, reviews

**步驟 2**: 向量化特徵工程（使用前 9 題的技術）
- 價格分類、評分分層、優先級分配等

**步驟 3**: 向量化分析
- 按優先級統計銷售額、評分、成本
- 按客戶段分析回購率、平均訂單值
- 風險訂單識別

**步驟 4**: 生成報告

**函數簽名：**
```python
def complete_vectorized_analysis():
    """
    完整的向量化分析 Pipeline

    返回:
    - 帶所有特徵的 DataFrame
    - 分析報告字典
    - 性能統計
    """
    pass
```

**預期輸出：**
```
完整向量化分析 Pipeline
═══════════════════════════════════════

第 1 步: 數據準備
  ✓ 加載 4 個表
  ✓ 合併完成: 112650 行 × 20 列

第 2 步: 特徵工程
  ✓ 創建 10 個向量化特徵
  ✓ 耗時: 0.234s

第 3 步: 分析
  ✓ 優先級分析
  ✓ 客戶分層分析
  ✓ 風險檢測

第 4 步: 報告

優先級分佈:
  VIP:     12345 (11.0%) | R$ 9,123,456 | 評分 4.23
  High:    34567 (30.8%) | R$ 8,345,678 | 評分 4.01
  Medium:  45678 (40.6%) | R$ 3,234,567 | 評分 3.67
  Low:     18234 (16.2%) | R$ 543,234   | 評分 3.12
  Risk:     1826 ( 1.4%) | R$ 125,345   | 評分 2.45

客戶分層:
  Bronze:  24567 (25.0%) | 平均 R$ 45.23 | 回購 12.3%
  Silver:  24512 (25.0%) | 平均 R$ 156.34 | 回購 34.5%
  Gold:    24534 (25.0%) | 平均 R$ 456.78 | 回購 67.8%
  Platinum:24567 (25.0%) | 平均 R$ 1234.56 | 回購 89.2%

風險檢測:
  高風險訂單: 2341 (2.1%)
  異常訂單:   1845 (1.6%)
  需要關注:   4186 (3.7%)

耗時統計:
  數據準備:  0.125s
  特徵工程:  0.234s
  分析:      0.342s
  報告生成:  0.089s
  ─────────
  總耗時:    0.790s ✓ (超快！)
```

---

## 答案提交格式

### 針對每個題目，請提交：

**題目 1-3 (簡單題):**
```python
# 題目 1
df['price_category'] = np.where(...)
result = df.groupby('price_category').agg({...})
print(result)
```

**題目 4-6 (進階題):**
```python
# 題目 4 - np.select
conditions = [...]
priorities = [...]
df['priority'] = np.select(conditions, priorities, default=...)
print(df['priority'].value_counts())
```

**題目 7-10 (高級題):**
```python
# 完整函數 + 應用
def your_function(...):
    ...
    return result

# 執行
result = your_function(...)
print(result)
```

---

## 評分標準

### 正確性
- 邏輯正確：40 分
- 結果準確：30 分
- 邊界處理：20 分

### 性能
- 使用向量化：30 分
- 避免迴圈：30 分

### 代碼質量
- 可讀性：20 分
- 文檔/註釋：10 分

### 總分：100 分

---

## 常見陷阱

### ❌ 避免

```python
# 1. for loop（太慢！）
for idx, row in df.iterrows():
    if row['price'] < 100:
        price_category = 'Budget'

# 2. apply（仍然很慢）
df['category'] = df['price'].apply(lambda x: 'Budget' if x < 100 else 'Standard')

# 3. 多層嵌套 np.where（難以讀）
result = np.where(cond1, val1, np.where(cond2, val2, np.where(cond3, val3, val4)))
```

### ✓ 推薦

```python
# 1. np.where（簡單情況）
df['category'] = np.where(df['price'] < 100, 'Budget', 'Standard')

# 2. np.select（複雜情況）
conditions = [cond1, cond2, cond3, cond4]
choices = [val1, val2, val3, val4]
df['category'] = np.select(conditions, choices, default=default)

# 3. pd.cut（分箱）
df['tier'] = pd.cut(df['price'], bins=[0, 100, 500, 1000])

# 4. pd.qcut（等頻）
df['quartile'] = pd.qcut(df['price'], q=4, labels=['Q1', 'Q2', 'Q3', 'Q4'])
```

---

## 延伸閱讀

- [NumPy where](https://numpy.org/doc/stable/reference/generated/numpy.where.html)
- [NumPy select](https://numpy.org/doc/stable/reference/generated/numpy.select.html)
- [Pandas cut](https://pandas.pydata.org/docs/reference/api/pandas.cut.html)
- [Pandas qcut](https://pandas.pydata.org/docs/reference/api/pandas.qcut.html)

---

## 自我檢查清單

- [ ] 理解 np.where 的三個參數
- [ ] 會使用 np.select 處理多條件
- [ ] 掌握 pd.cut 和 pd.qcut 的區別
- [ ] 能夠嵌套多個向量化操作
- [ ] 理解性能提升的原因
- [ ] 可以測試和對比性能
- [ ] 已經完全放棄使用 for loop！

---

**下一章：Exercise 12 - Merge 策略 14 題**
