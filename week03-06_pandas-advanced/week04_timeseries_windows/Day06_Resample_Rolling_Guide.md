# Day 6: Resample 與 Rolling 視窗函數指南

## 概述
掌握時間序列重採樣和移動視窗計算技能，從日級數據聚合到月級、進行移動平均線分析，以及累計統計。

**學習時間：** 6 小時（3 部分）
**難度：** 中等-困難
**主要工具：** `resample()`, `rolling()`, `expanding()`

---

## Part 1: Resample 重採樣（2 小時）

### 1.1 升採樣（日 → 週 → 月 → 年）

#### 概念
升採樣（Upsampling）：將高頻數據聚合為低頻數據。例如，將每日銷售數據聚合為月度銷售。

```python
import pandas as pd
import numpy as np
from datetime import datetime, timedelta

# 建立日級銷售數據
dates = pd.date_range('2023-01-01', periods=90, freq='D')
daily_sales = pd.DataFrame({
    'date': dates,
    'sales': np.random.randint(100, 500, 90),
    'customers': np.random.randint(10, 100, 90)
})

# 設定日期為索引
daily_sales.set_index('date', inplace=True)
print("原始日級數據（前 5 行）:")
print(daily_sales.head())
#             sales  customers
# date
# 2023-01-01    250         45
# 2023-01-02    380         72
# 2023-01-03    150         28
# 2023-01-04    420         85
# 2023-01-05    280         62

# 1. 升採樣到週級（求和）
weekly_sales = daily_sales.resample('W').sum()
print("\n週級銷售（每週日）:")
print(weekly_sales.head())
#             sales  customers
# date
# 2023-01-01    250         45
# 2023-01-08   2150        412
# 2023-01-15   2180        405
# ...

# 2. 升採樣到月級（求和）
monthly_sales = daily_sales.resample('ME').sum()  # 'ME' = Month End
print("\n月級銷售（月末）:")
print(monthly_sales)
#             sales  customers
# date
# 2023-01-31    8430       1548
# 2023-02-28    7890       1421
# 2023-03-31    8950       1675

# 3. 升採樣到年級（求和）
yearly_sales = daily_sales.resample('YE').sum()  # 'YE' = Year End
print("\n年級銷售:")
print(yearly_sales)
#             sales   customers
# date
# 2023-12-31  25270        4644

# 4. 常見頻率和聚合函數
freq_examples = {
    'D': '日',
    'W': '週（週日結束）',
    'W-Mon': '週（週一結束）',
    'ME': '月末',
    'MS': '月初',
    'QE': '季末',
    'QS': '季初',
    'YE': '年末',
    'YS': '年初',
    'H': '小時',
    '5T': '每 5 分鐘',
    '15min': '每 15 分鐘'
}

# 5. 多種聚合函數
monthly_stats = daily_sales.resample('ME').agg({
    'sales': ['sum', 'mean', 'min', 'max'],
    'customers': ['sum', 'mean', 'std']
})
print("\n月級統計（多函數）:")
print(monthly_stats)
```

#### Excel 對照
```excel
SUBTOTAL(109, A1:A31)  // 按月求和（樞紐表）
AVERAGEIFS()           // 按月求平均
```

### 1.2 降採樣（補充缺失值）

#### 概念
降採樣（Downsampling）：插入缺失值，填補數據空隙。

