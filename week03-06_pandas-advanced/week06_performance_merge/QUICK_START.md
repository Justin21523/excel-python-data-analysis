# QUICK START: 5 分鐘上手 Week 6

## 📋 前置檢查

```python
# 1. 檢查環境
import pandas as pd
import numpy as np
print(f"✓ Pandas {pd.__version__}")
print(f"✓ NumPy {np.__version__}")

# 2. 檢查數據
import os
data_path = '/home/justin/web-projects/excel-python-data-analysis/week03-06_pandas-advanced/data/'
print(f"✓ 找到 {len(os.listdir(data_path))} 個數據文件")
```

---

## 🎯 3 分鐘速成

### 記憶體優化 (Day 13)

**核心技能：** 減少 80%+ 的記憶體使用

```python
import pandas as pd
import numpy as np

orders = pd.read_csv('.../olist_orders_dataset.csv')

# 1. 分析記憶體
print(orders.memory_usage(deep=True).sum() / 1024**2)  # MB

# 2. 轉換時間戳 (省 90%)
orders['order_purchase_timestamp'] = pd.to_datetime(
    orders['order_purchase_timestamp']
)

# 3. 轉換 Category (省 95%)
orders['order_status'] = orders['order_status'].astype('category')

# 4. 檢驗結果
print(orders.memory_usage(deep=True).sum() / 1024**2)  # 更小！
```

**期望結果：** 49.97 MB → 3.82 MB (92.4% ↓)

---

### 向量化操作 (Day 14)

**核心技能：** 100x+ 性能提升，零迴圈

```python
import pandas as pd
import numpy as np

df = pd.read_csv('.../olist_order_items_dataset.csv')

# ❌ 不要這樣（太慢！）
# for idx, row in df.iterrows():
#     if row['price'] < 100:
#         category = 'Low'

# ✓ 這樣做（1000x 快）
df['price_category'] = np.where(
    df['price'] < 100,
    'Low',
    np.where(
        df['price'] < 500,
        'Medium',
        'High'
    )
)

print(df['price_category'].value_counts())
```

**期望結果：** 毫秒級完成 112,650 行

---

### Merge 策略 (Day 15)

**核心技能：** 高效整合多個表

```python
import pandas as pd

orders = pd.read_csv('.../olist_orders_dataset.csv')
customers = pd.read_csv('.../olist_customers_dataset.csv')

# ✓ LEFT JOIN (最常用)
result = orders.merge(
    customers,
    on='customer_id',
    how='left'
)

# ✓ 驗證數據完整性
print(result['customer_city'].isna().sum())  # 應該 = 0

# ✓ 檢查關係
result = orders.merge(
    customers,
    on='customer_id',
    how='left',
    validate='m:1'  # 多個訂單對應一個客戶
)
```

**期望結果：** 99,441 行 × 13 列

---

## 🏃 10 分鐘完整練習

### 練習 1：完整的記憶體優化 Pipeline

```python
def optimize_all():
    import pandas as pd
    import numpy as np

    # 加載
    orders = pd.read_csv('.../olist_orders_dataset.csv')
    customers = pd.read_csv('.../olist_customers_dataset.csv')

    print("優化前:")
    total_before = (
        orders.memory_usage(deep=True).sum() +
        customers.memory_usage(deep=True).sum()
    ) / 1024**2
    print(f"  總記憶體: {total_before:.2f} MB")

    # 優化 orders
    for col in orders.columns:
        if 'timestamp' in col or 'at' in col:
            orders[col] = pd.to_datetime(orders[col])
    orders['order_status'] = orders['order_status'].astype('category')

    # 優化 customers
    customers['customer_state'] = customers['customer_state'].astype('category')
    customers['customer_city'] = customers['customer_city'].astype('category')

    print("\n優化後:")
    total_after = (
        orders.memory_usage(deep=True).sum() +
        customers.memory_usage(deep=True).sum()
    ) / 1024**2
    print(f"  總記憶體: {total_after:.2f} MB")

    reduction = (1 - total_after / total_before) * 100
    print(f"\n減少: {reduction:.1f}% ✓")

    return orders, customers

# 執行
opt_orders, opt_customers = optimize_all()
```

### 練習 2：向量化複雜邏輯

```python
import pandas as pd
import numpy as np

# 準備數據
order_items = pd.read_csv('.../olist_order_items_dataset.csv')
reviews = pd.read_csv('.../olist_order_reviews_dataset.csv')

df = order_items.merge(reviews[['order_id', 'review_score']], on='order_id', how='left')

# 複雜規則（全部向量化）
# 規則：根據價格和評分決定是否需要跟進
df['needs_followup'] = np.select(
    [
        (df['price'] > 500) & (df['review_score'] < 4),
        (df['price'] > 500) & (df['review_score'].isna()),
        (df['price'].between(100, 500)) & (df['review_score'] < 3),
    ],
    [
        'High_Value_Issue',
        'High_Value_NoReview',
        'Medium_Issue',
    ],
    default='No_Action'
)

# 統計
print(df['needs_followup'].value_counts())
```

### 練習 3：多表高效合併

