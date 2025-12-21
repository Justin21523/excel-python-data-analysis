# Exercise 09: Named Aggregation 命名聚合 12 題

## 難度說明
- 🟢 **Easy** (4題): 基礎 Named Agg 和簡單聚合
- 🟡 **Medium** (5題): 多欄位聚合和自訂函數
- 🔴 **Hard** (3題): 複雜報表和多層聚合

---

## 🟢 Easy Questions (1-4)

### 📌 Q1: 基礎 Named Aggregation
```python
# 題目：使用 Named Aggregation 聚合銷售數據

sales_data = pd.DataFrame({
    'region': ['North', 'North', 'North', 'South', 'South'],
    'sales': [1000, 1500, 2000, 800, 1200]
})

# 填寫代碼：計算地區的銷售總額和平均值
result = sales_data.groupby('region').agg(
    total_sales=('sales', ???),
    avg_sales=('sales', ???)
)

# 預期輸出：
#        total_sales  avg_sales
# region
# North        4500    1500.00
# South        2000    1000.00

print(result)
```

**答案提示**: 'sum' 和 'mean'

---

### 📌 Q2: 多個函數於同一列
```python
# 題目：對銷售數據計算多個統計指標

product_sales = pd.DataFrame({
    'category': ['A', 'A', 'A', 'B', 'B'],
    'product': ['P1', 'P2', 'P3', 'P4', 'P5'],
    'sales': [100, 150, 120, 200, 180]
})

# 填寫代碼：計算類別的銷售統計
result = product_sales.groupby('category').agg(
    total_sales=('sales', 'sum'),
    avg_sales=('sales', 'mean'),
    max_sales=('sales', 'max'),
    min_sales=('sales', 'min'),
    num_products=('product', 'count')
)

# 預期輸出：
#          total_sales  avg_sales  max_sales  min_sales  num_products
# category
# A              370        123.3        150        100              3
# B              380        190.0        200        180              2

print(result)
```

**答案提示**: 分別使用 sum, mean, max, min, count

---

### 📌 Q3: 多列聚合
```python
# 題目：聚合多個不同的欄位

customer_data = pd.DataFrame({
    'customer_id': ['C1', 'C1', 'C1', 'C2', 'C2'],
    'order_id': ['O1', 'O2', 'O3', 'O4', 'O5'],
    'amount': [100, 150, 120, 200, 180],
    'product_count': [2, 3, 2, 5, 3]
})

# 填寫代碼
result = customer_data.groupby('customer_id').agg(
    total_spent=('amount', 'sum'),
    num_orders=('order_id', 'count'),
    total_products=('product_count', 'sum'),
    avg_product_per_order=('product_count', 'mean')
)

# 預期輸出：
#            total_spent  num_orders  total_products  avg_product_per_order
# customer_id
# C1                 370           3               7                 2.333...
# C2                 380           2               8                 4.000

print(result)
```

---

### 📌 Q4: 多層分組聚合
```python
# 題目：按地區和類別進行多層聚合

sales_by_region_category = pd.DataFrame({
    'region': ['East', 'East', 'East', 'West', 'West'],
    'category': ['A', 'A', 'B', 'A', 'B'],
    'sales': [1000, 1500, 2000, 800, 1200]
})

# 填寫代碼：按地區和類別聚合
result = sales_by_region_category.groupby(['region', 'category']).agg(
    total_sales=('sales', 'sum'),
    avg_sales=('sales', 'mean'),
    count=('sales', 'count')
)

# 預期輸出：
#                  total_sales  avg_sales  count
# region category
# East   A              2500       1250       2
#        B              2000       2000       1
# West   A               800        800       1
#        B              1200       1200       1

print(result)
```

---

## 🟡 Medium Questions (5-9)