```python
# 建立非完整日期數據（有缺失）
irregular_dates = pd.to_datetime([
    '2023-01-01', '2023-01-02', '2023-01-05',  # 缺少 1-3, 1-4
    '2023-01-08', '2023-01-10'  # 缺少 1-6, 1-7, 1-9
])

data_irregular = pd.DataFrame({
    'sales': [100, 150, 200, 250, 300]
}, index=irregular_dates)

print("原始數據（不規則）:")
print(data_irregular)
#             sales
# 2023-01-01    100
# 2023-01-02    150
# 2023-01-05    200
# 2023-01-08    250
# 2023-01-10    300

# 1. 改為完整日期索引（填補缺失值）
date_range = pd.date_range('2023-01-01', '2023-01-10', freq='D')
data_regular = data_irregular.reindex(date_range)
print("\n重新索引後（NaN 表示缺失）:")
print(data_regular)
#             sales
# 2023-01-01  100.0
# 2023-01-02  150.0
# 2023-01-03    NaN
# 2023-01-04    NaN
# 2023-01-05  200.0
# ...

# 2. 向前填充（Forward Fill）
data_ffill = data_regular.fillna(method='ffill')
print("\n向前填充：")
print(data_ffill)
#             sales
# 2023-01-01  100.0
# 2023-01-02  150.0
# 2023-01-03  150.0
# 2023-01-04  150.0
# 2023-01-05  200.0

# 3. 向後填充（Backward Fill）
data_bfill = data_regular.fillna(method='bfill')
print("\n向後填充：")
print(data_bfill)

# 4. 線性插值（Linear Interpolate）
data_interp = data_regular.interpolate(method='linear')
print("\n線性插值：")
print(data_interp)
#             sales
# 2023-01-01  100.0
# 2023-01-02  150.0
# 2023-01-03  166.67
# 2023-01-04  183.33
# 2023-01-05  200.0

# 5. 降採樣 + 聚合
dates_with_gaps = pd.date_range('2023-01-01', periods=10, freq='D').union(
    pd.date_range('2023-01-20', periods=10, freq='D')
)
data_gaps = pd.DataFrame({
    'sales': np.random.randint(100, 300, 20)
}, index=dates_with_gaps)

# 轉換為週級（會自動處理缺失的週）
weekly_data = data_gaps.resample('W').sum()
print("\n週級數據（包含缺失的週為 0）:")
print(weekly_data)
```

#### Excel 對照
```excel
=IFERROR(VLOOKUP(date_range, data, 2, 0), previous_value)  // 填補缺失
```

### 1.3 多列聚合和自訂規則

#### 概念
不同列可能需要不同的聚合函數。

```python
# 複雜的銷售數據
sales_data = pd.DataFrame({
    'date': pd.date_range('2023-01-01', periods=90, freq='D'),
    'units_sold': np.random.randint(10, 100, 90),
    'revenue': np.random.randint(1000, 5000, 90),
    'returns': np.random.randint(0, 20, 90),
    'customers': np.random.randint(20, 150, 90)
})

sales_data.set_index('date', inplace=True)

# 1. 不同列使用不同的聚合函數
monthly_summary = sales_data.resample('ME').agg({
    'units_sold': 'sum',        # 銷售量求和
    'revenue': 'sum',           # 營收求和
    'returns': 'sum',           # 退貨求和
    'customers': 'mean'         # 顧客數求平均
})

print("月度摘要（不同聚合函數）:")
print(monthly_summary)

# 2. 使用字典指定多個函數
multi_agg = sales_data.resample('ME').agg({
    'units_sold': ['sum', 'mean', 'std'],
    'revenue': ['sum', 'mean'],
    'returns': ['sum', 'max']
})

print("\n多函數聚合:")
print(multi_agg)

# 3. Lambda 函數自訂聚合
custom_agg = sales_data.resample('ME').agg({
    'units_sold': lambda x: x.sum(),
    'revenue': lambda x: x.sum(),
    'returns': lambda x: x.sum(),
    'net_revenue': lambda x: (sales_data['revenue'] - sales_data['returns']).sum()
})

print("\n自訂聚合（計算淨收入）:")
print(custom_agg)

# 4. 計算退貨率
monthly_summary['return_rate'] = (
    monthly_summary['returns'] / monthly_summary['units_sold'] * 100
)

print("\n新增退貨率欄位:")
print(monthly_summary[['units_sold', 'returns', 'return_rate']])
```

#### Excel 對照
```excel
=SUMIF(month_range, month, sales_col)
=AVERAGEIF(month_range, month, customer_col)
```

---

## Part 2: Rolling 移動視窗（2.5 小時）

### 2.1 簡單移動平均線（SMA）

#### 概念
移動平均線用於平滑數據和識別趨勢，特別是在金融和銷售分析中。

