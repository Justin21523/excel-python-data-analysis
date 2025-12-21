# Day 11: Named Aggregation 命名聚合與報表生成 (2.5-3 小時)

## 📚 目錄
1. [Named Aggregation 基礎](#named-aggregation-基礎)
2. [自訂聚合函數](#自訂聚合函數)
3. [建立完整報表](#建立完整報表)
4. [12 個實戰案例](#12-個實戰案例)
5. [Excel 對照教學](#excel-對照教學)

---

## Named Aggregation 基礎

### 1.1 什麼是 Named Aggregation？（30 分鐺）

Named Aggregation 是 Pandas 0.25.0+ 引入的功能，允許你以清晰的方式給聚合結果命名。

```python
import pandas as pd
from olist.datasets import load_datasets

# 加載數據
orders_df = load_datasets('orders')
order_items_df = load_datasets('order_items')
order_payments_df = load_datasets('order_payments')

# 準備測試數據
sales_data = pd.DataFrame({
    'region': ['East', 'East', 'East', 'West', 'West', 'West'],
    'quarter': ['Q1', 'Q1', 'Q2', 'Q1', 'Q1', 'Q2'],
    'sales': [100000, 120000, 150000, 80000, 95000, 110000]
})

print("原始數據:")
print(sales_data)

# ==== 老方法：不清晰的列名 ====
result_old = sales_data.groupby('region').agg({
    'sales': ['sum', 'mean', 'count']
})
print("\n老方法結果（列名不清晰）:")
print(result_old)
print(f"列名: {result_old.columns.tolist()}")

# ==== 新方法：Named Aggregation ====
result_new = sales_data.groupby('region').agg(
    total_sales=('sales', 'sum'),
    avg_sales=('sales', 'mean'),
    num_quarters=('sales', 'count')
)
print("\n新方法結果（列名清晰）:")
print(result_new)
print(f"列名: {result_new.columns.tolist()}")
```

**關鍵優點：**
1. 列名清晰可讀
2. 易於訪問（.total_sales 而非 .('sales', 'sum')）
3. 易於維護和理解

### 1.2 基本語法詳解（30 分鐺）

```python
# Named Aggregation 語法
df.groupby('grouping_column').agg(
    new_col_name=('source_column', 'function'),
    another_col=('source_column', 'different_function'),
    ...
)

# 實際例子：客戶訂單分析
customer_orders = order_payments_df.merge(
    orders_df[['order_id', 'customer_id']],
    on='order_id'
)

# 單個分組列
result1 = customer_orders.groupby('customer_id').agg(
    total_spent=('payment_value', 'sum'),
    avg_order_value=('payment_value', 'mean'),
    order_count=('payment_value', 'count')
).head(10)

print("單分組結果:")
print(result1)

# 多個分組列
orders_with_customer = orders_df.merge(
    customers_df[['customer_id', 'customer_state']],
    on='customer_id'
)

result2 = orders_with_customer.groupby(['customer_state', 'order_status']).agg(
    num_orders=('order_id', 'count'),
    avg_approval_time=('order_approved_at', lambda x: (x - orders_df['order_purchase_timestamp']).dt.total_seconds().mean())
).head(10)

print("\n多分組結果:")
print(result2)
```

### 1.3 使用多個函數於同一列（20 分鐺）

```python
# 同一列應用多個函數，需要分別命名

order_stats = order_items_df.groupby('order_id').agg(
    total_items=('product_id', 'count'),
    total_price=('price', 'sum'),
    avg_price=('price', 'mean'),
    max_price=('price', 'max'),
    min_price=('price', 'min'),
    price_std=('price', 'std')
)

print("訂單統計:")
print(order_stats.head(10))

# 不能這樣做（會報錯）❌
# result = df.groupby('col').agg(
#     sum=('value', 'sum'),
#     sum_again=('value', 'sum')  # 重複列名
# )

# 正確方法：使用不同的列名
result = order_items_df.groupby('product_id').agg(
    items_sold=('product_id', 'count'),
    total_revenue=('price', 'sum'),
    items_in_stock_count=('product_id', 'nunique')  # 假如有庫存信息
)

print("\n產品統計:")
print(result.head())
```

### 1.4 與不同列組合（20 分鐺）

```python
# Named Aggregation 支持多個不同來源的列

complete_stats = order_items_df.merge(
    order_payments_df,
    left_on='order_id',
    right_on='order_id'
).groupby('seller_id').agg(
    # 來自 order_items
    num_products_sold=('product_id', 'count'),
    avg_product_price=('price', 'mean'),

    # 來自 order_payments
    total_payment=('payment_value', 'sum'),
    avg_payment=('payment_value', 'mean'),

    # 計算計數（使用 nunique）
    unique_buyers=('order_id', 'nunique')
)

print("賣家綜合統計:")
print(complete_stats.head())
```

---

## 自訂聚合函數

### 2.1 定義自訂聚合函數（30 分鐺）

```python
import numpy as np

# 定義自訂聚合函數

# 1. 簡單的自訂函數
def calculate_median(series):
    """計算中位數"""
    return series.median()

# 2. 帶參數的自訂函數（需要用 lambda）
def percentile_25(series):
    """計算 25 百分位"""
    return series.quantile(0.25)

def percentile_75(series):
    """計算 75 百分位"""
    return series.quantile(0.75)

# 3. 更複雜的自訂函數
def coefficient_of_variation(series):
    """變異係數：標準差 / 平均值，表示相對波動性"""
    return series.std() / series.mean() if series.mean() != 0 else 0

def value_range(series):
    """數據範圍：最大值 - 最小值"""
    return series.max() - series.min()

# 4. 計數相關函數
def count_above_threshold(series, threshold=1000):
    """計算超過閾值的數量"""
    return (series > threshold).sum()

def count_below_threshold(series, threshold=1000):
    """計算低於閾值的數量"""
    return (series < threshold).sum()

# 應用自訂函數
sales_data = pd.DataFrame({
    'region': ['East'] * 10 + ['West'] * 10,
    'monthly_sales': np.random.uniform(500, 3000, 20)
})

result = sales_data.groupby('region').agg(
    total_sales=('monthly_sales', 'sum'),
    avg_sales=('monthly_sales', 'mean'),
    median_sales=('monthly_sales', calculate_median),
    p25_sales=('monthly_sales', percentile_25),
    p75_sales=('monthly_sales', percentile_75),
    sales_variation=('monthly_sales', coefficient_of_variation),
    sales_range=('monthly_sales', value_range)
)

print("自訂函數聚合結果:")
print(result)
```

### 2.2 帶參數的聚合函數（30 分鐺）

```python
# 使用 lambda 或 partial 傳遞參數

from functools import partial

# 方法1：使用 lambda
result_lambda = sales_data.groupby('region')['monthly_sales'].agg(
    count_high=lambda x: (x > 2000).sum(),
    count_low=lambda x: (x < 1000).sum(),
    pct_high=lambda x: (x > 2000).sum() / len(x) * 100
)

print("使用 Lambda 的結果:")
print(result_lambda)

# 方法2：使用 partial（適合參數多的情況）
count_above_1500 = partial(count_above_threshold, threshold=1500)
count_below_1500 = partial(count_above_threshold, threshold=1500)

result_partial = sales_data.groupby('region')['monthly_sales'].agg(
    high_count=count_above_1500,
    low_count=count_below_1500
)

print("\n使用 Partial 的結果:")
print(result_partial)
```

### 2.3 複雜聚合函數：加權平均（30 分鐺）

```python
# 加權平均是常見的自訂聚合場景

# 場景 1：加權平均評分
product_ratings = pd.DataFrame({
    'category': ['Electronics'] * 3 + ['Books'] * 3,
    'product_name': ['Phone', 'Laptop', 'Tablet', 'Python', 'Data', 'Novel'],
    'rating': [4.5, 4.8, 4.2, 4.9, 4.7, 4.3],
    'num_reviews': [1000, 500, 300, 100, 150, 2000]
})

print("產品評分數據:")
print(product_ratings)

def weighted_average(values, weights):
    """計算加權平均"""
    return (values * weights).sum() / weights.sum()

# 無法直接在 agg 中使用帶兩個參數的函數
# 需要使用 apply 或 groupby().apply()

category_ratings = product_ratings.groupby('category').apply(
    lambda x: pd.Series({
        'avg_rating': weighted_average(x['rating'], x['num_reviews']),
        'total_reviews': x['num_reviews'].sum(),
        'products': x['product_name'].count()
    })
)

print("\n類別加權評分:")
print(category_ratings)

# 場景 2：加權平均成本
inventory = pd.DataFrame({
    'department': ['Sales'] * 4 + ['Marketing'] * 3,
    'item': ['Item1', 'Item2', 'Item3', 'Item4', 'Item5', 'Item6', 'Item7'],
    'unit_cost': [100, 200, 150, 300, 50, 75, 120],
    'quantity_in_stock': [50, 30, 20, 10, 100, 80, 60]
})

dept_weighted_cost = inventory.groupby('department').apply(
    lambda x: pd.Series({
        'avg_unit_cost': weighted_average(x['unit_cost'], x['quantity_in_stock']),
        'total_value': (x['unit_cost'] * x['quantity_in_stock']).sum(),
        'num_items': len(x)
    })
)

print("\n部門加權平均成本:")
print(dept_weighted_cost)
```

---

## 建立完整報表

### 3.1 多層次聚合報表（40 分鐺）

```python
# 加載完整數據
orders_df = load_datasets('orders')
order_items_df = load_datasets('order_items')
order_payments_df = load_datasets('order_payments')
customers_df = load_datasets('customers')
sellers_df = load_datasets('sellers')

# 階段 1：構建基礎數據
order_complete = order_items_df.merge(
    orders_df[['order_id', 'customer_id', 'order_purchase_timestamp', 'order_status']],
    on='order_id'
).merge(
    order_payments_df.groupby('order_id')['payment_value'].sum().reset_index(),
    on='order_id'
).merge(
    sellers_df[['seller_id', 'seller_state']],
    on='seller_id'
)

print("合併後的數據樣本:")
print(order_complete.head())

# 階段 2：多層次聚合

# 層級1：賣家聚合
seller_report = order_complete.groupby('seller_id').agg(
    seller_state=('seller_state', 'first'),
    total_orders=('order_id', 'nunique'),
    total_revenue=('payment_value', 'sum'),
    avg_order_value=('payment_value', 'mean'),
    total_items_sold=('product_id', 'count'),
    avg_items_per_order=('product_id', 'mean'),
    num_customers=('customer_id', 'nunique')
).reset_index()

seller_report.columns = ['seller_id', 'state', 'orders', 'revenue', 'avg_value', 'items_sold', 'items_per_order', 'unique_customers']

print("\n賣家報表（前10）:")
print(seller_report.head(10))

# 層級2：地區聚合
state_report = order_complete.groupby('seller_state').agg(
    total_orders=('order_id', 'nunique'),
    total_revenue=('payment_value', 'sum'),
    avg_order_value=('payment_value', 'mean'),
    num_sellers=('seller_id', 'nunique'),
    num_customers=('customer_id', 'nunique'),
    avg_items_per_order=('product_id', 'mean')
).reset_index()

state_report.columns = ['state', 'orders', 'revenue', 'avg_value', 'sellers', 'customers', 'avg_items']

# 添加排名
state_report['rank'] = state_report['revenue'].rank(ascending=False).astype(int)

print("\n地區報表（按收入排序）:")
print(state_report.sort_values('revenue', ascending=False))

# 層級3：訂單狀態聚合
status_report = order_complete.groupby('order_status').agg(
    num_orders=('order_id', 'nunique'),
    total_revenue=('payment_value', 'sum'),
    avg_order_value=('payment_value', 'mean'),
    total_items=('product_id', 'count'),
    num_customers=('customer_id', 'nunique')
).reset_index()

print("\n訂單狀態報表:")
print(status_report)
```

### 3.2 格式化和導出報表（30 分鐺）

```python
# 美化報表輸出

# 添加百分比和格式化
seller_report['revenue_pct'] = (seller_report['revenue'] / seller_report['revenue'].sum() * 100).round(2)

# 添加績效指標
seller_report['revenue_per_seller'] = seller_report['revenue'] / seller_report['orders']
seller_report['customer_satisfaction_proxy'] = seller_report['unique_customers'] / seller_report['orders']

# 添加評級
def rate_seller(row):
    """評定賣家績效"""
    if row['revenue'] > state_report['revenue'].quantile(0.75):
        if row['customer_satisfaction_proxy'] > 1:  # 平均每個訂單超過1個客戶
            return '★★★'
        else:
            return '★★'
    else:
        return '★'

seller_report['performance'] = seller_report.apply(rate_seller, axis=1)

# 格式化輸出
print("\n格式化賣家報表:")
display_columns = ['seller_id', 'orders', 'revenue', 'revenue_pct', 'avg_value', 'performance']

# 使用 to_string 進行格式化
formatted_report = seller_report[display_columns].copy()
formatted_report['revenue'] = formatted_report['revenue'].apply(lambda x: f"${x:,.0f}")
formatted_report['avg_value'] = formatted_report['avg_value'].apply(lambda x: f"${x:,.2f}")
formatted_report['revenue_pct'] = formatted_report['revenue_pct'].apply(lambda x: f"{x:.1f}%")

print(formatted_report.head(15).to_string())

# 導出為 Excel（帶格式化）
# formatted_report.to_csv('seller_report.csv', index=False)
# 或者使用 openpyxl 進行更複雜的格式化
```

### 3.3 時間序列報表（30 分鐺）

```python
# 按時間分組的聚合報表

# 提取月份
order_complete['month'] = order_complete['order_purchase_timestamp'].dt.to_period('M')

# 月度聚合
monthly_report = order_complete.groupby('month').agg(
    total_orders=('order_id', 'nunique'),
    total_revenue=('payment_value', 'sum'),
    avg_order_value=('payment_value', 'mean'),
    num_sellers=('seller_id', 'nunique'),
    num_customers=('customer_id', 'nunique'),
    avg_items_per_order=('product_id', 'mean')
).reset_index()

monthly_report.columns = ['month', 'orders', 'revenue', 'avg_value', 'sellers', 'customers', 'items_per_order']

# 計算月度增長率
monthly_report['revenue_change'] = monthly_report['revenue'].pct_change() * 100
monthly_report['orders_change'] = monthly_report['orders'].pct_change() * 100

print("月度報表:")
print(monthly_report)

# 月份內的賣家排名
top_sellers_by_month = order_complete.groupby(['month', 'seller_id']).agg(
    monthly_revenue=('payment_value', 'sum'),
    monthly_orders=('order_id', 'nunique')
).reset_index()

top_sellers_by_month['rank'] = top_sellers_by_month.groupby('month')['monthly_revenue'].rank(ascending=False)

print("\n月度Top 5賣家:")
top_5 = top_sellers_by_month[top_sellers_by_month['rank'] <= 5]
print(top_5.sort_values(['month', 'rank']))
```

---

## 12 個實戰案例

### 案例 1-4: 基礎報表生成

**案例1: 簡單的部門總結**
```python
# 員工績效總結

employee_data = pd.DataFrame({
    'department': ['Sales', 'Sales', 'Sales', 'Marketing', 'Marketing', 'Marketing', 'Tech', 'Tech'],
    'employee': ['Alice', 'Bob', 'Charlie', 'Diana', 'Eve', 'Frank', 'George', 'Hannah'],
    'salary': [50000, 55000, 60000, 48000, 52000, 45000, 70000, 72000],
    'performance_score': [8.5, 8.0, 9.0, 7.5, 8.2, 7.8, 9.5, 8.8]
})

dept_summary = employee_data.groupby('department').agg(
    num_employees=('employee', 'count'),
    total_payroll=('salary', 'sum'),
    avg_salary=('salary', 'mean'),
    median_salary=('salary', 'median'),
    avg_performance=('performance_score', 'mean')
)

print("部門薪酬與績效總結:")
print(dept_summary)
```

**案例2: 客戶消費級別分析**
```python
# 根據消費額分級的客戶報表

customer_spending = order_payments_df.merge(
    orders_df[['order_id', 'customer_id']],
    on='order_id'
)

customer_summary = customer_spending.groupby('customer_id').agg(
    total_spent=('payment_value', 'sum'),
    num_orders=('order_id', 'nunique'),
    avg_order_value=('payment_value', 'mean')
).reset_index()

# 分級
customer_summary['segment'] = pd.cut(
    customer_summary['total_spent'],
    bins=[0, 1000, 5000, 10000, float('inf')],
    labels=['Small', 'Medium', 'Large', 'VIP']
)

segment_summary = customer_summary.groupby('segment').agg(
    num_customers=('customer_id', 'count'),
    total_revenue=('total_spent', 'sum'),
    avg_customer_value=('total_spent', 'mean'),
    avg_orders_per_customer=('num_orders', 'mean'),
    avg_order_value=('avg_order_value', 'mean')
)

print("客戶分群報表:")
print(segment_summary)
```

**案例3: 產品類別績效**
```python
# 產品類別銷售分析

product_categories = load_datasets('product_categories')
products = load_datasets('products')

category_sales = order_items_df.merge(
    products[['product_id', 'product_category_id', 'price']],
    on='product_id'
).merge(
    product_categories[['product_category_id', 'product_category_name']],
    on='product_category_id'
)

category_report = category_sales.groupby('product_category_name').agg(
    total_items_sold=('product_id', 'count'),
    total_revenue=('price', 'sum'),
    avg_price=('price', 'mean'),
    num_unique_products=('product_id', 'nunique'),
    num_transactions=('order_id', 'nunique')
).reset_index()

category_report.columns = ['category', 'items_sold', 'revenue', 'avg_price', 'products', 'transactions']

# 添加排名
category_report['rank'] = category_report['revenue'].rank(ascending=False).astype(int)

print("產品類別績效（Top 20）:")
print(category_report.nlargest(20, 'revenue')[['rank', 'category', 'revenue', 'items_sold']])
```

**案例4: 地理位置分析**
```python
# 按地區統計客戶和銷售

geo_data = orders_df.merge(
    customers_df[['customer_id', 'customer_state']],
    on='customer_id'
).merge(
    order_items_df[['order_id', 'price']],
    on='order_id'
)

state_report = geo_data.groupby('customer_state').agg(
    num_customers=('customer_id', 'nunique'),
    num_orders=('order_id', 'nunique'),
    total_revenue=('price', 'sum'),
    avg_order_value=('price', 'mean'),
    orders_per_customer=('order_id', lambda x: x.nunique() / x.nunique())
).reset_index()

state_report['revenue_rank'] = state_report['total_revenue'].rank(ascending=False).astype(int)

print("地區銷售報表（按收入排序）:")
print(state_report.sort_values('total_revenue', ascending=False).head(15))
```

### 案例 5-8: 進階報表

**案例5: RFM 分析與分段**
```python
# 完整的 RFM 分析報表

from datetime import datetime, timedelta

reference_date = orders_df['order_purchase_timestamp'].max()

rfm_analysis = order_payments_df.merge(
    orders_df[['order_id', 'customer_id', 'order_purchase_timestamp']],
    on='order_id'
).groupby('customer_id').agg(
    recency=('order_purchase_timestamp', lambda x: (reference_date - x.max()).days),
    frequency=('order_id', 'nunique'),
    monetary=('payment_value', 'sum')
).reset_index()

# 五分位分級
rfm_analysis['R_score'] = pd.qcut(rfm_analysis['recency'], 5, labels=[5,4,3,2,1], duplicates='drop')
rfm_analysis['F_score'] = pd.qcut(rfm_analysis['frequency'].rank(method='first'), 5, labels=[1,2,3,4,5], duplicates='drop')
rfm_analysis['M_score'] = pd.qcut(rfm_analysis['monetary'].rank(method='first'), 5, labels=[1,2,3,4,5], duplicates='drop')

# 分級
def assign_segment(row):
    r, f, m = int(row['R_score']), int(row['F_score']), int(row['M_score'])
    if r >= 4 and f >= 4 and m >= 4:
        return 'Champions'
    elif f >= 4 and m >= 3:
        return 'Loyal Customers'
    elif r <= 2:
        return 'At Risk'
    elif f <= 2:
        return 'Need Attention'
    else:
        return 'Potential'

rfm_analysis['segment'] = rfm_analysis.apply(assign_segment, axis=1)

# 生成報表
rfm_report = rfm_analysis.groupby('segment').agg(
    num_customers=('customer_id', 'count'),
    avg_recency=('recency', 'mean'),
    avg_frequency=('frequency', 'mean'),
    avg_monetary=('monetary', 'mean'),
    total_value=('monetary', 'sum')
).reset_index()

print("RFM 分段報表:")
print(rfm_report)
```

**案例6: 時間序列與趨勢**
```python
# 季度銷售趨勢

order_complete['quarter'] = order_complete['order_purchase_timestamp'].dt.to_period('Q')

quarterly_report = order_complete.groupby('quarter').agg(
    total_orders=('order_id', 'nunique'),
    total_revenue=('payment_value', 'sum'),
    avg_order_value=('payment_value', 'mean'),
    num_sellers=('seller_id', 'nunique'),
    num_customers=('customer_id', 'nunique')
).reset_index()

quarterly_report['yoy_growth'] = quarterly_report['total_revenue'].pct_change(4) * 100
quarterly_report['qoq_growth'] = quarterly_report['total_revenue'].pct_change() * 100

print("季度銷售趨勢:")
print(quarterly_report)
```

**案例7: 交叉表報表（樞紐表風格）**
```python
# 生成交叉表格式的報表

order_complete['quarter'] = order_complete['order_purchase_timestamp'].dt.to_period('Q')

# 按地區和季度統計
pivot_report = order_complete.pivot_table(
    values='payment_value',
    index='seller_state',
    columns='quarter',
    aggfunc='sum'
)

print("地區季度銷售表（樞紐風格）:")
print(pivot_report)

# 添加合計
pivot_report['Total'] = pivot_report.sum(axis=1)
pivot_report.loc['Total'] = pivot_report.sum()

print("\n帶合計的樞紐表:")
print(pivot_report)
```

**案例8: 客戶生命週期價值 (CLV) 報表**
```python
# 計算客戶生命週期價值

customer_clv = order_complete.groupby('customer_id').agg(
    first_purchase=('order_purchase_timestamp', 'min'),
    last_purchase=('order_purchase_timestamp', 'max'),
    total_spent=('payment_value', 'sum'),
    num_orders=('order_id', 'nunique'),
    num_items=('product_id', 'count')
).reset_index()

customer_clv['customer_lifetime_days'] = (customer_clv['last_purchase'] - customer_clv['first_purchase']).dt.days
customer_clv['avg_daily_value'] = customer_clv['total_spent'] / (customer_clv['customer_lifetime_days'] + 1)

# 估計 CLV（假設客戶保留 2 年）
customer_clv['estimated_2yr_clv'] = customer_clv['avg_daily_value'] * 730

# 分級
customer_clv['clv_tier'] = pd.qcut(
    customer_clv['estimated_2yr_clv'],
    q=4,
    labels=['Tier D', 'Tier C', 'Tier B', 'Tier A']
)

clv_report = customer_clv.groupby('clv_tier').agg(
    num_customers=('customer_id', 'count'),
    avg_spent=('total_spent', 'mean'),
    avg_orders=('num_orders', 'mean'),
    avg_lifetime_days=('customer_lifetime_days', 'mean'),
    avg_2yr_clv=('estimated_2yr_clv', 'mean'),
    total_tier_value=('estimated_2yr_clv', 'sum')
)

print("客戶生命週期價值報表:")
print(clv_report)
```

### 案例 9-12: 複雜業務報表

**案例9: 賣家績效計分卡**
```python
# 綜合賣家績效的計分卡

seller_performance = order_complete.groupby('seller_id').agg(
    total_revenue=('payment_value', 'sum'),
    total_orders=('order_id', 'nunique'),
    unique_customers=('customer_id', 'nunique'),
    avg_order_value=('payment_value', 'mean'),
    total_items=('product_id', 'count'),
    avg_items_per_order=('product_id', 'mean')
).reset_index()

# 計算評分（每項都轉換為 0-100）
seller_performance['revenue_score'] = (
    seller_performance['total_revenue'] / seller_performance['total_revenue'].max() * 100
)
seller_performance['frequency_score'] = (
    seller_performance['total_orders'] / seller_performance['total_orders'].max() * 100
)
seller_performance['customer_score'] = (
    seller_performance['unique_customers'] / seller_performance['unique_customers'].max() * 100
)
seller_performance['avg_order_score'] = (
    seller_performance['avg_order_value'] / seller_performance['avg_order_value'].max() * 100
)

# 加權綜合分數
seller_performance['composite_score'] = (
    seller_performance['revenue_score'] * 0.4 +
    seller_performance['frequency_score'] * 0.3 +
    seller_performance['customer_score'] * 0.2 +
    seller_performance['avg_order_score'] * 0.1
)

# 評級
seller_performance['rating'] = pd.cut(
    seller_performance['composite_score'],
    bins=[0, 20, 40, 60, 80, 100],
    labels=['F', 'D', 'C', 'B', 'A']
)

print("賣家績效計分卡（Top 20）:")
print(seller_performance.nlargest(20, 'composite_score')[
    ['seller_id', 'total_revenue', 'composite_score', 'rating']
])
```

**案例10: 產品品質與銷售報告**
```python
# 結合評論評分和銷售的產品報表

product_performance = order_items_df.groupby('product_id').agg(
    total_sold=('product_id', 'count'),
    total_revenue=('price', 'sum'),
    avg_price=('price', 'mean'),
    num_orders=('order_id', 'nunique')
).reset_index()

product_performance['revenue_rank'] = product_performance['total_revenue'].rank(ascending=False).astype(int)
product_performance['avg_revenue_per_order'] = product_performance['total_revenue'] / product_performance['num_orders']

# 判斷星級（基於銷量）
product_performance['sales_tier'] = pd.qcut(
    product_performance['total_sold'],
    q=5,
    labels=['Emerging', 'Growing', 'Popular', 'Best Seller', 'Top Seller'],
    duplicates='drop'
)

print("產品銷售績效（Top 15 Best Sellers）:")
print(product_performance[product_performance['revenue_rank'] <= 15][
    ['product_id', 'total_sold', 'total_revenue', 'sales_tier']
])
```

**案例11: 訂單狀態與客戶滿意度報告**
```python
# 分析訂單狀態對客戶重複購買的影響

order_status_analysis = order_complete.groupby(['customer_id', 'order_status']).agg(
    num_orders=('order_id', 'nunique'),
    total_spent=('payment_value', 'sum')
).reset_index()

# 計算各狀態客戶的重複購買率
customer_repeat = order_complete.groupby('customer_id')['order_id'].nunique().reset_index()
customer_repeat.columns = ['customer_id', 'total_orders']

# 只有交付的訂單
delivered_customers = order_complete[order_complete['order_status'] == 'delivered'].groupby('customer_id').agg(
    delivered_orders=('order_id', 'nunique')
).reset_index()

merge_data = customer_repeat.merge(delivered_customers, on='customer_id', how='left').fillna(0)
merge_data['repeat_rate'] = merge_data['delivered_orders'] / merge_data['total_orders'] * 100

status_report = order_complete.groupby('order_status').agg(
    num_orders=('order_id', 'nunique'),
    num_customers=('customer_id', 'nunique'),
    total_value=('payment_value', 'sum'),
    avg_order_value=('payment_value', 'mean')
).reset_index()

status_report['orders_per_customer'] = status_report['num_orders'] / status_report['num_customers']

print("訂單狀態分析報告:")
print(status_report)
```

**案例12: 完整的組織績效儀表板**
```python
# 多維度的完整績效儀表板

dashboard_data = {
    '總體指標': {
        '總訂單數': order_complete['order_id'].nunique(),
        '總收入': order_complete['payment_value'].sum(),
        '活躍客戶': order_complete['customer_id'].nunique(),
        '活躍賣家': order_complete['seller_id'].nunique()
    },
    '平均指標': {
        '平均訂單價值': order_complete['payment_value'].mean(),
        '平均每單商品數': order_complete.groupby('order_id')['product_id'].count().mean(),
        '客戶復購率': order_complete.groupby('customer_id')['order_id'].nunique().mean()
    },
    '地區Top 3': order_complete.groupby('seller_state')['payment_value'].sum().nlargest(3).to_dict(),
    '狀態分佈': order_complete['order_status'].value_counts().to_dict()
}

print("績效儀表板:")
for section, metrics in dashboard_data.items():
    print(f"\n{section}:")
    if isinstance(metrics, dict):
        for key, value in metrics.items():
            if isinstance(value, float):
                print(f"  {key}: {value:,.2f}")
            else:
                print(f"  {key}: {value}")
```

---

## Excel 對照教學

### 從 Excel 樞紐表到 Python Named Agg

#### 對照1: 簡單求和

**Excel 樞紐表:**
```
行：城市
值：銷售額（求和）
```

**Python Named Agg:**
```python
df.groupby('city').agg(
    total_sales=('sales', 'sum')
)
```

#### 對照2: 多個指標

**Excel 樞紐表:**
```
行：產品
值：銷售額（求和）、銷量（計數）、平均價格（平均）
```

**Python Named Agg:**
```python
df.groupby('product').agg(
    total_sales=('sales', 'sum'),
    sales_count=('sales', 'count'),
    avg_price=('price', 'mean')
)
```

#### 對照3: 多層分組

**Excel 樞紐表:**
```
行：地區、城市
值：銷售額
```

**Python Named Agg:**
```python
df.groupby(['region', 'city']).agg(
    total_sales=('sales', 'sum')
)
```

---

## 效能提示

### 聚合函數效能對比

```python
import time
import numpy as np

# 準備大數據集
n = 1000000
test_data = pd.DataFrame({
    'group': np.random.choice(['A', 'B', 'C', 'D', 'E'], n),
    'value': np.random.randn(n),
    'amount': np.random.uniform(0, 1000, n)
})

# 測試1: Named Agg vs 傳統 agg
start = time.time()
result1 = test_data.groupby('group').agg(
    total=('amount', 'sum'),
    mean=('amount', 'mean')
)
named_time = time.time() - start

start = time.time()
result2 = test_data.groupby('group')[['amount']].agg(['sum', 'mean'])
traditional_time = time.time() - start

print(f"Named Agg: {named_time:.4f}s")
print(f"Traditional: {traditional_time:.4f}s")
```

---

## 學習檢查清單

- [ ] 理解 Named Aggregation 的基本語法
- [ ] 能夠使用多個函數於同一列
- [ ] 掌握自訂聚合函數的實現
- [ ] 理解加權平均的應用
- [ ] 能夠生成多層次聚合報表
- [ ] 掌握時間序列報表生成
- [ ] 理解 Excel 樞紐表到 Python 的轉換
- [ ] 能夠建立完整的業務報表

---

**建立時間**: 2025-12-11
**版本**: 1.0
**狀態**: 完整版
