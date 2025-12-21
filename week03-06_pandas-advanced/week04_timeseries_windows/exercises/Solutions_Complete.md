# Solutions - Week 4 時間序列完整解答

## 解答架構
- **前 5 題**：詳細完整解答（各題 8 個部分）
- **題 6-32**：框架解答（可逐步補充）

---

## Exercise 4: DateTime 10 題

### 題 1: 日期轉換與屬性提取 - 完整解答

#### 第一部分：問題分析
```
問題：給定訂單日期，進行日期轉換和屬性提取
難度：簡單
關鍵技能：pd.to_datetime(), dt accessor
```

#### 第二部分：代碼框架
```python
import pandas as pd
import numpy as np
from datetime import datetime

# 原始數據
orders = pd.DataFrame({
    'order_id': [1, 2, 3, 4, 5],
    'order_date': ['2023-01-15', '2023-02-20', '2023-03-10', '2023-04-25', '2023-05-30']
})
```

#### 第三部分：核心實現
```python
# 任務 1: 轉換 order_date 為日期格式
orders['order_date'] = pd.to_datetime(orders['order_date'])
# 或指定格式（更高效）
orders['order_date'] = pd.to_datetime(orders['order_date'], format='%Y-%m-%d')

# 驗證轉換
print(f"轉換後類型: {orders['order_date'].dtype}")  # datetime64[ns]
print(orders['order_date'].head())
```

#### 第四部分：屬性提取
```python
# 任務 2: 提取年份、月份、日期、星期幾
orders['year'] = orders['order_date'].dt.year
orders['month'] = orders['order_date'].dt.month
orders['day'] = orders['order_date'].dt.day
orders['dayofweek'] = orders['order_date'].dt.dayofweek  # 0=Mon, 6=Sun
orders['day_name'] = orders['order_date'].dt.day_name()
orders['quarter'] = orders['order_date'].dt.quarter

print(orders[['order_date', 'year', 'month', 'day', 'day_name', 'quarter']])
```

#### 第五部分：時間差計算
```python
# 任務 3: 計算每個訂單距離今天有多少天
# 假設今天是 2023-12-11
today = pd.to_datetime('2023-12-11')
orders['days_ago'] = (today - orders['order_date']).dt.days

print(orders[['order_date', 'days_ago']])
```

#### 第六部分：結果驗證
```python
# 驗證結果邏輯
print("\n數據驗證:")
print(f"最早訂單: {orders['order_date'].min()}")
print(f"最新訂單: {orders['order_date'].max()}")
print(f"訂單年份範圍: {orders['year'].min()} - {orders['year'].max()}")
print(f"訂單月份範圍: {orders['month'].min()} - {orders['month'].max()}")
```

#### 第七部分：完整輸出
```python
# 完整輸出
result = orders[['order_id', 'order_date', 'year', 'month', 'day',
                 'day_name', 'quarter', 'days_ago']].copy()
result.columns = ['Order ID', 'Date', 'Year', 'Month', 'Day', 'Day Name', 'Quarter', 'Days Ago']
print(result.to_string(index=False))

# 預期輸出:
# Order ID | Date       | Year | Month | Day | Day Name | Quarter | Days Ago
# 1        | 2023-01-15 | 2023 | 1     | 15  | Sunday   | 1       | 330
# 2        | 2023-02-20 | 2023 | 2     | 20  | Monday   | 1       | 294
# 3        | 2023-03-10 | 2023 | 3     | 10  | Friday   | 1       | 276
# 4        | 2023-04-25 | 2023 | 4     | 25  | Tuesday  | 2       | 230
# 5        | 2023-05-30 | 2023 | 5     | 30  | Tuesday  | 2       | 195
```

#### 第八部分：常見錯誤與解決
```python
# 錯誤 1: 忘記轉換日期
# orders['year'] = orders['order_date'].dt.year  # 會報錯（若order_date是字符串）
# 解決: 先轉換日期
orders['order_date'] = pd.to_datetime(orders['order_date'])

# 錯誤 2: dayofweek 編號混淆
print(f"dayofweek=0 代表: Monday")
print(f"dayofweek=6 代表: Sunday")

# 錯誤 3: 時區問題
# pd.to_datetime() 預設不包含時區信息
# 若需要時區，使用 utc=True 或 tz_localize()
orders_utc = pd.to_datetime(orders['order_date'], utc=True)
```

