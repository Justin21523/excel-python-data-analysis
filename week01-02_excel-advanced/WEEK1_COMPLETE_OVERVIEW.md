# 📘 Week 1 完整學習總覽

## 🎯 Week 1 目標

掌握 Excel 365 的所有進階函數和 Power Query，為 Week 2（Pivot Tables + VBA）和後續的 Python 學習打下堅實基礎。

**總時數：** 24-28 小時
**完成後：** 能獨立處理複雜的資料分析任務，建立自動化報表系統

---

## 📚 學習路線圖

```
Day 1 (3-4h)     Day 2 (3-4h)      Day 3 (3-4h)        Day 4 (4-5h)         Day 5 (3-4h)        Day 6-7 (6-8h)
───────────────────────────────────────────────────────────────────────────────────────────────────────────
   FILTER          SORT             UNIQUE            文字函數              LET                Power Query
  (動態篩選)      SORTBY           SEQUENCE         (提取/清理)          (定義變數)           (ETL神器)
                (動態排序)         XLOOKUP          日期函數            LAMBDA
                                  (強大查找)        (計算/格式化)        (自訂函數)           批次處理
   ↓                ↓                ↓                 ↓                   ↓                   ↓
篩選訂單        排名分析         去重/序列        資料清洗            簡化公式            多檔整合
多條件          Top N           查找客戶         格式化報表          建立函數庫          自動更新
```

---

## 📁 所有學習資源

### 教學文件（完整版，含範例、練習、作業）

| 檔案 | 內容 | 頁數/時數 | 狀態 |
|------|------|---------|------|
| `Day01_FILTER_Function_Guide.md` | FILTER 完全攻略 | 2500+ 字 / 3-4h | ✅ |
| `Day02_SORT_SORTBY_Guide.md` | SORT/SORTBY 完全攻略 | 2500+ 字 / 3-4h | ✅ |
| `Day03_UNIQUE_SEQUENCE_Guide.md` | UNIQUE/SEQUENCE/XLOOKUP | 3000+ 字 / 3-4h | ✅ |
| `Day04_TEXT_DATE_Functions_Guide.md` | 文字 & 日期函數 | 3500+ 字 / 4-5h | ✅ |
| `Day05_LET_LAMBDA_Guide.md` | LET & LAMBDA 函數式編程 | 3000+ 字 / 3-4h | ✅ |
| `Day06-07_Power_Query_Complete_Guide.md` | Power Query 完整教學 | 5000+ 字 / 6-8h | ✅ |

**總計：** 19500+ 字，24-28 小時完整教學

---

### 練習資料（超真實商業資料）

| 檔案 | 內容 | 記錄數 | 欄位數 |
|------|------|--------|--------|
| `case01_realistic_sales_data.xlsx` | **訂單明細** | 1000 筆 | **40 欄** |
| ├─ 訂單明細 | 完整訂單資料 | 1000 | 40 |
| ├─ 產品主檔 | 產品資訊 | 40 | 17 |
| └─ 客戶主檔 | 客戶資訊 | 500 | 12 |
| `case02_realistic_inventory.xlsx` | **庫存資料** | 200 筆 | **30 欄** |
| ├─ 庫存明細 | 庫存狀態 | 200 | 30+ |
| ├─ 類別統計 | 自動彙總 | 8 | 5 |
| └─ 庫存警示 | 警示清單 | 動態 | 30+ |

**資料特色：**
- ✅ 真實品牌：Logitech, Apple, Dyson, Nike...
- ✅ 完整欄位：客戶電話/Email/地址、產品品牌/型號/SKU、促銷折扣、物流單號、發票資訊、評分評論
- ✅ 商業邏輯：20/80 客戶規則、週末購物高峰、時段分佈、評分分佈
- ✅ 台灣在地化：手機格式(09XX)、地址格式、郵遞區號

---

### 練習工作簿

| 檔案 | 內容 |
|------|------|
| `Day01_FILTER_Practice.xlsx` | 8 個 FILTER 練習題（含提示和參考答案） |

