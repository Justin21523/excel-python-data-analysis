# 🚀 Excel to Python Advanced Analytics - 開始指南

> **專案狀態：** ✅ 環境設定完成，準備下載資料集
> **最後更新：** 2025-12-10

---

## 📋 快速開始（3 步驟）

### 步驟 1：啟動 conda 環境

```bash
conda activate data_env
```

### 步驟 2：下載資料集（選擇一種方式）

#### 方式 A：下載所有 14 個資料集（推薦）

```bash
cd datasets
python download_all_datasets.py --all
```

#### 方式 B：只下載優先資料集（適合新手）

```bash
python download_all_datasets.py --priority 1
```

包含：
- Online Retail (UCI) - 商業分析基礎
- Olist Brazilian - 完整電商流程
- Instacart - 購物籃分析
- Store Sales - 時間序列預測

#### 方式 C：按類別下載

```bash
# 下載大型資料集（百萬筆以上）
python download_all_datasets.py --category large

# 下載中型資料集（10萬-100萬筆）
python download_all_datasets.py --category medium

# 下載機器學習專用資料集
python download_all_datasets.py --category ml
```

### 步驟 3：開始學習

```bash
jupyter lab
```

---

## 📦 包含的 14 個資料集

### 🔥 超大型資料集（百萬筆以上）

1. **Amazon Reviews 2023** (142.8M 筆評論)
   - 平台：HuggingFace
   - 用途：推薦系統、NLP/文字分析、情感分析
   - 大小：數十 GB（下載子集版本）

2. **Instacart Market Basket** (3M+ 筆訂單)
   - 平台：Kaggle
   - 用途：購物籃分析、關聯規則、產品推薦
   - 大小：200 MB

3. **eCommerce Behavior Data** (285M 筆用戶事件)
   - 平台：Kaggle
   - 用途：客戶行為分析、漏斗分析、轉換率優化
   - 大小：數 GB
   - ⚠️  非常大，確保足夠空間

4. **H&M Fashion** (1.37M 客戶，106K 產品)
   - 平台：Kaggle
   - 用途：推薦系統、圖像識別、時尚分析
   - 大小：數 GB（含圖片）

5. **Store Sales** (3M 筆記錄，54 商店)
   - 平台：Kaggle
   - 用途：時間序列預測、需求預測、銷售預測

### 📊 中型資料集（10萬-100萬筆）

6. **Online Retail (UCI)** (541,909 筆交易)
   - 平台：UCI Repository
   - 用途：商業分析基礎、RFM 分析、客戶分群
   - 大小：45 MB
   - ⭐ 最適合入門

7. **Online Retail II (UCI)**
   - 平台：UCI Repository
   - 用途：商業分析、RFM 分析、時間序列

8. **Brazilian E-Commerce (Olist)** (100,000 筆訂單)
   - 平台：Kaggle
   - 用途：RFM 分析、端到端專案、物流分析、評論分析
   - 大小：50 MB

9. **Pakistan Retail** (500,000+ 筆交易)
   - 平台：GitHub（手動下載）
   - 用途：商業分析、新興市場分析

10. **ASOS E-commerce** (30,845 個服飾商品)
    - 平台：HuggingFace
    - 用途：時尚產業分析、價格策略、產品分類

### 🤖 機器學習專用資料集

11. **Retail Rocket Recommender System**
    - 平台：Kaggle
    - 用途：協同過濾、內容過濾、混合推薦系統

12. **Bitext Retail E-commerce Chatbot** (8.47M tokens)
    - 平台：HuggingFace
    - 用途：聊天機器人訓練、客服自動化、NLP 模型微調

13. **E-commerce FAQ** (79 問答對)
    - 平台：HuggingFace
    - 用途：FAQ 系統、聊天機器人

14. **Sales Conversations**
    - 平台：HuggingFace
    - 用途：銷售機器人訓練、對話系統

---

## 📁 專案結構（AI_WAREHOUSE 3.0）

```
AI_WAREHOUSE 3.0 結構：
├── /mnt/c/ai_projects/excel-python-data-analysis/  # 專案代碼
├── /mnt/data/datasets/ecommerce/                   # 資料集
│   ├── kaggle/
│   │   ├── instacart/
│   │   ├── olist/
│   │   ├── h-and-m/
│   │   ├── store-sales/
│   │   ├── ecommerce-behavior/
│   │   └── retail-rocket/
│   ├── uci/
│   │   ├── online_retail/
│   │   └── online_retail_ii/
│   ├── huggingface/
│   │   ├── amazon_reviews/
│   │   ├── asos/
│   │   ├── ecommerce_chatbot/
│   │   ├── ecommerce_faq/
│   │   └── sales_conversations/
│   └── download_log.json                           # 下載記錄
└── /mnt/c/ai_cache/                                # 快取
    ├── huggingface/
    ├── kaggle/
    └── torch/
```

