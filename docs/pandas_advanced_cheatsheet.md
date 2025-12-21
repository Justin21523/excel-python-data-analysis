# pandas 進階技巧速查表

這份速查表涵蓋課程中會用到的所有 pandas 進階技巧。

---

## 📌 MultiIndex（多層索引）

### 建立 MultiIndex

```python
# 方法 1：從 columns 建立
df.set_index(['地區', '產品類別'], inplace=True)

# 方法 2：從 arrays 建立
arrays = [['台北', '台北', '台中', '台中'], ['A', 'B', 'A', 'B']]
index = pd.MultiIndex.from_arrays(arrays, names=['地區', '類別'])
df = pd.DataFrame({'銷售額': [100, 200, 150, 250]}, index=index)

# 方法 3：從 tuples 建立
tuples = [('台北', 'A'), ('台北', 'B'), ('台中', 'A')]
index = pd.MultiIndex.from_tuples(tuples, names=['地區', '類別'])
```

### MultiIndex 操作

```python
# 切片特定層級
df.loc[('台北', 'A')]  # 取得台北 A 的資料
df.xs('台北', level='地區')  # 取得所有台北的資料

# 交換層級
df.swaplevel('地區', '產品類別')

# 排序索引
df.sort_index(level=0)

# 移除層級
df.reset_index(level='地區')  # 將地區從索引移回欄位
df.reset_index(drop=True)  # 完全重置索引
```

---

## 📌 GroupBy 進階

### 多函數聚合

```python
# 方法 1：agg with list
df.groupby('產品類別')['銷售額'].agg(['sum', 'mean', 'std', 'count'])

# 方法 2：agg with dict（不同欄位不同函數）
df.groupby('產品類別').agg({
    '銷售額': ['sum', 'mean'],
    '數量': 'sum',
    '客戶ID': 'nunique'  # 不重複計數
})

# 方法 3：命名聚合（pandas 0.25+）
df.groupby('產品類別').agg(
    總銷售額=('銷售額', 'sum'),
    平均銷售額=('銷售額', 'mean'),
    訂單數=('訂單編號', 'count'),
    客戶數=('客戶ID', 'nunique')
)
```

### 自訂聚合函數

```python
def range_func(x):
    return x.max() - x.min()

df.groupby('產品類別')['銷售額'].agg([
    'sum',
    'mean',
    ('極差', range_func)
])

# Lambda 函數
df.groupby('產品類別')['銷售額'].agg(
    lambda x: x.quantile(0.75)
)
```

### Apply vs Transform vs Agg

```python
# agg: 回傳摘要統計（縮減維度）
df.groupby('產品類別')['銷售額'].agg('sum')  # 回傳每類別總和

# transform: 回傳與原 DataFrame 相同長度的結果
df['組內百分比'] = df.groupby('產品類別')['銷售額'].transform(
    lambda x: x / x.sum() * 100
)

# apply: 最靈活，可回傳任何形狀
df.groupby('產品類別').apply(lambda x: x.nlargest(3, '銷售額'))
```

---

## 📌 Pivot & Stack/Unstack

### pivot_table

```python
# 基本透視表
pd.pivot_table(
    df,
    values='銷售額',
    index='產品類別',
    columns='月份',
    aggfunc='sum',
    fill_value=0
)

# 多值、多函數
pd.pivot_table(
    df,
    values=['銷售額', '數量'],
    index='產品類別',
    columns='月份',
    aggfunc={'銷售額': 'sum', '數量': 'mean'}
)

# 多層索引
pd.pivot_table(
    df,
    values='銷售額',
    index=['地區', '產品類別'],
    columns=['年', '月'],
    aggfunc='sum'
)
```

### pivot vs pivot_table

```python
# pivot: 不需要聚合，資料已唯一
df.pivot(index='日期', columns='產品', values='銷售額')

# pivot_table: 需要聚合函數
df.pivot_table(index='日期', columns='產品', values='銷售額', aggfunc='sum')
```

### melt（逆透視）

