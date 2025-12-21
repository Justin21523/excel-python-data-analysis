# 📊 Olist 巴西電商資料集完整使用指南

## 📋 資料集總覽

**Olist Brazilian E-Commerce Dataset**

- **來源：** Kaggle
- **大小：** 121 MB
- **時間範圍：** 2016-09-04 至 2018-10-17
- **訂單數：** 99,441 筆
- **客戶數：** 99,441 個（獨立客戶 96,096 個）
- **商品數：** 32,951 個
- **賣家數：** 3,095 個
- **表數：** 9 張表

**資料集特色：**
- ✅ 真實電商資料（脫敏處理）
- ✅ 完整商業流程（下單 → 付款 → 配送 → 評價）
- ✅ 多維度資訊（客戶、商品、賣家、地理、時間）
- ✅ 適合練習 pandas 進階技能

---

## 🗂️ 資料集結構

### 資料表關係圖

```
核心流程：
orders (訂單主表)
  └─ order_id (PK)
      ├─ order_items (訂單明細) ← product_id → products (商品)
      ├─ order_payments (付款)
      ├─ order_reviews (評論)
      └─ customer_id → customers (客戶)

賣家與地理：
sellers (賣家)
  ├─ seller_id (FK in order_items)
  └─ seller_zip_code_prefix → geolocation (地理位置)

類別翻譯：
product_category_name_translation (類別翻譯)
  └─ product_category_name (FK in products)
```

### 表之間的連接關係

| 左表 | 右表 | 連接鍵 | 關係 |
|-----|-----|--------|------|
| orders | customers | customer_id | 1:1 |
| orders | order_items | order_id | 1:N |
| order_items | products | product_id | N:1 |
| order_items | sellers | seller_id | N:1 |
| orders | order_payments | order_id | 1:N |
| orders | order_reviews | order_id | 1:1 |
| products | category_translation | product_category_name | N:1 |
| sellers/customers | geolocation | zip_code_prefix | N:N |

---

## 📁 9 張表詳細說明

### 1. olist_orders_dataset.csv（訂單主表）⭐

**筆數：** 99,441
**主鍵：** `order_id`
**說明：** 訂單的核心資訊，包含訂單狀態、時間戳記

#### 欄位說明

| 欄位名稱 | 型別 | 說明 | 範例 |
|---------|------|------|------|
| `order_id` | string | 訂單唯一識別碼（主鍵） | `e481f51cbdc54678b7cc49136f2d6af7` |
| `customer_id` | string | 客戶 ID | `9ef432eb6251297304e76186b10a928d` |
| `order_status` | string | 訂單狀態 | `delivered`, `shipped`, `canceled` 等 |
| `order_purchase_timestamp` | datetime | 下單時間 | `2017-10-02 10:56:33` |
| `order_approved_at` | datetime | 訂單批准時間 | `2017-10-02 11:07:15` |
| `order_delivered_carrier_date` | datetime | 交給物流時間 | `2017-10-04 19:55:00` |
| `order_delivered_customer_date` | datetime | 送達客戶時間 | `2017-10-10 21:25:13` |
| `order_estimated_delivery_date` | datetime | 預計送達時間 | `2017-10-18 00:00:00` |

#### 訂單狀態值

| 狀態 | 說明 | 筆數 |
|------|------|------|
| `delivered` | 已送達 | 96,478（97.0%）|
| `shipped` | 已出貨 | 1,107（1.1%）|
| `canceled` | 已取消 | 625（0.6%）|
| `unavailable` | 無庫存 | 609（0.6%）|
| `invoiced` | 已開發票 | 314（0.3%）|
| `processing` | 處理中 | 301（0.3%）|
| `created` | 已建立 | 5（0.0%）|
| `approved` | 已批准 | 2（0.0%）|

#### 載入代碼

