# 📥 資料集下載工具使用指南

> **整合腳本：** `download_datasets_complete.py`
> **包含資料集：** 14 個（Kaggle + HuggingFace + UCI + 手動）

---

## 🚀 快速開始

### 1. 列出所有資料集

```bash
python download_datasets_complete.py --list
```

### 2. 下載單一資料集

```bash
# 下載最適合入門的資料集
python download_datasets_complete.py --dataset online-retail
```

### 3. 下載多個資料集

```bash
# 同時下載多個
python download_datasets_complete.py --datasets online-retail olist instacart
```

### 4. 下載所有資料集

```bash
# 下載全部 14 個（需要較長時間和空間）
python download_datasets_complete.py --all
```

---

## 📊 按條件下載

### 按類別下載

```bash
# 下載大型資料集（百萬筆以上）
python download_datasets_complete.py --category large

# 下載中型資料集（10萬-100萬筆）
python download_datasets_complete.py --category medium

# 下載機器學習專用資料集
python download_datasets_complete.py --category ml
```

### 按優先級下載

```bash
# 下載優先級 1（最推薦）
python download_datasets_complete.py --priority 1

# 優先級 1 包含：
# - online-retail
# - olist
# - instacart
# - store-sales
```

---

## 🛠️ 進階功能

### 自訂路徑

```bash
# 自訂資料集目錄
python download_datasets_complete.py --dataset online-retail \\
    --dataset-root /custom/path

# 自訂快取目錄
python download_datasets_complete.py --dataset online-retail \\
    --cache-root /custom/cache

# 同時自訂
python download_datasets_complete.py --all \\
    --dataset-root /mnt/external/datasets \\
    --cache-root /mnt/external/cache
```

### 乾跑模式

```bash
# 查看會下載什麼，但不實際下載
python download_datasets_complete.py --all --dry-run
```

### 跳過檢查

```bash
# 跳過環境檢查（不建議）
python download_datasets_complete.py --dataset online-retail --skip-checks
```

### 詳細輸出

```bash
# 顯示詳細日誌
python download_datasets_complete.py --dataset online-retail --verbose
```

---

## 📋 所有資料集列表

### 超大型資料集（large）

| 資料集 ID | 名稱 | 大小 | 記錄數 | 平台 | 優先級 |
|----------|------|------|--------|------|--------|
| amazon-reviews | Amazon Reviews 2023 | 數十 GB | 142.8M | HF | ⭐⭐ |
| instacart | Instacart Market Basket | 200 MB | 3M+ | Kaggle | ⭐⭐⭐ |
| ecommerce-behavior | eCommerce Behavior Data | 數 GB | 285M | Kaggle | ⭐⭐ |
| h-and-m | H&M Fashion | 數 GB | 1.37M | Kaggle | ⭐⭐ |
| store-sales | Store Sales - Time Series | - | 3M | Kaggle | ⭐⭐⭐ |

### 中型資料集（medium）

| 資料集 ID | 名稱 | 大小 | 記錄數 | 平台 | 優先級 |
|----------|------|------|--------|------|--------|
| online-retail | Online Retail (UCI) | 45 MB | 541K | UCI | ⭐⭐⭐ |
| online-retail-ii | Online Retail II (UCI) | - | - | UCI | ⭐⭐ |
| olist | Brazilian E-Commerce | 50 MB | 100K | Kaggle | ⭐⭐⭐ |
| pakistan-retail | Pakistan Retail | - | 500K+ | Manual | ⭐ |
| asos | ASOS E-commerce | - | 30K+ | HF | ⭐ |

### 機器學習專用（ml）

| 資料集 ID | 名稱 | 大小 | 記錄數 | 平台 | 優先級 |
|----------|------|------|--------|------|--------|
| retail-rocket | Retail Rocket | - | - | Kaggle | ⭐⭐ |
| ecommerce-chatbot | E-commerce Chatbot | 8.47M tokens | - | HF | ⭐ |
| ecommerce-faq | E-commerce FAQ | - | 79 | HF | ⭐ |
| sales-conversations | Sales Conversations | - | - | HF | ⭐ |

---

## 💡 使用建議

### 新手推薦組合

```bash
# 1. 先下載最適合入門的
python download_datasets_complete.py --dataset online-retail

# 2. 熟悉後下載優先級 1 的所有資料集
python download_datasets_complete.py --priority 1
```

### 進階使用者

