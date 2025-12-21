# 快速開始 - 5 分鐘入門 Week 4

## 1. 環境設置（1 分鐘）

```python
import pandas as pd
import numpy as np
from datetime import datetime, timedelta
from pandas.tseries.offsets import BDay

# 驗證 Pandas 版本（需要 1.5+）
print(f"Pandas 版本: {pd.__version__}")
```

---

## 2. 核心概念速覽（2 分鐘）

### DateTime：日期轉換和屬性
```python
# 轉換日期字符串
dates = pd.to_datetime(['2023-01-15', '2023-02-20', '2023-03-10'])

# 提取屬性
df = pd.DataFrame({'date': dates, 'sales': [100, 150, 120]})
df['year'] = df['date'].dt.year
df['month'] = df['date'].dt.month
df['day'] = df['date'].dt.day
df['day_name'] = df['date'].dt.day_name()  # Monday, Tuesday, ...
```

### Resample：時間序列聚合
```python
# 設置日期為索引
df.set_index('date', inplace=True)

# 日 → 週 → 月 聚合
weekly = df.resample('W').sum()   # 按週求和
monthly = df.resample('ME').sum() # 按月求和
```

### Rolling：移動視窗計算
```python
# 計算移動平均線
df['sma_7'] = df['sales'].rolling(7).mean()    # 7 日平均
df['sma_30'] = df['sales'].rolling(30).mean()  # 30 日平均
```

### Shift & pct_change：時間比較
```python
# 時間平移（對比上期）
df['previous'] = df['sales'].shift(1)

# 計算增長率
df['growth_pct'] = df['sales'].pct_change() * 100  # 日環比
df['yoy_pct'] = df['sales'].pct_change(periods=365) * 100  # 年同期
```

---

## 3. 完整示例（2 分鐘）

### 建立完整的時間序列分析

```python
# 建立示例數據
np.random.seed(42)
dates = pd.date_range('2023-01-01', periods=90, freq='D')
df = pd.DataFrame({
    'date': dates,
    'sales': np.random.randint(100, 500, 90)
})

# 設置日期索引
df.set_index('date', inplace=True)

# ============ DateTime 技能 ============
df['year'] = df.index.year
df['month'] = df.index.month
df['day_name'] = df.index.day_name()

# ============ Resample 技能 ============
weekly_sum = df.resample('W').sum()
monthly_sum = df.resample('ME').sum()
monthly_avg = df.resample('ME').mean()

# ============ Rolling 技能 ============
df['sma_7'] = df['sales'].rolling(7).mean()
df['sma_30'] = df['sales'].rolling(30).mean()

# ============ Shift 技能 ============
df['previous_day'] = df['sales'].shift(1)
df['previous_week'] = df['sales'].shift(7)

# ============ Growth 技能 ============
df['daily_growth'] = df['sales'].pct_change() * 100
df['weekly_growth'] = df['sales'].pct_change(periods=7) * 100

# ============ Expanding 技能 ============
df['cumsum'] = df['sales'].expanding().sum()
df['cumavg'] = df['sales'].expanding().mean()

# 查看結果
print("前 10 行數據：")
print(df.head(10))
print("\n月度摘要：")
print(monthly_sum)
```

---

## 4. 常用代碼片段

### 日期篩選
```python
# 篩選特定日期範圍
q1_data = df['2023-01-01':'2023-03-31']

# 篩選特定月份
jan_data = df[df.index.month == 1]

# 篩選工作日
df['is_weekday'] = df.index.dayofweek < 5
weekday_data = df[df['is_weekday']]
```

### 月環比 (MoM)
```python
monthly = df.resample('ME').sum()
monthly['mom_growth'] = monthly['sales'].pct_change() * 100
print(monthly)
```

### 年同期 (YoY)
```python
# 去年同日數據
df['last_year'] = df['sales'].shift(365)
df['yoy_growth'] = (df['sales'] - df['last_year']) / df['last_year'] * 100
```

### 異常檢測
```python
# 基於移動平均的異常檢測
df['ma'] = df['sales'].rolling(30).mean()
df['std'] = df['sales'].rolling(30).std()
df['is_anomaly'] = abs(df['sales'] - df['ma']) > 2 * df['std']
print(f"異常日期：{df[df['is_anomaly']].index.tolist()}")
```

### 工作日計算
```python
from pandas.tseries.offsets import BDay

# 計算 N 個工作日後的日期
today = pd.to_datetime('2023-01-13')  # Friday
next_workday = today + 2 * BDay()  # = 2023-01-17 (Tuesday)
```

---

## 5. 學習路徑建議

```
【5 分鐘】理解核心概念（本頁）
     ↓
【1 小時】Day 5: DateTime 基礎
     ↓
【1 小時】Exercise 4: DateTime 簡單題
     ↓
【1 小時】Day 6: Resample 與 Rolling
     ↓
【1 小時】Exercise 5: Resample 簡單題
     ↓
【1 小時】Day 7: 時間比較
     ↓
【1 小時】Exercise 6: 時間比較簡單題
     ↓
【1 小時】完成中等題
     ↓
【1 小時】Day 8: 實踐整合
     ↓
【1 小時】完成困難題和進階練習
```

---

## 6. 我該從哪裡開始？

### 如果您是 Excel 用戶
→ 從 **Day 5: DateTime** 開始，學習日期轉換基礎

### 如果您已懂 Pandas 基礎
→ 從 **Exercise 5: Resample** 開始，直接進入實踐

### 如果您想快速應用
→ 複製本頁的完整示例，修改數據後直接使用

### 如果您要準備面試
→ 完成所有 32 題練習題，重點掌握困難題

---

## 7. 常見問題速答

**Q: Resample 和 Rolling 的區別？**
- Resample：重新定義時間粒度（日→周→月）
- Rolling：在固定時間窗口內計算（7 日平均）

**Q: shift(1) vs pct_change() 的區別？**
- shift(1)：獲取上一期原始數據
- pct_change()：計算增長率百分比

**Q: 什麼時候用 expanding？**
- 累計統計：年度累計、客戶終身價值
- 增量計算：逐漸更新的平均值

**Q: 如何處理缺失日期？**
```python
# 方法 1: 重新索引
df = df.reindex(pd.date_range(start, end, freq='D'))

# 方法 2: 填補
df = df.fillna(method='ffill')  # 向前填充
```

---

## 8. 下一步

✅ 理解了核心概念
↓
📖 閱讀詳細指南（Day 5-8）
↓
✍️ 完成練習題（32 題）
↓
🚀 應用到實際項目

---

**建議耗時：** 5 分鐘閱讀 + 5 分鐘代碼實驗

**進度檢查：**
- [ ] 理解 DateTime、Resample、Rolling、Shift 四個核心概念
- [ ] 能夠執行完整示例代碼
- [ ] 知道去哪裡找詳細教學

---

**準備好了嗎？** → 前往 [Day 5: DateTime 主要指南](Day05_DateTime_Mastery_Guide.md)