```python
import pandas as pd

# 載入訂單主表
orders = pd.read_csv('data/olist_orders_dataset.csv')

# 轉換日期欄位
date_cols = ['order_purchase_timestamp', 'order_approved_at',
             'order_delivered_carrier_date', 'order_delivered_customer_date',
             'order_estimated_delivery_date']

for col in date_cols:
    orders[col] = pd.to_datetime(orders[col], errors='coerce')

# 設定 order_id 為索引
orders = orders.set_index('order_id')

print(f"✅ 訂單數：{len(orders):,}")
print(f"📅 時間範圍：{orders['order_purchase_timestamp'].min()} 至 {orders['order_purchase_timestamp'].max()}")
```

---

### 2. olist_order_items_dataset.csv（訂單明細）⭐

**筆數：** 112,650
**主鍵：** (`order_id`, `order_item_id`)
**外鍵：** `order_id`, `product_id`, `seller_id`
**說明：** 訂單中包含的商品明細，一筆訂單可以有多個商品

#### 欄位說明

| 欄位名稱 | 型別 | 說明 | 範例 |
|---------|------|------|------|
| `order_id` | string | 訂單 ID（外鍵） | `e481f51cbdc54678b7cc49136f2d6af7` |
| `order_item_id` | int | 商品序號（1, 2, 3...） | `1` |
| `product_id` | string | 商品 ID | `0beea0d3e8bbd9f43e89d8e3f7fcbe16` |
| `seller_id` | string | 賣家 ID | `c1512f8f75f48921d3d0faa53545ea9e` |
| `shipping_limit_date` | datetime | 出貨期限 | `2017-10-15 18:30:00` |
| `price` | float | 商品價格（BRL） | `29.99` |
| `freight_value` | float | 運費（BRL） | `8.72` |

#### 關鍵統計

```python
import pandas as pd

order_items = pd.read_csv('data/olist_order_items_dataset.csv')

print(f"✅ 訂單明細數：{len(order_items):,}")
print(f"📦 平均每筆訂單商品數：{order_items.groupby('order_id').size().mean():.2f}")
print(f"💰 平均商品價格：R$ {order_items['price'].mean():.2f}")
print(f"🚚 平均運費：R$ {order_items['freight_value'].mean():.2f}")

# 計算每筆訂單總金額
order_totals = order_items.groupby('order_id').agg({
    'price': 'sum',
    'freight_value': 'sum'
}).reset_index()

order_totals['total'] = order_totals['price'] + order_totals['freight_value']

print(f"💳 平均訂單總金額：R$ {order_totals['total'].mean():.2f}")
```

**預期輸出：**
```
✅ 訂單明細數：112,650
📦 平均每筆訂單商品數：1.13
💰 平均商品價格：R$ 120.65
🚚 平均運費：R$ 19.99
💳 平均訂單總金額：R$ 154.10
```

---

### 3. olist_products_dataset.csv（商品）

**筆數：** 32,951
**主鍵：** `product_id`
**說明：** 商品的屬性資訊

#### 欄位說明

| 欄位名稱 | 型別 | 說明 | 單位 |
|---------|------|------|------|
| `product_id` | string | 商品 ID（主鍵） | - |
| `product_category_name` | string | 商品類別（葡萄牙文） | - |
| `product_name_length` | int | 商品名稱長度 | 字元數 |
| `product_description_length` | int | 商品描述長度 | 字元數 |
| `product_photos_qty` | int | 商品照片數量 | 張 |
| `product_weight_g` | int | 商品重量 | 公克 |
| `product_length_cm` | int | 商品長度 | 公分 |
| `product_height_cm` | int | 商品高度 | 公分 |
| `product_width_cm` | int | 商品寬度 | 公分 |

#### 載入代碼

```python
products = pd.read_csv('data/olist_products_dataset.csv')

print(f"✅ 商品數：{len(products):,}")
print(f"📂 類別數：{products['product_category_name'].nunique()}")
print(f"📸 平均照片數：{products['product_photos_qty'].mean():.2f}")
print(f"⚖️ 平均重量：{products['product_weight_g'].mean():.0f} g")

# 類別分佈（Top 10）
print("\n📦 Top 10 商品類別：")
print(products['product_category_name'].value_counts().head(10))
```

---

### 4. olist_customers_dataset.csv（客戶）

