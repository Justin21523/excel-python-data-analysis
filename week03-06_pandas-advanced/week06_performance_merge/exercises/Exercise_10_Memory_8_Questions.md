# Exercise 10: 記憶體優化 - 8 題

## 準備工作

```python
import pandas as pd
import numpy as np

# 載入數據
orders = pd.read_csv('/home/justin/web-projects/excel-python-data-analysis/week03-06_pandas-advanced/data/olist_orders_dataset.csv')
customers = pd.read_csv('/home/justin/web-projects/excel-python-data-analysis/week03-06_pandas-advanced/data/olist_customers_dataset.csv')
order_items = pd.read_csv('/home/justin/web-projects/excel-python-data-analysis/week03-06_pandas-advanced/data/olist_order_items_dataset.csv')
reviews = pd.read_csv('/home/justin/web-projects/excel-python-data-analysis/week03-06_pandas-advanced/data/olist_order_reviews_dataset.csv')
products = pd.read_csv('/home/justin/web-projects/excel-python-data-analysis/week03-06_pandas-advanced/data/olist_products_dataset.csv')
```

---

## 🟢 入門題 (Easy)

### 題目 1: 分析 orders 表的記憶體使用

**題目描述：**

使用 memory_usage(deep=True) 分析 orders 表，找出：
1. 記憶體使用最多的前 3 列
2. 整個 DataFrame 的總記憶體 (MB)
3. 記憶體使用最多的列佔總記憶體的百分比

**預期輸出：**
```
記憶體使用最多的 3 列:
  order_purchase_timestamp: 7.58 MB
  order_delivered_customer_at: 7.60 MB
  order_estimated_delivery_at: 7.46 MB

總記憶體: 49.97 MB

佔比最高: 15.2%
```

---

### 題目 2: 簡單的 Dtype 轉換

**題目描述：**

將 orders 表中的所有時間戳列轉換為 datetime64 類型，計算：
1. 轉換前的總記憶體
2. 轉換後的總記憶體
3. 減少的百分比

**提示：**
- 時間戳列包含 'timestamp' 或 'at' 字樣
- 使用 pd.to_datetime()

**預期輸出：**
```
優化前: 49.97 MB
優化後: 12.39 MB
減少: 75.2%
```

---

### 題目 3: 識別應該使用 category 的列

**題目描述：**

在 customers 表中，找出所有應該轉換為 category 類型的列（條件：唯一值 < 50 且比例 < 30%），並列出：
1. 列名
2. 唯一值數量
3. 唯一值比例

**預期輸出：**
```
應該使用 category:
  customer_state: 27 唯一值 (0.03%)
  customer_city: 4119 唯一值 (4.14%)  ✗ (太多唯一值)
```

---

## 🟡 進階題 (Medium)

### 題目 4: 完整的 DataFrame 優化

**題目描述：**

編寫一個 optimize_dataframe(df) 函數，對任意 DataFrame 進行優化：
1. 轉換所有時間戳為 datetime64
2. 轉換合適的 object 列為 category
3. 縮小適當的整數類型

並應用到 order_items 表，計算優化效果。

**函數簽名：**
```python
def optimize_dataframe(df):
    """
    自動優化 DataFrame 的記憶體使用
    返回優化後的 df 和優化統計信息
    """
    pass
```

**預期輸出：**
```
優化效果:
  order_id: object → object (不變)
  price: float64 → float32 (50% 減少)
  seller_id: object → object (不變)

優化前: 8.43 MB
優化後: 1.54 MB
減少: 81.7%
```

---

### 題目 5: 整數類型縮小

**題目描述：**

在 customers 表中：
1. 找出所有 int64 列
2. 對每列計算最小和最大值
3. 選擇最合適的整數類型（int8, int16, int32）
4. 計算節省的記憶體

**提示：**
```
int8:  -128 到 127
int16: -32,768 到 32,767
int32: -2,147,483,648 到 2,147,483,647
uint8: 0 到 255
uint16: 0 到 65,535
```

**預期輸出：**
```
customer_zip_code_prefix:
  原始類型: int64 (8 bytes)
  最小值: 1000, 最大值: 99950
  推薦類型: int16 (2 bytes)
  節省: 75%
```

---

### 題目 6: Chunking 處理大文件

**題目描述：**

使用 chunking 方式讀取 order_items 表（chunksize=50000），分塊進行優化，並計算：
1. 每個 chunk 的平均大小
2. 總共有多少個 chunk
3. 如果一次性加載需要多少記憶體
4. 使用 chunking 能節省多少記憶體

**預期輸出：**
```
Chunking 分析:
  總行數: 112650
  Chunk 大小: 50000
  Chunk 數: 3
  每個 chunk 平均: 2.10 MB (優化後)
  一次性加載: 8.43 MB
  使用 chunking 所需: 2.10 MB (峰值)
  節省: 75.1%
```

