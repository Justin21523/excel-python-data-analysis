# 🎯 Exercise 02: GroupBy 進階實戰（15 題）

> **課程：** Week 3 - MultiIndex & 複雜 GroupBy
> **資料集：** Olist 巴西電商資料
> **時間分配：** 基礎 5-10 分鐘/題 | 進階 10-20 分鐘/題 | 挑戰 20-30 分鐘/題

---

## 📊 難度分級

- 🟢 **基礎（1-5 題）：** 基本聚合與多函數應用
- 🟡 **進階（6-11 題）：** Transform、Filter、Named Aggregation
- 🔴 **挑戰（12-15 題）：** 自訂函數與複雜商業邏輯

---

## 🟢 基礎題（1-5 題）

### 🟢 題目 1：基礎 GroupBy - 單欄位單函數

**情境：**
管理層想快速了解各州的訂單總額分布。

**任務：**
1. 載入訂單（orders）、訂單明細（order_items）、客戶（customers）資料
2. 合併資料表，連接訂單與客戶（獲取州別資訊）
3. 使用 `groupby('customer_state')['price'].sum()` 計算各州訂單總額
4. 對結果降序排序，找出 Top 10 州別
5. 計算 Top 10 州別的總額佔全國比例

**提示：**
- 使用 `pd.merge()` 連接訂單與客戶
- `df.groupby('column')['value'].agg_func()`
- 使用 `.sort_values(ascending=False)` 排序
- 佔比計算：`top10_sum / total_sum * 100`

**預期輸出：**
```
customer_state
SP    1,234,567.89
RJ      987,654.32
MG      765,432.10
...

Top 10 州別總額：$5,678,901.23
佔全國比例：67.8%
```

**Excel 對照：**
- Excel：樞紐表，列標籤選「州別」，值選「價格（加總）」
- pandas：`df.groupby('customer_state')['price'].sum()`

---

### 🟢 題目 2：多函數聚合 - agg([...])

**情境：**
財務部門需要每個產品類別的詳細統計資訊。

**任務：**
1. 載入產品與訂單明細資料
2. 合併資料表
3. 使用 `.agg(['sum', 'mean', 'count', 'min', 'max'])` 對每個產品類別計算：
   - 總銷售額
   - 平均訂單金額
   - 訂單數量
   - 最小單筆金額
   - 最大單筆金額
4. 將結果轉換為 DataFrame 並重命名欄位為中文
5. 找出「高價值類別」（總額 > 100000 且訂單數 > 500）

**提示：**
- `df.groupby('category')['price'].agg(['sum', 'mean', 'count', 'min', 'max'])`
- 使用 `.rename(columns={...})` 重命名
- 使用 `.query("sum > 100000 and count > 500")` 篩選

**預期輸出：**
```
                            總銷售額    平均金額   訂單數   最小金額   最大金額
product_category_name
cama_mesa_banho          234,567.89   156.78    1,496    9.90    1,234.56
beleza_saude             198,765.43   178.92    1,111   12.34    2,345.67
eletronicos              345,678.90   487.65      709   45.67    5,678.90
...

高價值類別（3 個）：
cama_mesa_banho, beleza_saude, eletronicos
```

**Excel 對照：**
- Excel：樞紐表值區域新增多個欄位（加總、平均、計數、最小、最大）
- pandas：使用 `.agg([...])` 一次計算

---

### 🟢 題目 3：多欄位聚合 - 字典形式

**情境：**
分析團隊需要對「價格」與「運費」使用不同的聚合函數。

**任務：**
1. 對每個產品類別分別計算：
   - 價格（price）：總額、平均值
   - 運費（freight_value）：總額、中位數
2. 使用字典形式的 agg：
   ```python
   {
       'price': ['sum', 'mean'],
       'freight_value': ['sum', 'median']
   }
   ```
3. 將結果扁平化（flatten MultiIndex columns）
4. 計算「運費佔售價比例」（freight_sum / price_sum）
5. 找出運費比例最高的 5 個類別

