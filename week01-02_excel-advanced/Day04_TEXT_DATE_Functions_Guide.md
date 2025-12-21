# Day 4: 文字 & 日期函數完全攻略

## 🎯 學習目標（4-5 小時）

掌握文字處理和日期計算，這是資料清洗的核心技能。

**學完後你將能夠：**
- ✅ 提取、分割、組合文字
- ✅ 格式化數字和日期顯示
- ✅ 計算日期差異、工作日
- ✅ 處理真實業務中的髒資料

---

## 📚 Part 1: 文字提取函數（60 分鐘）

### LEFT / RIGHT / MID

**語法：**
```excel
=LEFT(text, num_chars)      // 從左邊取 N 個字元
=RIGHT(text, num_chars)     // 從右邊取 N 個字元
=MID(text, start_num, num_chars)  // 從中間取
```

---

### 範例 1：提取訂單編號的年月

**訂單編號格式：** `ORD20241101001`

```excel
// 提取年份（位置 4-7）
=MID(A2, 4, 4)  // 結果：2024

// 提取月份（位置 8-9）
=MID(A2, 8, 2)  // 結果：11

// 提取日期（位置 10-11）
=MID(A2, 10, 2)  // 結果：01

// 提取流水號（最後 3 碼）
=RIGHT(A2, 3)  // 結果：001
```

---

### 範例 2：提取 Email 使用者名稱

**Email：** `customer@example.com`

```excel
// 方法 1：使用 LEFT + FIND
=LEFT(A2, FIND("@", A2) - 1)  // 結果：customer

// 方法 2：使用 TEXTBEFORE（Excel 365）
=TEXTBEFORE(A2, "@")  // 結果：customer
```

---

### 範例 3：提取地址中的城市

**地址：** `台北市信義區信義路五段7號`

```excel
// 提取前 3 個字（城市）
=LEFT(A2, 3)  // 結果：台北市

// 或提取「市」之前的部分
=TEXTBEFORE(A2, "市") & "市"  // 結果：台北市
```

---

## 📖 Part 2: 文字搜尋函數（45 分鐘）

### FIND / SEARCH

**語法：**
```excel
=FIND(find_text, within_text, [start_num])  // 區分大小寫
=SEARCH(find_text, within_text, [start_num])  // 不區分大小寫
```

---

### 範例 4：找到 "@" 的位置

```excel
=FIND("@", "customer@example.com")  // 結果：9
```

---

### 範例 5：判斷文字是否包含關鍵字

**情境：** 檢查地址是否包含「台北」

```excel
// 方法 1：ISNUMBER + SEARCH
=ISNUMBER(SEARCH("台北", A2))  // 結果：TRUE 或 FALSE

// 方法 2：結合 IF
=IF(ISNUMBER(SEARCH("台北", A2)), "北部", "其他")
```

**用途：** 用於 FILTER 條件

```excel
=FILTER(訂單明細!A:AN, ISNUMBER(SEARCH("台北", 訂單明細!L:L)))
```

---

## 🔥 Part 3: 文字替換與清理（60 分鐘）

### SUBSTITUTE / REPLACE

**語法：**
```excel
=SUBSTITUTE(text, old_text, new_text, [instance_num])
=REPLACE(old_text, start_num, num_chars, new_text)
```

---

### 範例 6：統一地址格式

**情境：** 將「台北市」統一改成「臺北市」

```excel
=SUBSTITUTE(A2, "台北市", "臺北市")
```

**批次替換：**
```excel
=SUBSTITUTE(SUBSTITUTE(A2, "台北", "臺北"), "台中", "臺中")
```

---

### 範例 7：移除空格

**情境：** 客戶姓名中有多餘空格：`" 王小明 "`

```excel
// 移除所有空格
=SUBSTITUTE(A2, " ", "")  // 結果：王小明

// 只移除前後空格（保留中間）
=TRIM(A2)  // 結果：王小明
```

---

### 範例 8：遮蔽手機號碼

**情境：** `0912-345-678` → `0912-XXX-XXX`

```excel
=LEFT(A2, 5) & "XXX-XXX"
```

**或使用 REPLACE：**
```excel
=REPLACE(A2, 6, 8, "XXX-XXX")
```

---

### 範例 9：移除特殊字元

