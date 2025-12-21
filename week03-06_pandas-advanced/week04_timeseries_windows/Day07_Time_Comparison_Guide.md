# Day 7: 時間比較與同期分析指南

## 概述
掌握時間序列比較技能，從簡單的按時間平移 (shift) 到複雜的同期比較 (MoM, YoY, WoW)，以及成長率和趨勢分析。

**學習時間：** 6 小時（3 部分）
**難度：** 中等-困難
**主要工具：** `shift()`, `pct_change()`, `diff()`, 自訂比較函數

---

## Part 1: Shift 時間平移（2 小時）

### 1.1 基礎 Shift 操作

#### 概念
`shift()` 用於向上或向下移動行，從而獲取上一期、下一期或去年同期的數據。

```python
import pandas as pd
import numpy as np

# 建立 3 年每日銷售數據
dates = pd.date_range('2021-01-01', periods=1095, freq='D')
sales_data = pd.DataFrame({
    'date': dates,
    'sales': np.random.randint(100, 500, 1095)
})

sales_data.set_index('date', inplace=True)

print("原始數據（前 10 行）:")
print(sales_data.head(10))
#             sales
# 2021-01-01    250
# 2021-01-02    380
# 2021-01-03    150
# 2021-01-04    420
# 2021-01-05    280

# 1. 向下 Shift（向後看，上一期數據）
sales_data['previous_day'] = sales_data['sales'].shift(1)

print("\n當日 vs 前一日:")
print(sales_data[['sales', 'previous_day']].head(10))
#             sales  previous_day
# 2021-01-01    250            NaN
# 2021-01-02    380            250
# 2021-01-03    150            380
# 2021-01-04    420            150

# 2. 向上 Shift（向前看，下一期數據）
sales_data['next_day'] = sales_data['sales'].shift(-1)

print("\n當日 vs 下一日:")
print(sales_data[['sales', 'next_day']].head(10))

# 3. Shift 多期（去年同期）
# 365 天前（大約 1 年）
sales_data['sales_1y_ago'] = sales_data['sales'].shift(365)

print("\n當日 vs 去年同期（前 370 行）:")
print(sales_data[['sales', 'sales_1y_ago']].iloc[360:375])

# 4. Shift 多期（上季度）
# 90 天前（大約 1 季度）
sales_data['sales_1q_ago'] = sales_data['sales'].shift(90)

print("\n當日 vs 去季度同期:")
print(sales_data[['sales', 'sales_1q_ago']].head(95))

# 5. 多列同時 Shift
sales_data['previous_3_days'] = sales_data['sales'].shift(3)
sales_data['previous_7_days'] = sales_data['sales'].shift(7)
sales_data['previous_30_days'] = sales_data['sales'].shift(30)

print("\n不同期間對比:")
print(sales_data[['sales', 'previous_3_days', 'previous_7_days', 'previous_30_days']].head(35))
```

#### Excel 對照
```excel
=OFFSET(A1, -1, 0)     // 上一行數據
=OFFSET(A1, 1, 0)      // 下一行數據
=OFFSET(A1, -365, 0)   // 去年同期
```

### 1.2 Shift 與分組

#### 概念
在分組環境中使用 shift，可以按類別比較相鄰期間的數據。

```python
# 建立多個門店的銷售數據
dates = pd.date_range('2023-01-01', periods=90, freq='D')
stores = ['Store_A', 'Store_B', 'Store_C']

sales_multi = pd.DataFrame({
    'date': dates.repeat(len(stores)),
    'store': stores * len(dates),
    'sales': np.random.randint(100, 500, 90 * 3)
})

print("多門店銷售數據（前 10 行）:")
print(sales_multi.head(10))

# 1. 按門店分組並 Shift
sales_multi['previous_day_sales'] = (
    sales_multi.groupby('store')['sales'].shift(1)
)

print("\n按門店分組的前一日銷售:")
print(sales_multi.head(15))

# 2. 檢查 Shift 邊界
# 第一個 Store_A 的前一日應該是 NaN
# 第一個 Store_B 的前一日也應該是 NaN（不是 Store_A 的最後一天）
print("\n邊界檢查（應該看到 NaN）:")
print(sales_multi[sales_multi.index.isin([0, 90, 180])])

# 3. 多門店按時間和門店分組 Shift
sales_multi['prev_week_sales'] = (
    sales_multi.groupby('store')['sales'].shift(7)
)

print("\n按門店分組的前 7 日銷售:")
print(sales_multi[['date', 'store', 'sales', 'prev_week_sales']].head(20))
```

