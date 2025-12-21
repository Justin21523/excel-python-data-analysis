# Week 4: 時間序列 & 視窗函數 - 完整教學系統

## 系統概述

這是一個完整的時間序列分析教學系統，涵蓋 Pandas 日期時間處理、時間序列重採樣、移動視窗計算，以及同期比較分析的所有核心技能。

**總學習時間：** 24 小時（4 天，每天 6 小時）
**難度曲線：** 初級 → 中級 → 高級
**目標學生：** Excel 高級用戶，準備學習 Python 進階數據分析

---

## 系統結構

### 📚 教學資料（4 個指南）

#### 1️⃣ Day 5: DateTime 主要指南
**檔案：** `Day05_DateTime_Mastery_Guide.md`
**耗時：** 6 小時
**內容：**
- Part 1: DateTime 基礎（2h）- `pd.to_datetime()`, `dt accessor`, `date_range()`
- Part 2: Timedelta 與 DateOffset（2h）- 時間差計算、業務日期
- Part 3: Period vs Timestamp（2h）- 時間點 vs 時間區間
- 10 個實戰案例（訂單日期分析、配送時間計算）

**核心概念：**
```python
# 日期轉換
dates = pd.to_datetime(['2023-01-15', '2023-02-20'])

# 屬性提取
df['year'] = df['date'].dt.year
df['month'] = df['date'].dt.month

# 生成日期序列
date_range = pd.date_range('2023-01-01', periods=365, freq='D')

# 時間差計算
days_diff = (date2 - date1).dt.days

# 工作日計算
from pandas.tseries.offsets import BDay
next_workday = date + 1 * BDay()
```

---

#### 2️⃣ Day 6: Resample 與 Rolling 視窗函數
**檔案：** `Day06_Resample_Rolling_Guide.md`
**耗時：** 6 小時
**內容：**
- Part 1: Resample 重採樣（2h）- 日→週→月，升降採樣
- Part 2: Rolling 移動視窗（2.5h）- MA, WMA, rolling aggregations
- Part 3: Expanding 累計（1.5h）- YTD, cumsum, expanding mean
- 12 個實戰案例（銷售趨勢、移動平均線）

**核心概念：**
```python
# 升採樣：日 → 月
monthly = df.resample('ME').sum()

# 簡單移動平均線
df['sma_7'] = df['price'].rolling(7).mean()
df['sma_30'] = df['price'].rolling(30).mean()

# 指數加權平均
df['ewma'] = df['price'].ewm(span=7, adjust=False).mean()

# 累計統計
df['cumsum'] = df['sales'].expanding().sum()
df['cumavg'] = df['sales'].expanding().mean()

# 年度累計
df['ytd'] = df.groupby(df.index.year)['sales'].expanding().sum()
```

---

#### 3️⃣ Day 7: 時間比較與同期分析
**檔案：** `Day07_Time_Comparison_Guide.md`
**耗時：** 6 小時
**內容：**
- Part 1: Shift 時間平移（2h）- 上期、去年同期
- Part 2: pct_change & diff（2h）- 成長率、差異計算
- Part 3: 同期比較實戰（2h）- MoM, YoY, WoW
- 10 個實戰案例（成長率分析、趨勢識別）

**核心概念：**
```python
# 時間平移
df['previous'] = df['sales'].shift(1)
df['last_year'] = df['sales'].shift(365)

# 環比增長
df['mom'] = df['sales'].pct_change() * 100

# 同比增長
df['yoy'] = df['sales'].pct_change(periods=12) * 100

# 絕對變化
df['change'] = df['sales'].diff()

# 複合年增長率 (CAGR)
cagr = (end / start) ** (1 / years) - 1
```

---

#### 4️⃣ Day 8: 實踐整合 - 時間序列分析儀表板
**檔案：** `Day08_Practice_Integration.md`
**耗時：** 5 小時
**內容：**
- 最終專案：完整的時間序列分析系統
- 整合 Day 5-7 所有技能
- 6 大功能：日週月趨勢、MA、YTD、成長率、季節性、異常檢測

**專案功能：**
```python
# 1. 日週月趨勢
daily = df.resample('D').sum()
weekly = df.resample('W').sum()
monthly = df.resample('ME').sum()

# 2. 移動平均線
df['sma_7'] = df['sales'].rolling(7).mean()
df['sma_30'] = df['sales'].rolling(30).mean()

# 3. YTD 累計
df['ytd'] = df['sales'].expanding().sum()

# 4. 成長率
df['growth'] = df['sales'].pct_change() * 100

# 5. 季節性分析
seasonal = df.groupby(df.index.dayofweek).mean()

# 6. 異常檢測
df['is_outlier'] = np.abs(df['sales'] - df['sma_30']) > 2 * df['sma_30'].std()
```

