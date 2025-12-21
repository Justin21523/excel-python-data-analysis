# Exercise 07: Apply 深度應用 15 題

## 難度說明
- 🟢 **Easy** (5題): 基礎 Series.apply 和簡單函數
- 🟡 **Medium** (6題): DataFrame.apply(axis=1) 和複雜邏輯
- 🔴 **Hard** (4題): 高級應用和性能優化

---

## 🟢 Easy Questions (1-5)

### 📌 Q1: 基礎價格轉換
```python
# 題目：使用 apply 將價格從美元轉換為人民幣
# 匯率：1 USD = 7.2 CNY

prices = pd.Series([10, 50, 100, 250])

# 填寫代碼
result = prices.apply(???)

# 預期輸出：
# 0       72.0
# 1      360.0
# 2      720.0
# 3     1800.0

print(result)
```

**答案提示**: 使用 lambda 函數，將每個價格乘以 7.2

---

### 📌 Q2: 文本大寫轉換
```python
# 題目：將產品名稱轉換為大寫，並添加前綴 "PRODUCT_"

product_names = pd.Series(['laptop', 'mouse', 'keyboard', 'monitor'])

# 填寫代碼
result = product_names.apply(???)

# 預期輸出：
# 0       PRODUCT_LAPTOP
# 1       PRODUCT_MOUSE
# 2       PRODUCT_KEYBOARD
# 3       PRODUCT_MONITOR

print(result)
```

**答案提示**: 組合字符串操作和大寫轉換

---

### 📌 Q3: 簡單分類函數
```python
# 題目：根據溫度分類：<0='冷', 0-20='涼', 20-30='溫暖', >30='熱'

temperatures = pd.Series([-5, 10, 25, 35, 0, 30])

def categorize_temp(temp):
    if temp < 0:
        return '冷'
    elif temp < 20:
        return '涼'
    elif temp < 30:
        return '溫暖'
    else:
        return '熱'

# 填寫代碼
result = temperatures.apply(???)

# 預期輸出：
# 0      冷
# 1      涼
# 2      溫暖
# 3      熱
# 4      涼
# 5      熱

print(result)
```

**答案提示**: 直接使用定義好的函數

---

### 📌 Q4: 處理缺失值的 apply
```python
# 題目：使用 apply 清洗電話號碼，不合法的返回 '無效'
# 合法電話：11 位數字

phone_numbers = pd.Series(['13812345678', 'invalid', None, '12345', '12345678901'])

def validate_phone(phone):
    if pd.isna(phone):
        return '無效'
    phone_str = str(phone)
    if len(phone_str) == 11 and phone_str.isdigit():
        return '有效'
    else:
        return '無效'

# 填寫代碼
result = phone_numbers.apply(???)

# 預期輸出：
# 0       有效
# 1       無效
# 2       無效
# 3       無效
# 4       有效

print(result)
```

**答案提示**: 使用定義好的驗證函數

---

### 📌 Q5: 字符串長度分類
```python
# 題目：根據字符串長度分類：<5='短', 5-10='中', >10='長'

descriptions = pd.Series(['Hi', 'Hello World', 'This is a test description', 'Python'])

# 填寫代碼
result = descriptions.apply(???)

# 預期輸出：
# 0       短
# 1       中
# 2       長
# 3       短

print(result)
```

**答案提示**: 在 lambda 中使用 len() 函數

---

## 🟡 Medium Questions (6-11)

### 📌 Q6: 複雜條件邏輯 (DataFrame.apply axis=1)
```python
# 題目：根據銷售額和數量評定優惠級別
# 邏輯：
# - 銷售額 >= 1000 且數量 >= 5: '高級優惠'
# - 銷售額 >= 500 或 數量 >= 3: '標準優惠'
# - 否則: '基礎優惠'

sales_data = pd.DataFrame({
    'product': ['A', 'B', 'C', 'D', 'E'],
    'amount': [1200, 800, 1500, 300, 600],
    'quantity': [4, 3, 6, 2, 2]
})

def assign_discount(row):
    if row['amount'] >= 1000 and row['quantity'] >= 5:
        return '高級優惠'
    elif row['amount'] >= 500 or row['quantity'] >= 3:
        return '標準優惠'
    else:
        return '基礎優惠'

# 填寫代碼
sales_data['discount_level'] = sales_data.apply(???, axis=???)

# 預期輸出：
# discount_level: ['高級優惠', '標準優惠', '高級優惠', '基礎優惠', '標準優惠']

print(sales_data)
```

**答案提示**: 需要同時訪問 amount 和 quantity 列，因此需要 axis=1

---