**筆數：** 99,441
**主鍵：** `customer_id`
**說明：** 客戶的基本資訊與地理位置

#### 欄位說明

| 欄位名稱 | 型別 | 說明 | 範例 |
|---------|------|------|------|
| `customer_id` | string | 客戶 ID（主鍵） | `9ef432eb6251297304e76186b10a928d` |
| `customer_unique_id` | string | 客戶唯一 ID（跨訂單） | `f3c38ab652836d21` |
| `customer_zip_code_prefix` | int | 郵遞區號前 5 碼 | `14409` |
| `customer_city` | string | 城市 | `sao paulo` |
| `customer_state` | string | 州（2 碼） | `SP` |

#### 關鍵統計

```python
customers = pd.read_csv('data/olist_customers_dataset.csv')

print(f"✅ 客戶數：{len(customers):,}")
print(f"👤 獨立客戶數：{customers['customer_unique_id'].nunique():,}")
print(f"🏙️ 城市數：{customers['customer_city'].nunique():,}")
print(f"🗺️ 州數：{customers['customer_state'].nunique()}")

# 州分佈（Top 10）
print("\n🗺️ Top 10 客戶州：")
print(customers['customer_state'].value_counts().head(10))

# 計算複購率
repeat_customers = customers['customer_unique_id'].value_counts()
repeat_rate = (repeat_customers > 1).mean() * 100

print(f"\n🔄 複購率：{repeat_rate:.2f}%")
```

---

### 5. olist_sellers_dataset.csv（賣家）

**筆數：** 3,095
**主鍵：** `seller_id`
**說明：** 賣家的地理位置資訊

#### 欄位說明

| 欄位名稱 | 型別 | 說明 |
|---------|------|------|
| `seller_id` | string | 賣家 ID（主鍵） |
| `seller_zip_code_prefix` | int | 郵遞區號前 5 碼 |
| `seller_city` | string | 城市 |
| `seller_state` | string | 州（2 碼） |

#### 載入代碼

```python
sellers = pd.read_csv('data/olist_sellers_dataset.csv')

print(f"✅ 賣家數：{len(sellers):,}")
print(f"🏙️ 城市數：{sellers['seller_city'].nunique():,}")
print(f"🗺️ 州數：{sellers['seller_state'].nunique()}")

# 州分佈（Top 10）
print("\n🗺️ Top 10 賣家州：")
print(sellers['seller_state'].value_counts().head(10))
```

---

### 6. olist_order_payments_dataset.csv（付款）

**筆數：** 103,886
**主鍵：** (`order_id`, `payment_sequential`)
**外鍵：** `order_id`
**說明：** 訂單的付款資訊，一筆訂單可能有多筆付款（分期或組合支付）

#### 欄位說明

| 欄位名稱 | 型別 | 說明 |
|---------|------|------|
| `order_id` | string | 訂單 ID（外鍵） |
| `payment_sequential` | int | 付款序號（1, 2, 3...） |
| `payment_type` | string | 付款方式 |
| `payment_installments` | int | 分期期數 |
| `payment_value` | float | 付款金額（BRL） |

#### 付款方式

| 付款方式 | 說明 | 筆數 |
|---------|------|------|
| `credit_card` | 信用卡 | 76,795（73.9%）|
| `boleto` | Boleto（巴西支付方式） | 19,784（19.0%）|
| `voucher` | 優惠券 | 5,775（5.6%）|
| `debit_card` | 簽帳卡 | 1,529（1.5%）|

#### 載入代碼

```python
payments = pd.read_csv('data/olist_order_payments_dataset.csv')

print(f"✅ 付款筆數：{len(payments):,}")
print(f"💳 平均付款金額：R$ {payments['payment_value'].mean():.2f}")
print(f"📊 平均分期期數：{payments['payment_installments'].mean():.2f}")

# 付款方式分佈
print("\n💳 付款方式分佈：")
print(payments['payment_type'].value_counts())

# 計算每筆訂單的總付款金額
order_payment_totals = payments.groupby('order_id')['payment_value'].sum()
print(f"\n💰 平均訂單付款總額：R$ {order_payment_totals.mean():.2f}")
```