**提示：**
- `df.groupby('category').agg({'price': [...], 'freight_value': [...]})`
- 扁平化欄位：`df.columns = ['_'.join(col).strip() for col in df.columns.values]`
- 新增欄位計算比例

**預期輸出：**
```
                            price_sum  price_mean  freight_sum  freight_median  freight_ratio
product_category_name
cama_mesa_banho          234,567.89     156.78    23,456.78        15.67         10.0%
moveis_decoracao         198,765.43     487.92    34,567.89        28.90         17.4%
...

運費比例最高 Top 5：
1. moveis_decoracao: 17.4%
2. eletrodomesticos: 15.8%
...
```

**Excel 對照：**
- Excel：樞紐表中對不同欄位分別設定值區域的計算方式
- pandas：使用字典形式的 `agg()`

---

### 🟢 題目 4：分組後計算衍生指標

**情境：**
產品經理想知道每個類別的「訂單平均商品數」與「平均客單價」。

**任務：**
1. 對每個產品類別分組
2. 計算以下指標：
   - 總訂單數（order_id 去重計數）
   - 總商品數（order_item_id 計數）
   - 總銷售額（price 加總）
3. 計算衍生指標：
   - 訂單平均商品數 = 總商品數 / 總訂單數
   - 平均客單價 = 總銷售額 / 總訂單數
4. 找出「高客單價類別」（平均客單價 > 200）
5. 視覺化：繪製「平均商品數 vs 平均客單價」散點圖

**提示：**
- 使用 `df.groupby('category').agg({'order_id': 'nunique', 'order_item_id': 'count', 'price': 'sum'})`
- 計算新欄位：`df['avg_items'] = df['total_items'] / df['total_orders']`
- 使用 `matplotlib` 或 `seaborn` 繪圖

**預期輸出：**
```
                            總訂單數  總商品數   總銷售額    平均商品數  平均客單價
product_category_name
eletronicos                  709      892   345,678.90    1.26      487.65
cama_mesa_banho            1,496    2,134   234,567.89    1.43      156.78
...

高客單價類別（8 個）：
eletronicos, informatica_acessorios, ...

[散點圖]
```

**Excel 對照：**
- Excel：樞紐表計算值後，手動新增計算欄位
- pandas：直接在 DataFrame 中新增欄位計算

---

### 🟢 題目 5：時間序列分組 - 按月統計

**情境：**
營運團隊需要分析 2017-2018 年各月的訂單量與銷售額趨勢。

**任務：**
1. 將訂單購買時間（order_purchase_timestamp）轉換為 datetime
2. 提取年月資訊（使用 `.dt.to_period('M')`）
3. 按月分組計算：
   - 訂單數量
   - 總銷售額
   - 平均訂單金額
4. 計算月度成長率（MoM Growth）
5. 找出成長率最高的 3 個月份

**提示：**
- `pd.to_datetime(df['timestamp'])`
- `df['year_month'] = df['timestamp'].dt.to_period('M')`
- `df.groupby('year_month').agg(...)`
- 成長率：`df['growth'] = df['value'].pct_change() * 100`

**預期輸出：**
```
year_month  訂單數   總銷售額      平均金額    月成長率
2017-01      234   45,678.90     195.12       -
2017-02      289   56,789.01     196.50      24.3%
2017-03      312   62,345.67     199.82       9.8%
...

成長率最高 3 個月：
1. 2017-11: 45.6% (黑色星期五效應)
2. 2018-05: 38.2%
3. 2017-02: 24.3%
```

**Excel 對照：**
- Excel：使用 `TEXT(日期, "YYYY-MM")` 建立年月欄位，再建立樞紐表
- pandas：使用 `.dt.to_period('M')` 提取年月

---

## 🟡 進階題（6-11 題）

### 🟡 題目 6：Named Aggregation - 命名聚合