```bash
# 下載所有中型和部分大型資料集
python download_datasets_complete.py --category medium
python download_datasets_complete.py --datasets instacart store-sales
```

### 機器學習研究

```bash
# 下載機器學習相關資料集
python download_datasets_complete.py --category ml

# 加上推薦系統資料集
python download_datasets_complete.py --datasets amazon-reviews h-and-m retail-rocket
```

---

## 📁 下載後的檔案結構

```
/mnt/data/datasets/ecommerce/
├── kaggle/
│   ├── instacart/
│   │   ├── orders.csv
│   │   ├── products.csv
│   │   └── ...
│   ├── olist/
│   │   ├── olist_orders_dataset.csv
│   │   └── ...
│   └── ...
├── uci/
│   ├── online_retail/
│   │   ├── online_retail.csv
│   │   ├── online_retail.parquet
│   │   └── README.txt
│   └── ...
├── huggingface/
│   ├── amazon_reviews/
│   │   ├── amazon_reviews_beauty_50k.csv
│   │   └── amazon_reviews_beauty_50k.parquet
│   └── ...
├── manual/
│   └── pakistan-retail/  # 需手動下載
├── logs/
│   └── download_20251210_*.log
└── download_log.json  # 下載記錄
```

---

## 🔍 檢查下載狀態

### 查看下載記錄

```bash
# 查看 JSON 記錄
cat /mnt/data/datasets/ecommerce/download_log.json | jq

# 查看日誌
tail -f /mnt/data/datasets/ecommerce/logs/download_*.log
```

### 查看已下載的資料集

```bash
# 列出所有 CSV 檔案
cd /mnt/data/datasets/ecommerce
find . -name '*.csv' -type f

# 檢查檔案大小
du -sh kaggle/* uci/* huggingface/*
```

---

## ⚠️ 常見問題

### Q1: Kaggle API 錯誤

**錯誤：** `OSError: Could not find kaggle.json`

**解決：**
```bash
# 1. 前往 https://www.kaggle.com/account
# 2. 下載 kaggle.json
# 3. 設定：
mkdir -p /mnt/c/ai_cache/kaggle
cp ~/Downloads/kaggle.json /mnt/c/ai_cache/kaggle/
chmod 600 /mnt/c/ai_cache/kaggle/kaggle.json
export KAGGLE_CONFIG_DIR=/mnt/c/ai_cache/kaggle
```

### Q2: HuggingFace 下載很慢

**解決：**
```bash
# 設定鏡像（中國用戶）
export HF_ENDPOINT=https://hf-mirror.com
```

### Q3: 磁碟空間不足

**解決：**
```bash
# 檢查空間
df -h /mnt/data

# 只下載小型資料集
python download_datasets_complete.py --priority 1

# 或使用外部硬碟
python download_datasets_complete.py --all \\
    --dataset-root /mnt/external/datasets
```

### Q4: 下載中斷了

**解決：**
```bash
# 腳本支援續傳，重新執行即可
python download_datasets_complete.py --dataset <中斷的資料集>

# 或下載所有（已下載的會跳過）
python download_datasets_complete.py --all
```

---

## 📊 預估下載時間

| 類別 | 資料集數 | 總大小 | 預估時間 |
|------|---------|--------|---------|
| 優先級 1 | 4 個 | ~300 MB | 10-20 分鐘 |
| 中型資料集 | 5 個 | ~100-500 MB | 15-30 分鐘 |
| 大型資料集 | 5 個 | 20-50 GB | 1-3 小時 |
| 全部資料集 | 14 個 | 20-50 GB | 1-4 小時 |

*時間依網速而定*

---

## 🎯 下一步

### 1. 驗證資料

```python
import pandas as pd

# 讀取資料
df = pd.read_csv('/mnt/data/datasets/ecommerce/uci/online_retail/online_retail.csv')

# 檢查
print(df.shape)
print(df.head())
print(df.info())
```

### 2. 開始學習

```bash
cd /home/justin/web-projects/excel-python-data-analysis
conda activate data_env
jupyter lab
```

### 3. 參考文件

- **完整資料集清單：** `docs/ecommerce_datasets_comprehensive.md`
- **快速開始指南：** `docs/quick_start_datasets.md`
- **pandas 速查表：** `docs/pandas_advanced_cheatsheet.md`

---

**🎉 開始你的資料分析之旅！**

*Last updated: 2025-12-10*
