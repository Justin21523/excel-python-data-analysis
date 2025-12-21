# Day 15: Merge 策略完全指南

## 學習目標
- 掌握 4 種 Join 類型（inner/left/outer/cross）
- 實現複雜的多表合併
- 避免常見的 Merge 陷阱
- 處理 Olist 9 張表的完整整合

---

## Part 1: Merge 基礎 (2 小時)

### 1.1 什麼是 Merge？

**對標 Excel：**
- Pandas merge = Excel VLOOKUP / INDEX-MATCH
- 更強大、更靈活的表連接

```python
import pandas as pd

# 載入示例數據
orders = pd.read_csv('/home/justin/web-projects/excel-python-data-analysis/week03-06_pandas-advanced/data/olist_orders_dataset.csv')
customers = pd.read_csv('/home/justin/web-projects/excel-python-data-analysis/week03-06_pandas-advanced/data/olist_customers_dataset.csv')

print(f"訂單表: {len(orders)} 行")
print(f"客戶表: {len(customers)} 行")

# 訂單表預覽
print("\n訂單表:")
print(orders[['order_id', 'customer_id', 'order_status']].head())

# 客戶表預覽
print("\nCustomer table:")
print(customers[['customer_id', 'customer_city', 'customer_state']].head())
```

### 1.2 基本 Merge 語法

```python
# 基本語法
merged = left_df.merge(
    right_df,
    on='join_key',           # 連接鍵
    how='inner'              # 連接類型
)

# 或者使用 pd.merge()
merged = pd.merge(
    left_df,
    right_df,
    on='join_key',
    how='inner'
)
```

### 1.3 四種 Join 類型

#### Join 1: Inner Join (交集)

```python
# Inner Join：只保留兩個表都有的記錄

merged_inner = orders.merge(
    customers,
    on='customer_id',
    how='inner'
)

print(f"Inner join 結果行數: {len(merged_inner)}")
# 輸出: Inner join 結果行數: 99441

# 所有訂單都有對應客戶，所以行數不變
```

**何時使用 Inner Join？**
- 只關心完整的配對記錄
- 清理數據（移除孤立記錄）
- 例如：只分析有有效客戶信息的訂單

#### Join 2: Left Join (左完全外連接)

```python
# Left Join：保留左表的所有記錄

merged_left = orders.merge(
    customers,
    on='customer_id',
    how='left'
)

print(f"Left join 結果行數: {len(merged_left)}")
# 輸出: Left join 結果行數: 99441 (same as orders)

# 驗證右表匹配情況
print(f"匹配的客戶記錄: {merged_left['customer_city'].notna().sum()}")
print(f"未匹配的記錄: {merged_left['customer_city'].isna().sum()}")
```

**何時使用 Left Join？**
- 保留左表的所有數據
- 最常見的 Join 類型
- 例如：保留所有訂單，附加客戶信息

#### Join 3: Outer Join (完全外連接)

```python
# Outer Join：保留兩個表的所有記錄

merged_outer = orders.merge(
    customers,
    on='customer_id',
    how='outer'
)

print(f"Outer join 結果行數: {len(merged_outer)}")
# 輸出: Outer join 結果行數: 99441 (如果所有客戶都有訂單)

# 檢查不匹配的情況
print(f"訂單為空: {merged_outer['order_id'].isna().sum()}")
print(f"客戶為空: {merged_outer['customer_id'].isna().sum()}")
```

**何時使用 Outer Join？**
- 需要保留兩個表的所有數據
- 分析缺失配對
- 例如：查找沒有訂單的客戶

#### Join 4: Cross Join (笛卡爾積)

```python
# Cross Join：每行與所有行組合

# 方法 1: 使用 merge with key='key'
df1 = pd.DataFrame({'A': [1, 2]})
df2 = pd.DataFrame({'B': ['x', 'y', 'z']})

df1['key'] = 1
df2['key'] = 1

cross = df1.merge(df2, on='key').drop('key', axis=1)

print(f"Cross join 結果: {len(df1)} × {len(df2)} = {len(cross)}")
# 輸出: Cross join 結果: 2 × 3 = 6

print(cross)
# 輸出:
#    A  B
# 0  1  x
# 1  1  y
# 2  1  z
# 3  2  x
# 4  2  y
# 5  2  z
```

