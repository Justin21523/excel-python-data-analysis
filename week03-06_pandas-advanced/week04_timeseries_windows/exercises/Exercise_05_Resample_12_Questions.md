# Exercise 5: Resample & Rolling 12 題練習

## 練習說明
- 難度標記：🟢 簡單（1-4 題）| 🟡 中等（5-9 題）| 🔴 困難（10-12 題）
- 建議時間：2 小時
- 使用 Olist 訂單數據進行練習

---

## 題目

### 🟢 簡單題

#### 題 1: 基礎 Resample 升採樣
**難度：簡單 | 預計時間：15 分鐘**

將日級銷售數據聚合為週級和月級：

```python
import pandas as pd
import numpy as np

# 生成 90 天的日級銷售數據
dates = pd.date_range('2023-01-01', periods=90, freq='D')
daily_sales = pd.DataFrame({
    'date': dates,
    'sales': np.random.randint(100, 500, 90),
    'orders': np.random.randint(5, 50, 90)
})

# 任務 1: 將日期設為索引
# 任務 2: 升採樣到週級（週日結束），計算銷售額求和和訂單數求和
# 任務 3: 升採樣到月級（月末），計算銷售額求和、訂單數求和、平均訂單值
# 任務 4: 比較日級、週級、月級的數據粒度差異

# 預期輸出:
# Weekly Summary:
#             sales  orders
# date
# 2023-01-08   2150    185
# 2023-01-15   2180    190
#
# Monthly Summary:
#             sales  orders  avg_order
# date
# 2023-01-31   8430   1548     5.44
# 2023-02-28   7890   1421     5.55
# 2023-03-31   8950   1675     5.35
```

**任務清單：**
1. [ ] 使用 `set_index()` 設定日期索引
2. [ ] 使用 `resample('W')` 進行週聚合
3. [ ] 使用 `resample('ME')` 進行月聚合
4. [ ] 計算多個聚合函數

---

#### 題 2: 簡單移動平均線（SMA）
**難度：簡單 | 預計時間：15 分鐘**

計算 7 日和 30 日簡單移動平均線：

```python
import pandas as pd
import numpy as np

# 生成股票/商品價格數據
dates = pd.date_range('2023-01-01', periods=100, freq='D')
prices = pd.Series(
    100 + np.cumsum(np.random.randn(100) * 2),
    index=dates
)

# 任務 1: 建立 DataFrame，包含日期、價格
# 任務 2: 計算 7 日簡單移動平均
# 任務 3: 計算 30 日簡單移動平均
# 任務 4: 識別移動平均線交叉點（7 日 > 30 日 為買入信號）

# 預期輸出:
# date       | price  | sma_7  | sma_30 | signal
# 2023-01-01 | 100.5  | NaN    | NaN    | -
# 2023-01-07 | 105.2  | 102.4  | NaN    | -
# 2023-01-31 | 110.8  | 108.5  | 105.2  | Buy
```

**任務清單：**
1. [ ] 建立包含價格的 Series
2. [ ] 使用 `rolling(7).mean()` 計算 7 日 SMA
3. [ ] 使用 `rolling(30).mean()` 計算 30 日 SMA
4. [ ] 比較兩個 SMA 生成交易信號

---

#### 題 3: 移動標準差與波動率
**難度：簡單 | 預計時間：15 分鐘**

計算移動標準差識別市場波動率：

```python
import pandas as pd
import numpy as np

# 價格數據
dates = pd.date_range('2023-01-01', periods=100, freq='D')
prices = pd.Series(
    100 + np.cumsum(np.random.randn(100) * 2),
    index=dates
)

# 任務 1: 計算 7 日移動標準差（波動率）
# 任務 2: 計算 30 日移動標準差
# 任務 3: 識別高波動期間（標準差 > 平均值 + 1 倍標準差）
# 任務 4: 統計高波動天數

# 預期輸出:
# date       | price  | volatility_7 | volatility_30 | high_volatility
# 2023-01-01 | 100.5  | NaN          | NaN           | False
# 2023-01-31 | 110.8  | 2.34         | 2.10          | True
#
# High volatility days: 12
```

**任務清單：**
1. [ ] 使用 `rolling(7).std()` 計算 7 日標準差
2. [ ] 使用 `rolling(30).std()` 計算 30 日標準差
3. [ ] 識別異常波動
4. [ ] 統計異常天數

---

