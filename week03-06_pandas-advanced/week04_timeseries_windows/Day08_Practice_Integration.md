# Day 8: 實踐整合 - 時間序列分析儀表板

## 概述
整合 Day 5-7 所有技能，建立一個完整的時間序列分析儀表板。此專案結合了日期時間處理、重採樣、移動平均線、同期比較等所有概念。

**學習時間：** 5 小時（含完整項目）
**難度：** 困難
**目標：** 建立可用於實際業務的分析工具

---

## 項目概述

### 目標
使用 Olist 電商數據集，建立一個時間序列分析系統，包含以下功能：

1. **日週月趨勢分析** - 不同時間粒度的銷售數據聚合
2. **移動平均線分析** - 識別短期和長期趨勢
3. **同期比較** - MoM、YoY、QoQ 分析
4. **YTD 累計** - 年度目標達成追蹤
5. **成長率分析** - 增長加速/減速識別
6. **異常檢測** - 識別異常銷售日期

### 數據源
模擬 Olist 訂單數據（2023 全年）

---

## 完整代碼

### Part 1: 數據準備

```python
import pandas as pd
import numpy as np
from datetime import datetime, timedelta
import warnings
warnings.filterwarnings('ignore')

# ============================================
# 1. 生成模擬 Olist 數據
# ============================================

np.random.seed(42)
n_records = 5000

# 生成日期（2023 年全年）
dates = pd.date_range('2023-01-01', periods=365, freq='D')
order_dates = np.random.choice(dates, n_records)

# 建立 DataFrame
orders = pd.DataFrame({
    'order_id': range(1, n_records + 1),
    'order_date': order_dates,
    'customer_id': np.random.randint(1000, 3000, n_records),
    'order_value': np.random.randint(50, 1000, n_records),
    'product_category': np.random.choice(
        ['Electronics', 'Clothing', 'Home', 'Sports', 'Books'],
        n_records
    )
})

# 排序以便分析
orders = orders.sort_values('order_date').reset_index(drop=True)

# 轉換日期格式
orders['order_date'] = pd.to_datetime(orders['order_date'])

# 設置日期為索引
orders_ts = orders.set_index('order_date')

print("數據集概覽:")
print(orders.head(10))
print(f"\n數據範圍: {orders['order_date'].min().date()} 到 {orders['order_date'].max().date()}")
print(f"總訂單數: {len(orders):,}")
print(f"總銷售額: ${orders['order_value'].sum():,.0f}")

# ============================================
# 2. 提取日期屬性
# ============================================

orders['year'] = orders['order_date'].dt.year
orders['month'] = orders['order_date'].dt.month
orders['day'] = orders['order_date'].dt.day
orders['quarter'] = orders['order_date'].dt.quarter
orders['week'] = orders['order_date'].dt.isocalendar().week
orders['day_of_week'] = orders['order_date'].dt.day_name()
orders['day_of_week_num'] = orders['order_date'].dt.dayofweek
orders['is_weekend'] = orders['day_of_week_num'].isin([5, 6])
orders['year_month'] = orders['order_date'].dt.to_period('M')
orders['year_week'] = orders['order_date'].dt.to_period('W')

print("\n數據屬性提取完成")
print(orders[['order_date', 'year', 'month', 'quarter', 'week', 'day_of_week']].head())
```

---

### Part 2: 日週月趨勢分析

```python
# ============================================
# 3. 日級銷售數據
# ============================================

# 按日期聚合
daily_summary = orders.groupby(orders['order_date'].dt.date).agg({
    'order_id': 'count',
    'order_value': ['sum', 'mean', 'std', 'min', 'max']
}).reset_index()

daily_summary.columns = ['date', 'orders', 'total_sales', 'avg_order', 'std_order', 'min_order', 'max_order']
daily_summary['date'] = pd.to_datetime(daily_summary['date'])
daily_summary = daily_summary.set_index('date')

print("日級銷售摘要:")
print(daily_summary.head(10))

# ============================================
# 4. 週級銷售數據
# ============================================

weekly_summary = orders_ts.resample('W').agg({
    'order_id': 'count',
    'order_value': ['sum', 'mean', 'std']
}).reset_index()

weekly_summary.columns = ['week_end_date', 'orders', 'total_sales', 'avg_order', 'std_order']
weekly_summary = weekly_summary.set_index('week_end_date')

print("\n週級銷售摘要:")
print(weekly_summary.head(15))

# ============================================
# 5. 月級銷售數據
# ============================================

monthly_summary = orders_ts.resample('ME').agg({
    'order_id': 'count',
    'order_value': ['sum', 'mean', 'std']
}).reset_index()

monthly_summary.columns = ['month_end_date', 'orders', 'total_sales', 'avg_order', 'std_order']
monthly_summary = monthly_summary.set_index('month_end_date')

# 添加月份名稱
monthly_summary['month_name'] = monthly_summary.index.strftime('%Y-%m')

print("\n月級銷售摘要:")
print(monthly_summary)

# ============================================
# 6. 季度銷售數據
# ============================================

quarterly_summary = orders_ts.resample('QE').agg({
    'order_id': 'count',
    'order_value': ['sum', 'mean', 'std']
}).reset_index()

quarterly_summary.columns = ['quarter_end_date', 'orders', 'total_sales', 'avg_order', 'std_order']

print("\n季度銷售摘要:")
print(quarterly_summary)
```

