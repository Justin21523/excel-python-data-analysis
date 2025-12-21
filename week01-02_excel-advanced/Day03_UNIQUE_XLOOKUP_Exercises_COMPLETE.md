# Day 3: UNIQUE & XLOOKUP 函數完整實戰練習

**學習時間：** 4-5 小時
**資料檔案：** case01_realistic_sales_data.xlsx + case02_realistic_inventory.xlsx
**前置知識：** Day 1 FILTER, Day 2 SORT

---

## 📋 學習目標

完成本日練習後，你將能夠：

- ✅ 使用 UNIQUE 去除重複值
- ✅ 理解 exactly_once 參數的應用
- ✅ 使用 SEQUENCE 生成數列
- ✅ 完全掌握 XLOOKUP 取代 VLOOKUP
- ✅ 處理查找錯誤與預設值
- ✅ 實現嵌套查找
- ✅ 建立產品查詢系統

---

## 🎯 三大函數總覽

### **UNIQUE - 去重函數**
```excel
=UNIQUE(array, [by_col], [exactly_once])
```
**用途：** 取得不重複的值

### **SEQUENCE - 數列生成**
```excel
=SEQUENCE(rows, [columns], [start], [step])
```
**用途：** 生成連續數字序列

### **XLOOKUP - 強大查找**
```excel
=XLOOKUP(lookup_value, lookup_array, return_array, [if_not_found], [match_mode], [search_mode])
```
**用途：** 完全取代 VLOOKUP/HLOOKUP

---

## 📊 Part 1: UNIQUE 函數實戰（60 分鐘）

### **練習 1：基礎去重**

**題目：** 列出所有不重複的產品類別

**Excel 公式：**
```excel
=UNIQUE(訂單明細!N2:N1001)
```

**Python 對照：**
```python
df['產品類別'].unique()
```

**預期結果：**
```
電腦周邊
手機配件
家電用品
美妝保養
服飾配件
運動用品
書籍文具
食品飲料
```

**應用場景：**
- 建立篩選器的選項清單
- 快速了解資料中有哪些類別
- 建立下拉選單

---

### **練習 2：去重 + 排序**

**題目：** 列出所有不重複的產品類別，並按字母順序排列

**Excel 公式：**
```excel
=SORT(UNIQUE(訂單明細!N2:N1001))
```

**Python 對照：**
```python
sorted(df['產品類別'].unique())
# 或
df['產品類別'].unique().sort()
```

**組合技巧：**
- UNIQUE 先去重
- SORT 再排序
- 由內而外思考

---

### **練習 3：多欄位去重**

**題目：** 列出所有不重複的「品牌+產品類別」組合

**Excel 公式：**
```excel
=UNIQUE(訂單明細!M2:N1001)
```

**參數說明：**
- 選擇多個欄位（M:N = 品牌+類別）
- UNIQUE 會把整列當作一個組合

**Python 對照：**
```python
df[['品牌', '產品類別']].drop_duplicates()
```

**預期結果：**
```
品牌          產品類別
--------     --------
Apple        手機配件
Logitech     電腦周邊
Samsung      家電用品
...
```

---

### **練習 4：計算不重複值的數量**

**題目：** 計算有多少個不重複的客戶

**Excel 公式：**
```excel
=COUNTA(UNIQUE(訂單明細!C2:C1001))
```

**或使用組合：**
```excel
=ROWS(UNIQUE(訂單明細!C2:C1001))
```

**Python 對照：**
```python
df['客戶ID'].nunique()
```

**公式解析：**
- UNIQUE 先取得不重複客戶列表
- COUNTA 或 ROWS 計算有幾個
- COUNTA 計算非空值個數
- ROWS 計算列數

---

### **練習 5：exactly_once 參數**

**題目：** 找出「只購買過一次」的客戶（單次購買客戶）

**Excel 公式：**
```excel
=UNIQUE(訂單明細!C2:C1001, , TRUE)
```

**參數說明：**
- 第一個 `,` - 跳過 by_col 參數（預設 FALSE）
- 第二個 `TRUE` - exactly_once 參數
- TRUE = 只返回「恰好出現一次」的值