---

### 7. olist_order_reviews_dataset.csv（評論）

**筆數：** 99,224
**主鍵：** `review_id`
**外鍵：** `order_id`
**說明：** 客戶對訂單的評分與評論

#### 欄位說明

| 欄位名稱 | 型別 | 說明 |
|---------|------|------|
| `review_id` | string | 評論 ID（主鍵） |
| `order_id` | string | 訂單 ID（外鍵） |
| `review_score` | int | 評分（1-5 星） |
| `review_comment_title` | string | 評論標題 |
| `review_comment_message` | string | 評論內容 |
| `review_creation_date` | datetime | 評論建立日期 |
| `review_answer_timestamp` | datetime | 評論回覆時間戳記 |

#### 評分分佈

```python
reviews = pd.read_csv('data/olist_order_reviews_dataset.csv')

print(f"✅ 評論數：{len(reviews):,}")
print(f"⭐ 平均評分：{reviews['review_score'].mean():.2f}")

# 評分分佈
print("\n⭐ 評分分佈：")
score_dist = reviews['review_score'].value_counts().sort_index()
for score, count in score_dist.items():
    pct = count / len(reviews) * 100
    print(f"{score} 星：{count:,}（{pct:.1f}%）")

# 評論內容
has_comment = reviews['review_comment_message'].notna().sum()
print(f"\n💬 有評論內容的比例：{has_comment / len(reviews) * 100:.1f}%")
```

**預期輸出：**
```
✅ 評論數：99,224
⭐ 平均評分：4.08

⭐ 評分分佈：
1 星：11,336（11.4%）
2 星：3,151（3.2%）
3 星：8,287（8.4%）
4 星：19,200（19.4%）
5 星：57,250（57.7%）

💬 有評論內容的比例：41.1%
```

---

### 8. olist_geolocation_dataset.csv（地理位置）

**筆數：** 1,000,163
**說明：** 巴西郵遞區號對應的經緯度

#### 欄位說明

| 欄位名稱 | 型別 | 說明 |
|---------|------|------|
| `geolocation_zip_code_prefix` | int | 郵遞區號前 5 碼 |
| `geolocation_lat` | float | 緯度 |
| `geolocation_lng` | float | 經度 |
| `geolocation_city` | string | 城市 |
| `geolocation_state` | string | 州（2 碼） |

#### 注意事項

⚠️ **此表非常大（100 萬筆），通常不需要完整載入**

建議用法：
1. 只載入需要的郵遞區號
2. 先對 customers/sellers 去重，再 merge
3. 使用 chunking 分批處理

#### 載入代碼（優化版）

```python
# 方法 1：只載入需要的郵遞區號
needed_zips = customers['customer_zip_code_prefix'].unique()

geolocation = pd.read_csv('data/olist_geolocation_dataset.csv')
geolocation_filtered = geolocation[
    geolocation['geolocation_zip_code_prefix'].isin(needed_zips)
]

print(f"✅ 原始地理位置數：{len(geolocation):,}")
print(f"✅ 過濾後地理位置數：{len(geolocation_filtered):,}")

# 方法 2：去重（一個郵遞區號可能有多個經緯度）
geolocation_unique = geolocation.groupby('geolocation_zip_code_prefix').agg({
    'geolocation_lat': 'mean',
    'geolocation_lng': 'mean',
    'geolocation_city': 'first',
    'geolocation_state': 'first'
}).reset_index()

print(f"✅ 去重後地理位置數：{len(geolocation_unique):,}")
```

---

### 9. product_category_name_translation.csv（類別翻譯）

**筆數：** 71
**主鍵：** `product_category_name`
**說明：** 葡萄牙文類別名稱 → 英文翻譯

#### 欄位說明

| 欄位名稱 | 型別 | 說明 |
|---------|------|------|
| `product_category_name` | string | 類別名稱（葡萄牙文，主鍵） |
| `product_category_name_english` | string | 類別名稱（英文） |

#### 載入代碼

