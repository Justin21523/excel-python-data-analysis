# Day 04: 綜合實踐 - Olist 多維度分析系統

## 專案概述

本專案整合 Day 1-3 所有技能，建立一套完整的多維度分析系統。通過該系統，您將學會如何使用 MultiIndex、GroupBy、Pivot Table 等技術解決實際商業分析問題。

---

## 專案目標

### 主要目標
整合 MultiIndex、GroupBy、Pivot Table 等技術，建立完整的 Olist 多維度分析報表系統

### 具體成果
1. 建立「年-月-類別-地區」四維度分析結構
2. 計算各維度 KPI（銷售額、訂單數、客單價、成長率等）
3. 生成三份可視化報表
4. 實現動態報表更新機制

---

## 專案架構

```
Olist 多維度分析系統
│
├─ Step 1: 資料載入與預處理
│  ├─ 載入多個資料表
│  ├─ 資料清洗與驗證
│  └─ 建立聯合資料集
│
├─ Step 2: 建立 MultiIndex 結構
│  ├─ 定義四維度索引
│  ├─ 計算基礎指標
│  └─ 驗證資料完整性
│
├─ Step 3: 計算各維度 KPI
│  ├─ 時間維度分析（月度、季度、年度）
│  ├─ 地區維度分析（州別、城市）
│  ├─ 產品維度分析（類別、細分）
│  └─ 綜合維度分析（上述組合）
│
├─ Step 4: 生成透視表報表
│  ├─ 報表 1: 月度類別表現
│  ├─ 報表 2: 地區類別矩陣
│  └─ 報表 3: Top 產品排行
│
└─ Step 5: 格式化與輸出
   ├─ 數據格式化
   ├─ 條件計算（MoM 成長率等）
   └─ 導出 Excel
```

---

## Step 1: 資料載入與預處理（30min）

### 1.1 載入資料集

```python
import pandas as pd
import numpy as np
from datetime import datetime, timedelta
import warnings
warnings.filterwarnings('ignore')

# 載入 Olist 資料
from utils.data_loader import OlistDataLoader

loader = OlistDataLoader()

# 加載各表
orders = loader.get_orders()
order_items = loader.get_order_items()
customers = loader.get_customers()
products = loader.get_products()
sellers = loader.get_sellers()

print("=== 資料集信息 ===")
print(f"訂單表: {orders.shape}")
print(f"訂單項目表: {order_items.shape}")
print(f"客戶表: {customers.shape}")
print(f"產品表: {products.shape}")
print(f"賣家表: {sellers.shape}")

# 驗證欄位
print("\n=== 欄位驗證 ===")
print(f"訂單表欄位: {orders.columns.tolist()}")
print(f"訂單項目表欄位: {order_items.columns.tolist()}")
print(f"客戶表欄位: {customers.columns.tolist()}")
```

### 1.2 資料清洗與檢驗

```python
# 檢查缺失值
print("=== 缺失值檢查 ===")
print("訂單表缺失值:")
print(orders.isnull().sum())

print("\n訂單項目表缺失值:")
print(order_items.isnull().sum())

print("\n客戶表缺失值:")
print(customers.isnull().sum())

# 檢查時間範圍
orders['order_purchase_timestamp'] = pd.to_datetime(orders['order_purchase_timestamp'])

min_date = orders['order_purchase_timestamp'].min()
max_date = orders['order_purchase_timestamp'].max()

print(f"\n=== 時間範圍 ===")
print(f"最早訂單: {min_date}")
print(f"最新訂單: {max_date}")
print(f"跨度: {(max_date - min_date).days} 天")

# 訂單狀態分佈
print(f"\n=== 訂單狀態分佈 ===")
print(orders['order_status'].value_counts())

# 支付方式分佈
print(f"\n=== 支付方式分佈 ===")
print(orders['payment_type'].value_counts())
```

### 1.3 建立聯合資料集