---

## 🎓 知識體系

### Day 1: FILTER() - 動態篩選的藝術

**核心概念：**
- 動態陣列 vs 傳統公式
- #SPILL! 錯誤處理

**語法掌握：**
```excel
=FILTER(array, include, [if_empty])
```

**7 個實戰範例：**
1. ✅ 單條件：篩選「已完成」訂單
2. ✅ 數值條件：篩選「總額>5000」
3. ✅ AND 條件：`(條件1)*(條件2)` - 已完成且總額>5000
4. ✅ OR 條件：`(條件1)+(條件2)` - 電腦周邊或手機配件
5. ✅ 日期範圍：篩選「2024年11月」
6. ✅ 組合條件：`((OR1)+(OR2))*(AND)` - 複雜篩選
7. ✅ 文字搜尋：`ISNUMBER(SEARCH(...))` - 地址包含「台北」

**Excel → Python 對照：**
```excel
=FILTER(A:Z, B:B="值")
```
```python
df[df['B'] == '值']
```

**實戰作業：**
- 動態訂單查詢系統（4 條件組合）
- Top N 客戶清單

---

### Day 2: SORT() & SORTBY() - 動態排序

**核心概念：**
- SORT：按本身欄位排序
- SORTBY：按其他欄位排序

**語法掌握：**
```excel
=SORT(array, [sort_index], [sort_order], [by_col])
=SORTBY(array, by_array1, [sort_order1], ...)
```

**7 個實戰範例：**
1. ✅ 單欄排序：按訂單總額升序/降序
2. ✅ 多欄排序：`{14, 28}, {1, -1}` - 先類別後金額
3. ✅ 按日期排序：最新訂單在上
4. ✅ SORTBY：只顯示 3 欄，但按第 4 欄排序
5. ✅ FILTER + SORT：先篩選後排序
6. ✅ SORT + TAKE：Top 10 排名
7. ✅ FILTER + SORT + TAKE：條件 Top N

**Excel → Python 對照：**
```excel
=SORT(A:Z, 3, -1)
```
```python
df.sort_values('欄3', ascending=False)
```

**實戰作業：**
- 動態排行榜系統（可切換排序依據）
- 客戶消費排名分析
- 產品銷售排名

---

### Day 3: UNIQUE, SEQUENCE, XLOOKUP - 萬用工具集

**核心概念：**
- UNIQUE：去除重複
- SEQUENCE：生成序列
- XLOOKUP：取代 VLOOKUP 的強大查找

**語法掌握：**
```excel
=UNIQUE(array, [by_col], [exactly_once])
=SEQUENCE(rows, [columns], [start], [step])
=XLOOKUP(lookup_value, lookup_array, return_array, [if_not_found], [match_mode], [search_mode])
```

**12 個實戰範例：**

**UNIQUE：**
1. ✅ 單欄不重複：所有產品類別
2. ✅ 多欄組合：品牌+類別組合
3. ✅ 只出現一次：一次性客戶
4. ✅ UNIQUE + SORT：排序不重複清單

**SEQUENCE：**
5. ✅ 生成 1-100
6. ✅ 生成偶數序列
7. ✅ 生成日期序列（本月所有日期）
8. ✅ 加上排名序號：HSTACK(SEQUENCE(...), 資料)

**XLOOKUP：**
9. ✅ 基礎查找：查客戶姓名
10. ✅ 預設值：找不到顯示「不存在」
11. ✅ 返回多欄：一次返回 4 個欄位
12. ✅ 反向查找：產品名稱→產品編號
13. ✅ 模糊匹配：分數→等級（區間查找）
14. ✅ 反向搜尋：找最後一筆記錄

**實戰作業：**
- 動態產品查詢系統
- 客戶消費統計表（UNIQUE + XLOOKUP + SUMIFS）
- 產品銷售彙總表

---

### Day 4: 文字 & 日期函數 - 資料清洗核心

**核心概念：**
- 文字提取、分割、組合、清理
- 數字和日期格式化
- 日期計算與工作日處理