**Python 對照：**
```python
df['客戶ID'].value_counts()[df['客戶ID'].value_counts() == 1].index
# 或更簡潔
df.groupby('客戶ID').filter(lambda x: len(x) == 1)['客戶ID'].unique()
```

**預期結果：**
- 只顯示購買次數 = 1 的客戶ID
- 這些是「新客」或「一次性客戶」
- 可用於流失分析

**應用場景：**
- 找出單次購買客戶（可能流失）
- 識別新客戶
- 找出孤立值（異常檢測）

---

### **練習 6：建立動態下拉選單**

**題目：** 建立一個動態下拉選單，自動包含所有產品類別

**步驟 1：在某個儲存格（例如 Z1）輸入：**
```excel
=SORT(UNIQUE(訂單明細!N2:N1001))
```

**步驟 2：為其他儲存格建立資料驗證：**
- 選取目標儲存格
- 資料 → 資料驗證 → 允許：清單
- 來源：`=Z1#`（# 代表溢出範圍）

**優點：**
- 資料更新後，下拉選單自動更新
- 不需要手動維護清單
- 始終保持最新

**Python 概念對照：**
```python
# 動態取得類別清單
categories = df['產品類別'].unique().tolist()
# 用於網頁下拉選單或 GUI
```

---

## 📊 Part 2: SEQUENCE 函數實戰（45 分鐘）

### **練習 7：生成基礎數列**

**題目：** 生成 1 到 100 的數字序列

**Excel 公式：**
```excel
=SEQUENCE(100)
```

**Python 對照：**
```python
list(range(1, 101))
# 或
np.arange(1, 101)
```

**預期結果：**
```
1
2
3
...
100
```

---

### **練習 8：生成偶數序列**

**題目：** 生成 2, 4, 6, 8...到 100 的偶數序列

**Excel 公式：**
```excel
=SEQUENCE(50, 1, 2, 2)
```

**參數說明：**
- `50` - 生成 50 個數字（rows）
- `1` - 1 欄（columns）
- `2` - 起始值
- `2` - 每次加 2（step）

**Python 對照：**
```python
list(range(2, 101, 2))
# 或
np.arange(2, 101, 2)
```

---

### **練習 9：生成日期序列**

**題目：** 生成 2024 年 11 月的所有日期

**Excel 公式：**
```excel
=SEQUENCE(30, 1, DATE(2024,11,1), 1)
```

**或動態計算天數：**
```excel
=LET(
    年, 2024,
    月, 11,
    開始日期, DATE(年, 月, 1),
    天數, DAY(EOMONTH(開始日期, 0)),
    SEQUENCE(天數, 1, 開始日期, 1)
)
```

**Python 對照：**
```python
import pandas as pd
pd.date_range('2024-11-01', '2024-11-30')
```

**應用場景：**
- 建立日期軸
- 檢查缺失日期
- 建立日曆系統

---

### **練習 10：生成排名序號**

**題目：** 為排序後的訂單加上排名序號（1, 2, 3...）

**Excel 公式：**
```excel
=HSTACK(
    SEQUENCE(ROWS(訂單明細!A2:A1001)),
    SORT(訂單明細!A2:AN1001, 28, -1)
)
```

**公式解析：**
- `SEQUENCE(ROWS(...))` - 生成 1 到 N 的序號
- `SORT(...)` - 排序資料
- `HSTACK(...)` - 水平合併（序號在左，資料在右）

**Python 對照：**
```python
df_sorted = df.sort_values('訂單總額', ascending=False).reset_index(drop=True)
df_sorted.index = df_sorted.index + 1  # 從 1 開始
```

**預期結果：**
```
排名  訂單編號    ...  訂單總額
----  ----------      --------
1     ORD...          25,000
2     ORD...          22,000
3     ORD...          20,500
...
```

---

## 📊 Part 3: XLOOKUP 函數實戰（120 分鐘）

### **XLOOKUP vs VLOOKUP 對比**