```python
# 合併訂單和訂單項目
order_full = orders.merge(order_items, on='order_id', how='inner')

print(f"合併後行數: {len(order_full)}")

# 加入客戶信息
order_full = order_full.merge(customers[['customer_id', 'customer_state', 'customer_city']],
                               on='customer_id',
                               how='left')

# 加入產品信息
order_full = order_full.merge(products[['product_id', 'product_category_name']],
                               on='product_id',
                               how='left')

# 加入賣家信息
order_full = order_full.merge(sellers[['seller_id', 'seller_state']],
                               on='seller_id',
                               how='left')

print(f"\n最終資料集形狀: {order_full.shape}")
print(f"\n欄位列表: {order_full.columns.tolist()}")

# 驗證合併結果
print(f"\n=== 驗證 ===")
print(f"不重複訂單數: {order_full['order_id'].nunique()}")
print(f"不重複客戶數: {order_full['customer_id'].nunique()}")
print(f"不重複產品類別: {order_full['product_category_name'].nunique()}")
print(f"不重複州別: {order_full['customer_state'].nunique()}")

# 查看樣本資料
print("\n=== 樣本資料 ===")
print(order_full[['order_id', 'customer_state', 'product_category_name', 'price', 'order_purchase_timestamp']].head(10))
```

### 1.4 特徵工程

```python
# 建立時間維度欄位
order_full['order_date'] = order_full['order_purchase_timestamp'].dt.date
order_full['order_year'] = order_full['order_purchase_timestamp'].dt.year
order_full['order_month'] = order_full['order_purchase_timestamp'].dt.month
order_full['order_year_month'] = order_full['order_purchase_timestamp'].dt.to_period('M')
order_full['order_quarter'] = order_full['order_purchase_timestamp'].dt.quarter
order_full['order_day_of_week'] = order_full['order_purchase_timestamp'].dt.day_name()

# 建立計算欄位
order_full['total_value'] = order_full['price'] + order_full['freight_value']

# 處理缺失類別
order_full['product_category_name'] = order_full['product_category_name'].fillna('其他')
order_full['customer_state'] = order_full['customer_state'].fillna('未知')

# 檢驗特徵工程
print("=== 特徵工程驗證 ===")
print(f"時間範圍: {order_full['order_year_month'].min()} 到 {order_full['order_year_month'].max()}")
print(f"有效的年月數: {order_full['order_year_month'].nunique()}")
print(f"狀態分佈:\n{order_full['order_status'].value_counts()}")
print(f"\n前 10 個產品類別:")
print(order_full['product_category_name'].value_counts().head(10))

print("\n資料準備完成！")
```

---

## Step 2: 建立 MultiIndex 結構（45min）

### 2.1 四維度基礎指標計算

```python
# 基礎聚合：按四維度分組計算
four_dim_base = order_full.groupby(
    ['order_year_month', 'customer_state', 'product_category_name', 'payment_type']
).agg(
    # 銷售指標
    銷售額=('price', 'sum'),
    訂單數=('order_id', 'count'),
    客戶數=('customer_id', 'nunique'),

    # 品質指標
    平均客單價=('price', 'mean'),
    平均評分=('review_score', 'mean'),

    # 物流指標
    平均運費=('freight_value', 'mean')
).reset_index()

print("四維度基礎指標:")
print(four_dim_base.head(20))

# 計算派生指標
four_dim_base['客單價_人均'] = (四_dim_base['銷售額'] / four_dim_base['客戶數']).round(2)
four_dim_base['回購率'] = (four_dim_base['訂單數'] / four_dim_base['客戶數']).round(2)

print("\n包含派生指標:")
print(four_dim_base[['order_year_month', 'customer_state', 'product_category_name',
                     '銷售額', '訂單數', '客戶數', '客單價_人均']].head(20))
```

### 2.2 建立 MultiIndex

```python
# 建立四層級 MultiIndex
four_dim_multi = four_dim_base.copy()

# 轉換 period 為 string 便於操作
four_dim_multi['order_year_month'] = four_dim_multi['order_year_month'].astype(str)

# 設置 MultiIndex
four_dim_multi = four_dim_multi.set_index(
    ['order_year_month', 'customer_state', 'product_category_name', 'payment_type']
)

print("=== MultiIndex 結構 ===")
print(f"索引名稱: {four_dim_multi.index.names}")
print(f"索引層數: {four_dim_multi.index.nlevels}")
print(f"資料形狀: {four_dim_multi.shape}")

print("\n前 10 行:")
print(four_dim_multi.head(10))

# 驗證索引
print(f"\n=== 索引驗證 ===")
print(f"年月數: {four_dim_multi.index.get_level_values(0).nunique()}")
print(f"州數: {four_dim_multi.index.get_level_values(1).nunique()}")
print(f"產品類別數: {four_dim_multi.index.get_level_values(2).nunique()}")
print(f"支付方式數: {four_dim_multi.index.get_level_values(3).nunique()}")
```