**21 個實戰範例：**

**文字提取（LEFT/RIGHT/MID）：**
1. ✅ 提取訂單編號的年月日流水號
2. ✅ 提取 Email 使用者名稱
3. ✅ 提取地址中的城市

**文字搜尋（FIND/SEARCH）：**
4. ✅ 找到 "@" 的位置
5. ✅ 判斷地址是否包含「台北」

**文字替換（SUBSTITUTE/REPLACE）：**
6. ✅ 統一地址格式（台北→臺北）
7. ✅ 移除空格（TRIM）
8. ✅ 遮蔽手機號碼
9. ✅ 移除特殊字元

**TEXT() 格式化：**
10. ✅ 數字格式：`#,##0` `$#,##0` `0.00%`
11. ✅ 日期格式：`yyyy年mm月dd日` `dddd` `yyyy-Q#`
12. ✅ 時間格式：`hh:mm:ss` `hh:mm AM/PM`
13. ✅ 條件格式化：正數/負數/零顯示不同文字

**日期函數：**
14. ✅ DATE/TODAY/NOW：建立日期
15. ✅ YEAR/MONTH/DAY/WEEKDAY：提取元件
16. ✅ EOMONTH：月初/月底日期
17. ✅ DATEDIF：計算年齡、天數差
18. ✅ DATEDIF：計算會員資格
19. ✅ NETWORKDAYS：計算工作日數
20. ✅ WORKDAY：加上 N 個工作日
21. ✅ 判斷訂單是「本月/上月/其他」

**實戰作業：**
- 資料清洗報告（電話標準化、地址分割、Email 驗證）
- 訂單時效分析（年月、星期、時段、距今天數）
- 格式化專業報表

---

### Day 5: LET() & LAMBDA() - 函數式編程

**核心概念：**
- LET：定義變數，簡化複雜公式
- LAMBDA：建立自訂函數
- MAP/REDUCE/SCAN：高階函數

**15 個實戰範例：**

**LET()：**
1. ✅ 簡化重複計算：折扣價計算
2. ✅ 多步驟計算：會員等級判斷
3. ✅ 簡化 FILTER + SORT 組合
4. ✅ 動態查詢系統（完整範例）
5. ✅ 資料清洗流程（電話號碼標準化）

**LAMBDA()：**
6. ✅ 建立折扣價函數
7. ✅ BMI 計算器
8. ✅ 文字清理函數
9. ✅ 日期格式化函數

**MAP()：**
10. ✅ 計算陣列平方
11. ✅ 兩陣列相加
12. ✅ 格式化價格陣列

**REDUCE()：**
13. ✅ 計算階乘
14. ✅ 累計總和

**SCAN()：**
15. ✅ Running Total（顯示每步累積）

**實戰作業：**
- 建立訂單分析函數庫（4 個自訂函數）
- 動態 RFM 分析（使用 LET 整合）
- 可重複使用的資料清理函數庫

---

### Day 6-7: Power Query - ETL 神器

**核心概念：**
- ETL：Extract-Transform-Load
- 非破壞性轉換
- 可重複執行
- 步驟式記錄

**Power Query 介面：**
```
查詢清單 | 資料預覽 | 查詢設定（套用的步驟）
```

**基礎操作（10 種）：**
1. ✅ 載入檔案（Excel/CSV）
2. ✅ 從資料夾批次載入
3. ✅ 移除欄位
4. ✅ 篩選列
5. ✅ 排序
6. ✅ 重新命名欄位
7. ✅ 變更資料類型
8. ✅ 文字清理（修剪、取代）
9. ✅ 新增計算欄位（M 語言）
10. ✅ 移除重複列

**進階轉換（5 種核心技術）：**

**1. Unpivot（寬→長）**
```
Before: 產品 | 1月 | 2月 | 3月
After:  產品 | 月份 | 銷售額
```
- Python 等效：`df.melt()`

**2. Pivot（長→寬）**
```
Before: 日期 | 產品 | 數量
After:  日期 | 產品A | 產品B
```
- Python 等效：`df.pivot()`

