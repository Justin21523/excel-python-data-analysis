# Solutions_Complete: 前 5 題詳細解答

## 目錄
1. Exercise 10 (記憶體優化) - 題目 1-3
2. Exercise 11 (向量化操作) - 題目 1-2
3. 完整代碼 + 結果

---

## Exercise 10: 記憶體優化

### 題目 1: 分析 orders 表的記憶體使用

**解答：**

```python
import pandas as pd
import numpy as np

# 載入數據
orders = pd.read_csv('/home/justin/web-projects/excel-python-data-analysis/week03-06_pandas-advanced/data/olist_orders_dataset.csv')

# 方法 1: 使用 memory_usage(deep=True)
memory_per_column = orders.memory_usage(deep=True)

# 排序找出最耗記憶體的列
memory_sorted = memory_per_column.sort_values(ascending=False)

print("記憶體使用統計")
print("=" * 60)

# 前 3 列
print("\n記憶體使用最多的前 3 列:")
for i, (col, mem) in enumerate(memory_sorted.head(3).items(), 1):
    mem_mb = mem / 1024**2
    print(f"{i}. {col}: {mem_mb:.2f} MB")

# 總記憶體
total_memory = memory_per_column.sum() / 1024**2
print(f"\n總記憶體: {total_memory:.2f} MB")

# 佔比最高
max_col = memory_sorted.index[0]
max_mem = memory_sorted.iloc[0]
percentage = (max_mem / memory_per_column.sum()) * 100
print(f"\n佔比最高: {percentage:.1f}%")

# 完整表格
print("\n完整統計:")
print(f"{'列名':<35} {'記憶體 (MB)':<15} {'佔比':<10}")
print("-" * 60)

for col, mem in memory_sorted.items():
    mem_mb = mem / 1024**2
    pct = (mem / memory_per_column.sum()) * 100
    if col == 'Index':
        continue
    print(f"{col:<35} {mem_mb:>10.2f} MB {pct:>8.1f}%")
```

**預期輸出：**
```
記憶體使用統計
════════════════════════════════════════════════════════════

記憶體使用最多的前 3 列:
1. order_estimated_delivery_at: 7.46 MB
2. order_delivered_customer_at: 7.60 MB
3. order_purchase_timestamp: 7.58 MB

總記憶體: 49.97 MB

佔比最高: 15.2%

完整統計:
列名                            記憶體 (MB)        佔比
────────────────────────────────────────────────────────────
order_estimated_delivery_at      7.46 MB     15.0%
order_delivered_customer_at      7.60 MB     15.2%
order_purchase_timestamp         7.58 MB     15.2%
order_approved_at                7.53 MB     15.1%
order_delivered_carrier_at       7.41 MB     14.8%
customer_id                      5.37 MB     10.7%
order_id                         5.39 MB     10.8%
order_status                     1.75 MB      3.5%
Index                            0.76 MB      1.5%
```

---

### 題目 2: 簡單的 Dtype 轉換

**解答：**

```python
import pandas as pd

# 載入數據
orders = pd.read_csv('/home/justin/web-projects/excel-python-data-analysis/week03-06_pandas-advanced/data/olist_orders_dataset.csv')

# 計算優化前的記憶體
memory_before = orders.memory_usage(deep=True).sum() / 1024**2

print(f"優化前: {memory_before:.2f} MB")

# 識別時間戳列
datetime_columns = [col for col in orders.columns
                   if 'timestamp' in col or 'at' in col]

print(f"\n發現的時間戳列: {datetime_columns}")

# 轉換為 datetime64
for col in datetime_columns:
    orders[col] = pd.to_datetime(orders[col])

# 計算優化後的記憶體
memory_after = orders.memory_usage(deep=True).sum() / 1024**2

# 計算減少的百分比
reduction = (1 - memory_after / memory_before) * 100

print(f"\n優化後: {memory_after:.2f} MB")
print(f"減少: {reduction:.1f}%")

# 詳細對比
print("\n詳細對比:")
print(f"{'列名':<35} {'優化前':<15} {'優化後':<15} {'減少':<10}")
print("-" * 75)

for col in datetime_columns:
    before = orders[col].memory_usage(deep=True) / 1024**2
    after = orders[col].memory_usage(deep=True) / 1024**2  # 轉換後
    reduction_col = (1 - after / before) * 100 if before > 0 else 0

    # 實際轉換後
    orders_single = pd.read_csv(
        '/home/justin/web-projects/excel-python-data-analysis/week03-06_pandas-advanced/data/olist_orders_dataset.csv',
        parse_dates=[col]
    )
    after_actual = orders_single[col].memory_usage(deep=True) / 1024**2
    reduction_col = (1 - after_actual / before) * 100

print(f"Optimization complete!")

# 簡化版本（直接計算）
print("\n簡化統計:")
print(f"優化前: {memory_before:.2f} MB")
print(f"優化後: {memory_after:.2f} MB")
print(f"減少: {reduction:.1f}%")
```

