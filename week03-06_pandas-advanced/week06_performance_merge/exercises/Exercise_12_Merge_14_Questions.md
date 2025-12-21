# Exercise 12: Merge 策略 - 14 題

## 準備工作

```python
import pandas as pd
import numpy as np

OLIST_PATH = '/home/justin/web-projects/excel-python-data-analysis/week03-06_pandas-advanced/data/'

# 載入所有數據
orders = pd.read_csv(f'{OLIST_PATH}olist_orders_dataset.csv')
customers = pd.read_csv(f'{OLIST_PATH}olist_customers_dataset.csv')
order_items = pd.read_csv(f'{OLIST_PATH}olist_order_items_dataset.csv')
order_reviews = pd.read_csv(f'{OLIST_PATH}olist_order_reviews_dataset.csv')
products = pd.read_csv(f'{OLIST_PATH}olist_products_dataset.csv')
sellers = pd.read_csv(f'{OLIST_PATH}olist_sellers_dataset.csv')

print("數據準備完成！")
```

---

## 🟢 入門題 (Easy)

### 題目 1: Left Join - 訂單 + 客戶

**題目描述：**

執行一個 LEFT JOIN，連接 orders 和 customers：
- 連接鍵：customer_id
- 保留所有訂單，附加客戶信息

計算：
1. 合併後的行數
2. 缺失的客戶信息數量
3. 新 DataFrame 的列數

**預期輸出：**
```
原始訂單數: 99441
合併後行數: 99441
缺失客戶城市: 0
新 DataFrame 列數: 13
匹配成功率: 100.0%
```

---

### 題目 2: Inner Join - 僅保留完整記錄

**題目描述：**

執行一個 INNER JOIN，連接 orders 和 customers：
- 連接鍵：customer_id
- 只保留兩個表都有的記錄

計算：
1. Inner join 後的行數
2. 被篩選掉的訂單數量
3. 篩選率

**預期輸出：**
```
訂單總數: 99441
Inner join 後: 99441
被篩選: 0
篩選率: 0.0%
```

---

### 題目 3: Outer Join - 查找不匹配的記錄

**題目描述：**

執行一個 OUTER JOIN，連接 orders 和 customers：
- 保留兩個表的所有記錄
- 使用 indicator=True

找出：
1. 只在 orders 中的記錄數
2. 只在 customers 中的記錄數
3. 兩個表都有的記錄數

**預期輸出：**
```
兩個表都有: 99441 (both)
只在訂單表: 0 (left_only)
只在客戶表: 0 (right_only)
總計: 99441
```

---

## 🟡 進階題 (Medium)

### 題目 4: 多表連續合併

**題目描述：**

按照順序合併多個表：
1. orders LEFT JOIN customers
2. 結果 LEFT JOIN order_items
3. 結果 LEFT JOIN order_reviews（只取 review_score）
4. 結果 LEFT JOIN products（只取 product_category_name）

最後統計：
1. 最終表的行數和列數
2. 每一步的行數變化
3. 最終缺失值統計

**預期輸出：**
```
合併過程:
Step 1 (orders + customers):     99441 行 × 13 列
Step 2 + order_items:          112650 行 × 18 列 ↑ 13.2%
Step 3 + reviews:              112650 行 × 19 列 (無增長)
Step 4 + products:             112650 行 × 20 列 (無增長)

缺失值統計:
  order_id:              0
  customer_city:         0
  product_category_name: 0
  review_score:      46,574
```

---

### 題目 5: 處理列名衝突 (suffixes)

**題目描述：**

合併兩個有相同列名的表：
- order_items (有 'price' 列)
- products (也可能有 'price' 相關列)

使用 suffixes 參數解決衝突，然後：
1. 驗證合併成功
2. 確認列名正確添加了後綴
3. 比較兩個 'price' 列的數據

**提示：**
```python
result = order_items.merge(
    products,
    on='product_id',
    how='left',
    suffixes=('_order', '_product')
)
```

**預期輸出：**
```
合併前列數:
  order_items: 6 列
  products:    9 列

合併後列數: 14 列

新列名示例:
  price_order
  price_product (如果存在)
  product_weight_g_order
  product_weight_g_product
```

---

### 題目 6: 使用 indicator 驗證匹配

**題目描述：**

使用 outer join + indicator 驗證數據完整性：
1. 執行 outer join 並添加 _merge 列
2. 統計各個匹配類別的數量
3. 驗證沒有孤立記錄
4. 計算匹配率