```python
# 從寬表轉長表
df_wide = pd.DataFrame({
    '產品': ['A', 'B'],
    '1月': [100, 200],
    '2月': [150, 250]
})

df_long = df_wide.melt(
    id_vars='產品',
    var_name='月份',
    value_name='銷售額'
)
```

### stack / unstack

```python
# unstack: 將列索引轉為欄索引（長 → 寬）
df.unstack()
df.unstack(level='月份')

# stack: 將欄索引轉為列索引（寬 → 長）
df.stack()
```

---

## 📌 時間序列

### 日期解析

```python
# 轉換為日期型態
df['訂單日期'] = pd.to_datetime(df['訂單日期'])

# 多種格式解析
pd.to_datetime('2024/12/10')
pd.to_datetime('2024-12-10')
pd.to_datetime('20241210', format='%Y%m%d')

# 處理錯誤
pd.to_datetime(df['日期'], errors='coerce')  # 無法解析 → NaT
```

### 日期屬性提取

```python
df['年'] = df['訂單日期'].dt.year
df['月'] = df['訂單日期'].dt.month
df['日'] = df['訂單日期'].dt.day
df['星期幾'] = df['訂單日期'].dt.dayofweek  # 0=週一, 6=週日
df['週'] = df['訂單日期'].dt.isocalendar().week
df['季'] = df['訂單日期'].dt.quarter
df['年月'] = df['訂單日期'].dt.to_period('M')
```

### resample（重採樣）

```python
# 設定日期為索引
df.set_index('訂單日期', inplace=True)

# 每日 → 每週
df.resample('W')['銷售額'].sum()

# 每日 → 每月
df.resample('M')['銷售額'].sum()

# 每月 → 每季
df.resample('Q')['銷售額'].sum()

# 常用頻率代碼
# D: 天, W: 週, M: 月, Q: 季, Y: 年
# H: 小時, T/min: 分鐘, S: 秒
```

### rolling（移動視窗）

```python
# 7 日移動平均
df['7日均'] = df['銷售額'].rolling(window=7).mean()

# 30 日移動總和
df['30日總和'] = df['銷售額'].rolling(window=30).sum()

# 移動最大值
df['7日最高'] = df['銷售額'].rolling(window=7).max()

# 移動標準差（波動性）
df['7日波動'] = df['銷售額'].rolling(window=7).std()
```

### shift & diff（時間位移）

```python
# 向後位移（取得前一期數值）
df['上月銷售額'] = df['銷售額'].shift(1)

# 計算成長率
df['月成長率'] = df['銷售額'].pct_change() * 100

# 計算差值
df['月增量'] = df['銷售額'].diff()

# 年增率（YoY）
df['YoY'] = df['銷售額'].pct_change(periods=12) * 100
```

---

## 📌 Merge & Concat

### merge（SQL-like join）

```python
# Inner join（預設）
pd.merge(orders, customers, on='客戶ID', how='inner')

# Left join
pd.merge(orders, customers, on='客戶ID', how='left')

# Right join
pd.merge(orders, customers, on='客戶ID', how='right')

# Outer join（全外連接）
pd.merge(orders, customers, on='客戶ID', how='outer')

# 不同欄位名稱
pd.merge(
    orders,
    customers,
    left_on='customer_id',
    right_on='id',
    how='left'
)

# 多欄位 join
pd.merge(df1, df2, on=['欄位1', '欄位2'], how='inner')

# 檢查 merge 結果
pd.merge(orders, customers, on='客戶ID', how='left', indicator=True)
# _merge 欄位：left_only, right_only, both
```

### concat（上下或左右合併）

```python
# 垂直合併（上下堆疊）
pd.concat([df1, df2], axis=0, ignore_index=True)

# 水平合併（左右拼接）
pd.concat([df1, df2], axis=1)

# 保留來源標籤
pd.concat([df1, df2], keys=['來源1', '來源2'])
```

---

## 📌 效能優化

### 記憶體優化