### 2.3 索引切片與查詢

```python
# 查詢特定月份的資料
specific_month = '2018-01'
month_data = four_dim_multi.loc[specific_month]

print(f"=== {specific_month} 的資料 ===")
print(month_data.head(10))

# 查詢特定州的資料
sp_state = 'SP'
sp_data = four_dim_multi.loc[(slice(None), sp_state), :]

print(f"\n=== {sp_state} 州的資料 (前 20 行) ===")
print(sp_data.head(20))

# 查詢特定類別
specific_category = 'esportes'
category_data = four_dim_multi.loc[(slice(None), slice(None), specific_category), :]

print(f"\n=== {specific_category} 類別的資料 (前 20 行) ===")
print(category_data.head(20))

# 跨層級查詢（月份和州）
query_data = four_dim_multi.loc[('2018-01', 'SP'), :]

print(f"\n=== 2018年1月 SP州的資料 ===")
print(query_data)
```

---

## Step 3: 計算各維度 KPI（1h）

### 3.1 時間維度 KPI

```python
# 月度銷售額聚合
monthly_sales = order_full.groupby('order_year_month').agg(
    銷售額=('price', 'sum'),
    訂單數=('order_id', 'count'),
    客戶數=('customer_id', 'nunique'),
    平均客單價=('price', 'mean'),
    平均評分=('review_score', 'mean')
).round(2)

# 計算環比增長
monthly_sales['銷售額環比增長(%)'] = monthly_sales['銷售額'].pct_change() * 100
monthly_sales['訂單數環比增長(%)'] = monthly_sales['訂單數'].pct_change() * 100

print("=== 月度銷售 KPI ===")
print(monthly_sales)

# 季度銷售額聚合
quarterly_sales = order_full.groupby(['order_year', 'order_quarter']).agg(
    銷售額=('price', 'sum'),
    訂單數=('order_id', 'count'),
    客戶數=('customer_id', 'nunique'),
).round(2)

print("\n=== 季度銷售 KPI ===")
print(quarterly_sales)

# 年度銷售額聚合
yearly_sales = order_full.groupby('order_year').agg(
    銷售額=('price', 'sum'),
    訂單數=('order_id', 'count'),
    客戶數=('customer_id', 'nunique'),
    平均客單價=('price', 'mean')
).round(2)

print("\n=== 年度銷售 KPI ===")
print(yearly_sales)
```

### 3.2 地區維度 KPI

```python
# 州別銷售分析
state_sales = order_full.groupby('customer_state').agg(
    銷售額=('price', 'sum'),
    訂單數=('order_id', 'count'),
    客戶數=('customer_id', 'nunique'),
    平均客單價=('price', 'mean'),
    平均評分=('review_score', 'mean'),
    平均運費=('freight_value', 'mean')
).round(2)

state_sales['銷售額占比(%)'] = (state_sales['銷售額'] / state_sales['銷售額'].sum() * 100).round(2)
state_sales = state_sales.sort_values('銷售額', ascending=False)

print("=== 州別銷售 KPI (Top 15) ===")
print(state_sales.head(15))

# 城市銷售分析（Top 20 城市）
city_sales = order_full.groupby(['customer_state', 'customer_city']).agg(
    銷售額=('price', 'sum'),
    訂單數=('order_id', 'count'),
    客戶數=('customer_id', 'nunique'),
    平均客單價=('price', 'mean')
).round(2).reset_index()

city_sales = city_sales.sort_values('銷售額', ascending=False)

print("\n=== 城市銷售 KPI (Top 20) ===")
print(city_sales.head(20))
```

### 3.3 產品維度 KPI

