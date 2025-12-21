# Day 01: MultiIndex（階層式索引）完全掌握

## 🎯 學習目標（5-6 小時）

今天我們要完全掌握 pandas 最強大但也最容易混淆的功能：**MultiIndex（階層式索引）**

**學完後你將能夠：**
- ✅ 理解 MultiIndex 的概念與優勢
- ✅ 掌握 4 種建立 MultiIndex 的方法
- ✅ 熟練使用 loc、xs、IndexSlice 進行多層切片
- ✅ 靈活運用 stack/unstack/swaplevel 進行重塑
- ✅ 在實戰中使用 MultiIndex 分析 Olist 資料

---

## 📚 Part 1: MultiIndex 基礎（2小時）

### 1.1 什麼是 MultiIndex？（20分鐘）

**單層索引（普通 DataFrame）：**

```python
import pandas as pd

# 單層索引
df_single = pd.DataFrame({
    '地區': ['台北', '台北', '台中', '台中'],
    '類別': ['電腦', '手機', '電腦', '手機'],
    '營收': [1000, 800, 700, 600]
})

print(df_single)
```

輸出：
```
   地區  類別   營收
0  台北  電腦  1000
1  台北  手機   800
2  台中  電腦   700
3  台中  手機   600
```

**問題：** 如何快速選取「台北」的所有資料？需要用 `df[df['地區'] == '台北']`

---

**MultiIndex（階層式索引）：**

```python
# 建立 MultiIndex
df_multi = df_single.set_index(['地區', '類別'])

print(df_multi)
```

輸出：
```
           營收
地區  類別
台北  電腦  1000
     手機   800
台中  電腦   700
     手機   600
```

**優勢：** 可以直接用 `df_multi.loc['台北']` 選取「台北」的所有資料！

---

### 1.2 為什麼需要 MultiIndex？（10分鐘）

#### 優勢 1：更直觀的層次結構

Excel 樞紐表的「多列標籤」就是 MultiIndex 的概念：

**Excel 樞紐表：**
```
                    營收
地區    類別
台北    電腦        1000
       手機         800
台中    電腦         700
       手機         600
```

**pandas MultiIndex：** 完全對應！

---

#### 優勢 2：高效切片與選取

```python
# 單層索引：需要布林索引
df_single[df_single['地區'] == '台北']

# MultiIndex：直接切片
df_multi.loc['台北']
```

---

#### 優勢 3：支援複雜的數據重塑

```python
# stack / unstack / swaplevel / sort_index
# 在 MultiIndex 上操作非常強大
```

---

#### 優勢 4：與 GroupBy 完美結合

```python
# GroupBy 的結果通常是 MultiIndex
result = df.groupby(['地區', '類別'])['營收'].sum()
# result 就是一個 MultiIndex Series
```

---

### 1.3 建立 MultiIndex 的 4 種方法（50分鐘）

#### 方法 1：set_index() - 從現有欄位建立（最常用）⭐

```python
import pandas as pd

# 建立測試資料
df = pd.DataFrame({
    '地區': ['台北', '台北', '台中', '台中', '高雄', '高雄'],
    '類別': ['電腦', '手機', '電腦', '手機', '電腦', '手機'],
    '營收': [1000, 800, 700, 600, 500, 400],
    '訂單數': [10, 8, 7, 6, 5, 4]
})

# 建立 MultiIndex
df_multi = df.set_index(['地區', '類別'])

print(df_multi)
print(f"\nIndex 類型: {type(df_multi.index)}")
print(f"Index 層數: {df_multi.index.nlevels}")
```

**輸出：**
```
           營收  訂單數
地區  類別
台北  電腦  1000    10
     手機   800     8
台中  電腦   700     7
     手機   600     6
高雄  電腦   500     5
     手機   400     4

Index 類型: <class 'pandas.core.indexes.multi.MultiIndex'>
Index 層數: 2
```

**Excel 對照：**
- Excel 樞紐表：將「地區」和「類別」拖到「列」區域
- pandas：`df.set_index(['地區', '類別'])`

---

#### 方法 2：from_tuples() - 從 tuple 列表建立