---

### Part 3: 移動平均線分析

```python
# ============================================
# 7. 簡單移動平均線（SMA）
# ============================================

daily_summary['sma_7'] = daily_summary['total_sales'].rolling(window=7).mean()
daily_summary['sma_30'] = daily_summary['total_sales'].rolling(window=30).mean()

print("日度銷售 + 7 日和 30 日 SMA:")
print(daily_summary[['total_sales', 'sma_7', 'sma_30']].head(35))

# 繪製簡單的文本圖表
print("\n銷售趨勢（最後 30 天）:")
for idx, row in daily_summary[['total_sales', 'sma_7', 'sma_30']].tail(30).iterrows():
    actual = '█' * int(row['total_sales'] / 100)
    sma7 = '─' * int((row['sma_7'] or 0) / 100)
    print(f"{idx}: {actual}")

# ============================================
# 8. 指數加權移動平均線（EWMA）
# ============================================

daily_summary['ewma_7'] = daily_summary['total_sales'].ewm(span=7, adjust=False).mean()
daily_summary['ewma_30'] = daily_summary['total_sales'].ewm(span=30, adjust=False).mean()

print("\n日度銷售 + EWMA:")
print(daily_summary[['total_sales', 'ewma_7', 'ewma_30']].tail(20))

# ============================================
# 9. 波動率分析
# ============================================

daily_summary['volatility_7'] = daily_summary['total_sales'].rolling(window=7).std()
daily_summary['volatility_30'] = daily_summary['total_sales'].rolling(window=30).std()

# Bollinger Bands
daily_summary['bb_middle'] = daily_summary['total_sales'].rolling(window=20).mean()
daily_summary['bb_std'] = daily_summary['total_sales'].rolling(window=20).std()
daily_summary['bb_upper'] = daily_summary['bb_middle'] + (daily_summary['bb_std'] * 2)
daily_summary['bb_lower'] = daily_summary['bb_middle'] - (daily_summary['bb_std'] * 2)

# 識別異常
daily_summary['is_above_bb'] = daily_summary['total_sales'] > daily_summary['bb_upper']
daily_summary['is_below_bb'] = daily_summary['total_sales'] < daily_summary['bb_lower']

print("\nBollinger Bands 分析:")
anomalies = daily_summary[daily_summary['is_above_bb'] | daily_summary['is_below_bb']]
print(f"異常天數: {len(anomalies)}")
print(anomalies[['total_sales', 'bb_middle', 'bb_upper', 'bb_lower']].head(10))

# ============================================
# 10. 高低點分析
# ============================================

daily_summary['high_30'] = daily_summary['total_sales'].rolling(window=30).max()
daily_summary['low_30'] = daily_summary['total_sales'].rolling(window=30).min()
daily_summary['range_30'] = daily_summary['high_30'] - daily_summary['low_30']

print("\n30 日高低點:")
print(daily_summary[['total_sales', 'high_30', 'low_30', 'range_30']].tail(20))
```

---

### Part 4: 同期比較分析