**3. Group By（分組彙總）**
```
按「產品類別」分組
計算：總銷售額、訂單數、平均單價
```
- Python 等效：`df.groupby().agg()`

**4. Merge（水平合併）**
```
Join 類型：
- Left Outer（保留左表所有）
- Inner（只保留匹配）
- Full Outer（保留所有）
- Left/Right Anti（找差異）
```
- Python 等效：`pd.merge()`

**5. Append（垂直合併）**
```
1月資料
2月資料  → 合併成一張完整表
3月資料
```
- Python 等效：`pd.concat()`

**4 個實戰專案：**
1. ✅ 多檔案銷售資料整合（3 分店）
2. ✅ 髒資料清理流程（8 步驟）
3. ✅ 訂單+產品+客戶整合（2 次 Merge）
4. ✅ 每日自動更新報表

**M 語言基礎：**
```m
// 文字
Text.Length([欄位])
Text.Replace([欄位], "舊", "新")

// 日期
Date.Year([日期])
Date.AddDays([日期], 7)

// 邏輯
if [金額] > 5000 then "高" else "低"
```

---

## 🎯 學習檢核清單

### Day 1-2: 動態陣列函數
- [ ] 理解動態陣列的溢出概念
- [ ] 掌握 FILTER 的 3 種條件組合（單一、AND、OR）
- [ ] 能處理 #SPILL! 錯誤
- [ ] 掌握 SORT 的單欄和多欄排序
- [ ] 理解 SORT 和 SORTBY 的差異
- [ ] 能組合 FILTER + SORT + TAKE 建立 Top N

### Day 3: 萬用工具集
- [ ] 使用 UNIQUE 建立動態下拉選單
- [ ] 使用 SEQUENCE 生成數字和日期序列
- [ ] 掌握 XLOOKUP 的 5 種用法
- [ ] 能用 XLOOKUP 取代所有 VLOOKUP
- [ ] 理解模糊匹配（match_mode=1）

### Day 4: 資料清洗
- [ ] 使用 LEFT/MID/RIGHT 提取文字
- [ ] 使用 SUBSTITUTE 批次替換文字
- [ ] 使用 TEXT 格式化數字和日期（至少 5 種格式）
- [ ] 使用 DATEDIF 計算日期差異
- [ ] 使用 WORKDAY/NETWORKDAYS 處理工作日

### Day 5: 函數式編程
- [ ] 使用 LET 簡化至少一個複雜公式
- [ ] 建立至少 2 個 LAMBDA 自訂函數
- [ ] 理解 MAP 的運作原理
- [ ] 知道 REDUCE 和 SCAN 的差異

### Day 6-7: Power Query
- [ ] 能從資料夾批次載入多個檔案
- [ ] 掌握 Unpivot 轉換（寬→長）
- [ ] 掌握 Pivot 轉換（長→寬）
- [ ] 掌握 Group By 彙總
- [ ] 掌握 Merge（至少 2 種 Join 類型）
- [ ] 掌握 Append 垂直合併
- [ ] 能建立可重複執行的 ETL 流程
- [ ] 寫過至少 3 個 M 語言自訂欄位公式

---

## 📊 Excel → Python 完整對照表

### 篩選與排序
| Excel | Python pandas |
|-------|---------------|
| `=FILTER(A:Z, B:B="值")` | `df[df['B'] == '值']` |
| `=FILTER(..., (條件1)*(條件2))` | `df[(條件1) & (條件2)]` |
| `=FILTER(..., (條件1)+(條件2))` | `df[(條件1) | (條件2)]` |
| `=SORT(A:Z, 3, -1)` | `df.sort_values('欄3', ascending=False)` |
| `=SORT(A:Z, {3,5}, {1,-1})` | `df.sort_values(['欄3','欄5'], ascending=[True,False])` |
| `=TAKE(SORT(...), 10)` | `df.sort_values(...).head(10)` |