```python
# 產品類別銷售分析
category_sales = order_full.groupby('product_category_name').agg(
    銷售額=('price', 'sum'),
    訂單數=('order_id', 'count'),
    客戶數=('customer_id', 'nunique'),
    平均客單價=('price', 'mean'),
    平均評分=('review_score', 'mean'),
    平均運費=('freight_value', 'mean'),
    產品數=('product_id', 'nunique')
).round(2)

category_sales['銷售額占比(%)'] = (category_sales['銷售額'] / category_sales['銷售額'].sum() * 100).round(2)
category_sales = category_sales.sort_values('銷售額', ascending=False)

print("=== 產品類別銷售 KPI ===")
print(category_sales)

# 計算 ABC 分類
category_sales['累計銷售額'] = category_sales['銷售額'].cumsum()
total_sales = category_sales['銷售額'].sum()
category_sales['累計銷售占比(%)'] = (category_sales['累計銷售額'] / total_sales * 100).round(2)

def abc_class(pct):
    if pct <= 80:
        return 'A'
    elif pct <= 95:
        return 'B'
    else:
        return 'C'

category_sales['ABC分類'] = category_sales['累計銷售占比(%)'].apply(abc_class)

print("\n=== 產品 ABC 分類 ===")
print(category_sales[['銷售額', '累計銷售占比(%)', 'ABC分類']])
```

### 3.4 綜合維度 KPI

```python
# 月度×州別分析
monthly_state = order_full.groupby(['order_year_month', 'customer_state']).agg(
    銷售額=('price', 'sum'),
    訂單數=('order_id', 'count'),
    客戶數=('customer_id', 'nunique')
).round(2).reset_index()

print("=== 月度×州別銷售 KPI (前 20 行) ===")
print(monthly_state.head(20))

# 月度×類別分析
monthly_category = order_full.groupby(['order_year_month', 'product_category_name']).agg(
    銷售額=('price', 'sum'),
    訂單數=('order_id', 'count'),
    客戶數=('customer_id', 'nunique'),
    平均評分=('review_score', 'mean')
).round(2).reset_index()

print("\n=== 月度×類別銷售 KPI (前 20 行) ===")
print(monthly_category.head(20))

# 州別×類別分析
state_category = order_full.groupby(['customer_state', 'product_category_name']).agg(
    銷售額=('price', 'sum'),
    訂單數=('order_id', 'count'),
    客戶數=('customer_id', 'nunique'),
    平均客單價=('price', 'mean')
).round(2).reset_index()

state_category = state_category.sort_values('銷售額', ascending=False)

print("\n=== 州別×類別銷售 KPI (前 30 行) ===")
print(state_category.head(30))
```

---

## Step 4: 生成透視表報表（1h）

### 4.1 報表 1: 月度類別表現 (含 MoM 成長率)

```python
print("\n" + "="*80)
print("報表 1: 月度類別表現分析（MoM 成長率）")
print("="*80 + "\n")

# 建立透視表
monthly_category_pivot = order_full.pivot_table(
    index='order_year_month',
    columns='product_category_name',
    values='price',
    aggfunc='sum',
    fill_value=0
).round(0).astype(int)

print("=== 月度×類別銷售額透視表 ===")
print(monthly_category_pivot)

# 計算環比增長率
monthly_growth = monthly_category_pivot.pct_change() * 100

print("\n=== 月度環比增長率(%)===")
print(monthly_growth.round(2))

# 加入總計欄位
monthly_category_pivot['全部類別'] = monthly_category_pivot.sum(axis=1)
monthly_growth_with_total = monthly_category_pivot.pct_change() * 100

print("\n=== 月度銷售額及成長率 ===")
print(f"最近 12 個月銷售額:")
print(monthly_category_pivot.tail(12))

# 計算各類別的環比平均增長率
avg_growth_by_category = monthly_growth.mean()
print("\n=== 各類別的平均環比增長率(%) ===")
print(avg_growth_by_category.sort_values(ascending=False).head(10))

# 總體趨勢分析
print("\n=== 總體銷售趨勢 ===")
total_monthly = monthly_category_pivot.sum(axis=1)
print(total_monthly)

print(f"\n最高銷售月份: {total_monthly.idxmax()} ({total_monthly.max():,.0f})")
print(f"最低銷售月份: {total_monthly.idxmin()} ({total_monthly.min():,.0f})")
```

### 4.2 報表 2: 地區類別矩陣（熱力圖資料）