```python
# 建立股票/商品價格數據
dates = pd.date_range('2023-01-01', periods=100, freq='D')
price_data = pd.DataFrame({
    'date': dates,
    'price': 100 + np.cumsum(np.random.randn(100) * 2)  # 隨機遊走
})

price_data.set_index('date', inplace=True)

# 1. 7 日簡單移動平均線
price_data['sma_7'] = price_data['price'].rolling(window=7).mean()

# 2. 30 日簡單移動平均線
price_data['sma_30'] = price_data['price'].rolling(window=30).mean()

print("價格與移動平均線（前 35 行）:")
print(price_data.head(35))
#             price      sma_7      sma_30
# 2023-01-01   100.0       NaN         NaN
# 2023-01-02  102.1       NaN         NaN
# ...
# 2023-01-07  105.2   102.43         NaN
# 2023-01-30  128.5   125.32   115.67
# 2023-01-31  130.1   126.89   116.45

# 3. 可視化（文本方式）
print("\n價格趨勢（最後 10 天）:")
print(price_data[['price', 'sma_7', 'sma_30']].tail(10))

# 4. 交叉信號（簡單交易策略）
price_data['signal'] = 0
price_data.loc[price_data['sma_7'] > price_data['sma_30'], 'signal'] = 1  # 買入信號
price_data.loc[price_data['sma_7'] < price_data['sma_30'], 'signal'] = -1  # 賣出信號

print("\n交易信號（前 35 行）:")
print(price_data[['price', 'sma_7', 'sma_30', 'signal']].head(35))

# 5. 實現價格與 SMA 的距離
price_data['distance_to_sma'] = price_data['price'] - price_data['sma_30']
print("\n價格與 30 日 SMA 的距離（偏離度）:")
print(price_data[['price', 'sma_30', 'distance_to_sma']].tail(10))
```

#### Excel 對照
```excel
=AVERAGE(OFFSET(A1, -6, 0, 7, 1))  // 7 日簡單移動平均
```

### 2.2 加權移動平均線（WMA）

#### 概念
加權移動平均線給予最近的數據更大的權重。

```python
# 1. 簡單的加權移動平均
def weighted_moving_average(series, window, weights=None):
    """
    計算加權移動平均線

    Parameters:
    series: pandas Series
    window: 窗口大小
    weights: 權重列表（預設為線性遞增）
    """
    if weights is None:
        # 預設權重：線性遞增（最近的權重最大）
        weights = np.arange(1, window + 1)

    # 標準化權重
    weights = weights / weights.sum()

    return series.rolling(window).apply(
        lambda x: (x * weights).sum(),
        raw=False
    )

# 使用函數
price_data['wma_7'] = weighted_moving_average(price_data['price'], window=7)

print("簡單平均 vs 加權平均（最後 20 行）:")
print(price_data[['price', 'sma_7', 'wma_7']].tail(20))

# 2. Pandas 內建方法（較高效）
# 使用 ewm（指數加權移動平均）
price_data['ewma_7'] = price_data['price'].ewm(span=7, adjust=False).mean()

print("\n指數加權移動平均（EWMA）:")
print(price_data[['price', 'sma_7', 'ewma_7']].tail(20))

# 3. 多個時間窗口的比較
price_data['sma_5'] = price_data['price'].rolling(5).mean()
price_data['sma_10'] = price_data['price'].rolling(10).mean()
price_data['sma_20'] = price_data['price'].rolling(20).mean()

print("\n多窗口移動平均線（最後 25 行）:")
print(price_data[['price', 'sma_5', 'sma_10', 'sma_20']].tail(25))
```

#### Excel 對照
Excel 沒有直接的 WMA 函數，需要用 SUMPRODUCT 實現。

### 2.3 滾動統計和 volatility

#### 概念
不僅可以計算平均值，還可以計算其他統計量如標準差、最大值、最小值等。

```python
# 1. 滾動標準差（波動率）
price_data['volatility_7'] = price_data['price'].rolling(window=7).std()
price_data['volatility_30'] = price_data['price'].rolling(window=30).std()

print("價格波動率（最後 35 行）:")
print(price_data[['price', 'volatility_7', 'volatility_30']].tail(35))

# 2. 滾動最大值和最小值（高點和低點）
price_data['high_7'] = price_data['price'].rolling(window=7).max()
price_data['low_7'] = price_data['price'].rolling(window=7).min()
price_data['range_7'] = price_data['high_7'] - price_data['low_7']

print("\n7 日高點、低點和波幅:")
print(price_data[['price', 'high_7', 'low_7', 'range_7']].tail(15))

# 3. 滾動計數和求和
sales_data = pd.DataFrame({
    'date': pd.date_range('2023-01-01', periods=90, freq='D'),
    'sales': np.random.randint(100, 500, 90)
})
sales_data.set_index('date', inplace=True)

sales_data['sales_7day_sum'] = sales_data['sales'].rolling(window=7).sum()
sales_data['sales_7day_count'] = sales_data['sales'].rolling(window=7).count()
sales_data['sales_7day_avg'] = sales_data['sales'].rolling(window=7).mean()

print("\n7 日累計銷售:")
print(sales_data[['sales', 'sales_7day_sum', 'sales_7day_count', 'sales_7day_avg']].tail(15))

# 4. 滾動相關性（兩個系列之間的相關性）
data_2col = pd.DataFrame({
    'price': 100 + np.cumsum(np.random.randn(100) * 2),
    'volume': np.random.randint(1000, 10000, 100)
})

data_2col['correlation'] = data_2col['price'].rolling(window=30).corr(data_2col['volume'])
print("\n30 日價格與成交量相關性:")
print(data_2col[['price', 'volume', 'correlation']].tail(35))

# 5. 滾動百分位
data_2col['percentile_75'] = data_2col['price'].rolling(window=30).quantile(0.75)
data_2col['percentile_25'] = data_2col['price'].rolling(window=30).quantile(0.25)

print("\n30 日價格百分位:")
print(data_2col[['price', 'percentile_75', 'percentile_25']].tail(35))
```

