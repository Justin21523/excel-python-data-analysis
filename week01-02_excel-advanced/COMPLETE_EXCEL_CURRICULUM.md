# Week 1-2: Excel 進階完整課程 - 終極詳細版

## 📚 課程總覽

**總時長：** 40-48 小時（2 週密集學習）
**目標：** 從函數到巨集，完整掌握 Excel 進階技能
**前置需求：** 基本 Excel 操作（輸入資料、簡單公式、格式設定）

---

# 🎯 Week 1: 進階函數 + 動態陣列 + Power Query（24 小時）

## Day 1-2: 動態陣列函數完全攻略（8 小時）

### 📖 理論基礎（1 小時）

#### 什麼是動態陣列？
- **傳統公式：** 一個公式 = 一個結果
- **動態陣列：** 一個公式 = 多個結果（自動溢出）
- **溢出範圍：** 結果自動填滿相鄰儲存格
- **#SPILL! 錯誤：** 溢出範圍被佔用時的錯誤

#### Excel 365 獨有的動態陣列函數
```
FILTER()    - 條件篩選，返回符合條件的所有列
SORT()      - 排序資料
SORTBY()    - 依其他欄位排序
UNIQUE()    - 去除重複值
SEQUENCE()  - 生成數字序列
RANDARRAY() - 生成隨機陣列
XLOOKUP()   - 新版查詢（取代 VLOOKUP）
XMATCH()    - 新版配對（取代 MATCH）
```

---

### 1️⃣ FILTER() - 條件篩選（1.5 小時）

#### 基礎語法
```excel
=FILTER(array, include, [if_empty])
```

#### 範例 1：單條件篩選
```excel
// 篩選銷售額 > 5000 的訂單
=FILTER(A2:E100, E2:E100>5000)
```

#### 範例 2：多條件篩選（AND 邏輯）
```excel
// 篩選類別='電子產品' 且 金額>5000
=FILTER(A2:E100, (C2:C100="電子產品")*(E2:E100>5000))
```

#### 範例 3：多條件篩選（OR 邏輯）
```excel
// 篩選類別='電子產品' 或 '家電'
=FILTER(A2:E100, (C2:C100="電子產品")+(C2:C100="家電"))
```

#### 範例 4：日期範圍篩選
```excel
// 篩選本月訂單
=FILTER(A2:E100, (B2:B100>=DATE(2024,11,1))*(B2:B100<=DATE(2024,11,30)))
```

#### 範例 5：使用 if_empty 參數
```excel
// 沒有結果時顯示訊息
=FILTER(A2:E100, E2:E100>10000, "查無符合條件的資料")
```

#### 進階應用：FILTER 巢狀
```excel
// 先篩選類別，再篩選金額，最後排序
=SORT(FILTER(FILTER(A2:E100, C2:C100="電子產品"), E2:E100>5000), 5, -1)
```

#### Python 對照
```python
# 單條件
df[df['金額'] > 5000]

# 多條件 AND
df[(df['類別'] == '電子產品') & (df['金額'] > 5000)]

# 多條件 OR
df[(df['類別'] == '電子產品') | (df['類別'] == '家電')]

# 日期範圍
df[(df['日期'] >= '2024-11-01') & (df['日期'] <= '2024-11-30')]
```

#### 練習作業（30 分鐘）
1. 篩選「北部地區」的「已完成」訂單
2. 篩選「本季」的訂單（使用 DATE 函數）
3. 篩選金額在「5000-10000」之間的訂單
4. 篩選「客戶名稱包含'王'」的訂單（使用 SEARCH）

---

### 2️⃣ SORT() & SORTBY() - 排序（1 小時）

#### SORT() 語法
```excel
=SORT(array, [sort_index], [sort_order], [by_col])
```

#### 範例 1：單欄位排序
```excel
// 按金額降序
=SORT(A2:E100, 5, -1)
```

#### 範例 2：多欄位排序
```excel
// 先按類別升序，再按金額降序
=SORT(A2:E100, {3,5}, {1,-1})
```

#### SORTBY() 語法
```excel
=SORTBY(array, by_array1, [sort_order1], [by_array2], [sort_order2], ...)
```

#### 範例 3：依其他欄位排序
```excel
// 依照「客戶總消費」排序訂單
=SORTBY(A2:E100, F2:F100, -1)
```

#### 範例 4：組合 FILTER + SORT
```excel
// 篩選後排序
=SORT(FILTER(A2:E100, C2:C100="電子產品"), 5, -1)
```

#### Python 對照
```python
# 單欄位排序
df.sort_values('金額', ascending=False)

# 多欄位排序
df.sort_values(['類別', '金額'], ascending=[True, False])
```

---

### 3️⃣ UNIQUE() - 去除重複（1 小時）

#### 語法
```excel
=UNIQUE(array, [by_col], [exactly_once])
```

#### 範例 1：取得唯一值清單
```excel
// 取得所有產品類別
=UNIQUE(C2:C100)
```

#### 範例 2：多欄位組合去重
```excel
// 取得唯一的「類別-產品」組合
=UNIQUE(C2:D100)
```

#### 範例 3：只取出現一次的值
```excel
// 找出只購買一次的客戶
=UNIQUE(A2:A100, FALSE, TRUE)
```

#### 範例 4：組合 SORT + UNIQUE
```excel
// 取得排序後的唯一類別清單
=SORT(UNIQUE(C2:C100))
```

#### Python 對照
```python
# 唯一值
df['類別'].unique()

# 去重後的 DataFrame
df.drop_duplicates(subset=['類別', '產品'])

# 只出現一次的值
df[df.groupby('客戶')['客戶'].transform('count') == 1]
```

---

### 4️⃣ SEQUENCE() & RANDARRAY() - 生成陣列（1 小時）

#### SEQUENCE() 語法
```excel
=SEQUENCE(rows, [columns], [start], [step])
```

#### 範例 1：生成數字序列
```excel
// 生成 1-100
=SEQUENCE(100)

// 生成偶數 2,4,6,...,100
=SEQUENCE(50, 1, 2, 2)
```

#### 範例 2：生成日期序列
```excel
// 生成本月所有日期
=SEQUENCE(30, 1, DATE(2024,11,1), 1)
```

#### 範例 3：生成二維陣列
```excel
// 生成 10x10 的數字陣列
=SEQUENCE(10, 10)
```

#### RANDARRAY() 語法
```excel
=RANDARRAY([rows], [columns], [min], [max], [whole_number])
```

#### 範例 4：生成隨機測試資料
```excel
// 生成 100 個隨機金額（1000-10000）
=RANDARRAY(100, 1, 1000, 10000, TRUE)
```

#### Python 對照
```python
# SEQUENCE
np.arange(1, 101)  # 1-100
pd.date_range('2024-11-01', periods=30)  # 日期序列

# RANDARRAY
np.random.randint(1000, 10000, size=100)
```

---

### 5️⃣ XLOOKUP() - 新版查詢（1.5 小時）

#### 語法
```excel
=XLOOKUP(lookup_value, lookup_array, return_array, [if_not_found], [match_mode], [search_mode])
```

#### 範例 1：基本查詢
```excel
// 根據產品名稱查詢價格
=XLOOKUP(A2, 產品表!$A$2:$A$100, 產品表!$C$2:$C$100)
```

#### 範例 2：設定預設值
```excel
// 找不到時返回「查無此產品」
=XLOOKUP(A2, 產品表!$A$2:$A$100, 產品表!$C$2:$C$100, "查無此產品")
```

#### 範例 3：近似配對
```excel
// 根據分數查詢等級（60分以下=不及格，60-70=及格...）
=XLOOKUP(A2, {0,60,70,80,90}, {"不及格","及格","中等","良好","優秀"}, , 1)
```

#### 範例 4：返回多欄位
```excel
// 返回產品的「價格」和「庫存」
=XLOOKUP(A2, 產品表!$A$2:$A$100, 產品表!$C$2:$E$100)
```

#### 範例 5：反向搜尋
```excel
// 從後往前找（找最新的記錄）
=XLOOKUP(A2, 訂單表!$A$2:$A$100, 訂單表!$E$2:$E$100, , , -1)
```