### 📌 Q7: 會員等級評定系統
```python
# 題目：根據消費額和購買次數評定會員等級
# 邏輯：
# - 白金: 消費 >= 5000 且購買 >= 10
# - 黃金: 消費 >= 2000 或購買 >= 5
# - 銀牌: 消費 >= 500
# - 普通: 否則

customer_data = pd.DataFrame({
    'customer_id': ['C1', 'C2', 'C3', 'C4', 'C5'],
    'total_spent': [6000, 1500, 500, 3000, 8000],
    'num_orders': [12, 3, 1, 4, 20]
})

def assign_member_level(row):
    spent = row['total_spent']
    orders = row['num_orders']

    if spent >= 5000 and orders >= 10:
        return '白金'
    elif spent >= 2000 or orders >= 5:
        return '黃金'
    elif spent >= 500:
        return '銀牌'
    else:
        return '普通'

# 填寫代碼
customer_data['member_level'] = customer_data.apply(???, axis=???)

# 預期輸出：
# member_level: ['白金', '普通', '銀牌', '黃金', '白金']

print(customer_data)
```

---

### 📌 Q8: 生成個性化消息
```python
# 題目：根據客戶等級生成個性化問候消息

customer_data = pd.DataFrame({
    'name': ['Alice', 'Bob', 'Charlie'],
    'spent': [6000, 1500, 3000],
    'level': ['白金', '普通', '黃金']
})

def generate_message(row):
    name = row['name']
    level = row['level']

    if level == '白金':
        return f"親愛的 {name} 先生/女士，感謝您的尊貴支持！"
    elif level == '黃金':
        return f"尊敬的 {name}，感謝您的持續購買！"
    else:
        return f"Hi {name}, 歡迎回來！"

# 填寫代碼
customer_data['message'] = customer_data.apply(???, axis=???)

# 預期輸出：
# message: [
#     '親愛的 Alice 先生/女士，感謝您的尊貴支持！',
#     'Hi Bob, 歡迎回來！',
#     '尊敬的 Charlie，感謝您的持續購買！'
# ]

print(customer_data)
```

---

### 📌 Q9: 計算複雜指標
```python
# 題目：計算投資回報率 (ROI)
# ROI = (收益 - 投資) / 投資 * 100%
# 若投資為 0，返回 None

investment_data = pd.DataFrame({
    'project': ['A', 'B', 'C', 'D'],
    'investment': [1000, 2000, 0, 1500],
    'return': [1200, 1800, 500, 2200]
})

def calculate_roi(row):
    if row['investment'] == 0:
        return None
    return (row['return'] - row['investment']) / row['investment'] * 100

# 填寫代碼
investment_data['roi'] = investment_data.apply(???, axis=???)

# 預期輸出：
# roi: [20.0, -10.0, None, 46.66...]

print(investment_data)
```

---

### 📌 Q10: RFM 簡化版評分
```python
# 題目：根據最近性(days)、頻率(orders)、金額(monetary) 計算簡化 RFM 評分
# 評分標準：R(≤30天=5分), F(≥10次=5分), M(≥5000=5分)，其他遞減

rfm_data = pd.DataFrame({
    'customer_id': ['C1', 'C2', 'C3'],
    'recency': [10, 60, 120],
    'frequency': [15, 5, 2],
    'monetary': [8000, 2000, 500]
})

def score_rfm(row):
    r_score = 5 if row['recency'] <= 30 else (4 if row['recency'] <= 60 else 3)
    f_score = 5 if row['frequency'] >= 10 else (4 if row['frequency'] >= 5 else 2)
    m_score = 5 if row['monetary'] >= 5000 else (4 if row['monetary'] >= 2000 else 2)
    return r_score + f_score + m_score

# 填寫代碼
rfm_data['rfm_score'] = rfm_data.apply(???, axis=???)

# 預期輸出：
# rfm_score: [15, 13, 8]

print(rfm_data)
```

---

### 📌 Q11: 條件賦值與文本組合
```python
# 題目：根據訂單狀態和金額生成訂單摘要

order_data = pd.DataFrame({
    'order_id': ['O1', 'O2', 'O3', 'O4'],
    'status': ['completed', 'pending', 'completed', 'cancelled'],
    'amount': [100, 200, 50, 150]
})

def generate_summary(row):
    status_cn = {
        'completed': '已完成',
        'pending': '待處理',
        'cancelled': '已取消'
    }
    level = '大額' if row['amount'] >= 100 else '小額'
    return f"訂單 {row['order_id']}: {status_cn[row['status']]} - {level} (${row['amount']})"

# 填寫代碼
order_data['summary'] = order_data.apply(???, axis=???)

# 預期輸出：
# 訂單 O1: 已完成 - 大額 ($100)
# 訂單 O2: 待處理 - 大額 ($200)
# ...

print(order_data['summary'])
```

---

## 🔴 Hard Questions (12-15)

### 📌 Q12: 性能優化 - Apply vs 向量化
```python
# 題目：識別下列兩個代碼中，哪個效率更高？並說明原因

import time
import numpy as np

# 準備數據
prices = pd.Series(np.random.uniform(0, 1000, 10000))

# 方法1: Apply
start = time.time()
method1 = prices.apply(lambda x: x * 1.2 if x >= 500 else x)
time1 = time.time() - start

# 方法2: 向量化
start = time.time()
method2 = np.where(prices >= 500, prices * 1.2, prices)
time2 = time.time() - start

print(f"Apply 耗時: {time1:.4f}s")
print(f"向量化耗時: {time2:.4f}s")
print(f"性能提升: {time1/time2:.1f}x")

# 問題：
# 1. 哪個方法更快？
# 2. 在什麼情況下應該使用 apply？
# 3. 寫出改進的向量化版本代碼
```