---

### 📝 練習題系統（3 個練習集 + 32 題）

#### Exercise 4: DateTime 10 題
**檔案：** `exercises/Exercise_04_DateTime_10_Questions.md`
**難度分布：** 🟢3題 | 🟡4題 | 🔴3題
**建議時間：** 1.5 小時

**題目類型：**
1. 日期轉換與屬性提取
2. Timedelta 計算
3. 月末識別
4. 日期範圍篩選與工作日
5. Period 時間區間
6. 複雜日期計算
7. 季度分析
8. 工作日和節假日
9. 時間序列完整性驗證
10. 時區和國際日期

---

#### Exercise 5: Resample & Rolling 12 題
**檔案：** `exercises/Exercise_05_Resample_12_Questions.md`
**難度分布：** 🟢4題 | 🟡5題 | 🔴3題
**建議時間：** 2 小時

**題目類型：**
1. 基礎 Resample 升採樣
2. 簡單移動平均線 (SMA)
3. 移動標準差與波動率
4. 7 日銷售累計
5. 多函數聚合
6. 加權移動平均線 (WMA)
7. Expanding 累計分析
8. 年度累計 (YTD)
9. 季度與月度累計
10. Bollinger Bands
11. 多時間窗口組合
12. 時間序列完整性與異常修復

---

#### Exercise 6: 時間比較 10 題
**檔案：** `exercises/Exercise_06_TimeComparison_10_Questions.md`
**難度分布：** 🟢3題 | 🟡4題 | 🔴3題
**建議時間：** 1.5 小時

**題目類型：**
1. Shift 基礎應用
2. 月環比增長率 (MoM)
3. 年度同期比較 (YoY)
4. MoM 成長率計算與分類
5. YoY 年度比較
6. 多期成長率計算
7. 成長趨勢識別
8. WoW、MoM、YoY 多維度比較
9. CAGR 與複合增長率
10. 異常檢測與同期比較

---

#### 完整解答集
**檔案：** `exercises/Solutions_Complete.md`
**內容：**
- 前 5 題：詳細完整解答（各題 8 部分）
- 題 6-32：解答框架（可逐步補充）
- 通用最佳實踐
- 常見錯誤及解決方案

---

### 🎯 快速開始指南
**檔案：** `QUICK_START.md`（5 分鐘快速開始）

---

### 📊 完整索引
**檔案：** `INDEX.md`（32 題完整索引）

---

## 學習路徑

### 初級學習者（首次接觸時間序列）
```
Day 5: DateTime Mastery
  ↓
Exercise 4: DateTime 10 題（簡單 + 部分中等）
  ↓
Day 6: Resample & Rolling
  ↓
Exercise 5: Resample 12 題（簡單）
  ↓
Day 7: 時間比較
  ↓
Exercise 6: 時間比較 10 題（簡單）
  ↓
Day 8: 實踐整合
```

### 中級學習者（有 Pandas 基礎）
```
Day 5 + Day 6 (並行學習)
  ↓
Exercise 4 + Exercise 5 (中等題)
  ↓
Day 7
  ↓
Exercise 6 (全部)
  ↓
Day 8: 實踐整合
```

### 高級學習者（有統計背景）
```
快速掃讀 Day 5-7
  ↓
Exercise 4-6 (困難題 + 自訂擴展)
  ↓
Day 8: 實踐整合 + 進階應用
```

---

## 核心技能矩陣

| 技能 | Day 5 | Day 6 | Day 7 | 相關題目 |
|-----|-------|-------|-------|---------|
| 日期轉換 | ✅ | - | - | Ex4: 1-3 |
| 日期屬性 | ✅ | - | - | Ex4: 1, 3 |
| Timedelta | ✅ | - | - | Ex4: 2, 6 |
| 工作日計算 | ✅ | - | - | Ex4: 4, 8 |
| Period 處理 | ✅ | - | - | Ex4: 5 |
| 升採樣 | - | ✅ | - | Ex5: 1-4 |
| 降採樣 | - | ✅ | - | Ex5: 12 |
| 移動平均線 | - | ✅ | - | Ex5: 2, 6 |
| 移動標準差 | - | ✅ | - | Ex5: 3, 10 |
| 累計統計 | - | ✅ | - | Ex5: 7-9 |
| Shift | - | - | ✅ | Ex6: 1-4 |
| 成長率計算 | - | - | ✅ | Ex6: 2-7 |
| 同期比較 | - | - | ✅ | Ex6: 8-10 |
| 綜合應用 | ✅ | ✅ | ✅ | Day 8 |

---

## Excel vs Pandas 對照