| 特性 | VLOOKUP | XLOOKUP |
|------|---------|---------|
| 查找方向 | 只能向右 | 任意方向 |
| 預設值 | 不支援 | 支援 if_not_found |
| 近似匹配 | 複雜 | 簡單明確 |
| 多欄返回 | 不支援 | 原生支援 |
| 反向查找 | 不支援 | 支援 |
| 語法複雜度 | 中等 | 簡單直觀 |

---

### **練習 11：基礎查找**

**題目：** 根據客戶ID查找客戶姓名

**準備工作：** 使用 case01 中的「客戶主檔」工作表

**VLOOKUP 舊寫法：**
```excel
=VLOOKUP(A2, 客戶主檔!A:B, 2, FALSE)
```

**XLOOKUP 新寫法：**
```excel
=XLOOKUP(A2, 客戶主檔!A:A, 客戶主檔!B:B)
```

**Python 對照：**
```python
# 方法 1：merge
df.merge(customers[['客戶ID', '客戶姓名']], on='客戶ID', how='left')

# 方法 2：map
df['客戶姓名'] = df['客戶ID'].map(customers.set_index('客戶ID')['客戶姓名'])
```

**XLOOKUP 優點：**
- 不需要計算欄位位置
- 語法更直觀
- 可以向左查找

---

### **練習 12：查找不到時的預設值**

**題目：** 查找客戶姓名，如果找不到顯示「客戶不存在」

**Excel 公式：**
```excel
=XLOOKUP(
    A2,
    客戶主檔!A:A,
    客戶主檔!B:B,
    "客戶不存在"
)
```

**參數說明：**
- 第 4 個參數 `if_not_found` - 找不到時返回的值

**Python 對照：**
```python
df['客戶姓名'] = df['客戶ID'].map(
    customers.set_index('客戶ID')['客戶姓名']
).fillna('客戶不存在')
```

---

### **練習 13：返回多個欄位**

**題目：** 根據客戶ID查找「姓名、電話、地址」三個欄位

**Excel 公式：**
```excel
=XLOOKUP(
    A2,
    客戶主檔!A:A,
    客戶主檔!B:D
)
```

**這會一次返回 3 個欄位！**

**Python 對照：**
```python
df.merge(
    customers[['客戶ID', '客戶姓名', '客戶電話', '客戶地址']],
    on='客戶ID',
    how='left'
)
```

**預期結果：**
- 橫向溢出 3 個儲存格
- 自動顯示姓名、電話、地址

---

### **練習 14：反向查找**

**題目：** 根據產品名稱（在 O 欄）查找產品 SKU（在 L 欄）

**VLOOKUP 無法做到！** 因為 SKU 在產品名稱「左邊」

**XLOOKUP 可以：**
```excel
=XLOOKUP(
    "iPhone 15 Pro",
    產品主檔!B:B,
    產品主檔!A:A
)
```

**Python 對照：**
```python
products[products['產品名稱'] == 'iPhone 15 Pro']['產品SKU'].values[0]
# 或
products.set_index('產品名稱').loc['iPhone 15 Pro', '產品SKU']
```

---

### **練習 15：近似匹配（範圍查找）**

**題目：** 根據訂單金額判斷折扣等級

| 金額範圍 | 折扣 |
|---------|------|
| 0-1,000 | 0% |
| 1,000-5,000 | 5% |
| 5,000-10,000 | 10% |
| 10,000+ | 15% |

**Excel 公式：**
```excel
=XLOOKUP(
    AB2,
    {0, 1000, 5000, 10000},
    {"0%", "5%", "10%", "15%"},
    ,
    1
)
```

**參數說明：**
- `AB2` - 訂單金額
- `{0, 1000, 5000, 10000}` - 門檻陣列
- `{"0%", "5%", "10%", "15%"}` - 對應折扣
- `,` - 跳過 if_not_found
- `1` - match_mode = 1（精確匹配或次小值）

**match_mode 說明：**
- `0` - 精確匹配（預設）
- `1` - 精確或次小值（適合範圍查找）
- `-1` - 精確或次大值
- `2` - 萬用字元匹配