#### Excel 對照
```excel
=IFERROR(VLOOKUP(store & "前一日", lookup_table, 2, 0), "")
// 需要建立 Helper 列
```

### 1.3 填補 Shift 後的 NaN

#### 概念
Shift 會產生 NaN 值，需要進行填補或移除。

```python
# 簡單數據
data = pd.Series(
    [10, 20, 30, 40, 50],
    index=pd.date_range('2023-01-01', periods=5, freq='D')
)

# Shift 後包含 NaN
shifted = data.shift(1)
print("Shift 後（包含 NaN）:")
print(shifted)
#     10
# 2023-01-01 NaN
# 2023-01-02 10.0
# 2023-01-03 20.0
# 2023-01-04 30.0
# 2023-01-05 40.0

# 1. 刪除 NaN 行
shifted_clean = shifted.dropna()
print("\n刪除 NaN 後:")
print(shifted_clean)

# 2. 向後填充 NaN（用下一個值填補）
shifted_bfill = shifted.bfill()
print("\n向後填充:")
print(shifted_bfill)

# 3. 向前填充 NaN（用前一個值填補）
shifted_ffill = shifted.ffill()
print("\n向前填充:")
print(shifted_ffill)

# 4. 用特定值填充
shifted_zero = shifted.fillna(0)
print("\n用 0 填充:")
print(shifted_zero)

# 5. 在計算中自動跳過 NaN
df = pd.DataFrame({
    'current': [10, 20, 30, 40, 50],
    'previous': [np.nan, 10, 20, 30, 40]
})

# 計算差異時自動跳過 NaN
df['diff'] = df['current'] - df['previous']
print("\n差異計算（自動跳過 NaN）:")
print(df)
```

---

## Part 2: pct_change 與 diff（2 小時）

### 2.1 百分比變化（pct_change）

#### 概念
計算相鄰期間的百分比變化率。

```python
# 每日價格數據
price_data = pd.DataFrame({
    'date': pd.date_range('2023-01-01', periods=20, freq='D'),
    'price': [100, 102, 101, 105, 103, 108, 107, 110, 109, 112,
              115, 114, 118, 120, 119, 122, 125, 124, 128, 130]
})

price_data.set_index('date', inplace=True)

# 1. 日環比增長率
price_data['pct_change_daily'] = price_data['price'].pct_change()

print("日環比增長率:")
print(price_data.head(10))
#             price  pct_change_daily
# 2023-01-01    100               NaN
# 2023-01-02    102            0.020000  (2%)
# 2023-01-03    101           -0.009804  (-0.98%)
# 2023-01-04    105            0.039604  (3.96%)

# 2. 百分比顯示（更易讀）
price_data['pct_change_pct'] = price_data['price'].pct_change() * 100

print("\nDaily return (%):")
print(price_data[['price', 'pct_change_pct']].head(10))

# 3. 週環比增長率
price_data['pct_change_weekly'] = price_data['price'].pct_change(periods=7)

print("\n週環比增長率 (7 日):")
print(price_data[['price', 'pct_change_daily', 'pct_change_weekly']].head(15))

# 4. 多期增長率
price_data['pct_change_3d'] = price_data['price'].pct_change(periods=3)
price_data['pct_change_5d'] = price_data['price'].pct_change(periods=5)

print("\n多期增長率:")
print(price_data[['price', 'pct_change_3d', 'pct_change_5d']])
```

#### Excel 對照
```excel
=(B2-B1)/B1        // 日增長率
=(B8-B1)/B1        // 週增長率
=(C1-C1)/C1        // 年增長率
```

### 2.2 絕對變化（diff）

#### 概念
計算相鄰期間的絕對值變化。