---

## 🔴 高級題 (Hard)

### 題目 7: 並行優化 + 記憶體監控

**題目描述：**

創建一個完整的記憶體優化 Pipeline，包括：
1. 監控當前記憶體使用
2. 按順序優化 orders, customers, order_items, reviews
3. 每個表優化前後的記憶體對比
4. 整體優化效果統計
5. 記憶體峰值監控

**函數簽名：**
```python
def memory_optimization_pipeline(df_list, max_memory_mb=4000):
    """
    完整的內存優化 Pipeline

    參數:
    - df_list: DataFrame 列表
    - max_memory_mb: 最大允許記憶體 (MB)

    返回:
    - 優化後的 DataFrame 列表
    - 優化統計報告
    """
    pass
```

**預期輸出：**
```
記憶體優化 Pipeline
═══════════════════════════════════════

表          優化前    優化後    減少幅度    當前內存
────────────────────────────────────────
orders      49.97 MB  3.82 MB   92.4%      3.82 MB
customers    6.18 MB  4.95 MB   19.9%      8.77 MB
items        8.43 MB  1.54 MB   81.7%      10.31 MB
reviews     12.56 MB  2.18 MB   82.6%      12.49 MB

總體優化: 77.14 MB → 12.49 MB (83.8% 減少)
記憶體峰值: 12.49 MB (< 4000 MB ✓)
```

---

### 題目 8: 大文件處理 + 即時分析

**題目描述：**

實現一個完整的流式數據處理系統：
1. 分塊讀取 order_items（每塊 25000 行）
2. 對每個塊進行優化
3. 實時統計：
   - 總銷售額
   - 平均價格
   - 商品數量統計
4. 監控記憶體使用（防止超過 3GB）
5. 生成最終報告

**函數簽名：**
```python
def streaming_analysis(file_path, chunksize=25000, memory_limit_gb=3.0):
    """
    流式數據分析

    實時計算統計信息，同時控制記憶體
    """
    pass
```

**預期輸出：**
```
流式分析報告
═══════════════════════════════════════

Chunk 1 (25000 行): 已處理, 內存 0.95 MB
Chunk 2 (25000 行): 已處理, 內存 0.95 MB
Chunk 3 (25000 行): 已處理, 內存 0.95 MB
Chunk 4 (25000 行): 已處理, 內存 0.95 MB
Chunk 5 (12650 行): 已處理, 內存 0.50 MB

統計結果:
  總行數: 112650
  總銷售額: R$ 4,876,234.50
  平均價格: R$ 43.21
  最高價格: R$ 13,664.31
  商品種類: 32,951

記憶體峰值: 0.95 MB (< 3000 MB ✓)
```

---

## 答案提交格式

### 針對每個題目，請提交：

**題目 1-3 (簡單題):**
```python
# 題目 1
# 代碼
...
# 結果輸出
```

**題目 4-6 (進階題):**
```python
# 題目 4 - 函數定義
def optimize_dataframe(df):
    ...
    return optimized_df, statistics

# 應用和結果
optimized_order_items, stats = optimize_dataframe(order_items)
print(stats)
```

**題目 7-8 (高級題):**
```python
# 完整的函數 + 應用
def memory_optimization_pipeline(...):
    ...
    return optimized_dfs, report

# 執行和驗證
optimized, report = memory_optimization_pipeline([orders, customers, order_items, reviews])
print(report)
```

---

## 評分標準

### 記憶體優化效果
- 達成 50% 優化：20 分
- 達成 70% 優化：30 分
- 達成 80%+ 優化：40 分

### 代碼質量
- 正確性：20 分
- 可讀性：20 分
- 效率：20 分

### 總分：100 分

---

## 延伸閱讀

- [Pandas Memory Usage](https://pandas.pydata.org/docs/reference/api/pandas.DataFrame.memory_usage.html)
- [Pandas Data Types](https://pandas.pydata.org/docs/user_guide/basics.html#dtypes)
- [Memory Profiler](https://pypi.org/project/memory-profiler/)

---

## 提示

1. **always check before converting**: 某些列可能有 NaN，轉換時要小心
2. **category 的陷阱**: 當唯一值數量接近行數時，category 會更耗內存
3. **浮點精度**: float64 → float32 時注意精度丟失
4. **時間戳優化**: 這通常是記憶體使用最多的地方
5. **監控很重要**: 使用 psutil 監控實際記憶體使用

---

## 自我檢查清單

- [ ] 理解 memory_usage(deep=True) 的含義
- [ ] 能夠識別應該優化的列
- [ ] 掌握 Dtype 轉換的方法
- [ ] 實現了 downcast_integer 函數
- [ ] 理解 chunking 的優勢
- [ ] 能夠監控記憶體防止溢出
- [ ] 實現了完整的優化 Pipeline

---

**下一章：Exercise 11 - 向量化操作 10 題**
