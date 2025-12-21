# 🎯 Exercise 03: Pivot Table 透視表實戰（10 題）

> **課程：** Week 3 - MultiIndex & 複雜 GroupBy
> **資料集：** Olist 巴西電商資料
> **時間分配：** 基礎 5-10 分鐘/題 | 進階 10-20 分鐘/題 | 挑戰 20-30 分鐘/題

---

## 📊 難度分級

- 🟢 **基礎（1-3 題）：** 基本 pivot_table 操作
- 🟡 **進階（4-7 題）：** Stack/Unstack、Melt、複雜轉換
- 🔴 **挑戰（8-10 題）：** 綜合應用與報表設計

---

## 🟢 基礎題（1-3 題）

### 🟢 題目 1：建立基本透視表 - 單維度

**情境：**
快速建立一個「各州別的訂單總額」透視表。

**任務：**
1. 載入訂單、訂單明細、客戶資料並合併
2. 使用 `pd.pivot_table()` 建立透視表：
   - index（列）：customer_state（州別）
   - values（值）：price（價格）
   - aggfunc（聚合函數）：sum（加總）
3. 對結果降序排序
4. 找出 Top 10 州別
5. 計算 Top 10 佔全國比例

**提示：**
```python
pivot = pd.pivot_table(
    df,
    index='customer_state',
    values='price',
    aggfunc='sum'
)
```

**預期輸出：**
```
customer_state
SP    1,234,567.89
RJ      987,654.32
MG      765,432.10
...

Top 10 佔全國比例：67.8%
```

**Excel 對照：**
- Excel：插入 → 樞紐分析表 → 列標籤選「州別」，值選「價格（加總）」
- pandas：`pd.pivot_table(df, index='state', values='price', aggfunc='sum')`

---

### 🟢 題目 2：雙維度透視表 - 交叉分析

**情境：**
建立「州別 × 產品類別」交叉透視表，查看各地區的產品偏好。

**任務：**
1. 使用 `pivot_table()` 建立透視表：
   - index（列）：customer_state
   - columns（欄）：product_category_name
   - values：price
   - aggfunc：sum
2. 填補 NaN 值為 0
3. 新增「Total」欄（每列總計）
4. 新增「Total」列（每欄總計）使用 `margins=True`
5. 找出每個州別的 Top 3 產品類別

**提示：**
```python
pivot = pd.pivot_table(
    df,
    index='customer_state',
    columns='product_category_name',
    values='price',
    aggfunc='sum',
    fill_value=0,
    margins=True,
    margins_name='總計'
)
```

**預期輸出：**
```
product_category_name  eletronicos  beleza_saude  cama_mesa_banho  ...  總計
customer_state
SP                      45,678.90    23,456.78       34,567.89    ...  234,567.89
RJ                      34,567.89    18,765.43       28,765.43    ...  187,654.32
MG                      12,345.67     9,876.54       15,432.10    ...   98,765.43
...
總計                   234,567.89   123,456.78      156,789.01    ... 1,234,567.89

各州 Top 3 產品類別：
SP:  1. eletronicos  2. cama_mesa_banho  3. beleza_saude
RJ:  1. eletronicos  2. cama_mesa_banho  3. beleza_saude
...
```

**Excel 對照：**
- Excel：列標籤選「州別」，欄標籤選「產品類別」
- pandas：`pivot_table(index='state', columns='category', ...)`

---

### 🟢 題目 3：多值透視表 - 同時顯示總額與數量

**情境：**
在同一個透視表中顯示「訂單總額」與「訂單數量」。

**任務：**
1. 使用 `pivot_table()` 同時計算多個值：
   - values：['price', 'order_id']
   - aggfunc：{'price': 'sum', 'order_id': 'nunique'}
2. 將結果的 MultiIndex columns 扁平化
3. 計算「平均客單價」（總額 / 訂單數）
4. 找出「高客單價州別」（平均 > 200）
5. 視覺化：繪製「訂單數 vs 客單價」散點圖

**提示：**
```python
pivot = pd.pivot_table(
    df,
    index='customer_state',
    values=['price', 'order_id'],
    aggfunc={'price': 'sum', 'order_id': 'nunique'}
)

# 扁平化欄位名稱
pivot.columns = ['_'.join(col).strip() for col in pivot.columns.values]
```