```python
# 銷售數據
sales = pd.Series(
    [100, 150, 120, 200, 180, 160, 140, 190, 170, 210],
    index=pd.date_range('2023-01-01', periods=10, freq='D')
)

# 1. 日銷售變化（絕對值）
sales_diff = sales.diff()
print("日銷售變化（絕對值）:")
print(sales_diff)
#     NaN
# 50
# -30
# 80
# -20
# -20
# -20
# 50
# -20
# 40

# 2. 判斷增長還是下降
df = pd.DataFrame({
    'sales': sales,
    'change': sales.diff(),
    'growing': sales.diff() > 0
})

print("\n銷售變化分析:")
print(df)

# 3. 多期差異
sales_diff_3 = sales.diff(periods=3)
print("\n3 日銷售變化:")
print(sales_diff_3)

# 4. 週度差異
sales_diff_weekly = sales.diff(periods=7)
print("\n週度銷售變化:")
print(sales_diff_weekly)

# 5. 累計變化
cumulative_change = sales.diff().cumsum() + sales.iloc[0]
print("\n累計銷售（從第一個值開始）:")
print(cumulative_change)
```

#### Excel 對照
```excel
=B2-B1             // 絕對變化
=(B2-B1)/B1        // 百分比變化
=SUM($B$1:B1)      // 累計變化
```

### 2.3 複合增長率（CAGR）

#### 概念
計算期間內的年均複合增長率。

```python
# 多年銷售數據
yearly_sales = pd.Series(
    [100, 120, 145, 174, 209],
    index=pd.date_range('2019-01-01', periods=5, freq='YE')
)

print("年度銷售:")
print(yearly_sales)

# 1. 計算 CAGR (Compound Annual Growth Rate)
start_value = yearly_sales.iloc[0]
end_value = yearly_sales.iloc[-1]
num_years = len(yearly_sales) - 1

cagr = (end_value / start_value) ** (1 / num_years) - 1

print(f"\n開始值: {start_value}")
print(f"結束值: {end_value}")
print(f"年數: {num_years}")
print(f"CAGR: {cagr:.4f} ({cagr*100:.2f}%)")

# 2. 計算每年的增長率
yearly_sales_pct = yearly_sales.pct_change()
print("\n年度增長率:")
print(yearly_sales_pct)

# 3. 累計增長（從基準年起）
cumulative_growth = yearly_sales / yearly_sales.iloc[0] - 1
print("\n累計增長（相對於 2019 年）:")
print(cumulative_growth)

# 4. CAGR 驗證
# 每年按 CAGR 複合增長
cagr_verification = pd.Series(
    [100 * (1 + cagr) ** i for i in range(len(yearly_sales))],
    index=yearly_sales.index
)
print("\nCAGR 驗證（預測值）:")
print(cagr_verification)
```

---

## Part 3: 同期比較（2 小時）

### 3.1 環比（MoM - Month-over-Month）

#### 概念
比較相鄰兩個月的數據變化。

```python
# 全年每月銷售數據
monthly_data = pd.DataFrame({
    'date': pd.date_range('2023-01-01', periods=12, freq='MS'),
    'sales': [10000, 11000, 9500, 12000, 11500, 13000,
              12500, 14000, 13500, 15000, 14500, 16000],
    'costs': [6000, 6500, 5700, 7000, 6800, 7500,
              7200, 8000, 7800, 8500, 8200, 9000]
})

monthly_data['month'] = monthly_data['date'].dt.month_name()

# 1. 月環比（MoM）增長率
monthly_data['sales_mom'] = monthly_data['sales'].pct_change()
monthly_data['sales_mom_pct'] = monthly_data['sales'].pct_change() * 100

# 2. 成本的月環比
monthly_data['costs_mom_pct'] = monthly_data['costs'].pct_change() * 100

# 3. 利潤計算和月環比
monthly_data['profit'] = monthly_data['sales'] - monthly_data['costs']
monthly_data['profit_mom_pct'] = monthly_data['profit'].pct_change() * 100

print("月環比分析:")
print(monthly_data[['month', 'sales', 'sales_mom_pct', 'profit', 'profit_mom_pct']])

# 4. 判斷趨勢
monthly_data['sales_trend'] = pd.cut(
    monthly_data['sales_mom_pct'],
    bins=[-np.inf, -5, 0, 5, np.inf],
    labels=['大幅下降', '小幅下降', '小幅增長', '大幅增長']
)

print("\n銷售趨勢分類:")
print(monthly_data[['month', 'sales_mom_pct', 'sales_trend']])
```

#### Excel 對照
```excel
=(B2-B1)/B1        // 月環比增長
```

### 3.2 同比（YoY - Year-over-Year）

#### 概念
比較同一季度或同一月份去年的數據。