#### 與 VLOOKUP 比較
```excel
// VLOOKUP（舊方法）
=VLOOKUP(A2, 產品表!$A$2:$E$100, 3, FALSE)

// XLOOKUP（新方法）
=XLOOKUP(A2, 產品表!$A$2:$A$100, 產品表!$C$2:$C$100)
```

#### Python 對照
```python
# 基本合併
df.merge(product_df, on='產品名稱', how='left')

# 設定預設值
df['價格'] = df['產品名稱'].map(product_dict).fillna('查無此產品')
```

---

### 6️⃣ LET() & LAMBDA() - 進階函數（2 小時）

#### LET() - 定義變數

**語法**
```excel
=LET(name1, value1, [name2, value2, ...], calculation)
```

**範例 1：簡化重複計算**
```excel
// 沒有 LET（重複計算）
=IF(SUM(A1:A10)/COUNT(A1:A10)>100, SUM(A1:A10)/COUNT(A1:A10)*1.1, SUM(A1:A10)/COUNT(A1:A10)*0.9)

// 使用 LET
=LET(
    平均值, SUM(A1:A10)/COUNT(A1:A10),
    IF(平均值>100, 平均值*1.1, 平均值*0.9)
)
```

**範例 2：複雜資料處理**
```excel
// 計算本月銷售額，並與上月比較
=LET(
    訂單範圍, 訂單表!A2:E1000,
    本月資料, FILTER(訂單範圍, (INDEX(訂單範圍,,2)>=DATE(2024,11,1))*(INDEX(訂單範圍,,2)<=DATE(2024,11,30))),
    本月營收, SUM(INDEX(本月資料,,5)),
    上月營收, 950000,
    成長率, (本月營收-上月營收)/上月營收,
    本月營收 & " (成長率: " & TEXT(成長率,"0.0%") & ")"
)
```

**範例 3：多步驟資料清洗**
```excel
=LET(
    原始資料, A2:C100,
    去重資料, UNIQUE(原始資料),
    排序資料, SORT(去重資料, 3, -1),
    前10筆, TAKE(排序資料, 10),
    前10筆
)
```

#### LAMBDA() - 自訂函數

**語法**
```excel
=LAMBDA(parameter1, [parameter2, ...], calculation)
```

**範例 1：簡單自訂函數**
```excel
// 定義一個計算折扣價的函數
折扣價 = LAMBDA(原價, 折扣率, 原價 * (1 - 折扣率))

// 使用
=折扣價(1000, 0.2)  // 結果：800
```

**範例 2：BMI 計算函數**
```excel
BMI計算 = LAMBDA(身高, 體重, 體重 / (身高/100)^2)

// 使用
=BMI計算(170, 65)  // 結果：22.5
```

**範例 3：與 MAP 結合**
```excel
// 對陣列中每個元素應用函數
=MAP(A2:A10, LAMBDA(x, x * 1.1))
```

#### Python 對照
```python
# LET（變數賦值）
avg = df['金額'].mean()
result = avg * 1.1 if avg > 100 else avg * 0.9

# LAMBDA
discount_price = lambda price, rate: price * (1 - rate)
df['折扣價'] = df.apply(lambda row: discount_price(row['原價'], row['折扣率']), axis=1)
```

---

### 📝 Day 1-2 實戰作業（2 小時）

#### 作業 1：動態銷售報表
使用 `case01_dynamic_sales_report.xlsx`

**任務：**
1. 使用 FILTER 篩選本月（11月）所有「已完成」的訂單
2. 使用 SORT 按金額降序排列
3. 使用 UNIQUE 建立產品類別下拉選單
4. 使用 XLOOKUP 從產品主檔查詢「建議售價」
5. 計算每筆訂單的「折扣率」=（建議售價-實際售價）/建議售價
6. 使用 LET 簡化以上所有步驟

**預期產出：**
- 動態篩選的訂單清單
- 自動更新的類別下拉選單
- 完整的價格比較分析

---

## Day 3-4: 條件與邏輯函數大全（8 小時）

### 1️⃣ IF / IFS / SWITCH（2 小時）

#### IF() - 基礎條件判斷

**語法**
```excel
=IF(logical_test, value_if_true, value_if_false)
```

**範例 1：簡單判斷**
```excel
// 判斷是否達標
=IF(A2>=100, "達標", "未達標")
```

**範例 2：巢狀 IF**
```excel
// 多級別判斷（不建議超過 3 層）
=IF(A2>=90, "優秀", IF(A2>=80, "良好", IF(A2>=60, "及格", "不及格")))
```

#### IFS() - 多條件判斷（推薦）

**語法**
```excel
=IFS(condition1, value1, [condition2, value2], ..., [TRUE, default_value])
```

**範例 3：取代巢狀 IF**
```excel
// 多級別判斷（清晰易讀）
=IFS(
    A2>=90, "優秀",
    A2>=80, "良好",
    A2>=60, "及格",
    TRUE, "不及格"
)
```

**範例 4：業績等級判定**
```excel
=IFS(
    A2>=1000000, "鑽石",
    A2>=500000, "黃金",
    A2>=200000, "白銀",
    A2>=50000, "銅牌",
    TRUE, "普通"
)
```

#### SWITCH() - 多重分支

**語法**
```excel
=SWITCH(expression, value1, result1, [value2, result2], ..., [default])
```

**範例 5：月份轉季度**
```excel
=SWITCH(MONTH(A2),
    1, "Q1", 2, "Q1", 3, "Q1",
    4, "Q2", 5, "Q2", 6, "Q2",
    7, "Q3", 8, "Q3", 9, "Q3",
    10, "Q4", 11, "Q4", 12, "Q4"
)
```

**範例 6：產品類別代碼**
```excel
=SWITCH(A2,
    "電子產品", "ELEC",
    "家電", "HOME",
    "服飾", "CLOTH",
    "食品", "FOOD",
    "OTHER"
)
```

#### Python 對照
```python
# IF
df['結果'] = df['分數'].apply(lambda x: '達標' if x >= 100 else '未達標')

# IFS（使用 np.select）
conditions = [df['分數'] >= 90, df['分數'] >= 80, df['分數'] >= 60]
choices = ['優秀', '良好', '及格']
df['等級'] = np.select(conditions, choices, default='不及格')

# SWITCH（使用 map）
season_map = {1:'Q1', 2:'Q1', 3:'Q1', 4:'Q2', ...}
df['季度'] = df['月份'].map(season_map)
```

---

### 2️⃣ SUMIF / SUMIFS / COUNTIF / COUNTIFS（2 小時）

#### SUMIF() - 單條件加總

**語法**
```excel
=SUMIF(range, criteria, [sum_range])
```

**範例 1：類別銷售額**
```excel
// 計算「電子產品」的總銷售額
=SUMIF(C2:C100, "電子產品", E2:E100)
```

**範例 2：大於某值的加總**
```excel
// 計算金額 > 5000 的訂單總額
=SUMIF(E2:E100, ">5000")
```

#### SUMIFS() - 多條件加總

**語法**
```excel
=SUMIFS(sum_range, criteria_range1, criteria1, [criteria_range2, criteria2], ...)
```

**範例 3：雙條件加總**
```excel
// 計算「電子產品」且「北部地區」的銷售額
=SUMIFS(E2:E100, C2:C100, "電子產品", D2:D100, "北部")
```

**範例 4：日期範圍加總**
```excel
// 計算本月銷售額
=SUMIFS(E2:E100, B2:B100, ">=2024-11-01", B2:B100, "<=2024-11-30")
```

**範例 5：三條件加總**
```excel
// 電子產品 + 北部 + 已完成
=SUMIFS(E2:E100, C2:C100, "電子產品", D2:D100, "北部", F2:F100, "已完成")
```

#### COUNTIF / COUNTIFS - 條件計數

**範例 6：統計訂單數**
```excel
// 計算「電子產品」的訂單數
=COUNTIF(C2:C100, "電子產品")

// 計算「電子產品」且「已完成」的訂單數
=COUNTIFS(C2:C100, "電子產品", F2:F100, "已完成")
```

#### AVERAGEIF / AVERAGEIFS - 條件平均