**預期輸出：**
```
customer_state  price_sum   order_id_nunique  avg_order_value
SP             1,234,567.89      5,678            217.45
RJ               987,654.32      4,321            228.56
MG               765,432.10      3,456            221.48
...

高客單價州別（8 個）：
RJ, MG, ES, SC, ...

[散點圖]
```

**Excel 對照：**
- Excel：在值區域拖曳多個欄位，分別設定加總與計數
- pandas：使用字典形式的 `aggfunc`

---

## 🟡 進階題（4-7 題）

### 🟡 題目 4：多函數聚合透視表

**情境：**
對每個產品類別顯示完整的統計摘要（總額、平均、中位數、訂單數）。

**任務：**
1. 建立透視表，使用多個聚合函數：
   - aggfunc：['sum', 'mean', 'median', 'count']
2. 將 MultiIndex columns 轉換為易讀格式
3. 計算「變異係數」（標準差 / 平均值），衡量價格離散程度
4. 找出「價格最穩定」的 5 個類別（變異係數最小）
5. 找出「價格最不穩定」的 5 個類別

**提示：**
```python
pivot = pd.pivot_table(
    df,
    index='product_category_name',
    values='price',
    aggfunc=['sum', 'mean', 'median', 'count', 'std']
)

# 計算變異係數
pivot['cv'] = pivot['std'] / pivot['mean']
```

**預期輸出：**
```
product_category_name  sum         mean    median  count  std      cv
eletronicos           345,678.90  487.65  456.78   709   234.56  0.48
cama_mesa_banho       234,567.89  156.78  145.67  1,496  89.12   0.57
beleza_saude          198,765.43  178.92  167.89  1,111  67.34   0.38
...

價格最穩定 Top 5（CV 最小）：
1. beleza_saude (CV: 0.38)
2. livros_tecnicos (CV: 0.42)
...

價格最不穩定 Top 5（CV 最大）：
1. informatica_acessorios (CV: 1.23)
2. eletrodomesticos (CV: 1.08)
...
```

**Excel 對照：**
- Excel：在值區域對同一欄位新增多次，分別選擇不同的計算方式
- pandas：`aggfunc=['sum', 'mean', ...]`

---

### 🟡 題目 5：條件格式透視表 - 百分比顯示

**情境：**
建立「州別 × 產品類別」透視表，顯示每個組合佔該州總額的百分比。

**任務：**
1. 建立基本的「州別 × 類別」銷售額透視表
2. 計算每列的百分比（每個州內各類別的佔比）
3. 使用 `.div()` 或 `.apply()` 實現列方向百分比
4. 找出每個州「佔比最高」的產品類別
5. 識別「全國通用熱門類別」（在 80% 以上的州都排前 3）

**提示：**
```python
# 建立透視表
pivot = pd.pivot_table(df, index='state', columns='category', values='price', aggfunc='sum', fill_value=0)

# 計算列百分比
pivot_pct = pivot.div(pivot.sum(axis=1), axis=0) * 100

# 找出每列最大值
pivot.idxmax(axis=1)
```

**預期輸出：**
```
各州類別佔比（%）：
product_category_name  eletronicos  beleza_saude  cama_mesa_banho  ...
customer_state
SP                         19.5%        10.0%          14.7%      ...
RJ                         18.4%        10.0%          15.3%      ...
MG                         12.5%        10.0%          15.6%      ...
...

各州最熱門類別：
SP: cama_mesa_banho (14.7%)
RJ: cama_mesa_banho (15.3%)
MG: cama_mesa_banho (15.6%)
...

全國通用熱門類別（3 個）：
1. cama_mesa_banho（26/27 州排前 3）
2. beleza_saude（24/27 州排前 3）
3. esporte_lazer（21/27 州排前 3）
```

**Excel 對照：**
- Excel：樞紐表 → 值的欄位設定 → 顯示值的方式 → 列總和的百分比
- pandas：使用 `.div(pivot.sum(axis=1), axis=0)`

---

### 🟡 題目 6：Stack / Unstack 轉換 - 寬窄表互轉

**情境：**
將「寬格式」的透視表轉換為「長格式」（適合繪圖），再轉回寬格式。

**任務：**
1. 建立「州別 × 產品類別」的寬格式透視表
2. 使用 `.stack()` 轉換為長格式（MultiIndex Series）
3. 使用 `.reset_index()` 轉換為三欄 DataFrame（state, category, value）
4. 使用 `seaborn` 或 `plotly` 繪製熱力圖
5. 使用 `.pivot()` 或 `.unstack()` 轉回寬格式
6. 驗證轉換前後資料一致性

