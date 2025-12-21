# Day 5: DateTime 主要指南

## 概述
在本節課中，您將掌握 Pandas 日期時間處理的核心技能：從字符串轉換到日期物件、提取日期屬性、計算時間差異，以及處理業務日期。

**學習時間：** 6 小時（3 部分）
**難度：** 中等
**主要工具：** `pd.to_datetime()`, `dt` accessor, `DateOffset`, `Period`

---

## Part 1: DateTime 基礎（2 小時）

### 1.1 pd.to_datetime() 轉換日期

#### 概念
`pd.to_datetime()` 是將各種格式的字符串轉換為 Pandas Timestamp 物件的核心函數。

```python
import pandas as pd
import numpy as np
from datetime import datetime, timedelta

# 1. 從字符串轉換
date_str = "2023-01-15"
dt = pd.to_datetime(date_str)
print(f"轉換類型: {type(dt)}")  # <class 'pandas._libs.tslibs.timestamps.Timestamp'>
print(f"轉換結果: {dt}")  # 2023-01-15 00:00:00

# 2. 從列表/Series 轉換
dates_list = ["2023-01-15", "2023-01-16", "2023-01-17"]
dt_series = pd.to_datetime(dates_list)
print(dt_series)
# 0   2023-01-15
# 1   2023-01-16
# 2   2023-01-17
# dtype: datetime64[ns]

# 3. 混合日期格式自動識別
mixed_dates = pd.to_datetime([
    "2023-01-15",
    "01/15/2023",
    "15-Jan-2023"
])
print(mixed_dates)

# 4. 指定日期格式（提高性能）
dates_str = ["2023-01-15", "2023-02-20", "2023-03-10"]
dt_fast = pd.to_datetime(dates_str, format="%Y-%m-%d")
print(dt_fast)

# 5. 處理無效日期
dates_with_errors = ["2023-01-15", "invalid", "2023-02-20"]
dt_with_errors = pd.to_datetime(dates_with_errors, errors="coerce")
print(dt_with_errors)
# 0   2023-01-15
# 1          NaT  <- 無效日期轉換為 NaT (Not a Time)
# 2   2023-02-20
```

#### Excel 對照
```excel
=DATEVALUE("2023-01-15")  // 轉換為日期
```

### 1.2 dt accessor 提取日期屬性

#### 概念
透過 `dt` accessor，可以方便地從 DatetimeIndex 或 Series 提取日期的各個成分。

```python
# 準備數據
orders = pd.DataFrame({
    'order_date': ['2023-01-15', '2023-02-20', '2023-03-10'],
    'value': [100, 150, 200]
})

# 轉換為日期格式
orders['order_date'] = pd.to_datetime(orders['order_date'])

# 使用 dt accessor 提取屬性
print(orders['order_date'].dt.year)       # 2023
print(orders['order_date'].dt.month)      # 1, 2, 3
print(orders['order_date'].dt.day)        # 15, 20, 10
print(orders['order_date'].dt.dayofweek)  # 0=Monday, 6=Sunday
print(orders['order_date'].dt.quarter)    # 1, 1, 1
print(orders['order_date'].dt.is_month_end)  # 是否月末
print(orders['order_date'].dt.is_month_start)  # 是否月初
print(orders['order_date'].dt.is_quarter_end)  # 是否季末
print(orders['order_date'].dt.days_in_month)  # 該月天數

# 建立新列
orders['year'] = orders['order_date'].dt.year
orders['month'] = orders['order_date'].dt.month
orders['day_of_week'] = orders['order_date'].dt.dayofweek
orders['week_name'] = orders['order_date'].dt.day_name()
orders['month_name'] = orders['order_date'].dt.month_name()

print(orders)
#   order_date  value  year  month  day_of_week week_name month_name
# 0 2023-01-15    100  2023      1            6     Sunday    January
# 1 2023-02-20    150  2023      2            0     Monday  February
# 2 2023-03-10    200  2023      3            4     Friday     March
```