**範例 7：平均客單價**
```excel
// 計算「電子產品」的平均訂單金額
=AVERAGEIF(C2:C100, "電子產品", E2:E100)

// 計算「電子產品」且「北部」的平均訂單金額
=AVERAGEIFS(E2:E100, C2:C100, "電子產品", D2:D100, "北部")
```

#### 進階應用：動態條件

**範例 8：使用儲存格作為條件**
```excel
// A1 儲存格輸入類別，自動計算該類別的銷售額
=SUMIF(C2:C100, A1, E2:E100)
```

**範例 9：使用萬用字元**
```excel
// 計算產品名稱包含「手機」的銷售額
=SUMIF(D2:D100, "*手機*", E2:E100)
```

#### Python 對照
```python
# SUMIF
df[df['類別'] == '電子產品']['金額'].sum()

# SUMIFS
df[(df['類別'] == '電子產品') & (df['地區'] == '北部')]['金額'].sum()

# COUNTIF
(df['類別'] == '電子產品').sum()

# AVERAGEIF
df[df['類別'] == '電子產品']['金額'].mean()

# groupby 版本（更優雅）
df.groupby('類別')['金額'].agg(['sum', 'count', 'mean'])
```

---

### 3️⃣ 文字處理函數（2 小時）

#### LEFT / RIGHT / MID - 擷取文字

**語法**
```excel
LEFT(text, [num_chars])
RIGHT(text, [num_chars])
MID(text, start_num, num_chars)
```

**範例 1：擷取訂單編號前綴**
```excel
// ORD20241101001 → ORD
=LEFT(A2, 3)

// ORD20241101001 → 2024
=MID(A2, 4, 4)

// ORD20241101001 → 001
=RIGHT(A2, 3)
```

**範例 2：擷取日期部分**
```excel
// 2024-11-15 → 2024（年）
=LEFT(A2, 4)

// 2024-11-15 → 11（月）
=MID(A2, 6, 2)
```

#### LEN / FIND / SEARCH - 文字長度與搜尋

**範例 3：計算文字長度**
```excel
// 計算客戶名稱長度
=LEN(A2)

// 判斷是否超過 10 個字
=IF(LEN(A2)>10, "名稱過長", "正常")
```

**範例 4：搜尋文字位置**
```excel
// 找出 "@" 的位置
=FIND("@", A2)

// 擷取 email 的使用者名稱
=LEFT(A2, FIND("@", A2) - 1)
```

#### SUBSTITUTE / REPLACE - 取代文字

**範例 5：取代文字**
```excel
// 將「台北市」改成「臺北市」
=SUBSTITUTE(A2, "台北市", "臺北市")

// 移除所有空格
=SUBSTITUTE(A2, " ", "")
```

**範例 6：取代特定位置的文字**
```excel
// 將第 4-7 字元改成 "****"
=REPLACE(A2, 4, 4, "****")
```

#### TEXT - 格式化文字

**範例 7：數字格式化**
```excel
// 1234567 → 1,234,567
=TEXT(A2, "#,##0")

// 0.1234 → 12.34%
=TEXT(A2, "0.00%")

// 1234.5 → $1,234.50
=TEXT(A2, "$#,##0.00")
```

**範例 8：日期格式化**
```excel
// 2024-11-15 → 2024年11月15日
=TEXT(A2, "yyyy年mm月dd日")

// 2024-11-15 → 星期五
=TEXT(A2, "dddd")

// 2024-11-15 → 2024-Q4
=TEXT(A2, "yyyy") & "-Q" & ROUNDUP(MONTH(A2)/3, 0)
```

#### TEXTJOIN - 合併文字

**語法**
```excel
=TEXTJOIN(delimiter, ignore_empty, text1, [text2], ...)
```

**範例 9：合併多個儲存格**
```excel
// 合併產品名稱，用逗號分隔
=TEXTJOIN(", ", TRUE, A2:A10)

// 合併姓名（姓 + 名）
=TEXTJOIN(" ", TRUE, A2, B2)
```

#### TEXTSPLIT - 分割文字（Excel 365）

**語法**
```excel
=TEXTSPLIT(text, col_delimiter, [row_delimiter])
```

**範例 10：分割文字**
```excel
// "Apple,Banana,Orange" → 分割成 3 個儲存格
=TEXTSPLIT(A2, ",")

// 分割姓名
=TEXTSPLIT(A2, " ")
```

#### Python 對照
```python
# LEFT/RIGHT/MID
df['前綴'] = df['訂單編號'].str[:3]
df['年份'] = df['訂單編號'].str[3:7]
df['序號'] = df['訂單編號'].str[-3:]

# LEN
df['長度'] = df['名稱'].str.len()

# FIND/SEARCH
df['位置'] = df['email'].str.find('@')

# SUBSTITUTE
df['地址'] = df['地址'].str.replace('台北市', '臺北市')

# TEXT
df['格式化金額'] = df['金額'].apply(lambda x: f'${x:,.2f}')
df['日期文字'] = df['日期'].dt.strftime('%Y年%m月%d日')

# TEXTJOIN
','.join(df['產品名稱'].tolist())

# TEXTSPLIT
df['名稱'].str.split(',', expand=True)
```

---

### 4️⃣ 日期時間函數（2 小時）

#### DATE / TIME / NOW / TODAY

**範例 1：建立日期**
```excel
// 建立特定日期
=DATE(2024, 11, 15)

// 今天的日期
=TODAY()

// 現在的日期時間
=NOW()
```

#### YEAR / MONTH / DAY / WEEKDAY

**範例 2：擷取日期部分**
```excel
// 從日期擷取年份
=YEAR(A2)

// 從日期擷取月份
=MONTH(A2)

// 判斷星期幾（1=星期日, 2=星期一...）
=WEEKDAY(A2)

// 顯示星期幾的中文
=TEXT(A2, "aaaa")
```

#### EOMONTH - 月底日期

**範例 3：計算月初月底**
```excel
// 本月的月底
=EOMONTH(TODAY(), 0)

// 下個月的月底
=EOMONTH(TODAY(), 1)

// 本月的月初
=EOMONTH(TODAY(), -1) + 1
```

#### DATEDIF - 日期差異

**範例 4：計算日期差**
```excel
// 計算天數差
=DATEDIF(A2, B2, "D")

// 計算完整月數差
=DATEDIF(A2, B2, "M")

// 計算完整年數差
=DATEDIF(A2, B2, "Y")

// 計算年齡
=DATEDIF(A2, TODAY(), "Y")
```

#### NETWORKDAYS - 工作日

**範例 5：計算工作日**
```excel
// 計算兩日期之間的工作日（排除週末）
=NETWORKDAYS(A2, B2)

// 計算工作日（排除週末和假日）
=NETWORKDAYS(A2, B2, 假日清單!A2:A10)
```

#### WORKDAY - 工作日計算

**範例 6：加上工作日**
```excel
// 今天加上 10 個工作日
=WORKDAY(TODAY(), 10)

// 訂單日期加上 5 個工作日（交貨日）
=WORKDAY(A2, 5)
```

#### 進階應用：季度、週數

**範例 7：計算季度**
```excel
// 計算季度（Q1, Q2, Q3, Q4）
="Q" & ROUNDUP(MONTH(A2)/3, 0)

// 完整季度表示（2024-Q4）
=YEAR(A2) & "-Q" & ROUNDUP(MONTH(A2)/3, 0)
```

**範例 8：計算週數**
```excel
// 計算第幾週
=WEEKNUM(A2)

// 計算該週的週一日期
=A2 - WEEKDAY(A2, 2) + 1
```

#### Python 對照
```python
# 今天
pd.Timestamp.today()
datetime.now()

# 擷取年月日
df['年'] = df['日期'].dt.year
df['月'] = df['日期'].dt.month
df['日'] = df['日期'].dt.day
df['星期'] = df['日期'].dt.dayofweek

# 月底
df['月底'] = df['日期'] + pd.offsets.MonthEnd(0)

# 日期差
(df['結束日期'] - df['開始日期']).dt.days

# 工作日
pd.bdate_range(start, end)

# 季度
df['季度'] = df['日期'].dt.quarter
df['季度文字'] = df['日期'].dt.to_period('Q')

# 週數
df['週數'] = df['日期'].dt.isocalendar().week
```