```python
# ============================================
# 11. 環比分析（MoM - Month-over-Month）
# ============================================

monthly_summary['sales_mom'] = monthly_summary['total_sales'].pct_change() * 100
monthly_summary['orders_mom'] = monthly_summary['orders'].pct_change() * 100
monthly_summary['avg_order_mom'] = monthly_summary['avg_order'].pct_change() * 100

print("月環比分析（MoM）:")
print(monthly_summary[['total_sales', 'sales_mom', 'orders', 'orders_mom']])

# ============================================
# 12. 同比分析（YoY - Year-over-Year）
# ============================================

# 由於只有 1 年數據，創建假想的去年數據用於演示
previous_year_monthly = monthly_summary.copy()
previous_year_monthly['total_sales'] = previous_year_monthly['total_sales'] * 0.85  # 假設去年低 15%
previous_year_monthly.index = previous_year_monthly.index - pd.DateOffset(years=1)

# 合併數據
yoy_data = pd.concat([previous_year_monthly[['total_sales']], monthly_summary[['total_sales']]], axis=1)
yoy_data.columns = ['sales_prior_year', 'sales_current_year']
yoy_data['yoy_pct'] = (yoy_data['sales_current_year'] - yoy_data['sales_prior_year']) / yoy_data['sales_prior_year'] * 100

print("\nYear-over-Year 分析（假想數據）:")
print(yoy_data)

# ============================================
# 13. 日度環比
# ============================================

daily_summary['daily_mom'] = daily_summary['total_sales'].pct_change() * 100
daily_summary['previous_day'] = daily_summary['total_sales'].shift(1)

print("\n日度環比（最後 15 天）:")
print(daily_summary[['total_sales', 'previous_day', 'daily_mom']].tail(15))

# ============================================
# 14. 週環比
# ============================================

weekly_summary['wow_pct'] = weekly_summary['total_sales'].pct_change() * 100

print("\n週環比分析（WoW）:")
print(weekly_summary[['total_sales', 'wow_pct']])

# ============================================
# 15. 季度環比
# ============================================

quarterly_summary['qoq_pct'] = quarterly_summary['total_sales'].pct_change() * 100

print("\n季度環比分析（QoQ）:")
print(quarterly_summary[['total_sales', 'qoq_pct']])
```

---

### Part 5: YTD 累計分析

```python
# ============================================
# 16. 年度累計（YTD）
# ============================================

# 重新準備數據用於 YTD 計算
daily_sales_series = orders_ts['order_value'].resample('D').sum()
daily_sales_df = daily_sales_series.reset_index()
daily_sales_df.columns = ['date', 'daily_sales']
daily_sales_df['date'] = pd.to_datetime(daily_sales_df['date'])

# 計算 YTD
daily_sales_df['ytd_sales'] = daily_sales_df['daily_sales'].expanding().sum()
daily_sales_df['ytd_avg_daily'] = daily_sales_df['ytd_sales'] / (daily_sales_df.index + 1)

print("年度累計銷售（YTD）:")
print(daily_sales_df[['date', 'daily_sales', 'ytd_sales', 'ytd_avg_daily']].head(40))

# YTD 與目標比較
annual_target = 1500000  # 假設年度目標
daily_sales_df['ytd_target'] = annual_target * (daily_sales_df.index + 1) / 365
daily_sales_df['ytd_vs_target'] = (daily_sales_df['ytd_sales'] - daily_sales_df['ytd_target']) / daily_sales_df['ytd_target'] * 100

print("\nYTD vs 年度目標:")
print(daily_sales_df[['date', 'ytd_sales', 'ytd_target', 'ytd_vs_target']].iloc[[30, 60, 90, 180, 270, 364]])

# ============================================
# 17. 月度累計（MTD）
# ============================================

daily_sales_df['month'] = daily_sales_df['date'].dt.month
daily_sales_df['mtd_sales'] = (
    daily_sales_df.groupby('month')['daily_sales'].transform(lambda x: x.expanding().sum())
)

print("\n月度累計銷售（MTD）:")
print(daily_sales_df[['date', 'daily_sales', 'mtd_sales']].head(35))

# ============================================
# 18. 季度累計（QTD）
# ============================================

daily_sales_df['quarter'] = daily_sales_df['date'].dt.quarter
daily_sales_df['qtd_sales'] = (
    daily_sales_df.groupby('quarter')['daily_sales'].transform(lambda x: x.expanding().sum())
)

print("\n季度累計銷售（QTD）:")
print(daily_sales_df[['date', 'daily_sales', 'qtd_sales']].head(95))
```

---

### Part 6: 成長率分析