**情境：**
報表需要清晰的欄位名稱，避免 `price_sum`、`price_mean` 等技術性命名。

**任務：**
1. 使用 pandas 命名聚合語法：
   ```python
   df.groupby('category').agg(
       總銷售額=('price', 'sum'),
       平均訂單=('price', 'mean'),
       訂單數量=('order_id', 'nunique'),
       最高單價=('price', 'max')
   )
   ```
2. 對「州別」與「產品類別」雙層分組使用命名聚合
3. 將結果輸出為格式化的 Excel 報表
4. 新增計算欄位：「總銷售額排名」、「訂單數排名」
5. 找出「銷售冠軍但訂單數較少」的類別（銷售排名 < 10，訂單排名 > 20）

**提示：**
- 命名聚合：`df.groupby(...).agg(新名稱=(欄位, 函數))`
- 排名：`df['rank'] = df['value'].rank(ascending=False)`
- 使用 `to_excel()` 輸出

**預期輸出：**
```
                            總銷售額    平均訂單   訂單數量  最高單價  銷售排名  訂單排名
product_category_name
eletronicos              345,678.90   487.65      709    5,678     1        15
cama_mesa_banho          234,567.89   156.78    1,496    1,234     2         3
beleza_saude             198,765.43   178.92    1,111    2,345     3         8
...

高價值低頻類別（2 個）：
informatica_acessorios (銷售排名 7, 訂單排名 25)
relogios_presentes (銷售排名 9, 訂單排名 28)
```

**Excel 對照：**
- Excel：樞紐表中手動重命名欄位
- pandas：使用命名聚合直接指定中文名稱

---

### 🟡 題目 7：Transform - 組內計算百分比

**情境：**
行銷部門想標記每筆訂單在該產品類別中的「銷售額佔比」，找出「明星訂單」。

**任務：**
1. 使用 `transform()` 計算每個產品類別的總銷售額
2. 將類別總額廣播回每一列（使用 transform）
3. 計算每筆訂單在該類別的佔比（訂單額 / 類別總額 × 100）
4. 找出佔比 > 5% 的「明星訂單」（異常高價訂單）
5. 分析這些明星訂單的特徵（平均價格、主要州別、時間分布）

**提示：**
- `df['category_total'] = df.groupby('category')['price'].transform('sum')`
- `df['pct'] = df['price'] / df['category_total'] * 100`
- 使用 `.query("pct > 5")` 篩選

**預期輸出：**
```
order_id    product_category  price     category_total  pct_of_category
abc123      eletronicos      5,678.90   345,678.90         1.64%
def456      eletronicos      8,999.00   345,678.90         2.60%  [明星]
ghi789      cama_mesa_banho 12,345.00   234,567.89         5.26%  [明星]
...

明星訂單數量：23 筆
明星訂單平均金額：$8,765.43
主要州別：SP (12 筆), RJ (7 筆)
時間分布：集中在黑色星期五、聖誕節前
```

**Excel 對照：**
- Excel：`=訂單額 / SUMIF(類別, [@類別], 訂單額) * 100`
- pandas：`transform(lambda x: x / x.sum() * 100)`

---

### 🟡 題目 8：Transform - 組內標準化與異常檢測

**情境：**
資料科學團隊需要識別每個產品類別中的「異常高價」或「異常低價」訂單。

**任務：**
1. 對每個產品類別計算平均價格與標準差（使用 transform）
2. 計算每筆訂單的 Z-score：`(price - mean) / std`
3. 標記異常訂單：
   - 異常高價：Z-score > 2
   - 異常低價：Z-score < -2
   - 正常：-2 ≤ Z-score ≤ 2
4. 統計每個類別的異常訂單比例
5. 找出異常率最高的 5 個類別

**提示：**
- `df['mean'] = df.groupby('category')['price'].transform('mean')`
- `df['std'] = df.groupby('category')['price'].transform('std')`
- `df['zscore'] = (df['price'] - df['mean']) / df['std']`
- 使用 `np.select()` 建立異常標記