---

### 📝 Day 3-4 實戰作業（2 小時）

#### 作業 2：客戶 RFM 分析（Excel 版）

使用 `case01_dynamic_sales_report.xlsx` 的訂單資料

**任務：**
1. 計算每位客戶的 Recency（最近一次購買距今天數）
   - 使用 `DATEDIF(MAX(...), TODAY(), "D")`

2. 計算每位客戶的 Frequency（購買次數）
   - 使用 `COUNTIF()`

3. 計算每位客戶的 Monetary（總消費金額）
   - 使用 `SUMIF()`

4. 使用 `PERCENTILE()` 計算五等分
   - R分數：`IFS(Recency <= PERCENTILE(..., 0.2), 5, ...)`
   - F分數：同上
   - M分數：同上

5. 客戶分群
   - 使用 `IFS()` 根據 RFM 分數組合分類
   - 重要客戶：R>=4, F>=4, M>=4
   - 流失客戶：R<=2
   - 新客戶：F=1

**預期產出：**
- 完整的客戶 RFM 分析表
- 客戶分群統計（使用樞紐分析表）

---

## Day 5-7: Power Query 完全攻略（8 小時）

### 📖 Power Query 基礎（2 小時）

#### 什麼是 Power Query？
- **Excel 內建的 ETL 工具**
- **E**xtract（提取）- 從各種來源讀取資料
- **T**ransform（轉換）- 清洗、整形資料
- **L**oad（載入）- 載入到 Excel 或資料模型

#### 啟動 Power Query
```
資料 → 取得資料 → 從檔案 / 從其他來源
或
資料 → 從表格/範圍
```

#### Power Query 介面
```
左側：查詢窗格（已載入的查詢）
中間：資料預覽
右側：套用的步驟（每個操作都是一個步驟）
上方：功能區（常用轉換操作）
```

#### 核心概念：步驟
- 每個操作都會記錄成一個「步驟」
- 步驟可以重新排序、刪除、修改
- 步驟是可重複執行的（重新整理資料時自動執行）

---

### 1️⃣ 資料來源（1 小時）

#### 從檔案匯入

**Excel 檔案**
```
資料 → 取得資料 → 從檔案 → 從活頁簿
```

**CSV 檔案**
```
資料 → 取得資料 → 從檔案 → 從文字/CSV
```

**從資料夾（批次處理）**
```
資料 → 取得資料 → 從檔案 → 從資料夾
→ 選擇資料夾 → 合併與轉換
```

#### 從網頁匯入
```
資料 → 取得資料 → 從其他來源 → 從 Web
→ 輸入 URL
```

#### Python 對照
```python
# Excel
df = pd.read_excel('file.xlsx', sheet_name='Sheet1')

# CSV
df = pd.read_csv('file.csv', encoding='utf-8')

# 批次處理多個檔案
import glob
files = glob.glob('data/*.csv')
df_list = [pd.read_csv(f) for f in files]
df = pd.concat(df_list, ignore_index=True)

# 從網頁
df = pd.read_html('https://example.com/table.html')[0]
```

---

### 2️⃣ 基本轉換操作（2 小時）

#### 移除欄位
```
選取欄位 → 右鍵 → 移除
或
選取欄位 → 常用 → 移除欄位
```

#### 篩選列
```
點擊欄位標題的篩選圖示 → 勾選要保留的值
或
欄位標題 → 文字篩選 → 自訂篩選
```

**進階篩選範例：**
- 包含特定文字：`Text.Contains([欄位名稱], "關鍵字")`
- 日期範圍：`Date.IsInCurrentMonth([日期])`
- 數值範圍：`[金額] > 5000 and [金額] < 10000`

#### 排序
```
欄位標題 → 排序遞增 / 排序遞減
```

#### 去除重複
```
常用 → 移除重複資料列
```

#### 取代值
```
選取欄位 → 轉換 → 取代值
→ 輸入「要尋找的值」和「取代成」
```

**批次取代：**
```
選取多個欄位 → 轉換 → 取代值
```

#### 填補空值
```
選取欄位 → 轉換 → 填入 → 向下 / 向上
或
右鍵 → 取代值 → 將 null 取代成指定值
```

#### Python 對照
```python
# 移除欄位
df = df.drop(columns=['欄位1', '欄位2'])

# 篩選列
df = df[df['金額'] > 5000]

# 排序
df = df.sort_values('金額', ascending=False)

# 去重
df = df.drop_duplicates()

# 取代
df['狀態'] = df['狀態'].replace('已完成', '完成')

# 填補空值
df['地區'] = df['地區'].fillna('未知')
df['數量'] = df['數量'].fillna(method='ffill')  # 向下填補
```

---

### 3️⃣ 進階轉換（3 小時）

#### Unpivot（取消樞紐）- 寬表轉長表

**使用情境：**
原始資料（寬表）：
```
產品     | 1月  | 2月  | 3月
--------|------|------|-----
產品A    | 100  | 150  | 200
產品B    | 80   | 90   | 110
```

目標資料（長表）：
```
產品     | 月份 | 銷售額
--------|------|-------
產品A    | 1月  | 100
產品A    | 2月  | 150
產品A    | 3月  | 200
產品B    | 1月  | 80
...
```

**操作步驟：**
```
1. 選取「產品」欄位（識別碼欄位）
2. 轉換 → 取消樞紐欄位 → 取消樞紐其他欄位
3. 重新命名欄位：「屬性」→「月份」，「值」→「銷售額」
```

**Python 對照：**
```python
df_long = df.melt(id_vars=['產品'],
                  var_name='月份',
                  value_name='銷售額')
```

#### Pivot（樞紐）- 長表轉寬表

**使用情境：**
原始資料（長表）：
```
日期      | 產品   | 數量
----------|--------|-----
2024-11-01| 產品A  | 100
2024-11-01| 產品B  | 80
2024-11-02| 產品A  | 120
2024-11-02| 產品B  | 90
```

目標資料（寬表）：
```
日期       | 產品A | 產品B
-----------|-------|------
2024-11-01 | 100   | 80
2024-11-02 | 120   | 90
```

**操作步驟：**
```
1. 選取「產品」欄位
2. 轉換 → 樞紐欄位
3. 值欄位：選擇「數量」
4. 進階選項 → 彙總值函數：總和
```

**Python 對照：**
```python
df_wide = df.pivot(index='日期', columns='產品', values='數量')
# 或
df_wide = df.pivot_table(index='日期', columns='產品', values='數量', aggfunc='sum')
```

#### Group By（分組聚合）

**操作步驟：**
```
1. 常用 → 分組依據
2. 選擇分組欄位（例如：產品類別）
3. 新增彙總欄位：
   - 新欄位名稱：總銷售額
   - 作業：總和
   - 欄位：金額
4. 點擊「新增彙總」可以加入更多彙總
```

**範例：計算每個類別的統計**
```
分組依據：產品類別
彙總：
- 總銷售額 = 總和(金額)
- 訂單數 = 計數資料列
- 平均單價 = 平均(金額)
- 最大訂單 = 最大值(金額)
```

**Python 對照：**
```python
df.groupby('產品類別').agg({
    '金額': ['sum', 'count', 'mean', 'max']
})
```

#### Merge（合併查詢）

**操作步驟：**
```
1. 在查詢中 → 常用 → 合併查詢
2. 選擇要合併的另一個查詢
3. 選擇合併欄位（兩邊都要選）
4. 選擇聯結類型：
   - 左外部（Left Outer）：保留左表所有列
   - 右外部（Right Outer）：保留右表所有列
   - 完整外部（Full Outer）：保留兩表所有列
   - 內部（Inner）：只保留兩表都有的列
   - 左反向（Left Anti）：只保留左表獨有的列
   - 右反向（Right Anti）：只保留右表獨有的列
5. 確定後，展開合併的欄位
```

**範例：訂單表 + 客戶表**
```
訂單表（左）： 訂單編號, 客戶ID, 金額
客戶表（右）： 客戶ID, 客戶名稱, 地區

合併欄位：客戶ID
聯結類型：左外部
結果：訂單編號, 客戶ID, 金額, 客戶名稱, 地區
```