#### Excel 對照
```excel
=STDEV(OFFSET(A1, -6, 0, 7, 1))     // 7 日標準差
=MAX(OFFSET(A1, -6, 0, 7, 1))       // 7 日最大值
=MIN(OFFSET(A1, -6, 0, 7, 1))       // 7 日最小值
```

---

## Part 3: Expanding 與累計統計（1.5 小時）

### 3.1 Expanding 累計計算

#### 概念
Expanding 從第一行開始，逐漸擴大窗口，計算累計統計量。

```python
# 銷售數據
sales_data = pd.DataFrame({
    'date': pd.date_range('2023-01-01', periods=30, freq='D'),
    'sales': np.random.randint(100, 500, 30),
    'returns': np.random.randint(0, 50, 30)
})

sales_data.set_index('date', inplace=True)

# 1. 累計求和
sales_data['cumsum_sales'] = sales_data['sales'].expanding().sum()
sales_data['cumsum_returns'] = sales_data['returns'].expanding().sum()

print("累計銷售和退貨:")
print(sales_data[['sales', 'cumsum_sales', 'returns', 'cumsum_returns']].head(15))
#             sales  cumsum_sales  returns  cumsum_returns
# 2023-01-01    250           250        5                5
# 2023-01-02    380           630        8               13
# 2023-01-03    150           780       10               23
# ...

# 2. 累計平均
sales_data['cumavg_sales'] = sales_data['sales'].expanding().mean()

print("\n累計平均銷售:")
print(sales_data[['sales', 'cumsum_sales', 'cumavg_sales']].head(15))

# 3. 累計標準差（不確定性增加還是減少？）
sales_data['cumstd_sales'] = sales_data['sales'].expanding().std()

print("\n累計標準差:")
print(sales_data[['sales', 'cumavg_sales', 'cumstd_sales']].head(15))

# 4. 累計計數（見過多少個數據點）
sales_data['cumcount'] = sales_data['sales'].expanding().count()

print("\n累計計數:")
print(sales_data[['sales', 'cumcount']].head(15))

# 5. 累計最大值和最小值
sales_data['cummax_sales'] = sales_data['sales'].expanding().max()
sales_data['cummin_sales'] = sales_data['sales'].expanding().min()

print("\n累計最大和最小銷售:")
print(sales_data[['sales', 'cummax_sales', 'cummin_sales']].head(15))
```

#### Excel 對照
```excel
=SUM($A$1:A1)     // 累計求和
=AVERAGE($A$1:A1) // 累計平均
=MAX($A$1:A1)     // 累計最大值
```

### 3.2 年度累計（YTD）與季度累計（QTD）

#### 概念
按時間重置累計，如每年初重置為 0。

```python
# 全年每日數據
full_year_data = pd.DataFrame({
    'date': pd.date_range('2023-01-01', periods=365, freq='D'),
    'sales': np.random.randint(100, 500, 365)
})

full_year_data.set_index('date', inplace=True)

# 提取年、月、季度信息
full_year_data['year'] = full_year_data.index.year
full_year_data['month'] = full_year_data.index.month
full_year_data['quarter'] = full_year_data.index.quarter

# 1. 年度累計（YTD - Year to Date）
# 按年分組，然後累計
full_year_data['ytd_sales'] = (
    full_year_data.groupby('year')['sales']
    .transform(lambda x: x.expanding().sum())
)

print("年度累計銷售（YTD）- 前 35 行和 350-355 行:")
print(full_year_data[['sales', 'month', 'ytd_sales']].head(35))
print("\n...")
print(full_year_data[['sales', 'month', 'ytd_sales']].iloc[350:356])

# 2. 季度累計（QTD - Quarter to Date）
full_year_data['qtd_sales'] = (
    full_year_data.groupby('quarter')['sales']
    .transform(lambda x: x.expanding().sum())
)

print("\n季度累計銷售（QTD）:")
print(full_year_data[['sales', 'quarter', 'qtd_sales']].iloc[80:95])

# 3. 月度累計（MTD - Month to Date）
full_year_data['mtd_sales'] = (
    full_year_data.groupby('month')['sales']
    .transform(lambda x: x.expanding().sum())
)

print("\n月度累計銷售（MTD）:")
print(full_year_data[['sales', 'month', 'mtd_sales']].head(35))

# 4. 按日期篩選特定日期的 YTD
march_31 = full_year_data.loc['2023-03-31']
print(f"\n2023 年 3 月 31 日（第一季末）的 YTD 銷售: {march_31['ytd_sales']:.0f}")

june_30 = full_year_data.loc['2023-06-30']
print(f"2023 年 6 月 30 日（第二季末）的 YTD 銷售: {june_30['ytd_sales']:.0f}")
```