```python
import pandas as pd

# 加載數據
orders = pd.read_csv('.../olist_orders_dataset.csv')
customers = pd.read_csv('.../olist_customers_dataset.csv')
order_items = pd.read_csv('.../olist_order_items_dataset.csv')
products = pd.read_csv('.../olist_products_dataset.csv')

print("合併流程:")

# 第 1 步
df = orders.merge(customers, on='customer_id', how='left')
print(f"1. orders + customers: {len(df):,} 行")

# 第 2 步
df = df.merge(order_items, on='order_id', how='left')
print(f"2. + order_items: {len(df):,} 行")

# 第 3 步
df = df.merge(products[['product_id', 'product_category_name']],
              on='product_id', how='left')
print(f"3. + products: {len(df):,} 行")

# 驗證
print(f"\n最終列數: {len(df.columns)}")
print(f"缺失值: {df.isnull().sum().sum()}")

print("\n✓ 多表合併完成！")
```

---

## 📊 預期結果對比

### 記憶體優化
```
orders          49.97 MB → 3.82 MB  (92.4% ↓)
customers        6.18 MB → 4.95 MB  (19.9% ↓)
─────────────────────────────────────────────
總計             77.14 MB → 12.49 MB (83.8% ↓)
```

### 向量化性能
```
For Loop:        28.47 秒 (99,441 行)
np.where:         0.0045 秒
性能提升:         6,326 倍 ✓
```

### Merge 耗時
```
orders + customers:   0.01s ✓
+ order_items:        0.05s ✓
+ reviews:            0.08s ✓
+ products:           0.10s ✓
總計:                 0.24s ✓
```

---

## 🎓 接下來做什麼

### 短期 (今天完成)

1. **✓ 完成 3 個練習** (30 分鐘)
2. **開始 Exercise 10** (第 1-3 題) (1 小時)
3. **開始 Exercise 11** (第 1-3 題) (1 小時)

### 中期 (本周完成)

1. 完成所有 32 題練習 (2-3 天)
2. 完成 Day 16 挑戰 (1 天)
3. 在自己的項目上應用 (1 天)

### 長期 (進階學習)

1. 使用 Dask 處理更大數據
2. 探索 Polars（更快的 DataFrame）
3. 參考自己的數據集進行優化

---

## 🔍 診斷你的瓶頸

### 記憶體問題？

```python
# 檢查
import pandas as pd

df = pd.read_csv('...')
print(df.memory_usage(deep=True))

# 看哪列最耗內存？通常是：
# 1. object (字符串)
# 2. datetime (時間戳存儲為字符串)
```

**解決方案：** 閱讀 Day 13

### 代碼太慢？

```python
# 檢查
import time

start = time.time()
# 你的代碼
elapsed = time.time() - start

# 如果 > 1 秒，可能用了 for 迴圈
```

**解決方案：** 閱讀 Day 14 + 使用 np.where

### 多表操作複雜？

```python
# 檢查
# 如果需要合併 3+ 個表
# 或者 join 關係複雜
```

**解決方案：** 閱讀 Day 15 + Exercise 12

---

## ❌ 常見陷阱 (避免)

### 陷阱 1: 忘記 deep=True

```python
# ❌ 不完整
df.memory_usage()  # 只計算索引

# ✓ 正確
df.memory_usage(deep=True)  # 計算所有內容
```

### 陷阱 2: For 迴圈

```python
# ❌ 太慢！
for idx, row in df.iterrows():
    if row['price'] < 100:
        category = 'Low'

# ✓ 用向量化
df['category'] = np.where(df['price'] < 100, 'Low', 'High')
```

### 陷阱 3: 忽視 Merge 驗證

```python
# ❌ 危險
df = orders.merge(customers, on='customer_id')

# ✓ 安全
df = orders.merge(customers, on='customer_id', how='left', validate='m:1')
assert df['customer_city'].notna().all()
```

---

## 💬 常見問題 Quick FAQ

**Q: 我應該先讀什麼？**
A: 按順序：Day 13 → Day 14 → Day 15 → Day 16

**Q: 需要跳過任何部分嗎？**
A: 不建議。但如果時間緊，至少要讀 Day 13 + 14

**Q: 練習有答案嗎？**
A: Solutions_Complete.md 有前 5 題的答案。教學文件有案例參考。

**Q: 我可以在自己的數據上試嗎？**
A: 可以！用同樣的方法。記得測試和驗證。

**Q: 性能一定會提升 100 倍嗎？**
A: 如果你從 for 迴圈改為向量化，是的。改進優化空間取決於代碼。

---

## ✅ 自檢清單

在開始之前，確認你能做到：

- [ ] 導入 pandas, numpy 無誤
- [ ] 找到 Olist 數據文件
- [ ] 運行上面的 3 個練習
- [ ] 看到了性能提升
- [ ] 理解了為什麼需要優化

如果都✓了，**你已經準備好了！**

---

## 🚀 立即開始

### 選項 1：按教學順序 (推薦)
```
QUICK_START (你在這裡)
    ↓
Day 13 (記憶體優化)
    ↓
Day 14 (向量化)
    ↓
Day 15 (Merge)
    ↓
Day 16 (實踐)
```

### 選項 2：跟著練習走
```
Exercise 10 (記憶體 8 題)
    ↓
Exercise 11 (向量化 10 題)
    ↓
Exercise 12 (Merge 14 題)
    ↓
Solutions (查看答案)
```

### 選項 3：混合學習 (最有效)
```
讀 Day 13 (1h) + 做 Exercise 10 (1h)
    ↓
讀 Day 14 (1h) + 做 Exercise 11 (1.5h)
    ↓
讀 Day 15 (1h) + 做 Exercise 12 (1.5h)
    ↓
讀 Day 16 (1h) + 完成項目 (2h)
```

---

**選擇你的路徑，現在開始！**

👉 [進入 Day 13](Day13_Memory_Optimization_Guide.md)