**預期輸出：**
```
order_id    category         price    mean     std      zscore   flag
abc123      eletronicos     487.65   492.30   123.45   -0.04    正常
def456      eletronicos   1,234.56   492.30   123.45    6.01    異常高價
ghi789      cama_mesa_banho  12.34   156.78    67.89   -2.13    異常低價
...

各類別異常統計：
                      總訂單數  異常高價  異常低價  異常率
product_category_name
eletronicos              709       18       12    4.23%
construcao_ferramentas   543       34       28   11.42%
...

異常率最高 Top 5：
1. construcao_ferramentas: 11.42%
2. esporte_lazer: 9.87%
...
```

**Excel 對照：**
- Excel：`AVERAGE()` + `STDEV()` 計算後手動建立公式
- pandas：使用 `transform()` 自動廣播統計量

---

### 🟡 題目 9：Transform vs Apply - 效能比較

**情境：**
學習 `transform()` 與 `apply()` 的差異，並比較效能。

**任務：**
1. 建立測試場景：計算每個產品類別的「訂單價格排名」
2. 方法 1：使用 `transform(lambda x: x.rank())`
3. 方法 2：使用 `apply(lambda x: x.rank())` 再 `explode()`
4. 比較兩種方法的執行時間（使用 `%%timeit` 或 `time` 模組）
5. 驗證結果是否相同
6. 總結何時使用 transform、何時使用 apply

**提示：**
- `df['rank_transform'] = df.groupby('category')['price'].transform(lambda x: x.rank(ascending=False))`
- `df['rank_apply'] = df.groupby('category')['price'].apply(lambda x: x.rank(ascending=False))`
- 使用 `time.time()` 或 `%%timeit` 計時

**預期輸出：**
```
方法 1 (transform)：執行時間 0.12 秒
方法 2 (apply)：執行時間 0.45 秒

效能提升：3.75x

結果驗證：
(df['rank_transform'] == df['rank_apply']).all() = True

總結：
✅ transform() 適用場景：
  - 回傳與原 DataFrame 相同長度的結果
  - 需要將組統計量廣播回每一列
  - 速度快（向量化運算）

✅ apply() 適用場景：
  - 回傳聚合結果（每組一個值）
  - 需要複雜的自訂邏輯
  - 可以回傳任意形狀的結果
```

**Excel 對照：**
- Excel：使用 `RANK()` 函數手動建立公式
- pandas：transform 自動處理分組排名

---

### 🟡 題目 10：Filter - 篩選符合條件的組

**情境：**
只保留「訂單數 > 100」的產品類別，過濾掉小眾類別。

**任務：**
1. 使用 `.filter(lambda x: len(x) > 100)` 篩選訂單數 > 100 的類別
2. 比較篩選前後的資料筆數與類別數
3. 建立更複雜的篩選條件：
   - 訂單數 > 100
   - 平均訂單金額 > 100
   - 總銷售額 > 50,000
4. 對篩選後的資料進行分析
5. 將被過濾掉的「小眾類別」單獨輸出

**提示：**
- `df.groupby('category').filter(lambda x: len(x) > 100)`
- 多條件：`lambda x: len(x) > 100 and x['price'].mean() > 100`
- 使用 `~` 反向選取被過濾的資料

**預期輸出：**
```
篩選前：
- 總訂單數：99,441 筆
- 產品類別數：73 個

篩選後（訂單數 > 100）：
- 總訂單數：95,234 筆
- 產品類別數：42 個
- 保留比例：95.8%

被過濾的小眾類別（31 個）：
product_category_name  訂單數  總銷售額
flores                   23    1,234.56
fraldas_higiene          45    2,345.67
seguros_servicos         12      987.65
...

複合條件篩選後（訂單 > 100, 平均 > 100, 總額 > 50000）：
- 保留類別數：18 個
- 這些類別佔總銷售額：87.3%
```