#### 題 4: 7 日銷售累計
**難度：簡單 | 預計時間：15 分鐘**

計算 7 日滾動銷售累計用於週度分析：

```python
import pandas as pd
import numpy as np

# 日級銷售數據
dates = pd.date_range('2023-01-01', periods=30, freq='D')
sales = pd.Series(
    np.random.randint(100, 500, 30),
    index=dates
)

# 任務 1: 計算 7 日銷售累計
# 任務 2: 計算 7 日平均每日銷售
# 任務 3: 識別銷售高峰週（7 日累計 > 中位數 + 1.5*IQR）
# 任務 4: 計算 7 日均線相對於月平均的偏差

# 預期輸出:
# date       | daily_sales | 7day_total | 7day_avg | peak_week
# 2023-01-01 | 250         | NaN        | NaN      | False
# 2023-01-07 | 350         | 1950       | 278.6    | False
# 2023-01-31 | 420         | 2450       | 350.0    | True
```

**任務清單：**
1. [ ] 使用 `rolling(7).sum()` 計算 7 日累計
2. [ ] 使用 `rolling(7).mean()` 計算 7 日平均
3. [ ] 計算 IQR 識別高峰週
4. [ ] 計算偏差百分比

---

### 🟡 中等題

#### 題 5: 多函數聚合
**難度：中等 | 預計時間：20 分鐘**

進行複雜的多函數聚合：

```python
import pandas as pd
import numpy as np

# 銷售數據（包含多個指標）
sales_data = pd.DataFrame({
    'date': pd.date_range('2023-01-01', periods=90, freq='D'),
    'units_sold': np.random.randint(10, 100, 90),
    'revenue': np.random.randint(1000, 5000, 90),
    'returns': np.random.randint(0, 20, 90),
    'customers': np.random.randint(20, 150, 90)
})

# 任務 1: 設定日期為索引
# 任務 2: 按月聚合，使用不同的聚合函數：
#         - units_sold: sum, mean, std
#         - revenue: sum, mean, max
#         - returns: sum, max
#         - customers: mean
# 任務 3: 計算淨收入（revenue - returns * avg_price）
# 任務 4: 計算退貨率（returns / units_sold）

# 預期輸出:
# Month    | total_units | avg_units | std_units | total_revenue | ... | return_rate
```

**任務清單：**
1. [ ] 建立聚合函數字典
2. [ ] 使用 `.agg()` 進行多函數聚合
3. [ ] 計算衍生指標
4. [ ] 格式化輸出

---

#### 題 6: 加權移動平均線（WMA）
**難度：中等 | 預計時間：20 分鐘**

實現加權移動平均線，給予最近數據更大權重：

```python
import pandas as pd
import numpy as np

# 銷售數據
dates = pd.date_range('2023-01-01', periods=30, freq='D')
sales = pd.Series(
    np.random.randint(100, 500, 30),
    index=dates
)

# 任務 1: 實現手動 WMA（7 日，線性遞增權重）
# 任務 2: 使用 ewm（指數加權移動平均）計算 EWMA
# 任務 3: 比較 SMA、WMA、EWMA 三種移動平均
# 任務 4: 分析不同方法對趨勢識別的影響

def weighted_moving_average(series, window, weights=None):
    """計算加權移動平均線"""
    if weights is None:
        weights = np.arange(1, window + 1)
    weights = weights / weights.sum()
    return series.rolling(window).apply(lambda x: (x * weights).sum(), raw=False)

# 預期輸出:
# date       | sales | sma_7  | wma_7  | ewma_7
# 2023-01-01 | 250   | NaN    | NaN    | 250.0
# 2023-01-07 | 350   | 285.7  | 297.3  | 288.4
# 2023-01-31 | 400   | 320.0  | 335.8  | 315.2
```

**任務清單：**
1. [ ] 實現自訂 WMA 函數
2. [ ] 使用 `.ewm()` 計算 EWMA
3. [ ] 繪製三種平均線的比較
4. [ ] 分析權重對結果的影響

---

#### 題 7: Expanding 累計分析
**難度：中等 | 預計時間：20 分鐘**

使用 expanding 進行累計統計：