```python
category_translation = pd.read_csv('data/product_category_name_translation.csv')

print(f"✅ 類別數：{len(category_translation)}")
print("\n📂 前 10 個類別：")
print(category_translation.head(10).to_string(index=False))
```

---

## 🔗 常用多表整合代碼

### 基礎整合：訂單 + 客戶 + 商品

```python
import pandas as pd

# 載入核心表
orders = pd.read_csv('data/olist_orders_dataset.csv')
order_items = pd.read_csv('data/olist_order_items_dataset.csv')
customers = pd.read_csv('data/olist_customers_dataset.csv')
products = pd.read_csv('data/olist_products_dataset.csv')
category_translation = pd.read_csv('data/product_category_name_translation.csv')

# 只保留已送達的訂單
orders_delivered = orders[orders['order_status'] == 'delivered'].copy()

# Step 1: 訂單 + 客戶
df = orders_delivered.merge(
    customers,
    on='customer_id',
    how='left'
)

# Step 2: + 訂單明細
df = df.merge(
    order_items,
    on='order_id',
    how='left'
)

# Step 3: + 商品
df = df.merge(
    products,
    on='product_id',
    how='left'
)

# Step 4: + 類別翻譯
df = df.merge(
    category_translation,
    on='product_category_name',
    how='left'
)

print(f"✅ 整合完成！")
print(f"📊 最終筆數：{len(df):,}")
print(f"📊 最終欄位數：{len(df.columns)}")
```

---

### 完整整合：包含付款、評論

```python
# 接續上面的代碼

# Step 5: + 付款（先聚合）
payments = pd.read_csv('data/olist_order_payments_dataset.csv')
payment_summary = payments.groupby('order_id').agg({
    'payment_value': 'sum',
    'payment_type': lambda x: ', '.join(x.unique()),
    'payment_installments': 'mean'
}).reset_index()

payment_summary.columns = ['order_id', 'total_payment', 'payment_methods', 'avg_installments']

df = df.merge(
    payment_summary,
    on='order_id',
    how='left'
)

# Step 6: + 評論
reviews = pd.read_csv('data/olist_order_reviews_dataset.csv')
review_summary = reviews[['order_id', 'review_score', 'review_comment_message']]

df = df.merge(
    review_summary,
    on='order_id',
    how='left'
)

print(f"✅ 完整整合完成！")
print(f"📊 最終筆數：{len(df):,}")
print(f"📊 最終欄位數：{len(df.columns)}")
```

---

### 記憶體優化版載入

```python
import pandas as pd

# Dtype 優化配置
dtypes_orders = {
    'order_id': 'string',
    'customer_id': 'string',
    'order_status': 'category'
}

dtypes_order_items = {
    'order_id': 'string',
    'order_item_id': 'int8',
    'product_id': 'string',
    'seller_id': 'string',
    'price': 'float32',
    'freight_value': 'float32'
}

dtypes_products = {
    'product_id': 'string',
    'product_category_name': 'category',
    'product_name_length': 'int16',
    'product_description_length': 'int16',
    'product_photos_qty': 'int8',
    'product_weight_g': 'int32',
    'product_length_cm': 'int16',
    'product_height_cm': 'int16',
    'product_width_cm': 'int16'
}

# 載入並優化
orders = pd.read_csv('data/olist_orders_dataset.csv', dtype=dtypes_orders)
order_items = pd.read_csv('data/olist_order_items_dataset.csv', dtype=dtypes_order_items)
products = pd.read_csv('data/olist_products_dataset.csv', dtype=dtypes_products)

# 檢查記憶體使用
print("📊 記憶體使用：")
print(f"orders: {orders.memory_usage(deep=True).sum() / 1024**2:.2f} MB")
print(f"order_items: {order_items.memory_usage(deep=True).sum() / 1024**2:.2f} MB")
print(f"products: {products.memory_usage(deep=True).sum() / 1024**2:.2f} MB")
```

---

## 📊 資料品質說明

### 缺失值統計