**Python 對照：**
```python
def get_discount(amount):
    if amount < 1000:
        return "0%"
    elif amount < 5000:
        return "5%"
    elif amount < 10000:
        return "10%"
    else:
        return "15%"

df['折扣'] = df['訂單總額'].apply(get_discount)

# 或使用 pd.cut
df['折扣'] = pd.cut(
    df['訂單總額'],
    bins=[0, 1000, 5000, 10000, float('inf')],
    labels=["0%", "5%", "10%", "15%"]
)
```

---

### **練習 16：從後往前查找**

**題目：** 查找客戶「最後一筆」訂單的日期

**Excel 公式：**
```excel
=XLOOKUP(
    C2,
    訂單明細!C:C,
    訂單明細!B:B,
    ,
    0,
    -1
)
```

**參數說明：**
- `,` - 跳過 if_not_found
- `0` - 精確匹配
- `-1` - search_mode = -1（從後往前搜尋）

**search_mode 說明：**
- `1` - 從頭到尾（預設）
- `-1` - 從尾到頭（找最後一個匹配）
- `2` - 二分搜尋（升序排列）
- `-2` - 二分搜尋（降序排列）

**Python 對照：**
```python
df.groupby('客戶ID')['訂單日期'].last()
```

---

### **練習 17：嵌套 XLOOKUP**

**題目：** 兩步查找
1. 根據訂單編號查找客戶ID
2. 根據客戶ID查找客戶姓名

**Excel 公式：**
```excel
=XLOOKUP(
    XLOOKUP(A2, 訂單明細!A:A, 訂單明細!C:C),
    客戶主檔!A:A,
    客戶主檔!B:B
)
```

**公式解析：**
- 內層 XLOOKUP：訂單編號 → 客戶ID
- 外層 XLOOKUP：客戶ID → 客戶姓名

**Python 對照：**
```python
# 方法 1：兩次 merge
df.merge(orders[['訂單編號', '客戶ID']], on='訂單編號') \
  .merge(customers[['客戶ID', '客戶姓名']], on='客戶ID')

# 方法 2：鏈式查找
order_to_customer = orders.set_index('訂單編號')['客戶ID']
customer_to_name = customers.set_index('客戶ID')['客戶姓名']
df['客戶姓名'] = df['訂單編號'].map(order_to_customer).map(customer_to_name)
```

---

## 🎯 實戰專案：產品查詢與庫存管理系統（90 分鐘）

**需求說明：**
建立一個完整的產品查詢系統，整合訂單資料和庫存資料

**功能要求：**
1. 輸入產品 SKU 或名稱
2. 自動顯示產品完整資訊
3. 顯示庫存狀態
4. 顯示銷售統計
5. 庫存警示功能

---

### **步驟 1：準備資料**

**使用兩個檔案：**
- case01_realistic_sales_data.xlsx（訂單資料）
- case02_realistic_inventory.xlsx（庫存資料）

**建立新工作表「產品查詢系統」**

---

### **步驟 2：建立查詢介面**

**A. 查詢輸入區：**

| 項目 | 儲存格 | 說明 |
|------|--------|------|
| 產品 SKU | B2 | 輸入查詢的 SKU |

**B. 產品資訊顯示區（從 A5 開始）：**

```excel
// A5-B11：產品基本資訊
產品SKU:     =B2
產品名稱:    =XLOOKUP(B2, 產品主檔!A:A, 產品主檔!B:B, "查無此產品")
品牌:       =XLOOKUP(B2, 產品主檔!A:A, 產品主檔!C:C)
類別:       =XLOOKUP(B2, 產品主檔!A:A, 產品主檔!D:D)
單價:       =XLOOKUP(B2, 產品主檔!A:A, 產品主檔!E:E)
規格:       =XLOOKUP(B2, 產品主檔!A:A, 產品主檔!F:F)
```

---

### **步驟 3：庫存資訊查詢**

```excel
// A13-B18：庫存資訊
當前庫存:    =XLOOKUP(B2, 庫存明細!A:A, 庫存明細!B:B, 0)
安全庫存:    =XLOOKUP(B2, 庫存明細!A:A, 庫存明細!C:C, 0)
補貨中數量:  =XLOOKUP(B2, 庫存明細!A:A, 庫存明細!D:D, 0)
庫存狀態:    =IF(B13<B14, "⚠️ 低於安全庫存", "✅ 庫存正常")
```