```python
# ============================================
# 19. 日度成長率
# ============================================

daily_sales_df['daily_growth_pct'] = daily_sales_df['daily_sales'].pct_change() * 100

print("日度成長率分析:")
print(daily_sales_df[['date', 'daily_sales', 'daily_growth_pct']].head(20))

# ============================================
# 20. 計算成長率加速/減速
# ============================================

# 計算成長率的變化
daily_sales_df['growth_accel'] = daily_sales_df['daily_growth_pct'].diff()

# 正加速 = 成長率增速
# 負加速 = 成長率減速
daily_sales_df['accel_direction'] = daily_sales_df['growth_accel'].apply(
    lambda x: '加速' if x > 0 else ('減速' if x < 0 else '持平')
)

print("\n成長率加速/減速分析:")
print(daily_sales_df[['date', 'daily_growth_pct', 'growth_accel', 'accel_direction']].head(30))

# ============================================
# 21. CAGR（年均複合增長率）
# ============================================

# 月度 CAGR 計算示例
monthly_values = monthly_summary['total_sales'].values
first_month = monthly_values[0]
last_month = monthly_values[-1]
months = len(monthly_values) - 1

# 月度 CAGR
monthly_cagr = (last_month / first_month) ** (1 / months) - 1

print(f"\n月度 CAGR 分析:")
print(f"首月銷售額: ${first_month:,.0f}")
print(f"末月銷售額: ${last_month:,.0f}")
print(f"月度 CAGR: {monthly_cagr * 100:.2f}%")

# ============================================
# 22. 成長趨勢分類
# ============================================

def classify_growth(growth_pct):
    if growth_pct > 20:
        return '高速增長'
    elif growth_pct > 5:
        return '中速增長'
    elif growth_pct > 0:
        return '低速增長'
    elif growth_pct > -5:
        return '小幅下降'
    else:
        return '大幅下降'

daily_sales_df['growth_category'] = daily_sales_df['daily_growth_pct'].apply(classify_growth)

print("\n按成長速度分類:")
print(daily_sales_df['growth_category'].value_counts())
```

---

### Part 7: 異常檢測

```python
# ============================================
# 23. 統計異常檢測（Z-Score）
# ============================================

from scipy import stats

daily_sales_df['z_score'] = np.abs(stats.zscore(daily_sales_df['daily_sales'].fillna(0)))
daily_sales_df['is_outlier_zscore'] = daily_sales_df['z_score'] > 2  # 2 個標準差

print("Z-Score 異常檢測:")
outliers_zscore = daily_sales_df[daily_sales_df['is_outlier_zscore']]
print(f"異常日期數: {len(outliers_zscore)}")
print(outliers_zscore[['date', 'daily_sales', 'z_score']].head(10))

# ============================================
# 24. IQR 異常檢測
# ============================================

Q1 = daily_sales_df['daily_sales'].quantile(0.25)
Q3 = daily_sales_df['daily_sales'].quantile(0.75)
IQR = Q3 - Q1
lower_bound = Q1 - 1.5 * IQR
upper_bound = Q3 + 1.5 * IQR

daily_sales_df['is_outlier_iqr'] = (
    (daily_sales_df['daily_sales'] < lower_bound) |
    (daily_sales_df['daily_sales'] > upper_bound)
)

print("\nIQR 異常檢測:")
print(f"Q1: {Q1:.0f}, Q3: {Q3:.0f}")
print(f"下界: {lower_bound:.0f}, 上界: {upper_bound:.0f}")
outliers_iqr = daily_sales_df[daily_sales_df['is_outlier_iqr']]
print(f"異常日期數: {len(outliers_iqr)}")
print(outliers_iqr[['date', 'daily_sales']].head(10))

# ============================================
# 25. 同期比較異常檢測
# ============================================

# 與去年同期比較（使用模擬數據）
daily_sales_df['day_of_year'] = daily_sales_df['date'].dt.dayofyear
daily_sales_df['day_of_week'] = daily_sales_df['date'].dt.day_name()

# 計算同星期幾的平均銷售
dow_avg = daily_sales_df.groupby('day_of_week')['daily_sales'].mean()
daily_sales_df['dow_avg_sales'] = daily_sales_df['day_of_week'].map(dow_avg)
daily_sales_df['deviation_from_dow_avg'] = (
    (daily_sales_df['daily_sales'] - daily_sales_df['dow_avg_sales']) /
    daily_sales_df['dow_avg_sales'] * 100
)

print("\n同星期幾異常檢測:")
print(daily_sales_df[['date', 'day_of_week', 'daily_sales', 'dow_avg_sales', 'deviation_from_dow_avg']].head(20))

# 識別明顯偏離的日期
significant_deviation = daily_sales_df[daily_sales_df['deviation_from_dow_avg'].abs() > 50]
print(f"\n顯著偏離同星期幾平均的日期: {len(significant_deviation)}")
print(significant_deviation[['date', 'day_of_week', 'daily_sales', 'deviation_from_dow_avg']].head(10))
```

---

### Part 8: 綜合儀表板輸出