```python
import pandas as pd
import numpy as np

# 銷售數據
dates = pd.date_range('2023-01-01', periods=30, freq='D')
sales = pd.Series(
    np.random.randint(100, 500, 30),
    index=dates
)

# 任務 1: 計算累計銷售
# 任務 2: 計算累計平均銷售
# 任務 3: 計算累計最大和最小值
# 任務 4: 識別銷售穩定性趨勢（累計標準差變化）

# 預期輸出:
# date       | sales | cumsum | cumavg | cummax | cummin | cumstd
# 2023-01-01 | 250   | 250    | 250.0  | 250    | 250    | 0.0
# 2023-01-02 | 350   | 600    | 300.0  | 350    | 250    | 50.0
# 2023-01-30 | 400   | 9450   | 315.0  | 500    | 100    | 112.3
```

**任務清單：**
1. [ ] 使用 `expanding().sum()` 累計求和
2. [ ] 使用 `expanding().mean()` 累計平均
3. [ ] 使用 `expanding().max()` 和 `expanding().min()`
4. [ ] 分析穩定性趨勢

---

#### 題 8: 年度累計（YTD）
**難度：中等 | 預計時間：20 分鐘**

計算年度累計銷售追蹤目標達成進度：

```python
import pandas as pd
import numpy as np

# 全年銷售數據
dates = pd.date_range('2023-01-01', periods=365, freq='D')
sales = pd.Series(
    np.random.randint(100, 500, 365),
    index=dates
)

# 任務 1: 計算 YTD（Year-to-Date）銷售
# 任務 2: 設定年度目標為 $100,000，計算 YTD vs 目標進度
# 任務 3: 計算需要的平均每日銷售以達成目標
# 任務 4: 識別低於目標進度的日期

# 預期輸出:
# date       | daily_sales | ytd_sales | ytd_target | % completion | on_pace
# 2023-01-01 | 250         | 250       | 274        | 0.25%        | No
# 2023-06-30 | 300         | 52500     | 50000      | 52.5%        | Yes
# 2023-12-31 | 350         | 110000    | 100000     | 110%         | Yes
```

**任務清單：**
1. [ ] 使用 `expanding().sum()` 計算 YTD
2. [ ] 計算日度目標
3. [ ] 計算完成進度百分比
4. [ ] 預警低於目標的日期

---

#### 題 9: 季度累計（QTD）與月度累計（MTD）
**難度：中等 | 預計時間：20 分鐘**

計算季度和月度的累計指標：

```python
import pandas as pd
import numpy as np

# 全年銷售數據
dates = pd.date_range('2023-01-01', periods=365, freq='D')
sales = pd.DataFrame({
    'date': dates,
    'sales': np.random.randint(100, 500, 365)
})

# 任務 1: 提取季度和月份信息
# 任務 2: 計算 QTD（Quarter-to-Date）銷售
# 任務 3: 計算 MTD（Month-to-Date）銷售
# 任務 4: 比較 MTD 末日與月度目標

# 預期輸出:
# date       | sales | quarter | qtd_sales | month | mtd_sales | mtd_target | % mtd
# 2023-01-01 | 250   | 1       | 250       | 1     | 250       | 10000      | 2.5%
# 2023-01-31 | 320   | 1       | 9600      | 1     | 9600      | 10000      | 96%
# 2023-04-01 | 280   | 2       | 280       | 4     | 280       | 10500      | 2.7%
```

**任務清單：**
1. [ ] 提取 quarter 和 month 欄位
2. [ ] 按季度和月份分組，計算累計
3. [ ] 設定月度目標進行比較
4. [ ] 計算完成百分比

---

### 🔴 困難題

#### 題 10: 進階 Bollinger Bands 與異常檢測
**難度：困難 | 預計時間：25 分鐘**

實現 Bollinger Bands 進行市場異常檢測：

```python
import pandas as pd
import numpy as np

# 股票/商品價格數據
dates = pd.date_range('2023-01-01', periods=200, freq='D')
prices = pd.Series(
    100 + np.cumsum(np.random.randn(200) * 2),
    index=dates
)

# 任務 1: 計算 20 日中軌（移動平均）
# 任務 2: 計算 20 日標準差
# 任務 3: 計算上軌（中軌 + 2*標準差）和下軌（中軌 - 2*標準差）
# 任務 4: 識別超買（價格 > 上軌）和超賣（價格 < 下軌）情況
# 任務 5: 計算 Band Width（上軌 - 下軌 / 中軌）識別波動率水平

# 預期輸出:
# date       | price  | middle | upper  | lower  | overbought | oversold | band_width
# 2023-01-01 | 100.5  | NaN    | NaN    | NaN    | False      | False    | NaN
# 2023-01-21 | 105.2  | 102.3  | 107.8  | 96.8   | False      | False    | 5.6%
# 2023-02-10 | 110.5  | 104.2  | 110.1  | 98.3   | True       | False    | 11.4%
```