#### Excel 對照
```excel
=YEAR(A1)              // 提取年份
=MONTH(A1)            // 提取月份
=DAY(A1)              // 提取日期
=WEEKDAY(A1, 2)       // 提取星期幾
=QUARTER(A1)          // 提取季度
=TEXT(A1, "DDDD")     // 提取星期名稱
```

### 1.3 date_range 生成日期序列

#### 概念
`pd.date_range()` 可以生成規律的日期序列，用於建立時間索引。

```python
# 1. 按天生成
date_range_daily = pd.date_range(start='2023-01-01', periods=5, freq='D')
print(date_range_daily)
# DatetimeIndex(['2023-01-01', '2023-01-02', '2023-01-03', '2023-01-04',
#                '2023-01-05'],
#               dtype='datetime64[ns]', freq='D')

# 2. 按週生成
date_range_weekly = pd.date_range(start='2023-01-01', periods=4, freq='W')
print(date_range_weekly)

# 3. 按月生成
date_range_monthly = pd.date_range(start='2023-01-01', periods=6, freq='MS')
# freq='MS' = Month Start
# freq='M' = Month End (deprecated, use 'ME')
# freq='ME' = Month End (新版本)
print(date_range_monthly)

# 4. 按季度生成
date_range_quarterly = pd.date_range(start='2023-01-01', periods=4, freq='QS')
# freq='QS' = Quarter Start
print(date_range_quarterly)

# 5. 指定開始和結束日期
date_range_between = pd.date_range(start='2023-01-01', end='2023-03-31', freq='D')
print(f"日期數量: {len(date_range_between)}")

# 6. 常見頻率（Frequency）
freq_examples = {
    'D': '日',
    'W': '週（周日結束）',
    'W-Mon': '週（周一結束）',
    'MS': '月初',
    'ME': '月末',
    'QS': '季初',
    'QE': '季末',
    'YS': '年初',
    'YE': '年末',
    'H': '小時',
    'min': '分鐘',
    'S': '秒'
}
```

### 1.4 DatetimeIndex 索引

#### 概念
將日期設置為 DataFrame 的索引，可以方便地進行時間序列操作。

```python
# 建立 DataFrame，日期作為索引
dates = pd.date_range('2023-01-01', periods=5, freq='D')
data = pd.DataFrame({
    'sales': [100, 150, 120, 200, 180],
    'inventory': [50, 40, 60, 30, 45]
}, index=dates)

print(data)
#             sales  inventory
# 2023-01-01    100          50
# 2023-01-02    150          40
# 2023-01-03    120          60
# 2023-01-04    200          30
# 2023-01-05    180          45

# 使用日期索引進行時間序列操作
print(data.loc['2023-01-02':'2023-01-04'])  # 按日期範圍選擇

# 按月份選擇
data_monthly = data.loc['2023-01']
print(data_monthly)
```

---

## Part 2: Timedelta 與 DateOffset（2 小時）

### 2.1 Timedelta 時間差計算

#### 概念
Timedelta 表示兩個時間點之間的差異，用於計算天數、小時數等。

```python
# 1. 直接創建 Timedelta
td = pd.Timedelta(days=5)
print(f"5 天: {td}")  # 5 days 00:00:00
print(f"總秒數: {td.total_seconds()}")  # 432000.0

# 2. 從字符串創建
td_str = pd.Timedelta('5 days 2 hours 30 minutes')
print(td_str)  # 5 days 02:30:00

# 3. 日期相減得到 Timedelta
date1 = pd.to_datetime('2023-02-15')
date2 = pd.to_datetime('2023-01-15')
diff = date1 - date2
print(f"日期差異: {diff}")  # 31 days 00:00:00
print(f"天數: {diff.days}")  # 31

# 4. 日期加減 Timedelta
order_date = pd.to_datetime('2023-01-15')
delivery_date = order_date + pd.Timedelta(days=3)
print(f"訂單日期: {order_date.date()}")
print(f"配送日期: {delivery_date.date()}")
# 訂單日期: 2023-01-15
# 配送日期: 2023-01-18

# 5. 計算配送時間
orders = pd.DataFrame({
    'order_date': pd.to_datetime(['2023-01-15', '2023-02-10', '2023-03-05']),
    'delivery_date': pd.to_datetime(['2023-01-18', '2023-02-12', '2023-03-08'])
})

orders['delivery_days'] = (orders['delivery_date'] - orders['order_date']).dt.days
print(orders)
#   order_date delivery_date  delivery_days
# 0 2023-01-15    2023-01-18              3
# 1 2023-02-10    2023-02-12              2
# 2 2023-03-05    2023-03-08              3

# 6. 提取 Timedelta 的成分
td = pd.Timedelta('5 days 3 hours 30 minutes')
print(f"天數: {td.days}")
print(f"秒數: {td.seconds}")
print(f"總秒數: {td.total_seconds()}")
print(f"小時: {td.total_seconds() / 3600}")
```