```python
# ============================================
# 26. 綜合儀表板摘要
# ============================================

print("=" * 80)
print("時間序列分析儀表板 - 2023 年度報告")
print("=" * 80)

print("\n【1. 年度概覽】")
print(f"數據期間: {orders['order_date'].min().date()} ~ {orders['order_date'].max().date()}")
print(f"總訂單數: {len(orders):,} 單")
print(f"總銷售額: ${orders['order_value'].sum():,.0f}")
print(f"平均訂單值: ${orders['order_value'].mean():,.0f}")
print(f"日均訂單數: {len(orders) / 365:.0f} 單")
print(f"日均銷售額: ${orders['order_value'].sum() / 365:,.0f}")

print("\n【2. 月度表現】")
monthly_perf = monthly_summary[['total_sales', 'orders', 'sales_mom']].copy()
monthly_perf.columns = ['銷售額', '訂單數', '環比增長%']
print(monthly_perf)

print("\n【3. 季度表現】")
quarterly_perf = quarterly_summary[['total_sales', 'orders', 'qoq_pct']].copy()
quarterly_perf.columns = ['銷售額', '訂單數', '環比增長%']
print(quarterly_perf)

print("\n【4. 移動平均線指標（最後 30 天）】")
ma_summary = daily_summary[['total_sales', 'sma_7', 'sma_30', 'volatility_30']].tail(30)
print(f"最後日銷售額: ${ma_summary.iloc[-1]['total_sales']:,.0f}")
print(f"7 日 SMA: ${ma_summary['sma_7'].iloc[-1]:,.0f}")
print(f"30 日 SMA: ${ma_summary['sma_30'].iloc[-1]:,.0f}")
print(f"30 日波動率: ${ma_summary['volatility_30'].iloc[-1]:,.0f}")

print("\n【5. 異常檢測摘要】")
print(f"Z-Score 異常日期: {daily_sales_df['is_outlier_zscore'].sum()}")
print(f"IQR 異常日期: {daily_sales_df['is_outlier_iqr'].sum()}")
print(f"同星期幾顯著偏離日期: {len(significant_deviation)}")

print("\n【6. 成長率分析】")
print(f"平均日成長率: {daily_sales_df['daily_growth_pct'].mean():.2f}%")
print(f"最大日增長: {daily_sales_df['daily_growth_pct'].max():.2f}%")
print(f"最大日下降: {daily_sales_df['daily_growth_pct'].min():.2f}%")

print("\n【7. 產品類別表現】")
category_perf = orders.groupby('product_category').agg({
    'order_id': 'count',
    'order_value': ['sum', 'mean']
}).round(0)
category_perf.columns = ['訂單數', '銷售額', '平均訂單值']
category_perf = category_perf.sort_values('銷售額', ascending=False)
print(category_perf)

print("\n" + "=" * 80)
```

---

## 練習題

### 練習 1: 比較不同移動平均窗口
修改 SMA 的窗口大小（如 14、21 天），比較不同窗口對趨勢識別的影響。

### 練習 2: 自訂異常檢測
實現基於 Bollinger Bands 的交易信號生成。

### 練習 3: 預測
基於歷史 SMA，預測未來 7 天的銷售。

### 練習 4: 分類分析
為每個產品類別建立獨立的時間序列分析。

### 練習 5: 假日效應分析
識別假日（如黑色星期五、年末）對銷售的影響。

---

## 關鍵知識點回顧

### Day 5: DateTime 基礎
- `pd.to_datetime()` - 日期轉換
- `dt` accessor - 日期屬性提取
- `pd.date_range()` - 日期序列生成
- Timedelta 和 DateOffset - 時間計算

### Day 6: Resample 與 Rolling
- `resample()` - 時間序列重採樣
- `rolling()` - 移動視窗計算
- `expanding()` - 累計統計

### Day 7: 時間比較
- `shift()` - 時間平移
- `pct_change()` - 增長率計算
- 同期比較 - MoM、YoY、QoQ

---

## 實戰建議

1. **數據驗證**：始終檢查日期範圍和缺失值
2. **時區處理**：國際業務中需特別注意
3. **異常檢測**：多種方法結合使用效果更好
4. **可視化**：時間序列最適合用圖表展示
5. **性能優化**：大型數據集使用適當的聚合粒度

---

## 進階主題

1. **時間序列分解**：將數據分離為趨勢、季節性、殘差
2. **自相關分析**：ACFPLAC 分析
3. **預測模型**：ARIMA、Prophet、LSTM
4. **實時監控**：流式數據的增量計算

---

**本章節耗時：** 5 小時
**預計完成時間：** 1 天
**作者備註：** 這個專案展示了如何在實際業務中應用時間序列技能。建議在完成後進行代碼最佳化和視覺化改進。