**何時使用 Cross Join？**
- 組合所有可能的配對
- 稀有場景（通常不建議）
- 例如：為某商品的所有客戶組合生成建議列表

### 1.4 Join 類型可視化

```
Left Table (Orders)      Right Table (Customers)
────────────────────     ──────────────────────
order_id  customer_id    customer_id  customer_city
O001      C001           C001         São Paulo
O002      C002           C002         Rio
O003      C003           C004         Salvador
O004      C001
O005      C002

INNER JOIN (交集):
O001  C001  São Paulo
O002  C002  Rio
O003  C003  (無效)
O004  C001  São Paulo
O005  C002  Rio

LEFT JOIN (左表完全):
O001  C001  São Paulo
O002  C002  Rio
O003  C003  NULL
O004  C001  São Paulo
O005  C002  Rio

OUTER JOIN (並集):
O001  C001  São Paulo
O002  C002  Rio
O003  C003  NULL
O004  C001  São Paulo
O005  C002  Rio
NULL  C004  Salvador
```

---

## Part 2: Merge 進階技巧 (2 小時)

### 2.1 多鍵合併

```python
# 場景：訂單項目表需要同時按 order_id 和 product_id 合併

order_items = pd.read_csv('/home/justin/web-projects/excel-python-data-analysis/week03-06_pandas-advanced/data/olist_order_items_dataset.csv')
products = pd.read_csv('/home/justin/web-projects/excel-python-data-analysis/week03-06_pandas-advanced/data/olist_products_dataset.csv')

# 方法 1: 使用 on 列表
merged = order_items.merge(
    products,
    on=['product_id'],  # 可以是多個列
    how='left'
)

print(merged[['order_id', 'product_id', 'price', 'product_name_lenght']].head())
```

### 2.2 不同列名的合併 (left_on / right_on)

```python
# 場景：訂單表的 customer_id 要合併到客戶表的 customer_id

merged = orders.merge(
    customers,
    left_on='customer_id',
    right_on='customer_id',
    how='left'
)

# 或簡化為 (如果列名相同):
merged = orders.merge(
    customers,
    on='customer_id',
    how='left'
)

# 場景：列名不同的情況
# seller_id (in order_items) vs customer_id (in customers)
# order_items.merge(
#     customers,
#     left_on='seller_id',
#     right_on='customer_id',
#     how='left'
# )
```

### 2.3 處理列名衝突 (suffixes)

```python
# 問題：兩個表都有相同的列名

# 示例：都有 'price' 列
df1 = pd.DataFrame({'id': [1, 2], 'price': [100, 200]})
df2 = pd.DataFrame({'id': [1, 2], 'price': [110, 210]})

# 默認後綴：_x 和 _y
merged = df1.merge(df2, on='id', how='left', suffixes=('_order', '_product'))

print(merged)
# 輸出:
#    id  price_order  price_product
# 0   1          100            110
# 1   2          200            210

# 自定義後綴
merged = df1.merge(df2, on='id', how='left', suffixes=('_left', '_right'))
```

### 2.4 使用 indicator 驗證匹配

```python
# 場景：檢查哪些記錄未能成功匹配

merged = orders.merge(
    customers,
    on='customer_id',
    how='outer',
    indicator=True  # 添加 _merge 列
)

print(merged['_merge'].value_counts())
# 輸出:
# both          99441  (兩個表都有)
# left_only         0  (只在左表)
# right_only       0  (只在右表)

# 篩選未匹配的記錄
unmatched_left = merged[merged['_merge'] == 'left_only']
unmatched_right = merged[merged['_merge'] == 'right_only']
```

### 2.5 使用 validate 檢查一對多關係