```python
import pandas as pd
import numpy as np

# 載入所有表
orders = pd.read_csv('data/olist_orders_dataset.csv')
order_items = pd.read_csv('data/olist_order_items_dataset.csv')
products = pd.read_csv('data/olist_products_dataset.csv')
customers = pd.read_csv('data/olist_customers_dataset.csv')
reviews = pd.read_csv('data/olist_order_reviews_dataset.csv')

# 缺失值檢查函數
def check_missing(df, name):
    print(f"\n📊 {name} 缺失值：")
    missing = df.isnull().sum()
    missing = missing[missing > 0].sort_values(ascending=False)

    if len(missing) == 0:
        print("✅ 無缺失值")
    else:
        for col, count in missing.items():
            pct = count / len(df) * 100
            print(f"  {col}: {count:,}（{pct:.2f}%）")

# 檢查各表
check_missing(orders, 'Orders')
check_missing(order_items, 'Order Items')
check_missing(products, 'Products')
check_missing(customers, 'Customers')
check_missing(reviews, 'Reviews')
```

**已知缺失值：**

1. **orders 表：**
   - `order_approved_at`：160 筆（訂單未批准就取消）
   - `order_delivered_carrier_date`：1,783 筆（未交給物流）
   - `order_delivered_customer_date`：2,965 筆（未送達客戶）

2. **products 表：**
   - `product_category_name`：610 筆（無類別）
   - `product_name_length`：610 筆
   - `product_description_length`：610 筆
   - `product_photos_qty`：610 筆
   - `product_weight_g`：2 筆
   - `product_length_cm`：2 筆
   - `product_height_cm`：2 筆
   - `product_width_cm`：2 筆

3. **reviews 表：**
   - `review_comment_title`：87,656 筆（58.8% 未填寫標題）
   - `review_comment_message`：58,247 筆（58.9% 未填寫內容）

**處理建議：**
- 時間欄位：保留 NaT，代表該狀態未發生
- 商品屬性：可用中位數或類別平均填充
- 評論內容：保留 NaN，代表未填寫

---

### 重複值檢查

```python
# 檢查訂單 ID 是否唯一
print(f"orders 重複訂單 ID：{orders['order_id'].duplicated().sum()}")

# 檢查客戶 ID vs 獨立客戶 ID
print(f"客戶總數：{len(customers)}")
print(f"獨立客戶數：{customers['customer_unique_id'].nunique()}")
print(f"重複客戶數：{len(customers) - customers['customer_unique_id'].nunique()}")

# 檢查商品 ID 是否唯一
print(f"products 重複商品 ID：{products['product_id'].duplicated().sum()}")
```

**已知重複：**
- `customer_id` 每筆訂單唯一，但同一位客戶多次購買會有不同的 `customer_id`
- 使用 `customer_unique_id` 追蹤同一位客戶

---

## 🚀 快速啟動代碼模板

### 模板 1：基礎分析（單表）

```python
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns

# 設定
plt.rcParams['font.sans-serif'] = ['Arial Unicode MS', 'SimHei']
sns.set_style('whitegrid')

# 載入資料
orders = pd.read_csv('data/olist_orders_dataset.csv')

# 轉換日期
orders['order_purchase_timestamp'] = pd.to_datetime(orders['order_purchase_timestamp'])

# 只保留已送達的訂單
orders_delivered = orders[orders['order_status'] == 'delivered'].copy()

# 新增年月欄位
orders_delivered['year_month'] = orders_delivered['order_purchase_timestamp'].dt.to_period('M')

# 分析：每月訂單數
monthly_orders = orders_delivered.groupby('year_month').size()

# 視覺化
plt.figure(figsize=(12, 6))
monthly_orders.plot(kind='line', marker='o')
plt.title('每月訂單數趨勢', fontsize=14)
plt.xlabel('年月')
plt.ylabel('訂單數')
plt.grid(True, alpha=0.3)
plt.tight_layout()
plt.show()
```

---

### 模板 2：多表分析

