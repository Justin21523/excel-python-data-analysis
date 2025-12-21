# Day 9: Apply 深度應用與函數設計 (2-3 小時)

## 📚 目錄
1. [Series.apply 完全掌握](#series-apply-完全掌握)
2. [DataFrame.apply 多維應用](#dataframe-apply-多維應用)
3. [Apply 與向量化對比](#apply-與向量化對比)
4. [15 個實戰案例](#15-個實戰案例)
5. [Excel 對照教學](#excel-對照教學)

---

## Series.apply 完全掌握

### 1.1 基礎概念（20 分鐘）

`Series.apply()` 將函數逐行應用於 Series 的每個元素，返回新的 Series。

```python
import pandas as pd
import numpy as np
from olist.datasets import load_datasets

# 加載數據
orders_df = load_datasets('orders')
customers_df = load_datasets('customers')
products_df = load_datasets('products')

# 基礎 apply：單值函數
prices = products_df['price'].head(10)

# 方法1：Lambda 函數
result1 = prices.apply(lambda x: round(x, 2))

# 方法2：命名函數
def round_price(price):
    return round(price, 2)

result2 = prices.apply(round_price)

# 方法3：內置函數
result3 = prices.apply(str)
```

### 1.2 複雜邏輯實現（40 分鐘）

#### 情境 1: 根據訂單金額分類

```python
# 加載訂單數據
order_payments_df = load_datasets('order_payments')

# 定義分類函數
def categorize_payment(amount):
    """
    將支付金額分為：
    - 小額: < 50
    - 中額: 50-200
    - 大額: 200-1000
    - 超大額: >= 1000
    """
    if amount < 50:
        return '小額'
    elif amount < 200:
        return '中額'
    elif amount < 1000:
        return '大額'
    else:
        return '超大額'

# 應用函數
order_payments_df['payment_category'] = order_payments_df['payment_value'].apply(
    categorize_payment
)

print(order_payments_df[['payment_value', 'payment_category']].head(10))
print(order_payments_df['payment_category'].value_counts())
```

**輸出示例：**
```
   payment_value payment_category
0           27.5               小額
1           75.00              中額
2          150.00              中額
3          950.00              大額
4         1500.00             超大額

payment_category
中額       2500
小額       1800
大額       1200
超大額      500
```

#### 情境 2: 文字清洗與標準化

```python
# 客戶城市名稱清洗
customers_df_copy = customers_df.copy()

def clean_city_name(city):
    """
    清洗城市名稱：
    - 去除空格
    - 轉換為標題格式
    - 統一特殊字符
    """
    if pd.isna(city):
        return '未知'

    city = str(city).strip().title()
    # 替換常見的錯誤寫法
    city = city.replace('Sao Paulo', 'São Paulo')
    city = city.replace('Belo Horizonte', 'Belo Horizonte')

    return city

customers_df_copy['customer_city_clean'] = customers_df_copy['customer_city'].apply(
    clean_city_name
)

print(customers_df_copy[['customer_city', 'customer_city_clean']].head(10))
print(f"清洗前唯一城市數: {customers_df['customer_city'].nunique()}")
print(f"清洗後唯一城市數: {customers_df_copy['customer_city_clean'].nunique()}")
```

#### 情境 3: 根據城市和狀態判斷地區

```python
def categorize_region(state):
    """
    根據州縮寫判斷地區（巴西）
    """
    northeast = ['BA', 'PE', 'CE', 'MA', 'PI', 'RN', 'PB', 'AL', 'SE']
    north = ['AM', 'PA', 'AP', 'AC', 'RO', 'RR', 'TO']
    midwest = ['MS', 'GO', 'MT', 'DF']
    southeast = ['SP', 'RJ', 'MG', 'ES']
    south = ['PR', 'SC', 'RS']

    state = str(state).upper().strip()

    if state in northeast:
        return '東北地區'
    elif state in north:
        return '北部地區'
    elif state in midwest:
        return '中西部地區'
    elif state in southeast:
        return '東南地區'
    elif state in south:
        return '南部地區'
    else:
        return '未知'

customers_df_copy['region'] = customers_df_copy['customer_state'].apply(
    categorize_region
)

print(customers_df_copy['region'].value_counts())
```

**輸出示例：**
```
東南地區     7000
南部地區     2500
東北地區     1500
中西部地區    800
北部地區      200
未知          0
```

### 1.3 參數傳遞技巧（30 分鐘）

#### 技巧 1: 使用 args 傳遞固定參數

```python
def calculate_discount(price, discount_rate):
    """根據折扣率計算折扣價"""
    return price * (1 - discount_rate)

prices = products_df['price'].head(5)

# 傳遞固定的折扣率 10%
discounted = prices.apply(calculate_discount, args=(0.1,))

print(f"原價: {prices.values}")
print(f"折扣後 (10%): {discounted.values}")
```

#### 技巧 2: 使用 kwargs 傳遞命名參數

```python
def apply_shipping_cost(amount, method='standard'):
    """根據方式計算運費"""
    rates = {
        'standard': 0.05,      # 5% 運費
        'express': 0.10,       # 10% 運費
        'premium': 0.02        # 2% 運費
    }
    return amount * rates.get(method, 0.05)

prices = products_df['price'].head(5)

# 使用快速配送（10% 運費）
express_cost = prices.apply(apply_shipping_cost, kwargs={'method': 'express'})

print(express_cost)
```

#### 技巧 3: 使用 lambda 結合上下文

```python
# 結合 Series 索引創建個性化消息
customer_ids = customers_df['customer_id'].head(5)

messages = customer_ids.apply(
    lambda cid: f"親愛的客戶 {cid[-4:]}, 感謝您的購買!"
)

print(messages)
```

---

## DataFrame.apply 多維應用

### 2.1 axis 參數理解（30 分鐘）

#### axis=0（按列操作，預設）

```python
# 準備測試數據
sales_data = pd.DataFrame({
    '1月': [1000, 1500, 800],
    '2月': [1200, 1600, 900],
    '3月': [1100, 1700, 950],
}, index=['產品A', '產品B', '產品C'])

print("原始數據：")
print(sales_data)

# axis=0: 對每一列應用函數
column_max = sales_data.apply(max, axis=0)
print("\n各月最高銷售額：")
print(column_max)

column_sum = sales_data.apply(sum, axis=0)
print("\n各月總銷售額：")
print(column_sum)
```

#### axis=1（按行操作）

```python
# axis=1: 對每一行應用函數
row_sum = sales_data.apply(sum, axis=1)
print("\n各產品總銷售額：")
print(row_sum)

row_mean = sales_data.apply(np.mean, axis=1)
print("\n各產品平均銷售額：")
print(row_mean)

# 自訂函數：計算波動範圍
def calculate_range(row):
    """計算最大值 - 最小值"""
    return row.max() - row.min()

price_range = sales_data.apply(calculate_range, axis=1)
print("\n各產品銷售波動範圍：")
print(price_range)
```

### 2.2 行級複雜邏輯（axis=1）（40 分鐘）

#### 情境 1: 會員等級評定系統

```python
# 構建客戶消費數據（真實場景）
orders_df = load_datasets('orders')
order_items_df = load_datasets('order_items')
order_payments_df = load_datasets('order_payments')

# 計算客戶消費統計
customer_stats = order_payments_df.groupby('order_id').agg({
    'payment_value': 'sum'
}).reset_index()

# 合併訂單信息
customer_stats = customer_stats.merge(
    orders_df[['order_id', 'customer_id']],
    on='order_id'
)

# 計算客戶指標
customer_summary = customer_stats.groupby('customer_id').agg({
    'payment_value': ['sum', 'mean', 'count']
}).reset_index()

customer_summary.columns = ['customer_id', 'total_spent', 'avg_order', 'order_count']

print("客戶消費統計：")
print(customer_summary.head())

# 會員等級函數
def assign_member_level(row):
    """
    根據消費額和購買次數評定會員等級
    - 白金會員: 消費 >= 5000 且購買次數 >= 10
    - 黃金會員: 消費 >= 2000 或購買次數 >= 5
    - 銀牌會員: 消費 >= 500 或購買次數 >= 2
    - 普通會員: 其他
    """
    total_spent = row['total_spent']
    order_count = row['order_count']

    if total_spent >= 5000 and order_count >= 10:
        return '白金會員'
    elif total_spent >= 2000 or order_count >= 5:
        return '黃金會員'
    elif total_spent >= 500 or order_count >= 2:
        return '銀牌會員'
    else:
        return '普通會員'

customer_summary['member_level'] = customer_summary.apply(
    assign_member_level,
    axis=1
)

print("\n會員等級分佈：")
print(customer_summary['member_level'].value_counts())
```

**輸出示例：**
```
會員等級分佈：
普通會員    50000
銀牌會員    25000
黃金會員    18000
白金會員     7000
```

#### 情境 2: RFM 評分系統

```python
from datetime import datetime, timedelta

# 計算 RFM 指標
reference_date = orders_df['order_purchase_timestamp'].max()

# 構建 RFM 數據
rfm_data = []

for customer_id in orders_df['customer_id'].unique()[:1000]:  # 示例：前1000個客戶
    customer_orders = orders_df[orders_df['customer_id'] == customer_id]

    # R: 最近性（距離最後購買天數）
    last_purchase = customer_orders['order_purchase_timestamp'].max()
    recency = (reference_date - last_purchase).days

    # F: 頻率（購買次數）
    frequency = len(customer_orders)

    # M: 金額（消費總額）
    customer_payments = order_payments_df.merge(
        orders_df[['order_id', 'customer_id']],
        on='order_id'
    )
    monetary = customer_payments[
        customer_payments['customer_id'] == customer_id
    ]['payment_value'].sum()

    rfm_data.append({
        'customer_id': customer_id,
        'recency': recency,
        'frequency': frequency,
        'monetary': monetary
    })

rfm_df = pd.DataFrame(rfm_data)

# 對 RFM 進行五分位分級（1-5，5最優）
rfm_df['R_score'] = pd.qcut(rfm_df['recency'], 5, labels=[5,4,3,2,1], duplicates='drop')
rfm_df['F_score'] = pd.qcut(rfm_df['frequency'].rank(method='first'), 5, labels=[1,2,3,4,5], duplicates='drop')
rfm_df['M_score'] = pd.qcut(rfm_df['monetary'].rank(method='first'), 5, labels=[1,2,3,4,5], duplicates='drop')

# RFM 評分函數
def assign_rfm_segment(row):
    """
    根據 RFM 評分分配客戶分群
    """
    r, f, m = int(row['R_score']), int(row['F_score']), int(row['M_score'])

    # VIP 客戶: R >= 4 且 F >= 4 且 M >= 4
    if r >= 4 and f >= 4 and m >= 4:
        return 'VIP客戶'

    # 重要客戶: R >= 3 且 F >= 3
    elif r >= 3 and f >= 3:
        return '重要客戶'

    # 高價值客戶: M >= 4（雖然不常購）
    elif m >= 4:
        return '高價值客戶'

    # 活躍客戶: F >= 4 或 R >= 4
    elif f >= 4 or r >= 4:
        return '活躍客戶'

    # 流失風險: R <= 2 且 F <= 2
    elif r <= 2 and f <= 2:
        return '流失風險'

    # 普通客戶: 其他
    else:
        return '普通客戶'

rfm_df['segment'] = rfm_df.apply(assign_rfm_segment, axis=1)

print("RFM 客戶分群分佈：")
print(rfm_df['segment'].value_counts())
print("\nRFM 數據樣本：")
print(rfm_df.head(10))
```

#### 情境 3: 複雜條件規則引擎

```python
# 商品推薦規則
def recommend_product_category(row):
    """
    根據客戶消費習慣推薦產品類別
    """
    total_spent = row['total_spent']
    order_count = row['order_count']
    avg_order = row['avg_order']

    recommendations = []

    # 規則1: 高消費客戶推薦高端產品
    if total_spent >= 5000:
        recommendations.append('高端電子產品')

    # 規則2: 頻繁購買推薦衝動購物商品
    if order_count >= 20:
        recommendations.append('便利食品')

    # 規則3: 大額購買推薦家居用品
    if avg_order >= 1000:
        recommendations.append('家居裝飾品')

    # 規則4: 中等消費推薦日用品
    if 500 <= total_spent < 3000:
        recommendations.append('日用品')

    # 規則5: 低消費推薦優惠商品
    if total_spent < 500:
        recommendations.append('折扣商品')

    return ' | '.join(recommendations) if recommendations else '促銷商品'

customer_summary['recommendations'] = customer_summary.apply(
    recommend_product_category,
    axis=1
)

print("推薦示例：")
print(customer_summary[['customer_id', 'total_spent', 'recommendations']].head(10))
```

### 2.3 返回 DataFrame 的 apply（20 分鐘）

```python
# apply 可以返回 Series 或 DataFrame，自動展開為列

# 方法1: 返回 Series（自動轉換為多列）
def split_name_parts(name):
    """從完整名稱中提取名字和姓氏"""
    if pd.isna(name):
        return pd.Series({'first_name': '', 'last_name': ''})

    parts = str(name).split()
    first = parts[0] if len(parts) > 0 else ''
    last = ' '.join(parts[1:]) if len(parts) > 1 else ''

    return pd.Series({'first_name': first, 'last_name': last})

# 假設有客戶名稱數據
customer_names = pd.Series([
    'João Silva',
    'Maria Santos',
    'Pedro Oliveira',
    None
])

name_parts = customer_names.apply(split_name_parts)
print("名稱分解結果：")
print(name_parts)

# 方法2: 使用 DataFrame.apply 返回 Series
def calculate_statistics(col):
    """計算列的統計數據"""
    return pd.Series({
        'mean': col.mean(),
        'median': col.median(),
        'std': col.std(),
        'min': col.min(),
        'max': col.max()
    })

numeric_cols = sales_data
statistics = numeric_cols.apply(calculate_statistics, axis=0)
print("\n銷售數據統計：")
print(statistics)
```

---

## Apply 與向量化對比

### 3.1 效能測試（30 分鐘）

```python
import time
import numpy as np

# 準備測試數據
n_samples = 100000
test_data = pd.Series(np.random.uniform(0, 1000, n_samples))

print(f"測試數據量: {n_samples:,} 行")
print("=" * 60)

# 測試1: Apply vs Numpy 向量化（簡單函數）
def round_to_nearest_10(x):
    """舍入到最近的10"""
    return round(x / 10) * 10

# Apply 方法
start = time.time()
result_apply = test_data.apply(round_to_nearest_10)
apply_time = time.time() - start

# 向量化方法
start = time.time()
result_vectorized = np.round(test_data / 10) * 10
vectorized_time = time.time() - start

print(f"簡單舍入運算:")
print(f"  Apply:      {apply_time:.4f} 秒")
print(f"  Vectorized: {vectorized_time:.4f} 秒")
print(f"  性能提升:   {apply_time / vectorized_time:.1f}x 倍")
print()

# 測試2: Apply vs pd.cut（分類）
def categorize_score(score):
    """根據分數分類"""
    if score >= 750:
        return 'A'
    elif score >= 500:
        return 'B'
    elif score >= 250:
        return 'C'
    else:
        return 'D'

# Apply 方法
start = time.time()
result_apply = test_data.apply(categorize_score)
apply_time = time.time() - start

# 向量化方法
start = time.time()
result_vectorized = pd.cut(
    test_data,
    bins=[0, 250, 500, 750, 1000],
    labels=['D', 'C', 'B', 'A']
)
vectorized_time = time.time() - start

print(f"分類運算:")
print(f"  Apply:      {apply_time:.4f} 秒")
print(f"  Vectorized: {vectorized_time:.4f} 秒")
print(f"  性能提升:   {apply_time / vectorized_time:.1f}x 倍")
print()

# 測試3: Apply vs np.where（條件賦值）
def apply_discount(price):
    """根據價格應用折扣"""
    if price >= 1000:
        return price * 0.8  # 20% 折扣
    elif price >= 500:
        return price * 0.9  # 10% 折扣
    else:
        return price

# Apply 方法
start = time.time()
result_apply = test_data.apply(apply_discount)
apply_time = time.time() - start

# 向量化方法
start = time.time()
result_vectorized = np.where(
    test_data >= 1000,
    test_data * 0.8,
    np.where(test_data >= 500, test_data * 0.9, test_data)
)
vectorized_time = time.time() - start

print(f"折扣計算:")
print(f"  Apply:      {apply_time:.4f} 秒")
print(f"  Vectorized: {vectorized_time:.4f} 秒")
print(f"  性能提升:   {apply_time / vectorized_time:.1f}x 倍")
```

**典型輸出：**
```
測試數據量: 100,000 行
============================================================
簡單舍入運算:
  Apply:      0.2156 秒
  Vectorized: 0.0012 秒
  性能提升:   179.7x 倍

分類運算:
  Apply:      0.1845 秒
  Vectorized: 0.0018 秒
  性能提升:   102.5x 倍

折扣計算:
  Apply:      0.1923 秒
  Vectorized: 0.0015 秒
  性能提升:   128.2x 倍
```

### 3.2 何時使用 Apply vs 向量化（20 分鐘）

#### 使用 Apply 的情況

**情況1: 複雜邏輯（多條件判斷）**
```python
# 複雜的會員等級評定，用 apply 更清晰
def assign_complex_level(row):
    """複雜邏輯：難以用向量化表達"""
    if row['total_spent'] > 10000 and row['order_count'] > 20:
        if row['recency'] < 30:
            return '白金VIP'
        else:
            return '白金普通'
    elif row['total_spent'] > 5000:
        return '黃金'
    else:
        return '銀牌'

customer_summary['level'] = customer_summary.apply(assign_complex_level, axis=1)
```

**情況2: 使用字典對應**
```python
# 狀態碼轉換
status_mapping = {
    'pending': '待處理',
    'processing': '處理中',
    'shipped': '已發貨',
    'delivered': '已送達',
    'cancelled': '已取消'
}

orders_df['status_cn'] = orders_df['order_status'].apply(
    lambda x: status_mapping.get(x, '未知')
)
```

**情況3: 字符串複雜處理**
```python
# 地址解析
def extract_state_from_address(address):
    """從複雜地址中提取州信息"""
    if pd.isna(address):
        return None

    # 複雜的正則表達式和邏輯
    parts = str(address).split(',')
    for part in reversed(parts):
        part = part.strip()
        if len(part) == 2:  # 巴西州縮寫通常為2位
            return part.upper()

    return None

customers_df['state_extracted'] = customers_df['customer_city'].apply(
    extract_state_from_address
)
```

#### 使用向量化的情況

**情況1: 簡單數學運算**
```python
# 簡單計算：優先使用向量化
prices = products_df['price']

# 不好 ❌
prices_with_tax = prices.apply(lambda x: x * 1.15)

# 好 ✓
prices_with_tax = prices * 1.15
```

**情況2: 條件賦值**
```python
# 條件賦值：使用 np.where
payment_values = order_payments_df['payment_value']

# 不好 ❌
discounted = payment_values.apply(
    lambda x: x * 0.9 if x >= 100 else x
)

# 好 ✓
discounted = np.where(
    payment_values >= 100,
    payment_values * 0.9,
    payment_values
)
```

**情況3: 簡單分類**
```python
# 簡單分類：使用 pd.cut 或 pd.qcut
prices = products_df['price']

# 不好 ❌
price_cat = prices.apply(
    lambda x: 'High' if x >= 500 else 'Low'
)

# 好 ✓
price_cat = pd.cut(prices, bins=[0, 500, float('inf')], labels=['Low', 'High'])
```

### 3.3 優化策略（20 分鐘）

#### 策略1: 使用 numba 加速

```python
from numba import jit

# Numba JIT 編譯加速
@jit(nopython=True)
def fast_discount_calculation(price):
    """使用 numba 加速的折扣計算"""
    if price >= 1000:
        return price * 0.8
    elif price >= 500:
        return price * 0.9
    else:
        return price

# 測試性能
n = 100000
prices = np.random.uniform(0, 1000, n)

# Apply 方法（不用 numba）
start = time.time()
result_apply = pd.Series(prices).apply(fast_discount_calculation)
apply_time = time.time() - start

# 向量化方法
start = time.time()
result_vec = np.where(
    prices >= 1000, prices * 0.8,
    np.where(prices >= 500, prices * 0.9, prices)
)
vec_time = time.time() - start

print(f"Apply (Numba): {apply_time:.4f} 秒")
print(f"Vectorized:    {vec_time:.4f} 秒")
```

#### 策略2: 使用 map 處理小數據集

```python
# 對於小數據集，使用 map 有時更高效
category_map = {'BA': 'East', 'SP': 'South', 'RJ': 'South'}

# 使用 map
states = pd.Series(['BA', 'SP', 'RJ', 'BA'])
result = states.map(category_map)
```

#### 策略3: 分批處理大型函數

```python
# 對於複雜的外部 API 調用，分批處理
def batch_process_addresses(addresses, batch_size=1000):
    """批量處理地址，減少 API 調用開銷"""
    results = []

    for i in range(0, len(addresses), batch_size):
        batch = addresses.iloc[i:i + batch_size]
        # 假設這裡調用 API
        batch_results = process_batch(batch)  # 自定義函數
        results.extend(batch_results)

    return pd.Series(results, index=addresses.index)
```

---

## 15 個實戰案例

### 案例 1-5: Series.apply 基礎應用

**案例1: 價格分級**
```python
# 根據價格範圍分級
def price_tier(price):
    if price < 100:
        return '經濟型'
    elif price < 300:
        return '標準型'
    elif price < 800:
        return '優質型'
    else:
        return '奢侈型'

products_df['price_tier'] = products_df['price'].apply(price_tier)
print(products_df['price_tier'].value_counts())
```

**案例2: 簡化名稱**
```python
# 提取產品類別名稱的簡稱
def simplify_category(category_name):
    if pd.isna(category_name):
        return 'OTHER'

    cat_str = str(category_name).lower()

    # 簡化映射
    if 'electronic' in cat_str:
        return 'ELEC'
    elif 'furniture' in cat_str:
        return 'FURN'
    elif 'sport' in cat_str:
        return 'SPORT'
    else:
        return 'OTHER'

# 假設 product_categories_df 包含類別信息
product_categories_df['category_abbr'] = product_categories_df['product_category_name'].apply(
    simplify_category
)
```

**案例3: 計算年份**
```python
# 從時間戳提取年份
def extract_year(timestamp):
    if pd.isna(timestamp):
        return None
    return pd.to_datetime(timestamp).year

orders_df['purchase_year'] = orders_df['order_purchase_timestamp'].apply(extract_year)
print(f"購買年份分佈: {orders_df['purchase_year'].value_counts()}")
```

**案例4: 郵編驗證**
```python
# 驗證郵編格式
def validate_zipcode(zipcode):
    if pd.isna(zipcode):
        return '無效'

    zipcode_str = str(int(zipcode))  # 轉換為字符串

    if len(zipcode_str) == 5:
        return '有效'
    else:
        return '無效'

customers_df['zip_valid'] = customers_df['customer_zip_code_prefix'].apply(
    validate_zipcode
)

print(f"郵編有效性: {customers_df['zip_valid'].value_counts()}")
```

**案例5: 計算運費**
```python
# 根據重量計算運費
def calculate_shipping_fee(weight_kg):
    if pd.isna(weight_kg):
        return 0

    weight = float(weight_kg)

    if weight <= 1:
        return 10
    elif weight <= 5:
        return 15
    elif weight <= 10:
        return 25
    elif weight <= 30:
        return 40
    else:
        return weight * 2  # 每公斤 2元

products_df['shipping_fee'] = products_df['product_weight_g'].apply(
    lambda w: calculate_shipping_fee(w / 1000) if pd.notna(w) else 0
)
```

### 案例 6-10: DataFrame.apply 多維應用

**案例6: 完整的會員等級系統**
```python
# 構建完整的會員等級評定
def evaluate_customer_grade(row):
    """
    綜合考慮消費金額、購買頻率、最近性評定等級
    """
    total = row['total_spent']
    freq = row['order_count']
    recency = row['recency']

    # 計算綜合分數（滿分100）
    score = 0

    # 消費金額佔分40%
    if total >= 10000:
        score += 40
    elif total >= 5000:
        score += 30
    elif total >= 1000:
        score += 20
    elif total >= 500:
        score += 10

    # 購買頻率佔分35%
    if freq >= 20:
        score += 35
    elif freq >= 10:
        score += 25
    elif freq >= 5:
        score += 15
    elif freq >= 2:
        score += 7

    # 最近性佔分25%
    if recency <= 30:
        score += 25
    elif recency <= 60:
        score += 18
    elif recency <= 90:
        score += 12
    elif recency <= 180:
        score += 5

    # 根據分數分級
    if score >= 85:
        return 'S級VIP'
    elif score >= 70:
        return 'A級客戶'
    elif score >= 55:
        return 'B級客戶'
    elif score >= 40:
        return 'C級客戶'
    else:
        return 'D級客戶'

customer_summary['grade'] = customer_summary.apply(evaluate_customer_grade, axis=1)
print(customer_summary['grade'].value_counts())
```

**案例7: 客戶風險評分**
```python
def calculate_churn_risk(row):
    """
    計算客戶流失風險分數（0-100，越高風險越大）
    """
    risk_score = 0

    # 如果很久沒購買（30+）
    if row['recency'] > 180:
        risk_score += 40
    elif row['recency'] > 90:
        risk_score += 20
    elif row['recency'] > 30:
        risk_score += 10

    # 如果購買次數少
    if row['order_count'] == 1:
        risk_score += 30
    elif row['order_count'] <= 3:
        risk_score += 15

    # 如果消費額小
    if row['total_spent'] < 500:
        risk_score += 20
    elif row['total_spent'] < 1000:
        risk_score += 10

    return min(risk_score, 100)

customer_summary['churn_risk'] = customer_summary.apply(calculate_churn_risk, axis=1)

# 分級
def classify_risk(score):
    if score >= 80:
        return '極高風險'
    elif score >= 60:
        return '高風險'
    elif score >= 40:
        return '中等風險'
    else:
        return '低風險'

customer_summary['risk_level'] = customer_summary['churn_risk'].apply(classify_risk)
print(customer_summary['risk_level'].value_counts())
```

**案例8: 交叉銷售建議**
```python
def generate_cross_sell(row):
    """根據客戶特徵生成交叉銷售建議"""
    suggestions = []

    # 根據消費習慣
    if row['avg_order'] > 1000:
        suggestions.append('高端配件')
    elif row['avg_order'] > 500:
        suggestions.append('進階配件')

    if row['order_count'] > 15:
        suggestions.append('VIP會員計劃')

    if row['total_spent'] > 5000:
        suggestions.append('商務禮品套裝')

    if 'A級' in row.get('grade', ''):
        suggestions.append('優先客服')
        suggestions.append('免費配送')

    return ' | '.join(suggestions) if suggestions else '基礎商品'

customer_summary['cross_sell'] = customer_summary.apply(generate_cross_sell, axis=1)
```

**案例9: 定價策略**
```python
def recommend_pricing_strategy(row):
    """根據銷售額推薦定價策略"""
    if row['total_spent'] >= 10000:
        return 'VIP定價 (9折)'
    elif row['total_spent'] >= 5000:
        return '高級定價 (9.5折)'
    elif row['order_count'] >= 10:
        return '常客優惠 (10%折)'
    elif row['total_spent'] >= 1000:
        return '標準優惠 (5%折)'
    else:
        return '促銷定價 (無折扣)'

customer_summary['pricing'] = customer_summary.apply(recommend_pricing_strategy, axis=1)
```

**案例10: 生命週期階段評估**
```python
def evaluate_lifecycle_stage(row):
    """評估客戶在生命週期中的階段"""
    recency = row['recency']
    frequency = row['order_count']
    monetary = row['total_spent']

    # 新客戶：最近購買，但購買次數少
    if recency <= 30 and frequency <= 2:
        return '新客戶'

    # 活躍客戶：經常購買
    if frequency >= 10:
        return '活躍客戶'

    # 高價值客戶：消費高
    if monetary >= 5000:
        return '高價值客戶'

    # 流失風險：很久沒購買
    if recency > 180:
        return '流失客戶'

    # 有復活潛力：曾經購買過，最近活動減少
    if 30 < recency <= 180 and frequency >= 3:
        return '復活潛力'

    # 普通客戶
    return '普通客戶'

customer_summary['lifecycle'] = customer_summary.apply(evaluate_lifecycle_stage, axis=1)
print(customer_summary['lifecycle'].value_counts())
```

### 案例 11-15: 高級應用與優化

**案例11: 文本情感分析（使用第三方庫）**
```python
# 需要安裝: pip install textblob

from textblob import TextBlob

def analyze_sentiment(text):
    """分析評論情感"""
    if pd.isna(text):
        return '無法分析'

    blob = TextBlob(str(text))
    polarity = blob.sentiment.polarity

    if polarity > 0.5:
        return '正面'
    elif polarity > 0:
        return '中立偏正'
    elif polarity > -0.5:
        return '中立偏負'
    else:
        return '負面'

# 假設有評論數據
# reviews_df['sentiment'] = reviews_df['review_text'].apply(analyze_sentiment)
```

**案例12: 批量郵件個性化**
```python
def generate_personalized_email(row):
    """根據客戶信息生成個性化郵件主旨"""
    grade = row.get('grade', 'D級客戶')
    recency = row.get('recency', 180)

    if 'S級' in grade or 'A級' in grade:
        subject = f"尊敬的 VIP 客戶，{row['customer_id'][-4:]}，我們有特別好禮相送！"
    elif recency > 60:
        subject = f"親愛的客戶，很久不見！特別回饋禮券 30 元！"
    else:
        subject = f"親愛的客戶，新品上市，享 8 折優惠！"

    return subject

# customer_summary['email_subject'] = customer_summary.apply(generate_personalized_email, axis=1)
```

**案例13: 複雜的稅費計算**
```python
def calculate_total_with_tax_and_fee(row):
    """計算包含稅費和運費的最終價格"""
    base_price = row['price']
    weight = row['weight_kg']
    customer_state = row['customer_state']

    # 運費計算
    shipping = weight * 5  # 每公斤 5元

    # 州稅計算（不同州稅率不同）
    state_tax_rates = {
        'SP': 0.18, 'RJ': 0.16, 'MG': 0.14,
        'BA': 0.12, 'RS': 0.15, 'PR': 0.14
    }
    tax_rate = state_tax_rates.get(customer_state, 0.12)

    tax = (base_price + shipping) * tax_rate

    total = base_price + shipping + tax

    return round(total, 2)

# 使用示例（需要有相應的數據欄位）
```

**案例14: 異常值檢測**
```python
def detect_anomaly(row):
    """檢測異常交易"""
    amount = row['amount']
    customer_avg = row['customer_avg']
    customer_std = row['customer_std']

    # 使用 Z-score 方法：超過 3 倍標準差視為異常
    if customer_std == 0:
        # 所有交易金額相同
        z_score = 0
    else:
        z_score = abs((amount - customer_avg) / customer_std)

    if z_score > 3:
        return '高度異常'
    elif z_score > 2:
        return '異常'
    else:
        return '正常'

# 計算客戶的平均值和標準差
customer_stats = order_payments_df.groupby('customer_id')['payment_value'].agg(['mean', 'std']).reset_index()
customer_stats.columns = ['customer_id', 'customer_avg', 'customer_std']

# 合併數據
order_payments_enhanced = order_payments_df.merge(customer_stats, on='customer_id')

# 檢測異常
order_payments_enhanced['anomaly'] = order_payments_enhanced.apply(detect_anomaly, axis=1)
```

**案例15: 動態折扣引擎**
```python
def calculate_dynamic_discount(row):
    """根據多個因素計算動態折扣"""
    base_price = row['price']
    customer_grade = row.get('grade', 'C級客戶')
    order_count = row.get('order_count', 1)
    total_spent = row.get('total_spent', 0)
    quantity = row.get('quantity', 1)

    discount = 0

    # 客戶等級折扣
    grade_discounts = {
        'S級VIP': 0.20,
        'A級客戶': 0.15,
        'B級客戶': 0.10,
        'C級客戶': 0.05,
        'D級客戶': 0
    }
    discount += grade_discounts.get(customer_grade, 0)

    # 購買頻率額外折扣
    if order_count >= 20:
        discount += 0.05
    elif order_count >= 10:
        discount += 0.03

    # 購買數量折扣
    if quantity >= 50:
        discount += 0.05
    elif quantity >= 20:
        discount += 0.03

    # 累積消費折扣
    if total_spent >= 10000:
        discount += 0.05
    elif total_spent >= 5000:
        discount += 0.03

    # 限制最大折扣不超過 30%
    discount = min(discount, 0.30)

    final_price = base_price * (1 - discount)

    return {
        'final_price': round(final_price, 2),
        'discount_rate': f"{discount*100:.1f}%"
    }

# 返回 Series，會自動展開為多列
result = products_df.apply(lambda row: pd.Series(calculate_dynamic_discount(row)), axis=1)
```

---

## Excel 對照教學

### 從 Excel 到 Python：常見轉換

#### 對照1: IF 邏輯 → Series.apply

**Excel 公式:**
```excel
=IF(B2<50, "小額", IF(B2<200, "中額", "大額"))
```

**Python 等價:**
```python
def categorize(amount):
    if amount < 50:
        return "小額"
    elif amount < 200:
        return "中額"
    else:
        return "大額"

df['category'] = df['amount'].apply(categorize)

# 或使用 pd.cut（推薦用於簡單分類）
df['category'] = pd.cut(
    df['amount'],
    bins=[0, 50, 200, float('inf')],
    labels=['小額', '中額', '大額']
)
```

#### 對照2: IFERROR → Series.apply

**Excel 公式:**
```excel
=IFERROR(B2/C2, 0)
```

**Python 等價:**
```python
def safe_divide(row):
    try:
        return row['numerator'] / row['denominator']
    except (ZeroDivisionError, TypeError):
        return 0

df['result'] = df.apply(safe_divide, axis=1)

# 或使用 pandas 內置（推薦）
df['result'] = df['numerator'] / df['denominator']
df['result'] = df['result'].fillna(0)
```

#### 對照3: CONCATENATE → Series.apply

**Excel 公式:**
```excel
=CONCATENATE("客戶 ", A2, " 消費 ", B2, " 元")
```

**Python 等價:**
```python
def format_message(row):
    return f"客戶 {row['name']} 消費 {row['amount']} 元"

df['message'] = df.apply(format_message, axis=1)

# 或使用字符串方法（推薦）
df['message'] = "客戶 " + df['name'] + " 消費 " + df['amount'].astype(str) + " 元"
```

#### 對照4: VLOOKUP → Series.apply + map

**Excel 公式:**
```excel
=VLOOKUP(A2, 查詢表, 2, FALSE)
```

**Python 等價:**
```python
# 建立查詢字典
lookup_dict = dict(zip(lookup_df['key'], lookup_df['value']))

# 使用 map（推薦）
df['result'] = df['code'].map(lookup_dict)

# 或使用 apply
df['result'] = df['code'].apply(lambda x: lookup_dict.get(x, '未找到'))
```

#### 對照5: 複雜的巢狀邏輯 → DataFrame.apply(axis=1)

**Excel 公式:**
```excel
=IF(AND(B2>=5000, C2>=10), "VIP",
  IF(OR(B2>=2000, C2>=5), "金卡",
    IF(B2>=500, "銀卡", "普通")))
```

**Python 等價:**
```python
def assign_level(row):
    if row['spent'] >= 5000 and row['orders'] >= 10:
        return 'VIP'
    elif row['spent'] >= 2000 or row['orders'] >= 5:
        return '金卡'
    elif row['spent'] >= 500:
        return '銀卡'
    else:
        return '普通'

df['level'] = df.apply(assign_level, axis=1)
```

#### 對照6: SUMIF 廣播回原表 → Transform

**Excel 方法:** 使用輔助欄，SUMIF 計算後複製粘貼

**Python 方法:**
```python
# 計算每個城市的總銷售額
city_total = df.groupby('city')['sales'].transform('sum')

# 自動廣播回原表
df['city_total_sales'] = city_total
```

---

## 完整工作流範例

### 從原始數據到最終報表

```python
# 1. 加載數據
orders_df = load_datasets('orders')
customers_df = load_datasets('customers')
order_payments_df = load_datasets('order_payments')

# 2. 計算客戶指標
customer_stats = order_payments_df.groupby('order_id').agg({
    'payment_value': 'sum'
}).reset_index()

customer_stats = customer_stats.merge(
    orders_df[['order_id', 'customer_id']],
    on='order_id'
)

customer_summary = customer_stats.groupby('customer_id').agg({
    'payment_value': ['sum', 'mean', 'count']
}).reset_index()

customer_summary.columns = ['customer_id', 'total_spent', 'avg_order', 'order_count']

# 3. 計算 RFM
reference_date = orders_df['order_purchase_timestamp'].max()
last_purchase = orders_df.groupby('customer_id')['order_purchase_timestamp'].max().reset_index()
last_purchase.columns = ['customer_id', 'last_purchase_date']

customer_summary = customer_summary.merge(last_purchase, on='customer_id')
customer_summary['recency'] = (reference_date - customer_summary['last_purchase_date']).dt.days

# 4. 應用 apply 進行複雜評估
def comprehensive_evaluation(row):
    """綜合評估客戶"""
    evaluation = {}

    # 會員等級
    if row['total_spent'] >= 5000 and row['order_count'] >= 10:
        evaluation['member_level'] = '白金'
    elif row['total_spent'] >= 2000 or row['order_count'] >= 5:
        evaluation['member_level'] = '黃金'
    else:
        evaluation['member_level'] = '銀牌'

    # 流失風險
    if row['recency'] > 180:
        evaluation['risk'] = '高風險'
    elif row['recency'] > 90:
        evaluation['risk'] = '中等風險'
    else:
        evaluation['risk'] = '低風險'

    return pd.Series(evaluation)

result = customer_summary.apply(comprehensive_evaluation, axis=1)
customer_summary = pd.concat([customer_summary, result], axis=1)

# 5. 生成最終報表
final_report = customer_summary.sort_values('total_spent', ascending=False).head(100)

print("Top 100 客戶摘要：")
print(final_report[['customer_id', 'total_spent', 'order_count', 'member_level', 'risk']])
```

---

## 學習檢查清單

- [ ] 理解 Series.apply 的基本用法
- [ ] 掌握自訂函數設計最佳實踐
- [ ] 能夠使用 DataFrame.apply(axis=1) 實現複雜邏輯
- [ ] 了解 apply 與向量化的性能差異
- [ ] 知道何時使用 apply vs 向量化方法
- [ ] 能夠實現完整的會員評級系統
- [ ] 掌握 RFM 分析的實踐應用
- [ ] 理解 Excel 到 Python 的轉換模式

---

## 後續資源

- **Day 10**: Transform 保持形狀的轉換
- **Day 11**: Named Aggregation 命名聚合
- **Day 12**: 實戰整合專案（RFM 完整系統）
- **Exercise**: 15 題練習 (Easy/Medium/Hard)

---

**建立時間**: 2025-12-11
**版本**: 1.0
**狀態**: 完整版