#### Excel 對照
```excel
=B1-A1                 // 日期差異（天數）
=A1 + 3                // 日期加 3 天
=DAYS(B1, A1)         // 計算兩日期間隔天數
=DATEDIF(A1, B1, "D") // 計算完整天數
```

### 2.2 DateOffset 與業務日期

#### 概念
DateOffset 用於處理業務日期（工作日），排除週末和節假日。

```python
# 1. 基本 DateOffset
from pandas.tseries.offsets import BDay, CDay, MonthEnd, QuarterEnd

# BDay = Business Day（排除週末）
date = pd.to_datetime('2023-01-13')  # 週五
print(f"原始日期: {date.date()}, {date.day_name()}")  # 2023-01-13, Friday

# 加 3 個工作日
next_bday = date + 3 * BDay()
print(f"加 3 個工作日: {next_bday.date()}, {next_bday.day_name()}")
# 2023-01-18, Wednesday (跳過了 16, 17 週末)

# 2. 計算配送承諾（工作日）
orders = pd.DataFrame({
    'order_date': pd.to_datetime(['2023-01-13', '2023-01-16', '2023-01-17']),
})

# 承諾 3 個工作日內配送
orders['promised_delivery'] = orders['order_date'] + 3 * BDay()
print(orders)

# 3. MonthEnd - 月末
month_end = pd.to_datetime('2023-01-15') + MonthEnd(0)
print(f"本月月末: {month_end.date()}")  # 2023-01-31

# 4. QuarterEnd - 季末
quarter_end = pd.to_datetime('2023-02-15') + QuarterEnd(0)
print(f"本季季末: {quarter_end.date()}")  # 2023-03-31

# 5. 節假日處理（需要定義節假日列表）
from pandas.tseries.holiday import USFederalHolidayCalendar
from pandas.tseries.offsets import CustomBusinessDay

# 建立自訂業務日（包含節假日）
holidays = ['2023-01-01', '2023-12-25']
cday = CustomBusinessDay(holidays=holidays)

# 計算排除節假日的工作日
start = pd.to_datetime('2023-01-01')
end = start + 3 * cday
print(f"加 3 個工作日（排除節假日）: {end.date()}")

# 6. 批量計算工作日
dates = pd.date_range('2023-01-01', periods=10, freq='D')
df = pd.DataFrame({'date': dates})
df['is_business_day'] = df['date'].dt.dayofweek < 5  # 0-4 是工作日
print(df)
```

#### Excel 對照
```excel
=WORKDAY(A1, 3)              // 加 3 個工作日
=NETWORKDAYS(A1, B1)         // 計算兩日期間的工作日
=NETWORKDAYS(A1, B1, holidays) // 計算工作日，排除節假日
```

---

## Part 3: Period 與 Timestamp（2 小時）

### 3.1 Period 時間區間

#### 概念
Period 表示一個時間區間（如一月、一季），而 Timestamp 表示一個特定時間點。

