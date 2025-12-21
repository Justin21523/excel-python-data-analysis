# 🎯 Exercise 01: MultiIndex 實戰練習（12 題）

> **課程：** Week 3 - MultiIndex & 複雜 GroupBy
> **資料集：** Olist 巴西電商資料
> **時間分配：** 基礎 5-10 分鐘/題 | 進階 10-20 分鐘/題 | 挑戰 20-30 分鐘/題

---

## 📊 難度分級

- 🟢 **基礎（1-4 題）：** 建立與基本操作
- 🟡 **進階（5-8 題）：** 切片與轉換
- 🔴 **挑戰（9-12 題）：** 綜合應用與報表生成

---

## 🟢 基礎題（1-4 題）

### 🟢 題目 1：建立地區 × 產品類別 MultiIndex

**情境：**
你是 Olist 的資料分析師，需要建立一個「客戶州別 × 產品類別」的雙層索引，以便快速分析不同地區的產品類別表現。

**任務：**
1. 載入訂單（orders）、訂單明細（order_items）、產品（products）、客戶（customers）資料
2. 合併資料表，保留所有必要欄位
3. 使用 `set_index()` 建立「客戶州別」和「產品類別」的雙層索引
4. 計算每個組合的訂單總額（price 欄位加總）
5. 查看前 10 筆資料並檢視索引結構

**提示：**
- 使用 `pd.merge()` 逐步合併多張表
- 使用 `df.groupby(['col1', 'col2'])['value'].sum()` 會自動建立 MultiIndex
- 使用 `index.names` 和 `index.nlevels` 檢視索引結構

**預期輸出：**
```
customer_state  product_category_name
AC              beleza_saude             2847.89
                cama_mesa_banho          1234.56
SP              eletronicos             45678.90
                esporte_lazer           12345.67
RJ              moveis_decoracao        23456.78
...
Name: price, dtype: float64

索引層級：['customer_state', 'product_category_name']
索引層數：2
```

**Excel 對照：**
- Excel 樞紐表：列標籤依序放入「州別」→「產品類別」
- 值：價格（加總）
- pandas：`groupby(['customer_state', 'product_category_name'])['price'].sum()`

---

### 🟢 題目 2：使用 from_tuples 建立自訂 MultiIndex

**情境：**
行銷部門提供了一份重點推廣的「地區 × 類別」組合清單，你需要建立對應的 MultiIndex 來快速查詢這些組合的銷售數據。

**任務：**
1. 建立一個包含以下組合的 tuple 清單：
   - ('SP', 'eletronicos')
   - ('SP', 'moveis_decoracao')
   - ('RJ', 'beleza_saude')
   - ('RJ', 'esporte_lazer')
   - ('MG', 'cama_mesa_banho')
2. 使用 `pd.MultiIndex.from_tuples()` 建立 MultiIndex
3. 為每個組合建立假設的銷售數據（可用隨機數）
4. 建立 Series，使用上述 MultiIndex 作為索引
5. 驗證索引結構並輸出完整資料

**提示：**
- 使用 `tuples = [('A', 'X'), ('A', 'Y'), ...]` 建立清單
- 使用 `pd.MultiIndex.from_tuples(tuples, names=['level1', 'level2'])`
- 使用 `pd.Series(data, index=multi_index)` 建立 Series

**預期輸出：**
```
SP  eletronicos         125,234.56
    moveis_decoracao     98,765.43
RJ  beleza_saude         87,654.32
    esporte_lazer        76,543.21
MG  cama_mesa_banho      65,432.10
dtype: float64
```

**Excel 對照：**
- Excel：手動建立兩欄（州別、類別），再輸入數值
- pandas：使用 `from_tuples()` 直接建立階層式索引

---

### 🟢 題目 3：MultiIndex 基本切片 - loc 單層選取

**情境：**
管理層想查看「聖保羅州（SP）」所有產品類別的銷售表現。

**任務：**
1. 使用題目 1 的結果（州別 × 類別的 MultiIndex）
2. 使用 `.loc['SP']` 選取聖保羅州的所有資料
3. 對結果進行降序排序
4. 輸出 Top 10 產品類別
5. 計算 SP 州的總銷售額與平均銷售額

**提示：**
- `series.loc['SP']` 會返回該州的所有類別
- 使用 `.sort_values(ascending=False)` 降序排序
- 使用 `.sum()` 和 `.mean()` 計算統計量

