# Day 02: GroupBy 進階聚合 - 完全掌握分組運算

## 課程目錄
- [Part 1: GroupBy 基礎回顧（1h）](#part-1-groupby-基礎回顧)
- [Part 2: 命名聚合（Named Aggregation）（2h）](#part-2-命名聚合named-aggregation2h)
- [Part 3: Transform vs Aggregate vs Filter（2h）](#part-3-transform-vs-aggregate-vs-filter2h)
- [Part 4: 綜合實戰練習（3h）](#part-4-綜合實戰練習3h)
- [學習資源與相關文件](#學習資源與相關文件)

---

## Part 1: GroupBy 基礎回顧

### 1.1 GroupBy 機制詳解

**Excel 類比：**
- Excel 中的「小計」功能
- 樞紐分析表的列/欄分組
- SUMIF、AVERAGEIF 等條件聚合函數

**pandas GroupBy 三步驟：Split-Apply-Combine**

```python
import pandas as pd
import numpy as np
from datetime import datetime, timedelta

# 載入 Olist 資料
from utils.data_loader import OlistDataLoader
loader = OlistDataLoader()
orders = loader.get_orders()
items = loader.get_order_items()
customers = loader.get_customers()
products = loader.get_products()

# 合併資料
order_data = orders.merge(items, on='order_id')
order_data = order_data.merge(customers, on='customer_id')
order_data = order_data.merge(products, on='product_id', how='left')

print("資料維度:", order_data.shape)
print("\n主要欄位:", order_data.columns.tolist())
print("\n前五筆資料:")
print(order_data.head())
```

### 1.2 單欄分組 vs 多欄分組

#### 案例 1: 單欄位分組 - 州別銷售額

```python
# Excel: 依州別建立樞紐分析表，計算總銷售額
# pandas: groupby('州別') + sum()

# 方法 1: 直接聚合單個函數
state_sales = order_data.groupby('customer_state')['price'].sum().sort_values(ascending=False)
print("各州銷售額 (Top 10):")
print(state_sales.head(10))

# 方法 2: 使用 agg() 方法多個函數
state_stats = order_data.groupby('customer_state')['price'].agg([
    'sum',      # 總銷售額
    'mean',     # 平均客單價
    'count',    # 訂單數
    'max',      # 最高單價
    'min'       # 最低單價
]).round(2)

# 重新命名欄位
state_stats.columns = ['總銷售額', '平均客單價', '訂單數', '最高單價', '最低單價']
state_stats = state_stats.sort_values('總銷售額', ascending=False)

print("\n各州銷售統計 (Top 10):")
print(state_stats.head(10))
```

**Excel 對照：**
```
Excel 樞紐分析表:
列欄位: customer_state
值欄位: 加總 price, 平均 price, 計數, 最大值 price, 最小值 price

SUMIF(customer_state, state, price)      # 計算州別銷售額
AVERAGEIF(customer_state, state, price)  # 計算州別平均
COUNTIF(customer_state, state)           # 計算州別訂單數
```

#### 案例 2: 多欄位分組 - 州市組合分析

```python
# Excel: 多層樞紐分析表 (州 + 城市)
# pandas: groupby(['州', '城市'])

# 州 + 城市分組
city_sales = order_data.groupby(['customer_state', 'customer_city'])['price'].agg([
    ('銷售額', 'sum'),
    ('訂單數', 'count'),
    ('平均客單價', 'mean')
]).reset_index().round(2)

# 排序並顯示
city_sales = city_sales.sort_values('銷售額', ascending=False)
print("州/城市銷售統計 (Top 15):")
print(city_sales.head(15))

# 計算每個城市佔州的銷售比例
city_sales['州銷售額'] = city_sales.groupby('customer_state')['銷售額'].transform('sum')
city_sales['城市佔比(%)'] = (city_sales['銷售額'] / city_sales['州銷售額'] * 100).round(2)

print("\n帶佔比的銷售統計 (Top 10):")
print(city_sales[['customer_state', 'customer_city', '銷售額', '城市佔比(%)']].head(10))
```

#### 案例 3: 多欄位 + 多欄值 - 產品類別×支付方式

```python
# Excel: 三層樞紐分析表 (類別 + 支付方式)
# pandas: groupby 多欄位，agg 多個欄位

product_payment = order_data.groupby(['product_category_name', 'payment_type']).agg({
    'price': ['sum', 'count', 'mean'],
    'freight_value': 'mean'
}).round(2)

# 重新設置欄位名稱
product_payment.columns = ['銷售額', '訂單數', '平均客單價', '平均運費']
product_payment = product_payment.sort_values('銷售額', ascending=False)

print("產品類別×支付方式分析 (Top 20):")
print(product_payment.head(20))
```

### 1.3 基本聚合函數總結表

| 聚合函數 | 說明 | Excel 對照 | 用途 |
|---------|------|-----------|------|
| `sum()` | 求和 | SUM | 總銷售額、總數量 |
| `mean()` | 平均值 | AVERAGE | 客單價、平均評分 |
| `count()` | 計數 | COUNTA | 訂單數、樣本數 |
| `median()` | 中位數 | MEDIAN | 中位客單價 |
| `std()` | 標準差 | STDEV | 波動性分析 |
| `min()`/`max()` | 最小/最大 | MIN/MAX | 價格範圍 |
| `first()`/`last()` | 首末值 | - | 時間序列首末 |
| `size()` | 組大小 | COUNTIF | 每組樣本數 |

---

## Part 2: 命名聚合(Named Aggregation)(2h)

### 2.1 命名聚合的優勢

傳統 agg() 方法的問題：

```python
# 傳統方法（易產生混淆）
result = order_data.groupby('customer_state')['price'].agg([
    'sum', 'mean', 'count'
])
# 結果欄位名為: sum, mean, count （不清楚）

# 或者需要重新命名
result.columns = ['總銷售額', '平均客單價', '訂單數']
```

命名聚合（Named Aggregation）的優勢：

```python
# 命名聚合方法（清晰易讀）
result = order_data.groupby('customer_state')['price'].agg(
    總銷售額=('price', 'sum'),
    平均客單價=('price', 'mean'),
    訂單數=('price', 'count')
).round(2)
```

### 2.2 命名聚合語法與應用

#### 案例 4: 產品類別銷售分析

```python
# 計算各產品類別的關鍵 KPI
product_analysis = order_data.groupby('product_category_name').agg(
    # 銷售相關
    總銷售額=('price', 'sum'),
    平均客單價=('price', 'mean'),
    訂單數=('order_id', 'count'),

    # 運費相關
    平均運費=('freight_value', 'mean'),
    總運費=('freight_value', 'sum'),

    # 其他指標
    客戶數=('customer_id', 'nunique'),
    平均評分=('review_score', 'mean')
).round(2)

product_analysis = product_analysis.sort_values('總銷售額', ascending=False)
print("產品類別銷售分析 (Top 15):")
print(product_analysis.head(15))

# 計算派生指標
product_analysis['平均運費率(%)'] = (
    product_analysis['平均運費'] / product_analysis['平均客單價'] * 100
).round(2)
product_analysis['人均購買次數'] = (
    product_analysis['訂單數'] / product_analysis['客戶數']
).round(2)

print("\n帶派生指標的分析結果:")
print(product_analysis[['訂單數', '客戶數', '人均購買次數', '平均運費率(%)']].head(10))
```

#### 案例 5: 支付方式分析

```python
# 各支付方式的效果分析
payment_analysis = order_data.groupby('payment_type').agg(
    交易額=('price', 'sum'),
    交易數=('order_id', 'count'),
    人均客單價=('price', 'mean'),
    客戶數=('customer_id', 'nunique'),
    平均評分=('review_score', 'mean'),
    及時交付率=('order_status', lambda x: (x == 'delivered').mean() * 100)
).round(2)

payment_analysis = payment_analysis.sort_values('交易額', ascending=False)
print("支付方式效果分析:")
print(payment_analysis)

# 計算支付方式分佈
payment_analysis['銷售額占比(%)'] = (
    payment_analysis['交易額'] / payment_analysis['交易額'].sum() * 100
).round(2)
```

#### 案例 6: 客戶分群分析

```python
# 客戶分群：按客戶總購買額分組
# 首先計算每個客戶的購買情況
customer_value = order_data.groupby('customer_id').agg(
    客戶州別=('customer_state', 'first'),
    購買次數=('order_id', 'count'),
    總購買額=('price', 'sum'),
    平均客單價=('price', 'mean'),
    購買日期數=('order_purchase_timestamp', 'nunique')
).reset_index()

# 定義客戶分群
def segment_customer(total_value):
    if total_value >= 1000:
        return 'VIP'
    elif total_value >= 500:
        return '高價值'
    elif total_value >= 100:
        return '中價值'
    else:
        return '低價值'

customer_value['客戶分群'] = customer_value['總購買額'].apply(segment_customer)

# 分群統計
segment_analysis = customer_value.groupby('客戶分群').agg(
    客戶數=('customer_id', 'count'),
    平均購買額=('總購買額', 'mean'),
    平均購買次數=('購買次數', 'mean'),
    總銷售額=('總購買額', 'sum'),
    平均客單價=('平均客單價', 'mean')
).round(2)

# 計算占比
segment_analysis['銷售額占比(%)'] = (
    segment_analysis['總銷售額'] / segment_analysis['總銷售額'].sum() * 100
).round(2)

print("客戶分群分析:")
print(segment_analysis)
```

#### 案例 7: 時間維度分析

```python
# 轉換時間戳為日期
order_data['order_date'] = pd.to_datetime(order_data['order_purchase_timestamp']).dt.date
order_data['order_year_month'] = pd.to_datetime(order_data['order_purchase_timestamp']).dt.to_period('M')

# 月度銷售分析
monthly_analysis = order_data.groupby('order_year_month').agg(
    月度銷售額=('price', 'sum'),
    月度訂單數=('order_id', 'count'),
    月度客戶數=('customer_id', 'nunique'),
    月度平均客單價=('price', 'mean'),
    月度平均運費=('freight_value', 'mean')
).round(2)

# 計算環比增長
monthly_analysis['銷售額環比增長(%)'] = (
    monthly_analysis['月度銷售額'].pct_change() * 100
).round(2)

print("月度銷售分析 (Last 12 months):")
print(monthly_analysis.tail(12))
```

#### 案例 8: 多維度綜合分析

```python
# 州別 × 產品類別 的複合分析
state_product = order_data.groupby(['customer_state', 'product_category_name']).agg(
    銷售額=('price', 'sum'),
    訂單數=('order_id', 'count'),
    客戶數=('customer_id', 'nunique'),
    平均客單價=('price', 'mean'),
    平均評分=('review_score', 'mean')
).round(2)

state_product = state_product.reset_index()
state_product = state_product.sort_values('銷售額', ascending=False)

print("州別×產品類別分析 (Top 20):")
print(state_product.head(20))

# 計算各州的主要產品類別（貢獻度超過 20%）
for state in state_product['customer_state'].unique()[:5]:
    state_data = state_product[state_product['customer_state'] == state]
    state_total = state_data['銷售額'].sum()
    state_data['類別銷售占比(%)'] = (state_data['銷售額'] / state_total * 100).round(2)

    print(f"\n{state} 州的主要產品類別:")
    main_products = state_data[state_data['類別銷售占比(%)'] >= 15]
    print(main_products[['product_category_name', '銷售額', '類別銷售占比(%)']].head(5))
```

---

## Part 3: Transform vs Aggregate vs Filter(2h)

### 3.1 三者差異與應用場景

| 方法 | 形狀 | 用途 | 傳播值 |
|------|------|------|--------|
| `agg()` | 縮小 | 聚合計算，得到分組統計 | 否 |
| `transform()` | 保持 | 廣播計算，每行保留分組結果 | 是 |
| `filter()` | 縮小 | 篩選符合條件的組，保留原始行 | 否 |

### 3.2 Transform - 保留原始行數

#### 案例 9: 計算組內百分比排名

```python
# 場景：計算每個產品類別內的商品排名百分比

# 先計算每個產品的銷售額
product_sales = order_data.groupby('product_id').agg(
    銷售額=('price', 'sum'),
    product_category_name=('product_category_name', 'first')
).reset_index()

# 在每個類別內計算排名百分比
product_sales['類別內銷售排名'] = product_sales.groupby('product_category_name')['銷售額'].rank(method='min')
product_sales['類別內排名百分比'] = (
    product_sales.groupby('product_category_name')['銷售額'].rank(method='min', pct=True) * 100
).round(2)

print("產品銷售排名 (Top 20):")
print(product_sales.nlargest(20, '銷售額')[['product_id', 'product_category_name', '銷售額', '類別內排名百分比']])
```

**Excel 對照:**
```
Excel: 使用 RANK 或 PERCENTRANK 函數
=RANK(單元格, 範圍)
=PERCENTRANK(範圍, 單元格)

pandas: groupby().rank()
```

#### 案例 10: 計算組內標準化分數

```python
# 場景：計算每個客戶相對於同州客戶的購買力排名

customer_state_purchase = order_data.groupby('customer_id').agg(
    州別=('customer_state', 'first'),
    購買額=('price', 'sum'),
    購買次數=('order_id', 'count')
).reset_index()

# 方法 1: 使用 transform 計算組內統計
customer_state_purchase['州平均購買額'] = customer_state_purchase.groupby('州別')['購買額'].transform('mean')
customer_state_purchase['州標準差'] = customer_state_purchase.groupby('州別')['購買額'].transform('std')

# 計算 Z-score（標準化分數）
customer_state_purchase['購買力Z分數'] = (
    (customer_state_purchase['購買額'] - customer_state_purchase['州平均購買額'])
    / customer_state_purchase['州標準差']
).round(2)

print("客戶購買力排名 (Top 30):")
print(customer_state_purchase.nlargest(30, '購買力Z分數')[['customer_id', '州別', '購買額', '購買力Z分數']])

# 方法 2: 使用 transform 計算組內比例
customer_state_purchase['占州銷售比例(%)'] = (
    customer_state_purchase.groupby('州別')['購買額'].transform(lambda x: (x / x.sum() * 100))
).round(2)

print("\n購買力占州銷售比例 (Top 10):")
print(customer_state_purchase.nlargest(10, '占州銷售比例(%)')[['customer_id', '州別', '購買額', '占州銷售比例(%)']])
```

#### 案例 11: Transform 廣播聚合結果

```python
# 場景：每行標注其所屬類別的平均評分

# 直接在原始資料上加入組聚合結果
order_data['類別平均評分'] = order_data.groupby('product_category_name')['review_score'].transform('mean').round(2)
order_data['個品評分差異'] = (order_data['review_score'] - order_data['類別平均評分']).round(2)

print("個品評分與類別平均對比 (Top 30):")
print(order_data[['product_category_name', 'review_score', '類別平均評分', '個品評分差異']].drop_duplicates().head(30))

# 計算組內排名
order_data['類別內銷售排名'] = order_data.groupby('product_category_name')['price'].rank(method='min', ascending=False).astype(int)

print("\n包含排名的資料:")
print(order_data[['product_id', 'product_category_name', 'price', '類別內銷售排名']].drop_duplicates().head(20))
```

### 3.3 Filter - 組篩選

#### 案例 12: 篩選出熱銷產品

```python
# 場景：只保留銷售額超過各類別平均值的產品

product_category_avg = order_data.groupby('product_category_name')['price'].mean()

# 方法 1: filter() - 保留符合條件的組
hot_selling = order_data.groupby('product_category_name').filter(
    lambda x: x['price'].sum() > x['price'].sum().mean() * 1.5  # 超過平均值 1.5 倍
)

print(f"篩選前資料行數: {len(order_data)}")
print(f"篩選後資料行數: {len(hot_selling)}")
print(f"熱銷產品類別數: {hot_selling['product_category_name'].nunique()}")

# 方法 2: filter() 結合多條件
high_value_categories = order_data.groupby('product_category_name').filter(
    lambda x: (x['price'].sum() > 100000) & (x['review_score'].mean() >= 4.0)
)

print("\n高價值產品類別（銷售額>10w 且評分>=4）:")
print(high_value_categories['product_category_name'].unique()[:10])
```

#### 案例 13: 篩選出活躍客戶

```python
# 場景：篩選購買次數大於中位數的客戶

customer_purchase_count = order_data.groupby('customer_id').size()
median_purchase = customer_purchase_count.median()

# 使用 filter 篩選
active_customers = order_data.groupby('customer_id').filter(
    lambda x: len(x) > median_purchase
)

print(f"活躍客戶篩選結果:")
print(f"總客戶數: {order_data['customer_id'].nunique()}")
print(f"活躍客戶數: {active_customers['customer_id'].nunique()}")
print(f"活躍客戶的訂單數: {len(active_customers)}")

# 計算活躍客戶的 RFM 指標
active_customer_rfm = active_customers.groupby('customer_id').agg(
    R=('order_purchase_timestamp', lambda x: (pd.Timestamp.now() - pd.to_datetime(x).max()).days),
    F=('order_id', 'count'),
    M=('price', 'sum')
).round(2)

print("\n活躍客戶 RFM 分析:")
print(active_customer_rfm.describe())
```

#### 案例 14: 篩選出 Top 類別

```python
# 場景：只保留銷售額排名前 5 的產品類別的資料

# 方法 1: 使用 filter() 加 rank
top_categories = order_data.groupby('product_category_name').filter(
    lambda x: order_data.groupby('product_category_name')['price'].sum().rank(ascending=False).loc[x.name] <= 5
)

# 更簡潔的方法 2: 先計算，再篩選
top_category_names = order_data.groupby('product_category_name')['price'].sum().nlargest(5).index

top_categories_data = order_data[order_data['product_category_name'].isin(top_category_names)]

print(f"Top 5 產品類別的銷售資料:")
print(f"資料行數: {len(top_categories_data)}")
print(f"類別: {top_categories_data['product_category_name'].unique()}")

# 計算 Top 類別的詳細統計
top_category_stats = top_categories_data.groupby('product_category_name').agg(
    銷售額=('price', 'sum'),
    訂單數=('order_id', 'count'),
    平均客單價=('price', 'mean'),
    平均評分=('review_score', 'mean')
).round(2).sort_values('銷售額', ascending=False)

print("\nTop 5 產品類別統計:")
print(top_category_stats)
```

### 3.4 Transform vs Aggregate vs Filter 比較表

```python
# 演示三者的差異

# 原始資料
sample_data = order_data[['customer_state', 'price']].head(10)
print("原始資料:")
print(sample_data)

# Aggregate: 縮小成 1 行
agg_result = order_data.groupby('customer_state')['price'].agg(['sum', 'mean'])
print(f"\nAggregate 結果 (形狀: {agg_result.shape}):")
print(agg_result.head())

# Transform: 保持原始行數
transform_result = order_data.groupby('customer_state')['price'].transform('mean')
print(f"\nTransform 結果 (形狀: {transform_result.shape}):")
print(transform_result.head())

# Filter: 按條件篩選組
filter_result = order_data.groupby('customer_state').filter(lambda x: x['price'].sum() > 1000000)
print(f"\nFilter 結果 (形狀: {filter_result.shape}):")
print(filter_result.head())
```

---

## Part 4: 綜合實戰練習(3h)

### 練習 1: RFM 客戶價值分析

**目標：** 基於 Recency、Frequency、Monetary 三維度分析客戶價值

```python
from datetime import datetime, timedelta

# 計算 RFM 指標
latest_date = pd.to_datetime(order_data['order_purchase_timestamp']).max()

rfm_data = order_data.groupby('customer_id').agg(
    # R: Recency (最後購買距今天數)
    Recency=('order_purchase_timestamp', lambda x: (latest_date - pd.to_datetime(x).max()).days),
    # F: Frequency (購買次數)
    Frequency=('order_id', 'count'),
    # M: Monetary (購買總額)
    Monetary=('price', 'sum')
).reset_index()

print("RFM 基礎統計:")
print(rfm_data.describe())

# 定義 RFM 評分標準
# R: 最近性評分（越小越好）
rfm_data['R_Score'] = pd.qcut(rfm_data['Recency'], q=5, labels=[5, 4, 3, 2, 1], duplicates='drop')

# F: 頻次評分（越大越好）
rfm_data['F_Score'] = pd.qcut(rfm_data['Frequency'].rank(method='first'), q=5, labels=[1, 2, 3, 4, 5], duplicates='drop')

# M: 金額評分（越大越好）
rfm_data['M_Score'] = pd.qcut(rfm_data['Monetary'], q=5, labels=[1, 2, 3, 4, 5], duplicates='drop')

# 轉換為數值型
rfm_data[['R_Score', 'F_Score', 'M_Score']] = rfm_data[['R_Score', 'F_Score', 'M_Score']].astype(int)

# 計算綜合評分
rfm_data['RFM_Score'] = rfm_data['R_Score'] + rfm_data['F_Score'] + rfm_data['M_Score']

# 客戶分群
def rfm_segment(row):
    if row['RFM_Score'] >= 12:
        return '高價值客戶'
    elif row['RFM_Score'] >= 9:
        return '中價值客戶'
    elif row['RFM_Score'] >= 6:
        return '低價值客戶'
    else:
        return '流失客戶'

rfm_data['客戶分群'] = rfm_data.apply(rfm_segment, axis=1)

# 客戶分群統計
rfm_summary = rfm_data.groupby('客戶分群').agg(
    客戶數=('customer_id', 'count'),
    平均購買次數=('Frequency', 'mean'),
    平均購買額=('Monetary', 'mean'),
    總購買額=('Monetary', 'sum')
).round(2)

rfm_summary['銷售額占比(%)'] = (rfm_summary['總購買額'] / rfm_summary['總購買額'].sum() * 100).round(2)

print("\n客戶分群統計:")
print(rfm_summary)

# 詳細客戶列表
print("\n高價值客戶列表 (Top 20):")
high_value = rfm_data[rfm_data['客戶分群'] == '高價值客戶'].nlargest(20, 'Monetary')
print(high_value[['customer_id', 'Recency', 'Frequency', 'Monetary', 'RFM_Score']].head(20))
```

### 練習 2: 產品 ABC 分類

**目標：** 根據帕累托法則（80-20 原則）對產品進行分類

```python
# 計算每個產品的銷售貢獻度

product_contribution = order_data.groupby('product_id').agg(
    銷售額=('price', 'sum'),
    product_category_name=('product_category_name', 'first'),
    訂單數=('order_id', 'count'),
    平均評分=('review_score', 'mean')
).reset_index()

# 按銷售額排序
product_contribution = product_contribution.sort_values('銷售額', ascending=False)

# 計算累計銷售額和占比
product_contribution['累計銷售額'] = product_contribution['銷售額'].cumsum()
total_sales = product_contribution['銷售額'].sum()
product_contribution['累計銷售占比(%)'] = (product_contribution['累計銷售額'] / total_sales * 100).round(2)

# ABC 分類
def abc_classification(pct):
    if pct <= 80:
        return 'A'
    elif pct <= 95:
        return 'B'
    else:
        return 'C'

product_contribution['分類'] = product_contribution['累計銷售占比(%)'].apply(abc_classification)

# 分類統計
abc_summary = product_contribution.groupby('分類').agg(
    產品數=('product_id', 'count'),
    總銷售額=('銷售額', 'sum'),
    平均銷售額=('銷售額', 'mean'),
    總訂單數=('訂單數', 'sum')
).round(2)

abc_summary['銷售額占比(%)'] = (abc_summary['總銷售額'] / total_sales * 100).round(2)

print("產品 ABC 分類統計:")
print(abc_summary)

# 詳細列表
print("\nA 類產品（核心產品）Top 20:")
print(product_contribution[product_contribution['分類'] == 'A'][['product_id', 'product_category_name', '銷售額', '累計銷售占比(%)']].head(20))

print("\nB 類產品（重點產品）Top 10:")
print(product_contribution[product_contribution['分類'] == 'B'][['product_id', 'product_category_name', '銷售額', '累計銷售占比(%)']].head(10))
```

### 練習 3: 客戶分群報表

**目標：** 建立多維度客戶分群報表

```python
# 綜合客戶分群（結合地理位置、購買行為、評分等）

customer_profile = order_data.groupby('customer_id').agg(
    # 基本信息
    州別=('customer_state', 'first'),
    城市=('customer_city', 'first'),

    # 購買行為
    購買次數=('order_id', 'count'),
    總購買額=('price', 'sum'),
    平均客單價=('price', 'mean'),
    購買產品種類=('product_id', 'nunique'),
    購買類別數=('product_category_name', 'nunique'),

    # 評分情況
    平均評分=('review_score', 'mean'),
    低分訂單占比=('review_score', lambda x: (x <= 3).sum() / len(x) * 100),

    # 時間指標
    首次購買=('order_purchase_timestamp', 'min'),
    最後購買=('order_purchase_timestamp', 'max')
).reset_index()

# 計算額外指標
customer_profile['客戶生命週期天數'] = (
    pd.to_datetime(customer_profile['最後購買']) -
    pd.to_datetime(customer_profile['首次購買'])
).dt.days

customer_profile['客戶生命週期月數'] = (customer_profile['客戶生命週期天數'] / 30).round(0)

# 分群邏輯
def segment_customer(row):
    total_value = row['總購買額']
    frequency = row['購買次數']
    avg_score = row['平均評分']

    # 高價值 + 高頻率 + 高評分
    if total_value >= 1000 and frequency >= 5 and avg_score >= 4.0:
        return '忠實客戶'
    # 高價值 + 低頻率
    elif total_value >= 1000 and frequency < 3:
        return '大客戶'
    # 中價值 + 高頻率
    elif 300 <= total_value < 1000 and frequency >= 3:
        return '活躍客戶'
    # 新客戶
    elif frequency == 1:
        return '新客戶'
    # 低評分
    elif avg_score < 3:
        return '風險客戶'
    else:
        return '普通客戶'

customer_profile['分群'] = customer_profile.apply(segment_customer, axis=1)

# 分群統計
segment_stats = customer_profile.groupby('分群').agg(
    客戶數=('customer_id', 'count'),
    平均購買額=('總購買額', 'mean'),
    平均購買次數=('購買次數', 'mean'),
    平均評分=('平均評分', 'mean'),
    平均生命週期月數=('客戶生命週期月數', 'mean'),
    總購買額=('總購買額', 'sum')
).round(2)

segment_stats['銷售額占比(%)'] = (segment_stats['總購買額'] / segment_stats['總購買額'].sum() * 100).round(2)
segment_stats = segment_stats.sort_values('總購買額', ascending=False)

print("客戶分群統計:")
print(segment_stats)

# 各州的分群分佈
state_segment = customer_profile.groupby(['州別', '分群']).agg(
    客戶數=('customer_id', 'count'),
    平均購買額=('總購買額', 'mean')
).reset_index()

print("\n州別×分群矩陣 (Top 20):")
print(state_segment.nlargest(20, '客戶數'))

# 分群詳細客戶列表
for segment in customer_profile['分群'].unique():
    segment_customers = customer_profile[customer_profile['分群'] == segment]
    print(f"\n{segment} - 客戶樣本 (Top 5):")
    print(segment_customers[['customer_id', '州別', '城市', '購買次數', '總購買額', '平均評分']].nlargest(5, '總購買額'))
```

---

## 學習資源與相關文件

### 相關文件
- **Day01_MultiIndex_Complete_Guide.md** - MultiIndex 基礎
- **Day03_Pivot_Reshape_Guide.md** - 透視表與資料重塑
- **Day04_Practice_Integration.md** - 綜合專案實戰

### 推薦練習
1. 使用自己的 Olist 資料完成 RFM 分析
2. 實現產品 ABC 分類並輸出報表
3. 建立動態客戶分群系統

### 關鍵概念複習
- [ ] GroupBy Split-Apply-Combine 機制
- [ ] agg() vs transform() vs filter() 三者區別
- [ ] 命名聚合提高代碼可讀性
- [ ] 聚合函數選擇與應用場景

### 常見問題
**Q: 為何 transform() 後形狀不變？**
A: transform() 會將聚合結果廣播回原始行，保持 1:1 映射關係。

**Q: agg() 和 transform() 效能差異？**
A: 大型資料集中，transform() 通常快於多次 agg()，因為只需單次遍歷。

**Q: 如何處理 groupby 後的 NaN？**
A: 使用 `dropna=False` 參數或 `.fillna()` 方法。

---

## 習題答案與解答指南

若需要習題答案，請參考 `exercises/Day02_Solutions.ipynb`

**更新日期：** 2024年12月11日
**適用版本：** pandas 1.5.0+
**難度級別：** 進階（建議先完成 Day 01）