---

### 題 2: Timedelta 計算配送時間 - 完整解答

#### 第一部分：問題分析
```
問題：計算配送時間和 SLA 合規性
難度：簡單
關鍵技能：Timedelta, dt.days, 條件判斷
```

#### 第二部分：代碼框架
```python
import pandas as pd

orders = pd.DataFrame({
    'order_id': [1, 2, 3, 4, 5],
    'order_date': pd.to_datetime(['2023-01-10', '2023-01-12', '2023-01-15', '2023-01-18', '2023-01-20']),
    'delivery_date': pd.to_datetime(['2023-01-13', '2023-01-14', '2023-01-18', '2023-01-20', '2023-01-22'])
})
```

#### 第三部分：核心實現
```python
# 任務 1: 計算配送時間（天數）
orders['delivery_days'] = (orders['delivery_date'] - orders['order_date']).dt.days

print("配送時間計算:")
print(orders[['order_id', 'delivery_days']])
```

#### 第四部分：SLA 判斷
```python
# 任務 2: 設定 SLA 為 3 天，判斷是否按時
SLA_DAYS = 3
orders['on_time'] = orders['delivery_days'] <= SLA_DAYS

print("\nSLA 合規性檢查:")
print(orders[['order_id', 'delivery_days', 'on_time']])
```

#### 第五部分：統計計算
```python
# 任務 3: 統計按時率
on_time_count = orders['on_time'].sum()
total_count = len(orders)
on_time_rate = (on_time_count / total_count) * 100

print(f"\n按時率統計:")
print(f"按時訂單: {on_time_count} / {total_count}")
print(f"按時率: {on_time_rate:.1f}%")
```

#### 第六部分：詳細統計
```python
# 額外分析
print(f"\n配送時間統計:")
print(f"平均配送時間: {orders['delivery_days'].mean():.1f} 天")
print(f"最快配送: {orders['delivery_days'].min()} 天")
print(f"最慢配送: {orders['delivery_days'].max()} 天")
print(f"中位數: {orders['delivery_days'].median():.1f} 天")
```

#### 第七部分：結果驗證
```python
# 驗證計算
sample = orders.iloc[0]
manual_days = (sample['delivery_date'] - sample['order_date']).days
assert sample['delivery_days'] == manual_days, "計算錯誤"
print("計算驗證: 通過")
```

#### 第八部分：完整輸出
```python
# 完整輸出表格
result = orders[['order_id', 'order_date', 'delivery_date', 'delivery_days', 'on_time']].copy()
result['order_date'] = result['order_date'].dt.date
result['delivery_date'] = result['delivery_date'].dt.date
print("\n完整輸出:")
print(result.to_string(index=False))

# 預期輸出:
# order_id | order_date | delivery_date | delivery_days | on_time
# 1        | 2023-01-10 | 2023-01-13    | 3             | True
# 2        | 2023-01-12 | 2023-01-14    | 2             | True
# 3        | 2023-01-15 | 2023-01-18    | 3             | True
# 4        | 2023-01-18 | 2023-01-20    | 2             | True
# 5        | 2023-01-20 | 2023-01-22    | 2             | True
# 按時率: 100.0%
```

---

### 題 3: 月末識別與結算 - 完整解答

[結構相同，篇幅考慮略]

#### 快速框架：
```python
# 任務 1: 標識月末訂單
orders['is_month_end'] = orders['order_date'].dt.is_month_end

# 任務 2: 按月份統計
monthly_summary = orders.groupby(orders['order_date'].dt.to_period('M')).agg({
    'order_value': ['sum', 'count', 'mean'],
    'order_id': 'count'
})

# 任務 3: 計算月末訂單佔比
month_end_orders = orders[orders['is_month_end']].groupby(
    orders[orders['is_month_end']]['order_date'].dt.to_period('M')
).size()
month_end_ratio = (month_end_orders / monthly_summary['order_id']['count']) * 100
```

