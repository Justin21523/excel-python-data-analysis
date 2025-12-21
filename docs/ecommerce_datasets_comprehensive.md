# 🗂️ 電商/零售大型資料集完整清單

> **更新日期：** 2025-12-10
>
> **用途：** 商業分析、機器學習訓練、推薦系統、時間序列預測、客戶分群

這份文件整理了所有可用於電商/零售分析與機器學習訓練的大型公開資料集，涵蓋 Kaggle、HuggingFace、GitHub、UCI Repository 等平台。

---

## 📊 超大型資料集（百萬筆以上）

### 1. Amazon Reviews 2023 ⭐⭐⭐⭐⭐

**規模：** 142.8 百萬筆評論（1996-2023）

**內容：**
- 用戶評論（評分、文字、有用性投票）
- 商品元資料（描述、價格、圖片）
- 關聯圖（用戶-商品、一起購買）

**適用場景：**
- 情感分析
- 產品推薦系統
- 自然語言處理（NLP）
- 評論分類與摘要

**下載：**
- [HuggingFace - McAuley-Lab/Amazon-Reviews-2023](https://huggingface.co/datasets/McAuley-Lab/Amazon-Reviews-2023)
- [官方網站 - Amazon Reviews'23](https://amazon-reviews-2023.github.io/)
- [Julian McAuley's Dataset](https://jmcauley.ucsd.edu/data/amazon/)
- [AWS S3 - Amazon Customer Reviews](https://s3.amazonaws.com/amazon-reviews-pds/readme.html)

**檔案大小：** 數十 GB

---

### 2. Instacart Market Basket Analysis ⭐⭐⭐⭐⭐

**規模：** 3+ 百萬筆訂單，200,000+ 用戶

**內容：**
- 訂單資料（時間、星期、小時）
- 產品資料（49,688 個產品）
- 過道與部門資訊（134 過道、21 部門）
- 用戶購買序列（每位用戶 4-100 筆訂單）

**適用場景：**
- 購物籃分析（Market Basket Analysis）
- 關聯規則（Apriori、FP-Growth）
- 訂單預測
- 產品推薦

**下載：**
- [Kaggle Competition](https://www.kaggle.com/competitions/instacart-market-basket-analysis/data)
- [Kaggle Dataset](https://www.kaggle.com/datasets/yasserh/instacart-online-grocery-basket-analysis-dataset)
- [GitHub 分析範例](https://github.com/archd3sai/Instacart-Market-Basket-Analysis)

**檔案大小：** ~200 MB

**授權：** 僅限非商業用途

---

### 3. eCommerce Behavior Data (Multi-Category Store) ⭐⭐⭐⭐⭐

**規模：** 285 百萬筆用戶事件

**時間範圍：** 2019年10月 - 2020年4月（7個月）

**內容：**
- 用戶行為事件（瀏覽、加入購物車、購買）
- 產品資訊
- 用戶 ID 與 Session ID
- 時間戳記

**適用場景：**
- 用戶行為分析
- 轉換率優化
- 推薦系統
- 漏斗分析

**下載：**
- [Kaggle - eCommerce behavior data](https://www.kaggle.com/datasets/mkechinov/ecommerce-behavior-data-from-multi-category-store)
- [HuggingFace](https://huggingface.co/datasets/kevykibbz/ecommerce-behavior-data-from-multi-category-store_oct-nov_2019)

**檔案大小：** 數 GB

---

### 4. H&M Personalized Fashion Recommendations ⭐⭐⭐⭐⭐

**規模：**
- 106,000 個產品
- 1.37 百萬客戶
- 2 年交易資料（2018年9月 - 2020年9月）

**內容：**
- 商品元資料（名稱、類別、顏色、部門、描述）
- 客戶元資料（會員狀態、年齡、訂閱偏好）
- 歷史交易記錄
- **商品圖片**（105,542 張）

**適用場景：**
- 時尚推薦系統
- 圖像識別
- 個人化行銷
- 季節性趨勢分析

**下載：**
- [Kaggle Competition](https://www.kaggle.com/competitions/h-and-m-personalized-fashion-recommendations)
- [GitHub 解決方案](https://github.com/Wp-Zhang/H-M-Fashion-RecSys)

**檔案大小：** 數 GB（含圖片）

---

### 5. Store Sales - Time Series Forecasting ⭐⭐⭐⭐

**規模：** 3 百萬筆記錄

**時間範圍：** 2013年1月1日 - 2017年8月15日

**內容：**
- 54 個不同商店
- 33 個產品類別
- 每日銷售資料
- 促銷活動資訊
- 假日資訊

**適用場景：**
- 時間序列預測
- 需求預測
- 庫存優化
- 季節性分析

**下載：**
- [Kaggle Competition](https://www.kaggle.com/competitions/store-sales-time-series-forecasting)
- [Mendeley Data - Sales Dataset](https://data.mendeley.com/datasets/sv3vg8g755/1)

---

## 📈 中型資料集（10萬 - 100萬筆）

### 6. Online Retail Dataset (UCI) ⭐⭐⭐⭐⭐

**規模：** 541,909 筆交易

**時間範圍：** 2010年12月1日 - 2011年12月9日

**內容：**
- InvoiceNo（發票編號）
- StockCode（商品代碼）
- Description（商品描述）
- Quantity（數量）
- InvoiceDate（發票日期）
- UnitPrice（單價）
- CustomerID（客戶ID）
- Country（國家）

**特點：**
- 英國註冊的線上零售商
- 主要銷售獨特的禮品
- 包含 B2B 交易

**適用場景：**
- RFM 分析
- 客戶分群
- 購物籃分析
- 流失預測

**下載：**
- [UCI Repository - Online Retail](https://archive.ics.uci.edu/dataset/352/online+retail)
- [UCI Repository - Online Retail II](https://archive-beta.ics.uci.edu/dataset/502/online+retail+ii)
- [Kaggle Mirror](https://www.kaggle.com/datasets/jihyeseo/online-retail-data-set-from-uci-ml-repo)

**Python 下載：**
```python
from ucimlrepo import fetch_ucirepo
online_retail = fetch_ucirepo(id=352)
X = online_retail.data.features
y = online_retail.data.targets
```

**授權：** CC BY 4.0

---

### 7. Brazilian E-Commerce (Olist) ⭐⭐⭐⭐⭐

**規模：** 100,000 筆訂單

**時間範圍：** 2016-2018

**內容：**
- 訂單資料（狀態、價格、運費）
- 客戶資料（地理位置）
- 產品資料（類別、照片）
- 評論資料（評分、文字）
- 賣家資料
- 物流資料（預計交付時間、實際交付時間）

**適用場景：**
- 端到端電商分析
- 物流效率分析
- 評論情感分析
- 地理分析

**下載：**
- [Kaggle - Brazilian E-Commerce](https://www.kaggle.com/datasets/olistbr/brazilian-ecommerce)

**檔案大小：** ~50 MB

---

### 8. Pakistan Largest Retail E-commerce Dataset ⭐⭐⭐⭐

**規模：** 500,000+ 筆交易

**時間範圍：** 2016年3月 - 2018年8月

**內容：**
- 訂單資料
- 產品類別
- 價格資訊
- 時間戳記

**特點：**
- 巴基斯坦電商市場資料
- 新興市場資料分析

**下載：**
- [GitHub](https://github.com/mm-mazhar/Data-Analysis-and-Visualization-on-Ecommerce-Dataset)

---

### 9. ASOS E-commerce Dataset ⭐⭐⭐

**規模：** 30,845 個服飾商品

**內容：**
- 商品資訊
- 價格
- 類別
- 品牌
- 尺寸

**適用場景：**
- 時尚產業分析
- 價格策略
- 產品分類

**下載：**
- [HuggingFace - ASOS Dataset](https://huggingface.co/datasets/TrainingDataPro/asos-e-commerce-dataset)

---

## 🤖 機器學習專用資料集

### 10. Retail Rocket Recommender System ⭐⭐⭐⭐

**內容：**
- 用戶行為事件
- 產品資訊
- 推薦系統評估資料

**適用場景：**
- 協同過濾
- 內容過濾
- 混合推薦系統
- 推薦系統評估

**下載：**
- [Kaggle](https://www.kaggle.com/code/johnosorio/retail-rocket-ecommerce-recommender-system/data)

---

### 11. E-commerce Chatbot Training Dataset ⭐⭐⭐

**規模：** 8.47 百萬 tokens

**內容：**
- 電商客服對話
- FAQ 問答對
- 銷售對話腳本

**適用場景：**
- 聊天機器人訓練
- 客服自動化
- NLP 模型微調

**下載：**
- [HuggingFace - Bitext Retail Chatbot](https://huggingface.co/datasets/bitext/Bitext-retail-ecommerce-llm-chatbot-training-dataset)
- [HuggingFace - E-commerce FAQ](https://huggingface.co/datasets/Andyrasika/Ecommerce_FAQ)
- [HuggingFace - Sales Conversations](https://huggingface.co/datasets/goendalf666/sales-conversations)

---

## 🎯 特定領域資料集

### 12. Fashion & Apparel

**時尚相關資料集清單：**
- H&M Fashion Recommendations（上述）
- ASOS Dataset（上述）
- [DeepFashion](http://mmlab.ie.cuhk.edu.hk/projects/DeepFashion.html)（需申請）

---

### 13. Electronics & Tech Products

**電子產品資料集：**
- Amazon Electronics Reviews
- [Best Buy Product Data](https://github.com/luminati-io/eCommerce-dataset-samples)

---

### 14. Grocery & Food

**食品雜貨資料集：**
- Instacart（上述）
- [Tesco Grocery Dataset](https://github.com/luminati-io/eCommerce-dataset-samples)

---

## 📚 資料集彙整平台

### GitHub Awesome Lists

**推薦 GitHub 資源：**
- [rawatpranjal/industry-datasets](https://github.com/rawatpranjal/ecommerce-datasets) - 商業資料集精選清單
- [luminati-io/eCommerce-dataset-samples](https://github.com/luminati-io/eCommerce-dataset-samples) - 多個電商資料集樣本

---

## 🔧 資料集使用指南

### 下載與載入範例

#### Kaggle 資料集

```bash
# 安裝 Kaggle API
pip install kaggle

# 設定 API Token（從 Kaggle 帳號下載 kaggle.json）
mkdir ~/.kaggle
cp kaggle.json ~/.kaggle/
chmod 600 ~/.kaggle/kaggle.json

# 下載資料集
kaggle competitions download -c instacart-market-basket-analysis
kaggle datasets download -d olistbr/brazilian-ecommerce
```

#### HuggingFace 資料集

```python
from datasets import load_dataset

# 載入 Amazon Reviews 2023
dataset = load_dataset("McAuley-Lab/Amazon-Reviews-2023", "raw_review_All_Beauty")

# 載入電商行為資料
dataset = load_dataset("kevykibbz/ecommerce-behavior-data-from-multi-category-store_oct-nov_2019")
```

#### UCI Repository

```python
from ucimlrepo import fetch_ucirepo

# 載入 Online Retail
online_retail = fetch_ucirepo(id=352)
df = online_retail.data.features
```

---

## 🎓 資料集選擇建議

### 根據學習目標選擇

| 學習目標 | 推薦資料集 | 理由 |
|---------|----------|------|
| **商業分析基礎** | Online Retail (UCI) | 資料乾淨、適合入門 |
| **RFM 分析** | Online Retail, Olist | 包含完整客戶交易歷程 |
| **購物籃分析** | Instacart | 專為 Market Basket 設計 |
| **推薦系統** | Amazon Reviews, H&M | 大規模、包含評分與元資料 |
| **時間序列預測** | Store Sales Dataset | 多年每日資料 |
| **客戶行為分析** | eCommerce Behavior (285M) | 詳細用戶事件追蹤 |
| **圖像識別** | H&M Fashion | 包含產品圖片 |
| **NLP/文字分析** | Amazon Reviews | 大量評論文字 |
| **端到端專案** | Olist Brazilian | 涵蓋完整電商流程 |

---

## 📊 資料集規模比較

| 資料集 | 記錄數 | 檔案大小 | 時間跨度 | 難度 |
|-------|--------|---------|---------|------|
| Amazon Reviews 2023 | 142.8M | 數十 GB | 27 年 | ⭐⭐⭐⭐⭐ |
| eCommerce Behavior | 285M | 數 GB | 7 個月 | ⭐⭐⭐⭐⭐ |
| Instacart | 3M+ | 200 MB | 不明 | ⭐⭐⭐⭐ |
| Store Sales | 3M | - | 4.5 年 | ⭐⭐⭐⭐ |
| H&M Fashion | 1.37M 客戶 | 數 GB | 2 年 | ⭐⭐⭐⭐⭐ |
| Olist Brazilian | 100K | 50 MB | 2 年 | ⭐⭐⭐ |
| Online Retail (UCI) | 541K | 45 MB | 1 年 | ⭐⭐⭐ |
| Pakistan Retail | 500K | - | 2.5 年 | ⭐⭐⭐ |

---

## 🚀 進階機器學習應用場景

### 1. 推薦系統

**適用資料集：**
- Amazon Reviews 2023
- H&M Fashion
- Instacart
- Retail Rocket

**可實作模型：**
- 協同過濾（User-based、Item-based）
- 矩陣分解（SVD、ALS）
- 深度學習（Neural Collaborative Filtering）
- 混合推薦系統

---

### 2. 時間序列預測

**適用資料集：**
- Store Sales
- Olist Brazilian
- Online Retail

**可實作模型：**
- ARIMA / SARIMA
- Prophet
- LSTM / GRU
- Transformer (Temporal Fusion Transformer)

---

### 3. 客戶分群與分類

**適用資料集：**
- Online Retail
- Olist Brazilian
- eCommerce Behavior

**可實作模型：**
- K-Means
- DBSCAN
- Hierarchical Clustering
- RFM + Clustering

---

### 4. 自然語言處理

**適用資料集：**
- Amazon Reviews
- Olist Reviews

**可實作模型：**
- 情感分析（BERT、RoBERTa）
- 主題建模（LDA、NMF）
- 文字摘要
- 評論生成

---

### 5. 圖像識別

**適用資料集：**
- H&M Fashion（含圖片）

**可實作模型：**
- CNN 分類
- ResNet、EfficientNet
- 圖像搜尋
- 風格辨識

---

### 6. 需求預測

**適用資料集：**
- Store Sales
- Instacart

**可實作模型：**
- XGBoost / LightGBM
- Random Forest
- Time Series with External Features
- Ensemble Methods

---

## 📝 資料集引用與授權

### 引用格式

使用資料集發表研究時，請正確引用：

**Amazon Reviews 2023:**
```
McAuley, J. (2023). Amazon Reviews 2023.
Retrieved from https://amazon-reviews-2023.github.io/
```

**Instacart:**
```
"The Instacart Online Grocery Shopping Dataset 2017",
Accessed from https://www.instacart.com/datasets/grocery-shopping-2017
```

**Online Retail (UCI):**
```
Dua, D. and Graff, C. (2019). UCI Machine Learning Repository.
Irvine, CA: University of California, School of Information and Computer Science.
Online Retail Dataset: https://archive.ics.uci.edu/dataset/352/online+retail
```

### 授權類型

| 資料集 | 授權 | 商業使用 |
|-------|------|---------|
| Amazon Reviews | 研究用途 | ❌ |
| Instacart | 非商業 | ❌ |
| Online Retail (UCI) | CC BY 4.0 | ✅ |
| Olist Brazilian | - | 查看 Kaggle |
| H&M Fashion | Kaggle Competition | ❌ |

---

## 🔗 相關資源連結

### 學習資源

- [Kaggle Learn](https://www.kaggle.com/learn) - 免費課程
- [HuggingFace Course](https://huggingface.co/course) - NLP 與 Transformers
- [Fast.ai](https://www.fast.ai/) - 深度學習課程

### 論文與研究

- [RecSys Conference](https://recsys.acm.org/) - 推薦系統會議
- [KDD](https://www.kdd.org/) - 資料探勘會議
- [Papers with Code](https://paperswithcode.com/) - 論文與實作

---

## 📞 資料集問題與支援

遇到問題時：

1. **查看資料集官方文件** - 大多數資料集都有詳細文件
2. **Kaggle Discussions** - 查看其他人的討論
3. **GitHub Issues** - 提出技術問題
4. **Stack Overflow** - 搜尋相關問題

---

## 🎉 開始使用

建議從以下順序開始：

1. **入門：** Online Retail (UCI) - 資料乾淨、規模適中
2. **進階：** Olist Brazilian - 完整電商流程
3. **挑戰：** Instacart - 大規模購物籃分析
4. **專家：** Amazon Reviews 2023 - 百萬級資料處理

---

## Sources

本文參考以下來源：

- [Kaggle Shopping/Retail Datasets](https://www.kaggle.com/tags/shopping)
- [HuggingFace Datasets](https://huggingface.co/datasets)
- [Amazon Reviews 2023](https://amazon-reviews-2023.github.io/)
- [UCI Machine Learning Repository](https://archive.ics.uci.edu/)
- [GitHub Industry Datasets](https://github.com/rawatpranjal/ecommerce-datasets)
- [Instacart Market Basket Analysis](https://www.kaggle.com/competitions/instacart-market-basket-analysis)
- [H&M Personalized Fashion Recommendations](https://www.kaggle.com/competitions/h-and-m-personalized-fashion-recommendations)
- [Store Sales Time Series Forecasting](https://www.kaggle.com/competitions/store-sales-time-series-forecasting)

---

*最後更新：2025-12-10*
*如發現新的資料集或有任何建議，歡迎提交 PR！*