**提示**: 執行程序並觀察性能差異

---

### 📌 Q13: 自訂聚合函數 - RFM 完整評分
```python
# 題目：實現一個完整的 RFM 評分系統，處理邊界情況

customer_data = pd.DataFrame({
    'customer_id': ['C1', 'C2', 'C3', 'C4'],
    'recency': [5, 45, 90, 180],
    'frequency': [50, 15, 5, 1],
    'monetary': [10000, 3000, 800, 100]
})

def assign_rfm_segment(row):
    """
    實現完整的 RFM 分群邏輯：
    - VIP: R>=4 且 F>=4 且 M>=4
    - 核心: F>=4 或 M>=4
    - 流失: R<=2 且 F<=2
    """
    # 先進行五分位分級
    r_scores = pd.qcut(customer_data['recency'], q=5, labels=[5,4,3,2,1], duplicates='drop')
    f_scores = pd.qcut(customer_data['frequency'].rank(method='first'), q=5, labels=[1,2,3,4,5], duplicates='drop')
    m_scores = pd.qcut(customer_data['monetary'].rank(method='first'), q=5, labels=[1,2,3,4,5], duplicates='drop')

    r = r_scores.loc[row.name]
    f = f_scores.loc[row.name]
    m = m_scores.loc[row.name]

    if r >= 4 and f >= 4 and m >= 4:
        return 'VIP'
    elif f >= 4 or m >= 4:
        return '核心'
    elif r <= 2 and f <= 2:
        return '流失'
    else:
        return '普通'

# 填寫代碼
customer_data['segment'] = customer_data.apply(???, axis=???)

# 預期輸出會因五分位分級的結果而異，但應返回恰當的分群標籤
print(customer_data)
```

---

### 📌 Q14: 複雜的多列依賴邏輯
```python
# 題目：設計一個客戶流失預警系統，同時考慮多個因素

customer_data = pd.DataFrame({
    'customer_id': ['C1', 'C2', 'C3', 'C4', 'C5'],
    'recency_days': [5, 45, 90, 150, 200],
    'total_spent': [5000, 1500, 800, 3000, 4000],
    'last_order_days_ago': [5, 45, 90, 120, 60],
    'order_frequency': [20, 8, 3, 10, 12]
})

def assess_churn_risk(row):
    """
    評估流失風險：
    - 紅色警告: 最近無購買>90天 且 消費 >5000
    - 橙色警告: 最近無購買>60天
    - 黃色警告: 購買頻率下降
    """
    risk = row['last_order_days_ago']
    spent = row['total_spent']
    freq = row['order_frequency']

    if risk > 90 and spent > 5000:
        return 'RED'
    elif risk > 60:
        return 'ORANGE'
    elif freq < 5 and risk > 30:
        return 'YELLOW'
    else:
        return 'GREEN'

# 填寫代碼
customer_data['churn_risk'] = customer_data.apply(???, axis=???)

# 預期輸出：
# churn_risk: ['GREEN', 'YELLOW', 'RED', 'ORANGE', 'GREEN']

print(customer_data)
```

---

### 📌 Q15: 時間序列與複雜計算
```python
# 題目：基於訂單時間和金額，計算客戶的購買加速度

order_data = pd.DataFrame({
    'order_id': ['O1', 'O2', 'O3', 'O4', 'O5'],
    'customer_id': ['C1', 'C1', 'C1', 'C2', 'C2'],
    'order_date': pd.date_range('2023-01-01', periods=5),
    'amount': [100, 150, 200, 100, 120]
})

def calculate_purchase_acceleration(row):
    """
    計算購買加速度（訂單 i 的金額增長率）
    加速度 = (當前金額 - 前一金額) / 前一金額 * 100%
    若沒有前一訂單，返回 0
    """
    customer_orders = order_data[order_data['customer_id'] == row['customer_id']].sort_values('order_date')
    idx = customer_orders.index.get_loc(row.name)

    if idx == 0:
        return 0
    else:
        prev_amount = customer_orders.iloc[idx-1]['amount']
        return (row['amount'] - prev_amount) / prev_amount * 100

# 填寫代碼
order_data['acceleration'] = order_data.apply(???, axis=???)

# 預期輸出：
# acceleration: [0, 50.0, 33.33..., 0, 20.0]

print(order_data)
```

---

## 答案提交格式

請按照以下格式提交答案：

```markdown
### Q1 答案
```python
代碼...
```

### Q2 答案
```python
代碼...
```

... 以此類推
```

---

**重點複習**

1. Series.apply() vs DataFrame.apply(axis=1) 的區別
2. Lambda 函數 vs 命名函數的選擇
3. Apply 的性能考量
4. 複雜條件邏輯的實現模式
5. 數據驗證和邊界情況處理

---

**參考資源**
- Day 09: Apply 深度應用指南
- Pandas 官方文檔: apply()

---

**更新時間**: 2025-12-11
**版本**: 1.0