| 操作 | Excel | Pandas |
|-----|-------|--------|
| 轉換日期 | `DATEVALUE()` | `pd.to_datetime()` |
| 提取年份 | `YEAR()` | `dt.year` |
| 計算天數差 | `DATEDIF()` | `(date2-date1).dt.days` |
| 加 N 天 | `A1 + N` | `date + pd.Timedelta(days=N)` |
| 計算工作日 | `WORKDAY()` | `date + N * BDay()` |
| 按月聚合 | 樞紐表 | `resample('ME').sum()` |
| 移動平均 | `AVERAGE(OFFSET())` | `rolling().mean()` |
| 日期範圍篩選 | SUMIFS | 日期比較篩選 |
| 環比增長 | `(B2-B1)/B1` | `pct_change()` |
| 同比增長 | `(B13-B1)/B1` | `pct_change(periods=12)` |

---

## 數據集

本系統使用 **Olist 電商數據集**（模擬）：

```python
# 數據特徵
- 時間範圍：2023 年全年（365 天）
- 訂單記錄：~5000 筆
- 字段：order_id, order_date, delivery_date, sales, category
- 包含週期性和季節性特徵
```

---

## 常見問題 (FAQ)

### Q: 應該按什麼順序學習？
A: 建議按 Day 5 → Day 6 → Day 7 → Day 8 的順序學習。每個 Day 都基於前一個 Day 的概念。

### Q: 練習題難度如何分配？
A:
- 🟢 簡單（40%）：鞏固基本概念
- 🟡 中等（35%）：實際應用
- 🔴 困難（25%）：進階技能和整合

### Q: 有沒有視頻教學？
A: 當前版本是文字教學。建議配合 Jupyter Notebook 逐段執行代碼。

### Q: 如何使用解答集？
A:
1. 先嘗試自己做題
2. 卡住時查看框架
3. 完成後對照詳細解答
4. 理解關鍵概念

### Q: 學完這個系統能做什麼？
A:
- ✅ 進行完整的時間序列分析
- ✅ 識別銷售趨勢和異常
- ✅ 進行同期比較分析
- ✅ 建立業務儀表板
- ✅ 使用進階統計方法

---

## 延伸資源

### 推薦進階主題
1. **時間序列分解** - 分離趨勢、季節性、殘差
2. **自相關分析** - ACF/PACF 圖
3. **預測模型** - ARIMA, Prophet, LSTM
4. **異常檢測** - 統計方法與機器學習
5. **實時計算** - 流式數據處理

### 推薦工具和庫
- `statsmodels` - 時間序列統計
- `Prophet` - Facebook 的時間序列預測庫
- `plotly` - 交互式視覺化
- `scikit-learn` - 機器學習
- `xarray` - 多維時間序列

---

## 學習成果評估

完成本系統後，您應該能夠：

### 知識目標
- [ ] 理解 Timestamp 和 Period 的區別
- [ ] 掌握所有日期時間操作
- [ ] 理解 Resample 和 Rolling 的差異
- [ ] 實現多種同期比較分析

### 技能目標
- [ ] 獨立完成 32 題練習題
- [ ] 實現完整的時間序列分析
- [ ] 識別數據中的異常和趨勢
- [ ] 建立可重複使用的分析模板

### 應用目標
- [ ] 為企業生成月度/季度報告
- [ ] 進行銷售預測分析
- [ ] 識別業務機會和風險
- [ ] 優化業務決策

---

## 貢獻與反饋

如果您有任何建議或發現錯誤，歡迎提出反饋。本系統會根據用戶反饋持續改進。

---

## 許可證

本教學系統為開源教育資源，可自由使用、修改和分享。

---

**最後更新：** 2025-12-11
**版本：** 1.0
**作者：** 數據分析教學團隊

---

## 快速導航

- 📖 [Day 5: DateTime 主要指南](Day05_DateTime_Mastery_Guide.md)
- 📊 [Day 6: Resample & Rolling](Day06_Resample_Rolling_Guide.md)
- 📈 [Day 7: 時間比較](Day07_Time_Comparison_Guide.md)
- 🎯 [Day 8: 實踐整合](Day08_Practice_Integration.md)
- ✍️ [Exercise 4: DateTime 10 題](exercises/Exercise_04_DateTime_10_Questions.md)
- 📋 [Exercise 5: Resample 12 題](exercises/Exercise_05_Resample_12_Questions.md)
- 🔍 [Exercise 6: 時間比較 10 題](exercises/Exercise_06_TimeComparison_10_Questions.md)
- ✅ [完整解答集](exercises/Solutions_Complete.md)
- ⚡ [5 分鐘快速開始](QUICK_START.md)
- 📑 [完整題目索引](INDEX.md)