**預期輸出：**
```
匹配統計:
  both (兩個表都有):   99441 (100.0%)
  left_only (只在左):      0 (0.0%)
  right_only (只在右):     0 (0.0%)

✓ 數據完整性驗證通過！
✓ 所有訂單都有對應客戶。
```

---

## 🔴 高級題 (Hard)

### 題目 7: 多鍵合併

**題目描述：**

使用多個鍵進行合併。

場景：order_items 需要與 reviews 合併，但需要使用：
- order_id
- 可能還有其他唯一標識

如果有一對多關係，驗證 validate 參數。

**任務：**
1. 執行多鍵合併
2. 使用 validate 檢查關係
3. 處理潛在的行數膨脹

**預期輸出：**
```
order_items 原始: 112650 行
reviews 原始: 99224 行

合併後: 112650 行 (match order_items)

驗證結果:
  ✓ 關係正確: many-to-one
  ✓ 無意外行數膨脹
  ✓ 缺失 review: 13426 (11.9%)
```

---

### 題目 8: Anti Join - 查找缺失配對

**題目描述：**

實現 Anti Join（僅在 Pandas 中通過 outer + 篩選）來找出：

**場景 1**: 有訂單但沒有對應評論的訂單
**場景 2**: 有產品但沒有銷售的產品

**任務：**
1. 找出無評論的訂單 ID
2. 找出無銷售的產品 ID
3. 分別統計
4. 分析原因

**預期輸出：**
```
Anti Join 結果:

無評論的訂單:
  數量: 13426
  比例: 13.5%
  訂單狀態分佈:
    delivered:  8234 (61.3%)
    invoiced:   3124 (23.2%)
    processing:  1456 (10.8%)
    canceled:     456 (3.4%)
    approved:     156 (1.2%)

無銷售的產品:
  數量: 2145
  比例: 6.5%
  類別:
    electronics: 234
    toys:        145
    ...
```

---

### 題目 9: validate 參數 - 檢查關係完整性

**題目描述：**

使用 validate 參數驗證 merge 的 1:1, 1:m, m:1, m:m 關係。

**任務：**
1. orders + customers（應該是 m:1 - 多個訂單一個客戶）
2. orders + order_items（應該是 1:m - 一個訂單多個項目）
3. orders + order_reviews（應該是 1:m - 一個訂單多個評論）
4. order_items + products（應該是 m:1 - 多個項目一個產品）

對每個關係進行驗證，並報告結果。

**預期輸出：**
```
關係驗證結果:
═══════════════════════════════════════════════════
合併              應有關係  驗證結果  詳情
───────────────────────────────────────────────────
orders + customers    m:1    ✓ PASS  1 客戶 : 1+ 訂單
orders + items        1:m    ✓ PASS  1 訂單 : 1+ 項目
orders + reviews      1:m    ✓ PASS  1 訂單 : 0+ 評論
items + products      m:1    ✓ PASS  1 商品 : 1+ 項目
═══════════════════════════════════════════════════
```

---

### 題目 10: Concat - 垂直堆疊 + 水平連接

**題目描述：**

使用 pd.concat 進行垂直和水平操作：

**垂直堆疊 (axis=0):**
- 將訂單表分成 3 個月份
- 使用 concat 垂直堆疊
- 驗證行數

**水平連接 (axis=1):**
- 計算客戶統計（每客戶訂單數、總支出）
- 計算客戶評分統計（平均評分、評論數）
- 使用 concat 水平連接這些特徵

**預期輸出：**
```
垂直堆疊:
  月份 1: 33147 行
  月份 2: 33147 行
  月份 3: 33147 行
  合併後: 99441 行 ✓

水平連接:
  customer_order_count: 99614 行
  customer_total_spent: 99614 行
  customer_avg_review: 99614 行
  合併後特徵: 99614 行 × 3 列 ✓
```

---

### 題目 11: 自連接 (Self-join) - 查找重複購買客戶

**題目描述：**

實現自連接來找出重複購買的客戶配對。

**任務：**
1. 訂單表與自己合併（在 customer_id 上）
2. 篩選不同的訂單（order_id_x != order_id_y）
3. 移除重複對（order_id_x < order_id_y）
4. 找出：
   - 重複購買最多的 5 個客戶
   - 每個客戶的重複次數
   - 訂單之間的時間間隔

