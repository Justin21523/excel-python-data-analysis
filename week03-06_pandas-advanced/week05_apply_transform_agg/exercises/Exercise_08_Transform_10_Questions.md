# Exercise 08: Transform 保持形狀變換 10 題

## 難度說明
- 🟢 **Easy** (3題): 基礎 transform 和簡單統計
- 🟡 **Medium** (4題): 組內標準化和相對排名
- 🔴 **Hard** (3題): 複雜業務場景

---

## 🟢 Easy Questions (1-3)

### 📌 Q1: 計算組內平均值並廣播
```python
# 題目：計算每個城市的平均銷售額，並廣播到原表（保持行數不變）

sales_data = pd.DataFrame({
    'city': ['北京', '北京', '北京', '上海', '上海', '深圳'],
    'sales': [100, 150, 120, 200, 180, 90]
})

# 填寫代碼：計算每個城市的平均銷售額
sales_data['city_avg_sales'] = sales_data.groupby('city')['sales'].transform(???)

# 預期輸出：
#   city  sales  city_avg_sales
# 0   北京    100           123.3
# 1   北京    150           123.3
# 2   北京    120           123.3
# 3   上海    200           190.0
# 4   上海    180           190.0
# 5   深圳     90            90.0

print(sales_data)
```

**答案提示**: 使用 'mean' 作為聚合函數

---

### 📌 Q2: 計算組內排名
```python
# 題目：在每個部門內，根據績效評分進行排名（降序）

employee_data = pd.DataFrame({
    'department': ['Sales', 'Sales', 'Sales', 'Marketing', 'Marketing'],
    'employee': ['A', 'B', 'C', 'D', 'E'],
    'performance': [85, 92, 78, 88, 82]
})

# 填寫代碼：計算每個部門內的排名（1 = 最高）
employee_data['dept_rank'] = employee_data.groupby('department')['performance'].transform(
    lambda x: x.rank(ascending=False)
)

# 預期輸出：
#   department employee  performance  dept_rank
# 0      Sales        A            85         2.0
# 1      Sales        B            92         1.0
# 2      Sales        C            78         3.0
# 3   Marketing        D            88         1.0
# 4   Marketing        E            82         2.0

print(employee_data)
```

**答案提示**: 使用 lambda 和 rank() 方法

---

### 📌 Q3: 計算佔比（組內）
```python
# 題目：計算每個產品在其類別中的銷售額佔比

product_data = pd.DataFrame({
    'category': ['電子', '電子', '電子', '家居', '家居'],
    'product': ['手機', '平板', '筆電', '沙發', '椅子'],
    'sales': [50000, 45000, 60000, 8000, 12000]
})

# 填寫代碼：計算類別內佔比（百分比）
category_total = product_data.groupby('category')['sales'].transform('sum')
product_data['pct_of_category'] = (product_data['sales'] / category_total * 100).round(2)

# 預期輸出：
#   category product  sales  pct_of_category
# 0     電子    手機  50000           37.88
# 1     電子    平板  45000           34.09
# 2     電子    筆電  60000           45.45  # 應為 45.45
# 3     家居    沙發   8000           40.00
# 4     家居    椅子  12000           60.00

print(product_data)
```

**答案提示**: 先用 transform 得到類別總和，再計算比例

---

## 🟡 Medium Questions (4-7)

### 📌 Q4: Z-score 標準化（組內）
```python
# 題目：在每個城市內進行 Z-score 標準化

price_data = pd.DataFrame({
    'city': ['北京', '北京', '北京', '上海', '上海'],
    'house_price': [5000000, 6000000, 4500000, 3000000, 3500000]
})

# 填寫代碼：計算每個城市內的 Z-score
def z_score(group):
    return (group - group.mean()) / group.std()

price_data['price_zscore'] = price_data.groupby('city')['house_price'].transform(z_score)

# 預期輸出（Z-score 應該平均值為 0，標準差為 1）：
#    city house_price  price_zscore
# 0   北京     5000000       -0.112...
# 1   北京     6000000        1.121...
# 2   北京     4500000       -1.009...
# 3   上海     3000000       -0.707...
# 4   上海     3500000        0.707...

print(price_data)

# 驗證：城市內的平均 zscore 應該約為 0
print(price_data.groupby('city')['price_zscore'].mean())  # 應該接近 0
print(price_data.groupby('city')['price_zscore'].std())   # 應該接近 1
```

**答案提示**: (value - mean) / std