```python
# 建立 tuple 列表
index_tuples = [
    ('台北', '電腦'),
    ('台北', '手機'),
    ('台中', '電腦'),
    ('台中', '手機'),
    ('高雄', '電腦'),
    ('高雄', '手機')
]

# 建立 MultiIndex
multi_index = pd.MultiIndex.from_tuples(
    index_tuples,
    names=['地區', '類別']
)

# 建立 DataFrame
df_multi = pd.DataFrame({
    '營收': [1000, 800, 700, 600, 500, 400],
    '訂單數': [10, 8, 7, 6, 5, 4]
}, index=multi_index)

print(df_multi)
```

**適用場景：** 當你已經有一組 tuple 資料時

---

#### 方法 3：from_arrays() - 從陣列列表建立

```python
# 建立兩個陣列
regions = ['台北', '台北', '台中', '台中', '高雄', '高雄']
categories = ['電腦', '手機', '電腦', '手機', '電腦', '手機']

# 建立 MultiIndex
multi_index = pd.MultiIndex.from_arrays(
    [regions, categories],
    names=['地區', '類別']
)

# 建立 DataFrame
df_multi = pd.DataFrame({
    '營收': [1000, 800, 700, 600, 500, 400],
    '訂單數': [10, 8, 7, 6, 5, 4]
}, index=multi_index)

print(df_multi)
```

**適用場景：** 當你有分開的兩個列表時

---

#### 方法 4：from_product() - 從笛卡爾積建立⭐

```python
# 定義每層的值
regions = ['台北', '台中', '高雄']
categories = ['電腦', '手機']

# 建立 MultiIndex（笛卡爾積）
multi_index = pd.MultiIndex.from_product(
    [regions, categories],
    names=['地區', '類別']
)

# 建立 DataFrame
df_multi = pd.DataFrame({
    '營收': [1000, 800, 700, 600, 500, 400],
    '訂單數': [10, 8, 7, 6, 5, 4]
}, index=multi_index)

print(df_multi)
```

**輸出：**
```
           營收  訂單數
地區  類別
台北  電腦  1000    10
     手機   800     8
台中  電腦   700     7
     手機   600     6
高雄  電腦   500     5
     手機   400     4
```

**適用場景：** 當你需要完整的組合（所有地區 × 所有類別）

**Excel 對照：** 這就像在 Excel 中建立一個完整的交叉表架構

---

### 1.4 MultiIndex 的屬性（30分鐘）

#### 基本屬性

```python
import pandas as pd

# 建立 MultiIndex DataFrame
df_multi = pd.DataFrame({
    '營收': [1000, 800, 700, 600, 500, 400],
    '訂單數': [10, 8, 7, 6, 5, 4]
}, index=pd.MultiIndex.from_product(
    [['台北', '台中', '高雄'], ['電腦', '手機']],
    names=['地區', '類別']
))

# 1. 查看層數
print(f"層數: {df_multi.index.nlevels}")  # 2

# 2. 查看層級名稱
print(f"層級名稱: {df_multi.index.names}")  # ['地區', '類別']

# 3. 查看所有層級的值
print(f"所有層級: {df_multi.index.levels}")
# [Index(['台北', '台中', '高雄'], dtype='object', name='地區'),
#  Index(['手機', '電腦'], dtype='object', name='類別')]

# 4. 查看每層的形狀
print(f"每層形狀: {df_multi.index.levshape}")  # (3, 2) -> 3個地區 × 2個類別

# 5. 查看索引編碼
print(f"編碼:\n{df_multi.index.codes}")
# [array([0, 0, 1, 1, 2, 2]), array([0, 1, 0, 1, 0, 1])]
```

---

#### 獲取特定層級

```python
# 獲取第 0 層（地區）
print(df_multi.index.get_level_values(0))
# Index(['台北', '台北', '台中', '台中', '高雄', '高雄'], dtype='object', name='地區')

# 獲取第 1 層（類別）
print(df_multi.index.get_level_values(1))
# Index(['電腦', '手機', '電腦', '手機', '電腦', '手機'], dtype='object', name='類別')

# 也可以用名稱獲取
print(df_multi.index.get_level_values('地區'))
print(df_multi.index.get_level_values('類別'))
```

