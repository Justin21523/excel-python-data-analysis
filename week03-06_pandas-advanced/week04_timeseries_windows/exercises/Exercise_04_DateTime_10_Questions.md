# Exercise 4: DateTime 10 題練習

## 練習說明
- 難度標記：🟢 簡單（1-3 題）| 🟡 中等（4-7 題）| 🔴 困難（8-10 題）
- 建議時間：1.5 小時
- 使用 Olist 訂單數據進行練習

---

## 題目

### 🟢 簡單題

#### 題 1: 日期轉換與屬性提取
**難度：簡單 | 預計時間：10 分鐘**

給定以下訂單數據，請完成日期轉換和屬性提取：

```python
import pandas as pd

orders = pd.DataFrame({
    'order_id': [1, 2, 3, 4, 5],
    'order_date': ['2023-01-15', '2023-02-20', '2023-03-10', '2023-04-25', '2023-05-30']
})

# 任務 1: 轉換 order_date 為日期格式
# 任務 2: 提取年份、月份、日期、星期幾
# 任務 3: 計算每個訂單距離今天有多少天

# 預期輸出示例:
# order_id | order_date | year | month | day | day_of_week | days_ago
# 1        | 2023-01-15 | 2023 | 1     | 15  | Sunday      | 331
```

**任務清單：**
1. [ ] 使用 `pd.to_datetime()` 轉換日期
2. [ ] 提取 year、month、day、dayofweek
3. [ ] 計算距今天數
4. [ ] 使用 `day_name()` 獲取星期名稱

---

#### 題 2: Timedelta 計算配送時間
**難度：簡單 | 預計時間：10 分鐘**

給定訂單和配送日期，計算配送時間和 SLA 合規性：

```python
import pandas as pd

orders = pd.DataFrame({
    'order_id': [1, 2, 3, 4, 5],
    'order_date': pd.to_datetime(['2023-01-10', '2023-01-12', '2023-01-15', '2023-01-18', '2023-01-20']),
    'delivery_date': pd.to_datetime(['2023-01-13', '2023-01-14', '2023-01-18', '2023-01-20', '2023-01-22'])
})

# 任務 1: 計算配送時間（天數）
# 任務 2: 設定 SLA 為 3 天，判斷是否按時
# 任務 3: 統計按時率

# 預期輸出:
# order_id | delivery_days | on_time
# 1        | 3             | True
# 2        | 2             | True
# 3        | 3             | True
# 4        | 2             | True
# 5        | 2             | True
# 按時率: 100%
```

**任務清單：**
1. [ ] 計算 `(delivery_date - order_date).dt.days`
2. [ ] 建立 `on_time` 欄位 (delivery_days <= 3)
3. [ ] 計算按時率比例

---

#### 題 3: 月末識別與結算
**難度：簡單 | 預計時間：10 分鐘**

識別月末訂單並進行月度結算：

```python
import pandas as pd
import numpy as np

# 生成 2023 年全年訂單
dates = pd.date_range('2023-01-01', periods=365, freq='D')
orders = pd.DataFrame({
    'order_date': np.random.choice(dates, 100),
    'order_value': np.random.randint(100, 1000, 100)
}).sort_values('order_date')

# 任務 1: 標識月末訂單
# 任務 2: 按月份統計銷售額、訂單數、平均訂單值
# 任務 3: 計算每月的月末訂單佔比

# 預期輸出（摘要）:
# Month | Total Sales | Orders | Avg Order | Month-End % | Month-End Orders
```

**任務清單：**
1. [ ] 轉換日期並標識 `is_month_end`
2. [ ] 按月分組進行聚合
3. [ ] 計算月末訂單佔比

---

### 🟡 中等題

#### 題 4: 日期範圍篩選與工作日計算
**難度：中等 | 預計時間：15 分鐘**

進行複雜的日期篩選和工作日計算：

```python
from pandas.tseries.offsets import BDay
import pandas as pd

orders = pd.DataFrame({
    'order_id': range(1, 11),
    'order_date': pd.date_range('2023-01-13', periods=10, freq='D')  # 開始於週五
})

# 任務 1: 篩選 Q1 (2023-01-01 ~ 2023-03-31) 訂單
# 任務 2: 計算每個訂單的承諾配送日期（2 個工作日）
# 任務 3: 識別週末訂單
# 任務 4: 計算工作日內的訂單佔比

# 預期輸出示例:
# order_id | order_date | day_name  | promised_date | is_weekend
# 1        | 2023-01-13 | Friday    | 2023-01-17    | False
# 2        | 2023-01-14 | Saturday  | 2023-01-17    | True
# 3        | 2023-01-15 | Sunday    | 2023-01-17    | True
```