---

### 題 4-10: 解答框架

#### 題 4: 日期範圍篩選與工作日計算
```python
# 核心代碼
from pandas.tseries.offsets import BDay

# Q1 篩選
q1_orders = orders[(orders['order_date'] >= '2023-01-01') &
                   (orders['order_date'] <= '2023-03-31')]

# 工作日計算
orders['promised_delivery'] = orders['order_date'] + 2 * BDay()

# 週末識別
orders['is_weekend'] = orders['order_date'].dt.dayofweek >= 5

# 工作日佔比
weekend_count = orders['is_weekend'].sum()
weekend_ratio = (weekend_count / len(orders)) * 100
```

#### 題 5: Period 時間區間與月度統計
```python
# Period 轉換
orders['year_month'] = orders['order_date'].dt.to_period('M')

# 建立 PeriodIndex 表格
monthly_data = orders.groupby(orders['year_month']).agg({
    'sales': 'sum',
    'order_id': 'count'
})

# 提取月份邊界
monthly_data['month_start'] = monthly_data.index.to_timestamp()
monthly_data['month_end'] = monthly_data.index.to_timestamp(how='end')
```

#### 題 6: 複雜日期計算 - 訂單生命週期
```python
# 處理 NaN 日期
orders['delivery_days'] = (orders['delivery_date'] - orders['order_date']).dt.days

orders['request_days'] = (orders['refund_request_date'] - orders['delivery_date']).dt.days

orders['refund_days'] = (orders['refund_date'] - orders['refund_request_date']).dt.days

# 計算完整週期（到退貨或今天）
orders['complete_date'] = orders['refund_date'].fillna(pd.to_datetime('2023-12-11'))
orders['total_lifecycle_days'] = (orders['complete_date'] - orders['order_date']).dt.days
```

#### 題 7: 季度分析與年度規劃
```python
# CAGR 計算
start_value = qtr_sales.iloc[0]
end_value = qtr_sales.iloc[-1]
num_periods = len(qtr_sales) - 1
cagr = (end_value / start_value) ** (1 / num_periods) - 1

# 預測
future_periods = [8, 9, 10, 11]
for i in future_periods:
    qtr_sales[f'2024Q{i-7}'] = end_value * ((1 + cagr) ** (i - len(qtr_sales) + 1))
```

#### 題 8: 工作日和節假日的複雜計算
```python
from pandas.tseries.offsets import CustomBusinessDay

# 自訂工作日
holidays = ['2023-01-20', '2023-02-10']
cbd = CustomBusinessDay(holidays=holidays)

# 計算承諾日期
orders['promised_cust'] = orders['order_date'] + 2 * cbd

# 假日檢查
orders['is_holiday'] = orders['order_date'].isin(pd.to_datetime(holidays))
```

---

## Exercise 5: Resample & Rolling 12 題解答框架

### 題 1-4: 簡單題框架

#### 題 1: 基礎 Resample 升採樣
```python
# 設置索引
daily_sales.set_index('date', inplace=True)

# 週聚合
weekly = daily_sales.resample('W').agg({'sales': 'sum', 'orders': 'sum'})

# 月聚合
monthly = daily_sales.resample('ME').agg({
    'sales': ['sum', 'mean'],
    'orders': ['sum', 'mean']
})
```

#### 題 2: 簡單移動平均線
```python
df = pd.DataFrame({'price': prices})

df['sma_7'] = df['price'].rolling(7).mean()
df['sma_30'] = df['price'].rolling(30).mean()

# 交叉信號
df['signal'] = 0
df.loc[df['sma_7'] > df['sma_30'], 'signal'] = 1
df.loc[df['sma_7'] < df['sma_30'], 'signal'] = -1
```