**Python 對照：**
```python
# Left join
df_merged = pd.merge(orders_df, customers_df, on='客戶ID', how='left')

# Inner join
df_merged = pd.merge(orders_df, customers_df, on='客戶ID', how='inner')

# Outer join
df_merged = pd.merge(orders_df, customers_df, on='客戶ID', how='outer')
```

#### Append（附加查詢）

**使用情境：** 合併多個結構相同的資料表

**操作步驟：**
```
1. 常用 → 附加查詢
2. 選擇要附加的表格
3. 確定
```

**範例：合併多個月份的資料**
```
10月訂單 + 11月訂單 + 12月訂單 = 完整訂單
```

**Python 對照：**
```python
df_combined = pd.concat([df_oct, df_nov, df_dec], ignore_index=True)
```

---

### 📝 Day 5-7 實戰作業（2 小時）

#### 作業 3：多檔案整合 ETL 流程

**情境：** 公司有 3 個分店，每個分店每月提供一個 CSV 檔案

**資料結構：**
```
data/
├── 北部分店_202411.csv
├── 中部分店_202411.csv
└── 南部分店_202411.csv
```

**任務：**
1. 使用 Power Query「從資料夾」批次匯入所有 CSV
2. 從檔案名稱擷取「分店名稱」和「月份」
3. 移除不需要的欄位（例如：備註、內部編號）
4. 篩選「已完成」的訂單
5. 新增「年月」欄位（格式：2024-11）
6. Unpivot 產品銷售欄位（如果是寬表格式）
7. Group By 計算每個分店的每個產品的月銷售額
8. 合併「產品主檔」（使用 Merge）
9. 載入到 Excel

**預期產出：**
- 完整的多分店銷售整合表
- 可重複執行的 ETL 流程（新增檔案後，點擊「重新整理」即可更新）

---

# 🎯 Week 2: 樞紐分析 + VBA/巨集 + 綜合應用（24 小時）

## Day 8-9: 樞紐分析表完全攻略（8 小時）

### 📖 樞紐分析表基礎（1 小時）

#### 什麼是樞紐分析表？
- **快速摘要大量資料**
- **動態多維度分析**
- **即時切換檢視角度**
- **無需寫公式**

#### 建立基礎樞紐表
```
1. 選取資料範圍
2. 插入 → 樞紐分析表
3. 選擇放置位置（新工作表 / 現有工作表）
4. 拖曳欄位到四個區域：
   - 篩選：頁面層級篩選
   - 列：行標題
   - 欄：列標題
   - 值：要彙總的數值
```

#### 樞紐分析表的四個區域
```
篩選區（Filters）
┌────────────────┐
│ [地區: 全部]   │
└────────────────┘

         欄區（Columns）
         ┌─────┬─────┬─────┐
列區     │ 1月 │ 2月 │ 3月 │
(Rows)   ├─────┼─────┼─────┤
┌──────┐ │     │     │     │
│產品A │ │ 100 │ 150 │ 200 │
│產品B │ │  80 │  90 │ 110 │
└──────┘ └─────┴─────┴─────┘
          ↑
         值區（Values）
```

---

### 1️⃣ 基礎樞紐操作（2 小時）

#### 範例 1：產品類別銷售分析

**資料：** 訂單明細（訂單編號、日期、產品類別、產品名稱、金額）

**樞紐設定：**
```
列：產品類別
值：加總-金額
```

**結果：**
```
產品類別      | 總計
-------------|--------
電子產品      | 1,500,000
家電          | 800,000
服飾          | 600,000
食品          | 400,000
總計          | 3,300,000
```

#### 範例 2：雙維度分析

**樞紐設定：**
```
列：產品類別
欄：地區
值：加總-金額
```

**結果：**
```
產品類別  | 北部    | 中部   | 南部   | 總計
---------|---------|--------|--------|--------
電子產品  | 600,000 | 500,000| 400,000| 1,500,000
家電      | 300,000 | 250,000| 250,000| 800,000
...
```

#### 範例 3：多值欄位

**樞紐設定：**
```
列：產品類別
值：
  - 加總-金額（銷售額）
  - 計數-訂單編號（訂單數）
  - 平均-金額（平均單價）
```

**結果：**
```
產品類別  | 銷售額  | 訂單數 | 平均單價
---------|---------|--------|--------
電子產品  | 1,500,000| 150   | 10,000
家電      | 800,000 | 100   | 8,000
...
```

#### Python 對照
```python
# 範例 1
df.pivot_table(index='產品類別', values='金額', aggfunc='sum')

# 範例 2
df.pivot_table(index='產品類別', columns='地區', values='金額', aggfunc='sum')

# 範例 3
df.pivot_table(index='產品類別', values='金額', aggfunc=['sum', 'count', 'mean'])
```

---

### 2️⃣ 計算欄位與顯示方式（2 小時）

#### 新增計算欄位

**操作：**
```
選取樞紐分析表 → 樞紐分析表分析 → 欄位、項目與集 → 計算欄位
```

**範例 4：計算平均客單價**
```
名稱：平均客單價
公式：= 金額 / 訂單數
```

**範例 5：計算利潤**
```
名稱：利潤
公式：= 銷售額 * 0.3  // 假設利潤率 30%
```

#### 顯示值方式

**操作：**
```
選取值欄位 → 值欄位設定 → 顯示值方式
```

**常用選項：**
- **一般：** 原始值
- **總和的百分比：** 佔總計的百分比
- **列總和的百分比：** 佔該列總計的百分比
- **欄總和的百分比：** 佔該欄總計的百分比
- **差異：** 與基底項目的差異
- **差異百分比：** 與基底項目的差異百分比
- **累計：** 累計值

**範例 6：計算佔比**
```
列：產品類別
值：加總-金額
顯示值方式：總和的百分比
```

**結果：**
```
產品類別  | 佔比
---------|-------
電子產品  | 45.5%
家電      | 24.2%
服飾      | 18.2%
食品      | 12.1%
總計      | 100.0%
```

**範例 7：月度成長率**
```
列：產品類別
欄：月份
值：加總-金額
顯示值方式：差異百分比（基底項目：上一個月）
```

#### Python 對照
```python
# 計算欄位
pivot['平均客單價'] = pivot['金額'] / pivot['訂單數']

# 佔比
pivot['佔比'] = pivot['金額'] / pivot['金額'].sum()

# 成長率
pivot['成長率'] = pivot['金額'].pct_change()
```

---

### 3️⃣ 群組與切片篩選器（2 小時）

#### 日期群組

**操作：**
```
在樞紐分析表中選取日期欄位 → 右鍵 → 群組
```

**群組選項：**
- 秒、分鐘、小時
- 日、月、季、年

**範例 8：月度銷售趨勢**
```
列：日期（群組：月）
值：加總-金額
```

**結果：**
```
月份      | 銷售額
---------|--------
2024-01  | 1,200,000
2024-02  | 1,350,000
2024-03  | 1,500,000
...
```

**範例 9：季度分析**
```
列：日期（群組：季）
值：加總-金額
```

#### 數值群組

**範例 10：金額區間分析**
```
選取「金額」欄位 → 右鍵 → 群組
起始於：0
結束於：100000
間距：10000
```

**結果：**
```
金額區間    | 訂單數
-----------|-------
0-10000    | 450
10000-20000| 320
20000-30000| 180
...
```

#### 切片篩選器

**操作：**
```
選取樞紐分析表 → 樞紐分析表分析 → 插入切片篩選器
→ 選擇欄位（例如：產品類別、地區）
```

**功能：**
- 視覺化的篩選按鈕
- 可以同時控制多個樞紐分析表
- 支援多選

**範例 11：互動式儀表板**
```
建立 3 個樞紐分析表：
1. 類別銷售額
2. 地區銷售額
3. 月度趨勢

新增切片篩選器：產品類別、地區、月份
連接到所有 3 個樞紐分析表

→ 點擊切片篩選器，所有圖表同步更新
```

#### 時間軸

**操作：**
```
選取樞紐分析表 → 樞紐分析表分析 → 插入時間軸
→ 選擇日期欄位
```