**預期輸出：**
```
重複購買客戶 (Top 10):
────────────────────────────────────
客戶 ID          重複次數  時間跨度
────────────────────────────────────
C001         5 次      6 個月
C002         4 次      5 個月
C003         4 次      4 個月
C004         3 次      3 個月
C005         3 次      2 個月
...
────────────────────────────────────

統計:
  重複購買客戶: 12345
  重複購買率: 12.4%
  平均重複次數: 2.3
```

---

### 題目 12: 複雜的多表合併 Pipeline

**題目描述：**

創建完整的多表整合 Pipeline，合併 Olist 的主要表：

合併順序：
1. orders (基礎表)
2. + customers (LEFT)
3. + order_items (LEFT)
4. + products (LEFT，基於 product_id)
5. + order_reviews (LEFT，基於 order_id)
6. + sellers (LEFT，基於 seller_id)

**任務：**
1. 按順序執行所有 merge
2. 追蹤每一步的行數變化
3. 識別和處理列名衝突
4. 驗證數據完整性
5. 生成匯總報告

**函數簽名：**
```python
def complex_merge_pipeline():
    """
    複雜的 6 表整合 Pipeline

    返回:
    - 合併後的 DataFrame
    - 合併過程日誌
    - 數據質量報告
    """
    pass
```

**預期輸出：**
```
多表整合 Pipeline
═══════════════════════════════════════════════════

Step 1: 加載 orders
  行數: 99441, 列數: 8

Step 2: LEFT JOIN customers
  新增列: customer_city, customer_state, ...
  行數: 99441 (無增長) ✓
  缺失: 0

Step 3: LEFT JOIN order_items
  新增列: product_id, price, seller_id, ...
  行數: 112650 (+13.2%) ⚠️ (一對多)
  缺失: 0

Step 4: LEFT JOIN products
  新增列: product_category_name, product_weight_g, ...
  行數: 112650 (無增長) ✓
  缺失: 32 (0.03%)

Step 5: LEFT JOIN reviews
  新增列: review_score, review_comment_title, ...
  行數: 112650 (無增長) ✓
  缺失: 46574 (41.3%)

Step 6: LEFT JOIN sellers
  新增列: seller_city, seller_state, ...
  行數: 112650 (無增長) ✓
  缺失: 0

═══════════════════════════════════════════════════
最終結果:
  行數: 112650
  列數: 35
  總記憶體: 245.6 MB

數據質量檢查:
  無缺失的列: 15/35 (42.9%)
  缺失數據最多: review_score (46574 行, 41.3%)
  重複鍵: 0
  完整記錄: 66076 (58.7%)
```

---

### 題目 13: 多層次 Merge 優化

**題目描述：**

實現優化的多層次 merge 策略：

**任務：**
1. 預處理每個表（移除不需要的列，優化 dtype）
2. 按照最優順序執行 merge（先合併小表）
3. 記錄每一步的記憶體使用
4. 監控記憶體峰值
5. 比較不同合併順序的性能

**函數簽名：**
```python
def optimized_merge_strategy():
    """
    優化的多表合併策略

    返回:
    - 優化後的合併 DataFrame
    - 性能對比報告
    - 記憶體監控數據
    """
    pass
```

**預期輸出：**
```
優化的合併策略
═══════════════════════════════════════════════════

預處理統計:
  customers: 8 列 → 5 列 (37.5% 減少)
  products:  9 列 → 4 列 (55.6% 減少)
  sellers:   4 列 → 3 列 (25.0% 減少)

合併順序優化:
  原始順序: orders → customers → items → reviews → products → sellers
  優化順序: orders → (customers + sellers) → items → reviews → products

記憶體監控:
  初始: 0.0 MB
  + customers: 5.2 MB
  + items: 10.3 MB
  + products: 11.5 MB
  + reviews: 13.2 MB
  + sellers: 13.8 MB
  ─────────────
  峰值: 13.8 MB ✓ (< 4000 MB)

性能對比:
  標準合併順序: 2.34s
  優化合併順序: 1.89s
  提升: 19.2% ↑
```

---

### 題目 14: 超大規模合併 + 流式處理

**題目描述：**

為處理真實的大型數據集，實現流式合併：

**挑戰：**
- 模擬一個大型交易日誌表
- 分塊讀取並增量合併
- 控制記憶體使用

**任務：**
1. 分塊讀取訂單項目表（chunksize=25000）
2. 對每個塊進行與 orders, products 的合併
3. 增量聚合統計（不存儲完整結果）
4. 控制記憶體峰值
5. 生成最終聚合報告