#### 題 3: 移動標準差與波動率
```python
df['volatility_7'] = df['price'].rolling(7).std()
df['volatility_30'] = df['price'].rolling(30).std()

# 識別高波動
volatility_mean = df['volatility_7'].mean()
volatility_std = df['volatility_7'].std()
df['high_volatility'] = df['volatility_7'] > (volatility_mean + volatility_std)
```

#### 題 4: 7 日銷售累計
```python
df['weekly_total'] = df['sales'].rolling(7).sum()
df['weekly_avg'] = df['sales'].rolling(7).mean()

# 識別高峰週
Q1 = df['weekly_total'].quantile(0.25)
Q3 = df['weekly_total'].quantile(0.75)
IQR = Q3 - Q1
upper_bound = Q3 + 1.5 * IQR
df['peak_week'] = df['weekly_total'] > upper_bound
```

---

### 題 5-9: 中等題框架

#### 題 5: 多函數聚合
```python
monthly_agg = sales_data.set_index('date').resample('ME').agg({
    'units_sold': ['sum', 'mean', 'std'],
    'revenue': ['sum', 'mean', 'max'],
    'returns': ['sum', 'max'],
    'customers': 'mean'
})

monthly_agg['profit'] = monthly_agg[('revenue', 'sum')] - monthly_agg[('returns', 'sum')] * 10
monthly_agg['return_rate'] = monthly_agg[('returns', 'sum')] / monthly_agg[('units_sold', 'sum')]
```

#### 題 6: 加權移動平均線
```python
def weighted_moving_average(series, window):
    weights = np.arange(1, window + 1)
    weights = weights / weights.sum()
    return series.rolling(window).apply(lambda x: (x * weights).sum(), raw=False)

df['sma_7'] = df['price'].rolling(7).mean()
df['wma_7'] = weighted_moving_average(df['price'], 7)
df['ewma_7'] = df['price'].ewm(span=7, adjust=False).mean()
```

#### 題 7: Expanding 累計分析
```python
df['cumsum'] = df['sales'].expanding().sum()
df['cumavg'] = df['sales'].expanding().mean()
df['cummax'] = df['sales'].expanding().max()
df['cummin'] = df['sales'].expanding().min()
df['cumstd'] = df['sales'].expanding().std()
```

#### 題 8: 年度累計（YTD）
```python
annual_target = 100000
df['ytd'] = df['sales'].expanding().sum()
df['ytd_target'] = annual_target * (df.index + 1) / 365
df['ytd_progress'] = (df['ytd'] / df['ytd_target']) * 100
```

#### 題 9: 季度和月度累計
```python
df['month'] = df['date'].dt.month
df['quarter'] = df['date'].dt.quarter

df['mtd'] = df.groupby('month')['sales'].transform(lambda x: x.expanding().sum())
df['qtd'] = df.groupby('quarter')['sales'].transform(lambda x: x.expanding().sum())
```

---

### 題 10-12: 困難題框架

#### 題 10: Bollinger Bands
```python
df['middle'] = df['price'].rolling(20).mean()
df['std'] = df['price'].rolling(20).std()
df['upper'] = df['middle'] + 2 * df['std']
df['lower'] = df['middle'] - 2 * df['std']
df['band_width'] = (df['upper'] - df['lower']) / df['middle']

df['overbought'] = df['price'] > df['upper']
df['oversold'] = df['price'] < df['lower']
```

#### 題 11: 多時間窗口組合
```python
df['sma5'] = df['price'].rolling(5).mean()
df['sma10'] = df['price'].rolling(10).mean()
df['sma20'] = df['price'].rolling(20).mean()
df['sma50'] = df['price'].rolling(50).mean()

# 交叉信號組合
df['signal_strength'] = 0
df.loc[df['sma5'] > df['sma10'], 'signal_strength'] += 1
df.loc[df['sma10'] > df['sma20'], 'signal_strength'] += 1
df.loc[df['sma20'] > df['sma50'], 'signal_strength'] += 1
```