**功能：**
- 拖曳選擇日期範圍
- 支援日、月、季、年
- 視覺化時間篩選

---

### 4️⃣ 樞紐圖表（1 小時）

#### 建立樞紐圖表

**方法 1：從樞紐分析表建立**
```
選取樞紐分析表 → 樞紐分析表分析 → 樞紐圖
```

**方法 2：直接建立**
```
選取資料 → 插入 → 樞紐圖
```

#### 常用圖表類型

**範例 12：產品類別銷售 - 橫條圖**
```
列：產品類別
值：加總-金額
圖表：橫條圖
```

**範例 13：月度趨勢 - 折線圖**
```
列：月份
值：加總-金額
圖表：折線圖
```

**範例 14：類別佔比 - 圓餅圖**
```
列：產品類別
值：加總-金額
圖表：圓餅圖
```

**範例 15：銷售額 + 訂單數 - 組合圖**
```
列：月份
值：加總-金額（主要座標軸）、計數-訂單數（次要座標軸）
圖表：組合圖（折線 + 直條）
```

---

### 📝 Day 8-9 實戰作業（2 小時）

#### 作業 4：完整銷售儀表板

使用 `case01_dynamic_sales_report.xlsx`

**任務：**
1. 建立 4 個樞紐分析表：
   - 產品類別銷售額（含佔比）
   - 地區銷售額
   - 月度銷售趨勢
   - Top 10 產品

2. 新增計算欄位：
   - 平均客單價 = 金額 / 訂單數
   - 成長率（與上月比較）

3. 新增切片篩選器：
   - 產品類別
   - 地區
   - 訂單狀態

4. 新增時間軸：
   - 訂單日期

5. 建立樞紐圖表：
   - 類別銷售 - 橫條圖
   - 月度趨勢 - 折線圖
   - 地區佔比 - 圓餅圖
   - 銷售額+訂單數 - 組合圖

6. 美化儀表板：
   - 統一配色
   - 清晰的標題
   - 適當的間距

**預期產出：**
- 完整的互動式銷售儀表板
- 點擊切片篩選器，所有圖表同步更新

---

## Day 10-12: VBA 巨集與自動化（8 小時）

### 📖 VBA 基礎（2 小時）

#### 什麼是 VBA？
- **Visual Basic for Applications**
- Excel 內建的程式語言
- 可以自動化任何 Excel 操作
- 類似 Python，但專為 Office 設計

#### 啟用開發人員模式
```
檔案 → 選項 → 自訂功能區
→ 勾選「開發人員」
```

#### VBA 編輯器（VBE）
```
開發人員 → Visual Basic
或按 Alt + F11
```

**VBE 介面：**
```
左側：專案瀏覽器（顯示所有工作表、模組）
中間：程式碼編輯區
下方：即時運算視窗（用於測試）
```

#### 第一個 VBA 程式
```vb
Sub HelloWorld()
    MsgBox "Hello, World!"
End Sub
```

**執行方式：**
```
1. 在 VBE 中按 F5
2. 或回到 Excel → 開發人員 → 巨集 → 選擇 HelloWorld → 執行
```

---

### 1️⃣ 巨集錄製（1 小時）

#### 錄製巨集

**操作：**
```
開發人員 → 錄製巨集
→ 輸入巨集名稱
→ 執行一系列操作
→ 停止錄製
```

**範例 16：自動格式化表格**

**錄製步驟：**
```
1. 開始錄製
2. 選取 A1:E100
3. 設定框線
4. 標題列：粗體、藍底白字
5. 數字欄位：千分位、小數點 2 位
6. 自動調整欄寬
7. 停止錄製
```

**產生的程式碼：**
```vb
Sub 格式化表格()
    Range("A1:E100").Select
    Selection.Borders.LineStyle = xlContinuous
    Range("A1:E1").Select
    With Selection
        .Font.Bold = True
        .Interior.Color = RGB(68, 114, 196)
        .Font.Color = RGB(255, 255, 255)
    End With
    Columns("E:E").NumberFormat = "#,##0.00"
    Columns("A:E").AutoFit
End Sub
```

#### 檢視和編輯錄製的巨集
```
開發人員 → 巨集 → 選擇巨集 → 編輯
```

#### 指定快捷鍵
```
開發人員 → 巨集 → 選擇巨集 → 選項
→ 設定快速鍵（例如：Ctrl+Shift+F）
```

---

### 2️⃣ VBA 基本語法（2 小時）

#### 變數與資料型別

**宣告變數：**
```vb
Dim 變數名稱 As 資料型別
```

**常用資料型別：**
```vb
Dim 數量 As Integer          ' 整數（-32768 到 32767）
Dim 金額 As Long             ' 長整數
Dim 價格 As Double           ' 浮點數
Dim 名稱 As String           ' 文字
Dim 是否完成 As Boolean      ' 布林值（True/False）
Dim 日期 As Date             ' 日期
Dim 儲存格 As Range          ' 儲存格範圍
Dim 工作表 As Worksheet      ' 工作表
```

**範例：**
```vb
Sub 變數範例()
    Dim 產品名稱 As String
    Dim 單價 As Double
    Dim 數量 As Integer
    Dim 總金額 As Double

    產品名稱 = "無線滑鼠"
    單價 = 299.5
    數量 = 10
    總金額 = 單價 * 數量

    MsgBox "產品：" & 產品名稱 & vbCrLf & _
           "單價：" & 單價 & vbCrLf & _
           "數量：" & 數量 & vbCrLf & _
           "總金額：" & 總金額
End Sub
```

#### 操作儲存格

**範例 17：讀取儲存格**
```vb
Sub 讀取儲存格()
    Dim 值 As String

    ' 方法 1：使用 Range
    值 = Range("A1").Value

    ' 方法 2：使用 Cells（列, 欄）
    值 = Cells(1, 1).Value

    ' 方法 3：指定工作表
    值 = Worksheets("工作表1").Range("A1").Value

    MsgBox "A1 的值：" & 值
End Sub
```

**範例 18：寫入儲存格**
```vb
Sub 寫入儲存格()
    ' 寫入文字
    Range("A1").Value = "產品名稱"

    ' 寫入數字
    Range("B1").Value = 1000

    ' 寫入公式
    Range("C1").Formula = "=A1&B1"

    ' 寫入目前日期
    Range("D1").Value = Date
End Sub
```

#### 迴圈

**For 迴圈：**
```vb
Sub For迴圈範例()
    Dim i As Integer

    ' 在 A1:A10 填入 1-10
    For i = 1 To 10
        Cells(i, 1).Value = i
    Next i
End Sub
```

**For Each 迴圈：**
```vb
Sub ForEach範例()
    Dim 儲存格 As Range

    ' 對 A1:A10 的每個儲存格加上 10%
    For Each 儲存格 In Range("A1:A10")
        儲存格.Value = 儲存格.Value * 1.1
    Next 儲存格
End Sub
```

**Do While 迴圈：**
```vb
Sub DoWhile範例()
    Dim i As Integer
    i = 1

    ' 從 A1 開始，找到第一個空白儲存格
    Do While Cells(i, 1).Value <> ""
        i = i + 1
    Loop

    MsgBox "第一個空白儲存格在列 " & i
End Sub
```

#### 條件判斷

**If...Then...Else：**
```vb
Sub If範例()
    Dim 分數 As Integer
    Dim 等級 As String

    分數 = Range("A1").Value

    If 分數 >= 90 Then
        等級 = "優秀"
    ElseIf 分數 >= 80 Then
        等級 = "良好"
    ElseIf 分數 >= 60 Then
        等級 = "及格"
    Else
        等級 = "不及格"
    End If

    Range("B1").Value = 等級
End Sub
```

**Select Case：**
```vb
Sub SelectCase範例()
    Dim 月份 As Integer
    Dim 季度 As String

    月份 = Month(Date)

    Select Case 月份
        Case 1, 2, 3
            季度 = "Q1"
        Case 4, 5, 6
            季度 = "Q2"
        Case 7, 8, 9
            季度 = "Q3"
        Case 10, 11, 12
            季度 = "Q4"
    End Select

    MsgBox "目前是 " & 季度
End Sub
```