**預期輸出：**
```
product_category_name
eletronicos             45,678.90
cama_mesa_banho         34,567.89
beleza_saude            23,456.78
...

SP 州總銷售額：$1,234,567.89
SP 州平均銷售額：$12,345.67
```

**Excel 對照：**
- Excel：在樞紐表篩選器選擇「SP」
- pandas：`df.loc['SP']`

---

### 🟢 題目 4：MultiIndex 雙層切片 - loc 精確選取

**情境：**
產品經理想快速查詢特定「州別 × 類別」組合的銷售額。

**任務：**
1. 使用 `.loc[('SP', 'eletronicos')]` 查詢 SP 州電子產品銷售額
2. 查詢 RJ 州所有美容保健產品：`.loc[('RJ', 'beleza_saude')]`
3. 一次查詢多個組合（SP 電子產品 + RJ 家具）
4. 建立一個函數 `query_sales(state, category)` 方便快速查詢
5. 測試查詢 5 個不同組合

**提示：**
- 雙層切片：`series.loc[('level1_value', 'level2_value')]`
- 多個選取：`series.loc[[('SP', 'eletronicos'), ('RJ', 'moveis_decoracao')]]`
- 函數定義：`def query_sales(state, category): return series.loc[(state, category)]`

**預期輸出：**
```
查詢結果：
('SP', 'eletronicos'): $45,678.90
('RJ', 'beleza_saude'): $23,456.78

批次查詢：
SP  eletronicos         45,678.90
RJ  moveis_decoracao    34,567.89
dtype: float64
```

**Excel 對照：**
- Excel：同時篩選州別 = "SP" AND 類別 = "eletronicos"
- pandas：`df.loc[('SP', 'eletronicos')]`

---

## 🟡 進階題（5-8 題）

### 🟡 題目 5：IndexSlice 進階切片 - 範圍選取

**情境：**
分析團隊需要比較東南部重點州（RJ, SP, MG）的電子產品與家具類別銷售表現。

**任務：**
1. 匯入 `pd.IndexSlice`：`idx = pd.IndexSlice`
2. 選取 RJ, SP, MG 三州的所有類別資料
3. 選取所有州的「eletronicos」和「moveis_decoracao」類別
4. 組合查詢：RJ/SP 兩州的電子產品與家具
5. 將結果轉換為 DataFrame 並計算各州佔比

**提示：**
- `idx = pd.IndexSlice`
- 選取多個 level0：`series.loc[idx[['RJ', 'SP', 'MG'], :]]`
- 選取多個 level1：`series.loc[idx[:, ['eletronicos', 'moveis_decoracao']]]`
- 組合：`series.loc[idx[['RJ', 'SP'], ['eletronicos', 'moveis_decoracao']]]`

**預期輸出：**
```
customer_state  product_category_name
RJ              eletronicos             34,567.89
                moveis_decoracao        23,456.78
SP              eletronicos             45,678.90
                moveis_decoracao        38,765.43
dtype: float64

各州佔比：
RJ: 40.5%
SP: 59.5%
```

**Excel 對照：**
- Excel：在樞紐表篩選器手動勾選多個州別與類別
- pandas：使用 `IndexSlice` 一次選取多個層級值

---

### 🟡 題目 6：xs (cross-section) 跨層選取

**情境：**
快速報表需要提取所有州的「電子產品」類別數據，不關心州別分組。

**任務：**
1. 使用 `.xs('eletronicos', level='product_category_name')` 選取所有州的電子產品
2. 同樣方式選取「beleza_saude」類別
3. 比較兩個類別在不同州的銷售差異
4. 使用 `.xs('SP', level='customer_state')` 反向選取 SP 州所有類別
5. 計算電子產品在所有州的總銷售額佔比

**提示：**
- `series.xs('value', level='level_name')` 跨層選取
- `level=0` 或 `level='customer_state'` 指定層級
- 可以使用 `level=1` 選取第二層

**預期輸出：**
```
電子產品各州銷售：
customer_state
AC     2,345.67
AL     3,456.78
SP    45,678.90
RJ    34,567.89
...

電子產品總銷售額：$234,567.89
佔全部類別比例：23.4%
```

**Excel 對照：**
- Excel：在樞紐表篩選「產品類別 = eletronicos」，保留所有州別
- pandas：`df.xs('eletronicos', level=1)`