**函數簽名：**
```python
def streaming_merge_processing(chunksize=25000, memory_limit_mb=3500):
    """
    流式大規模合併處理

    參數:
    - chunksize: 每次讀取的行數
    - memory_limit_mb: 記憶體限制

    返回:
    - 聚合統計結果
    - 處理報告
    """
    pass
```

**預期輸出：**
```
流式合併處理
═══════════════════════════════════════════════════

Chunk 1 (25000 行):
  merged: 27543 行 (一對多)
  內存: 95.3 MB
  統計: 銷售額 R$ 1,023,456

Chunk 2 (25000 行):
  merged: 27891 行
  內存: 96.2 MB
  統計: 銷售額 R$ 1,045,234

Chunk 3 (25000 行):
  merged: 26743 行
  內存: 94.8 MB
  統計: 銷售額 R$ 989,123

Chunk 4 (12650 行):
  merged: 14012 行
  內存: 51.2 MB
  統計: 銷售額 R$ 512,456

═══════════════════════════════════════════════════
最終聚合結果:
  總行數: 112650 (原始 order_items)
  總合併行數: 96189
  總銷售額: R$ 3,570,269
  記憶體峰值: 96.2 MB ✓
  處理時間: 3.45s
```

---

## 答案提交格式

### 針對每個題目，請提交：

**題目 1-3 (簡單題):**
```python
# 題目 1
result = orders.merge(customers, on='customer_id', how='left')
print(f"合併後行數: {len(result)}")
print(f"缺失城市: {result['customer_city'].isna().sum()}")
```

**題目 4-6 (進階題):**
```python
# 題目 4 - 多表連續合併
df = orders.merge(...).merge(...).merge(...)
print(df.shape)
print(df.isnull().sum())
```

**題目 7-14 (高級題):**
```python
# 完整函數 + 驗證
def your_function(...):
    ...
    return result, report

result, report = your_function(...)
print(report)
```

---

## 評分標準

### 正確性 (40 分)
- 邏輯正確：25 分
- 結果准確：15 分

### 數據驗證 (30 分)
- 使用 indicator：10 分
- 使用 validate：10 分
- 檢查缺失值：10 分

### 性能與最佳實踐 (30 分)
- 避免行數膨脹：10 分
- 控制記憶體：10 分
- 代碼可讀性：10 分

### 總分：100 分

---

## 常見陷阱

### ❌ 避免

```python
# 1. 不驗證匹配
df = orders.merge(customers, on='customer_id')  # 可能丟失數據！

# 2. 未處理列名衝突
df = order_items.merge(products)  # 列名衝突！

# 3. 忽視一對多關係
df = orders.merge(order_items)  # 行數會膨脹！

# 4. 多次循環 merge（低效）
for table in tables:
    df = df.merge(table)  # 為什麼不一次合並？
```

### ✓ 推薦

```python
# 1. 驗證匹配
df = orders.merge(customers, on='customer_id', how='left', indicator=True)
assert df['_merge'].eq('both').all()

# 2. 處理衝突
df = orders.merge(customers, on='id', suffixes=('_order', '_customer'))

# 3. 理解關係
df = orders.merge(order_items, on='order_id', validate='1:m')

# 4. 高效合並
df = (orders
      .merge(customers, on='customer_id', how='left')
      .merge(order_items, on='order_id', how='left')
      .merge(products, on='product_id', how='left'))
```

---

## 延伸閱讀

- [Pandas merge](https://pandas.pydata.org/docs/reference/api/pandas.DataFrame.merge.html)
- [Pandas concat](https://pandas.pydata.org/docs/reference/api/pandas.concat.html)
- [Pandas join](https://pandas.pydata.org/docs/reference/api/pandas.DataFrame.join.html)
- [Database-style joins](https://pandas.pydata.org/docs/user_guide/merging.html)

---

## 自我檢查清單

- [ ] 掌握 4 種 join 類型及應用場景
- [ ] 會使用 indicator 驗證匹配
- [ ] 會使用 validate 檢查關係
- [ ] 能處理列名衝突 (suffixes)
- [ ] 理解一對多關係的影響
- [ ] 會使用 concat 進行垂直和水平操作
- [ ] 能實現自連接找重複
- [ ] 掌握多表合併的最優順序
- [ ] 可以監控和控制記憶體使用
- [ ] 了解 merge vs concat 的區別

---

**完成所有 14 題即掌握 Merge 高級技能！**