---

### 📌 Q5: 百分位排名
```python
# 題目：計算每個產品在其類別中的百分位排名（0-100）

product_sales = pd.DataFrame({
    'category': ['A', 'A', 'A', 'A', 'B', 'B', 'B'],
    'product': ['P1', 'P2', 'P3', 'P4', 'P5', 'P6', 'P7'],
    'sales': [1000, 5000, 3000, 2000, 2000, 4000, 1000]
})

# 填寫代碼：計算類別內的百分位排名
product_sales['percentile_rank'] = product_sales.groupby('category')['sales'].transform(
    lambda x: x.rank(pct=True) * 100
).round(2)

# 預期輸出：
#   category product  sales  percentile_rank
# 0        A      P1   1000            25.00
# 1        A      P2   5000           100.00
# 2        A      P3   3000            75.00
# 3        A      P4   2000            50.00
# 4        B      P5   2000            50.00
# 5        B      P6   4000           100.00
# 6        B      P7   1000            0.00  # 應為 0.00

print(product_sales)
```

**答案提示**: 使用 rank(pct=True) 獲得百分位值

---

### 📌 Q6: 組內異常值標記
```python
# 題目：標記每個部門內偏離平均值超過 2 倍標準差的異常值

performance_data = pd.DataFrame({
    'department': ['Sales', 'Sales', 'Sales', 'Sales', 'Tech', 'Tech', 'Tech'],
    'employee': ['A', 'B', 'C', 'D', 'E', 'F', 'G'],
    'score': [85, 88, 90, 35, 92, 95, 88]
})

# 填寫代碼：計算 Z-score，標記 |z| > 2 的為異常值
def z_score(group):
    return (group - group.mean()) / group.std()

performance_data['z_score'] = performance_data.groupby('department')['score'].transform(z_score)
performance_data['is_outlier'] = abs(performance_data['z_score']) > 2

# 預期輸出：
#   department employee  score   z_score  is_outlier
# 0      Sales        A     85  0.447...       False
# 1      Sales        B     88  0.559...       False
# 2      Sales        C     90  0.670...       False
# 3      Sales        D     35 -2.141...        True    <- 異常
# 4       Tech        E     92  0.000...       False
# 5       Tech        F     95  1.247...       False
# 6       Tech        G     88 -1.247...       False

print(performance_data)
print("\n異常值檢測結果:")
print(performance_data[performance_data['is_outlier']])
```

---

### 📌 Q7: 組內累計百分比（帕累托分析）
```python
# 題目：計算累計銷售額占類別總額的百分比（用於帕累托分析）

sales_by_product = pd.DataFrame({
    'category': ['A', 'A', 'A', 'B', 'B', 'B'],
    'product': ['P1', 'P2', 'P3', 'P4', 'P5', 'P6'],
    'sales': [1000, 3000, 2000, 500, 1500, 1000]
})

# 先按銷售額排序
sales_by_product = sales_by_product.sort_values(['category', 'sales'], ascending=[True, False]).reset_index(drop=True)

# 填寫代碼：計算累計百分比
def cumsum_pct(group):
    return (group.cumsum() / group.sum() * 100).round(2)

sales_by_product['cumsum_pct'] = sales_by_product.groupby('category')['sales'].transform(cumsum_pct)

# 預期輸出：
#   category product  sales  cumsum_pct
# 0        A      P2   3000       50.00
# 1        A      P3   2000       83.33
# 2        A      P1   1000      100.00
# 3        B      P5   1500       50.00
# 4        B      P6   1000       83.33
# 5        B      P4    500      100.00

print(sales_by_product)
```

---

## 🔴 Hard Questions (8-10)

### 📌 Q8: 組內增長率計算
```python
# 題目：計算每個銷售員月度的環月增長率

sales_trend = pd.DataFrame({
    'salesman': ['Alice', 'Alice', 'Alice', 'Bob', 'Bob', 'Bob'],
    'month': [1, 2, 3, 1, 2, 3],
    'sales': [10000, 12000, 11000, 8000, 9000, 10000]
})

# 填寫代碼：按銷售員分組，計算月度增長率
sales_trend = sales_trend.sort_values(['salesman', 'month'])

def monthly_growth(group):
    return group.pct_change() * 100

sales_trend['growth_rate'] = sales_trend.groupby('salesman')['sales'].transform(monthly_growth)

# 預期輸出：
#    salesman  month  sales  growth_rate
# 0    Alice      1  10000          NaN
# 1    Alice      2  12000         20.00
# 2    Alice      3  11000         -8.33...
# 3      Bob      1   8000          NaN
# 4      Bob      2   9000         12.50
# 5      Bob      3  10000         11.11...

print(sales_trend)
```

