# Week 1-2: Excel 進階技巧完整教學

## 📚 學習目標

**為什麼要學 Excel 進階？**
- 理解商業分析的**思維邏輯**
- 掌握 Excel → Python 的**對應關係**
- 快速處理中小型資料（< 100 萬筆）
- 建立互動式儀表板

**時間投入：** 20-24 小時（2 週）

---

## Week 1: 動態陣列 + 進階公式 (12 小時)

### 📖 核心函數清單

#### 1. 動態陣列函數 (Excel 365)

| 函數 | 用途 | Python 對應 |
|------|------|-------------|
| `FILTER()` | 條件篩選 | `df[df['col'] > value]` |
| `SORT()` | 排序 | `df.sort_values()` |
| `SORTBY()` | 依其他欄位排序 | `df.sort_values(by='col')` |
| `UNIQUE()` | 去重 | `df['col'].unique()` |
| `SEQUENCE()` | 生成序列 | `range()`, `np.arange()` |
| `RANDARRAY()` | 隨機陣列 | `np.random.rand()` |

#### 2. 查詢函數

| 函數 | 用途 | Python 對應 |
|------|------|-------------|
| `XLOOKUP()` | 新版查詢（取代VLOOKUP） | `df.merge()` |
| `VLOOKUP()` | 垂直查詢 | `df.merge()` |
| `HLOOKUP()` | 水平查詢 | `df.merge()` |
| `INDEX(MATCH())` | 雙向查詢 | `df.loc[]` |
| `XMATCH()` | 新版位置查詢 | `df.index.get_loc()` |

#### 3. 條件與邏輯

| 函數 | 用途 | Python 對應 |
|------|------|-------------|
| `IF()` | 條件判斷 | `np.where()` |
| `IFS()` | 多條件判斷 | `np.select()` |
| `SWITCH()` | 多重分支 | `pd.cut()`, `map()` |
| `SUMIF()`, `SUMIFS()` | 條件加總 | `df.groupby().sum()` |
| `COUNTIF()`, `COUNTIFS()` | 條件計數 | `df.groupby().count()` |
| `AVERAGEIF()` | 條件平均 | `df.groupby().mean()` |

#### 4. 文字處理

| 函數 | 用途 | Python 對應 |
|------|------|-------------|
| `LEFT()`, `RIGHT()`, `MID()` | 擷取文字 | `str.slice()` |
| `LEN()` | 文字長度 | `str.len()` |
| `FIND()`, `SEARCH()` | 搜尋文字 | `str.find()` |
| `SUBSTITUTE()`, `REPLACE()` | 取代文字 | `str.replace()` |
| `TEXT()` | 格式化文字 | `str.format()` |
| `TEXTJOIN()` | 合併文字 | `str.join()` |
| `TEXTSPLIT()` | 分割文字 | `str.split()` |

#### 5. 日期時間

| 函數 | 用途 | Python 對應 |
|------|------|-------------|
| `DATE()`, `TIME()` | 建立日期時間 | `pd.Timestamp()` |
| `YEAR()`, `MONTH()`, `DAY()` | 擷取年月日 | `dt.year`, `dt.month` |
| `WEEKDAY()` | 星期幾 | `dt.dayofweek` |
| `EOMONTH()` | 月底日期 | `dt.month_end` |
| `DATEDIF()` | 日期差 | `(date2 - date1).days` |
| `NETWORKDAYS()` | 工作日 | `pd.bdate_range()` |

#### 6. 統計函數

| 函數 | 用途 | Python 對應 |
|------|------|-------------|
| `SUM()`, `AVERAGE()` | 加總、平均 | `sum()`, `mean()` |
| `MIN()`, `MAX()` | 最小、最大 | `min()`, `max()` |
| `MEDIAN()`, `MODE()` | 中位數、眾數 | `median()`, `mode()` |
| `STDEV()`, `VAR()` | 標準差、變異數 | `std()`, `var()` |
| `PERCENTILE()` | 百分位數 | `quantile()` |
| `RANK()` | 排名 | `rank()` |

#### 7. 進階函數

| 函數 | 用途 | Python 對應 |
|------|------|-------------|
| `LET()` | 定義變數 | 變數賦值 |
| `LAMBDA()` | 自訂函數 | `lambda` |
| `MAP()` | 對陣列應用函數 | `apply()` |
| `REDUCE()` | 累加運算 | `reduce()` |
| `SCAN()` | 累進運算 | `cumsum()` |

---

## Week 2: Power Query + 樞紐進階 (12 小時)

### 📖 Power Query 核心操作

#### 1. 資料來源
- 從檔案匯入（Excel, CSV, TXT）
- 從資料夾匯入（批次處理）
- 從網頁匯入
- 從資料庫匯入