---

## 🔧 已設定的環境變數

當你啟動 `data_env` 時，會自動載入：

```bash
PROJECT_ROOT=/mnt/c/ai_projects/excel-python-data-analysis
DATASET_ROOT=/mnt/data/datasets/ecommerce
HF_HOME=/mnt/c/ai_cache/huggingface
KAGGLE_CONFIG_DIR=/mnt/c/ai_cache/kaggle
```

---

## 📚 學習路線

### 🎯 路線 1：商業分析入門（推薦新手）

**資料集：** Online Retail (UCI)

**學習內容：**
1. Week 1-2：資料清洗與探索
2. Week 3-4：RFM 客戶分群
3. Week 5-6：購物籃分析
4. Week 7-8：時間序列分析

**開始：**
```bash
conda activate data_env
cd week03-06_pandas-advanced
jupyter lab
```

### 🎯 路線 2：完整電商專案（進階）

**資料集：** Olist Brazilian E-Commerce

**學習內容：**
1. 訂單分析
2. 物流效率分析
3. 評論情感分析
4. 地理分析

### 🎯 路線 3：推薦系統（機器學習）

**資料集：** Instacart + Amazon Reviews

**學習內容：**
1. 購物籃分析（關聯規則）
2. 協同過濾
3. 內容過濾
4. 混合推薦系統

### 🎯 路線 4：時間序列預測（進階）

**資料集：** Store Sales

**學習內容：**
1. 時間序列建模（ARIMA、SARIMA）
2. 機器學習預測（XGBoost、LightGBM）
3. 深度學習（LSTM、GRU）

---

## 🛠️ 可用工具與範本

### 資料清洗工具

```python
from utils.data_cleaning import (
    remove_duplicates,
    handle_missing_values,
    standardize_text,
    detect_outliers,
    convert_dtypes,
    clean_data_pipeline
)
```

### Excel 樣式工具

```python
from utils.excel_styling import (
    apply_header_style,
    apply_number_format,
    auto_adjust_column_width,
    apply_table_style
)
```

### 資料生成工具

```python
# 生成模擬資料
cd datasets/synthetic
python generate_ecommerce_data.py --orders 10000 --customers 1000
```

---

## 📖 學習資源

### 文件

1. **完整資料集清單：** `docs/ecommerce_datasets_comprehensive.md`
2. **快速開始指南：** `docs/quick_start_datasets.md`
3. **pandas 進階速查：** `docs/pandas_advanced_cheatsheet.md`

### 範例代碼

- `week03-06_pandas-advanced/` - 12 個進階 pandas 案例
- `week07-08_openpyxl-mastery/` - 8 個 Excel 自動化案例
- `week12-14_business-analytics/` - 商業分析模型

---

## ⚠️ 重要提醒

### Kaggle API 設定

如果還沒設定 Kaggle API：

```bash
# 1. 前往 https://www.kaggle.com/account
# 2. 點擊 "Create New Token" 下載 kaggle.json
# 3. 執行：
mkdir -p /mnt/c/ai_cache/kaggle
cp ~/Downloads/kaggle.json /mnt/c/ai_cache/kaggle/
chmod 600 /mnt/c/ai_cache/kaggle/kaggle.json
```

### 磁碟空間

下載所有資料集需要：
- **最小：** ~5 GB（只下載優先資料集）
- **建議：** ~20 GB（包含大型資料集）
- **完整：** ~50+ GB（包含所有資料集和圖片）

檢查可用空間：
```bash
df -h /mnt/data
```

---

## 🎉 開始你的學習之旅！

### 建議的第一步：

1. **下載入門資料集：**
   ```bash
   conda activate data_env
   cd datasets
   python download_all_datasets.py --dataset online-retail
   ```

2. **查看資料：**
   ```bash
   cd /mnt/data/datasets/ecommerce/uci/online_retail
   ls -lh
   head -20 online_retail.csv
   ```

3. **開始第一個分析：**
   ```bash
   cd /home/justin/web-projects/excel-python-data-analysis
   jupyter lab
   # 開啟新的 Notebook，載入資料開始探索
   ```

4. **參考範例：**
   - 查看 `docs/quick_start_datasets.md` 的 RFM 分析範例
   - 閱讀 `docs/pandas_advanced_cheatsheet.md` 學習技巧

---

## 📞 需要幫助？

- **資料集清單：** `python download_all_datasets.py --list`
- **檢查環境：** `conda info --envs`
- **查看路徑：** `echo $DATASET_ROOT`

---

**🚀 現在就開始吧！祝學習愉快！**

*Last updated: 2025-12-10*