---

#### 重新命名層級

```python
# 重新命名層級
df_multi.index = df_multi.index.set_names(['Region', 'Category'])

print(df_multi)
```

**輸出：**
```
                 營收  訂單數
Region  Category
台北     電腦      1000    10
        手機       800     8
台中     電腦       700     7
        手機       600     6
高雄     電腦       500     5
        手機       400     4
```

---

### 1.5 MultiIndex 基礎選取（30分鐘）

#### 選取外層（第 0 層）

```python
# 選取「台北」的所有資料
result = df_multi.loc['台北']

print(result)
```

**輸出：**
```
      營收  訂單數
類別
電腦  1000    10
手機   800     8
```

**注意：** 選取後降為單層索引（只剩「類別」）

---

#### 選取內層（特定組合）

```python
# 選取「台北 + 電腦」
result = df_multi.loc[('台北', '電腦')]

print(result)
```

**輸出：**
```
營收      1000
訂單數      10
Name: (台北, 電腦), dtype: int64
```

**注意：** 選取後變成 Series

---

#### 選取多個外層

```python
# 選取「台北」和「高雄」
result = df_multi.loc[['台北', '高雄']]

print(result)
```

**輸出：**
```
           營收  訂單數
地區  類別
台北  電腦  1000    10
     手機   800     8
高雄  電腦   500     5
     手機   400     4
```

---

#### 部分索引（Partial Indexing）

```python
# 使用 slice(None) 表示「全選」
# 選取所有地區的「電腦」類別
result = df_multi.loc[(slice(None), '電腦'), :]

print(result)
```

**輸出：**
```
           營收  訂單數
地區  類別
台北  電腦  1000    10
台中  電腦   700     7
高雄  電腦   500     5
```

**說明：**
- `slice(None)` 表示「不限制」，類似 SQL 的 `*`
- `(slice(None), '電腦')` 表示「所有地區的電腦」

---

### 1.6 實戰案例 1：建立 Olist 地區 × 類別 MultiIndex（30分鐘）

#### 載入 Olist 資料

```python
import pandas as pd
import numpy as np

# 載入資料
orders = pd.read_csv('/mnt/data/datasets/ecommerce/kaggle/olist/olist_orders_dataset.csv')
order_items = pd.read_csv('/mnt/data/datasets/ecommerce/kaggle/olist/olist_order_items_dataset.csv')
customers = pd.read_csv('/mnt/data/datasets/ecommerce/kaggle/olist/olist_customers_dataset.csv')
products = pd.read_csv('/mnt/data/datasets/ecommerce/kaggle/olist/olist_products_dataset.csv')
category_translation = pd.read_csv('/mnt/data/datasets/ecommerce/kaggle/olist/product_category_name_translation.csv')

# 只保留已送達的訂單
orders_delivered = orders[orders['order_status'] == 'delivered'].copy()

# 整合資料
df = (orders_delivered
      .merge(customers, on='customer_id', how='left')
      .merge(order_items, on='order_id', how='left')
      .merge(products, on='product_id', how='left')
      .merge(category_translation, on='product_category_name', how='left'))

print(f"✅ 資料整合完成：{len(df):,} 筆")
```

---

#### 建立地區 × 類別聚合

```python
# 按地區 × 類別聚合
region_category = df.groupby(['customer_state', 'product_category_name_english']).agg({
    'order_id': 'nunique',  # 訂單數
    'price': 'sum',         # 總營收
    'freight_value': 'sum'  # 總運費
}).reset_index()

region_category.columns = ['地區', '類別', '訂單數', '總營收', '總運費']

print(region_category.head(10))
```

---

#### 建立 MultiIndex

```python
# 設定 MultiIndex
df_multi = region_category.set_index(['地區', '類別'])

print(df_multi)
print(f"\n資料形狀: {df_multi.shape}")
print(f"Index 層數: {df_multi.index.nlevels}")
print(f"地區數: {df_multi.index.get_level_values(0).nunique()}")
print(f"類別數: {df_multi.index.get_level_values(1).nunique()}")
```