**Excel 對照：**
- Excel：手動篩選或使用進階篩選
- pandas：使用 `.filter()` 自動保留符合條件的組

---

### 🟡 題目 11：Filter 與 Transform 結合

**情境：**
只對「高價值產品類別」（總銷售額 > 100,000）計算組內排名。

**任務：**
1. 先使用 `filter()` 篩選高價值類別
2. 再使用 `transform()` 計算組內價格排名
3. 建立「類別內 Top 10」標記
4. 分析這些 Top 10 訂單的特徵
5. 輸出每個高價值類別的 Top 5 訂單

**提示：**
- 鏈式操作：`df.groupby('category').filter(...).groupby('category')['price'].transform(...)`
- 使用 `df.groupby('category').head(5)` 取每組前 5 筆

**預期輸出：**
```
高價值類別（18 個）：
eletronicos, cama_mesa_banho, beleza_saude, ...

類別內 Top 10 訂單數量：180 筆

eletronicos Top 5：
order_id    price     rank_in_category
abc123     5,678.90         1
def456     4,567.89         2
ghi789     3,987.65         3
...

各類別 Top 10 訂單特徵：
- 平均金額：$2,345.67
- 總額：$422,220.60
- 佔該類別比例：23.4%
- 主要購買州別：SP (45%), RJ (28%)
```

**Excel 對照：**
- Excel：先篩選，再分組排名，需要多個步驟
- pandas：鏈式操作一次完成

---

## 🔴 挑戰題（12-15 題）

### 🔴 題目 12：自訂聚合函數 - 計算組內眾數

**情境：**
找出每個產品類別最常見的「訂單金額區間」（眾數）。

**任務：**
1. 將訂單金額分為區間：0-50, 50-100, 100-200, 200-500, 500+
2. 建立自訂函數 `get_mode(series)` 計算眾數
3. 使用 `.agg(get_mode)` 對每個類別計算最常見的價格區間
4. 同時計算該區間的訂單數量與佔比
5. 視覺化：繪製各類別的價格分布直方圖

**提示：**
```python
def get_mode(series):
    return series.mode()[0] if len(series.mode()) > 0 else None

# 分區間
bins = [0, 50, 100, 200, 500, float('inf')]
labels = ['0-50', '50-100', '100-200', '200-500', '500+']
df['price_range'] = pd.cut(df['price'], bins=bins, labels=labels)

# 聚合
df.groupby('category')['price_range'].agg(get_mode)
```

**預期輸出：**
```
product_category_name   最常見價格區間  該區間訂單數  佔比
eletronicos             200-500         234        33.0%
cama_mesa_banho         50-100          567        37.9%
beleza_saude            100-200         423        38.1%
...

[各類別價格分布直方圖]
```

**Excel 對照：**
- Excel：使用 `MODE()` 函數，需先手動分組
- pandas：自訂函數 + `agg()`

---

### 🔴 題目 13：複雜自訂函數 - 加權平均計算

**情境：**
計算每個賣家的「加權平均評分」（以訂單金額為權重）。

**任務：**
1. 載入評價資料（order_reviews）與訂單明細
2. 建立自訂函數計算加權平均：
   ```python
   def weighted_avg(group):
       return (group['review_score'] * group['price']).sum() / group['price'].sum()
   ```
3. 對每個賣家（seller_id）計算加權平均評分
4. 比較「簡單平均評分」與「加權平均評分」的差異
5. 找出「評分差異最大」的賣家（可能存在刷好評行為）

**提示：**
- 合併評價與訂單明細資料
- `df.groupby('seller_id').apply(weighted_avg)`
- 計算差異：`df['diff'] = df['weighted_avg'] - df['simple_avg']`