**提示：**
```python
# 寬 → 長
wide_df = pd.pivot_table(df, index='state', columns='category', values='price', aggfunc='sum')
long_df = wide_df.stack().reset_index()
long_df.columns = ['state', 'category', 'sales']

# 長 → 寬
wide_df_2 = long_df.pivot(index='state', columns='category', values='sales')

# 驗證
(wide_df == wide_df_2).all().all()
```

**預期輸出：**
```
寬格式（10 列 × 20 欄）：
product_category_name  eletronicos  beleza_saude  ...
customer_state
SP                      45,678.90    23,456.78   ...
...

轉換為長格式（200 列 × 3 欄）：
   state            category        sales
0  SP               eletronicos     45,678.90
1  SP               beleza_saude    23,456.78
2  RJ               eletronicos     34,567.89
...

[熱力圖]

轉回寬格式驗證：
✅ 資料一致性檢查通過！
```

**Excel 對照：**
- Excel：無直接對應功能，需使用 Power Query
- pandas：`stack()` / `unstack()` 一行搞定

---

### 🟡 題目 7：Melt - 寬表變長表（逆透視）

**情境：**
將月度銷售報表（寬格式：每月一欄）轉換為長格式（適合時間序列分析）。

**任務：**
1. 建立「產品類別 × 月份」的寬格式透視表（月份為欄位）
2. 使用 `pd.melt()` 將月份欄位「熔化」為長格式：
   - id_vars：product_category_name
   - value_vars：所有月份欄位
   - var_name：'month'
   - value_name：'sales'
3. 轉換月份為 datetime 格式
4. 繪製時間序列圖：各產品類別的月度趨勢
5. 識別「季節性明顯」的類別

**提示：**
```python
# 建立寬格式（類別 × 月份）
df['year_month'] = df['timestamp'].dt.to_period('M').astype(str)
wide_df = pd.pivot_table(df, index='category', columns='year_month', values='price', aggfunc='sum')

# 使用 melt 轉換
long_df = wide_df.reset_index().melt(
    id_vars='category',
    var_name='month',
    value_name='sales'
)
```

**預期輸出：**
```
寬格式（73 類別 × 24 月份）：
year_month             2017-01   2017-02   2017-03  ...
product_category_name
eletronicos           12,345.67  14,567.89  16,789.01 ...
cama_mesa_banho        8,765.43   9,876.54  10,987.65 ...
...

Melt 後長格式（1,752 列 × 3 欄）：
   category         month     sales
0  eletronicos      2017-01   12,345.67
1  eletronicos      2017-02   14,567.89
2  cama_mesa_banho  2017-01    8,765.43
...

[時間序列圖]

季節性明顯類別（5 個）：
1. brinquedos（11-12 月銷售額是平均值的 2.8 倍）
2. presentes（11-12 月銷售額是平均值的 2.3 倍）
...
```

**Excel 對照：**
- Excel：Power Query → 逆轉樞紐
- pandas：`pd.melt()` 函數

---

## 🔴 挑戰題（8-10 題）

### 🔴 題目 8：動態透視表函數

**情境：**
建立一個通用的透視表生成函數，可根據參數動態調整維度與指標。

**任務：**
1. 建立函數 `create_pivot_report(index_cols, column_cols=None, value_col='price', agg_funcs=['sum'])`
2. 函數內部自動載入與合併資料
3. 支援以下功能：
   - 單維度或多維度索引
   - 選擇性欄位分組
   - 多個聚合函數
   - 自動新增總計列與欄
   - 匯出為 Excel（含格式）
4. 測試以下組合：
   - `create_pivot_report(['customer_state'])`
   - `create_pivot_report(['customer_state'], ['product_category_name'])`
   - `create_pivot_report(['customer_state', 'seller_state'], agg_funcs=['sum', 'count'])`

**提示：**
```python
def create_pivot_report(index_cols, column_cols=None, value_col='price', agg_funcs=['sum'], export_excel=False):
    # 1. 載入資料
    # 2. 合併資料
    # 3. 建立透視表
    # 4. 格式化
    # 5. 選擇性匯出
    return pivot_table
```