---

#### 分析：選取特定地區

```python
# 選取 SP（聖保羅州）的所有類別
sp_data = df_multi.loc['SP']

# 排序並顯示 Top 10 類別
sp_top10 = sp_data.sort_values('總營收', ascending=False).head(10)

print("🏆 聖保羅州 Top 10 類別：")
print(sp_top10)
```

---

#### 分析：比較不同地區的同一類別

```python
# 選取所有地區的「bed_bath_table」類別
# 需要使用進階切片技巧（下一部分詳細講解）
category_comparison = df_multi.xs('bed_bath_table', level='類別')

# 排序
category_comparison = category_comparison.sort_values('總營收', ascending=False).head(10)

print("🏠 bed_bath_table 類別 Top 10 地區：")
print(category_comparison)
```

---

## 📖 Part 2: MultiIndex 切片進階（2小時）

### 2.1 loc 多層切片完整語法（40分鐘）

#### 語法 1：單層選取

```python
# 選取外層（第 0 層）
df_multi.loc['SP']           # 選取 SP 州
df_multi.loc[['SP', 'RJ']]   # 選取 SP 和 RJ 州
```

---

#### 語法 2：雙層選取（tuple）

```python
# 選取特定組合
df_multi.loc[('SP', 'bed_bath_table')]           # 單個組合
df_multi.loc[[('SP', 'bed_bath_table'),
              ('RJ', 'bed_bath_table')]]          # 多個組合
```

---

#### 語法 3：部分索引（Partial Indexing）

```python
# 選取所有地區的特定類別
df_multi.loc[(slice(None), 'bed_bath_table'), :]

# 選取特定地區的所有類別（這其實就是單層選取）
df_multi.loc['SP']
```

**重要：** `slice(None)` 表示「不限制」，相當於「全選」

---

#### 語法 4：範圍切片

```python
# 選取地區範圍（需先排序）
df_multi_sorted = df_multi.sort_index()

# 選取 BA 到 SP 之間的所有地區
df_multi_sorted.loc['BA':'SP']

# 選取特定地區範圍的特定類別
df_multi_sorted.loc[('BA', 'bed_bath_table'):('SP', 'bed_bath_table')]
```

---

#### 語法 5：多層布林索引

```python
# 篩選訂單數 > 100 的組合
mask = df_multi['訂單數'] > 100
df_filtered = df_multi[mask]

print(df_filtered)
```

---

### 2.2 xs() - 跨層選取（Cross-Section）（30分鐘）

#### 什麼是 xs？

`xs()` 用於選取「跨層」的資料，特別適合選取內層（第 1 層及以上）

**語法：**
```python
df.xs(key, level=層級, axis=0)
```

---

#### 範例 1：選取特定類別（所有地區）

```python
# 使用 xs 選取所有地區的「bed_bath_table」類別
result = df_multi.xs('bed_bath_table', level='類別')

print(result)
```

**輸出：**
```
      訂單數   總營收    總運費
地區
SP    523   52300.0  4500.0
RJ    320   31200.0  2800.0
MG    210   20500.0  1900.0
...
```

**注意：** 選取後只剩「地區」這一層索引

---

#### 範例 2：選取多個類別

```python
# 選取多個類別（需要用 loc 或迴圈）
categories = ['bed_bath_table', 'health_beauty', 'sports_leisure']

results = []
for cat in categories:
    result = df_multi.xs(cat, level='類別')
    result['類別'] = cat  # 加回類別欄位
    results.append(result)

df_selected = pd.concat(results)

print(df_selected)
```

---

#### xs vs loc 比較

| 方法 | 優勢 | 劣勢 |
|-----|------|------|
| `loc[(slice(None), 'key')]` | 保留 MultiIndex 結構 | 語法較複雜 |
| `xs('key', level=1)` | 語法簡潔 | 降層（失去 MultiIndex） |

**建議：**
- 需要保留 MultiIndex 結構 → 用 `loc`
- 只想快速查看某個切面 → 用 `xs`

---

### 2.3 IndexSlice - 切片神器（40分鐘）⭐