**預期輸出：**
```
seller_id                            簡單平均  加權平均  差異    訂單數
abc-123-def                          4.2      3.8      -0.4    156
xyz-456-ghi                          4.5      4.7      +0.2     89
...

評分差異最大 Top 10：
seller_id                            簡單平均  加權平均  差異    分析
abc-123-def                          4.2      3.8      -0.4    高價訂單評分較低
jkl-789-mno                          3.1      4.3      +1.2    低價訂單刷好評（可疑）
...
```

**Excel 對照：**
- Excel：`SUMPRODUCT(評分, 金額) / SUM(金額)`
- pandas：自訂函數處理複雜計算邏輯

---

### 🔴 題目 14：多層 GroupBy - 時間 × 地區 × 類別分析

**情境：**
建立完整的「年月 × 州別 × 產品類別」三維銷售分析報表。

**任務：**
1. 建立三層分組：年月 × 州別 × 產品類別
2. 計算每個組合的：
   - 訂單數量
   - 總銷售額
   - 平均訂單金額
   - 同比成長率（YoY，與去年同月比較）
3. 找出「成長最快的組合」（2018 vs 2017）
4. 識別「季節性明顯的類別」（11-12 月銷售額佔全年 > 30%）
5. 輸出 Executive Summary（管理層摘要）

**提示：**
- 提取年月：`df['year_month'] = df['timestamp'].dt.to_period('M')`
- 三層分組：`df.groupby(['year_month', 'state', 'category'])`
- YoY：需要將資料 pivot 後計算或使用 shift
- 使用 `unstack()` 轉換為易讀格式

**預期輸出：**
```
year_month  state  category         訂單數  總銷售額    平均   YoY成長
2018-01     SP     eletronicos       45    12,345.67  274.35   23.4%
2018-01     SP     cama_mesa_banho   67     8,765.43  130.83   -5.2%
...

成長最快組合 Top 10：
1. 2018-11, MG, eletronicos: +156.7%
2. 2018-05, RJ, esporte_lazer: +98.3%
...

季節性明顯類別（5 個）：
1. brinquedos (11-12月佔 45.6%)
2. presentes (11-12月佔 38.2%)
...

Executive Summary：
- 總分析組合數：4,567 個
- 正成長組合：2,345 個（51.3%）
- 平均成長率：+12.4%
- 重點發現：電子產品在黑色星期五帶動明顯成長
```

**Excel 對照：**
- Excel：多層樞紐表 + 手動計算 YoY
- pandas：GroupBy + Transform 自動計算

---

### 🔴 題目 15：綜合挑戰 - RFM 模型實作

**情境：**
使用 GroupBy 實作 RFM（Recency, Frequency, Monetary）客戶分群模型。

**任務：**
1. 對每個客戶（customer_unique_id）計算：
   - **Recency（最近購買）：** 距離資料集最後日期的天數
   - **Frequency（購買頻率）：** 總訂單數
   - **Monetary（消費金額）：** 總消費額
2. 將 R, F, M 分別分為 5 個等級（1-5，5 為最佳）
3. 建立 RFM 分數（例如：555 為最佳客戶）
4. 定義客戶分群：
   - 重要保持客戶（RFM > 444）
   - 重要挽留客戶（R < 3, F/M > 3）
   - 新客戶（F = 1, M > 平均）
   - 流失客戶（R < 2, F < 2）
5. 輸出各群體的統計分析與行銷建議

**提示：**
```python
# 計算 RFM
rfm = df.groupby('customer_unique_id').agg({
    'order_purchase_timestamp': lambda x: (df['order_purchase_timestamp'].max() - x.max()).days,
    'order_id': 'nunique',
    'price': 'sum'
}).rename(columns={...})

# 分級（使用 qcut）
rfm['R_score'] = pd.qcut(rfm['recency'], 5, labels=[5,4,3,2,1])  # 越小越好，反轉
rfm['F_score'] = pd.qcut(rfm['frequency'], 5, labels=[1,2,3,4,5])
rfm['M_score'] = pd.qcut(rfm['monetary'], 5, labels=[1,2,3,4,5])

# 建立 RFM 組合
rfm['RFM_score'] = rfm['R_score'].astype(str) + rfm['F_score'].astype(str) + rfm['M_score'].astype(str)
```