**情境：** 電話號碼格式不統一：`(02)2345-6789`、`02-2345-6789`

```excel
// 移除所有非數字字元
=SUBSTITUTE(SUBSTITUTE(SUBSTITUTE(A2, "-", ""), "(", ""), ")", "")
```

**進階（使用 TEXTJOIN + FILTER）：**
```excel
=TEXTJOIN("", TRUE, FILTER(MID(A2, SEQUENCE(LEN(A2)), 1), ISNUMBER(VALUE(MID(A2, SEQUENCE(LEN(A2)), 1)))))
```

---

## 💡 Part 4: 文字格式化（TEXT 函數）（60 分鐘）

### TEXT() - 最強大的格式化函數

**語法：**
```excel
=TEXT(value, format_text)
```

---

### 範例 10：數字格式化

**情境：** 格式化金額顯示

```excel
// 千分位
=TEXT(1234567, "#,##0")  // 結果：1,234,567

// 千分位 + 小數點 2 位
=TEXT(1234.5, "#,##0.00")  // 結果：1,234.50

// 貨幣格式
=TEXT(1234567, "$#,##0")  // 結果：$1,234,567
=TEXT(1234567, "NT$#,##0")  // 結果：NT$1,234,567

// 百分比
=TEXT(0.125, "0.00%")  // 結果：12.50%

// 帶正負號
=TEXT(1234, "+#,##0;-#,##0")  // 正數顯示 +1,234，負數顯示 -1,234
```

---

### 範例 11：日期格式化

**情境：** 格式化日期顯示

```excel
// 中文日期
=TEXT(TODAY(), "yyyy年mm月dd日")  // 結果：2024年11月15日

// 星期幾
=TEXT(TODAY(), "dddd")  // 結果：Friday（英文）
=TEXT(TODAY(), "aaaa")  // 結果：星期五（中文）

// 年-月-日
=TEXT(TODAY(), "yyyy-mm-dd")  // 結果：2024-11-15

// 月/日
=TEXT(TODAY(), "mm/dd")  // 結果：11/15

// 季度
=TEXT(TODAY(), "yyyy-Q") & ROUNDUP(MONTH(TODAY())/3, 0)  // 結果：2024-Q4
```

---

### 範例 12：時間格式化

```excel
// 時:分:秒
=TEXT(NOW(), "hh:mm:ss")  // 結果：14:30:25

// 24 小時制
=TEXT(NOW(), "hh:mm AM/PM")  // 結果：02:30 PM

// 完整日期時間
=TEXT(NOW(), "yyyy-mm-dd hh:mm:ss")  // 結果：2024-11-15 14:30:25
```

---

### 範例 13：條件格式化文字

**情境：** 根據數值顯示不同文字

```excel
// 正數顯示「盈利」，負數顯示「虧損」，零顯示「平衡」
=TEXT(A2, "[>0]盈利 #,##0;[<0]虧損 #,##0;平衡")
```

---

## 🔥 Part 5: 日期函數（90 分鐘）

### DATE / TODAY / NOW

**語法：**
```excel
=DATE(year, month, day)  // 建立日期
=TODAY()  // 今天日期
=NOW()  // 現在日期時間
```

---

### 範例 14：建立日期

```excel
=DATE(2024, 11, 15)  // 結果：2024-11-15

// 動態建立「本月 1 號」
=DATE(YEAR(TODAY()), MONTH(TODAY()), 1)
```

---

### YEAR / MONTH / DAY / WEEKDAY

**語法：**
```excel
=YEAR(date)  // 提取年份
=MONTH(date)  // 提取月份
=DAY(date)  // 提取日期
=WEEKDAY(date, [return_type])  // 星期幾（1=週日，2=週一...）
```

---

### 範例 15：提取日期元件

```excel
=YEAR(TODAY())  // 結果：2024
=MONTH(TODAY())  // 結果：11
=DAY(TODAY())  // 結果：15

// 星期幾（數字）
=WEEKDAY(TODAY())  // 結果：6（週五）

// 星期幾（中文）
=TEXT(TODAY(), "aaaa")  // 結果：星期五
```

---

### EOMONTH - 月底/月初日期

**語法：**
```excel
=EOMONTH(start_date, months)  // End Of Month
```

---

