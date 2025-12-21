# QUICK START: 30 分鐘快速入門

## ⚡ 5 分鐘理解核心概念

### Apply: 複雜邏輯轉換

```python
import pandas as pd

# 題目：根據銷售額分類
sales = pd.Series([100, 500, 1500])

# 方法1: Lambda（簡單）
result = sales.apply(lambda x: '高' if x > 500 else '低')
# 輸出: ['低', '低', '高']

# 方法2: 命名函數（複雜邏輯）
def classify_sales(amount):
    if amount < 500:
        return '低'
    elif amount < 1000:
        return '中'
    else:
        return '高'

result = sales.apply(classify_sales)
# 輸出: ['低', '低', '高']
```

### Transform: 廣播相對值

```python
# 題目：計算每個城市的平均銷售額，廣播回原表
data = pd.DataFrame({
    'city': ['北京', '北京', '上海'],
    'sales': [100, 150, 200]
})

# Transform: 自動廣播
data['city_avg'] = data.groupby('city')['sales'].transform('mean')

# 結果：
#   city  sales  city_avg
# 0   北京    100       125
# 1   北京    150       125
# 2   上海    200       200

# 核心：保持 3 行（與原表相同），值重複廣播
```

### Agg: 聚合統計

```python
# 題目：統計每個城市的銷售額
result = data.groupby('city').agg(
    total_sales=('sales', 'sum'),
    avg_sales=('sales', 'mean'),
    num_sales=('sales', 'count')
)

# 結果：2 行（一個城市一行）
#      total_sales  avg_sales  num_sales
# city
# 上海        200.0      200.0         1
# 北京        250.0      125.0         2
```

---

## 🎯 10 分鐘完整例子

### 場景：會員評級系統

```python
import pandas as pd

# 準備數據
customers = pd.DataFrame({
    'customer_id': ['C1', 'C2', 'C3', 'C4'],
    'city': ['北京', '北京', '上海', '上海'],
    'total_spent': [1000, 3000, 2000, 500],
    'num_orders': [2, 8, 5, 1]
})

print("原始數據:")
print(customers)

# ========== Step 1: Apply - 會員評級 ==========
def assign_level(row):
    """複雜邏輯：根據消費額和購買次數評級"""
    if row['total_spent'] >= 2000 and row['num_orders'] >= 5:
        return '金牌'
    elif row['total_spent'] >= 1000 or row['num_orders'] >= 3:
        return '銀牌'
    else:
        return '普通'

customers['level'] = customers.apply(assign_level, axis=1)

print("\n經過 Apply 後（評級）:")
print(customers[['customer_id', 'total_spent', 'level']])

# ========== Step 2: Transform - 城市排名 ==========
# 在城市內計算排名（保持原行數）
customers['city_rank'] = customers.groupby('city')['total_spent'].transform(
    lambda x: x.rank(ascending=False)
)

# 在城市內計算占比
city_total = customers.groupby('city')['total_spent'].transform('sum')
customers['city_pct'] = (customers['total_spent'] / city_total * 100).round(2)

print("\n經過 Transform 後（排名和占比）:")
print(customers[['customer_id', 'city', 'total_spent', 'city_rank', 'city_pct']])

# ========== Step 3: Agg - 城市報表 ==========
city_report = customers.groupby('city').agg(
    num_customers=('customer_id', 'count'),
    total_revenue=('total_spent', 'sum'),
    avg_customer_value=('total_spent', 'mean'),
    num_gold_members=('level', lambda x: (x == '金牌').sum()),
    num_silver_members=('level', lambda x: (x == '銀牌').sum())
)

print("\n城市聚合報表（Agg）:")
print(city_report)

# 最終結果：
print("\n最終完整表：")
print(customers[['customer_id', 'city', 'total_spent', 'level', 'city_rank', 'city_pct']])
```

**執行結果：**
```
原始數據:
  customer_id city  total_spent  num_orders
0          C1   北京         1000           2
1          C2   北京         3000           8
2          C3   上海         2000           5
3          C4   上海          500           1

經過 Apply 後（評級）:
  customer_id  total_spent level
0          C1         1000   銀牌
1          C2         3000   金牌
2          C3         2000   金牌
3          C4          500   普通

經過 Transform 後（排名和占比）:
  customer_id city  total_spent  city_rank  city_pct
0          C1   北京         1000        2.0      25.0
1          C2   北京         3000        1.0      75.0
2          C3   上海         2000        1.0      80.0
3          C4   上海          500        2.0      20.0

城市聚合報表（Agg）:
     num_customers  total_revenue  avg_customer_value  num_gold_members  num_silver_members
city
北京              2           4000              2000                  1                    1
上海              2           2500              1250                  1                    0

最終完整表：
  customer_id city  total_spent level  city_rank  city_pct
0          C1   北京         1000   銀牌       2.0      25.0
1          C2   北京         3000   金牌       1.0      75.0
2          C3   上海         2000   金牌       1.0      80.0
3          C4   上海          500   普通       2.0      20.0
```

---

## ⚙️ 性能提示（15 分鐘）

### ❌ 不要這樣做

```python
# 不好：複雜的 lambda（難讀且慢）
prices = pd.Series([100, 500, 1500])
result = prices.apply(lambda x: '高' if x >= 1000 else ('中' if x >= 500 else '低'))

# 不好：簡單運算也用 apply
result = prices.apply(lambda x: x * 1.2)  # 這可以直接 prices * 1.2
```

### ✅ 應該這樣做