**任務清單：**
1. [ ] 使用日期比較篩選 Q1
2. [ ] 使用 `BDay()` 計算工作日
3. [ ] 識別 `dayofweek` >= 5 為週末
4. [ ] 計算工作日訂單佔比

---

#### 題 5: Period 時間區間與月度統計
**難度：中等 | 預計時間：15 分鐘**

使用 Period 進行時間區間管理：

```python
import pandas as pd
import numpy as np

# 生成 2023 年訂單數據
orders = pd.DataFrame({
    'order_date': pd.date_range('2023-01-01', periods=365, freq='D'),
    'sales': np.random.randint(100, 500, 365)
})

# 任務 1: 將訂單轉換為月度 Period
# 任務 2: 使用 PeriodIndex 建立月度銷售表
# 任務 3: 提取每月的首尾日期
# 任務 4: 計算 Period 間的月份差異

# 預期輸出示例:
# Period | Total Sales | Month Start | Month End   | Days in Month
# 2023-01| 12000       | 2023-01-01  | 2023-01-31  | 31
# 2023-02| 10500       | 2023-02-01  | 2023-02-28  | 28
```

**任務清單：**
1. [ ] 使用 `dt.to_period('M')` 轉換
2. [ ] 建立 PeriodIndex
3. [ ] 使用 `period.start_time` 和 `period.end_time`
4. [ ] 計算月份差異

---

#### 題 6: 複雜日期計算 - 訂單生命週期
**難度：中等 | 預計時間：20 分鐘**

計算訂單的完整生命週期：

```python
import pandas as pd

orders = pd.DataFrame({
    'order_id': range(1, 6),
    'order_date': pd.to_datetime(['2023-01-15', '2023-01-20', '2023-02-05', '2023-02-10', '2023-03-01']),
    'delivery_date': pd.to_datetime(['2023-01-18', '2023-01-22', '2023-02-08', '2023-02-12', '2023-03-04']),
    'refund_request_date': pd.to_datetime(['2023-02-15', np.nan, '2023-02-15', np.nan, '2023-03-10']),
    'refund_date': pd.to_datetime(['2023-02-20', np.nan, np.nan, np.nan, '2023-03-15'])
})

# 任務 1: 計算訂單到配送時間
# 任務 2: 計算配送到退貨申請的時間
# 任務 3: 計算退貨申請到完成的時間
# 任務 4: 計算整個訂單週期（訂單到退貨完成或現在）

# 預期輸出:
# order_id | order_days | request_days | refund_days | total_days
```

**任務清單：**
1. [ ] 處理 NaN 日期
2. [ ] 多段 Timedelta 計算
3. [ ] 使用 `fillna()` 或條件判斷處理缺失日期

---

#### 題 7: 季度分析與年度規劃
**難度：中等 | 預計時間：20 分鐘**

進行季度分析和年度規劃：

```python
import pandas as pd
import numpy as np

# 2 年的季度銷售數據
quarters = pd.period_range('2022Q1', periods=8, freq='Q')
sales = [100000, 95000, 120000, 110000, 115000, 105000, 130000, 125000]

qtr_sales = pd.Series(sales, index=quarters)

# 任務 1: 計算季度環比增長
# 任務 2: 計算季度同比增長（YoY）
# 任務 3: 計算 4 季 CAGR
# 任務 4: 預測 2024 年各季度銷售（假設增速不變）

# 預期輸出:
# Quarter | Sales  | QoQ %  | YoY %  | CAGR %
# 2022Q1  | 100000 | -      | -      | 5.35
# 2022Q2  | 95000  | -5.0%  | -      | 5.35
```

**任務清單：**
1. [ ] 使用 `pct_change()` 計算環比
2. [ ] 使用 `shift(4)` 計算同比
3. [ ] 自訂 CAGR 計算函數
4. [ ] 基於增速進行簡單預測

---

### 🔴 困難題

#### 題 8: 工作日和節假日的複雜計算
**難度：困難 | 預計時間：25 分鐘**

處理複雜的工作日和節假日場景：