---

### 3️⃣ 實用 VBA 巨集範例（3 小時）

#### 範例 19：自動清洗資料

```vb
Sub 清洗資料()
    Dim 最後列 As Long
    Dim i As Long

    ' 找到最後一列
    最後列 = Cells(Rows.Count, 1).End(xlUp).Row

    ' 移除空白列
    For i = 最後列 To 2 Step -1
        If Application.WorksheetFunction.CountA(Rows(i)) = 0 Then
            Rows(i).Delete
        End If
    Next i

    ' 移除重複值
    Range("A1").CurrentRegion.RemoveDuplicates Columns:=1, Header:=xlYes

    ' 去除多餘空格
    For i = 2 To 最後列
        Cells(i, 1).Value = Trim(Cells(i, 1).Value)
    Next i

    MsgBox "資料清洗完成！"
End Sub
```

**Python 對照：**
```python
# 移除空白列
df = df.dropna(how='all')

# 移除重複值
df = df.drop_duplicates()

# 去除空格
df['欄位'] = df['欄位'].str.strip()
```

#### 範例 20：批次匯入檔案

```vb
Sub 批次匯入CSV()
    Dim 資料夾路徑 As String
    Dim 檔案名稱 As String
    Dim 工作表 As Worksheet
    Dim 目標列 As Long

    ' 設定資料夾路徑
    資料夾路徑 = "C:\資料\"

    ' 建立新工作表
    Set 工作表 = ThisWorkbook.Worksheets.Add
    工作表.Name = "整合資料"
    目標列 = 1

    ' 取得第一個 CSV 檔案
    檔案名稱 = Dir(資料夾路徑 & "*.csv")

    ' 迴圈處理所有 CSV 檔案
    Do While 檔案名稱 <> ""
        ' 開啟 CSV
        Workbooks.Open 資料夾路徑 & 檔案名稱

        ' 複製資料（跳過標題）
        If 目標列 = 1 Then
            ' 第一個檔案：複製含標題
            Range("A1").CurrentRegion.Copy _
                Destination:=工作表.Cells(目標列, 1)
            目標列 = 工作表.Cells(Rows.Count, 1).End(xlUp).Row + 1
        Else
            ' 後續檔案：只複製資料
            Range("A2").CurrentRegion.Copy _
                Destination:=工作表.Cells(目標列, 1)
            目標列 = 工作表.Cells(Rows.Count, 1).End(xlUp).Row + 1
        End If

        ' 關閉 CSV
        Workbooks(檔案名稱).Close SaveChanges:=False

        ' 下一個檔案
        檔案名稱 = Dir()
    Loop

    MsgBox "匯入完成！共 " & 目標列 - 1 & " 列資料"
End Sub
```

**Python 對照：**
```python
import glob
import pandas as pd

files = glob.glob('C:/資料/*.csv')
df_list = [pd.read_csv(f) for f in files]
df = pd.concat(df_list, ignore_index=True)
```

#### 範例 21：自動生成報表

```vb
Sub 生成月報()
    Dim 報表工作表 As Worksheet
    Dim 資料工作表 As Worksheet
    Dim 最後列 As Long
    Dim 樞紐表 As PivotTable

    ' 設定工作表
    Set 資料工作表 = Worksheets("訂單資料")

    ' 建立新工作表
    Set 報表工作表 = ThisWorkbook.Worksheets.Add
    報表工作表.Name = "月報_" & Format(Date, "yyyymm")

    ' 標題
    With 報表工作表.Range("A1")
        .Value = "銷售月報"
        .Font.Size = 16
        .Font.Bold = True
    End With

    ' 日期
    報表工作表.Range("A2").Value = "報表日期：" & Date

    ' KPI 摘要
    報表工作表.Range("A4").Value = "總營收"
    報表工作表.Range("B4").Formula = "=SUM(訂單資料!E:E)"

    報表工作表.Range("A5").Value = "訂單數"
    報表工作表.Range("B5").Formula = "=COUNT(訂單資料!A:A)-1"

    報表工作表.Range("A6").Value = "平均客單價"
    報表工作表.Range("B6").Formula = "=B4/B5"

    ' 格式化數字
    報表工作表.Range("B4:B6").NumberFormat = "#,##0"

    ' 建立樞紐分析表（類別銷售）
    最後列 = 資料工作表.Cells(Rows.Count, 1).End(xlUp).Row
    Set 樞紐表 = ThisWorkbook.PivotCaches.Create( _
        SourceType:=xlDatabase, _
        SourceData:=資料工作表.Range("A1:E" & 最後列) _
    ).CreatePivotTable( _
        TableDestination:=報表工作表.Range("A8"), _
        TableName:="類別銷售" _
    )

    With 樞紐表
        .PivotFields("產品類別").Orientation = xlRowField
        .AddDataField .PivotFields("金額"), "銷售額", xlSum
    End With

    MsgBox "月報生成完成！"
End Sub
```

#### 範例 22：自動寄送 Email

```vb
Sub 寄送報表()
    Dim OutlookApp As Object
    Dim OutlookMail As Object
    Dim 收件者 As String
    Dim 主旨 As String
    Dim 內文 As String

    ' 建立 Outlook 物件
    Set OutlookApp = CreateObject("Outlook.Application")
    Set OutlookMail = OutlookApp.CreateItem(0)

    ' 設定信件內容
    收件者 = "manager@example.com"
    主旨 = "銷售月報 - " & Format(Date, "yyyy-mm")
    內文 = "您好，" & vbCrLf & vbCrLf & _
           "附件為本月銷售報表，請參閱。" & vbCrLf & vbCrLf & _
           "總營收：" & Range("B4").Text & vbCrLf & _
           "訂單數：" & Range("B5").Text & vbCrLf & vbCrLf & _
           "系統自動發送"

    ' 建立郵件
    With OutlookMail
        .To = 收件者
        .Subject = 主旨
        .Body = 內文
        .Attachments.Add ThisWorkbook.FullName
        .Send  ' 或使用 .Display 預覽後再手動寄送
    End With

    MsgBox "報表已寄出！"
End Sub
```

#### 範例 23：進度條

```vb
Sub 處理大量資料_附進度條()
    Dim 總筆數 As Long
    Dim i As Long
    Dim 進度表單 As Object

    總筆數 = Cells(Rows.Count, 1).End(xlUp).Row

    ' 建立進度條表單（需先在 VBE 中建立 UserForm）
    ' 這裡簡化版：使用 Excel 儲存格當進度條
    Range("Z1").Value = "處理進度"

    For i = 2 To 總筆數
        ' 處理資料
        Cells(i, 2).Value = Cells(i, 1).Value * 1.1

        ' 更新進度
        If i Mod 100 = 0 Then
            Application.StatusBar = "處理中... " & _
                Format(i / 總筆數, "0%") & " 完成"
            DoEvents  ' 讓 Excel 更新畫面
        End If
    Next i

    Application.StatusBar = False
    MsgBox "處理完成！"
End Sub
```

---

### 📝 Day 10-12 實戰作業（2 小時）

#### 作業 5：完整自動化報表系統

**需求：**
建立一個完整的自動化報表系統，包含：

**功能 1：資料匯入**
```vb
Sub 匯入資料()
    ' 從指定資料夾匯入所有 CSV 檔案
    ' 自動清洗資料（去空白、去重複、Trim）
    ' 新增「匯入日期」欄位
End Sub
```

**功能 2：資料分析**
```vb
Sub 分析資料()
    ' 計算 KPI（總營收、訂單數、平均客單價）
    ' 建立樞紐分析表（類別、地區、月度）
    ' 找出 Top 10 產品
End Sub
```

**功能 3：生成報表**
```vb
Sub 生成報表()
    ' 建立新工作表「月報_yyyymm」
    ' 格式化標題與 KPI 區域
    ' 插入圖表（類別、趨勢）
    ' 自動調整欄寬、設定框線
End Sub
```

**功能 4：匯出與寄送**
```vb
Sub 匯出並寄送()
    ' 另存新檔到指定資料夾
    ' 產生 PDF 版本
    ' 寄送 Email 給主管
End Sub
```