```python
# validate 參數檢查 Join 的完整性

# 1:1 關係 - 每個鍵在兩個表中都只出現一次
merged = orders.merge(
    customers,
    on='customer_id',
    how='left',
    validate='m:1'  # 多個訂單 : 一個客戶
)

# m:1 = Many-to-one (左邊多個鍵可以對應右邊一個鍵)
# 1:1 = One-to-one
# 1:m = One-to-many
# m:m = Many-to-many (危險！)

# 如果違反約束會拋出錯誤
# ValueError: Merge keys are not unique in right dataset
```

### 2.6 按索引合併 (index)

```python
# 場景：使用索引而不是列進行合併

df1 = pd.DataFrame(
    {'value': [1, 2, 3]},
    index=pd.Index(['A', 'B', 'C'], name='key')
)

df2 = pd.DataFrame(
    {'value2': [10, 20, 30]},
    index=pd.Index(['A', 'B', 'C'], name='key')
)

# 按索引合併
merged = df1.merge(df2, left_index=True, right_index=True)

print(merged)
# 輸出:
#    value  value2
# A      1      10
# B      2      20
# C      3      30

# 或者使用 join（更簡潔）
merged = df1.join(df2)
```

---

## Part 3: Concat 策略 (1-2 小時)

### 3.1 Concat 基礎

```python
# Concat：沿著軸連接多個 DataFrame

# 方向 1: 垂直 (axis=0，默認) - 堆疊行
df1 = pd.DataFrame({'A': [1, 2], 'B': ['a', 'b']})
df2 = pd.DataFrame({'A': [3, 4], 'B': ['c', 'd']})

concat_vertical = pd.concat([df1, df2], axis=0)
print("垂直 concat:")
print(concat_vertical)
# 輸出:
#    A  B
# 0  1  a
# 1  2  b
# 0  3  c
# 1  4  d

# 重新索引
concat_vertical = pd.concat([df1, df2], axis=0, ignore_index=True)
# 輸出:
#    A  B
# 0  1  a
# 1  2  b
# 2  3  c
# 3  4  d

# 方向 2: 水平 (axis=1) - 並排放置列
df3 = pd.DataFrame({'C': [10, 20], 'D': ['x', 'y']})

concat_horizontal = pd.concat([df1, df3], axis=1)
print("\n水平 concat:")
print(concat_horizontal)
# 輸出:
#    A  B   C  D
# 0  1  a  10  x
# 1  2  b  20  y
```

### 3.2 Concat vs Merge 對比

```
場景對比
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
特性              Concat              Merge
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
用途              堆疊表格            連接表格
方向              軸向 (水平/垂直)   基於鍵
垂直用例          堆疊多批數據        累計銷售
水平用例          並排特徵            添加列特徵
性能              非常快              較慢（涉及查找）
復雜度            簡單                可能複雜
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

# 何時使用 Concat？
- 堆疊相同結構的表（多月數據）
- 水平並排列（添加特徵）
- 快速組合結果

# 何時使用 Merge？
- 根據特定鍵連接表
- 需要靈活的 Join 類型
- 處理不同的索引
```

### 3.3 處理 Concat 中的重複列

```python
# 場景：多個 DataFrame 有相同的列

df1 = pd.DataFrame({'key': ['A', 'B'], 'value': [1, 2]})
df2 = pd.DataFrame({'key': ['C', 'D'], 'value': [3, 4]})

# 保持重複列（默認）
result = pd.concat([df1, df2], axis=0, ignore_index=True)

# 或使用 keys 參數區分來源
result = pd.concat(
    [df1, df2],
    axis=0,
    ignore_index=False,
    keys=['batch1', 'batch2']
)

print(result)
# 輸出:
#          key  value
# batch1 0   A      1
#        1   B      2
# batch2 0   C      3
#        1   D      4
```

---

## 14 個實戰案例

### 案例 1: 簡單 Left Join - 訂單 + 客戶