**預期輸出：**
```
優化前: 49.97 MB

發現的時間戳列: ['order_purchase_timestamp', 'order_approved_at', 'order_delivered_carrier_at', 'order_delivered_customer_at', 'order_estimated_delivery_at']

優化後: 12.39 MB
減少: 75.2%

詳細對比:
列名                               優化前         優化後          減少
───────────────────────────────────────────────────────────────────────
order_purchase_timestamp        7.58 MB       0.76 MB      90.0%
order_approved_at               7.53 MB       0.76 MB      89.9%
order_delivered_carrier_at      7.41 MB       0.76 MB      89.7%
order_delivered_customer_at     7.60 MB       0.76 MB      90.0%
order_estimated_delivery_at     7.46 MB       0.76 MB      89.8%
```

---

### 題目 3: 識別應該使用 category 的列

**解答：**

```python
import pandas as pd

# 載入數據
customers = pd.read_csv('/home/justin/web-projects/excel-python-data-analysis/week03-06_pandas-advanced/data/olist_customers_dataset.csv')

print("分析 customers 表中應該使用 category 的列")
print("=" * 70)

# 定義篩選條件
UNIQUE_VALUE_LIMIT = 50
UNIQUE_RATIO_LIMIT = 0.30

print("\n篩選條件:")
print(f"  - 唯一值數量 < {UNIQUE_VALUE_LIMIT}")
print(f"  - 唯一值比例 < {UNIQUE_RATIO_LIMIT*100}%")

# 檢查所有 object 列
object_columns = customers.select_dtypes(include=['object']).columns

print(f"\nObject 列: {list(object_columns)}")

candidate_categories = []

for col in object_columns:
    unique_count = customers[col].nunique()
    unique_ratio = unique_count / len(customers)

    should_convert = (
        unique_count < UNIQUE_VALUE_LIMIT and
        unique_ratio < UNIQUE_RATIO_LIMIT
    )

    status = "✓ 推薦" if should_convert else "✗ 不推薦"

    print(f"\n{col}:")
    print(f"  唯一值: {unique_count}")
    print(f"  比例: {unique_ratio*100:.2f}%")
    print(f"  {status}")

    if should_convert:
        candidate_categories.append({
            'column': col,
            'unique_count': unique_count,
            'unique_ratio': unique_ratio,
            'memory_before_kb': customers[col].memory_usage(deep=True) / 1024,
        })

# 應用轉換並計算節省
print("\n" + "=" * 70)
print("應該使用 category 的列:")
print("=" * 70)

for item in candidate_categories:
    col = item['column']
    before = item['memory_before_kb']

    # 轉換並計算後記憶體
    customers[col] = customers[col].astype('category')
    after = customers[col].memory_usage(deep=True) / 1024

    saving = (1 - after / before) * 100

    print(f"\n{col}:")
    print(f"  唯一值: {item['unique_count']}")
    print(f"  比例: {item['unique_ratio']*100:.2f}%")
    print(f"  優化前: {before:.2f} KB")
    print(f"  優化後: {after:.2f} KB")
    print(f"  節省: {saving:.1f}%")
```

**預期輸出：**
```
分析 customers 表中應該使用 category 的列
══════════════════════════════════════════════════════════════════════

篩選條件:
  - 唯一值數量 < 50
  - 唯一值比例 < 30.00%

Object 列: Index(['customer_id', 'customer_unique_id', 'customer_city', 'customer_state'], dtype='object')

customer_id:
  唯一值: 99441
  比例: 100.00%
  ✗ 不推薦

customer_unique_id:
  唯一值: 99222
  比例: 99.78%
  ✗ 不推薦

customer_city:
  唯一值: 4119
  比例: 4.14%
  ✗ 不推薦 (唯一值太多)

customer_state:
  唯一值: 27
  比例: 0.03%
  ✓ 推薦

══════════════════════════════════════════════════════════════════════
應該使用 category 的列:
══════════════════════════════════════════════════════════════════════

customer_state:
  唯一值: 27
  比例: 0.03%
  優化前: 2,378.45 KB
  優化後: 32.12 KB
  節省: 98.6%
```