**預期輸出：**
```python
# 測試 1：單維度
result1 = create_pivot_report(['customer_state'])
print(result1.head())

# 測試 2：雙維度交叉表
result2 = create_pivot_report(['customer_state'], ['product_category_name'])
print(result2.head())

# 測試 3：多函數聚合 + 匯出
result3 = create_pivot_report(
    index_cols=['customer_state'],
    column_cols=['product_category_name'],
    agg_funcs=['sum', 'mean', 'count'],
    export_excel=True
)

輸出：
✅ 測試 1 完成：27 列 × 1 欄
✅ 測試 2 完成：27 列 × 73 欄
✅ 測試 3 完成：已匯出至 pivot_report_20180901.xlsx

函數特性：
- 支援 1-3 維索引
- 支援 0-2 維欄位分組
- 支援多聚合函數
- 自動處理 NaN 值
- 可選 Excel 匯出
```

**Excel 對照：**
- Excel：每次需手動調整樞紐表設定
- pandas：函數化後一行呼叫即可生成

---

### 🔴 題目 9：綜合透視報表 - 多層分析儀表板

**情境：**
建立一份「Executive Dashboard」，包含多個相關聯的透視表。

**任務：**
建立以下 5 個透視表，並整合為單一報表：

1. **總覽表：** 各州訂單數、總額、平均客單價
2. **產品表：** 各類別訂單數、總額、市佔率
3. **交叉表：** 州別 × 類別矩陣（熱力圖）
4. **時間表：** 月度趨勢（訂單數 & 總額）
5. **賣家表：** Top 20 賣家績效

要求：
- 所有表格使用一致的格式與配色
- 新增關鍵指標卡（KPI Cards）
- 使用 `plotly` 或 `matplotlib` 建立互動式視覺化
- 匯出為多工作表 Excel 檔案
- 新增 Summary 頁面（重點摘要）

**提示：**
```python
# 建立 Excel Writer
with pd.ExcelWriter('executive_dashboard.xlsx', engine='xlsxwriter') as writer:
    # Summary 頁
    summary_df.to_excel(writer, sheet_name='Summary')

    # 各透視表
    pivot1.to_excel(writer, sheet_name='州別分析')
    pivot2.to_excel(writer, sheet_name='產品分析')
    pivot3.to_excel(writer, sheet_name='交叉分析')
    pivot4.to_excel(writer, sheet_name='時間趨勢')
    pivot5.to_excel(writer, sheet_name='賣家排行')
```

**預期輸出：**
```
執行中...
✅ 總覽表建立完成（27 列 × 5 欄）
✅ 產品表建立完成（73 列 × 6 欄）
✅ 交叉表建立完成（27 列 × 73 欄）
✅ 時間表建立完成（24 列 × 4 欄）
✅ 賣家表建立完成（20 列 × 7 欄）

關鍵指標：
- 總訂單數：99,441 筆
- 總銷售額：$13,591,643.70
- 平均客單價：$136.72
- 活躍州別：27 個
- 產品類別：73 個
- 活躍賣家：3,095 位

✅ 報表已匯出：executive_dashboard.xlsx（6 個工作表）
✅ 視覺化已儲存：dashboard_charts.html（互動式）

[展示多個視覺化圖表]
```

**Excel 對照：**
- Excel：手動建立多個樞紐表，逐一調整格式
- pandas：自動化生成整套報表系統

---

### 🔴 題目 10：自訂透視表樣式與條件格式

**情境：**
建立專業的透視表報表，包含條件格式、資料條、色階等視覺化元素。

**任務：**
1. 建立「州別 × 產品類別」透視表
2. 使用 `Styler` 套用條件格式：
   - 數值欄位：千分位逗號、小數點 2 位
   - 背景色階：依銷售額高低顯示綠色深淺
   - 資料條：在儲存格內顯示橫條圖
   - 突顯最大值與最小值
3. 新增列總計與欄總計（不同底色）
4. 匯出為 HTML（保留格式）
5. 匯出為 Excel（使用 `xlsxwriter` 套用格式）

**提示：**
```python
# 建立 Styler
styled = pivot.style\
    .format('${:,.2f}')\
    .background_gradient(cmap='Greens', axis=None)\
    .bar(color='lightblue', vmin=0)\
    .highlight_max(axis=1, color='gold')\
    .highlight_min(axis=1, color='lightcoral')

# 匯出 HTML
styled.to_html('pivot_styled.html')

# 匯出 Excel（需要使用 xlsxwriter engine）
with pd.ExcelWriter('pivot_styled.xlsx', engine='xlsxwriter') as writer:
    pivot.to_excel(writer, sheet_name='銷售分析')
    workbook = writer.book
    worksheet = writer.sheets['銷售分析']

    # 套用條件格式
    # ...
```