```python
# 2 年的月度銷售數據
dates = pd.date_range('2022-01-01', periods=24, freq='MS')
sales_2year = pd.DataFrame({
    'date': dates,
    'sales': [10000, 11000, 9500, 12000, 11500, 13000, 12500, 14000, 13500, 15000, 14500, 16000,
              11000, 12000, 10500, 13200, 12800, 14500, 13800, 15500, 15000, 16500, 16000, 17500]
})

sales_2year['month'] = sales_2year['date'].dt.month
sales_2year['year'] = sales_2year['date'].dt.year

# 1. 計算 YoY（去年同月）
# 2023 年 1 月與 2022 年 1 月比較
sales_2year['sales_yoy'] = sales_2year['sales'].shift(12)  # 往回推 12 個月

# 2. YoY 增長率
sales_2year['sales_yoy_pct'] = sales_2year['sales'].pct_change(periods=12) * 100

print("年度同期比較:")
print(sales_2year[['date', 'sales', 'sales_yoy', 'sales_yoy_pct']])

# 3. 更清晰的顯示
sales_pivot = sales_2year.pivot(index='month', columns='year', values='sales')
print("\n按月份排列的 YoY:")
print(sales_pivot)

sales_pivot_yoy = (sales_pivot[2023] - sales_pivot[2022]) / sales_pivot[2022] * 100
print("\n年度同期增長率:")
print(sales_pivot_yoy)
```

#### Excel 對照
```excel
=SUMIFS($sales, $year, 2023, $month, 1) / SUMIFS($sales, $year, 2022, $month, 1) - 1
```

### 3.3 環比 vs 同比

#### 概念
理解環比和同比的區別，何時使用。

```python
# 完整數據集
daily_data = pd.DataFrame({
    'date': pd.date_range('2022-01-01', periods=730, freq='D'),
    'sales': np.random.randint(100, 500, 730)
})

daily_data['month'] = daily_data['date'].dt.month
daily_data['year'] = daily_data['date'].dt.year
daily_data['day_of_month'] = daily_data['date'].dt.day

# 1. 每月月底的銷售匯總
daily_data['is_month_end'] = daily_data['date'].dt.is_month_end
month_end_sales = daily_data[daily_data['is_month_end']].copy()

# 2. 環比（相鄰月份）
month_end_sales['mom_pct'] = month_end_sales['sales'].pct_change() * 100

# 3. 同比（去年同月）
month_end_sales['yoy_pct'] = month_end_sales['sales'].pct_change(periods=12) * 100

print("環比 vs 同比:")
print(month_end_sales[['date', 'sales', 'mom_pct', 'yoy_pct']].head(15))

# 4. 判斷哪個指標更有意義
print("\n環比用途：監測短期趨勢（季節性）")
print("同比用途：比較長期增長（年度增長）")
```

### 3.4 同期比較的實際應用

#### 概念
在實際業務分析中的應用。

```python
# 零售銷售數據（含多個分類）
sales_data = pd.DataFrame({
    'date': pd.date_range('2022-01-01', periods=730, freq='D'),
    'category': np.random.choice(['Electronics', 'Clothing', 'Food'], 730),
    'sales': np.random.randint(1000, 5000, 730)
})

# 1. 按分類和月份聚合
sales_data['year_month'] = sales_data['date'].dt.to_period('M')
monthly_by_category = sales_data.groupby(['year_month', 'category'])['sales'].sum().unstack(fill_value=0)

print("按分類的月度銷售:")
print(monthly_by_category.head(15))

# 2. 計算各分類的月環比
monthly_by_category['Electronics_mom'] = monthly_by_category['Electronics'].pct_change() * 100
monthly_by_category['Clothing_mom'] = monthly_by_category['Clothing'].pct_change() * 100

# 3. 按年份和月份分組計算同比
sales_data['year'] = sales_data['date'].dt.year
sales_data['month'] = sales_data['date'].dt.month

yearly_monthly = sales_data.groupby(['year', 'month'])['sales'].sum().unstack()
yearly_monthly_yoy = yearly_monthly.pct_change(fill_method=None) * 100

print("\nYoY 增長率:")
print(yearly_monthly_yoy)

# 4. 識別增長最快的月份
mom_stats = monthly_by_category['Electronics_mom'].describe()
print("\n環比增長統計:")
print(mom_stats)
```

---

## 實戰案例（10 個）