**預期輸出：**
```
customer_unique_id                  recency  frequency  monetary   R  F  M  RFM
abc-123-def-456                          12         8   2,345.67  5  4  4  544
xyz-789-ghi-012                         234         2     456.78  2  2  2  222
...

客戶分群統計：
群體              客戶數   佔比   平均消費   平均訂單數   平均間隔天數
重要保持客戶      1,234   12.3%  $3,456.78      12.3         45
重要挽留客戶        567    5.7%  $2,345.67       8.9        180
新客戶            2,345   23.5%  $1,234.56       1.2         30
一般客戶          4,567   45.7%    $567.89       3.4         90
流失客戶          1,287   12.9%    $234.56       1.8        320

行銷建議：
✅ 重要保持客戶：VIP 專屬優惠、優先客服
✅ 重要挽留客戶：個人化召回優惠、問卷調查
✅ 新客戶：新人禮包、推薦好友獎勵
✅ 流失客戶：大額折扣券、重新激活活動
```

**Excel 對照：**
- Excel：手動建立 VLOOKUP + IF 公式實現分級
- pandas：使用 `qcut()` 自動分級 + `apply()` 定義分群邏輯

---

## 📚 學習資源

### GroupBy 方法速查表

```python
# 基本聚合
df.groupby('col')['value'].sum()
df.groupby('col')['value'].mean()
df.groupby('col')['value'].agg(['sum', 'mean', 'count'])

# 多欄位不同聚合
df.groupby('col').agg({
    'value1': 'sum',
    'value2': ['mean', 'median']
})

# 命名聚合
df.groupby('col').agg(
    總額=('value', 'sum'),
    平均=('value', 'mean')
)

# Transform（組內計算）
df['group_sum'] = df.groupby('col')['value'].transform('sum')
df['pct'] = df.groupby('col')['value'].transform(lambda x: x / x.sum())

# Filter（篩選組）
df.groupby('col').filter(lambda x: len(x) > 100)
df.groupby('col').filter(lambda x: x['value'].sum() > 10000)

# Apply（自訂函數）
df.groupby('col').apply(custom_function)
df.groupby('col')['value'].apply(lambda x: x.max() - x.min())

# 取每組前 N 筆
df.groupby('col').head(5)
df.groupby('col').tail(3)

# 組資訊
df.groupby('col').size()          # 每組筆數
df.groupby('col').ngroups         # 組數
df.groupby('col').groups          # 組索引字典
```

---

## ✅ 學習檢核表

完成以下檢核點，確保你掌握 GroupBy 核心技能：

- [ ] 熟悉基本聚合函數（sum, mean, count, min, max）
- [ ] 能夠使用 `agg([...])` 多函數聚合
- [ ] 能夠使用字典形式對不同欄位應用不同函數
- [ ] 掌握命名聚合（Named Aggregation）語法
- [ ] 理解 `transform()` 的用途（組內計算、廣播統計量）
- [ ] 能夠使用 `filter()` 篩選符合條件的組
- [ ] 理解 `transform()` vs `apply()` 的差異與效能
- [ ] 能夠建立自訂聚合函數
- [ ] 能夠實作複雜商業邏輯（RFM、加權平均等）
- [ ] 能夠進行多層 GroupBy 分析
- [ ] 能夠計算同比、環比等時間序列指標
- [ ] 理解 GroupBy 與 Excel 樞紐表的對應關係

---

## 🎓 下一步

完成這 15 題後，請繼續：
1. **Exercise_03_Pivot_10_Questions.md** - 掌握透視表與寬窄表轉換
2. **Solutions_Complete.md** - 查看所有題目的詳細解答與說明

祝學習順利！💪