### 去重與序列
| Excel | Python |
|-------|--------|
| `=UNIQUE(A:A)` | `df['A'].unique()` 或 `df['A'].drop_duplicates()` |
| `=SEQUENCE(100)` | `range(1, 101)` 或 `np.arange(1, 101)` |
| `=SEQUENCE(30, 1, DATE(2024,11,1), 1)` | `pd.date_range('2024-11-01', periods=30)` |

### 查找與合併
| Excel | Python |
|-------|--------|
| `=XLOOKUP(val, A:A, B:B)` | `df.set_index('A').loc[val, 'B']` 或 `df.merge()` |
| `=VLOOKUP(...)` | `df.merge(how='left')` |

### 文字處理
| Excel | Python |
|-------|--------|
| `=LEFT(A2, 3)` | `df['A'].str[:3]` |
| `=MID(A2, 4, 4)` | `df['A'].str[3:7]` |
| `=SUBSTITUTE(A2, "X", "Y")` | `df['A'].str.replace('X', 'Y')` |
| `=TRIM(A2)` | `df['A'].str.strip()` |
| `=TEXT(A2, "#,##0")` | `df['A'].apply(lambda x: f'{x:,}')` |

### 日期計算
| Excel | Python |
|-------|--------|
| `=YEAR(A2)` | `df['A'].dt.year` |
| `=DATEDIF(A2, TODAY(), "Y")` | `(pd.Timestamp.now() - df['A']).dt.days // 365` |
| `=EOMONTH(TODAY(), 0)` | `pd.Period.now('M').end_time.date()` |

### Power Query 轉換
| Power Query | Python pandas |
|-------------|---------------|
| Unpivot | `df.melt()` |
| Pivot | `df.pivot()` 或 `df.pivot_table()` |
| Group By | `df.groupby().agg()` |
| Merge (Left) | `pd.merge(how='left')` |
| Append | `pd.concat()` |
| 移除重複 | `df.drop_duplicates()` |

### 函數式編程
| Excel | Python |
|-------|--------|
| `=LET(x, 10, x*2)` | `x = 10; x * 2` |
| `=LAMBDA(x, x*2)` | `lambda x: x*2` |
| `=MAP(A:A, LAMBDA(x, x*2))` | `df['A'].apply(lambda x: x*2)` |
| `=REDUCE(0, A:A, LAMBDA(a,b, a+b))` | `df['A'].sum()` |

---

## 🚀 學習建議

### 第一次學習（Follow 教學）
1. ✅ 按照 Day 1 → Day 7 順序
2. ✅ 每個範例都親自輸入一次
3. ✅ 做完所有練習題
4. ✅ 完成實戰作業
5. ✅ 做筆記，記錄重點和卡點

### 第二次複習（測試記憶）
1. ✅ 不看教學，直接做練習題
2. ✅ 嘗試創造自己的變化
3. ✅ 對照 Python 語法，建立心智模型
4. ✅ 挑戰綜合專案

### 第三次精通（實際應用）
1. ✅ 用自己的真實資料練習
2. ✅ 建立自己的函數庫和範本
3. ✅ 優化效能和使用者體驗
4. ✅ 教別人（最好的學習方式）

---

## 💡 常見問題 FAQ

### Q1: 我沒有 Excel 365，可以學習嗎？
**A:** 動態陣列函數（FILTER、SORT、UNIQUE、SEQUENCE、XLOOKUP、LET、LAMBDA）只支援 Excel 365 和 Excel 2021。

**替代方案：**
- 使用 **Google Sheets**（支援部分動態陣列函數）
- 直接跳到 **Power Query**（Excel 2016+ 都支援）
- 訂閱 **Microsoft 365**（最推薦）

### Q2: 學完 Week 1 後，我能做什麼？
**A:** 你將能夠：
- ✅ 建立複雜的動態查詢系統
- ✅ 自動化資料清洗流程
- ✅ 批次處理多個檔案
- ✅ 建立自動更新的報表
- ✅ 整合多個資料來源