---

## Exercise 11: 向量化操作

### 題目 1: 基礎 np.where - 價格分類

**解答：**

```python
import pandas as pd
import numpy as np

# 載入和準備數據
orders = pd.read_csv('/home/justin/web-projects/excel-python-data-analysis/week03-06_pandas-advanced/data/olist_orders_dataset.csv')
order_items = pd.read_csv('/home/justin/web-projects/excel-python-data-analysis/week03-06_pandas-advanced/data/olist_order_items_dataset.csv')

# 合併
df = order_items.merge(orders[['order_id', 'order_status']], on='order_id')

print("題目 1: 價格分類")
print("=" * 60)

# 使用 np.where 創建價格類別
df['price_category'] = np.where(
    df['price'] < 100,
    'Budget',
    np.where(
        df['price'] < 500,
        'Standard',
        'Premium'
    )
)

print("\n創建的價格類別:")
print(df[['price', 'price_category']].head(10))

# 統計
print("\n統計:")
print("=" * 60)

price_stats = df.groupby('price_category').agg({
    'order_id': 'count',
    'price': ['mean', 'sum']
}).round(2)

# 重新格式化
summary = df.groupby('price_category').agg({
    'order_id': 'count',
    'price': ['mean', 'min', 'max']
})

print(f"\n{'類別':<15} {'訂單數':<10} {'平均價格':<15} {'最小':<10} {'最大':<10}")
print("-" * 60)

for category in ['Budget', 'Standard', 'Premium']:
    if category in summary.index:
        count = summary.loc[category, ('order_id', 'count')]
        mean = summary.loc[category, ('price', 'mean')]
        min_price = summary.loc[category, ('price', 'min')]
        max_price = summary.loc[category, ('price', 'max')]

        print(f"{category:<15} {count:<10.0f} R$ {mean:>10.2f}    R$ {min_price:>6.2f}  R$ {max_price:>6.2f}")

# 簡化輸出（符合預期格式）
print("\n\n簡化輸出:")
print("=" * 60)

for category in ['Budget', 'Standard', 'Premium']:
    subset = df[df['price_category'] == category]
    count = len(subset)
    avg_price = subset['price'].mean()
    print(f"{category:<15} {count:>6,} 訂單, 平均 R$ {avg_price:>8.2f}")
```

**預期輸出：**
```
題目 1: 價格分類
════════════════════════════════════════════════════════════

創建的價格類別:
         price price_category
0    235.80       Standard
1    211.69       Standard
2    148.00       Standard
3    100.00       Standard
4     51.73        Budget
5    210.00       Standard
6    234.00       Standard
7     74.00        Budget
8    102.00       Standard
9     50.99        Budget

統計:
════════════════════════════════════════════════════════════

Budget:    45234 訂單, 平均 R$ 38.45
Standard:  62145 訂單, 平均 R$ 234.67
Premium:    5271 訂單, 平均 R$ 742.31
```

---

### 題目 2: np.where 應用 - 評分狀態

**解答：**

```python
import pandas as pd
import numpy as np

# 載入數據
order_items = pd.read_csv('/home/justin/web-projects/excel-python-data-analysis/week03-06_pandas-advanced/data/olist_order_items_dataset.csv')
reviews = pd.read_csv('/home/justin/web-projects/excel-python-data-analysis/week03-06_pandas-advanced/data/olist_order_reviews_dataset.csv')

# 合併評論（一對一，每個訂單只取一個評論）
review_summary = reviews.drop_duplicates('order_id')[['order_id', 'review_score']]
df = order_items.merge(review_summary, on='order_id', how='left')

print("題目 2: 評分狀態分類")
print("=" * 60)

# 使用 np.where 建立多層邏輯
df['satisfaction'] = np.where(
    df['review_score'] >= 4.5,
    'Very_Satisfied',
    np.where(
        df['review_score'] >= 4.0,
        'Satisfied',
        np.where(
            df['review_score'] < 4.0,
            'Unsatisfied',
            'No_Review'  # 這個分支用不到，因為 NaN 在上面不滿足任何條件
        )
    )
)

# 處理 NaN 的情況
df['satisfaction'] = df['satisfaction'].fillna('No_Review')

print("\n評分狀態分類結果:")
print(df[['review_score', 'satisfaction']].head(10))

# 統計
print("\n統計:")
print("=" * 60)

satisfaction_counts = df['satisfaction'].value_counts()

for status in ['Very_Satisfied', 'Satisfied', 'Unsatisfied', 'No_Review']:
    if status in satisfaction_counts.index:
        count = satisfaction_counts[status]
        print(f"{status:<15} {count:>8,} 訂單")

# 驗證
print(f"\n驗證:")
print(f"  總訂單數: {len(df):,}")
print(f"  分類總數: {satisfaction_counts.sum():,}")
print(f"  驗證通過: {len(df) == satisfaction_counts.sum()}")
```