---

### 🟡 題目 7：stack / unstack 轉換

**情境：**
報表需要將「州別為列、類別為欄」的交叉表格式呈現，方便橫向比較。

**任務：**
1. 將題目 1 的 MultiIndex Series 轉換為 DataFrame（使用 `to_frame()`）
2. 使用 `unstack()` 將「產品類別」從索引轉為欄位
3. 填補 NaN 值為 0
4. 計算每個州別的總銷售額（新增一欄 `Total`）
5. 使用 `stack()` 轉回長格式

**提示：**
- `series.unstack()` 或 `series.unstack(level=1)` 將第二層索引轉為欄位
- `df.fillna(0)` 填補缺失值
- `df['Total'] = df.sum(axis=1)` 計算列總和
- `df.stack()` 轉回長格式

**預期輸出（unstack 後）：**
```
product_category_name  eletronicos  beleza_saude  moveis_decoracao  Total
customer_state
SP                      45,678.90     23,456.78        38,765.43  107,901.11
RJ                      34,567.89     18,765.43        23,456.78   76,790.10
MG                      12,345.67      9,876.54        15,432.10   37,654.31
...
```

**Excel 對照：**
- Excel：樞紐表中將「類別」拖曳到「欄標籤」區域
- pandas：使用 `unstack()` 轉換

---

### 🟡 題目 8：swaplevel 與 sort_index

**情境：**
原本的「州別 × 類別」索引需要改為「類別 × 州別」，以便按類別分析各州表現。

**任務：**
1. 使用 `.swaplevel()` 交換 MultiIndex 的兩層順序
2. 使用 `sort_index()` 重新排序（先按類別、再按州別）
3. 選取「eletronicos」類別的所有州別資料
4. 找出每個類別的 Top 3 州別
5. 比較 swaplevel 前後的切片差異

**提示：**
- `series.swaplevel()` 交換相鄰兩層
- `series.swaplevel(0, 1)` 或 `series.swaplevel('level1', 'level2')` 指定交換
- `series.sort_index()` 依索引排序
- 交換後：`series.loc['eletronicos']` 會返回所有州的電子產品

**預期輸出：**
```
交換前：
customer_state  product_category_name
SP              eletronicos             45,678.90
                beleza_saude            23,456.78
...

交換後：
product_category_name  customer_state
beleza_saude           RJ                18,765.43
                       SP                23,456.78
eletronicos            MG                12,345.67
                       RJ                34,567.89
                       SP                45,678.90
...

eletronicos 類別 Top 3 州：
1. SP: $45,678.90
2. RJ: $34,567.89
3. MG: $12,345.67
```

**Excel 對照：**
- Excel：在樞紐表中拖曳調整「列標籤」順序
- pandas：使用 `swaplevel()` 交換層級

---

## 🔴 挑戰題（9-12 題）

### 🔴 題目 9：三層 MultiIndex - 時間 × 地區 × 類別

**情境：**
管理層要求建立「年月 × 州別 × 產品類別」三層索引，追蹤各地區產品類別的月度銷售趨勢。

**任務：**
1. 從訂單資料中提取年月資訊（`order_purchase_timestamp`）
2. 建立「年月 × 州別 × 產品類別」三層 MultiIndex
3. 計算每個組合的訂單總額與訂單數量
4. 使用 IndexSlice 查詢 2018 年所有資料
5. 找出 2018 年 1 月，SP 州的 Top 5 產品類別
6. 計算每個類別的月均成長率（MoM Growth Rate）

**提示：**
- `pd.to_datetime(df['timestamp']).dt.to_period('M')` 轉換為年月
- `groupby(['year_month', 'state', 'category'])` 建立三層索引
- 使用 `.agg(['sum', 'count'])` 計算多個統計量
- IndexSlice：`idx = pd.IndexSlice; df.loc[idx['2018', :, :], :]`

**預期輸出：**
```
year_month  customer_state  product_category_name
2018-01     SP              eletronicos             (sum: 45,678.90, count: 234)
                            cama_mesa_banho         (sum: 34,567.89, count: 189)
            RJ              beleza_saude            (sum: 23,456.78, count: 156)
2018-02     SP              eletronicos             (sum: 48,765.43, count: 245)
...

2018-01 SP 州 Top 5：
1. eletronicos: $45,678.90
2. cama_mesa_banho: $34,567.89
3. beleza_saude: $23,456.78
4. esporte_lazer: $18,765.43
5. moveis_decoracao: $15,432.10

eletronicos 月均成長率：6.8%
```