**功能 5：主控台（按鈕介面）**
```
在工作表建立 4 個按鈕，分別連接到上述 4 個巨集
或建立一個「執行全部」按鈕，依序執行所有步驟
```

**預期產出：**
- 完整的 VBA 自動化系統
- 一鍵產生專業報表
- 可重複使用的範本

---

## Day 13-14: 綜合實戰與總複習（8 小時）

### 📝 Final Project: 企業級銷售分析系統

#### 專案需求

**情境：**
你是一家電商公司的資料分析師，需要建立一個完整的銷售分析系統。

**資料來源：**
- 每日訂單 CSV 檔案（from 3 個分店）
- 產品主檔 Excel
- 客戶資料 Excel

**必須包含的功能：**

1. **自動化 ETL**
   - 使用 Power Query 批次匯入每日訂單
   - 合併產品主檔與客戶資料
   - 資料清洗（去重、填補空值、格式標準化）

2. **進階分析**
   - RFM 客戶分群（使用函數計算）
   - Top 20 產品（使用 FILTER + SORT）
   - 月度成長率分析
   - 庫存警示（使用 IF/IFS）

3. **互動式儀表板**
   - 4 個樞紐分析表：
     * 類別銷售（含佔比）
     * 地區分析
     * 月度趨勢
     * 客戶分群
   - 切片篩選器：類別、地區、時間
   - 4 個樞紐圖表

4. **VBA 自動化**
   - 一鍵匯入資料
   - 一鍵更新所有分析
   - 一鍵生成月報
   - 自動寄送報表

5. **專業報表**
   - 首頁：關鍵 KPI（大字體、配色）
   - 分析頁：圖表與表格
   - 明細頁：完整資料
   - 目錄頁：超連結導航

#### 評分標準

| 項目 | 權重 | 評分標準 |
|------|------|---------|
| 功能完整性 | 40% | 所有必須功能都實現 |
| 程式碼品質 | 20% | VBA 程式碼清晰、有註解、可維護 |
| 使用者體驗 | 20% | 操作簡單、直覺、有提示訊息 |
| 視覺呈現 | 20% | 專業美觀、配色協調、版面整齊 |

---

## 📚 學習資源總整理

### 官方文件
1. **Microsoft Excel 函數參考**
   https://support.microsoft.com/zh-tw/office/excel-函數

2. **Power Query 文件**
   https://support.microsoft.com/zh-tw/office/power-query

3. **VBA 語言參考**
   https://docs.microsoft.com/zh-tw/office/vba/api/overview/excel

### 推薦書籍
1. **《Excel VBA 程式設計實戰寶典》** - 適合進階學習
2. **《Power Query 資料整理實戰》** - 深入 Power Query
3. **《Excel 樞紐分析完全攻略》** - 樞紐表技巧

### YouTube 頻道
1. **Leila Gharani** - Excel 進階技巧
2. **MyOnlineTrainingHub** - Power Query 教學
3. **ExcelIsFun** - 綜合 Excel 技巧
4. **Wise Owl Tutorials** - VBA 完整教學

### 線上課程
1. **Coursera - Excel Skills for Business**
2. **Udemy - Excel VBA 程式設計**
3. **LinkedIn Learning - Power Query 實戰**

---

## ✅ 完整學習檢核表

### Week 1: 進階函數（24 小時）

#### Day 1-2: 動態陣列函數（8h）
- [ ] 理解動態陣列概念（#SPILL! 錯誤）
- [ ] FILTER() 單條件、多條件（AND/OR）
- [ ] SORT() / SORTBY() 單欄、多欄排序
- [ ] UNIQUE() 去重、多欄組合
- [ ] SEQUENCE() / RANDARRAY() 生成陣列
- [ ] XLOOKUP() 取代 VLOOKUP
- [ ] LET() 定義變數
- [ ] LAMBDA() 自訂函數
- [ ] 完成作業 1：動態銷售報表

#### Day 3-4: 條件與邏輯函數（8h）
- [ ] IF / IFS / SWITCH 條件判斷
- [ ] SUMIF / SUMIFS 條件加總
- [ ] COUNTIF / COUNTIFS 條件計數
- [ ] AVERAGEIF / AVERAGEIFS 條件平均
- [ ] LEFT / RIGHT / MID 文字擷取
- [ ] FIND / SEARCH / LEN 文字搜尋
- [ ] SUBSTITUTE / REPLACE 文字取代
- [ ] TEXT 格式化文字
- [ ] TEXTJOIN / TEXTSPLIT 合併分割
- [ ] DATE / YEAR / MONTH / DAY 日期函數
- [ ] DATEDIF / NETWORKDAYS 日期計算
- [ ] 完成作業 2：客戶 RFM 分析

#### Day 5-7: Power Query（8h）
- [ ] 理解 Power Query 概念與介面
- [ ] 從檔案/資料夾匯入資料
- [ ] 基本轉換（移除、篩選、排序、去重、取代）
- [ ] Unpivot（寬表→長表）
- [ ] Pivot（長表→寬表）
- [ ] Group By 分組聚合
- [ ] Merge 合併查詢（各種 Join）
- [ ] Append 附加查詢
- [ ] 完成作業 3：多檔案整合 ETL

### Week 2: 樞紐分析 + VBA（24 小時）

#### Day 8-9: 樞紐分析表（8h）
- [ ] 理解樞紐分析表概念與結構
- [ ] 建立基礎樞紐表（單維度、雙維度）
- [ ] 多值欄位（加總、計數、平均）
- [ ] 新增計算欄位
- [ ] 顯示值方式（百分比、差異、累計）
- [ ] 日期群組（月、季、年）
- [ ] 數值群組（金額區間）
- [ ] 切片篩選器（多選、連接多個樞紐表）
- [ ] 時間軸
- [ ] 樞紐圖表（橫條、折線、圓餅、組合）
- [ ] 完成作業 4：完整銷售儀表板

#### Day 10-12: VBA 巨集（8h）
- [ ] 理解 VBA 概念，啟用開發人員模式
- [ ] 使用巨集錄製
- [ ] 基本語法（變數、資料型別）
- [ ] 操作儲存格（讀取、寫入、公式）
- [ ] 迴圈（For, For Each, Do While）
- [ ] 條件判斷（If, Select Case）
- [ ] 實用範例：清洗資料
- [ ] 實用範例：批次匯入檔案
- [ ] 實用範例：自動生成報表
- [ ] 實用範例：寄送 Email
- [ ] 完成作業 5：自動化報表系統

#### Day 13-14: 綜合實戰（8h）
- [ ] 完成 Final Project：企業級銷售分析系統
- [ ] 自動化 ETL（Power Query）
- [ ] 進階分析（動態陣列函數）
- [ ] 互動式儀表板（樞紐分析表）
- [ ] VBA 自動化（一鍵執行）
- [ ] 專業報表（格式化、美化）

---

## 🎯 學習成果

完成 Week 1-2 後，你將能夠：

### 技能
✅ 熟練使用 50+ Excel 進階函數
✅ 掌握動態陣列與 XLOOKUP
✅ 使用 Power Query 進行 ETL 資料處理
✅ 建立複雜的樞紐分析表與圖表
✅ 編寫 VBA 巨集自動化重複工作
✅ 建立互動式商業儀表板

### 作品集
✅ 動態銷售報表（動態陣列函數）
✅ 客戶 RFM 分析（條件函數）
✅ 多檔案整合 ETL（Power Query）
✅ 互動式銷售儀表板（樞紐分析表）
✅ 自動化報表系統（VBA 巨集）
✅ 企業級銷售分析系統（綜合應用）

### 思維轉換
✅ 理解 Excel → Python 的對應關係
✅ 掌握資料分析的完整流程（ETL → 分析 → 視覺化）
✅ 建立自動化思維（減少重複工作）

---

## 🚀 下一步：Week 3-6 pandas 進階實戰

完成 Excel 進階學習後，你將：
- 理解「為什麼要用 Python」
- 輕鬆轉換 Excel 思維到 pandas
- 處理 Excel 無法處理的大量資料（100 萬筆以上）
- 建立更複雜的分析與機器學習模型

**準備好了嗎？讓我們開始 Week 1 的第一個練習吧！** 🎊