```python
# 1. 建立 Period
period = pd.Period('2023-01', freq='M')  # 2023 年 1 月
print(f"Period: {period}")  # 2023-01
print(f"Period 類型: {type(period)}")  # <class 'pandas._libs.tslibs.period.Period'>

# 2. 從 Period 到日期
start_date = period.start_time
end_date = period.end_time
print(f"月初: {start_date}")  # 2023-01-01 00:00:00
print(f"月末: {end_date}")    # 2023-01-31 23:59:59.999999999

# 3. 建立 PeriodIndex
periods = pd.period_range('2023-01', periods=6, freq='M')
print(periods)
# PeriodIndex(['2023-01', '2023-02', '2023-03', '2023-04', '2023-05', '2023-06'],
#             dtype='period[M]', freq='M')

# 4. 使用 Period 作為索引
monthly_sales = pd.DataFrame({
    'sales': [1000, 1200, 1100, 1300, 1400, 1350],
    'costs': [600, 700, 680, 750, 800, 790]
}, index=periods)

print(monthly_sales)
#        sales  costs
# 2023-01  1000    600
# 2023-02  1200    700
# 2023-03  1100    680
# 2023-04  1300    750
# 2023-05  1400    800
# 2023-06  1350    790

# 5. Timestamp 轉換為 Period
timestamps = pd.to_datetime(['2023-01-15', '2023-01-31', '2023-02-10'])
periods_from_ts = timestamps.to_period('M')
print(periods_from_ts)
# PeriodIndex(['2023-01', '2023-01', '2023-02'], dtype='period[M]', freq='M')

# 6. Period 轉換為 Timestamp
periods = pd.period_range('2023-01', periods=3, freq='M')
timestamps = periods.to_timestamp()
print(timestamps)
# DatetimeIndex(['2023-01-01', '2023-02-01', '2023-03-01'],
#               dtype='datetime64[ns]', freq='MS')

# 轉換為月末
timestamps_eom = periods.to_timestamp(how='end')
print(timestamps_eom)
# DatetimeIndex(['2023-01-31', '2023-02-28', '2023-03-31'],
#               dtype='datetime64[ns]', freq='ME')
```

#### Excel 對照
Period 概念在 Excel 中對應於樞紐表中按月份分組的概念，沒有直接等價函數。

### 3.2 Timestamp vs Period 選擇

#### 概念
何時使用 Timestamp，何時使用 Period？

```python
# Timestamp: 適合記錄具體事件發生的時間
orders = pd.DataFrame({
    'order_id': [1, 2, 3],
    'order_timestamp': pd.to_datetime([
        '2023-01-15 10:30:00',
        '2023-01-15 14:20:00',
        '2023-02-20 09:45:00'
    ])
})
print("訂單（Timestamp）:")
print(orders)

# Period: 適合進行區間分組和統計
order_year_month = orders['order_timestamp'].dt.to_period('M')
print("\n按月份分組（Period）:")
print(order_year_month)

# 轉換為 Period 進行分組
orders['year_month'] = orders['order_timestamp'].dt.to_period('M')
monthly_summary = orders.groupby('year_month').size()
print("\n月份銷售筆數:")
print(monthly_summary)
# year_month
# 2023-01    2
# 2023-02    1
# Freq: M, dtype: int64
```

---

## 實戰案例（10 個）

### 案例 1: 訂單日期分析

**場景：** 分析 Olist 訂單的日期特徵

```python
# 載入訂單數據
import pandas as pd
import numpy as np

# 模擬 Olist 訂單數據
orders = pd.DataFrame({
    'order_id': range(1, 11),
    'order_date': [
        '2023-01-15', '2023-01-16', '2023-01-20',
        '2023-02-01', '2023-02-10', '2023-02-28',
        '2023-03-05', '2023-03-10', '2023-03-15', '2023-03-31'
    ],
    'order_value': [100, 150, 120, 200, 180, 160, 140, 190, 170, 210]
})

# 1. 轉換日期
orders['order_date'] = pd.to_datetime(orders['order_date'])

# 2. 提取日期屬性
orders['year'] = orders['order_date'].dt.year
orders['month'] = orders['order_date'].dt.month
orders['day'] = orders['order_date'].dt.day
orders['quarter'] = orders['order_date'].dt.quarter
orders['day_of_week'] = orders['order_date'].dt.day_name()
orders['is_month_end'] = orders['order_date'].dt.is_month_end
orders['days_in_month'] = orders['order_date'].dt.days_in_month

# 3. 分析結果
print("訂單日期分析結果:")
print(orders[['order_date', 'day_of_week', 'is_month_end', 'order_value']])

# 4. 統計分析
print(f"\n按星期幾統計訂單:")
print(orders.groupby('day_of_week')['order_value'].agg(['count', 'sum', 'mean']))

print(f"\n按月份統計訂單:")
print(orders.groupby('month')['order_value'].agg(['count', 'sum', 'mean']))
```

