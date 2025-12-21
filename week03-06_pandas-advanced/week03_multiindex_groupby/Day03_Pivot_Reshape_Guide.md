# Day 03: Pivot 與資料重塑 - 樞紐分析與形狀轉換

## 課程目錄
- [Part 1: pivot_table 完全掌握（2h）](#part-1-pivot_table-完全掌握2h)
- [Part 2: stack / unstack 深度理解（2h）](#part-2-stack--unstack-深度理解2h)
- [Part 3: melt 寬表變長表（2h）](#part-3-melt-寬表變長表2h)
- [Part 4: 綜合實戰練習（3h）](#part-4-綜合實戰練習3h)
- [學習資源與相關文件](#學習資源與相關文件)

---

## Part 1: pivot_table 完全掌握(2h)

### 1.1 Pivot Table 基礎概念

**Excel 類比：**
- Excel 樞紐分析表（Pivot Table）
- 拖拽欄位到行、列、值的直觀操作
- 快速建立多維交叉分析

**pandas pivot_table 核心參數：**
- `index` - 行分組欄位
- `columns` - 列分組欄位
- `values` - 聚合欄位
- `aggfunc` - 聚合函數
- `margins` - 總計行列
- `fill_value` - 填充缺失值

### 1.2 基礎透視表

#### 案例 1: 簡單透視表 - 類別×支付方式

```python
import pandas as pd
import numpy as np

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

# 最簡單的透視表：計算各類別的銷售額
simple_pivot = order_data.pivot_table(
    values='price',           # 要聚合的欄位
    index='product_category_name',  # 行分組
    aggfunc='sum'            # 聚合函數
).sort_values(ascending=False)

print("各產品類別的銷售額:")
print(simple_pivot.head(15))
```

**Excel 對照：**
```
Excel 樞紐分析表:
列欄: 無
行欄: product_category_name
值欄: 加總 price
```

#### 案例 2: 二維透視表 - 類別×支付方式

```python
# 類別作為行，支付方式作為列，銷售額為值
pivot_2d = order_data.pivot_table(
    values='price',
    index='product_category_name',
    columns='payment_type',
    aggfunc='sum'
).fillna(0).round(0).astype(int)

print("產品類別×支付方式 銷售額透視表 (單位:元):")
print(pivot_2d)

# 計算行合計（各類別總銷售額）
pivot_2d['總計'] = pivot_2d.sum(axis=1)
print("\n包含行合計的透視表:")
print(pivot_2d)
```

#### 案例 3: 多值透視表

```python
# 同時計算銷售額和訂單數
pivot_multi = order_data.pivot_table(
    values=['price', 'order_id'],
    index='product_category_name',
    columns='payment_type',
    aggfunc={'price': 'sum', 'order_id': 'count'}
).round(2)

print("產品類別×支付方式 多維透視表:")
print(pivot_multi.head(10))

# 重新組織欄位使其更清晰
# 解析多層級欄位名稱
pivot_multi.columns = ['_'.join(col).strip() for col in pivot_multi.columns.values]
print("\nMulti-value pivot table:")
print(pivot_multi.head(10))
```

#### 案例 4: 使用 margins 計算總計

```python
# margins=True 自動添加行合計和列合計（All）
pivot_with_margins = order_data.pivot_table(
    values='price',
    index='customer_state',
    columns='payment_type',
    aggfunc='sum',
    margins=True,           # 添加總計行列
    margins_name='總計'     # 總計行/列名稱
).round(2)

print("州別×支付方式 銷售額（含總計）:")
print(pivot_with_margins)

# 計算各支付方式的銷售占比
pivot_pct = order_data.pivot_table(
    values='price',
    index='customer_state',
    columns='payment_type',
    aggfunc='sum',
    margins=True,
    margins_name='總計'
).fillna(0)

# 百分比計算（相對於列合計）
pivot_pct_normalized = pivot_pct.div(pivot_pct.loc['總計'], axis=1) * 100

print("\n各州在不同支付方式中的銷售占比(%):")
print(pivot_pct_normalized.round(2))
```

#### 案例 5: 複雜多維透視表

```python
# 州別和城市作為多層行索引，產品類別×支付方式
pivot_complex = order_data.pivot_table(
    values='price',
    index=['customer_state', 'customer_city'],
    columns=['product_category_name', 'payment_type'],
    aggfunc='count',  # 計數訂單數
    fill_value=0
)

print("複雜多維透視表 (前 10 行):")
print(pivot_complex.iloc[:10, :10])

# 簡化複雜表：只顯示頂層索引
print(f"\n複雜表的形狀: {pivot_complex.shape}")
print(f"行索引層數: {pivot_complex.index.nlevels}")
print(f"列索引層數: {pivot_complex.columns.nlevels}")
```

### 1.3 高級 pivot_table 技巧

#### 案例 6: 多聚合函數透視表

```python
# 同時計算多個統計指標
pivot_stats = order_data.pivot_table(
    values='price',
    index='product_category_name',
    columns='payment_type',
    aggfunc=['sum', 'mean', 'count', 'std'],  # 多個聚合函數
    fill_value=0
).round(2)

print("產品類別×支付方式 多統計指標:")
print(pivot_stats.head(10))

# 提取特定統計指標
sales_by_category_payment = pivot_stats['sum']
print("\n銷售額統計:")
print(sales_by_category_payment.head(10))

avg_by_category_payment = pivot_stats['mean']
print("\n平均客單價:")
print(avg_by_category_payment.head(10))
```

#### 案例 7: 自訂聚合函數

```python
# 使用 lambda 自訂函數計算四分位數
def q1(x):
    return x.quantile(0.25)

def q3(x):
    return x.quantile(0.75)

pivot_quantile = order_data.pivot_table(
    values='price',
    index='product_category_name',
    columns='payment_type',
    aggfunc={
        'price': ['min', q1, 'median', q3, 'max']
    },
    fill_value=0
).round(2)

print("產品類別 價格分佈分析 (min, Q1, median, Q3, max):")
print(pivot_quantile)
```

#### 案例 8: 時間維度透視表

```python
# 轉換時間戳為年月
order_data['order_year_month'] = pd.to_datetime(order_data['order_purchase_timestamp']).dt.to_period('M')
order_data['order_year'] = pd.to_datetime(order_data['order_purchase_timestamp']).dt.year
order_data['order_month'] = pd.to_datetime(order_data['order_purchase_timestamp']).dt.month

# 建立月度×產品類別銷售透視表
monthly_pivot = order_data.pivot_table(
    values='price',
    index='order_year_month',
    columns='product_category_name',
    aggfunc='sum',
    fill_value=0
).round(0).astype(int)

print("月度×產品類別 銷售額透視表 (Last 12 months):")
print(monthly_pivot.tail(12))

# 計算月度成長率
monthly_pivot_pct_change = monthly_pivot.pct_change() * 100

print("\n月度環比增長率(%) (Last 11 months):")
print(monthly_pivot_pct_change.tail(11).round(2))
```

#### 案例 9: 排名與占比

```python
# 建立銷售額透視表
sales_pivot = order_data.pivot_table(
    values='price',
    index='customer_state',
    columns='product_category_name',
    aggfunc='sum',
    fill_value=0
).round(2)

# 計算各州在各類別中的銷售額占比
sales_pct = sales_pivot.div(sales_pivot.sum(axis=0), axis=1) * 100

print("各州在不同產品類別中的銷售占比(%):")
print(sales_pct.round(2))

# 找出每個類別的 Top 3 州
print("\n各產品類別的 Top 3 州:")
for category in sales_pct.columns:
    top_states = sales_pct[category].nlargest(3)
    print(f"\n{category}:")
    for state, pct in top_states.items():
        print(f"  {state}: {pct:.2f}%")
```

#### 案例 10: 透視表轉為 DataFrame

```python
# 透視表常用於可視化，但需要轉回 DataFrame 進行進一步分析
sales_by_state = order_data.pivot_table(
    values='price',
    index='customer_state',
    aggfunc='sum'
).reset_index()

sales_by_state.columns = ['state', 'total_sales']
sales_by_state = sales_by_state.sort_values('total_sales', ascending=False)

print("州別銷售額排行:")
print(sales_by_state.head(10))

# 添加銷售排名
sales_by_state['rank'] = sales_by_state['total_sales'].rank(method='min', ascending=False).astype(int)
sales_by_state['sales_pct'] = (sales_by_state['total_sales'] / sales_by_state['total_sales'].sum() * 100).round(2)

print("\n帶排名和占比的州別銷售統計:")
print(sales_by_state.head(10))
```

---

## Part 2: stack / unstack 深度理解(2h)

### 2.1 Stack 和 Unstack 概念

**核心概念：**
- `stack()` - 將列變為索引（欄位→行索引）- 寬表→長表
- `unstack()` - 將索引變為列（索引→欄位）- 長表→寬表
- 互為反向操作

**Excel 對照：**
- `unstack()` - Excel Power Query 的 Pivot 功能
- `stack()` - Excel Power Query 的 Unpivot 功能

### 2.2 Stack 操作

#### 案例 11: 基本 Stack 操作

```python
# 建立簡單的 DataFrame
sample_data = order_data.groupby(['customer_state', 'payment_type']).agg({
    'price': 'sum',
    'order_id': 'count'
}).reset_index()

# 透視表形式
sales_pivot = sample_data.pivot_table(
    index='customer_state',
    columns='payment_type',
    values='price',
    fill_value=0
)

print("原始透視表 (寬表):")
print(sales_pivot)

# Stack 操作：將列轉為索引
stacked = sales_pivot.stack()
print("\nStack 後（長表）:")
print(stacked)
print(f"形狀: {stacked.shape}")

# Stack 後的資料結構
print("\nStack 後的索引結構:")
print(f"索引層數: {stacked.index.nlevels}")
print(f"索引名稱: {stacked.index.names}")
```

#### 案例 12: 多層級 Stack

```python
# 多欄值的透視表
multi_pivot = order_data.pivot_table(
    index='customer_state',
    columns='payment_type',
    values=['price', 'order_id'],
    aggfunc='sum',
    fill_value=0
)

print("多欄值透視表:")
print(multi_pivot)

# Stack 一層
stacked_once = multi_pivot.stack()
print("\nStack 一次後:")
print(stacked_once.head(10))

# Stack 二層（完全扁平化）
stacked_twice = multi_pivot.stack(dropna=False).stack(dropna=False)
print("\nStack 二次後:")
print(stacked_twice.head(20))
```

#### 案例 13: Stack 在資料重塑中的應用

```python
# 場景：將寬表轉為長表以便進行時間序列分析

# 時間序列寬表：每列是一個月份
monthly_sales = order_data.pivot_table(
    index='product_category_name',
    columns='order_year_month',
    values='price',
    aggfunc='sum',
    fill_value=0
)

print("月度×類別 銷售額寬表:")
print(monthly_sales)

# Stack 轉為長表
monthly_sales_long = monthly_sales.stack().reset_index()
monthly_sales_long.columns = ['category', 'month', 'sales']

print("\nStack 後的長表:")
print(monthly_sales_long.head(20))

# 現在可以方便地進行時間序列分析
monthly_growth = monthly_sales_long.groupby('category').apply(
    lambda x: x.sort_values('month').assign(growth_rate=x['sales'].pct_change() * 100)
)

print("\nTime series growth rate:")
print(monthly_growth[monthly_growth['category'] == monthly_growth['category'].unique()[0]])
```

### 2.3 Unstack 操作

#### 案例 14: 基本 Unstack 操作

```python
# 建立長表（多層索引）
long_data = order_data.groupby(['customer_state', 'payment_type']).agg({
    'price': 'sum'
}).round(2)

print("原始長表（多層索引）:")
print(long_data)
print(f"形狀: {long_data.shape}")

# Unstack：將索引層變為欄位
wide_data = long_data.unstack()
print("\nUnstack 後（寬表）:")
print(wide_data)
print(f"形狀: {wide_data.shape}")

# Unstack 特定層級
unstack_payment = long_data.unstack(level='payment_type')
print("\nUnstack 特定層級 (payment_type):")
print(unstack_payment.head(10))
```

#### 案例 15: 多層 Unstack

```python
# 多層索引資料
multi_index_data = order_data.groupby(['customer_state', 'product_category_name', 'payment_type']).agg({
    'price': ['sum', 'count']
}).round(2)

print("三層索引資料:")
print(multi_index_data.head(15))

# Unstack 一層（payment_type→columns）
unstack_1 = multi_index_data.unstack(level=-1)  # 最後一層
print("\nUnstack 最後一層:")
print(unstack_1.head(10))

# Unstack 多層
unstack_2 = multi_index_data.unstack(level=['payment_type', 'product_category_name'])
print("\nUnstack 多層:")
print(unstack_2.head(5))
```

#### 案例 16: Fill Value 與缺失值處理

```python
# Unstack 時處理缺失值
incomplete_data = order_data[order_data['customer_state'].isin(['SP', 'RJ', 'MG'])].groupby(
    ['customer_state', 'product_category_name']
)['price'].sum()

print("不完整的長表（某些組合不存在）:")
print(incomplete_data.head(20))

# Unstack 有缺失值
unstack_with_nan = incomplete_data.unstack()
print("\nUnstack 後含 NaN:")
print(unstack_with_nan)

# 用 0 填充缺失值
unstack_filled = incomplete_data.unstack(fill_value=0)
print("\nUnstack 並用 0 填充:")
print(unstack_filled)

# 用組內平均值填充
group_avg = incomplete_data.groupby(level=0).mean()
unstack_filled_avg = incomplete_data.unstack().fillna(group_avg)
print("\nUnstack 並用組平均值填充:")
print(unstack_filled_avg)
```

### 2.4 Stack/Unstack 高級應用

#### 案例 17: 轉換與合併多個透視表

```python
# 場景：比較不同支付方式的銷售情況

# 為每個支付方式建立透視表
for payment_type in order_data['payment_type'].unique()[:3]:  # 只看前 3 種支付方式
    payment_data = order_data[order_data['payment_type'] == payment_type]

    payment_pivot = payment_data.groupby(['customer_state', 'product_category_name'])['price'].sum()
    payment_pivot = payment_pivot.unstack(fill_value=0).round(0).astype(int)

    print(f"\n{payment_type} 的州×類別銷售額:")
    print(payment_pivot)
```

#### 案例 18: 索引與欄位互換

```python
# 場景：需要交換分析維度

# 原始透視：行為州，列為類別
sales_by_state_category = order_data.pivot_table(
    index='customer_state',
    columns='product_category_name',
    values='price',
    aggfunc='sum',
    fill_value=0
).round(0).astype(int)

print("原始透視（州×類別）:")
print(sales_by_state_category.iloc[:5, :5])

# 轉置：行變列，列變行
transposed = sales_by_state_category.T
print("\n轉置後（類別×州）:")
print(transposed.iloc[:5, :5])

# 使用 stack/unstack 達到同樣效果
long_form = sales_by_state_category.stack().reset_index()
long_form.columns = ['state', 'category', 'sales']

category_state = long_form.pivot_table(
    index='category',
    columns='state',
    values='sales',
    fill_value=0
).astype(int)

print("\n使用 Stack/Unstack 達到轉置效果:")
print(category_state.iloc[:5, :5])
```

---

## Part 3: melt 寬表變長表(2h)

### 3.1 Melt 基礎概念

**Melt 的作用：**
- 將寬表轉為長表（unpivot）
- 指定保留欄位（id_vars）和數值欄位（value_vars）
- 常用於資料清洗和準備

**Excel 對照：**
- 類似 Excel Power Query 的 Unpivot 功能

### 3.2 基本 Melt 操作

#### 案例 19: 簡單 Melt

```python
# 建立寬表：月份為欄位
monthly_wide = order_data.pivot_table(
    index='product_category_name',
    columns='order_year_month',
    values='price',
    aggfunc='sum',
    fill_value=0
).reset_index()

print("寬表（產品類別×月份）:")
print(monthly_wide.head())

# 基本 melt
monthly_long = pd.melt(
    monthly_wide,
    id_vars='product_category_name',  # 保留的欄位
    var_name='month',                  # 新欄位名（原列名）
    value_name='sales'                 # 新欄位名（原值）
)

print("\nMelt 後（長表）:")
print(monthly_long.head(15))
```

#### 案例 20: 多 ID 欄位 Melt

```python
# 場景：保留多個標識欄位

# 建立複雜寬表
state_city_monthly = order_data.pivot_table(
    index=['customer_state', 'customer_city'],
    columns='order_year_month',
    values='price',
    aggfunc='sum',
    fill_value=0
).reset_index()

print("寬表（州-城市×月份）:")
print(state_city_monthly.head(10))

# Melt 多個 ID 欄位
state_city_long = pd.melt(
    state_city_monthly,
    id_vars=['customer_state', 'customer_city'],  # 多個 ID 欄位
    var_name='month',
    value_name='sales'
)

print("\nMelt 後（保留州和城市）:")
print(state_city_long.head(20))

# 過濾出銷售額大於 0 的記錄
state_city_long_filtered = state_city_long[state_city_long['sales'] > 0]
print(f"\n過濾後行數: {len(state_city_long_filtered)}")
```

#### 案例 21: 部分欄位 Melt

```python
# 場景：只 Melt 特定欄位

# 建立混合寬表（包含多種指標）
mixed_wide = order_data.groupby('product_category_name').agg({
    '2017-01': ('price', 'sum'),
    '2017-02': ('price', 'sum'),
    '2017-03': ('price', 'sum'),
    'avg_score': ('review_score', 'mean'),
    'order_count': ('order_id', 'count')
}).reset_index()

# 簡化：只考慮月份欄位
month_cols = [col for col in mixed_wide.columns if col.startswith('201')]

melted = pd.melt(
    mixed_wide,
    id_vars=['product_category_name', 'avg_score', 'order_count'],
    value_vars=month_cols,
    var_name='month',
    value_name='sales'
)

print("部分欄位 Melt 結果:")
print(melted.head(15))
```

### 3.3 複雜 Melt 案例

#### 案例 22: 多層級欄位名 Melt

```python
# 建立包含多層級欄位的寬表
multi_level_wide = order_data.pivot_table(
    index='product_category_name',
    columns=['order_year_month', 'payment_type'],
    values='price',
    aggfunc='sum',
    fill_value=0
).reset_index()

print("多層級欄位寬表:")
print(multi_level_wide.head())

# Melt 多層級欄位
# 首先展平欄位名
multi_level_wide.columns = ['_'.join(col).strip('_') if col[0] != 'product_category_name' else col[0]
                             for col in multi_level_wide.columns.values]

melted_multi = pd.melt(
    multi_level_wide,
    id_vars='product_category_name',
    var_name='month_payment',
    value_name='sales'
)

# 分離月份和支付方式
melted_multi[['month', 'payment_type']] = melted_multi['month_payment'].str.split('_', expand=True)
melted_multi = melted_multi.drop('month_payment', axis=1)

print("\n展平多層級 Melt 結果:")
print(melted_multi.head(20))
```

#### 案例 23: Melt 後的資料聚合

```python
# 寬表
quarterly_wide = pd.DataFrame({
    'product': ['A', 'B', 'C'],
    'Q1_sales': [1000, 1500, 2000],
    'Q1_profit': [100, 150, 200],
    'Q2_sales': [1200, 1600, 2100],
    'Q2_profit': [120, 160, 210],
    'Q3_sales': [1300, 1700, 2200],
    'Q3_profit': [130, 170, 220]
})

print("原始寬表:")
print(quarterly_wide)

# Melt
quarterly_long = pd.melt(
    quarterly_wide,
    id_vars='product',
    var_name='quarter_metric',
    value_name='value'
)

# 分離季度和指標
quarterly_long[['quarter', 'metric']] = quarterly_long['quarter_metric'].str.split('_', expand=True)
quarterly_long = quarterly_long.drop('quarter_metric', axis=1)

print("\nMelt 後的長表:")
print(quarterly_long.head(15))

# 再次 Pivot：轉為 quarter（行）×metric（列）
quarterly_pivot = quarterly_long.pivot_table(
    index=['product', 'quarter'],
    columns='metric',
    values='value',
    aggfunc='sum'
)

print("\nRe-pivot 後:")
print(quarterly_pivot)
```

#### 案例 24: 時間序列 Melt

```python
# 場景：將客戶月度購買額轉為長表

# 建立客戶月度購買額寬表
customer_monthly = order_data.pivot_table(
    index='customer_id',
    columns='order_year_month',
    values='price',
    aggfunc='sum',
    fill_value=0
).reset_index()

print("客戶月度購買額寬表:")
print(customer_monthly.head())

# Melt
customer_monthly_long = pd.melt(
    customer_monthly,
    id_vars='customer_id',
    var_name='month',
    value_name='purchase_amount'
)

# 過濾出實際購買記錄
customer_monthly_long = customer_monthly_long[customer_monthly_long['purchase_amount'] > 0]

print("\nMelt 後的客戶購買時間序列:")
print(customer_monthly_long.head(20))

# 計算客戶購買频率和平均金額
customer_summary = customer_monthly_long.groupby('customer_id').agg({
    'month': 'count',           # 購買月數
    'purchase_amount': ['sum', 'mean', 'std']  # 購買總額、平均額、波動
}).round(2)

customer_summary.columns = ['purchase_months', 'total_amount', 'avg_amount', 'std_amount']
print("\n客戶購買統計:")
print(customer_summary.head(10))
```

### 3.4 Melt vs Stack 比較

#### 案例 25: Melt vs Stack 效果對比

```python
# 寬表
sales_wide = order_data.pivot_table(
    index='product_category_name',
    columns='payment_type',
    values='price',
    aggfunc='sum',
    fill_value=0
).reset_index()

print("原始寬表:")
print(sales_wide)

# 方法 1: Melt
melted = pd.melt(
    sales_wide,
    id_vars='product_category_name',
    var_name='payment_type',
    value_name='sales'
)

print("\nMelt 結果:")
print(melted.head(10))

# 方法 2: Stack（先設置索引）
stacked = sales_wide.set_index('product_category_name').stack().reset_index()
stacked.columns = ['product_category_name', 'payment_type', 'sales']

print("\nStack 結果:")
print(stacked.head(10))

# 驗證結果相同
print(f"\nMelt 和 Stack 結果是否相同? {melted.sort_values(['product_category_name', 'payment_type']).reset_index(drop=True).equals(stacked.sort_values(['product_category_name', 'payment_type']).reset_index(drop=True))}")
```

---

## Part 4: 綜合實戰練習(3h)

### 練習 1: 建立月度銷售透視表

**目標：** 建立一份專業的月度銷售分析報表

```python
# Step 1: 準備資料
monthly_data = order_data.groupby(['order_year_month', 'product_category_name']).agg({
    'price': 'sum',
    'order_id': 'count',
    'customer_id': 'nunique'
}).reset_index()

monthly_data.columns = ['month', 'category', 'sales', 'orders', 'customers']

print("原始聚合資料:")
print(monthly_data.head(20))

# Step 2: 建立透視表
sales_pivot = monthly_data.pivot_table(
    index='month',
    columns='category',
    values='sales',
    aggfunc='sum',
    margins=True,
    margins_name='合計'
).round(0).astype(int)

print("\n月度×類別 銷售額透視表:")
print(sales_pivot)

# Step 3: 計算環比增長
sales_pivot_growth = sales_pivot.pct_change() * 100

print("\n月度環比增長率(%):")
print(sales_pivot_growth.round(2))

# Step 4: 訂單數透視表
orders_pivot = monthly_data.pivot_table(
    index='month',
    columns='category',
    values='orders',
    aggfunc='sum',
    margins=True,
    margins_name='合計'
).fillna(0).astype(int)

print("\n月度×類別 訂單數透視表:")
print(orders_pivot)

# Step 5: 客戶數透視表
customers_pivot = monthly_data.pivot_table(
    index='month',
    columns='category',
    values='customers',
    aggfunc='sum',
    margins=True,
    margins_name='合計'
).fillna(0).astype(int)

print("\n月度×類別 客戶數透視表:")
print(customers_pivot)

# Step 6: 計算客單價
avg_order_value = (sales_pivot / orders_pivot).round(2)

print("\n月度×類別 平均客單價:")
print(avg_order_value.head(12))
```

### 練習 2: 地區 × 類別交叉分析

**目標：** 建立地區-產品類別矩陣報表

```python
# Step 1: 匯總資料
region_product = order_data.groupby(['customer_state', 'product_category_name']).agg({
    'price': 'sum',
    'order_id': 'count',
    'customer_id': 'nunique',
    'review_score': 'mean'
}).reset_index()

region_product.columns = ['state', 'category', 'sales', 'orders', 'customers', 'rating']

print("地區×類別原始資料:")
print(region_product.head(20))

# Step 2: 銷售額透視表
state_category_sales = region_product.pivot_table(
    index='state',
    columns='category',
    values='sales',
    aggfunc='sum',
    margins=True,
    margins_name='全國'
).round(0).astype(int)

print("\n地區×類別 銷售額透視表:")
print(state_category_sales)

# Step 3: 計算銷售占比（相對於行總計）
state_category_pct = state_category_sales.div(state_category_sales['全國'], axis=0) * 100

print("\n各地區的產品類別銷售占比(%):")
print(state_category_pct.round(2))

# Step 4: 計算銷售占比（相對於列總計）
state_category_pct_col = state_category_sales.div(state_category_sales.loc['全國'], axis=1) * 100

print("\n各產品類別在不同地區的銷售占比(%):")
print(state_category_pct_col.round(2))

# Step 5: 平均評分透視表
state_category_rating = region_product.pivot_table(
    index='state',
    columns='category',
    values='rating',
    aggfunc='mean'
).round(2)

print("\n地區×類別 平均評分透視表:")
print(state_category_rating)

# Step 6: 客戶數透視表
state_category_customers = region_product.pivot_table(
    index='state',
    columns='category',
    values='customers',
    aggfunc='sum',
    fill_value=0
).astype(int)

print("\n地區×類別 客戶數透視表:")
print(state_category_customers)
```

### 練習 3: 動態報表生成系統

**目標：** 建立靈活的報表生成工具，支援多維度分析

```python
# 定義報表生成函數
def generate_pivot_report(data, index_cols, column_cols, value_col, agg_func='sum', top_n=None):
    """
    生成透視表報表

    Parameters:
    -----------
    data : DataFrame
        輸入資料
    index_cols : list or str
        行分組欄位
    column_cols : list or str
        列分組欄位
    value_col : str
        聚合欄位
    agg_func : str or callable
        聚合函數
    top_n : int
        只顯示 Top N 行

    Returns:
    --------
    DataFrame : 透視表結果
    """
    pivot = data.pivot_table(
        index=index_cols,
        columns=column_cols,
        values=value_col,
        aggfunc=agg_func,
        margins=True,
        margins_name='合計',
        fill_value=0
    ).round(2)

    if top_n:
        # 按合計欄排序
        if isinstance(index_cols, str):
            pivot = pivot.sort_values('合計', ascending=False).head(top_n)

    return pivot

# 報表 1: 州別×支付方式
print("報表 1: 州別×支付方式 銷售額")
report1 = generate_pivot_report(
    order_data,
    index_cols='customer_state',
    column_cols='payment_type',
    value_col='price',
    agg_func='sum',
    top_n=10
)
print(report1)

# 報表 2: 產品類別×支付方式×訂單數
print("\n\n報表 2: 產品類別×支付方式 訂單數")
report2 = generate_pivot_report(
    order_data,
    index_cols='product_category_name',
    column_cols='payment_type',
    value_col='order_id',
    agg_func='count',
    top_n=10
)
print(report2)

# 報表 3: 月度×州別（Top 5 州）
top_states = order_data.groupby('customer_state')['price'].sum().nlargest(5).index
top_state_data = order_data[order_data['customer_state'].isin(top_states)]

print("\n\n報表 3: 月度×Top 5 州 銷售額")
report3 = generate_pivot_report(
    top_state_data,
    index_cols='order_year_month',
    column_cols='customer_state',
    value_col='price',
    agg_func='sum'
)
print(report3.tail(12))

# 定義高級報表函數：包含多個指標
def generate_multi_metric_report(data, index_cols, column_cols):
    """生成多指標綜合報表"""

    # 銷售額
    sales = data.pivot_table(
        index=index_cols,
        columns=column_cols,
        values='price',
        aggfunc='sum',
        fill_value=0
    )

    # 訂單數
    orders = data.pivot_table(
        index=index_cols,
        columns=column_cols,
        values='order_id',
        aggfunc='count',
        fill_value=0
    )

    # 客戶數
    customers = data.pivot_table(
        index=index_cols,
        columns=column_cols,
        values='customer_id',
        aggfunc='nunique',
        fill_value=0
    )

    return {
        'sales': sales.round(0).astype(int),
        'orders': orders.astype(int),
        'customers': customers.astype(int),
        'avg_order_value': (sales / orders).round(2)
    }

# 生成綜合報表
print("\n\n綜合報表: 州別×支付方式")
multi_report = generate_multi_metric_report(
    order_data[order_data['customer_state'].isin(top_states)],
    index_cols='customer_state',
    column_cols='payment_type'
)

print("\n銷售額:")
print(multi_report['sales'].head(10))

print("\n訂單數:")
print(multi_report['orders'].head(10))

print("\n客戶數:")
print(multi_report['customers'].head(10))

print("\n平均客單價:")
print(multi_report['avg_order_value'].head(10))
```

---

## 學習資源與相關文件

### 相關文件
- **Day01_MultiIndex_Complete_Guide.md** - MultiIndex 基礎
- **Day02_GroupBy_Advanced_Guide.md** - GroupBy 聚合
- **Day04_Practice_Integration.md** - 綜合專案實戰

### 推薦練習
1. 使用自己的 Olist 資料建立月度銷售報表
2. 建立地區-產品矩陣分析
3. 使用 Stack/Unstack 進行資料轉換

### 關鍵概念複習
- [ ] Pivot Table 三個核心參數
- [ ] Stack 與 Unstack 的互補性
- [ ] Melt 與 Stack 的區別和選擇
- [ ] 多層級索引的處理
- [ ] 缺失值在重塑時的處理

### 常見問題
**Q: Melt 和 Stack 有何區別？**
A: Melt 針對 DataFrame 欄位，Stack 針對索引；Melt 更直觀，Stack 更靈活。

**Q: Unstack 出現 NaN 怎麼辦？**
A: 使用 `fill_value` 參數或 `.fillna()` 方法進行填充。

**Q: 多層級 Pivot Table 如何處理？**
A: 設置多個 index 或 columns 參數；結果會有多層級索引。

---

## 習題答案與解答指南

若需要習題答案，請參考 `exercises/Day03_Solutions.ipynb`

**更新日期：** 2024年12月11日
**適用版本：** pandas 1.5.0+
**難度級別：** 進階（建議先完成 Day 01-02）