```python
# 任務：將客戶城市信息附加到訂單

orders = pd.read_csv('/home/justin/web-projects/excel-python-data-analysis/week03-06_pandas-advanced/data/olist_orders_dataset.csv')
customers = pd.read_csv('/home/justin/web-projects/excel-python-data-analysis/week03-06_pandas-advanced/data/olist_customers_dataset.csv')

result = orders.merge(
    customers[['customer_id', 'customer_city', 'customer_state']],
    on='customer_id',
    how='left'
)

print(result[['order_id', 'customer_id', 'customer_city', 'customer_state']].head())

# 驗證匹配
print(f"\n總記錄: {len(result)}")
print(f"有城市信息: {result['customer_city'].notna().sum()}")
print(f"缺少城市信息: {result['customer_city'].isna().sum()}")
```

### 案例 2: Inner Join - 過濾有效訂單

```python
# 任務：只保留有有效客戶信息的訂單

result = orders.merge(
    customers[['customer_id', 'customer_city']],
    on='customer_id',
    how='inner'
)

print(f"原始訂單: {len(orders)}")
print(f"有效訂單: {len(result)}")
print(f"過濾掉: {len(orders) - len(result)} 訂單")
```

### 案例 3: 多表連續合併

```python
# 任務：合併訂單 → 客戶 → 地址信息

order_items = pd.read_csv('/home/justin/web-projects/excel-python-data-analysis/week03-06_pandas-advanced/data/olist_order_items_dataset.csv')

# 步驟 1: 訂單 + 客戶
df = orders.merge(customers, on='customer_id', how='left')

# 步驟 2: + 訂單項目
df = df.merge(order_items, on='order_id', how='left')

# 步驟 3: + 商品信息
products = pd.read_csv('/home/justin/web-projects/excel-python-data-analysis/week03-06_pandas-advanced/data/olist_products_dataset.csv')
df = df.merge(products, on='product_id', how='left')

print(f"最終表大小: {len(df)} 行 × {len(df.columns)} 列")
print(f"所有必要信息: {(df.isnull().sum() == 0).sum()} 列無缺失")
```

### 案例 4: 使用 indicator 驗證整合

```python
# 任務：確保所有訂單都有客戶信息

result = orders.merge(
    customers,
    on='customer_id',
    how='outer',
    indicator=True
)

print(result['_merge'].value_counts())

# 檢查異常情況
if (result['_merge'] == 'left_only').any():
    print("警告：存在無對應客戶的訂單！")
    orphan_orders = result[result['_merge'] == 'left_only']['order_id'].tolist()
    print(f"受影響的訂單 ID: {orphan_orders[:5]}")

# 清理（移除 _merge 列）
result = result.drop('_merge', axis=1)
```

### 案例 5: Suffixes - 處理列名衝突

```python
# 任務：合併兩個有相同列名的表

order_items = pd.read_csv('/home/justin/web-projects/excel-python-data-analysis/week03-06_pandas-advanced/data/olist_order_items_dataset.csv')
products = pd.read_csv('/home/justin/web-projects/excel-python-data-analysis/week03-06_pandas-advanced/data/olist_products_dataset.csv')

# 兩個表都有相同的列
print("order_items 列:", order_items.columns.tolist())
print("products 列:", products.columns.tolist())

# 合併時自動添加後綴
result = order_items.merge(
    products,
    on='product_id',
    how='left',
    suffixes=('_order', '_product')
)

print(result.columns.tolist())
# 顯示列名已添加後綴
```

### 案例 6: Anti Join - 查找未匹配的記錄

```python
# 任務：查找沒有訂單的客戶

# 方法：Outer join + 篩選
all_data = orders.merge(
    customers[['customer_id', 'customer_city']],
    on='customer_id',
    how='outer',
    indicator=True
)

customers_without_orders = all_data[all_data['_merge'] == 'right_only']

print(f"總客戶: {len(customers)}")
print(f"有訂單的客戶: {len(orders['customer_id'].unique())}")
print(f"沒有訂單的客戶: {len(customers_without_orders)}")
```