```python
import pandas as pd
import numpy as np
from pathlib import Path

# 資料路徑
DATA_DIR = Path('/mnt/data/datasets/ecommerce/kaggle/olist')

# 載入資料
orders = pd.read_csv(DATA_DIR / 'olist_orders_dataset.csv')
order_items = pd.read_csv(DATA_DIR / 'olist_order_items_dataset.csv')
products = pd.read_csv(DATA_DIR / 'olist_products_dataset.csv')
category_translation = pd.read_csv(DATA_DIR / 'product_category_name_translation.csv')

# 只保留已送達訂單
orders_delivered = orders[orders['order_status'] == 'delivered']

# 整合資料
df = (orders_delivered
      .merge(order_items, on='order_id', how='left')
      .merge(products, on='product_id', how='left')
      .merge(category_translation, on='product_category_name', how='left'))

# 分析：Top 10 類別
top_categories = df.groupby('product_category_name_english').agg({
    'order_id': 'count',
    'price': 'sum'
}).sort_values('price', ascending=False).head(10)

print("💰 Top 10 營收類別：")
print(top_categories)
```

---

### 模板 3：使用工具函數

```python
# 使用自訂工具函數載入（Week 3 開始提供）
import sys
sys.path.append('../utils')

from data_loader import load_olist_data, load_olist_with_optimization

# 方法 1：標準載入
orders, order_items, products, customers, sellers, payments, reviews = load_olist_data()

# 方法 2：記憶體優化載入
orders, order_items, products, customers, sellers, payments, reviews = load_olist_with_optimization()

print("✅ 資料載入完成！")
print(f"訂單數：{len(orders):,}")
print(f"訂單明細數：{len(order_items):,}")
print(f"商品數：{len(products):,}")
print(f"客戶數：{len(customers):,}")
```

---

## 📖 常見分析場景

### 場景 1：營收分析

```python
# 每月營收趨勢
monthly_revenue = (df
    .groupby(df['order_purchase_timestamp'].dt.to_period('M'))
    ['price']
    .sum()
    .reset_index()
)

monthly_revenue.columns = ['年月', '營收']
monthly_revenue['年月'] = monthly_revenue['年月'].astype(str)

# MoM 成長率
monthly_revenue['MoM'] = monthly_revenue['營收'].pct_change() * 100

print(monthly_revenue.tail())
```

---

### 場景 2：客戶分析（RFM）

```python
import pandas as pd
from datetime import datetime

# 定義分析日期（資料集最後日期 + 1 天）
analysis_date = pd.to_datetime('2018-10-18')

# 計算 RFM
rfm = df.groupby('customer_unique_id').agg({
    'order_purchase_timestamp': lambda x: (analysis_date - x.max()).days,  # Recency
    'order_id': 'nunique',  # Frequency
    'price': 'sum'  # Monetary
}).reset_index()

rfm.columns = ['customer_unique_id', 'recency', 'frequency', 'monetary']

# RFM 評分（1-5 分）
rfm['R_score'] = pd.qcut(rfm['recency'], q=5, labels=[5,4,3,2,1])
rfm['F_score'] = pd.qcut(rfm['frequency'].rank(method='first'), q=5, labels=[1,2,3,4,5])
rfm['M_score'] = pd.qcut(rfm['monetary'], q=5, labels=[1,2,3,4,5])

# RFM 總分
rfm['RFM_score'] = rfm['R_score'].astype(str) + rfm['F_score'].astype(str) + rfm['M_score'].astype(str)

print(rfm.head())
```

---

### 場景 3：產品分析

```python
# Top 10 熱銷產品
top_products = (df
    .groupby(['product_id', 'product_category_name_english'])
    .agg({
        'order_id': 'count',
        'price': 'sum',
        'review_score': 'mean'
    })
    .sort_values('price', ascending=False)
    .head(10)
    .reset_index()
)

top_products.columns = ['商品ID', '類別', '訂單數', '總營收', '平均評分']

print("🔥 Top 10 熱銷產品：")
print(top_products.to_string(index=False))
```

---

## 🎯 Week 3-6 使用建議

### Week 3: MultiIndex & GroupBy
**主要使用表：**
- orders + order_items + products + category_translation
- 建立地區 × 類別 MultiIndex
- GroupBy 聚合計算各維度指標