```python
print("\n" + "="*80)
print("報表 2: 地區×產品類別矩陣分析")
print("="*80 + "\n")

# 建立透視表
state_category_pivot = order_full.pivot_table(
    index='customer_state',
    columns='product_category_name',
    values='price',
    aggfunc='sum',
    fill_value=0,
    margins=True,
    margins_name='全國'
).round(0).astype(int)

print("=== 地區×產品類別銷售額透視表 ===")
print(state_category_pivot)

# 計算銷售占比（相對於行總計）
state_category_pct = state_category_pivot.div(state_category_pivot['全國'], axis=0) * 100

print("\n=== 各地區的產品類別銷售占比(%) ===")
print(state_category_pct.iloc[:-1].round(1))  # 排除總計行

# 計算銷售占比（相對於列總計）
state_category_pct_col = state_category_pivot.div(state_category_pivot.loc['全國'], axis=1) * 100

print("\n=== 各產品類別在不同地區的銷售占比(%) ===")
print(state_category_pct_col.iloc[:-1, :-1].round(1))  # 排除總計行列

# 識別各州的主力產品（貢獻度>20%）
print("\n=== 各州的主力產品（貢獻度>20%）===")
for state in state_category_pct.index[:-1]:  # 排除總計行
    main_products = state_category_pct.loc[state]
    main_products = main_products[main_products > 20].sort_values(ascending=False)

    if len(main_products) > 0:
        print(f"\n{state}:")
        for category, pct in main_products.items():
            if category != '全國':
                print(f"  {category}: {pct:.1f}%")

# 各州銷售額排名
state_total = state_category_pivot['全國'].iloc[:-1].sort_values(ascending=False)

print("\n=== 州別銷售額排名 ===")
for rank, (state, sales) in enumerate(state_total.items(), 1):
    pct = sales / state_total.sum() * 100
    print(f"{rank:2d}. {state}: {sales:>10,.0f} ({pct:>5.1f}%)")
```

### 4.3 報表 3: Top 產品排行（動態更新）

```python
print("\n" + "="*80)
print("報表 3: Top 產品與動態排行")
print("="*80 + "\n")

# 計算各產品的銷售表現
product_performance = order_full.groupby('product_id').agg(
    銷售額=('price', 'sum'),
    訂單數=('order_id', 'count'),
    客戶數=('customer_id', 'nunique'),
    平均客單價=('price', 'mean'),
    平均評分=('review_score', 'mean'),
    類別=('product_category_name', 'first')
).reset_index()

product_performance = product_performance.sort_values('銷售額', ascending=False)

print("=== Top 50 暢銷產品 ===")
print(product_performance[['product_id', '類別', '銷售額', '訂單數', '客戶數', '平均評分']].head(50).to_string())

# 按類別的 Top 產品
print("\n\n=== 各類別 Top 5 暢銷產品 ===")
for category in order_full['product_category_name'].unique()[:10]:  # 只看前 10 個類別
    category_products = product_performance[product_performance['類別'] == category]

    if len(category_products) > 0:
        print(f"\n{category}:")
        top_products = category_products[['product_id', '銷售額', '訂單數', '平均評分']].head(5)

        for idx, row in top_products.iterrows():
            print(f"  {row['product_id'][:20]:20s} | 銷售額: {row['銷售額']:>10,.0f} | 訂單: {row['訂單數']:>6.0f} | 評分: {row['平均評分']:>4.2f}")

# 動態排名：按月份跟蹤 Top 產品變化
print("\n\n=== Top 10 產品的月度銷售趨勢 ===")
top_10_products = product_performance.head(10)['product_id'].values

for product_id in top_10_products[:5]:  # 只展示前 5 個
    product_data = order_full[order_full['product_id'] == product_id]

    monthly_sales = product_data.groupby('order_year_month')['price'].sum()

    print(f"\n產品 {product_id[:20]}: 首次銷售 {monthly_sales.idxmin()} -> 最高銷售 {monthly_sales.idxmax()}")
    print(f"銷售趨勢: {monthly_sales.to_dict()}")
```

---

## Step 5: 格式化與輸出（45min）

### 5.1 建立綜合報表資料結構

```python
print("\n" + "="*80)
print("步驟 5: 格式化與輸出")
print("="*80 + "\n")

# 建立報表字典
reports = {}

# 報表 A: 月度銷售概覽
reports['月度銷售概覽'] = monthly_sales.copy()

# 報表 B: 州別銷售排名
reports['州別銷售排名'] = state_sales.copy()

# 報表 C: 產品類別排名
reports['產品類別排名'] = category_sales.copy()

# 報表 D: 月度×類別透視
reports['月度類別透視'] = monthly_category_pivot.copy()

# 報表 E: 地區×類別透視
reports['地區類別透視'] = state_category_pivot.copy()

print("已生成 5 份報表:")
for report_name in reports.keys():
    print(f"  - {report_name}: {reports[report_name].shape}")
```