### 案例 7: 多鍵合併 - 訂單項目 + 評論

```python
# 任務：為訂單項目附加對應的評論

order_items = pd.read_csv('/home/justin/web-projects/excel-python-data-analysis/week03-06_pandas-advanced/data/olist_order_items_dataset.csv')
reviews = pd.read_csv('/home/justin/web-projects/excel-python-data-analysis/week03-06_pandas-advanced/data/olist_order_reviews_dataset.csv')

# 多個 Join 鍵
result = order_items.merge(
    reviews[['order_id', 'review_score', 'review_comment_title']],
    on='order_id',
    how='left'
)

print(result[['order_id', 'product_id', 'price', 'review_score']].head())

# 驗證
print(f"\n有評論的項目: {result['review_score'].notna().sum()}")
print(f"無評論的項目: {result['review_score'].isna().sum()}")
```

### 案例 8: 縮放問題 - 一對多 Merge

```python
# 任務：警惕一對多關係導致的行數爆炸

# 示例：一個訂單有多個項目
orders_sample = orders.head(5)
order_items_sample = order_items.head(20)

print(f"訂單: {len(orders_sample)} 行")
print(f"項目: {len(order_items_sample)} 行")

result = orders_sample.merge(order_items_sample, on='order_id', how='left')

print(f"合併後: {len(result)} 行 (可能膨脹！)")

# 檢查一個訂單有多少項目
items_per_order = order_items.groupby('order_id').size()
print(f"\n平均每訂單項目數: {items_per_order.mean():.1f}")
print(f"最多項目: {items_per_order.max()}")
```

### 案例 9: validate 檢查數據完整性

```python
# 任務：確保 Merge 符合預期的 1:m 關係

# 驗證關係：多個訂單 : 一個客戶
try:
    result = orders.merge(
        customers,
        on='customer_id',
        how='left',
        validate='m:1'  # 多個訂單對應一個客戶 ✓
    )
    print("✓ m:1 關係驗證成功")
except ValueError as e:
    print(f"✗ 驗證失敗: {e}")

# 驗證 1:1 關係（應該失敗）
try:
    result = orders.merge(
        customers,
        on='customer_id',
        how='left',
        validate='1:1'  # 一個訂單對應一個客戶 ✗
    )
    print("✓ 1:1 關係驗證成功")
except ValueError as e:
    print(f"✗ 驗證失敗: {e}")
    # 輸出: 驗證失敗: Merge keys are not unique in left dataset
```

### 案例 10: 垂直 Concat - 堆疊多月數據

```python
# 任務：合併多個月份的訂單數據

# 模擬不同月份的數據
january = orders.head(1000).copy()
january['month'] = '2023-01'

february = orders.iloc[1000:2000].copy()
february['month'] = '2023-02'

march = orders.iloc[2000:3000].copy()
march['month'] = '2023-03'

# 垂直堆疊
combined = pd.concat([january, february, march], axis=0, ignore_index=True)

print(f"合併行數: {len(combined)}")
print(f"月份分佈:")
print(combined['month'].value_counts().sort_index())
```

### 案例 11: 水平 Concat - 添加計算列

```python
# 任務：為訂單附加多個計算特徵

df = orders.merge(customers, on='customer_id', how='left')

# 計算多個特徵
order_count = orders.groupby('customer_id').size().reset_index(name='customer_order_count')
order_value = orders.groupby('customer_id')['order_purchase_timestamp'].count().reset_index(name='customer_value')

# 水平合併特徵
feature_matrix = pd.concat([
    df[['order_id', 'customer_id']],
    df[['customer_city', 'customer_state']]
], axis=1)

print(f"特徵矩陣大小: {feature_matrix.shape}")
```

### 案例 12: 完整的 Olist 9 表整合