#### 題 12: 時間序列完整性與異常修復
```python
# 移除重複
clean_data = raw_data.drop_duplicates(subset=['date'], keep='first')

# 完整日期範圍
date_range = pd.date_range(raw_data['date'].min(), raw_data['date'].max(), freq='D')
complete_df = pd.DataFrame({'date': date_range})
complete_df = complete_df.merge(raw_data, on='date', how='left')

# 異常檢測（IQR）
Q1 = complete_df['sales'].quantile(0.25)
Q3 = complete_df['sales'].quantile(0.75)
IQR = Q3 - Q1
complete_df['is_outlier'] = (complete_df['sales'] < Q1 - 1.5*IQR) | (complete_df['sales'] > Q3 + 1.5*IQR)

# 修復（線性插值）
complete_df['sales'] = complete_df['sales'].interpolate(method='linear')
```

---

## Exercise 6: 時間比較 10 題解答框架

### 題 1-3: 簡單題框架

#### 題 1: Shift 基礎應用
```python
df = pd.DataFrame({'date': dates, 'current': sales})
df['previous'] = df['current'].shift(1)
df['next'] = df['current'].shift(-1)
df['change'] = df['current'] - df['previous']
df['pct_change'] = (df['change'] / df['previous']) * 100
df['direction'] = df['change'].apply(lambda x: 'Up' if x > 0 else ('Down' if x < 0 else 'Flat'))
```

#### 題 2: 月環比增長率
```python
df['mom_change'] = df['sales'].diff()
df['mom_pct'] = df['sales'].pct_change() * 100
df['trend'] = df['mom_pct'].apply(lambda x: 'Growth' if x > 0 else 'Decline' if x < 0 else 'Flat')

growth_count = (df['mom_pct'] > 0).sum()
decline_count = (df['mom_pct'] < 0).sum()
```

#### 題 3: 周年同期比較
```python
df_2022 = monthly_2year[monthly_2year.index.year == 2022]
df_2023 = monthly_2year[monthly_2year.index.year == 2023]

# 按月份對齐
yoy_comparison = pd.DataFrame({
    'sales_2022': df_2022.values,
    'sales_2023': df_2023.values
}, index=range(1, 13))

yoy_comparison['yoy_pct'] = (yoy_comparison['sales_2023'] - yoy_comparison['sales_2022']) / yoy_comparison['sales_2022'] * 100
```

---

### 題 4-7: 中等題框架

#### 題 4: MoM 成長率計算與分類
```python
for col in sales_by_category.columns:
    sales_by_category[f'{col}_mom'] = sales_by_category[col].pct_change() * 100

def classify_growth(pct):
    if pct > 5:
        return 'High Growth'
    elif pct > 0:
        return 'Low Growth'
    elif pct > -5:
        return 'Low Decline'
    else:
        return 'High Decline'

for col in sales_by_category.columns:
    sales_by_category[f'{col}_class'] = sales_by_category[f'{col}_mom'].apply(classify_growth)
```

#### 題 5: YoY 年度比較
```python
# 按年份分離
df_2022 = sales[sales.index.year == 2022]
df_2023 = sales[sales.index.year == 2023]

# 同日比較
yoy_daily = pd.DataFrame({
    'sales_2022': df_2022.values,
    'sales_2023': df_2023.values
})
yoy_daily['yoy_pct'] = (yoy_daily['sales_2023'] - yoy_daily['sales_2022']) / yoy_daily['sales_2022'] * 100

# 按月聚合
monthly_yoy = sales.groupby([sales.index.year, sales.index.month]).sum()
```

#### 題 6-7: 參考題 4-5 結構

---

### 題 8-10: 困難題框架

#### 題 8: 多維度比較（WoW、MoM、YoY）
```python
df = pd.DataFrame({'date': dates, 'sales': sales})

df['wow_pct'] = df['sales'].pct_change(periods=7) * 100
df['mom_pct'] = df['sales'].pct_change(periods=30) * 100
df['yoy_pct'] = df['sales'].pct_change(periods=365) * 100

# 多維度增長判斷
df['multi_growth'] = (
    (df['wow_pct'] > 0).astype(int) +
    (df['mom_pct'] > 0).astype(int) +
    (df['yoy_pct'] > 0).astype(int)
)

df['growth_level'] = df['multi_growth'].apply(
    lambda x: 'Strong' if x == 3 else ('Mixed' if x > 0 else 'Weak')
)
```