### 5.2 數據格式化與驗證

```python
# 格式化函數
def format_currency(value):
    """格式化貨幣值"""
    return f"R${value:,.2f}" if isinstance(value, (int, float)) else value

def format_percent(value):
    """格式化百分比"""
    return f"{value:.2f}%" if isinstance(value, (int, float)) else value

# 建立格式化報表
print("\n=== 格式化後的月度銷售報表 ===")
monthly_formatted = monthly_sales.copy()
monthly_formatted['銷售額'] = monthly_formatted['銷售額'].apply(lambda x: f"R${x:,.0f}")
monthly_formatted['平均客單價'] = monthly_formatted['平均客單價'].apply(lambda x: f"R${x:,.2f}")
monthly_formatted['銷售額環比增長(%)'] = monthly_formatted['銷售額環比增長(%)'].apply(lambda x: f"{x:.2f}%")

print(monthly_formatted.tail(12))

# 驗證資料一致性
print("\n=== 資料驗證 ===")

# 驗證銷售額總和
total_pivot_sales = monthly_category_pivot['全部類別'].sum()
total_order_sales = order_full['price'].sum()

print(f"透視表銷售額總計: R${total_pivot_sales:,.0f}")
print(f"原始資料銷售額總計: R${total_order_sales:,.0f}")
print(f"差異: R${abs(total_pivot_sales - total_order_sales):,.0f}")

# 驗證訂單數
total_pivot_orders = monthly_category_pivot.shape[0]
total_order_items = len(order_full)

print(f"\n透視表訂單行數: {total_pivot_orders}")
print(f"原始訂單項目數: {total_order_items}")

print("\n資料驗證完成！")
```

### 5.3 匯出到 Excel（可選）

```python
# 定義輸出檔案路徑
output_file = '/home/justin/web-projects/excel-python-data-analysis/week03-06_pandas-advanced/week03_multiindex_groupby/notebooks/Olist_多維度分析報表.xlsx'

# 使用 ExcelWriter 匯出多個 Sheet
try:
    with pd.ExcelWriter(output_file, engine='openpyxl') as writer:
        # 報表 1: 月度銷售
        monthly_sales.to_excel(writer, sheet_name='月度銷售概覽')

        # 報表 2: 州別銷售
        state_sales.to_excel(writer, sheet_name='州別銷售排名')

        # 報表 3: 產品類別
        category_sales.to_excel(writer, sheet_name='產品類別排名')

        # 報表 4: 月度×類別
        monthly_category_pivot.to_excel(writer, sheet_name='月度類別透視')

        # 報表 5: 地區×類別
        state_category_pivot.to_excel(writer, sheet_name='地區類別透視')

        # 報表 6: 原始四維資料
        four_dim_base.to_excel(writer, sheet_name='四維度詳細資料', index=False)

    print(f"✓ 報表已導出至: {output_file}")

except Exception as e:
    print(f"✗ 導出失敗: {str(e)}")
```

### 5.4 生成執行摘要