**Excel 對照：**
- Excel：樞紐表列標籤依序放入「年月」→「州別」→「類別」
- pandas：`groupby(['year_month', 'state', 'category'])`

---

### 🔴 題目 10：MultiIndex 與 GroupBy 結合 - 複雜聚合

**情境：**
財務部門需要一份詳細報表，顯示每個「州別 × 類別」組合的銷售統計（總額、平均、中位數、訂單數）。

**任務：**
1. 建立「州別 × 類別」MultiIndex
2. 使用 `.agg()` 計算多個統計量：
   - 總銷售額（sum）
   - 平均訂單金額（mean）
   - 中位數（median）
   - 訂單數量（count）
   - 最大單筆訂單（max）
3. 將結果轉換為 DataFrame，欄位命名為中文
4. 找出「高價值組合」（總額 > 50000 且訂單數 > 100）
5. 計算每個組合的「單位訂單價值」（總額 / 訂單數）並排序

**提示：**
- `df.groupby(['state', 'category'])['price'].agg(['sum', 'mean', 'median', 'count', 'max'])`
- 使用 `.rename(columns={...})` 重命名欄位
- 使用 `.query()` 或布林索引篩選

**預期輸出：**
```
                                        總銷售額    平均金額   中位數   訂單數   最大單筆
customer_state  product_category_name
SP              eletronicos           125,678.90  537.26  489.90   234    4,567.89
                cama_mesa_banho        98,765.43  522.81  456.78   189    3,456.78
RJ              beleza_saude           87,654.32  561.89  512.34   156    2,987.65
...

高價值組合（5 個）：
SP × eletronicos: 總額 $125,678.90, 訂單數 234, 單位價值 $537.26
SP × cama_mesa_banho: 總額 $98,765.43, 訂單數 189, 單位價值 $522.81
...
```

**Excel 對照：**
- Excel：樞紐表值區域新增多個欄位（加總、平均、計數等）
- pandas：使用 `.agg([...])` 一次計算多個統計量

---

### 🔴 題目 11：MultiIndex 報表生成 - 分層小計與總計

**情境：**
月度報表需要顯示「州別 × 類別」銷售額，並在每個州別下方顯示小計，最後顯示總計。

**任務：**
1. 建立「州別 × 類別」MultiIndex 銷售報表
2. 計算每個州別的小計（使用 `groupby(level=0).sum()`）
3. 將小計加入原始 Series（索引為 `(state, 'Subtotal')`）
4. 計算總計並加入（索引為 `('TOTAL', '')`）
5. 排序並輸出完整報表
6. 匯出為 Excel 格式（使用 `to_excel()`）

**提示：**
- 原始資料：`original = df.groupby(['state', 'category'])['price'].sum()`
- 小計：`subtotals = df.groupby('state')['price'].sum()`
- 合併：`pd.concat([original, subtotals])` 並調整索引格式
- 使用 `.sort_index()` 排序

**預期輸出：**
```
customer_state  product_category_name    金額
AC              beleza_saude          2,847.89
                cama_mesa_banho       1,234.56
                esporte_lazer           987.65
                小計                  5,070.10
AL              eletronicos          12,345.67
                moveis_decoracao      8,765.43
                小計                 21,111.10
...
TOTAL                             1,234,567.89

✅ 報表已儲存至：sales_report_by_state_category.xlsx
```

**Excel 對照：**
- Excel：樞紐表設計 → 顯示小計與總計
- pandas：手動計算並合併多個 Series

---

### 🔴 題目 12：綜合挑戰 - 動態 MultiIndex 儀表板

**情境：**
建立一個互動式分析函數，可以根據使用者輸入的維度動態建立 MultiIndex 並進行分析。

**任務：**
1. 建立函數 `create_sales_dashboard(dimensions, metric='price', agg_func='sum')`
   - `dimensions`：list of str，例如 `['customer_state', 'product_category_name']`
   - `metric`：要分析的數值欄位
   - `agg_func`：聚合函數（'sum', 'mean', 'count' 等）