#### 什麼是 IndexSlice？

`IndexSlice` 是 pandas 提供的便捷切片工具，可以更優雅地處理 MultiIndex 切片。

**語法：**
```python
idx = pd.IndexSlice
df.loc[idx[外層條件, 內層條件], 欄位條件]
```

---

#### 範例 1：基礎用法

```python
# 建立 IndexSlice 物件
idx = pd.IndexSlice

# 選取所有地區的「bed_bath_table」類別
result = df_multi.loc[idx[:, 'bed_bath_table'], :]

print(result)
```

**說明：**
- `idx[:, 'bed_bath_table']` 相當於 `(slice(None), 'bed_bath_table')`
- `:` 表示「全選」，比 `slice(None)` 更直觀

---

#### 範例 2：多重條件

```python
# 選取 SP 和 RJ 的 bed_bath_table 和 health_beauty 類別
result = df_multi.loc[idx[['SP', 'RJ'], ['bed_bath_table', 'health_beauty']], :]

print(result)
```

---

#### 範例 3：範圍切片

```python
# 先排序（範圍切片需要排序）
df_multi_sorted = df_multi.sort_index()

# 選取地區 BA 到 SP，類別 'a' 開頭到 'c' 開頭
result = df_multi_sorted.loc[idx['BA':'SP', 'a':'c'], :]

print(result)
```

---

#### 範例 4：結合欄位選取

```python
# 只選取「總營收」欄位
result = df_multi.loc[idx[:, 'bed_bath_table'], '總營收']

print(result)
```

---

#### IndexSlice 實戰：篩選高營收組合

```python
idx = pd.IndexSlice

# 先排序
df_multi_sorted = df_multi.sort_index()

# 選取訂單數 > 50 且總營收 > 50000 的組合
mask = (df_multi_sorted['訂單數'] > 50) & (df_multi_sorted['總營收'] > 50000)
result = df_multi_sorted[mask]

# 只顯示 Top 5 地區的 Top 3 類別
top_regions = result.groupby(level=0)['總營收'].sum().nlargest(5).index
top_categories = result.groupby(level=1)['總營收'].sum().nlargest(3).index

final_result = result.loc[idx[top_regions, top_categories], :]

print("🏆 Top 5 地區 × Top 3 類別：")
print(final_result.sort_values('總營收', ascending=False))
```

---

### 2.4 實戰案例 2：地區 × 類別深度分析（30分鐘）

#### 分析 1：各地區的熱銷類別

```python
# 找出每個地區的 Top 3 類別
idx = pd.IndexSlice

top_categories_by_region = (
    df_multi
    .groupby(level=0)
    .apply(lambda x: x.nlargest(3, '總營收'))
)

print("📊 各地區 Top 3 類別：")
print(top_categories_by_region)
```

---

#### 分析 2：類別在不同地區的表現

```python
# 選取 Top 5 類別
top_categories = df_multi.groupby(level=1)['總營收'].sum().nlargest(5).index

# 比較這些類別在不同地區的表現
idx = pd.IndexSlice
comparison = df_multi.loc[idx[:, top_categories], :]

# 轉換成寬表（方便比較）
comparison_pivot = comparison.reset_index().pivot(
    index='地區',
    columns='類別',
    values='總營收'
)

print("📊 Top 5 類別在各地區的表現：")
print(comparison_pivot.head(10))
```

---

#### 分析 3：計算每個地區的類別集中度

```python
# 計算每個地區的營收集中度（Top 3 類別佔比）
def calculate_concentration(group):
    total = group['總營收'].sum()
    top3_sum = group.nlargest(3, '總營收')['總營收'].sum()
    return top3_sum / total * 100 if total > 0 else 0

concentration = df_multi.groupby(level=0).apply(calculate_concentration)
concentration = concentration.sort_values(ascending=False)

print("📊 各地區營收集中度（Top 3 類別佔比）：")
print(concentration.head(10))
```

---

## 🔥 Part 3: MultiIndex 重塑（2小時）

### 3.1 stack / unstack 深度理解（50分鐘）

#### 什麼是 stack 和 unstack？