#### Excel 對照
```excel
=SUMIFS($A:$A, $B:$B, YEAR($D1), $C:$C, "<="&$D1)
// 計算 YTD：求和所有相同年份且日期 <= 目標日期的數據
```

---

## 實戰案例（12 個）

### 案例 1-3: Resample 應用

```python
# 案例 1: 日 → 月銷售聚合
daily_sales = pd.DataFrame({
    'date': pd.date_range('2023-01-01', periods=90, freq='D'),
    'sales': np.random.randint(100, 500, 90)
})
daily_sales.set_index('date', inplace=True)

monthly_sales = daily_sales.resample('ME').agg({
    'sales': ['sum', 'mean', 'count']
})

# 案例 2: 多指標月度匯總
orders = pd.DataFrame({
    'date': pd.date_range('2023-01-01', periods=90, freq='D'),
    'orders': np.random.randint(10, 50, 90),
    'revenue': np.random.randint(1000, 5000, 90),
    'costs': np.random.randint(500, 2500, 90)
})
orders.set_index('date', inplace=True)

monthly_summary = orders.resample('ME').agg({
    'orders': 'sum',
    'revenue': 'sum',
    'costs': 'sum'
})
monthly_summary['profit'] = monthly_summary['revenue'] - monthly_summary['costs']
monthly_summary['profit_margin'] = (monthly_summary['profit'] / monthly_summary['revenue'] * 100)

# 案例 3: 填補缺失日期
irregular = pd.DataFrame({
    'sales': [100, 150, 200]
}, index=pd.to_datetime(['2023-01-01', '2023-01-05', '2023-01-10']))

regular = irregular.reindex(pd.date_range('2023-01-01', '2023-01-10', freq='D'))
regular_filled = regular.fillna(method='ffill')
```

### 案例 4-8: Rolling 應用

```python
# 案例 4: 移動平均線識別趨勢
prices = pd.Series(
    100 + np.cumsum(np.random.randn(100) * 2),
    index=pd.date_range('2023-01-01', periods=100, freq='D')
)

analysis = pd.DataFrame({
    'price': prices,
    'sma_7': prices.rolling(7).mean(),
    'sma_30': prices.rolling(30).mean()
})

analysis['trend'] = 'neutral'
analysis.loc[analysis['sma_7'] > analysis['sma_30'], 'trend'] = 'uptrend'
analysis.loc[analysis['sma_7'] < analysis['sma_30'], 'trend'] = 'downtrend'

# 案例 5: Bollinger Bands（布林帶）
analysis['middle_band'] = analysis['price'].rolling(20).mean()
analysis['std'] = analysis['price'].rolling(20).std()
analysis['upper_band'] = analysis['middle_band'] + (analysis['std'] * 2)
analysis['lower_band'] = analysis['middle_band'] - (analysis['std'] * 2)

analysis['overbought'] = analysis['price'] > analysis['upper_band']
analysis['oversold'] = analysis['price'] < analysis['lower_band']

# 案例 6: 波動率計算
analysis['volatility'] = analysis['price'].rolling(30).std()

# 案例 7: 7 日銷售累計
sales = pd.Series(
    np.random.randint(100, 500, 100),
    index=pd.date_range('2023-01-01', periods=100, freq='D')
)

analysis = pd.DataFrame({
    'daily_sales': sales,
    'weekly_sales': sales.rolling(7).sum()
})

# 案例 8: 風險指標（下跌天數占比）
returns = prices.pct_change()
analysis['negative_days_7'] = returns.rolling(7).apply(
    lambda x: (x < 0).sum()
)
analysis['downside_ratio_7'] = analysis['negative_days_7'] / 7 * 100
```