**答案提示**: 使用 pct_change() 計算百分比增長

---

### 📌 Q9: 組內對標分析
```python
# 題目：計算每個員工的績效相對於同部門平均的差異（偏差度）

employee_performance = pd.DataFrame({
    'department': ['Sales', 'Sales', 'Sales', 'Tech', 'Tech'],
    'employee': ['A', 'B', 'C', 'D', 'E'],
    'performance_score': [85, 90, 80, 92, 88]
})

# 填寫代碼：計算與部門平均的差異（絕對值和百分比）
dept_mean = employee_performance.groupby('department')['performance_score'].transform('mean')

employee_performance['diff_to_dept_avg'] = (
    employee_performance['performance_score'] - dept_mean
).round(2)

employee_performance['diff_pct'] = (
    (employee_performance['performance_score'] - dept_mean) / dept_mean * 100
).round(2)

# 預期輸出：
#   department employee  performance_score  diff_to_dept_avg  diff_pct
# 0      Sales        A                 85             -3.33       -3.75
# 1      Sales        B                 90              1.67        1.96
# 2      Sales        C                 80             -8.33        -9.79
# 3       Tech        D                 92              2.00         2.22
# 4       Tech        E                 88             -2.00        -2.22

print(employee_performance)
```

---

### 📌 Q10: 複雜的相對位置計算
```python
# 題目：計算每個城市內的房價相對位置
# 包含：排名、百分位、Z-score、與最高價的比例

house_prices = pd.DataFrame({
    'city': ['北京', '北京', '北京', '北京', '上海', '上海', '上海'],
    'house': ['H1', 'H2', 'H3', 'H4', 'H5', 'H6', 'H7'],
    'price': [5000000, 8000000, 6000000, 7000000, 3000000, 4000000, 3500000]
})

# 填寫代碼：計算多個相對位置指標
house_prices['rank'] = house_prices.groupby('city')['price'].transform(
    lambda x: x.rank(ascending=False).astype(int)
)

house_prices['percentile'] = house_prices.groupby('city')['price'].transform(
    lambda x: (x.rank(pct=True) * 100).round(2)
)

def z_score(group):
    return ((group - group.mean()) / group.std()).round(3)

house_prices['z_score'] = house_prices.groupby('city')['price'].transform(z_score)

house_prices['pct_of_max'] = house_prices.groupby('city')['price'].transform(
    lambda x: (x / x.max() * 100).round(2)
)

# 預期輸出會包含所有四個指標
print(house_prices)

# 統計：北京內 rank=1 的房子
print("\n北京最高價房子:")
print(house_prices[(house_prices['city'] == '北京') & (house_prices['rank'] == 1)])
```

---

## 常見錯誤與注意事項

### ❌ 錯誤示例
```python
# 錯誤1: 使用 agg 而不是 transform（改變了形狀）
result = df.groupby('city')['sales'].agg('mean')  # 返回 Series，索引為城市
# 正確應該是 transform
result = df.groupby('city')['sales'].transform('mean')  # 保持原形狀

# 錯誤2: 忘記處理缺失值
z_scores = (group - group.mean()) / group.std()  # std() 在空組中返回 NaN
# 應該使用
z_scores = (group - group.mean()) / group.std().replace(0, 1)

# 錯誤3: 自訂函數沒有返回正確形狀
def my_func(group):
    return group.sum()  # ❌ 返回標量

def my_func(group):
    return group / group.sum()  # ✓ 返回 Series
```

### ✓ 最佳實踐
```python
# 1. 總是驗證結果形狀
original_rows = len(df)
result_rows = len(df.groupby('col')[target].transform('mean'))
assert original_rows == result_rows, "形狀不匹配！"

# 2. 檢查缺失值
assert df[new_col].isna().sum() == 0, "有缺失值"

# 3. 驗證計算邏輯
print(df.groupby('col')[target].transform('mean').describe())
```

---

## 答案提交格式

```markdown
### Q1 答案
```python
# 代碼...
```
```

---

**參考資源**
- Day 10: Transform 保持形狀變換指南
- Pandas groupby().transform() 官方文檔

---

**更新時間**: 2025-12-11
**版本**: 1.0