---

### **步驟 4：銷售統計**

```excel
// A20-B25：銷售統計
總銷售數量:  =SUMIF(訂單明細!L:L, B2, 訂單明細!Q:Q)
總銷售金額:  =SUMIF(訂單明細!L:L, B2, 訂單明細!AB:AB)
平均客單價:  =B21/COUNTIF(訂單明細!L:L, B2)
最近銷售日:  =XLOOKUP(B2, 訂單明細!L:L, 訂單明細!B:B, "無銷售記錄", 0, -1)
銷售排名:    =RANK(B21, SUMIF(訂單明細!L:L, UNIQUE(訂單明細!L:L), 訂單明細!AB:AB))
```

---

### **步驟 5：建立產品下拉選單**

**在 B2 建立資料驗證：**
```excel
// 來源
=SORT(UNIQUE(產品主檔!A2:A1000))
```

**或建立「搜尋建議」功能：**
```excel
// 在 B1 輸入部分產品名稱，B2 顯示匹配的 SKU
=XLOOKUP(
    TRUE,
    ISNUMBER(SEARCH(B1, 產品主檔!B:B)),
    產品主檔!A:A,
    "找不到匹配產品"
)
```

---

### **步驟 6：銷售明細列表**

**顯示該產品的所有訂單：**
```excel
// 儲存格 A27
=FILTER(
    訂單明細!A:AN,
    訂單明細!L:L=B2,
    "該產品無銷售記錄"
)
```

**或只顯示關鍵欄位：**
```excel
=FILTER(
    CHOOSECOLS(訂單明細!A:AN, 1, 2, 3, 15, 17, 28),
    訂單明細!L:L=B2,
    "該產品無銷售記錄"
)
```

---

### **步驟 7：視覺化呈現**

**A. 條件格式：**

**庫存狀態顏色：**
- 選取 B17（庫存狀態）
- 條件格式 → 包含文字
- 包含「低於」→ 紅色背景
- 包含「正常」→ 綠色背景

**B. 迷你圖：**

**銷售趨勢（如果有每日資料）：**
```excel
// 插入 → 走勢圖
// 資料範圍：該產品每日銷售額
```

---

### **步驟 8：進階功能（選做）**

**A. 多產品對比：**

建立表格比較多個產品的庫存和銷售情況。

**B. 自動補貨建議：**

```excel
// 建議補貨量
=IF(
    當前庫存 < 安全庫存,
    (安全庫存 * 2) - 當前庫存,
    0
)
```

**C. 庫存週轉率：**

```excel
// 週轉率 = 銷售數量 / 平均庫存
=總銷售數量 / ((當前庫存 + 補貨中數量) / 2)
```

---

## 📊 專案評估標準

### **基礎功能（60 分）**
- [ ] 能正確查詢產品資訊
- [ ] 能顯示庫存狀態
- [ ] 能計算銷售統計
- [ ] 錯誤處理（找不到產品時的提示）

### **進階功能（30 分）**
- [ ] 產品下拉選單或搜尋功能
- [ ] 銷售明細列表
- [ ] 庫存警示
- [ ] 使用 LET 組織公式

### **視覺呈現（10 分）**
- [ ] 條件格式美化
- [ ] 清晰的介面設計
- [ ] 圖表或迷你圖

---

## 🎓 學習檢核清單

- [ ] 能使用 UNIQUE 去除重複值
- [ ] 理解 exactly_once 參數
- [ ] 能生成各種 SEQUENCE 數列
- [ ] 掌握 XLOOKUP 基本查找
- [ ] 能設定 if_not_found 預設值
- [ ] 能返回多個欄位
- [ ] 理解 match_mode 的 4 種模式
- [ ] 理解 search_mode 的 4 種模式
- [ ] 能實現嵌套查找
- [ ] 建立完整的查詢系統

---

## 🚀 下一步

**Day 4 預告：TEXT & DATE 函數**
- 文字提取與清洗
- 20+ TEXT 格式化範例
- 日期計算與工作日
- 資料清洗實戰

**準備好了嗎？開始 Day 3 實戰！** 💪