### 📌 Q5: 自訂聚合函數
```python
# 題目：定義並使用自訂聚合函數計算變異係數（標準差 / 平均值）

sales_variation = pd.DataFrame({
    'region': ['A', 'A', 'A', 'B', 'B', 'B'],
    'monthly_sales': [1000, 1100, 900, 2000, 1900, 2100]
})

def coefficient_of_variation(series):
    """計算變異係數"""
    return series.std() / series.mean() if series.mean() != 0 else 0

# 填寫代碼：使用自訂函數
result = sales_variation.groupby('region').agg(
    avg_sales=('monthly_sales', 'mean'),
    std_sales=('monthly_sales', 'std'),
    cv=('monthly_sales', coefficient_of_variation)
)

# 預期輸出：
#    avg_sales  std_sales        cv
# A       1000   100.0        0.1
# B       2000   100.0        0.05

print(result)
```

**答案提示**: 定義函數後直接作為參數傳遞

---

### 📌 Q6: 加權平均
```python
# 題目：計算加權平均評分

product_reviews = pd.DataFrame({
    'category': ['Electronics'] * 3 + ['Books'] * 3,
    'product': ['P1', 'P2', 'P3', 'P4', 'P5', 'P6'],
    'rating': [4.5, 4.8, 4.2, 4.9, 4.7, 4.3],
    'num_reviews': [1000, 500, 300, 100, 150, 2000]
})

def weighted_avg(values, weights):
    """計算加權平均"""
    # 需要在 groupby.apply 中使用，而不是 agg
    return (values * weights).sum() / weights.sum()

# 填寫代碼：計算類別的加權平均評分
result = product_reviews.groupby('category').apply(
    lambda x: pd.Series({
        'weighted_rating': weighted_avg(x['rating'], x['num_reviews']),
        'total_reviews': x['num_reviews'].sum(),
        'num_products': len(x)
    })
)

# 預期輸出：
#             weighted_rating  total_reviews  num_products
# category
# Books                4.467...           2250              3
# Electronics          4.505...           1800              3

print(result)
```

---

### 📌 Q7: 百分位聚合
```python
# 題目：計算銷售額的多個百分位數

sales_percentile = pd.DataFrame({
    'store': ['A'] * 10 + ['B'] * 10,
    'daily_sales': [1000, 1100, 1050, 950, 1200, 1150, 1080, 1020, 1100, 1050] +
                   [2000, 2100, 2050, 1950, 2200, 2150, 2080, 2020, 2100, 2050]
})

def percentile_25(series):
    return series.quantile(0.25)

def percentile_75(series):
    return series.quantile(0.75)

# 填寫代碼
result = sales_percentile.groupby('store').agg(
    min_sales=('daily_sales', 'min'),
    p25_sales=('daily_sales', percentile_25),
    median_sales=('daily_sales', 'median'),
    p75_sales=('daily_sales', percentile_75),
    max_sales=('daily_sales', 'max'),
    mean_sales=('daily_sales', 'mean')
)

# 預期輸出會顯示每個門店的銷售分佈
print(result)
```

---

### 📌 Q8: 跨多列的複雜聚合
```python
# 題目：生成完整的客戶摘要報表

customer_orders = pd.DataFrame({
    'customer_id': ['C1', 'C1', 'C1', 'C2', 'C2', 'C3'],
    'order_date': pd.date_range('2023-01-01', periods=6),
    'product_count': [2, 3, 1, 5, 3, 1],
    'amount': [100, 150, 50, 200, 180, 30],
    'region': ['East', 'East', 'East', 'West', 'West', 'South']
})

# 填寫代碼：生成完整的客戶報表
result = customer_orders.groupby('customer_id').agg(
    region=('region', 'first'),
    total_spent=('amount', 'sum'),
    num_orders=('order_id', 'count'),  # 錯誤：沒有 order_id 列，應改用其他
    avg_order_value=('amount', 'mean'),
    total_products=('product_count', 'sum'),
    first_purchase=('order_date', 'min'),
    last_purchase=('order_date', 'max')
)

# 修正版本（注意沒有 order_id，用其他方式計算訂單數）
result = customer_orders.groupby('customer_id').agg(
    region=('region', 'first'),
    total_spent=('amount', 'sum'),
    num_orders=('amount', 'count'),  # 使用任何列計數
    avg_order_value=('amount', 'mean'),
    total_products=('product_count', 'sum'),
    first_purchase=('order_date', 'min'),
    last_purchase=('order_date', 'max')
)

print(result)
```