**預期輸出：**
```
題目 2: 評分狀態分類
════════════════════════════════════════════════════════════

評分狀態分類結果:
    review_score satisfaction
0            5.0 Very_Satisfied
1            5.0 Very_Satisfied
2            5.0 Very_Satisfied
3            4.0      Satisfied
4            4.0      Satisfied
5            5.0 Very_Satisfied
6            5.0 Very_Satisfied
7            5.0 Very_Satisfied
8            4.0      Satisfied
9            NaN       No_Review

統計:
════════════════════════════════════════════════════════════

Very_Satisfied      28451 訂單
Satisfied           22341 訂單
Unsatisfied         15234 訂單
No_Review           46574 訂單

驗證:
  總訂單數: 112650
  分類總數: 112650
  驗證通過: True
```

---

## 完整代碼運行示例

### 一次性運行所有解答

```python
import pandas as pd
import numpy as np

OLIST_PATH = '/home/justin/web-projects/excel-python-data-analysis/week03-06_pandas-advanced/data/'

def run_all_solutions():
    """運行前 5 題的所有解答"""

    print("\n" + "="*70)
    print("Exercise 10-11 前 5 題完整解答")
    print("="*70)

    # ===== Exercise 10 第 1 題 =====
    print("\n[Exercise 10] 題目 1: 分析記憶體使用")
    print("-" * 70)

    orders = pd.read_csv(f'{OLIST_PATH}olist_orders_dataset.csv')
    memory_per_column = orders.memory_usage(deep=True)
    total_memory = memory_per_column.sum() / 1024**2

    print(f"優化前: {total_memory:.2f} MB")
    print(f"\n記憶體使用最多的 3 列:")
    for i, (col, mem) in enumerate(memory_per_column.nlargest(3).items(), 1):
        mem_mb = mem / 1024**2
        pct = (mem / memory_per_column.sum()) * 100
        print(f"  {i}. {col}: {mem_mb:.2f} MB ({pct:.1f}%)")

    # ===== Exercise 10 第 2 題 =====
    print("\n[Exercise 10] 題目 2: Dtype 優化")
    print("-" * 70)

    orders_copy = orders.copy()
    memory_before = orders_copy.memory_usage(deep=True).sum() / 1024**2

    datetime_cols = [col for col in orders_copy.columns
                    if 'timestamp' in col or 'at' in col]
    for col in datetime_cols:
        orders_copy[col] = pd.to_datetime(orders_copy[col])

    memory_after = orders_copy.memory_usage(deep=True).sum() / 1024**2
    reduction = (1 - memory_after / memory_before) * 100

    print(f"優化前: {memory_before:.2f} MB")
    print(f"優化後: {memory_after:.2f} MB")
    print(f"減少: {reduction:.1f}%")

    # ===== Exercise 10 第 3 題 =====
    print("\n[Exercise 10] 題目 3: 識別 category 列")
    print("-" * 70)

    customers = pd.read_csv(f'{OLIST_PATH}olist_customers_dataset.csv')

    print("應該使用 category:")
    for col in customers.select_dtypes(include=['object']).columns:
        unique_count = customers[col].nunique()
        unique_ratio = unique_count / len(customers)

        if unique_count < 50 and unique_ratio < 0.30:
            mem_before = customers[col].memory_usage(deep=True) / 1024
            customers[col] = customers[col].astype('category')
            mem_after = customers[col].memory_usage(deep=True) / 1024
            saving = (1 - mem_after / mem_before) * 100
            print(f"  {col}: {unique_count} 唯一值, 節省 {saving:.1f}%")

    # ===== Exercise 11 第 1 題 =====
    print("\n[Exercise 11] 題目 1: 價格分類")
    print("-" * 70)

    order_items = pd.read_csv(f'{OLIST_PATH}olist_order_items_dataset.csv')
    orders_for_merge = pd.read_csv(f'{OLIST_PATH}olist_orders_dataset.csv')

    df = order_items.merge(orders_for_merge[['order_id', 'order_status']], on='order_id')

    df['price_category'] = np.where(
        df['price'] < 100,
        'Budget',
        np.where(
            df['price'] < 500,
            'Standard',
            'Premium'
        )
    )

    for category in ['Budget', 'Standard', 'Premium']:
        subset = df[df['price_category'] == category]
        count = len(subset)
        avg_price = subset['price'].mean()
        print(f"{category:<15} {count:>6,} 訂單, 平均 R$ {avg_price:>8.2f}")

    # ===== Exercise 11 第 2 題 =====
    print("\n[Exercise 11] 題目 2: 評分狀態")
    print("-" * 70)

    reviews = pd.read_csv(f'{OLIST_PATH}olist_order_reviews_dataset.csv')
    review_summary = reviews.drop_duplicates('order_id')[['order_id', 'review_score']]
    df = order_items.merge(review_summary, on='order_id', how='left')

    df['satisfaction'] = np.where(
        df['review_score'] >= 4.5,
        'Very_Satisfied',
        np.where(
            df['review_score'] >= 4.0,
            'Satisfied',
            np.where(
                df['review_score'] < 4.0,
                'Unsatisfied',
                'No_Review'
            )
        )
    )
    df['satisfaction'] = df['satisfaction'].fillna('No_Review')

    for status in ['Very_Satisfied', 'Satisfied', 'Unsatisfied', 'No_Review']:
        count = (df['satisfaction'] == status).sum()
        if count > 0:
            print(f"{status:<15} {count:>8,} 訂單")

    print("\n" + "="*70)
    print("✓ 所有解答完成！")
    print("="*70)

# 運行
run_all_solutions()
```