### 案例 9-12: Expanding 應用

```python
# 案例 9: 累計銷售和平均值
sales = pd.Series(
    np.random.randint(100, 500, 100),
    index=pd.date_range('2023-01-01', periods=100, freq='D')
)

analysis = pd.DataFrame({
    'sales': sales,
    'cumsum': sales.expanding().sum(),
    'cumavg': sales.expanding().mean()
})

# 案例 10: 逐月 YTD 銷售
full_year = pd.DataFrame({
    'date': pd.date_range('2023-01-01', periods=365, freq='D'),
    'sales': np.random.randint(100, 500, 365)
})
full_year['month'] = full_year['date'].dt.month
full_year['ytd'] = full_year.groupby(full_year['date'].dt.year)['sales'].transform(
    lambda x: x.expanding().sum()
)

# 案例 11: 累計最大回撤
prices = 100 + np.cumsum(np.random.randn(100) * 2)
cummax = pd.Series(prices).expanding().max()
drawdown = (pd.Series(prices) - cummax) / cummax * 100

analysis = pd.DataFrame({
    'price': prices,
    'cummax': cummax,
    'drawdown': drawdown
})

# 案例 12: 客戶終身價值（LTV）追蹤
customers = pd.DataFrame({
    'date': pd.date_range('2023-01-01', periods=200, freq='D'),
    'customer_id': np.random.randint(1, 50, 200),
    'purchase_value': np.random.randint(50, 500, 200)
})

customers['customer_ltv'] = (
    customers.groupby('customer_id')['purchase_value']
    .transform(lambda x: x.expanding().sum())
)
```

---

## 關鍵知識點總結

| 功能 | Pandas 方法 | 用途 |
|-----|-----------|-----|
| 日聚合到月 | `resample('ME').sum()` | 升採樣 |
| 填補缺失日期 | `reindex() + fillna()` | 降採樣 |
| 7 日平均 | `rolling(7).mean()` | 趨勢平滑 |
| 30 日標準差 | `rolling(30).std()` | 波動率計算 |
| 累計求和 | `expanding().sum()` | YTD 計算 |
| 累計平均 | `expanding().mean()` | 逐漸更新平均 |
| 加權移動平均 | `ewm(span=7).mean()` | 强調最近數據 |
| 滾動最大值 | `rolling(7).max()` | 高點識別 |

---

## 常見錯誤與解決方案

### 錯誤 1: 忘記設置日期索引
```python
# 錯誤
data.resample('ME').sum()  # 報錯

# 解決方案
data.set_index('date', inplace=True)
data.resample('ME').sum()
```

### 錯誤 2: 邊界值為 NaN
```python
# 移動平均開始幾行為 NaN
ma7 = data['sales'].rolling(7).mean()
# 前 6 行是 NaN

# 解決方案
ma7_filled = data['sales'].rolling(7, min_periods=1).mean()
```

### 錯誤 3: 時區問題
```python
# 不同時區的數據無法正確合併
data1 = pd.date_range('2023-01-01', periods=10, freq='D', tz='UTC')
data2 = pd.date_range('2023-01-01', periods=10, freq='D', tz='Asia/Taipei')

# 解決方案
data2_utc = data2.tz_convert('UTC')
combined = pd.concat([data1, data2_utc])
```

---

## 練習題預覽

- **簡單：** 基礎 resample、簡單移動平均
- **中等：** 多函數聚合、滾動統計
- **困難：** 自訂聚合、進階指標計算

詳見 Exercise_05_Resample_12_Questions.md

---

## 延伸學習

1. **時間序列分解：** 季節性、趨勢和隨機成分分離
2. **異常檢測：** 基於移動平均的異常值識別
3. **預測：** ARIMA、Prophet 等時間序列模型
4. **實時計算：** 流式數據的增量滾動窗口

---

## 參考資源

- Pandas 官方文檔：[Resampling](https://pandas.pydata.org/docs/user_guide/timeseries.html#resampling)
- Pandas 官方文檔：[Rolling Windows](https://pandas.pydata.org/docs/user_guide/window.html)

---

**本章節耗時：** 6 小時
**預計完成時間：** 1 天
**作者備註：** Resample 和 Rolling 是時間序列分析的核心工具，掌握它們對於市場分析、銷售預測等應用至關重要。