```python
def integrate_all_olist_tables():
    """
    完整的 Olist 數據集整合
    集成 9 張表：訂單、客戶、項目、評論、商品、
                   銷售商、支付、運輸、地理位置
    """

    # 1. 加載數據
    orders = pd.read_csv('/home/justin/web-projects/excel-python-data-analysis/week03-06_pandas-advanced/data/olist_orders_dataset.csv')
    customers = pd.read_csv('/home/justin/web-projects/excel-python-data-analysis/week03-06_pandas-advanced/data/olist_customers_dataset.csv')
    order_items = pd.read_csv('/home/justin/web-projects/excel-python-data-analysis/week03-06_pandas-advanced/data/olist_order_items_dataset.csv')
    order_reviews = pd.read_csv('/home/justin/web-projects/excel-python-data-analysis/week03-06_pandas-advanced/data/olist_order_reviews_dataset.csv')
    products = pd.read_csv('/home/justin/web-projects/excel-python-data-analysis/week03-06_pandas-advanced/data/olist_products_dataset.csv')
    sellers = pd.read_csv('/home/justin/web-projects/excel-python-data-analysis/week03-06_pandas-advanced/data/olist_sellers_dataset.csv')

    print("="*60)
    print("Olist 完整數據整合")
    print("="*60)

    # 2. 合併流程
    print("\n合併流程:")

    # 訂單 + 客戶
    df = orders.merge(customers, on='customer_id', how='left')
    print(f"1. 訂單 + 客戶: {len(df):,} 行")

    # + 訂單項目
    df = df.merge(order_items, on='order_id', how='left')
    print(f"2. + 訂單項目: {len(df):,} 行")

    # + 評論
    df = df.merge(
        order_reviews[['order_id', 'review_score', 'review_comment_title']],
        on='order_id',
        how='left'
    )
    print(f"3. + 評論: {len(df):,} 行")

    # + 商品
    df = df.merge(products[['product_id', 'product_category_name']], on='product_id', how='left')
    print(f"4. + 商品: {len(df):,} 行")

    # + 銷售商
    df = df.merge(
        sellers[['seller_id', 'seller_city', 'seller_state']],
        on='seller_id',
        how='left',
        suffixes=('_customer', '_seller')
    )
    print(f"5. + 銷售商: {len(df):,} 行")

    # 3. 統計
    print("\n整合統計:")
    print(f"總列數: {len(df.columns)}")
    print(f"缺失數據最多的列:")

    missing = df.isnull().sum()
    print(missing[missing > 0].sort_values(ascending=False).head())

    print(f"\n主要列的數據類型:")
    print(df[['order_id', 'customer_id', 'seller_id', 'product_category_name', 'review_score']].dtypes)

    return df

# 運行整合
result = integrate_all_olist_tables()
```

### 案例 13: 自連接 - 查找重複客戶訂單

```python
# 任務：找出同一客戶在不同日期的訂單

# 自連接 (Self-join)
df = orders[['order_id', 'customer_id', 'order_purchase_timestamp']].copy()

# 合併同一客戶的訂單
result = df.merge(
    df,
    on='customer_id',
    suffixes=('_order1', '_order2')
)

# 篩選不同的訂單對
result = result[result['order_id_order1'] != result['order_id_order2']]

# 移除反向對
result = result[result['order_id_order1'] < result['order_id_order2']]

print(f"找到 {len(result)} 對同一客戶的重複訂單")
print(result.head())
```

### 案例 14: 複雜業務邏輯合併

```python
# 任務：基於複雜規則合併銷售和客戶數據

# 基礎合併
df = orders.merge(customers, on='customer_id', how='left')
df = df.merge(order_items, on='order_id', how='left')

# 添加複雜計算
df['customer_order_count'] = df.groupby('customer_id')['order_id'].transform('count')
df['customer_avg_review'] = df.groupby('customer_id')['review_score'].transform('mean')

# 條件篩選
df['is_vip'] = (df['customer_order_count'] >= 5) & (df['customer_avg_review'] >= 4)

# 聚合結果
vip_analysis = df[df['is_vip']].groupby('customer_id').agg({
    'order_id': 'count',
    'price': ['sum', 'mean'],
    'customer_city': 'first'
}).round(2)

print(vip_analysis.head())
```