- **stack：** 將欄位變成索引（寬表 → 長表）
- **unstack：** 將索引變成欄位（長表 → 寬表）

---

#### unstack - 長表變寬表

**範例：將類別從索引移到欄位**

```python
# 原始 MultiIndex DataFrame
print("原始資料（長表）：")
print(df_multi.head(10))

# unstack：將「類別」從索引移到欄位
df_wide = df_multi.unstack(level='類別')

print("\nunstack 後（寬表）：")
print(df_wide.head())
```

**輸出（寬表）：**
```
        訂單數                            總營收                          總運費
類別  bed_bath  health_beauty  ...  bed_bath  health_beauty  ...  bed_bath  health_beauty
地區
SP      523.0          320.0   ...   52300.0        31200.0   ...    4500.0        2800.0
RJ      320.0          210.0   ...   31200.0        20500.0   ...    2800.0        1900.0
...
```

**Excel 對照：**
- Excel 樞紐表：將「類別」從列拖到欄
- pandas：`df.unstack(level='類別')`

---

#### stack - 寬表變長表

```python
# 將寬表還原成長表
df_long = df_wide.stack(level='類別')

print("stack 後（還原成長表）：")
print(df_long.head(10))
```

**Excel 對照：**
- Power Query: Unpivot Columns
- pandas: `df.stack()`

---

#### 指定層級 unstack

```python
# unstack 第 0 層（地區）
df_wide_region = df_multi.unstack(level=0)

print("unstack 地區（將地區變成欄位）：")
print(df_wide_region.head())
```

**輸出：**
```
                訂單數                    總營收
地區                SP    RJ    MG  ...      SP      RJ      MG
類別
bed_bath_table  523.0 320.0 210.0  ...  52300.0 31200.0 20500.0
health_beauty   320.0 210.0 150.0  ...  31200.0 20500.0 14800.0
...
```

---

#### 處理缺失值

```python
# unstack 可能產生缺失值（某些組合不存在）
df_wide_with_na = df_multi.unstack(level='類別')

# 填充缺失值
df_wide_filled = df_multi.unstack(level='類別', fill_value=0)

print("填充缺失值後：")
print(df_wide_filled.head())
```

---

#### stack / unstack 實戰技巧

**技巧 1：多層 unstack**

```python
# 如果有 3 層索引，可以 unstack 多層
# df.unstack(level=[1, 2])
```

**技巧 2：與 pivot_table 的區別**

| 方法 | 適用場景 | 優勢 |
|-----|---------|------|
| `unstack()` | 已經有 MultiIndex | 簡潔、快速 |
| `pivot_table()` | 原始資料（未分組） | 靈活、功能強大 |

---

### 3.2 swaplevel - 交換層級順序（20分鐘）

#### 什麼是 swaplevel？

`swaplevel()` 用於交換 MultiIndex 的層級順序。

---

#### 範例：交換地區和類別

```python
# 原始：地區 × 類別
print("原始索引順序：")
print(df_multi.head())

# 交換層級：類別 × 地區
df_swapped = df_multi.swaplevel(0, 1)

print("\n交換層級後：")
print(df_swapped.head())
```

**輸出：**
```
原始索引順序：
           訂單數   總營收
地區  類別
SP   bed_bath  523  52300.0
     health    320  31200.0
...

交換層級後：
           訂單數   總營收
類別         地區
bed_bath    SP   523  52300.0
health      SP   320  31200.0
...
```

---

#### 為什麼要交換層級？

**原因 1：改變排序基準**

```python
# 按類別排序（交換後）
df_swapped_sorted = df_swapped.sort_index()

print("按類別排序：")
print(df_swapped_sorted.head(10))
```

---

**原因 2：改變切片方式**

```python
# 原始：選取特定地區很方便
df_multi.loc['SP']

# 交換後：選取特定類別很方便
df_swapped.loc['bed_bath_table']
```

---

### 3.3 sort_index - 排序 MultiIndex（20分鐘）

#### 基礎排序

```python
# 按索引排序（預設按所有層級）
df_sorted = df_multi.sort_index()

print(df_sorted.head(10))
```