### 範例 16：月初/月底

```excel
// 本月最後一天
=EOMONTH(TODAY(), 0)  // 結果：2024-11-30

// 本月第一天
=EOMONTH(TODAY(), -1) + 1  // 結果：2024-11-01

// 下個月最後一天
=EOMONTH(TODAY(), 1)  // 結果：2024-12-31

// 上個月最後一天
=EOMONTH(TODAY(), -1)  // 結果：2024-10-31
```

---

### DATEDIF - 日期差異計算

**語法：**
```excel
=DATEDIF(start_date, end_date, unit)
```

**unit 參數：**
- `"Y"` = 完整年數
- `"M"` = 完整月數
- `"D"` = 完整天數
- `"YM"` = 月數（不含年）
- `"MD"` = 天數（不含月）
- `"YD"` = 天數（不含年）

---

### 範例 17：計算年齡

```excel
=DATEDIF(A2, TODAY(), "Y")  // 結果：30（歲）

// 完整格式：30 歲 5 個月
=DATEDIF(A2, TODAY(), "Y") & " 歲 " & DATEDIF(A2, TODAY(), "YM") & " 個月"
```

---

### 範例 18：計算天數差

```excel
// 兩個日期相差幾天
=DATEDIF(DATE(2024,1,1), TODAY(), "D")  // 結果：319

// 或直接相減
=TODAY() - DATE(2024,1,1)  // 結果：319
```

---

### 範例 19：計算會員資格

**情境：** 客戶註冊日期，計算「註冊天數」和「會員年資」

```excel
// 註冊天數
=TODAY() - 註冊日期

// 會員年資（完整年數）
=DATEDIF(註冊日期, TODAY(), "Y")

// 分級
=IF(DATEDIF(註冊日期, TODAY(), "Y") >= 3, "資深會員",
   IF(DATEDIF(註冊日期, TODAY(), "M") >= 6, "正式會員", "新會員"))
```

---

### NETWORKDAYS / WORKDAY - 工作日計算

**語法：**
```excel
=NETWORKDAYS(start_date, end_date, [holidays])  // 計算工作日數（排除週末）
=WORKDAY(start_date, days, [holidays])  // 加上 N 個工作日
```

---

### 範例 20：計算交貨日（5 個工作日）

```excel
=WORKDAY(TODAY(), 5)  // 結果：2024-11-22（排除週末）

// 考慮假日
=WORKDAY(TODAY(), 5, 假日清單!A:A)
```

---

### 範例 21：計算實際工作天數

**情境：** 專案從 2024-11-01 到 2024-11-30，實際工作幾天？

```excel
=NETWORKDAYS(DATE(2024,11,1), DATE(2024,11,30))  // 結果：22（天）
```

---

## 🎯 Part 6: 實戰練習（60 分鐘）

### 練習 1：文字提取（15 分鐘）

**資料：** 訂單編號 `ORD20241101001`

**任務 1.1：** 提取年份
```excel
你的公式：
```

**任務 1.2：** 提取年月（202411）
```excel
你的公式：
```

**任務 1.3：** 提取流水號（001）
```excel
你的公式：
```

---

### 練習 2：文字清理（15 分鐘）

**資料：** 電話號碼格式不統一
- `0912-345-678`
- `(02)2345-6789`
- `04 2345 6789`

**任務 2.1：** 移除所有非數字字元
```excel
你的公式：
```

**任務 2.2：** 統一格式為 `0912-345-678`
```excel
你的公式：
提示：先移除，再加上「-」
```

---

### 練習 3：數字格式化（10 分鐘）

**任務 3.1：** 將 1234567 格式化為 `NT$ 1,234,567`
```excel
你的公式：
```

**任務 3.2：** 將 0.1234 格式化為 `12.34%`
```excel
你的公式：
```

---

### 練習 4：日期計算（20 分鐘）

**任務 4.1：** 計算訂單日期到今天相差幾天
```excel
你的公式：
```

**任務 4.2：** 計算客戶年齡（出生年份在客戶主檔）
```excel
你的公式：
```

**任務 4.3：** 根據訂單日期，計算「預計到貨日」（7 個工作日後）
```excel
你的公式：
```

**任務 4.4：** 判斷訂單是「本月」、「上月」還是「其他」
```excel
你的公式：
提示：比較年月
```