**預期輸出：**
```
透視表樣式設定：
✅ 數值格式：千分位逗號
✅ 色階：綠色漸層（深 = 高銷售額）
✅ 資料條：藍色橫條（相對大小）
✅ 最大值：金色突顯
✅ 最小值：淺珊瑚色突顯
✅ 總計列：灰色底

匯出檔案：
✅ pivot_styled.html（瀏覽器可開啟）
✅ pivot_styled.xlsx（Excel 可開啟，保留條件格式）

[展示格式化後的透視表截圖]

格式化前後對比：
Before: 純文字數字，難以快速識別重點
After:  視覺化呈現，一眼看出高低值與趨勢
```

**Excel 對照：**
- Excel：常用 → 設定格式化的條件 → 色階 / 資料橫條
- pandas：使用 `.style` API 自動化套用

---

## 📚 學習資源

### Pivot Table 方法速查表

```python
# 基本 pivot_table
pd.pivot_table(
    df,
    index='row_field',           # 列欄位
    columns='col_field',         # 欄欄位（可選）
    values='value_field',        # 值欄位
    aggfunc='sum',               # 聚合函數
    fill_value=0,                # 填補 NaN
    margins=True,                # 新增總計
    margins_name='Total'         # 總計名稱
)

# 多值多函數
pd.pivot_table(
    df,
    index='row_field',
    values=['value1', 'value2'],
    aggfunc={'value1': 'sum', 'value2': 'mean'}
)

# pivot（無聚合，直接重塑）
df.pivot(index='row', columns='col', values='value')

# Stack / Unstack
df.stack()          # 欄位 → 列（寬 → 長）
df.unstack()        # 列 → 欄位（長 → 寬）
df.stack(level=0)   # 指定層級

# Melt（逆透視）
pd.melt(
    df,
    id_vars=['固定欄位'],
    value_vars=['要融化的欄位'],
    var_name='新變數名稱',
    value_name='新值名稱'
)

# Crosstab（交叉表）
pd.crosstab(
    df['row_field'],
    df['col_field'],
    values=df['value_field'],
    aggfunc='sum'
)

# 樣式設定
df.style\
    .format('${:,.2f}')\
    .background_gradient(cmap='Blues')\
    .bar(color='lightgreen')\
    .highlight_max(color='yellow')
```

---

## ✅ 學習檢核表

完成以下檢核點，確保你掌握 Pivot Table 核心技能：

- [ ] 能夠建立基本的單維度透視表
- [ ] 能夠建立雙維度交叉透視表
- [ ] 熟悉 `pivot_table()` 的各項參數設定
- [ ] 能夠同時顯示多個值與多個聚合函數
- [ ] 理解如何新增總計列與欄（margins）
- [ ] 掌握百分比計算方式（列、欄、總計）
- [ ] 能夠使用 `stack()` 與 `unstack()` 轉換寬窄表
- [ ] 能夠使用 `melt()` 進行逆透視
- [ ] 理解 `pivot()` 與 `pivot_table()` 的差異
- [ ] 能夠使用 `.style` 套用條件格式
- [ ] 能夠將透視表匯出為格式化的 Excel
- [ ] 理解 pandas 透視表與 Excel 樞紐表的對應關係

---

## 🎓 總結與下一步

恭喜完成 Week 3 的所有練習題！你已經掌握：

### 核心技能
✅ MultiIndex（12 題）：多層索引的建立、切片、轉換
✅ GroupBy（15 題）：分組聚合、Transform、Filter、自訂函數
✅ Pivot Table（10 題）：透視表、寬窄轉換、視覺化

### 實戰應用
✅ 能夠處理複雜的多維度資料分析
✅ 能夠建立專業的商業報表
✅ 理解 pandas 與 Excel 的對應關係

### 下一步
1. **查看完整解答：** `Solutions_Complete.md`（37 題詳細解答）
2. **動手實作：** 使用 Olist 資料集完成所有練習
3. **進階學習：** Week 4 - 時間序列分析

繼續加油！💪