**任務清單：**
1. [ ] 計算 20 日 MA（中軌）
2. [ ] 計算 20 日標準差
3. [ ] 計算上下軌
4. [ ] 識別超買超賣
5. [ ] 計算波動帶寬

---

#### 題 11: 多時間窗口組合分析
**難度：困難 | 預計時間：25 分鐘**

實現多時間窗口的交叉分析：

```python
import pandas as pd
import numpy as np

# 銷售數據
dates = pd.date_range('2023-01-01', periods=100, freq='D')
sales = pd.Series(
    np.random.randint(100, 500, 100),
    index=dates
)

# 任務 1: 計算 5, 10, 20, 50 日四個 SMA
# 任務 2: 識別所有可能的 SMA 交叉信號
# 任務 3: 計算基於 SMA 交叉的交易信號強度
# 任務 4: 統計各交叉信號的準確率（假設股價上漲為交叉後的真實結果）

# 預期輸出:
# date       | sales | sma5  | sma10 | sma20 | sma50 | signal_type    | strength
# 2023-01-01 | 250   | NaN   | NaN   | NaN   | NaN   | -              | 0
# 2023-01-31 | 350   | 310   | 305   | 300   | NaN   | buy_5_10       | 3/4
```

**任務清單：**
1. [ ] 計算多個不同期數的 SMA
2. [ ] 識別所有可能的交叉組合
3. [ ] 實現信號評分機制
4. [ ] 統計信號有效性

---

#### 題 12: 時間序列完整性與異常修復
**難度：困難 | 預計時間：25 分鐘**

處理實際時間序列的數據質量問題：

```python
import pandas as pd
import numpy as np

# 有缺失、重複、異常值的銷售數據
raw_data = pd.DataFrame({
    'date': ['2023-01-01', '2023-01-02', '2023-01-02', '2023-01-04',
             '2023-01-05', '2023-01-10', '2023-01-11', '2023-01-12'],
    'sales': [100, 150, 140, 5000,  # 4000 為異常值
              200, 250, 300, 320]
})

# 任務 1: 識別並移除重複記錄（保留第一次出現）
# 任務 2: 識別缺失日期並插入 NaN
# 任務 3: 識別異常值（IQR 方法或 Z-Score）
# 任務 4: 修復異常值（使用中位數或線性插值）
# 任務 5: 驗證修復後的時間序列連續性和合理性

# 預期輸出:
# 原始記錄: 8
# 重複記錄: 1
# 缺失日期: ['2023-01-03', '2023-01-06', '2023-01-07', '2023-01-08', '2023-01-09']
# 異常值檢測: 5000 (2023-01-04)
# 修復方式: 使用線性插值 -> 175
# 最終記錄: 12
#
# 修復前後對比:
# date       | original | is_anomaly | modified | method
# 2023-01-02 | 150      | False      | 150      | -
# 2023-01-02 | 140      | True       | -        | removed
# 2023-01-04 | 5000     | True       | 175      | interpolate
```

**任務清單：**
1. [ ] 使用 `duplicated()` 移除重複
2. [ ] 使用 `reindex()` 填補缺失日期
3. [ ] 實現多種異常檢測方法
4. [ ] 實現多種異常值修復方法
5. [ ] 驗證修復結果的合理性

---

## 解答檢查清單

完成所有題目後，請檢查：

- [ ] 所有日期索引都設置正確
- [ ] 聚合函數的結果符合預期
- [ ] 移動平均線沒有前向偏差
- [ ] 累計計算從第一行開始
- [ ] NaN 值的處理恰當
- [ ] 所有計算都經過驗證

---

## 進階延伸

1. **實時計算**：為流式數據實現增量的滾動窗口
2. **分層聚合**：多層級時間序列聚合
3. **自適應窗口**：根據數據特性自動調整窗口大小
4. **並行計算**：大規模數據的並行 resample 和 rolling

---

**預計總耗時：** 2 小時
**建議完成方式：** 分兩個 60 分鐘的會話完成（簡單題 + 部分中等題；剩餘中等題 + 困難題）