---

#### 指定層級排序

```python
# 只按第 1 層（類別）排序
df_sorted_by_category = df_multi.sort_index(level=1)

print(df_sorted_by_category.head(10))
```

---

#### 多層排序（指定順序）

```python
# 先按類別排序，再按地區排序
df_sorted_multi = df_multi.sort_index(level=['類別', '地區'])

print(df_sorted_multi.head(10))
```

---

#### 降序排序

```python
# 按地區降序排序
df_sorted_desc = df_multi.sort_index(ascending=False)

print(df_sorted_desc.head(10))
```

---

### 3.4 實戰案例 3：建立地區 × 類別報表（30分鐘）

#### 需求：建立完整的地區 × 類別營收報表

```python
import pandas as pd
import numpy as np

# 載入並整合資料（前面已載入）

# 步驟 1：按地區 × 類別聚合
report = df.groupby(['customer_state', 'product_category_name_english']).agg({
    'order_id': 'nunique',
    'price': ['sum', 'mean'],
    'freight_value': 'sum'
}).reset_index()

# 扁平化欄位名稱
report.columns = ['地區', '類別', '訂單數', '總營收', '平均單價', '總運費']

# 計算客單價
report['客單價'] = report['總營收'] / report['訂單數']

# 步驟 2：建立 MultiIndex
report_multi = report.set_index(['地區', '類別'])

print("📊 完整報表：")
print(report_multi.head(20))
```

---

#### 進階：加入小計與總計

```python
# 計算地區小計
region_subtotal = report.groupby('地區').agg({
    '訂單數': 'sum',
    '總營收': 'sum',
    '總運費': 'sum'
}).reset_index()

region_subtotal['類別'] = '小計'
region_subtotal['平均單價'] = np.nan
region_subtotal['客單價'] = region_subtotal['總營收'] / region_subtotal['訂單數']

# 計算總計
total = pd.DataFrame([{
    '地區': '總計',
    '類別': '',
    '訂單數': report['訂單數'].sum(),
    '總營收': report['總營收'].sum(),
    '平均單價': np.nan,
    '總運費': report['總運費'].sum(),
    '客單價': report['總營收'].sum() / report['訂單數'].sum()
}])

# 合併
report_with_total = pd.concat([report, region_subtotal, total], ignore_index=True)

# 建立 MultiIndex
report_final = report_with_total.set_index(['地區', '類別'])

print("📊 含小計與總計的報表：")
print(report_final.tail(20))
```

---

#### 輸出：轉換成 Excel 樞紐表格式

```python
# unstack 成寬表
report_pivot = report_multi['總營收'].unstack(level='類別', fill_value=0)

print("📊 樞紐表格式（地區 × 類別營收）：")
print(report_pivot.head(10))

# 儲存成 Excel
report_pivot.to_excel('output/region_category_revenue.xlsx')
print("✅ 報表已儲存至 output/region_category_revenue.xlsx")
```

---

## 🎯 Part 4: 綜合實戰練習（30分鐘）

### 練習 1：建立月份 × 地區 × 類別 3 層 MultiIndex

**需求：** 分析每月、每個地區、每個類別的表現

```python
# 提示代碼
# 1. 新增年月欄位
df['year_month'] = pd.to_datetime(df['order_purchase_timestamp']).dt.to_period('M')

# 2. 按 3 個維度聚合
result = df.groupby(['year_month', 'customer_state', 'product_category_name_english']).agg({
    'order_id': 'nunique',
    'price': 'sum'
}).reset_index()

result.columns = ['年月', '地區', '類別', '訂單數', '總營收']

# 3. 建立 3 層 MultiIndex
result_multi = result.set_index(['年月', '地區', '類別'])

print(result_multi.head(20))
```

**問題：**
1. 如何選取 2018-01 的所有資料？
2. 如何選取所有月份的 SP 州資料？
3. 如何選取所有月份、所有地區的 bed_bath_table 類別？

---

### 練習 2：使用 IndexSlice 篩選高價值組合

**需求：** 找出 2018 年 1-3 月、SP 和 RJ 州、總營收 > 10000 的類別