```python
# 好：用函數名分類（清晰）
def classify_price(price):
    if price >= 1000:
        return '高'
    elif price >= 500:
        return '中'
    else:
        return '低'

result = prices.apply(classify_price)

# 好：簡單運算直接向量化（快 100 倍）
result = prices * 1.2

# 好：分類使用 pd.cut（最快）
result = pd.cut(prices, bins=[0, 500, 1000, float('inf')],
                labels=['低', '中', '高'])
```

### 性能對比

```python
import time
import numpy as np

prices_large = pd.Series(np.random.uniform(0, 1000, 100000))

# Apply 方法
start = time.time()
result = prices_large.apply(lambda x: x * 1.2)
apply_time = time.time() - start

# 向量化方法
start = time.time()
result = prices_large * 1.2
vec_time = time.time() - start

print(f"Apply: {apply_time:.4f}s")
print(f"Vectorized: {vec_time:.4f}s")
print(f"性能提升: {apply_time/vec_time:.1f}x")

# 輸出：
# Apply: 0.2156s
# Vectorized: 0.0012s
# 性能提升: 179.7x
```

---

## 📚 推薦學習順序

### Day 1（2 小時）
1. 重新閱讀本 QUICK_START（5 分鐘）
2. 完整例子練習（10 分鐘）
3. Day09_Apply_Deep_Dive_Guide.md - Part 1 (50 分鐘)
4. Exercise_07 - Easy 題 (75 分鐘)

### Day 2（2.5 小時）
1. Day10_Transform_Guide.md - Part 1 (50 分鐘)
2. Exercise_08 - Easy 題 (60 分鐘)
3. Day11_Agg_Named_Guide.md - Part 1 (40 分鐘)

### Day 3（2.5 小時）
1. Day09 Medium + Day10 Medium + Day11 Easy 題 (120 分鐘)
2. Solutions_Complete.md 對標 (30 分鐘)

### Day 4（4 小時）
1. Day11 進階 + Day12 完整整合 (180 分鐘)
2. Hard 題練習 (60 分鐘)

---

## 🎓 關鍵命令速查表

### Apply

```python
# Series.apply - 單列轉換
df['new_col'] = df['col'].apply(lambda x: ...)
df['new_col'] = df['col'].apply(my_function)

# DataFrame.apply - 多列邏輯
df['result'] = df.apply(
    lambda row: row['a'] + row['b'] if row['a'] > 0 else 0,
    axis=1
)
```

### Transform

```python
# 保持行數、廣播結果
df['group_mean'] = df.groupby('group')['value'].transform('mean')
df['z_score'] = df.groupby('group')['value'].transform(
    lambda x: (x - x.mean()) / x.std()
)
df['rank'] = df.groupby('group')['value'].transform(
    lambda x: x.rank(ascending=False)
)
```

### Agg

```python
# 簡單聚合
result = df.groupby('group')['value'].agg('sum')

# Named Aggregation
result = df.groupby('group').agg(
    total=('value', 'sum'),
    avg=('value', 'mean'),
    count=('id', 'nunique')
)

# 自訂函數
def my_agg(series):
    return series.std() / series.mean()

result = df.groupby('group')['value'].agg(my_agg)
```

---

## 🔍 常見陷阱

### 陷阱1: Apply 與 Transform 混淆

```python
# ❌ 不對：想要廣播卻用 agg
result = df.groupby('city')['sales'].agg('mean')  # 只有 2 行（每個城市一行）

# ✓ 正確：使用 transform 廣播
result = df.groupby('city')['sales'].transform('mean')  # 保持原行數，值重複
```

### 陷阱2: Lambda 過度複雜

```python
# ❌ 難讀
result = s.apply(lambda x: '高' if x >= 1000 else ('中' if x >= 500 else '低'))

# ✓ 清晰
def classify(x):
    if x >= 1000: return '高'
    elif x >= 500: return '中'
    else: return '低'

result = s.apply(classify)

# ✓ 最優
result = pd.cut(s, bins=[0, 500, 1000, float('inf')],
                labels=['低', '中', '高'])
```

### 陷阱3: 簡單操作也用 Apply

```python
# ❌ 慢（0.2s）
result = prices.apply(lambda x: x * 1.2)

# ✓ 快（0.001s）
result = prices * 1.2
```

---

## ✅ 自檢清單（5 分鐘）

完成以下任務來驗證理解：

```python
# 1. Apply: 根據分數等級化
scores = pd.Series([45, 65, 80, 95])
# 應該返回：['F', 'D', 'B', 'A']

# 2. Transform: 計算組內占比
data = pd.DataFrame({
    'group': ['A', 'A', 'B', 'B'],
    'value': [10, 20, 30, 70]
})
# 應該返回 8 行、4 行各兩個相同的占比值

# 3. Agg: 生成聚合報表
# 應該返回 2 行（一個 group 一行）、3 列（num_records, total, avg）

# 4. 性能：為什麼向量化比 apply 快？
# 原因：[你的答案]

# 5. 業務：會員評級為什麼用 apply？
# 原因：[你的答案]
```

---

## 🚀 下一步

✓ 完成本章節
↓
✓ 進行 Day 09-12 完整學習
↓
✓ 做完全部 37 題練習
↓
✓ 完成最終整合項目（Day 12）
↓
✓ 掌握完整的 RFM 客戶分析系統

---

## 📞 快速查詢

**忘記了 Transform 的用法？**
→ 見 Day10_Transform_Guide.md Part 1

**卡在某道題上？**
→ 見 Solutions_Complete.md 前 5 題解答

**想看完整案例？**
→ 見 Day12_Practice_Integration.md

**想找特定主題？**
→ 見 INDEX.md

---

**準備好了嗎？開始學習吧！** 🎓

首先完成這個 10 分鐘的完整例子，然後進入 Day 09。

祝你學習愉快！