### 案例 2: 配送時間計算

**場景：** 計算訂單到配送的時間

```python
# 模擬訂單和配送數據
orders = pd.DataFrame({
    'order_id': range(1, 6),
    'order_date': pd.to_datetime([
        '2023-01-15', '2023-01-20', '2023-02-05',
        '2023-02-10', '2023-03-01'
    ]),
    'delivery_date': pd.to_datetime([
        '2023-01-18', '2023-01-22', '2023-02-08',
        '2023-02-12', '2023-03-04'
    ])
})

# 1. 計算配送時間（天數）
orders['delivery_days'] = (orders['delivery_date'] - orders['order_date']).dt.days

# 2. 計算是否按時配送（假設 SLA 是 3 天）
orders['sla_days'] = 3
orders['on_time'] = orders['delivery_days'] <= orders['sla_days']

# 3. 統計結果
print("配送時間分析:")
print(orders[['order_id', 'delivery_days', 'on_time']])

print(f"\n統計摘要:")
print(f"平均配送時間: {orders['delivery_days'].mean():.1f} 天")
print(f"按時率: {orders['on_time'].mean() * 100:.1f}%")
print(f"最長配送: {orders['delivery_days'].max()} 天")
print(f"最短配送: {orders['delivery_days'].min()} 天")
```

### 案例 3: 工作日計算

**場景：** 計算工作日內的配送承諾

```python
from pandas.tseries.offsets import BDay

# 訂單數據
orders = pd.DataFrame({
    'order_id': range(1, 6),
    'order_date': pd.to_datetime([
        '2023-01-13',  # 週五
        '2023-01-16',  # 週一
        '2023-01-17',  # 週二
        '2023-01-19',  # 週四
        '2023-01-20'   # 週五
    ])
})

# 1. 承諾 2 個工作日內配送
orders['promised_delivery_bday'] = orders['order_date'] + 2 * BDay()

# 2. 顯示結果
orders['order_day_name'] = orders['order_date'].dt.day_name()
orders['promised_day_name'] = orders['promised_delivery_bday'].dt.day_name()

print("工作日承諾配送:")
print(orders[['order_date', 'order_day_name', 'promised_delivery_bday', 'promised_day_name']])
```

### 案例 4: 季度銷售分析

**場景：** 按季度統計銷售數據

```python
# 全年銷售數據
orders = pd.DataFrame({
    'order_date': pd.date_range('2023-01-01', periods=365, freq='D'),
    'sales': np.random.randint(100, 500, 365)
})

# 1. 提取季度
orders['quarter'] = orders['order_date'].dt.quarter
orders['year_quarter'] = orders['order_date'].dt.year.astype(str) + '-Q' + orders['order_date'].dt.quarter.astype(str)

# 2. 按季度統計
quarterly_summary = orders.groupby('year_quarter')['sales'].agg(['count', 'sum', 'mean', 'std'])
print("季度銷售摘要:")
print(quarterly_summary)

# 3. 季度增長率
quarterly_sales = orders.groupby('quarter')['sales'].sum()
qoq_growth = quarterly_sales.pct_change()
print(f"\n季度環比增長率:")
print(qoq_growth)
```

### 案例 5: 月末結算

**場景：** 提取月末數據進行結算

```python
# 每日銷售數據
daily_sales = pd.DataFrame({
    'date': pd.date_range('2023-01-01', periods=90, freq='D'),
    'sales': np.random.randint(100, 300, 90),
    'costs': np.random.randint(50, 150, 90)
})

# 1. 標識月末
daily_sales['is_month_end'] = daily_sales['date'].dt.is_month_end

# 2. 提取月末數據
month_end_data = daily_sales[daily_sales['is_month_end']]
print("月末結算數據:")
print(month_end_data)

# 3. 計算利潤
month_end_data = month_end_data.copy()
month_end_data['profit'] = month_end_data['sales'] - month_end_data['costs']
print(f"\n月末利潤:")
print(month_end_data[['date', 'sales', 'costs', 'profit']])
```