#### 2. 資料轉換

| 操作 | 用途 | Python 對應 |
|------|------|-------------|
| 移除欄位 | 刪除不需要的欄位 | `df.drop()` |
| 篩選列 | 條件篩選 | `df[df['col'] > 0]` |
| 排序 | 資料排序 | `df.sort_values()` |
| 去除重複 | 去重 | `df.drop_duplicates()` |
| 分割欄位 | 文字分割 | `str.split()` |
| 合併欄位 | 文字合併 | `str.cat()` |
| 取代值 | 值取代 | `replace()` |
| 填補空值 | 填補 null | `fillna()` |

#### 3. 資料整形

| 操作 | 用途 | Python 對應 |
|------|------|-------------|
| **Unpivot** (取消樞紐) | 寬表→長表 | `melt()` |
| **Pivot** (樞紐) | 長表→寬表 | `pivot()` |
| **Transpose** (轉置) | 行列互換 | `transpose()` |
| **Group By** (分組) | 分組聚合 | `groupby()` |

#### 4. 資料合併

| 操作 | 用途 | Python 對應 |
|------|------|-------------|
| **Merge** (合併查詢) | 橫向合併 | `merge()` |
| **Append** (附加查詢) | 縱向合併 | `concat()` |
| Left Join | 左連接 | `merge(how='left')` |
| Inner Join | 內連接 | `merge(how='inner')` |
| Full Outer Join | 完全外連接 | `merge(how='outer')` |

---

## 📁 案例練習檔案

### Case 01: 動態銷售報表
**檔案：** `case01_dynamic_sales_report.xlsx`

**情境：** 電商每日銷售資料，需要建立自動更新的報表

**練習內容：**
1. 使用 `FILTER()` 篩選本月訂單
2. 使用 `SORT()` + `SORTBY()` 排序銷售額
3. 使用 `UNIQUE()` 抓取所有產品類別
4. 使用 `XLOOKUP()` 查詢產品資訊
5. 使用 `SUMIFS()` 計算各類別銷售額
6. 使用 `LET()` 簡化複雜公式

**Excel → Python 對照：**
```excel
# Excel
=FILTER(訂單表, (訂單表[日期]>=本月初) * (訂單表[日期]<=本月底))
```

```python
# Python
df[(df['日期'] >= month_start) & (df['日期'] <= month_end)]
```

---

### Case 02: 庫存儀表板
**檔案：** `case02_inventory_dashboard.xlsx`

**情境：** 多倉庫庫存管理，需要即時監控庫存水位

**練習內容：**
1. 使用條件格式化（資料條、色階）
2. 使用 `IF()` + `IFS()` 設定庫存警示等級
3. 使用 `COUNTIFS()` 統計各等級商品數
4. 使用切片篩選器建立互動介面
5. 建立樞紐圖表
6. 使用 `SPARKLINE()` 微型圖表（Google Sheets）

---

### Case 03: Power Query 多檔案整合
**資料夾：** `power_query_examples/`

**情境：** 每月有多個分店的銷售 CSV 檔案，需要自動整合

**練習內容：**
1. 從資料夾批次匯入所有 CSV
2. 移除不需要的欄位
3. 篩選有效訂單（排除已取消）
4. 新增「年月」欄位
5. Unpivot 產品銷售欄位
6. Group By 計算各產品月銷售
7. 合併產品主檔（Merge）

**Power Query → Python 對照：**

```powerquery
// Power Query
= Table.Group(Source, {"產品"}, {{"銷售額", each List.Sum([金額]), type number}})
```

```python
# Python
df.groupby('產品')['金額'].sum()
```

---

### Case 04: 複雜樞紐分析
**檔案：** `case04_advanced_pivot.xlsx`

**情境：** 電商訂單資料，需要多維度交叉分析

**練習內容：**
1. 建立基礎樞紐表
2. 新增計算欄位（平均客單價、成長率）
3. 使用群組功能（日期群組、自訂群組）
4. 建立時間軸篩選器
5. 建立多個切片篩選器
6. 建立樞紐圖表（組合圖）
7. 格式化為專業報表

---

## 🎯 實戰作業

### 作業 1: 客戶 RFM 分析（Excel 版）

**目標：** 使用 Excel 計算客戶的 RFM 分數

**資料：** 訂單明細表（客戶ID、訂單日期、訂單金額）

**步驟：**
1. 計算 Recency（最近一次購買距今天數）
   - 使用 `DATEDIF()` 或 `TODAY() - MAX(日期)`

2. 計算 Frequency（購買頻率）
   - 使用 `COUNTIF()` 計算每位客戶的訂單數

3. 計算 Monetary（總消費金額）
   - 使用 `SUMIF()` 計算每位客戶的總金額