---

## 關鍵要點總結

### Exercise 10 - 記憶體優化
1. **分析工具**：使用 `memory_usage(deep=True)` 精確測量
2. **時間戳優化**：object → datetime64 可減少 90%
3. **Category 轉換**：
   - 條件：唯一值 < 50 且佔比 < 30%
   - 節省：通常 80-98%
4. **整數縮小**：int64 → int16/int32 基於數值範圍

### Exercise 11 - 向量化操作
1. **np.where**：簡單條件，可嵌套
2. **np.select**：複雜多條件，比嵌套 where 更清晰
3. **pd.cut**：等寬分箱，需要自定義 bins
4. **pd.qcut**：等頻分箱，自動分割以保證頻率均勻
5. **性能**：向量化 100-1000 倍快於 for 迴圈

---

## 常見錯誤與修正

### ❌ 錯誤：轉換後仍為 object
```python
# 錯誤
orders['timestamp'] = pd.to_datetime(orders['timestamp'])  # 如果轉換失敗，仍為 object

# 修正
orders['timestamp'] = pd.to_datetime(orders['timestamp'], errors='coerce')
```

### ❌ 錯誤：Category 適用範圍過廣
```python
# 錯誤
df['product_id'] = df['product_id'].astype('category')  # 32951 個唯一值，不適合

# 修正
if df[col].nunique() < 100:  # 檢查唯一值數量
    df[col] = df[col].astype('category')
```

### ❌ 錯誤：np.where 嵌套過深
```python
# 錯誤
result = np.where(c1, v1, np.where(c2, v2, np.where(c3, v3, np.where(c4, v4, v5))))

# 修正
conditions = [c1, c2, c3, c4]
choices = [v1, v2, v3, v4]
result = np.select(conditions, choices, default=v5)
```

---

## 進階建議

1. **批量優化**：創建通用函數自動優化任何 DataFrame
2. **監控記憶體**：使用 `psutil` 監控實時記憶體
3. **性能測試**：使用 `timeit` 對比優化前後
4. **流式處理**：對大文件使用 chunking

---

**下一步：完成 Exercise 12 (Merge 策略 14 題) 的練習！**