```python
print("\n" + "="*80)
print("執行摘要 - Olist 多維度分析系統")
print("="*80)

# 時間範圍
date_range = f"{order_full['order_purchase_timestamp'].min().date()} 至 {order_full['order_purchase_timestamp'].max().date()}"

print(f"\n分析時間範圍: {date_range}")
print(f"涵蓋月份數: {order_full['order_year_month'].nunique()}")

# 規模指標
print(f"\n=== 規模指標 ===")
print(f"總訂單數: {order_full['order_id'].nunique():,}")
print(f"總訂單項目數: {len(order_full):,}")
print(f"不重複客戶數: {order_full['customer_id'].nunique():,}")
print(f"不重複產品數: {order_full['product_id'].nunique():,}")

# 銷售指標
print(f"\n=== 銷售指標 ===")
total_sales = order_full['price'].sum()
total_freight = order_full['freight_value'].sum()
total_value = total_sales + total_freight

print(f"總銷售額: R${total_sales:,.2f}")
print(f"總運費: R${total_freight:,.2f}")
print(f"總交易額: R${total_value:,.2f}")
print(f"平均客單價: R${order_full['price'].mean():,.2f}")
print(f"平均訂單大小: {order_full.groupby('order_id')['product_id'].nunique().mean():.2f} 件/訂單")

# 地理覆蓋
print(f"\n=== 地理覆蓋 ===")
print(f"涵蓋州別數: {order_full['customer_state'].nunique()}")
print(f"涵蓋城市數: {order_full['customer_city'].nunique()}")

# 產品覆蓋
print(f"\n=== 產品覆蓋 ===")
print(f"產品類別數: {order_full['product_category_name'].nunique()}")

# Top 3 品類
top_3_categories = order_full.groupby('product_category_name')['price'].sum().nlargest(3)
print(f"\nTop 3 產品類別:")
for category, sales in top_3_categories.items():
    pct = sales / total_sales * 100
    print(f"  {category}: R${sales:,.0f} ({pct:.1f}%)")

# 品質指標
print(f"\n=== 品質指標 ===")
print(f"平均評分: {order_full['review_score'].mean():.2f}/5.0")
print(f"評分覆蓋率: {order_full['review_score'].notna().sum() / len(order_full) * 100:.1f}%")

# 及時交付
delivered_ratio = (order_full['order_status'] == 'delivered').sum() / len(order_full) * 100
print(f"已交付訂單占比: {delivered_ratio:.1f}%")

print("\n" + "="*80)
print("分析完成！")
print("="*80)
```

---

## 評估標準

| 評估維度 | 滿分 | 評估內容 |
|---------|------|---------|
| **功能完整性** | 40% | - MultiIndex 正確建立（10%）<br>- KPI 計算準確（15%）<br>- 報表內容齊全（15%）|
| **代碼清晰度** | 30% | - 註釋充足（10%）<br>- 代碼結構化（10%）<br>- 變數命名規範（10%）|
| **報表美觀度** | 20% | - 欄位命名清晰（5%）<br>- 數據格式化（7%）<br>- 排版整齊（8%）|
| **效能優化** | 10% | - 無冗餘計算（5%）<br>- 執行速度（5%）|

---

## 常見問題與解決方案

### Q1: MultiIndex 建立時出現 KeyError？
**A:** 確保分組欄位在 DataFrame 中存在，並檢查欄位名稱是否正確。

### Q2: Pivot Table 結果有大量 NaN？
**A:** 使用 `fill_value=0` 填充，或檢查分組組合是否存在。

### Q3: 計算環比增長時出現 NaN？
**A:** 第一行無法計算，使用 `pct_change()` 後應 skip 第一行。

### Q4: 匯出 Excel 時報錯？
**A:** 確保已安裝 `openpyxl` 包：`pip install openpyxl`

### Q5: 如何提高大資料集的處理速度？
**A:** 使用 `nlargest()` 代替排序，使用 Categorical 類型減少記憶體用量。

---

## 進階擴展方向

1. **機器學習應用**：使用客戶分群資料訓練聚類模型
2. **預測分析**：基於時間序列預測下月銷售
3. **異常檢測**：識別異常的銷售模式
4. **互動式儀表板**：使用 Plotly/Streamlit 建立動態報表
5. **自動化報表**：定期生成並自動發送報表

---

## 相關文件與資源

- **Day01_MultiIndex_Complete_Guide.md** - MultiIndex 基礎與進階
- **Day02_GroupBy_Advanced_Guide.md** - GroupBy 與聚合運算
- **Day03_Pivot_Reshape_Guide.md** - Pivot Table 與資料重塑
- **exercises/** 目錄 - 更多練習題與解答

---

## 學習檢查清單

完成本專案後，您應該能夠：

- [ ] 理解 MultiIndex 的作用與結構
- [ ] 使用 groupby() 進行多維度聚合
- [ ] 建立複雜的 pivot_table 報表
- [ ] 計算環比增長、占比等派生指標
- [ ] 匯出結構化報表到 Excel
- [ ] 使用 pandas 解決實際商業分析問題

**專案完成時間：** 約 4-5 小時
**建議環境：** Python 3.8+, pandas 1.3.0+
**更新日期：** 2024年12月11日