```python
from pandas.tseries.offsets import BDay, CustomBusinessDay
import pandas as pd

# 訂單數據
orders = pd.DataFrame({
    'order_id': range(1, 11),
    'order_date': pd.date_range('2023-01-10', periods=10, freq='D')
})

# 定義節假日
holidays = ['2023-01-20', '2023-02-10']  # 假日

# 任務 1: 建立包含節假日的自訂工作日日歷
# 任務 2: 計算不考慮節假日的承諾交付日期
# 任務 3: 計算某日期是否為節假日或週末
# 任務 4: 計算特定日期範圍內有多少個工作日

# 預期輸出:
# order_id | order_date | promised_date | days_to_delivery | is_holiday
```

**任務清單：**
1. [ ] 使用 `CustomBusinessDay(holidays=)`
2. [ ] 計算自訂工作日偏移
3. [ ] 建立假日檢查函數
4. [ ] 計算範圍內工作日數

---

#### 題 9: 時間序列數據完整性驗證
**難度：困難 | 預計時間：25 分鐘**

驗證時間序列數據的完整性並進行修復：

```python
import pandas as pd
import numpy as np

# 有缺失和重複日期的訂單數據
orders = pd.DataFrame({
    'order_date': ['2023-01-01', '2023-01-02', '2023-01-03', '2023-01-05',  # 缺少 1-4
                   '2023-01-05', '2023-01-06', '2023-01-10'],  # 1-5 重複
    'sales': [100, 150, 120, 200, 180, 160, 240]
})

# 任務 1: 識別並移除重複日期記錄
# 任務 2: 識別缺失日期
# 任務 3: 填補缺失日期和相應銷售數據
# 任務 4: 生成完整的日期索引
# 任務 5: 驗證時間序列連續性

# 預期輸出:
# 原始記錄數: 7, 重複記錄: 1
# 缺失日期: ['2023-01-04', '2023-01-07', '2023-01-08', '2023-01-09']
# 修復後記錄數: 10
```

**任務清單：**
1. [ ] 使用 `duplicated()` 識別重複
2. [ ] 使用 `reindex()` 建立完整日期範圍
3. [ ] 實現多種填補策略（前向填充、後向填充、線性插值）
4. [ ] 驗證時間序列連續性

---

#### 題 10: 時區和國際日期處理
**難度：困難 | 預計時間：25 分鐘**

處理多時區的國際訂單：

```python
import pandas as pd

# 不同時區的訂單（假設數據已是 naive datetime）
orders = pd.DataFrame({
    'order_id': range(1, 7),
    'order_time': pd.to_datetime([
        '2023-01-15 10:30:00',
        '2023-01-15 12:00:00',
        '2023-01-15 14:30:00',
        '2023-01-15 16:00:00',
        '2023-01-15 18:30:00',
        '2023-01-15 20:00:00'
    ]),
    'region': ['US/Eastern', 'US/Central', 'US/Mountain', 'US/Pacific', 'Europe/London', 'Asia/Tokyo']
})

# 任務 1: 為每個訂單添加時區信息
# 任務 2: 轉換所有訂單為 UTC 時間
# 任務 3: 識別按當地午夜時間的日期邊界
# 任務 4: 計算各地區的訂單量

# 預期輸出:
# order_id | local_time           | utc_time             | local_date | region
# 1        | 2023-01-15 10:30 EST | 2023-01-15 15:30 UTC | 2023-01-15 | US/Eastern
```

**任務清單：**
1. [ ] 為 naive datetime 添加時區 `localize()`
2. [ ] 轉換為 UTC `tz_convert('UTC')`
3. [ ] 計算本地午夜時間對應的 UTC 時間
4. [ ] 按地區統計訂單

---

## 解答檢查清單

完成所有題目後，請檢查：

- [ ] 所有日期都正確轉換為 datetime64 格式
- [ ] 沒有 NaN 值被忽視
- [ ] 計算結果的單位明確（天數、小時數等）
- [ ] 代碼注釋清晰，易於理解
- [ ] 邊界情況已考慮（月末、年末、閏年等）

---

## 進階延伸

完成基礎題後，嘗試以下進階練習：

1. **季節性分析**：識別特定日期（如黑色星期五）的訂單模式
2. **實時計算**：為每個新訂單動態更新統計量
3. **預測**：基於歷史模式預測未來訂單日期的分佈
4. **成本計算**：結合存儲成本和配送時間進行成本優化分析

---

**預計總耗時：** 1.5 小時
**建議完成方式：** 每題 10-25 分鐘，分次完成