### Q3: Excel 和 Python 我應該選哪個？
**A:** 兩個都學！
- **Excel**：快速原型、與非技術人員協作、小資料量
- **Python**：大資料量、複雜邏輯、自動化排程、機器學習

Week 1 的 Excel 訓練會讓你的 **Python pandas 學習速度提升 3-5 倍**，因為概念是相通的。

### Q4: Power Query 和 Excel 公式哪個好？
**A:** 看情境：
- **Excel 公式**：即時計算、公式可見、適合小資料
- **Power Query**：批次處理、可重複執行、大資料優化、不修改原資料

**最佳實踐：** Power Query 做 ETL，Excel 公式做計算，Pivot Table 做報表。

### Q5: 我需要記住所有函數嗎？
**A:** 不需要！重點是：
1. ✅ 理解概念和應用情境
2. ✅ 知道什麼時候用哪個函數
3. ✅ 能快速查閱語法（教學文件就是你的速查表）
4. ✅ 多練習，建立肌肉記憶

---

## 📈 學習進度追蹤

### Week 1 進度表

| Day | 主題 | 預估時數 | 實際時數 | 完成日期 | 筆記 |
|-----|------|---------|---------|---------|------|
| Day 1 | FILTER | 3-4h | | | |
| Day 2 | SORT/SORTBY | 3-4h | | | |
| Day 3 | UNIQUE/SEQUENCE/XLOOKUP | 3-4h | | | |
| Day 4 | 文字 & 日期函數 | 4-5h | | | |
| Day 5 | LET & LAMBDA | 3-4h | | | |
| Day 6 | Power Query 基礎 | 3-4h | | | |
| Day 7 | Power Query 實戰 | 3-4h | | | |
| **總計** | | **24-28h** | | | |

---

## 🎊 完成 Week 1 後的下一步

### Week 2 預告（Pivot Tables + VBA）

**Day 8-9: Pivot Tables 完全攻略**
- 樞紐分析四大區域
- 計算欄位
- Show Values As（% 顯示）
- 切片篩選器 + 時間軸
- 樞紐圖表

**Day 10-12: VBA Macros & 自動化**
- VBA 基礎語法
- 巨集錄製
- 5 個實戰範例（資料清洗、批次匯入、自動報表、Email 發送、進度條）

**Day 13-14: 綜合專案**
- 企業級銷售分析系統
- 整合 Power Query + Excel 函數 + Pivot Tables + VBA
- 一鍵自動化

---

## 📚 延伸學習資源

### 官方文件
- [Excel 函數參考](https://support.microsoft.com/zh-tw/office/excel-functions-by-category)
- [Power Query 文件](https://learn.microsoft.com/zh-tw/power-query/)
- [M 語言參考](https://learn.microsoft.com/zh-tw/powerquery-m/)

### YouTube 頻道
- **Leila Gharani**：Excel 進階技巧與 Power Query
- **MyOnlineTrainingHub**：Power Query 完整教學
- **ExcelIsFun**：Excel 綜合教學（2000+ 影片）
- **Chandoo**：商業分析實戰

### 線上課程
- **Coursera**: Excel Skills for Business（專項課程）
- **Udemy**: Excel - Excel從入門到專業
- **LinkedIn Learning**: Excel: Power Query、Excel: Advanced Formulas

### 書籍推薦
- 《Excel VBA 程式設計實戰寶典》
- 《Power Query 資料整理實戰》
- 《Excel 樞紐分析完全攻略》

---

## ✨ 總結

**Week 1 是整個 18-20 週課程的基石。**

投入 24-28 小時，你將獲得：
- ✅ 50+ 個實用函數的完整掌握
- ✅ Power Query 自動化 ETL 能力
- ✅ Excel → Python 的思維轉換能力
- ✅ 可直接應用於工作的技能

**記住：**
> 不要求完美，但要求完成。
> 不要死記硬背，但要理解概念。
> 不要孤軍奮戰，多問問題。

**現在，打開 `Day01_FILTER_Function_Guide.md`，開始你的學習之旅吧！** 🚀

---

**💪 You Got This!**