### 案例 6-10: 追加案例

```python
# 案例 6: 年份篩選
yearly_2023 = orders[orders['order_date'].dt.year == 2023]

# 案例 7: 特定月份篩選
january = orders[orders['order_date'].dt.month == 1]

# 案例 8: 日期範圍篩選
q1_2023 = orders[(orders['order_date'] >= '2023-01-01') &
                  (orders['order_date'] <= '2023-03-31')]

# 案例 9: 星期幾篩選（只含工作日）
weekdays = orders[orders['order_date'].dt.dayofweek < 5]

# 案例 10: 月初和月末篩選
boundaries = orders[
    orders['order_date'].dt.is_month_start |
    orders['order_date'].dt.is_month_end
]
```

---

## 關鍵知識點總結

| 功能 | Pandas 方法 | Excel 對照 |
|-----|----------|-----------|
| 轉換日期字符串 | `pd.to_datetime()` | `DATEVALUE()` |
| 提取年份 | `dt.year` | `YEAR()` |
| 提取月份 | `dt.month` | `MONTH()` |
| 提取日期 | `dt.day` | `DAY()` |
| 提取星期幾 | `dt.dayofweek` | `WEEKDAY()` |
| 計算天數差異 | `(date2-date1).dt.days` | `DATEDIF()` |
| 加減天數 | `date + Timedelta(days=n)` | `A1 + n` |
| 月末日期 | `dt.is_month_end` | `DAY(EOMONTH(A1,0))=DAY()` |
| 業務日計算 | `date + n * BDay()` | `WORKDAY()` |
| 生成日期序列 | `pd.date_range()` | 手動輸入或 FILL |

---

## 常見錯誤與解決方案

### 錯誤 1: 日期轉換失敗
```python
# 錯誤
dates = pd.to_datetime(['2023-01-15', 'invalid', '2023-02-20'])  # 報錯

# 解決方案
dates = pd.to_datetime(['2023-01-15', 'invalid', '2023-02-20'],
                       errors='coerce')  # 無效值轉為 NaT
```

### 錯誤 2: 性能問題
```python
# 低效（自動檢測格式）
dates = pd.to_datetime(['2023-01-15'] * 1000000)

# 高效（指定格式）
dates = pd.to_datetime(['2023-01-15'] * 1000000, format='%Y-%m-%d')
```

### 錯誤 3: 時區問題
```python
# 建立帶時區的日期
dates = pd.date_range('2023-01-01', periods=5, freq='D', tz='Asia/Taipei')
print(dates)
# DatetimeIndex(['2023-01-01 00:00:00+08:00', ...], dtype='datetime64[ns, Asia/Taipei]')

# 轉換時區
dates_utc = dates.tz_convert('UTC')
```

---

## 練習題預覽

- **簡單：** 日期轉換、屬性提取
- **中等：** 日期計算、業務日處理
- **困難：** Period 操作、時區處理

詳見 Exercise_04_DateTime_10_Questions.md

---

## 延伸學習

1. **時區處理：** 國際業務中的時區轉換
2. **假期處理：** CustomBusinessDay 與自訂節假日
3. **時間序列分析：** 結合 resample 和 rolling 進行趨勢分析
4. **財務日期：** 會計年度、財年等特殊時間概念

---

## 參考資源

- Pandas 官方文檔：[Timeseries / Date functionality](https://pandas.pydata.org/docs/user_guide/timeseries.html)
- Olist 數據集文檔
- 下一節課預告：Day 6 - Resample 與 Rolling 視窗函數

---

**本章節耗時：** 6 小時
**預計完成時間：** 1 天
**作者備註：** 這些是進行時間序列分析的基礎，後續的 Resample 和 Rolling 都依賴於對這些概念的理解。