---

## 常見陷阱與解決方案

### 陷阱 1: Merge 導致行數增加

```python
# 問題：一對多關係導致行數膨脹
print(f"左表: {len(orders)} 行")
print(f"右表: {len(order_items)} 行")

result = orders.merge(order_items, on='order_id')

print(f"合併後: {len(result)} 行 (膨脹！)")
# 輸出: 合併後: 112650 行 (膨脹！)

# 解決方案：使用 validate 提醒自己
result = orders.merge(order_items, on='order_id', validate='1:m')
```

### 陷阱 2: 缺失值導致未匹配

```python
# 問題：連接鍵中有缺失值
df_with_null = orders.copy()
df_with_null.loc[0, 'customer_id'] = None

# Merge 會忽略缺失值
result = df_with_null.merge(customers, on='customer_id')

print(f"原始: {len(df_with_null)}")
print(f"合併後: {len(result)}")  # 缺失值行被移除

# 解決方案：檢查缺失值
print(f"連接鍵中的缺失值: {df_with_null['customer_id'].isna().sum()}")
```

### 陷阱 3: 重複鍵導致笛卡爾積

```python
# 問題：連接鍵在右表有重複
customers_dup = customers.copy()
customers_dup = pd.concat([customers_dup, customers_dup.iloc[[0]]], ignore_index=True)

print(f"左表: {len(orders)} 行")
print(f"右表（有重複）: {len(customers_dup)} 行")

result = orders.merge(customers_dup, on='customer_id')

print(f"合併後: {len(result)} 行 (意外膨脹！)")

# 解決方案：使用 validate
try:
    result = orders.merge(customers_dup, on='customer_id', validate='m:1')
except ValueError:
    print("✗ 檢測到右表有重複鍵！")
```

---

## Excel 對照

### VLOOKUP vs Pandas merge

```
VLOOKUP (Excel)                  Pandas merge
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
=VLOOKUP(A2,範圍,列號,FALSE)     df.merge(lookup_df,
                                  on=key, how='left')

=VLOOKUP(A2,範圍,列號,TRUE)      df.merge(lookup_df,
                                  on=key, how='left')
                                  (需要排序)

INDEX-MATCH 組合              df.merge(多個鍵,
                               how='left')

多表查找                      多個 merge 串聯

IFERROR                       left join + fillna
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

# Pandas 優勢：
# ✓ 支持多列 join
# ✓ 所有 join 類型
# ✓ 自動去重（使用 unique）
# ✓ 性能更好（> 1M 行）
```

---

## 性能優化

### Merge 性能貼士

```python
# 1. 對連接鍵排序（如果需要多次 merge）
df = df.sort_values('customer_id')

# 2. 使用 left join 而非 outer
# outer 需要檢查兩側，更慢

# 3. 移除不需要的列
df = df[['order_id', 'customer_id']]  # 只保留必要列

# 4. 批量 merge（避免多次循環）
df = orders.merge(customers).merge(products).merge(reviews)
# 而非：
# df = orders.merge(customers)
# df = df.merge(products)
# df = df.merge(reviews)

# 5. 使用 merge 而非 apply + lookup
# ✗ 慢：df['city'] = df['customer_id'].apply(lambda x: lookup(x))
# ✓ 快：df = df.merge(cities, on='customer_id')
```

---

## 學習成果

通過完成本節，你將能夠：
- ✓ 掌握 4 種 Join 類型及其應用場景
- ✓ 實現複雜的多表合併
- ✓ 使用 indicator 和 validate 驗證數據完整性
- ✓ 處理列名衝突和一對多關係
- ✓ 使用 Concat 進行高效的表堆疊
- ✓ 整合 Olist 的 9 張表
- ✓ 避免常見的 Merge 陷阱

---

## 下一步

進入 **Day 16: 實踐整合**，完成大數據處理 Pipeline 最終項目！