---

### 📌 Q9: 條件聚合
```python
# 題目：計算高價訂單（>100）和低價訂單（<=100）的統計

orders = pd.DataFrame({
    'customer_id': ['C1', 'C1', 'C1', 'C2', 'C2', 'C2'],
    'order_value': [50, 150, 100, 200, 75, 125]
})

def high_value_count(series):
    return (series > 100).sum()

def low_value_count(series):
    return (series <= 100).sum()

# 填寫代碼
result = orders.groupby('customer_id').agg(
    total_orders=('order_value', 'count'),
    total_spent=('order_value', 'sum'),
    avg_order=('order_value', 'mean'),
    high_value_orders=('order_value', high_value_count),
    low_value_orders=('order_value', low_value_count),
    max_order=('order_value', 'max')
)

# 預期輸出：
#            total_orders  total_spent  avg_order  high_value_orders  low_value_orders  max_order
# customer_id
# C1                     3          300      100.0                  1                  2        150
# C2                     3          400      133.3                  2                  1        200

print(result)
```

---

## 🔴 Hard Questions (10-12)

### 📌 Q10: 完整的銷售報表（多欄位多函數）
```python
# 題目：生成完整的產品類別銷售報表

product_sales_detail = pd.DataFrame({
    'category': ['Electronics', 'Electronics', 'Electronics', 'Electronics',
                 'Books', 'Books', 'Books'],
    'product': ['P1', 'P2', 'P3', 'P4', 'P5', 'P6', 'P7'],
    'units_sold': [100, 150, 120, 90, 200, 250, 180],
    'unit_price': [500, 400, 600, 700, 20, 25, 30],
    'profit_margin': [0.30, 0.25, 0.35, 0.28, 0.40, 0.45, 0.35]
})

# 計算銷售額
product_sales_detail['revenue'] = product_sales_detail['units_sold'] * product_sales_detail['unit_price']
product_sales_detail['profit'] = product_sales_detail['revenue'] * product_sales_detail['profit_margin']

# 填寫代碼：生成完整的類別報表
result = product_sales_detail.groupby('category').agg(
    num_products=('product', 'count'),
    total_units=('units_sold', 'sum'),
    total_revenue=('revenue', 'sum'),
    total_profit=('profit', 'sum'),
    avg_unit_price=('unit_price', 'mean'),
    avg_margin=('profit_margin', 'mean'),
    revenue_per_product=('revenue', 'mean')
)

result['profit_margin_pct'] = (result['total_profit'] / result['total_revenue'] * 100).round(2)

# 預期輸出包含完整的財務指標
print(result)
```

---

### 📌 Q11: 時間序列聚合報表
```python
# 題目：按月份和地區生成銷售趨勢報表

sales_timeseries = pd.DataFrame({
    'date': pd.date_range('2023-01-01', periods=12, freq='D'),
    'region': ['North'] * 4 + ['South'] * 4 + ['East'] * 4,
    'sales': [1000, 1100, 950, 1200, 800, 900, 850, 950, 1500, 1600, 1400, 1550]
})

sales_timeseries['week'] = sales_timeseries['date'].dt.isocalendar().week

# 填寫代碼：按周和地區聚合
result = sales_timeseries.groupby(['week', 'region']).agg(
    total_sales=('sales', 'sum'),
    avg_daily_sales=('sales', 'mean'),
    max_daily_sales=('sales', 'max'),
    min_daily_sales=('sales', 'min'),
    num_days=('sales', 'count')
)

print(result)

# 額外分析：計算周度增長率
result_reset = result.reset_index()
region_groups = result_reset.groupby('region')
for region_name, group in region_groups:
    print(f"\n{region_name} 的周度增長：")
    print(group[['week', 'total_sales']].reset_index(drop=True))
```

---