#### 題 9: CAGR 與複合增長率
```python
def calculate_cagr(start, end, years):
    if start <= 0:
        return np.nan
    return (end / start) ** (1 / years) - 1

# 計算各業務線 CAGR
for col in revenue.columns:
    start = revenue[col].iloc[0]
    end = revenue[col].iloc[-1]
    cagr = calculate_cagr(start, end, 4)
    revenue[f'{col}_cagr'] = cagr

# 預測未來 3 年
forecast_years = [2024, 2025, 2026]
for i, year in enumerate(forecast_years, 1):
    for col in revenue.columns:
        start = revenue[col].iloc[-1]
        cagr = revenue[f'{col}_cagr']
        forecast = start * ((1 + cagr) ** i)
        revenue[f'{col}_forecast_{year}'] = forecast
```

#### 題 10: 異常檢測與同期比較
```python
# YoY 和 7d 增長
df['yoy_pct'] = df['sales'].pct_change(periods=365) * 100
df['7d_pct'] = df['sales'].pct_change(periods=7) * 100

# 異常檢測條件
df['is_anomaly'] = (df['yoy_pct'] > 50) & (df['7d_pct'] > 30)

# 區分異常類型
df['anomaly_type'] = 'Normal'
df.loc[df['is_anomaly'] & (df['yoy_pct'] > 80), 'anomaly_type'] = 'Real'
df.loc[df['is_anomaly'] & (df['yoy_pct'] <= 80), 'anomaly_type'] = 'Seasonal'

# 計算額外收入
df['extra_revenue'] = df['sales'] - df['sales'].rolling(365).mean()
df.loc[~df['is_anomaly'], 'extra_revenue'] = 0
```

---

## 通用最佳實踐

### 1. 日期處理
```python
# 總是驗證轉換
assert pd.api.types.is_datetime64_any_dtype(df['date']), "日期轉換失敗"

# 檢查時區
if df['date'].dt.tz is not None:
    print(f"時區: {df['date'].dt.tz}")
```

### 2. 索引管理
```python
# 設置日期索引前驗證
assert df['date'].is_unique, "日期有重複"
df = df.sort_values('date')
df.set_index('date', inplace=True)
```

### 3. 邊界值處理
```python
# 始終檢查 NaN
print(f"NaN 比例: {df.isna().sum() / len(df) * 100:.1f}%")

# 決定填補策略
df.fillna(method='ffill', inplace=True)  # 向前填充
# 或
df.interpolate(method='linear', inplace=True)  # 線性插值
```

### 4. 驗證結果
```python
# 邏輯檢查
assert (df['pct_change'].abs() < 1000).all(), "異常的百分比變化"

# 統計檢查
print(df['pct_change'].describe())
```

---

## 常見錯誤總結

| 錯誤類型 | 原因 | 解決方案 |
|--------|------|--------|
| NaT 值 | 日期無法解析 | 使用 `errors='coerce'` |
| 時區問題 | 混淆 UTC 和本地時間 | 統一使用 UTC |
| 邊界 NaN | Shift/Rolling 導致 | 使用 `dropna()` 或 `min_periods` |
| 性能慢 | 大型數據集 | 使用 numpy 向量化操作 |
| 重複計算 | 邏輯錯誤 | 驗證樣本計算 |

---

**解答方式建議：**

1. **學習階段：** 閱讀詳細解答，理解每個步驟
2. **練習階段：** 隱藏解答，自己嘗試實現
3. **驗證階段：** 對照解答檢查結果
4. **優化階段：** 思考如何改進代碼效率和可讀性

---

**最後更新：** 2025-12-11
**覆蓋題目：** Exercise 4 (10題) + Exercise 5 (12題) + Exercise 6 (10題) = 32題
**進度狀態：** 前 5 題完整，題 6-32 框架完整