4. 五等分評分（1-5分）
   - 使用 `PERCENTILE()` 找出分界點
   - 使用 `IFS()` 分配分數

5. 客戶分群
   - 使用 `SWITCH()` 或 `IFS()` 根據 RFM 組合分類

**Excel 公式範例：**

```excel
// Recency 分數
=IFS(
  [Recency] <= PERCENTILE($R$2:$R$1000, 0.2), 5,
  [Recency] <= PERCENTILE($R$2:$R$1000, 0.4), 4,
  [Recency] <= PERCENTILE($R$2:$R$1000, 0.6), 3,
  [Recency] <= PERCENTILE($R$2:$R$1000, 0.8), 2,
  TRUE, 1
)
```

---

### 作業 2: 互動式銷售儀表板

**目標：** 建立一個完整的互動式儀表板

**需求：**
1. **首頁 KPI 卡**
   - 本月總營收
   - 訂單數
   - 平均客單價
   - vs 上月成長率

2. **趨勢圖**
   - 每日營收折線圖
   - 累計營收面積圖

3. **類別分析**
   - Top 10 產品橫條圖
   - 類別銷售圓餅圖

4. **互動篩選**
   - 時間軸（選擇日期範圍）
   - 切片篩選器（產品類別、地區、銷售人員）

5. **格式化**
   - 專業配色
   - 清晰的標題與標籤
   - 適當的間距與對齊

---

## 💡 學習建議

### 第 1 週重點

1. **每天練習 2-3 小時**
   - 上午：學習新函數（1 小時）
   - 下午：實作案例（1.5-2 小時）

2. **建立函數速查表**
   - 記錄常用函數的語法
   - 寫下 Excel → Python 的對應關係

3. **做筆記**
   - 遇到的問題與解決方法
   - 特別技巧與小撇步

### 第 2 週重點

1. **Power Query 思維**
   - 「步驟」概念（每個操作都是一個步驟）
   - 可重複執行（自動化）
   - 不修改原始資料

2. **樞紐表技巧**
   - 不要怕嘗試，隨時可以調整
   - 善用「顯示值方式」（百分比、累計）
   - 計算欄位非常強大

3. **完成一個完整專案**
   - 從髒資料 → 清洗 → 分析 → 視覺化
   - 體驗完整流程

---

## 📚 學習資源

### Excel 官方文件
- [Excel 函數參考](https://support.microsoft.com/zh-tw/office/excel-函數-依類別列出-5f91f4e9-7b42-46d2-9bd1-63f26a86c0eb)
- [Power Query 文件](https://support.microsoft.com/zh-tw/office/power-query-說明-ed614c81-4b00-4291-bd3a-55d80767f81d)
- [樞紐分析表教學](https://support.microsoft.com/zh-tw/office/建立樞紐分析表以分析工作表資料-a9a84538-bfe9-40a9-a8e9-f99134456576)

### YouTube 頻道推薦
- Leila Gharani - Excel 進階技巧
- MyOnlineTrainingHub - Power Query
- ExcelIsFun - 各種 Excel 技巧

### 練習網站
- [Excel Exercises](https://www.excel-exercises.com/)
- [Chandoo.org](https://chandoo.org/) - Excel 儀表板

---

## ✅ 完成檢核表

### Week 1: 動態陣列 + 進階公式
- [ ] 熟悉 FILTER、SORT、UNIQUE、SEQUENCE
- [ ] 掌握 XLOOKUP 取代 VLOOKUP
- [ ] 理解 LET 變數定義
- [ ] 練習 LAMBDA 自訂函數
- [ ] 完成 Case 01: 動態銷售報表
- [ ] 完成 Case 02: 庫存儀表板

### Week 2: Power Query + 樞紐
- [ ] 從資料夾批次匯入檔案
- [ ] 熟悉 Unpivot 與 Pivot
- [ ] 掌握 Merge（各種 Join）
- [ ] 理解 Group By 聚合
- [ ] 建立進階樞紐分析表
- [ ] 使用切片篩選器與時間軸
- [ ] 完成 Case 03: 多檔案整合
- [ ] 完成 Case 04: 複雜樞紐分析

### 實戰作業
- [ ] 完成作業 1: 客戶 RFM 分析（Excel 版）
- [ ] 完成作業 2: 互動式銷售儀表板

---

## 🎯 下一步

完成 Week 1-2 後，你將：
- ✅ 理解資料分析的完整流程
- ✅ 掌握 Excel → Python 的思維轉換
- ✅ 能夠快速處理中小型資料
- ✅ 準備好進入 Week 3-6 的 pandas 進階實戰

**準備好了嗎？讓我們開始 Week 1 的第一個案例！** 🚀