**關鍵代碼：**
```python
# 建立 MultiIndex
df_multi = df.set_index(['customer_state', 'product_category_name_english'])

# GroupBy 命名聚合
result = df.groupby(['customer_state', 'product_category_name_english']).agg(
    訂單數=('order_id', 'nunique'),
    總營收=('price', 'sum'),
    平均客單價=('price', 'mean'),
    平均評分=('review_score', 'mean')
).reset_index()
```

---

### Week 4: 時間序列 & 視窗函數
**主要使用表：**
- orders（時間欄位）
- order_items（價格）

**關鍵代碼：**
```python
# 設定 DatetimeIndex
df_ts = df.set_index('order_purchase_timestamp')

# Resample 重採樣
monthly = df_ts.resample('M').agg({
    'order_id': 'nunique',
    'price': 'sum'
})

# Rolling 移動平均
monthly['ma_7d'] = monthly['price'].rolling(7).mean()

# MoM 成長率
monthly['mom'] = monthly['price'].pct_change() * 100
```

---

### Week 5: Apply/Transform/Agg
**主要使用表：**
- 完整整合資料（所有表）

**關鍵代碼：**
```python
# Transform 組內計算
df['category_pct'] = df.groupby('product_category_name_english')['price'].transform(
    lambda x: x / x.sum() * 100
)

# Agg 命名聚合
result = df.groupby('product_category_name_english').agg(
    訂單數=('order_id', 'nunique'),
    總營收=('price', 'sum'),
    平均單價=('price', 'mean'),
    單價標準差=('price', 'std'),
    最大單價=('price', 'max'),
    最小單價=('price', 'min')
)
```

---

### Week 6: 效能優化 & Merge
**主要使用表：**
- 所有表（練習 merge）

**關鍵代碼：**
```python
# Dtype 優化
df['order_status'] = df['order_status'].astype('category')
df['order_item_id'] = df['order_item_id'].astype('int8')
df['price'] = df['price'].astype('float32')

# Merge 驗證
df_merged = orders.merge(
    order_items,
    on='order_id',
    how='left',
    validate='1:m',  # 驗證 1對多關係
    indicator=True   # 追蹤來源
)

# 檢查未匹配
print(df_merged['_merge'].value_counts())
```

---

## 💾 資料儲存建議

### 儲存清洗後的資料（Parquet 格式）

```python
from pathlib import Path

# 建立輸出目錄
output_dir = Path('data/processed')
output_dir.mkdir(parents=True, exist_ok=True)

# 儲存完整寬表
df.to_parquet(output_dir / 'olist_complete.parquet', index=False)

print(f"✅ 資料已儲存")
print(f"📁 位置：{output_dir / 'olist_complete.parquet'}")
print(f"💾 大小：{(output_dir / 'olist_complete.parquet').stat().st_size / (1024**2):.2f} MB")
```

**為什麼使用 Parquet？**
- ✅ 檔案更小（壓縮率高）
- ✅ 讀取更快（列式儲存）
- ✅ 保留 dtype（不會丟失型別）
- ✅ 支援分區（大數據適用）

---

## 📚 參考資源

### 官方資源
- **Kaggle Dataset:** https://www.kaggle.com/datasets/olistbr/brazilian-ecommerce
- **Olist 官網:** https://olist.com/

### 相關分析
- Kaggle Notebooks: 搜尋 "olist"
- GitHub: 搜尋 "olist analysis"

### 推薦閱讀
- pandas 官方文檔：MultiIndex, GroupBy, Merge
- Week 3-6 教學指南

---

## 🎉 開始使用！

```bash
# 切換到專案目錄
cd /home/justin/web-projects/excel-python-data-analysis/week03-06_pandas-advanced

# 載入資料測試
python -c "
import pandas as pd
orders = pd.read_csv('/mnt/data/datasets/ecommerce/kaggle/olist/olist_orders_dataset.csv')
print(f'✅ 訂單數：{len(orders):,}')
"

# 開始 Week 3 學習
cd week03_multiindex_groupby
cat Day01_MultiIndex_Complete_Guide.md
```

**祝學習順利！ 📊💪**