### 案例 1: 日度成長率追蹤

```python
daily_sales = pd.Series(
    np.random.randint(100, 500, 100),
    index=pd.date_range('2023-01-01', periods=100, freq='D')
)

analysis = pd.DataFrame({
    'sales': daily_sales,
    'previous_day': daily_sales.shift(1),
    'daily_growth': daily_sales.pct_change() * 100,
    'daily_change': daily_sales.diff()
})

print("日度成長分析:")
print(analysis.head(10))
```

### 案例 2: 週度環比

```python
weekly_data = pd.Series(
    [10000, 11000, 9500, 12000, 11500, 13000, 12500, 14000, 13500, 15000],
    index=pd.date_range('2023-01-01', periods=10, freq='W')
)

weekly_analysis = pd.DataFrame({
    'sales': weekly_data,
    'wow_growth': weekly_data.pct_change() * 100
})

print("週環比成長:")
print(weekly_analysis)
```

### 案例 3: 月度環比和同比

```python
monthly_sales = pd.Series(
    [100000, 110000, 95000, 120000, 115000, 130000,
     125000, 140000, 135000, 150000, 145000, 160000,
     110000, 121000, 104500, 132000, 126500, 143000,
     137500, 154000, 148500, 165000, 159500, 176000],
    index=pd.date_range('2022-01-01', periods=24, freq='MS')
)

monthly_analysis = pd.DataFrame({
    'sales': monthly_sales,
    'mom': monthly_sales.pct_change() * 100,
    'yoy': monthly_sales.pct_change(periods=12) * 100
})

print("月度環比和同比:")
print(monthly_analysis)
```

### 案例 4-10: 進階應用

```python
# 案例 4: 多分類的同期比較
# 案例 5: 季度環比（QoQ）
# 案例 6: 成長率加速/減速（二階導數）
# 案例 7: 累計增長追蹤
# 案例 8: 異常檢測（基於歷史同期）
# 案例 9: 預測下一期（基於環比趨勢）
# 案例 10: 帕累托分析（20/80 法則驗證）
```

---

## 關鍵知識點總結

| 功能 | 方法 | 用途 | Excel 對照 |
|-----|------|------|-----------|
| 上期數據 | `shift(1)` | 計算環比 | =B1 的上一行 |
| 去年數據 | `shift(365)` | 計算同比 | OFFSET(..., -365) |
| 環比增長 | `pct_change()` | 短期趨勢 | =(B2-B1)/B1 |
| 同比增長 | `pct_change(periods=12)` | 長期增長 | =(B13-B1)/B1 |
| 絕對變化 | `diff()` | 變化額 | =B2-B1 |
| CAGR | 自訂函數 | 年均增長 | =(end/start)^(1/年數)-1 |

---

## 常見錯誤與解決方案

### 錯誤 1: 遺漏邊界的 NaN
```python
# 錯誤（混入 NaN）
growth = data.pct_change()
summary = growth.describe()  # 可能包含 NaN 行

# 解決方案
growth = data.pct_change().dropna()
summary = growth.describe()
```

### 錯誤 2: 忘記按分組 Shift
```python
# 錯誤（跨分組 Shift）
monthly_multi['previous'] = monthly_multi['sales'].shift(1)

# 解決方案
monthly_multi['previous'] = monthly_multi.groupby('category')['sales'].shift(1)
```

### 錯誤 3: 同比時間不正確
```python
# 錯誤（月度用 360 天）
yoy = data.shift(360)  # 不准確

# 解決方案
yoy = data.shift(365)  # 日度用 365
yoy = data.shift(12)   # 月度用 12
yoy = data.shift(4)    # 季度用 4
```

---

## 練習題預覽

- **簡單：** Shift 基礎、pct_change 計算
- **中等：** 分組 Shift、MoM 計算
- **困難：** YoY 分析、多維度比較

詳見 Exercise_06_TimeComparison_10_Questions.md

---

## 參考資源

- Pandas 官方文檔：[Compare with prior periods](https://pandas.pydata.org/docs/user_guide/basics.html#comparing-with-prior-periods)
- 金融分析最佳實踐

---

**本章節耗時：** 6 小時
**預計完成時間：** 1 天
**作者備註：** 時間比較是商業分析中最常用的技能，特別是在月度和季度報告中，掌握這些技能將大大提升您的分析效率。
