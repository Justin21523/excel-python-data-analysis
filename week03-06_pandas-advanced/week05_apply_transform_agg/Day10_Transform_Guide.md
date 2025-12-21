# Day 10: Transform 保持形狀的魔法轉換 (2.5-3 小時)

## 📚 目錄
1. [Transform 基礎概念](#transform-基礎概念)
2. [組內標準化與排名](#組內標準化與排名)
3. [組內百分比與累計計算](#組內百分比與累計計算)
4. [10 個實戰案例](#10-個實戰案例)
5. [Excel 對照教學](#excel-對照教學)

---

## Transform 基礎概念

### 1.1 什麼是 Transform？（30 分鐘）

Transform 是 GroupBy 操作中最特殊的方法，它：
- 應用函數到每個組
- **保持原始形狀**（返回與輸入相同大小的結果）
- 自動廣播結果回原表
- 適合計算「相對於組內」的值

**核心差異：**

```python
import pandas as pd
from olist.datasets import load_datasets

# 加載數據
orders_df = load_datasets('orders')
order_items_df = load_datasets('order_items')

# 準備測試數據
data = pd.DataFrame({
    'city': ['São Paulo', 'São Paulo', 'São Paulo', 'Rio de Janeiro', 'Rio de Janeiro', 'Belo Horizonte'],
    'sales': [1000, 1500, 2000, 800, 1200, 900]
})

print("原始數據：")
print(data)

# ==== 方法1: agg（聚合）- 返回縮小的結果 ====
agg_result = data.groupby('city')['sales'].agg('sum')
print("\nagg 結果（縮小）:")
print(agg_result)
print(f"形狀: {agg_result.shape}")  # (3,)

# ==== 方法2: transform（轉換）- 返回原始大小 ====
transform_result = data.groupby('city')['sales'].transform('sum')
print("\ntransform 結果（保持形狀）:")
print(transform_result)
print(f"形狀: {transform_result.shape}")  # (6,)

# ==== 方法3: apply（應用）- 視情況而定 ====
apply_result = data.groupby('city')['sales'].apply(list)
print("\napply 結果（視函數而定）:")
print(apply_result)
```

**關鍵區別圖示：**

```
原始數據 (6 行):
城市              銷售
São Paulo       1000
São Paulo       1500
São Paulo       2000
Rio de Janeiro   800
Rio de Janeiro  1200
Belo Horizonte   900

agg('sum') 結果 (3 行):
城市                 銷售
Belo Horizonte      900
Rio de Janeiro     2000
São Paulo          4500

transform('sum') 結果 (6 行):
城市              銷售
São Paulo       4500
São Paulo       4500
São Paulo       4500
Rio de Janeiro  2000
Rio de Janeiro  2000
Belo Horizonte   900
```

### 1.2 Transform 的基本語法（20 分鐺）

```python
# 基本語法
df.groupby('group_column')[target_column].transform(function)

# 案例：計算每個城市的平均銷售額，並廣播回原表
city_avg = data.groupby('city')['sales'].transform('mean')
data['city_avg_sales'] = city_avg

print(data)
```

**常見的內置函數：**

```python
# 統計函數
data['sum_by_city'] = data.groupby('city')['sales'].transform('sum')
data['mean_by_city'] = data.groupby('city')['sales'].transform('mean')
data['count_by_city'] = data.groupby('city')['sales'].transform('count')
data['min_by_city'] = data.groupby('city')['sales'].transform('min')
data['max_by_city'] = data.groupby('city')['sales'].transform('max')
data['std_by_city'] = data.groupby('city')['sales'].transform('std')

print(data)
```

**輸出：**
```
      city  sales  sum_by_city  mean_by_city  count_by_city  min_by_city  max_by_city  std_by_city
0  São Paulo   1000        4500        1500              3         1000         2000    500.000000
1  São Paulo   1500        4500        1500              3         1000         2000    500.000000
2  São Paulo   2000        4500        1500              3         1000         2000    500.000000
3  Rio ...    800        2000        1000              2          800         1200    282.842712
4  Rio ...   1200        2000        1000              2          800         1200    282.842712
5  Belo H...   900         900         900              1          900          900         NaN
```

### 1.3 自訂函數應用（30 分鐺）

```python
# Transform 也支持自訂函數

def z_score_normalize(group):
    """Z-score 標準化：(x - mean) / std"""
    return (group - group.mean()) / group.std()

def min_max_normalize(group):
    """Min-Max 標準化：(x - min) / (max - min)"""
    return (group - group.min()) / (group.max() - group.min())

def rank_in_group(group):
    """組內排名"""
    return group.rank()

# 應用自訂函數
data['z_score'] = data.groupby('city')['sales'].transform(z_score_normalize)
data['min_max'] = data.groupby('city')['sales'].transform(min_max_normalize)
data['rank'] = data.groupby('city')['sales'].transform(rank_in_group)

print(data[['city', 'sales', 'z_score', 'min_max', 'rank']])
```

---

## 組內標準化與排名

### 2.1 Z-score 標準化（30 分鐺）

Z-score 標準化是機器學習中的重要技術，將數據轉換為平均值 0、標準差 1 的分佈。

```python
import numpy as np

# 準備銷售數據
sales_data = pd.DataFrame({
    'department': ['Sales', 'Sales', 'Sales', 'Marketing', 'Marketing', 'Marketing', 'Tech', 'Tech', 'Tech'],
    'employee': ['A', 'B', 'C', 'D', 'E', 'F', 'G', 'H', 'I'],
    'monthly_revenue': [50000, 80000, 70000, 40000, 55000, 45000, 35000, 60000, 50000]
})

print("原始數據:")
print(sales_data)

# 方法1: 使用 transform 自訂函數
def z_score(group):
    """計算 Z-score"""
    return (group - group.mean()) / group.std()

sales_data['revenue_zscore'] = sales_data.groupby('department')['monthly_revenue'].transform(z_score)

print("\nZ-score 結果:")
print(sales_data[['department', 'monthly_revenue', 'revenue_zscore']])

# 方法2: 直接使用 lambda（對於簡單函數）
sales_data['revenue_normalized'] = sales_data.groupby('department')['monthly_revenue'].transform(
    lambda x: (x - x.mean()) / x.std()
)

# 驗證：標準化後的均值應該約等於 0，標準差應該約等於 1
print("\n驗證標準化結果:")
for dept in sales_data['department'].unique():
    dept_data = sales_data[sales_data['department'] == dept]['revenue_zscore']
    print(f"{dept:12} - 平均值: {dept_data.mean():.6f}, 標準差: {dept_data.std():.6f}")
```

**輸出示例：**
```
驗證標準化結果:
Sales        - 平均值: 0.000000, 標準差: 1.000000
Marketing    - 平均值: 0.000000, 標準差: 1.000000
Tech         - 平均值: 0.000000, 標準差: 1.000000
```

### 2.2 組內排名（30 分鐺）

```python
# 準備產品銷售數據
product_sales = pd.DataFrame({
    'category': ['電子', '電子', '電子', '家居', '家居', '家居', '服裝', '服裝'],
    'product': ['手機', '平板', '筆電', '沙發', '桌子', '椅子', '襯衣', '褲子'],
    'sales': [50000, 45000, 60000, 8000, 12000, 6000, 15000, 18000]
})

print("原始數據:")
print(product_sales)

# 方法1: 默認排名（昇序，相同值給相同排名）
product_sales['rank_asc'] = product_sales.groupby('category')['sales'].transform('rank')

# 方法2: 降序排名（大的排名靠前）
product_sales['rank_desc'] = product_sales.groupby('category')['sales'].transform(
    lambda x: x.rank(ascending=False)
)

# 方法3: 百分位排名（0-1 之間）
product_sales['percentile_rank'] = product_sales.groupby('category')['sales'].transform(
    lambda x: x.rank(pct=True)
)

# 方法4: 處理平手（dense_rank：沒有間隔）
product_sales['dense_rank'] = product_sales.groupby('category')['sales'].transform(
    lambda x: x.rank(method='dense', ascending=False)
)

print("\n排名結果:")
print(product_sales[['category', 'product', 'sales', 'rank_asc', 'rank_desc', 'percentile_rank', 'dense_rank']])
```

**輸出示例：**
```
category  product  sales  rank_asc  rank_desc  percentile_rank  dense_rank
電子        手機    50000      2      2          0.666667         2
電子        平板    45000      1      3          0.333333         3
電子        筆電    60000      3      1          1.000000         1
家居        沙發     8000      2      2          0.666667         2
家居        桌子    12000      3      1          1.000000         1
家居        椅子     6000      1      3          0.333333         3
...
```

### 2.3 實際應用：識別組內高績效者（30 分鐺）

```python
# 加載真實數據
orders_df = load_datasets('orders')
order_items_df = load_datasets('order_items')
sellers_df = load_datasets('sellers')

# 計算賣家月度銷售
seller_sales = order_items_df.merge(
    orders_df[['order_id', 'order_purchase_timestamp']],
    on='order_id'
)

seller_sales['month'] = seller_sales['order_purchase_timestamp'].dt.to_period('M')

# 計算每個賣家每月的銷售額
monthly_sales = seller_sales.groupby(['month', 'seller_id']).agg({
    'price': 'sum',
    'order_id': 'count'
}).reset_index()

monthly_sales.columns = ['month', 'seller_id', 'total_sales', 'order_count']

print("賣家月度銷售:")
print(monthly_sales.head(10))

# 方法1: 計算每月的平均銷售額和標準差
monthly_sales['month_avg_sales'] = monthly_sales.groupby('month')['total_sales'].transform('mean')
monthly_sales['month_std_sales'] = monthly_sales.groupby('month')['total_sales'].transform('std')

# 計算 Z-score，識別異常高的銷售（> 2 個標準差）
monthly_sales['sales_zscore'] = (
    (monthly_sales['total_sales'] - monthly_sales['month_avg_sales']) /
    monthly_sales['month_std_sales']
)

monthly_sales['performance'] = monthly_sales['sales_zscore'].apply(
    lambda z: '超高績效' if z > 2 else ('高績效' if z > 1 else ('正常' if z > -1 else '低績效'))
)

# 方法2: 計算組內排名
monthly_sales['month_rank'] = monthly_sales.groupby('month')['total_sales'].transform(
    lambda x: x.rank(ascending=False)
)

monthly_sales['percentile'] = monthly_sales.groupby('month')['total_sales'].transform(
    lambda x: x.rank(pct=True)
)

# 篩選每月的頂級賣家（排名前 10%）
top_sellers = monthly_sales[monthly_sales['percentile'] >= 0.90]

print("\n每月頂級賣家（前 10%）:")
print(top_sellers[['month', 'seller_id', 'total_sales', 'month_rank', 'performance']].head(20))

# 統計：多少賣家表現超常
print(f"\n超高績效賣家：{(monthly_sales['performance'] == '超高績效').sum()} 人")
print(f"高績效賣家：{(monthly_sales['performance'] == '高績效').sum()} 人")
```

---

## 組內百分比與累計計算

### 3.1 佔比計算（30 分鐺）

```python
# 準備類別銷售數據
category_sales = pd.DataFrame({
    'region': ['North', 'North', 'North', 'South', 'South', 'South', 'East', 'East'],
    'category': ['A', 'B', 'C', 'A', 'B', 'C', 'A', 'B'],
    'sales': [10000, 15000, 5000, 20000, 8000, 12000, 18000, 22000]
})

print("原始數據:")
print(category_sales)

# 方法1: 計算佔地區總銷售額的百分比
category_sales['region_total'] = category_sales.groupby('region')['sales'].transform('sum')
category_sales['pct_of_region'] = (category_sales['sales'] / category_sales['region_total'] * 100).round(2)

print("\n地區內佔比:")
print(category_sales[['region', 'category', 'sales', 'pct_of_region']])

# 方法2: 計算佔全國總銷售額的百分比
total_sales = category_sales['sales'].sum()
category_sales['pct_of_total'] = (category_sales['sales'] / total_sales * 100).round(2)

print("\n全國總銷售額占比:")
print(category_sales[['region', 'category', 'sales', 'pct_of_total']])

# 方法3: 計算佔該類別總銷售額的百分比（跨地區）
category_sales['category_total'] = category_sales.groupby('category')['sales'].transform('sum')
category_sales['pct_of_category'] = (category_sales['sales'] / category_sales['category_total'] * 100).round(2)

print("\n類別內地區占比:")
print(category_sales[['region', 'category', 'sales', 'pct_of_category']])
```

**輸出示例：**
```
region category  sales  pct_of_region  pct_of_total  category_total  pct_of_category
North    A      10000          33.33           6.25       48000        20.83
North    B      15000          50.00           9.38       30000        50.00
North    C       5000          16.67           3.13       17000        29.41
South    A      20000          55.56          12.50       48000        41.67
South    B       8000          22.22           5.00       30000        26.67
South    C      12000          33.33           7.50       17000        70.59
...
```

### 3.2 累計百分比（20 分鐺）

```python
# 計算累計銷售額百分比（用於帕累托分析）

# 首先按銷售額排序
category_sales_sorted = category_sales.sort_values('sales', ascending=False).reset_index(drop=True)

print("按銷售額排序:")
print(category_sales_sorted[['region', 'category', 'sales']])

# 計算累計銷售額
category_sales_sorted['cumsum_sales'] = category_sales_sorted['sales'].cumsum()

# 計算累計百分比
total = category_sales_sorted['sales'].sum()
category_sales_sorted['cumsum_pct'] = (category_sales_sorted['cumsum_sales'] / total * 100).round(2)

print("\n累計銷售額和百分比:")
print(category_sales_sorted[['region', 'category', 'sales', 'cumsum_sales', 'cumsum_pct']])

# 識別帕累托項目（80-20 法則：前 80% 銷售額的項目）
category_sales_sorted['pareto_rank'] = category_sales_sorted['cumsum_pct'].apply(
    lambda x: '80%內' if x <= 80 else '非關鍵'
)

print("\n帕累托分析:")
print(category_sales_sorted[['category', 'sales', 'cumsum_pct', 'pareto_rank']])
```

### 3.3 組內累計計算（30 分鐺）

```python
# 假設有月度銷售數據
monthly_data = pd.DataFrame({
    'department': ['Sales', 'Sales', 'Sales', 'Sales', 'Marketing', 'Marketing', 'Marketing', 'Marketing'],
    'month': [1, 2, 3, 4, 1, 2, 3, 4],
    'revenue': [100000, 120000, 130000, 140000, 50000, 55000, 60000, 65000]
})

print("月度銷售數據:")
print(monthly_data)

# 方法1: 按部門計算累計收入
monthly_data_sorted = monthly_data.sort_values(['department', 'month'])
monthly_data_sorted['dept_cumsum'] = monthly_data_sorted.groupby('department')['revenue'].cumsum()

print("\n按部門累計:")
print(monthly_data_sorted[['department', 'month', 'revenue', 'dept_cumsum']])

# 方法2: 計算組內累計百分比
monthly_data_sorted['dept_total'] = monthly_data_sorted.groupby('department')['revenue'].transform('sum')
monthly_data_sorted['dept_cumsum_pct'] = (
    monthly_data_sorted['dept_cumsum'] / monthly_data_sorted['dept_total'] * 100
).round(2)

print("\n累計百分比:")
print(monthly_data_sorted[['department', 'month', 'revenue', 'dept_cumsum_pct']])

# 方法3: 計算組內增長率（與前月相比）
monthly_data_sorted['revenue_prev'] = monthly_data_sorted.groupby('department')['revenue'].shift(1)
monthly_data_sorted['growth_rate'] = (
    (monthly_data_sorted['revenue'] - monthly_data_sorted['revenue_prev']) /
    monthly_data_sorted['revenue_prev'] * 100
).round(2)

print("\n月度增長率:")
print(monthly_data_sorted[['department', 'month', 'revenue', 'growth_rate']])
```

---

## 10 個實戰案例

### 案例 1-3: 基礎 Transform 應用

**案例1: 計算銷售額與組平均值的差距**
```python
# 業務目標：了解每個銷售人員相對於團隊平均的表現

sales_team = pd.DataFrame({
    'team': ['North', 'North', 'North', 'South', 'South', 'South'],
    'employee': ['Alice', 'Bob', 'Charlie', 'David', 'Eve', 'Frank'],
    'sales_amount': [50000, 45000, 60000, 55000, 48000, 52000]
})

# 計算組平均
sales_team['team_avg'] = sales_team.groupby('team')['sales_amount'].transform('mean')

# 計算差距
sales_team['gap_to_avg'] = sales_team['sales_amount'] - sales_team['team_avg']
sales_team['gap_pct'] = (sales_team['gap_to_avg'] / sales_team['team_avg'] * 100).round(2)

print("銷售績效分析:")
print(sales_team[['team', 'employee', 'sales_amount', 'team_avg', 'gap_to_avg', 'gap_pct']])

# 識別表現超群者
sales_team['performance_level'] = sales_team['gap_pct'].apply(
    lambda x: '超常' if x > 10 else ('正常' if x > -10 else '低於平均')
)

print(sales_team[['employee', 'performance_level']])
```

**案例2: 計算學生分數與班級平均分的標準差**
```python
# 教育場景：分析學生成績在班級中的相對位置

student_grades = pd.DataFrame({
    'class': ['A', 'A', 'A', 'A', 'B', 'B', 'B', 'B'],
    'student': ['S1', 'S2', 'S3', 'S4', 'S5', 'S6', 'S7', 'S8'],
    'math_score': [85, 92, 78, 88, 75, 88, 82, 95]
})

# 計算 Z-score（相對於班級）
student_grades['z_score'] = student_grades.groupby('class')['math_score'].transform(
    lambda x: (x - x.mean()) / x.std()
)

# 判斷優秀/及格/不及格
def grade_performance(z_score):
    if z_score > 1:
        return '優秀'
    elif z_score > -0.5:
        return '良好'
    else:
        return '需改進'

student_grades['performance'] = student_grades['z_score'].apply(grade_performance)

print("學生成績相對分析:")
print(student_grades[['class', 'student', 'math_score', 'z_score', 'performance']])
```

**案例3: 計算產品在分類中的銷售排名**
```python
# 電商場景：了解每個產品在其分類中的排名

product_data = pd.DataFrame({
    'category': ['Electronics', 'Electronics', 'Electronics', 'Books', 'Books', 'Books'],
    'product_name': ['Laptop', 'Phone', 'Tablet', 'Python Book', 'Data Book', 'Novel'],
    'monthly_sales': [50, 150, 80, 300, 250, 180]
})

# 計算分類內排名
product_data['category_rank'] = product_data.groupby('category')['monthly_sales'].transform(
    lambda x: x.rank(ascending=False)
)

# 計算分類內百分位
product_data['percentile'] = product_data.groupby('category')['monthly_sales'].transform(
    lambda x: x.rank(pct=True)
)

# 判斷暢銷度
product_data['sales_status'] = product_data['percentile'].apply(
    lambda x: '熱銷' if x >= 0.7 else ('暢銷' if x >= 0.4 else '需推廣')
)

print("產品排名分析:")
print(product_data[['category', 'product_name', 'monthly_sales', 'category_rank', 'sales_status']])
```

### 案例 4-7: 高級 Transform 應用

**案例4: 客戶價值評分（使用真實數據）**
```python
# 加載數據
orders_df = load_datasets('orders')
order_payments_df = load_datasets('order_payments')
customers_df = load_datasets('customers')

# 計算客戶消費統計（前 500 個客戶示例）
customer_purchases = order_payments_df.groupby('order_id')['payment_value'].sum().reset_index()
customer_purchases = customer_purchases.merge(
    orders_df[['order_id', 'customer_id', 'order_purchase_timestamp']],
    on='order_id'
)

customer_summary = customer_purchases.groupby('customer_id').agg({
    'payment_value': ['sum', 'mean', 'count'],
    'order_purchase_timestamp': 'max'
}).reset_index()

customer_summary.columns = ['customer_id', 'total_spent', 'avg_order', 'order_count', 'last_purchase']
customer_summary = customer_summary.head(500)

# 計算分位數排名（相對於所有客戶）
customer_summary['total_spent_percentile'] = customer_summary['total_spent'].rank(pct=True)
customer_summary['order_count_percentile'] = customer_summary['order_count'].rank(pct=True)
customer_summary['avg_order_percentile'] = customer_summary['avg_order'].rank(pct=True)

# 計算綜合評分（0-100）
customer_summary['value_score'] = (
    customer_summary['total_spent_percentile'] * 0.4 +
    customer_summary['order_count_percentile'] * 0.35 +
    customer_summary['avg_order_percentile'] * 0.25
) * 100

# 根據評分分級
def assign_value_tier(score):
    if score >= 80:
        return 'Platinum'
    elif score >= 60:
        return 'Gold'
    elif score >= 40:
        return 'Silver'
    else:
        return 'Bronze'

customer_summary['value_tier'] = customer_summary['value_score'].apply(assign_value_tier)

print("客戶價值評分分佈:")
print(customer_summary['value_tier'].value_counts())
print("\nTop 10 高價值客戶:")
print(customer_summary.nlargest(10, 'value_score')[
    ['customer_id', 'total_spent', 'order_count', 'value_score', 'value_tier']
])
```

**案例5: 銷售排序異常檢測**
```python
# 使用 transform 識別異常高或異常低的交易

transactions = pd.DataFrame({
    'seller_id': ['S1', 'S1', 'S1', 'S1', 'S1', 'S2', 'S2', 'S2', 'S2', 'S2'],
    'order_amount': [100, 105, 98, 102, 500, 50, 48, 52, 49, 51]
})

print("原始交易數據:")
print(transactions)

# 計算每個賣家的統計數據
transactions['seller_mean'] = transactions.groupby('seller_id')['order_amount'].transform('mean')
transactions['seller_std'] = transactions.groupby('seller_id')['order_amount'].transform('std')

# 計算 Z-score
transactions['z_score'] = (
    (transactions['order_amount'] - transactions['seller_mean']) /
    transactions['seller_std']
)

# 判斷是否異常
transactions['is_anomaly'] = transactions['z_score'].apply(
    lambda z: '異常高' if z > 2 else ('異常低' if z < -2 else '正常')
)

print("\n異常檢測結果:")
print(transactions[['seller_id', 'order_amount', 'z_score', 'is_anomaly']])
```

**案例6: 市場份額計算**
```python
# 計算每個公司在市場中的份額

market_data = pd.DataFrame({
    'year': [2022, 2022, 2022, 2023, 2023, 2023],
    'company': ['Apple', 'Samsung', 'Xiaomi', 'Apple', 'Samsung', 'Xiaomi'],
    'sales': [100, 80, 60, 110, 75, 70]
})

print("原始銷售數據:")
print(market_data)

# 計算年度市場份額
market_data['year_total'] = market_data.groupby('year')['sales'].transform('sum')
market_data['market_share'] = (market_data['sales'] / market_data['year_total'] * 100).round(2)

# 計算同比增長
market_data['rank'] = market_data.groupby('year')['sales'].transform(lambda x: x.rank(ascending=False))

print("\n市場份額分析:")
print(market_data[['year', 'company', 'sales', 'market_share', 'rank']])
```

**案例7: 客戶流失預警分數**
```python
# 計算每個客戶相對於同群組的流失風險

from datetime import datetime, timedelta

# 假設參考日期
reference_date = pd.Timestamp('2024-01-01')

churn_data = pd.DataFrame({
    'segment': ['Premium', 'Premium', 'Premium', 'Standard', 'Standard', 'Standard'],
    'customer_id': ['C1', 'C2', 'C3', 'C4', 'C5', 'C6'],
    'days_since_purchase': [15, 45, 90, 20, 60, 30],
    'purchase_count': [50, 10, 5, 30, 8, 20]
})

print("客戶數據:")
print(churn_data)

# 計算段內平均值
churn_data['segment_avg_recency'] = churn_data.groupby('segment')['days_since_purchase'].transform('mean')
churn_data['segment_avg_frequency'] = churn_data.groupby('segment')['purchase_count'].transform('mean')

# 計算偏離度（標準化）
churn_data['recency_deviation'] = (
    (churn_data['days_since_purchase'] - churn_data['segment_avg_recency']) /
    churn_data.groupby('segment')['days_since_purchase'].transform('std')
)

# 計算流失風險分數
churn_data['churn_risk'] = (
    churn_data['days_since_purchase'] / 30 * 0.6 +  # 最近性 60% 權重
    (1 - churn_data['purchase_count'] / churn_data.groupby('segment')['purchase_count'].transform('max')) * 40  # 頻率 40% 權重
).round(0)

print("\n流失風險分析:")
print(churn_data[['segment', 'customer_id', 'days_since_purchase', 'churn_risk']])
```

### 案例 8-10: 複雜業務場景

**案例8: 滾動相對排名（組內月份排名）**
```python
# 每月內的銷售排名

monthly_sales = pd.DataFrame({
    'month': [1, 1, 1, 2, 2, 2, 3, 3, 3],
    'salesperson': ['Alice', 'Bob', 'Charlie', 'Alice', 'Bob', 'Charlie', 'Alice', 'Bob', 'Charlie'],
    'sales': [100, 120, 110, 130, 115, 125, 140, 135, 145]
})

# 計算每月排名
monthly_sales['month_rank'] = monthly_sales.groupby('month')['sales'].transform(
    lambda x: x.rank(ascending=False)
)

# 計算月度增長（與前月同期相比）
monthly_sales['prev_sales'] = monthly_sales.groupby('salesperson')['sales'].shift(1)
monthly_sales['growth'] = (
    (monthly_sales['sales'] - monthly_sales['prev_sales']) /
    monthly_sales['prev_sales'] * 100
).round(2)

print("月度銷售排名:")
print(monthly_sales[['month', 'salesperson', 'sales', 'month_rank', 'growth']])
```

**案例9: 庫存周轉率比較**
```python
# 計算產品相對於類別平均的庫存周轉率

inventory = pd.DataFrame({
    'category': ['Electronics', 'Electronics', 'Electronics', 'Books', 'Books', 'Books'],
    'product': ['Phone', 'Laptop', 'Tablet', 'Fiction', 'Non-Fiction', 'Reference'],
    'turnover_rate': [12, 8, 10, 24, 18, 6]
})

# 計算類別平均
inventory['category_avg_turnover'] = inventory.groupby('category')['turnover_rate'].transform('mean')

# 計算相對表現
inventory['relative_performance'] = (
    inventory['turnover_rate'] / inventory['category_avg_turnover']
).round(2)

# 判斷庫存管理效率
inventory['inventory_status'] = inventory['relative_performance'].apply(
    lambda x: '高效' if x > 1.2 else ('正常' if x > 0.8 else '低效')
)

print("庫存周轉率分析:")
print(inventory[['category', 'product', 'turnover_rate', 'relative_performance', 'inventory_status']])
```

**案例10: 完整的多層級分析（組織層級）**
```python
# 完整的公司層級分析：公司 → 部門 → 團隊 → 個人

organization = pd.DataFrame({
    'department': ['Sales', 'Sales', 'Sales', 'Sales', 'Marketing', 'Marketing', 'Marketing'],
    'team': ['Team A', 'Team A', 'Team B', 'Team B', 'Digital', 'Digital', 'Content'],
    'employee': ['E1', 'E2', 'E3', 'E4', 'E5', 'E6', 'E7'],
    'performance': [90, 85, 88, 92, 80, 78, 82]
})

# 層級 1：全公司排名
organization['company_rank'] = organization['performance'].rank(ascending=False)
organization['company_percentile'] = organization['performance'].rank(pct=True)

# 層級 2：部門排名
organization['dept_rank'] = organization.groupby('department')['performance'].transform(
    lambda x: x.rank(ascending=False)
)
organization['dept_percentile'] = organization.groupby('department')['performance'].transform(
    lambda x: x.rank(pct=True)
)

# 層級 3：團隊排名
organization['team_rank'] = organization.groupby('team')['performance'].transform(
    lambda x: x.rank(ascending=False)
)

# 層級 4：計算每層級的平均值
organization['dept_avg'] = organization.groupby('department')['performance'].transform('mean')
organization['team_avg'] = organization.groupby('team')['performance'].transform('mean')

# 判斷績效等級
def assign_performance_level(row):
    if row['performance'] >= row['dept_avg'] and row['company_percentile'] >= 0.75:
        return 'Top Performer'
    elif row['performance'] >= row['team_avg']:
        return 'Above Average'
    else:
        return 'Needs Improvement'

organization['level'] = organization.apply(assign_performance_level, axis=1)

print("多層級績效分析:")
print(organization[['department', 'team', 'employee', 'performance', 'dept_rank', 'team_rank', 'level']])

print("\n統計分析:")
for dept in organization['department'].unique():
    dept_data = organization[organization['department'] == dept]
    print(f"\n{dept}:")
    print(f"  - 員工數: {len(dept_data)}")
    print(f"  - 平均績效: {dept_data['performance'].mean():.1f}")
    print(f"  - Top Performer 數量: {(dept_data['level'] == 'Top Performer').sum()}")
```

---

## Excel 對照教學

### Transform vs Excel 中的廣播公式

#### 對照1: 簡單廣播

**Excel 方法:**
```
A列：城市       B列：銷售額    C列：城市總銷售（輔助）
São Paulo     1000          SUMIF($A:$A, A2, $B:$B)
São Paulo     1500          SUMIF($A:$A, A2, $B:$B)
São Paulo     2000          SUMIF($A:$A, A2, $B:$B)
Rio de Janeiro 800          SUMIF($A:$A, A2, $B:$B)
```

**Python Transform:**
```python
df['city_total'] = df.groupby('city')['sales'].transform('sum')
```

#### 對照2: 佔比計算

**Excel 方法:**
```
= B2 / SUMIF($A:$A, A2, $B:$B) * 100
```

**Python Transform:**
```python
df['pct'] = (df['sales'] / df.groupby('city')['sales'].transform('sum') * 100)
```

#### 對照3: Z-score 標準化

**Excel 方法:**
```
= (B2 - AVERAGEIF($A:$A, A2, $B:$B)) / STDEV(IF($A:$A=A2, $B:$B))
```

**Python Transform:**
```python
df['z_score'] = df.groupby('city')['sales'].transform(
    lambda x: (x - x.mean()) / x.std()
)
```

---

## 完整工作流範例

```python
# 完整的客戶價值分析流程

# 1. 加載原始數據
orders = load_datasets('orders')
payments = load_datasets('order_payments')
customers = load_datasets('customers')

# 2. 計算客戶基礎指標
customer_orders = payments.merge(
    orders[['order_id', 'customer_id']],
    on='order_id'
)

customer_stats = customer_orders.groupby('customer_id').agg({
    'payment_value': ['sum', 'mean', 'count']
}).reset_index()

customer_stats.columns = ['customer_id', 'total_spent', 'avg_order', 'order_count']

# 3. 計算統計分位數
customer_stats['percentile_spent'] = customer_stats['total_spent'].rank(pct=True)
customer_stats['percentile_count'] = customer_stats['order_count'].rank(pct=True)

# 4. 使用 transform 計算標準化分數
customer_stats['spent_zscore'] = (
    (customer_stats['total_spent'] - customer_stats['total_spent'].mean()) /
    customer_stats['total_spent'].std()
)

# 5. 計算綜合評分
customer_stats['value_score'] = (
    customer_stats['percentile_spent'] * 0.6 +
    customer_stats['percentile_count'] * 0.4
) * 100

# 6. 分級
customer_stats['tier'] = pd.cut(
    customer_stats['value_score'],
    bins=[0, 25, 50, 75, 100],
    labels=['Bronze', 'Silver', 'Gold', 'Platinum']
)

# 7. 合併回原始表並分析
result = customers.merge(customer_stats, on='customer_id')

print("頂級客戶分析:")
print(result.nlargest(20, 'value_score')[
    ['customer_id', 'customer_state', 'total_spent', 'value_score', 'tier']
])
```

---

## 學習檢查清單

- [ ] 理解 Transform 的核心特性（保持形狀、自動廣播）
- [ ] 掌握 Z-score 標準化的實現
- [ ] 能夠實現組內排名和百分位計算
- [ ] 掌握佔比和累計計算
- [ ] 了解 Transform vs agg vs apply 的區別
- [ ] 能夠應用 Transform 進行異常檢測
- [ ] 理解 Excel 廣播公式到 Python 的轉換
- [ ] 能夠建立多層級的相對分析

---

**建立時間**: 2025-12-11
**版本**: 1.0
**狀態**: 完整版