```python
idx = pd.IndexSlice

# 先排序
result_sorted = result_multi.sort_index()

# 篩選
filtered = result_sorted.loc[
    idx['2018-01':'2018-03', ['SP', 'RJ'], :],
    :
]

# 再篩選營收 > 10000
high_value = filtered[filtered['總營收'] > 10000]

print("🏆 高價值組合：")
print(high_value)
```

---

### 練習 3：建立月度趨勢報表（unstack 應用）

**需求：** 將月份 × 類別的營收資料轉換成寬表（月份為列，類別為欄）

```python
# 先聚合成月份 × 類別
monthly_category = df.groupby([
    df['order_purchase_timestamp'].dt.to_period('M'),
    'product_category_name_english'
])['price'].sum().reset_index()

monthly_category.columns = ['年月', '類別', '營收']

# 建立 MultiIndex
monthly_category_multi = monthly_category.set_index(['年月', '類別'])

# unstack 成寬表
monthly_trend = monthly_category_multi.unstack(level='類別', fill_value=0)

print("📊 月度類別趨勢（寬表）：")
print(monthly_trend)

# 只看 Top 10 類別
top10_categories = monthly_category.groupby('類別')['營收'].sum().nlargest(10).index
monthly_trend_top10 = monthly_trend['營收'][top10_categories]

print("\n📊 Top 10 類別月度趨勢：")
print(monthly_trend_top10)
```

---

## 📝 Excel → pandas 對照表

### MultiIndex 概念對照

| Excel 功能 | pandas 對應 | 說明 |
|-----------|------------|------|
| 樞紐表多列標籤 | MultiIndex | 階層式索引 |
| 將欄位拖到「列」 | `df.set_index()` | 建立索引 |
| 樞紐表展開/摺疊 | `df.loc['key']` | 選取層級 |
| 樞紐表小計 | `margins=True` | 加入小計 |

### 樞紐表轉換對照

| Excel 操作 | pandas 對應 |
|-----------|------------|
| 將「類別」從列拖到欄 | `df.unstack(level='類別')` |
| 將「類別」從欄拖到列 | `df.stack(level='類別')` |
| 交換列的順序 | `df.swaplevel()` |
| 按列排序 | `df.sort_index()` |

---

## 📚 總結與複習

### ✅ 今天學到的核心技能

1. **MultiIndex 建立（4 種方法）**
   - `set_index()` - 從現有欄位（最常用）
   - `from_tuples()` - 從 tuple 列表
   - `from_arrays()` - 從陣列列表
   - `from_product()` - 從笛卡爾積

2. **MultiIndex 選取**
   - 單層選取：`df.loc['key']`
   - 雙層選取：`df.loc[('key1', 'key2')]`
   - 部分索引：`df.loc[(slice(None), 'key'), :]`
   - `xs()` 跨層選取
   - `IndexSlice` 優雅切片

3. **MultiIndex 重塑**
   - `unstack()` - 長表 → 寬表
   - `stack()` - 寬表 → 長表
   - `swaplevel()` - 交換層級
   - `sort_index()` - 排序

4. **實戰應用**
   - Olist 地區 × 類別分析
   - 建立完整報表
   - 多維度深度分析

---

### 🎓 下一步學習

**明天（Day 02）：GroupBy 進階聚合**
- 命名聚合（Named Aggregation）
- Transform vs Aggregate
- Filter 群組篩選
- 自訂聚合函數

---

### 💡 學習建議

1. **反覆練習 4 種建立方法** - 每種都要親手寫一遍
2. **熟練 IndexSlice** - 這是最優雅的切片方式
3. **理解 stack/unstack** - 與 Excel 樞紐表對照思考
4. **完成實戰案例** - 使用 Olist 真實資料

---

### 📖 延伸閱讀

- [pandas 官方文檔：MultiIndex](https://pandas.pydata.org/docs/user_guide/advanced.html)
- [pandas 官方文檔：Reshaping and Pivot Tables](https://pandas.pydata.org/docs/user_guide/reshaping.html)

---

**🎊 恭喜完成 Day 01！明天見！**