```python
# 檢查記憶體使用
df.memory_usage(deep=True).sum() / 1024**2  # MB

# Categorical 型態（節省記憶體）
df['產品類別'] = df['產品類別'].astype('category')

# Downcasting（降低精度）
df['整數欄位'] = pd.to_numeric(df['整數欄位'], downcast='integer')
df['浮點欄位'] = pd.to_numeric(df['浮點欄位'], downcast='float')

# 讀取時優化
df = pd.read_csv(
    'data.csv',
    dtype={'產品類別': 'category', 'ID': str},
    parse_dates=['訂單日期']
)
```

### 向量化運算

```python
# ❌ 慢：使用 for loop
for i in range(len(df)):
    df.loc[i, '折扣後'] = df.loc[i, '原價'] * 0.9

# ✅ 快：向量化
df['折扣後'] = df['原價'] * 0.9

# ❌ 慢：使用 apply with for loop
df['等級'] = df['分數'].apply(lambda x: 'A' if x >= 90 else 'B' if x >= 80 else 'C')

# ✅ 快：使用 np.where or pd.cut
df['等級'] = np.where(df['分數'] >= 90, 'A',
                     np.where(df['分數'] >= 80, 'B', 'C'))

# 或使用 pd.cut
df['等級'] = pd.cut(df['分數'], bins=[0, 79, 89, 100], labels=['C', 'B', 'A'])
```

### query & eval

```python
# query: 字串表達式篩選（較快）
df.query('銷售額 > 1000 and 地區 == "台北"')

# eval: 字串表達式計算（較快）
df.eval('利潤 = 銷售額 - 成本')

# 變數引用
threshold = 1000
df.query('銷售額 > @threshold')
```

---

## 📌 實用技巧

### 處理重複值

```python
# 檢查重複
df.duplicated()  # 回傳布林序列
df.duplicated(subset=['訂單編號'])  # 特定欄位

# 移除重複
df.drop_duplicates()
df.drop_duplicates(subset=['訂單編號'], keep='first')
```

### 處理缺失值

```python
# 檢查缺失
df.isnull().sum()
df.isnull().sum() / len(df)  # 缺失率

# 填充缺失
df.fillna(0)
df['欄位'].fillna(method='ffill')  # 向前填充
df['欄位'].fillna(method='bfill')  # 向後填充

# 移除缺失
df.dropna()  # 移除任何含缺失的列
df.dropna(subset=['重要欄位'])  # 只針對特定欄位
df.dropna(thresh=5)  # 至少有 5 個非缺失值才保留
```

### 字串處理

```python
# 基本操作
df['產品名稱'].str.lower()  # 轉小寫
df['產品名稱'].str.upper()  # 轉大寫
df['產品名稱'].str.strip()  # 去除前後空白

# 拆分
df['產品名稱'].str.split('_', expand=True)

# 包含
df[df['產品名稱'].str.contains('電子')]

# 替換
df['產品名稱'].str.replace('手機', 'Phone')

# 提取
df['產品名稱'].str.extract(r'(\d+)')  # 提取數字
```

### 排名

```python
# 基本排名
df['排名'] = df['銷售額'].rank(ascending=False)

# 組內排名
df['組內排名'] = df.groupby('產品類別')['銷售額'].rank(ascending=False)

# 百分位排名
df['百分位'] = df['銷售額'].rank(pct=True) * 100
```

---

## 📌 常用聚合函數

| 函數 | 說明 | 範例 |
|------|------|------|
| `sum()` | 總和 | `df['銷售額'].sum()` |
| `mean()` | 平均值 | `df['銷售額'].mean()` |
| `median()` | 中位數 | `df['銷售額'].median()` |
| `std()` | 標準差 | `df['銷售額'].std()` |
| `var()` | 變異數 | `df['銷售額'].var()` |
| `min()` | 最小值 | `df['銷售額'].min()` |
| `max()` | 最大值 | `df['銷售額'].max()` |
| `count()` | 計數 | `df['客戶ID'].count()` |
| `nunique()` | 不重複計數 | `df['客戶ID'].nunique()` |
| `quantile()` | 分位數 | `df['銷售額'].quantile(0.75)` |

---

這份速查表涵蓋了課程中 80% 會用到的 pandas 技巧。建議列印出來，隨時查閱！

*最後更新：2025-12-10*
