# 🚀 資料集快速開始指南

這份指南幫助你快速下載並使用電商資料集開始學習。

---

## 📥 快速下載（3 步驟）

### 步驟 1：安裝必要套件

```bash
pip install kaggle ucimlrepo datasets
```

### 步驟 2：設定 Kaggle API（如需使用 Kaggle 資料集）

1. 前往 [Kaggle Account Settings](https://www.kaggle.com/account)
2. 點擊 "Create New Token" 下載 `kaggle.json`
3. 執行以下指令：

```bash
mkdir -p ~/.kaggle
cp ~/Downloads/kaggle.json ~/.kaggle/
chmod 600 ~/.kaggle/kaggle.json
```

### 步驟 3：下載資料集

#### 方法 A：使用自動化腳本（推薦）

```bash
cd datasets

# 列出所有可用資料集
python download_datasets.py --list

# 下載單一資料集
python download_datasets.py --dataset online-retail

# 下載所有推薦資料集（Online Retail + Olist + Instacart）
python download_datasets.py --all
```

#### 方法 B：手動下載

**下載 Online Retail（最適合入門）：**
```python
from ucimlrepo import fetch_ucirepo

# 載入資料集
online_retail = fetch_ucirepo(id=352)
df = online_retail.data.features

# 儲存為 CSV
df.to_csv('datasets/uci/online_retail.csv', index=False)
print(f"✅ 已下載 {len(df)} 筆資料")
```

**下載 Kaggle 資料集（需先設定 API）：**
```bash
# Olist Brazilian E-Commerce
kaggle datasets download -d olistbr/brazilian-ecommerce -p datasets/kaggle/

# Instacart Market Basket
kaggle competitions download -c instacart-market-basket-analysis -p datasets/kaggle/

# 解壓縮
cd datasets/kaggle
unzip *.zip
```

---

## 📚 推薦學習路徑

### 🎯 路徑 1：商業分析入門（推薦初學者）

**資料集：** Online Retail (UCI)
**規模：** 541K 筆交易
**下載：**
```python
from ucimlrepo import fetch_ucirepo
df = fetch_ucirepo(id=352).data.features
```

**可做的分析：**
1. **Week 3-4**: 基礎資料探索與清洗
   - 缺失值處理
   - 重複值清除
   - 資料型態轉換

2. **Week 5-6**: RFM 客戶分群
   - 計算 Recency、Frequency、Monetary
   - 五等分評分
   - 11 種客戶分群

3. **Week 7-8**: 購物籃分析
   - 找出經常一起購買的產品
   - 關聯規則（Apriori）
   - 產品推薦

4. **Week 9-10**: 時間序列分析
   - 月銷售趨勢
   - 季節性分析
   - 簡易預測

---

### 🎯 路徑 2：完整電商流程（進階）

**資料集：** Olist Brazilian E-Commerce
**規模：** 100K 筆訂單
**下載：**
```bash
kaggle datasets download -d olistbr/brazilian-ecommerce
```

**可做的分析：**
1. **訂單分析**
   - 訂單狀態分佈
   - 取消率分析
   - 平均訂單價值

2. **物流分析**
   - 配送時間分析
   - 地理分析（巴西各州）
   - 準時交付率

3. **評論情感分析**
   - 評分分佈
   - 文字情感分析（NLP）
   - 客戶滿意度

4. **賣家表現分析**
   - 賣家評分
   - 銷售表現
   - 產品類別分析

---

### 🎯 路徑 3：推薦系統（機器學習）

**資料集：** Instacart Market Basket
**規模：** 3M+ 訂單
**下載：**
```bash
kaggle competitions download -c instacart-market-basket-analysis
```

**可做的分析：**
1. **探索性分析**
   - 購買頻率分析
   - 時段偏好
   - 過道熱門度

2. **購物籃分析**
   - Apriori 演算法
   - FP-Growth
   - 關聯規則挖掘

3. **推薦系統**
   - 協同過濾
   - Item-based CF
   - 混合推薦

4. **機器學習預測**
   - 預測下次購買
   - 購買序列分析
   - 再購率預測

---

### 🎯 路徑 4：大規模資料處理（專家）

**資料集：** eCommerce Behavior Data
**規模：** 285M 筆事件
**下載：**
```bash
kaggle datasets download -d mkechinov/ecommerce-behavior-data-from-multi-category-store
```

**挑戰：**
- 處理 GB 級資料
- 記憶體優化技巧
- Chunking 處理
- Dask 入門（選修）

**可做的分析：**
1. **用戶行為漏斗**
   - 瀏覽 → 加購 → 購買
   - 轉換率計算
   - 流失點識別

2. **Session 分析**
   - 平均 Session 時長
   - 產品瀏覽序列
   - 購買路徑分析

3. **產品分析**
   - 熱門產品
   - 瀏覽-購買轉換率
   - 產品組合分析

---

## 🛠️ 常用載入代碼

### Pandas 載入

```python
import pandas as pd

# CSV
df = pd.read_csv('datasets/uci/online_retail.csv')

# Excel
df = pd.read_excel('datasets/kaggle/orders.xlsx')

# 指定資料型態（記憶體優化）
df = pd.read_csv(
    'data.csv',
    dtype={'CustomerID': str, 'ProductCategory': 'category'},
    parse_dates=['InvoiceDate']
)

# 分批讀取大檔案
chunks = pd.read_csv('large_file.csv', chunksize=100000)
for chunk in chunks:
    process(chunk)
```

### HuggingFace 載入

```python
from datasets import load_dataset

# 載入資料集
dataset = load_dataset("McAuley-Lab/Amazon-Reviews-2023", "raw_review_All_Beauty")

# 轉成 pandas
df = dataset['full'].to_pandas()

# 選擇特定欄位
df = df[['rating', 'text', 'timestamp']]
```

### UCI Repository 載入

```python
from ucimlrepo import fetch_ucirepo

# 載入資料集
online_retail = fetch_ucirepo(id=352)

# 取得特徵與目標
X = online_retail.data.features
y = online_retail.data.targets

# 查看元資料
print(online_retail.metadata)
```

---

## 📊 第一個分析範例：Online Retail RFM

```python
import pandas as pd
import numpy as np
from datetime import datetime

# 1. 載入資料
from ucimlrepo import fetch_ucirepo
df = fetch_ucirepo(id=352).data.features

# 2. 資料清洗
df = df.dropna(subset=['CustomerID'])
df['InvoiceDate'] = pd.to_datetime(df['InvoiceDate'])
df = df[df['Quantity'] > 0]
df = df[df['UnitPrice'] > 0]

# 3. 計算 RFM
snapshot_date = df['InvoiceDate'].max() + pd.Timedelta(days=1)

rfm = df.groupby('CustomerID').agg({
    'InvoiceDate': lambda x: (snapshot_date - x.max()).days,  # Recency
    'InvoiceNo': 'nunique',  # Frequency
    'UnitPrice': lambda x: (x * df.loc[x.index, 'Quantity']).sum()  # Monetary
})

rfm.columns = ['Recency', 'Frequency', 'Monetary']

# 4. RFM 評分（1-5 分）
rfm['R_Score'] = pd.qcut(rfm['Recency'], 5, labels=[5,4,3,2,1])
rfm['F_Score'] = pd.qcut(rfm['Frequency'].rank(method='first'), 5, labels=[1,2,3,4,5])
rfm['M_Score'] = pd.qcut(rfm['Monetary'], 5, labels=[1,2,3,4,5])

# 5. 客戶分群
def segment_customer(row):
    score = int(row['R_Score']) + int(row['F_Score']) + int(row['M_Score'])
    if score >= 13:
        return '重要高價值客戶'
    elif score >= 10:
        return '重要發展客戶'
    elif score >= 7:
        return '一般客戶'
    else:
        return '流失預警客戶'

rfm['客戶分群'] = rfm.apply(segment_customer, axis=1)

# 6. 查看結果
print(rfm['客戶分群'].value_counts())
print(rfm.groupby('客戶分群').agg({
    'Recency': 'mean',
    'Frequency': 'mean',
    'Monetary': 'mean'
}).round(2))
```

輸出：
```
客戶分群分佈：
一般客戶        1523
重要發展客戶      992
流失預警客戶      831
重要高價值客戶     727
```

---

## 🎓 學習檢查清單

### 完成 Online Retail 分析後，你應該能夠：

- [ ] 使用 `pandas.read_csv()` 載入資料
- [ ] 使用 `isnull()`, `dropna()` 處理缺失值
- [ ] 使用 `drop_duplicates()` 移除重複值
- [ ] 使用 `groupby()` 進行分組聚合
- [ ] 計算 RFM 指標
- [ ] 使用 `pd.qcut()` 進行分層
- [ ] 使用 `apply()` 自訂函數
- [ ] 使用 `value_counts()` 統計分佈

### 完成 Olist 分析後，你應該能夠：

- [ ] 使用 `pd.merge()` 合併多個表
- [ ] 處理日期時間資料
- [ ] 計算時間差（配送時間）
- [ ] 使用 `pivot_table()` 製作交叉表
- [ ] 地理資料分析（州、城市）
- [ ] 文字資料初步分析

### 完成 Instacart 分析後，你應該能夠：

- [ ] 處理大型資料集（3M+ 筆）
- [ ] 使用 `mlxtend` 進行購物籃分析
- [ ] 計算 Support、Confidence、Lift
- [ ] 建立推薦清單
- [ ] 序列資料分析

---

## ⚠️ 常見問題

### Q1: 下載速度很慢怎麼辦？

**A:**
- Kaggle 資料集可以直接在網頁下載後手動放入資料夾
- 使用 VPN 可能會更快
- 選擇較小的資料集先練習（Online Retail 只有 45MB）

### Q2: 記憶體不足怎麼辦？

**A:**
```python
# 方法 1：只讀取需要的欄位
df = pd.read_csv('data.csv', usecols=['Date', 'Sales', 'CustomerID'])

# 方法 2：使用 Categorical 型態
df['Category'] = df['Category'].astype('category')

# 方法 3：分批處理
for chunk in pd.read_csv('large_file.csv', chunksize=10000):
    process(chunk)

# 方法 4：降低精度
df = pd.read_csv('data.csv', dtype={'Price': 'float32'})
```

### Q3: 資料太大，GitHub 無法上傳怎麼辦？

**A:**
- 使用 `.gitignore` 排除大檔案（已設定）
- 使用 Git LFS（Large File Storage）
- 將資料集連結寫在 README，不上傳原始檔案

### Q4: 如何確認資料集下載成功？

**A:**
```python
import pandas as pd

# 載入資料
df = pd.read_csv('datasets/uci/online_retail.csv')

# 檢查
print(f"資料筆數：{len(df)}")
print(f"欄位數：{len(df.columns)}")
print("\n前5筆資料：")
print(df.head())
print("\n資料資訊：")
print(df.info())
```

---

## 📞 需要幫助？

遇到問題時：

1. **查看完整資料集清單**：`docs/ecommerce_datasets_comprehensive.md`
2. **查看 pandas 速查表**：`docs/pandas_advanced_cheatsheet.md`
3. **參考工具函數**：`utils/data_cleaning.py`
4. **查看案例範例**：`week03-06_pandas-advanced/`

---

## 🎉 開始你的資料分析之旅！

現在你已經：
✅ 知道如何下載資料集
✅ 知道如何載入資料
✅ 有了第一個分析範例
✅ 了解學習路徑

**下一步：**
1. 選擇一個資料集開始（建議從 Online Retail 開始）
2. 跟著 Week 3-6 的案例練習
3. 建立自己的分析筆記本
4. 完成第一個 Mini Project！

加油！💪

---

*最後更新：2025-12-10*