---

## 🎯 Part 7: 實戰作業（60 分鐘）

### 作業 1：資料清洗報告

**情境：** 客戶主檔中的資料需要清理

**任務：**

1. **電話號碼標準化**
   - 移除所有非數字字元
   - 統一格式：`0912-345-678`

2. **地址分割**
   - 提取「城市」（前 3 個字）
   - 提取「區域」（「市」後到「區」之間）

3. **Email 驗證**
   - 檢查是否包含 "@"
   - 提取 Email 網域（`@` 之後）

4. **會員資格計算**
   - 計算註冊天數
   - 分級：新會員（<6 個月）、正式會員（6-36 個月）、資深會員（>36 個月）

---

### 作業 2：訂單時效分析

**需求：** 分析訂單處理時效

**計算欄位：**

1. **訂單年月**
   ```excel
   =TEXT(訂單日期, "yyyy-mm")
   ```

2. **訂單星期**
   ```excel
   =TEXT(訂單日期, "aaaa")
   ```

3. **訂單時段**
   ```excel
   =IF(HOUR(訂單時間)<12, "上午", IF(HOUR(訂單時間)<18, "下午", "晚上"))
   ```

4. **距今天數**
   ```excel
   =TODAY() - 訂單日期
   ```

5. **時效狀態**
   - 0-3 天：新訂單
   - 4-7 天：處理中
   - 8-14 天：逾期警告
   - 15+ 天：嚴重逾期

---

### 作業 3：建立格式化報表

**需求：** 將原始資料格式化成專業報表

**範例輸出：**
```
訂單編號：ORD-2024-11-001
客戶姓名：王小明
訂單日期：2024年11月01日（星期五）
訂單金額：NT$ 12,345
訂單狀態：✓ 已完成
```

**公式範例：**
```excel
="訂單編號：" & LEFT(A2,3) & "-" & MID(A2,4,4) & "-" & MID(A2,8,2) & "-" & RIGHT(A2,3) & CHAR(10) &
"客戶姓名：" & B2 & CHAR(10) &
"訂單日期：" & TEXT(C2, "yyyy年mm月dd日") & "（" & TEXT(C2, "aaaa") & "）" & CHAR(10) &
"訂單金額：" & TEXT(D2, "NT$ #,##0") & CHAR(10) &
"訂單狀態：" & IF(E2="已完成", "✓ 已完成", "⏳ " & E2)
```

---

## 📝 Day 4 總結

### ✅ 今天學到的技能

**文字函數：**
- LEFT / RIGHT / MID：提取文字
- FIND / SEARCH：搜尋位置
- SUBSTITUTE / REPLACE：替換文字
- TRIM：移除空格
- TEXT：格式化顯示
- TEXTBEFORE / TEXTAFTER（Excel 365）

**日期函數：**
- DATE / TODAY / NOW：建立日期
- YEAR / MONTH / DAY / WEEKDAY：提取元件
- EOMONTH：月初/月底
- DATEDIF：日期差異
- NETWORKDAYS / WORKDAY：工作日計算

**實務應用：**
- 資料清洗與標準化
- 格式化報表輸出
- 日期計算與分析

### 🎓 Excel → Python 對照

| Excel 功能 | Python pandas 對應 |
|-----------|-------------------|
| `=LEFT(A2, 3)` | `df['A'].str[:3]` |
| `=RIGHT(A2, 3)` | `df['A'].str[-3:]` |
| `=SUBSTITUTE(A2, "X", "Y")` | `df['A'].str.replace('X', 'Y')` |
| `=TEXT(A2, "#,##0")` | `df['A'].apply(lambda x: f'{x:,}')` |
| `=YEAR(A2)` | `df['A'].dt.year` |
| `=DATEDIF(A2, TODAY(), "Y")` | `(pd.Timestamp.now() - df['A']).dt.days // 365` |

### 🚀 明天預告：LET() & LAMBDA()

明天我們將學習 Excel 最強大的進階函數：
- LET()：定義變數，大幅簡化複雜公式
- LAMBDA()：建立自訂函數
- MAP() / REDUCE()：函數式編程

---

**🎊 恭喜完成 Day 4！你已經掌握了資料清洗的核心技能！**