### 📌 Q12: RFM 分析完整報表
```python
# 題目：生成完整的 RFM 分析報表，包含客戶分群

customer_transactions = pd.DataFrame({
    'customer_id': ['C1', 'C1', 'C1', 'C2', 'C2', 'C3', 'C3', 'C3', 'C3'],
    'transaction_date': [
        '2023-01-01', '2023-06-01', '2023-11-01',  # C1
        '2023-03-01', '2023-10-01',                 # C2
        '2023-01-15', '2023-02-20', '2023-09-01', '2023-12-01'  # C3
    ],
    'amount': [100, 150, 120, 200, 250, 50, 60, 80, 100]
})

# 設定參考日期
reference_date = pd.Timestamp('2023-12-31')
customer_transactions['transaction_date'] = pd.to_datetime(customer_transactions['transaction_date'])

# 填寫代碼：計算 RFM 並生成報表
rfm_result = customer_transactions.groupby('customer_id').agg(
    recency=('transaction_date', lambda x: (reference_date - x.max()).days),
    frequency=('transaction_date', 'count'),
    monetary=('amount', 'sum')
).reset_index()

# 計算五分位分級
rfm_result['R_score'] = pd.qcut(rfm_result['recency'], q=3, labels=[3,2,1], duplicates='drop')
rfm_result['F_score'] = pd.qcut(rfm_result['frequency'].rank(method='first'), q=3, labels=[1,2,3], duplicates='drop')
rfm_result['M_score'] = pd.qcut(rfm_result['monetary'].rank(method='first'), q=3, labels=[1,2,3], duplicates='drop')

print("RFM 分析結果:")
print(rfm_result)

# 進一步聚合：按 RFM 分數分組統計
rfm_result['rfm_score'] = rfm_result['R_score'].astype(int) + rfm_result['F_score'].astype(int) + rfm_result['M_score'].astype(int)

segment_summary = rfm_result.groupby('rfm_score').agg(
    num_customers=('customer_id', 'count'),
    avg_recency=('recency', 'mean'),
    avg_frequency=('frequency', 'mean'),
    avg_monetary=('monetary', 'mean'),
    total_monetary=('monetary', 'sum')
)

print("\nRFM 分數分佈:")
print(segment_summary)
```

---

## 常見技巧與陷阱

### ✓ 最佳實踐
```python
# 1. 使用清晰的列名
result = df.groupby('col').agg(
    total_value=('amount', 'sum'),      # ✓ 清晰
    avg_value=('amount', 'mean'),       # ✓ 清晰
    # vs
    ('amount', ['sum', 'mean'])         # ❌ 列名不清晰
)

# 2. 處理多欄位時使用一致的命名規則
result = df.groupby('group').agg(
    num_records=('id', 'count'),        # 計數用 num_
    total_spent=('amount', 'sum'),      # 求和用 total_
    avg_spent=('amount', 'mean')        # 平均用 avg_
)

# 3. 複雜聚合使用 apply
result = df.groupby('group').apply(
    lambda x: pd.Series({
        'complex_metric': some_complex_function(x)
    })
)
```

### ❌ 常見錯誤
```python
# 錯誤1: 列名重複
result = df.groupby('col').agg(
    sum=('amount', 'sum'),
    sum=('amount', 'mean')  # ❌ 列名重複，會報錯
)

# 錯誤2: 忘記括號
result = df.groupby('col').agg(
    total_sales=('sales', sum)  # ❌ sum 應該是字符串 'sum'
)

# 錯誤3: 自訂函數返回類型錯誤
def custom_agg(series):
    return series.sum() / len(series)  # ✓ 返回標量（正確）

def custom_agg(series):
    return series  # ❌ 返回 Series（會報錯）
```

---

## 答案提交格式

```markdown
### Q1 答案
```python
# 代碼...
```

說明: ...
```

---

**參考資源**
- Day 11: Named Aggregation 命名聚合指南
- Pandas groupby().agg() 官方文檔

---

**更新時間**: 2025-12-11
**版本**: 1.0