2. 函數內部自動合併所需資料表
3. 建立對應的 MultiIndex
4. 回傳分析結果與前 20 筆資料
5. 測試以下組合：
   - 一維：`['customer_state']`
   - 二維：`['customer_state', 'product_category_name']`
   - 三維：`['customer_state', 'product_category_name', 'seller_state']`（客戶州別 × 產品類別 × 賣家州別）

**提示：**
```python
def create_sales_dashboard(dimensions, metric='price', agg_func='sum'):
    # 1. 載入並合併資料
    # 2. 檢查維度欄位是否存在
    # 3. 建立 MultiIndex: df.groupby(dimensions)[metric].agg(agg_func)
    # 4. 排序並回傳
    pass
```

**預期輸出：**
```python
# 測試 1：一維分析
result1 = create_sales_dashboard(['customer_state'])
print("各州總銷售額 Top 10：")
print(result1.head(10))

# 測試 2：二維分析
result2 = create_sales_dashboard(['customer_state', 'product_category_name'], agg_func='mean')
print("各州 × 類別平均訂單金額 Top 20：")
print(result2.head(20))

# 測試 3：三維分析
result3 = create_sales_dashboard(
    ['customer_state', 'product_category_name', 'seller_state'],
    agg_func='count'
)
print("客戶州 × 產品類別 × 賣家州訂單數量：")
print(result3.head(20))

輸出：
各州總銷售額 Top 10：
customer_state
SP    1,234,567.89
RJ      987,654.32
MG      765,432.10
...

各州 × 類別平均訂單金額 Top 20：
customer_state  product_category_name
SP              eletronicos             537.26
                cama_mesa_banho         522.81
...

✅ 函數測試完成！可處理 1-3 維動態分析。
```

**Excel 對照：**
- Excel：手動調整樞紐表列標籤順序與組合
- pandas：使用參數化函數動態建立不同維度的 MultiIndex

---

## 📚 學習資源

### 資料路徑
```python
# Olist 資料集路徑
base_path = '/mnt/data/datasets/ecommerce/olist/'

# 主要檔案
orders = 'olist_orders_dataset.csv'
order_items = 'olist_order_items_dataset.csv'
products = 'olist_products_dataset.csv'
customers = 'olist_customers_dataset.csv'
sellers = 'olist_sellers_dataset.csv'
```

### 常用 MultiIndex 方法速查
```python
# 建立 MultiIndex
df.set_index(['col1', 'col2'])
df.groupby(['col1', 'col2'])['value'].sum()
pd.MultiIndex.from_tuples([(a, b), (c, d)])
pd.MultiIndex.from_product([list1, list2])

# 切片與選取
series.loc['level1_value']
series.loc[('level1', 'level2')]
series.xs('value', level='name')
idx = pd.IndexSlice; series.loc[idx['A':'C', :]]

# 轉換
series.unstack()  # 索引 → 欄位
df.stack()        # 欄位 → 索引
series.swaplevel()  # 交換層級順序
series.sort_index()  # 排序

# 資訊查詢
series.index.names      # 索引層級名稱
series.index.nlevels    # 索引層數
series.index.levels     # 各層級的唯一值
```

---

## ✅ 學習檢核表

完成以下檢核點，確保你掌握 MultiIndex 核心技能：

- [ ] 能夠使用 `groupby()` 自動建立 MultiIndex
- [ ] 能夠使用 `from_tuples()` 手動建立 MultiIndex
- [ ] 熟悉 `.loc[]` 單層與雙層切片
- [ ] 能夠使用 `IndexSlice` 進行複雜範圍選取
- [ ] 理解 `.xs()` 的跨層選取用途
- [ ] 掌握 `stack()` 與 `unstack()` 的轉換邏輯
- [ ] 能夠使用 `swaplevel()` 調整索引順序
- [ ] 能夠建立三層及以上的 MultiIndex
- [ ] 能夠結合 `groupby()` 與 `agg()` 進行複雜聚合
- [ ] 能夠生成包含小計與總計的報表
- [ ] 能夠將 MultiIndex 轉換為 Excel 報表
- [ ] 理解 MultiIndex 與 Excel 樞紐表的對應關係

---

## 🎓 下一步

完成這 12 題後，請繼續：
1. **Exercise_02_GroupBy_15_Questions.md** - 深入學習 GroupBy 進階技巧
2. **Exercise_03_Pivot_10_Questions.md** - 掌握透視表與寬窄表轉換
3. **Solutions_Complete.md** - 查看所有題目的詳細解答與說明

祝學習順利！💪
