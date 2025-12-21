# 📊 資料集下載狀態總覽

**更新時間：** 2025-12-10 23:58 UTC (2024-12-11 07:58 台北時間)

---

## ✅ **下載成功的資料集（9/14）**

### 1. ⭐ **eCommerce Behavior Data** (13.7 GB)
- **狀態：** ✅ 已完成
- **來源：** Kaggle
- **檔案數：** 2 個 CSV
  - 2019-Oct.csv (5.3 GB)
  - 2019-Nov.csv (8.4 GB)
- **記錄數：** 285M 用戶事件（view/cart/purchase）
- **位置：** `/mnt/data/datasets/ecommerce/kaggle/ecommerce-behavior`

### 2. ⭐ **Store Sales - Time Series** (120 MB)
- **狀態：** ✅ 已完成
- **來源：** Kaggle
- **檔案數：** 7 個 CSV
  - train.csv (117 MB)
  - test.csv, stores.csv, holidays_events.csv, oil.csv, transactions.csv
- **位置：** `/mnt/data/datasets/ecommerce/kaggle/store-sales`

### 3. ⭐ **Online Retail (UCI)** (45 MB)
- **狀態：** ✅ 已完成
- **來源：** UCI Machine Learning Repository
- **記錄數：** 541,909 筆交易
- **時間範圍：** 2010-2011
- **位置：** `/mnt/data/datasets/ecommerce/uci/online-retail`

### 4. ⭐ **Brazilian E-Commerce (Olist)** (121 MB)
- **狀態：** ✅ 已完成
- **來源：** Kaggle
- **檔案數：** 9 個 CSV
  - olist_orders_dataset.csv
  - olist_order_items_dataset.csv
  - olist_customers_dataset.csv
  - olist_products_dataset.csv
  - olist_sellers_dataset.csv
  - olist_order_payments_dataset.csv
  - olist_order_reviews_dataset.csv
  - olist_geolocation_dataset.csv
  - product_category_name_translation.csv
- **記錄數：** 100k 訂單
- **位置：** `/mnt/data/datasets/ecommerce/kaggle/olist`

### 5. ⭐ **ASOS E-commerce Dataset** (30,845 products)
- **狀態：** ✅ 已完成
- **來源：** HuggingFace
- **內容：** 產品資訊
- **位置：** `/mnt/data/datasets/ecommerce/huggingface/asos`

### 6. ⭐ **Retail Rocket Recommender** (942 MB)
- **狀態：** ✅ 已完成
- **來源：** Kaggle
- **檔案數：** 4 個 CSV
  - events.csv (90 MB)
  - category_tree.csv
  - item_properties_part1.csv (462 MB)
  - item_properties_part2.csv (390 MB)
- **位置：** `/mnt/data/datasets/ecommerce/kaggle/retail-rocket`

### 7. ⭐ **E-commerce Chatbot Dataset** (44,884 samples)
- **狀態：** ✅ 已完成
- **來源：** HuggingFace
- **Token 數：** 8.47M
- **位置：** `/mnt/data/datasets/ecommerce/huggingface/ecommerce-chatbot`

### 8. ⭐ **E-commerce FAQ Dataset** (79 FAQs)
- **狀態：** ✅ 已完成
- **來源：** HuggingFace
- **位置：** `/mnt/data/datasets/ecommerce/huggingface/ecommerce-faq`

### 9. ⭐ **Sales Conversations Dataset** (3,412 conversations)
- **狀態：** ✅ 已完成
- **來源：** HuggingFace
- **位置：** `/mnt/data/datasets/ecommerce/huggingface/sales-conversations`

---

## 🔄 **正在下載的資料集（1）**

### 10. 🔥 **Amazon Reviews 2023** (數十 GB)
- **狀態：** 🔄 **正在下載中**
- **來源：** 官方 UCSD McAuley Lab
- **類別數：** 33 個產品類別
- **檔案數：** 66 個（33 reviews + 33 metadata）
- **格式：** JSONL.gz
- **記錄數：** 571.54M reviews, 54.51M users, 48.19M items
- **時間範圍：** 1996-2023
- **位置：** `/mnt/data/datasets/ecommerce/amazon-reviews-2023`

**已完成類別（4/33）：**
- ✅ All_Beauty (reviews + metadata)
- ✅ Amazon_Fashion (reviews + metadata)
- ✅ Appliances (reviews + metadata)
- ✅ Arts_Crafts_and_Sewing (reviews + metadata)

**正在下載：**
- 🔄 Automotive (2.14 GB，進度：1%，下載速度：2 MB/s）

**待下載類別（29/33）：**
- Baby
- Beauty_and_Personal_Care
- Books
- CDs_and_Vinyl
- Cell_Phones_and_Accessories
- Clothing_Shoes_and_Jewelry
- Digital_Music
- Electronics
- Gift_Cards
- Grocery_and_Gourmet_Food
- Handmade_Products
- Health_and_Household
- Health_and_Personal_Care
- Home_and_Kitchen
- Industrial_and_Scientific
- Kindle_Store
- Magazine_Subscriptions
- Movies_and_TV
- Musical_Instruments
- Office_Products
- Patio_Lawn_and_Garden
- Pet_Supplies
- Software
- Sports_and_Outdoors
- Subscription_Boxes
- Tools_and_Home_Improvement
- Toys_and_Games
- Video_Games
- Unknown

**預計完成時間：** 根據當前速度（2 MB/s），預計需要 **6-8 小時**完成所有下載

---

## ⚠️ **需要手動下載的資料集（1）**

### 11. ⚠️ **Pakistan Retail Dataset**
- **狀態：** ⚠️ 需要手動下載
- **來源：** GitHub
- **原因：** 不在 Kaggle API 中
- **下載連結：** [GitHub Repository]
- **操作：** 需要手動從 GitHub clone 或下載 ZIP

---

## ❌ **下載失敗的資料集（3）**

### 12. ❌ **Instacart Market Basket Analysis** (200 MB)
- **狀態：** ❌ 下載失敗
- **來源：** Kaggle
- **錯誤：** `403 Forbidden - Competition dataset`
- **原因：** 需要接受競賽條款
- **解決方案：**
  1. 訪問：https://www.kaggle.com/competitions/instacart-market-basket-analysis
  2. 點擊「Accept Competition Rules」
  3. 使用正確的 dataset ID：`psparks/instacart-market-basket-analysis`（非競賽版）
  4. 重新下載：
     ```bash
     kaggle datasets download -d psparks/instacart-market-basket-analysis
     ```

### 13. ❌ **H&M Fashion Recommendations** (數 GB)
- **狀態：** ❌ 下載失敗
- **來源：** Kaggle
- **錯誤：** `403 Forbidden`
- **原因：** 需要接受競賽條款
- **解決方案：**
  1. 訪問：https://www.kaggle.com/competitions/h-and-m-personalized-fashion-recommendations/data
  2. 點擊「Accept Competition Rules」
  3. 手動下載資料
  4. 解壓到：`/mnt/data/datasets/ecommerce/kaggle/h-and-m`

### 14. ❌ **Online Retail II (UCI)**
- **狀態：** ❌ 下載失敗
- **來源：** UCI
- **錯誤：** UCI API 錯誤
- **解決方案：** 可能 UCI dataset ID 不正確，或該資料集已移除

---

## 📈 **總體進度**

```
✅ 成功：   9/14  (64.3%)
🔄 進行中： 1/14  (7.1%)
⚠️  手動：   1/14  (7.1%)
❌ 失敗：   3/14  (21.4%)
─────────────────────────
📊 總計：   14 個資料集
```

---

## 💾 **磁碟空間使用**

**已下載資料大小：**
```bash
eCommerce Behavior:    13.7 GB
Store Sales:           120 MB
Online Retail:         45 MB
Olist:                 121 MB
Retail Rocket:         942 MB
其他:                  ~100 MB
─────────────────────────────
小計:                  ~15 GB
```

**Amazon Reviews（預計）：**
```
預計總大小:            ~50-100 GB（全 33 類別）
已下載:                ~300 MB（4/33 類別）
進行中:                2.14 GB（Automotive）
待下載:                ~47-97 GB（29/33 類別）
```

**總空間需求：** ~65-115 GB

---

## 🔧 **後續操作建議**

### 立即可用的資料集（Week 3-6 pandas 學習）

**推薦順序：**

1. **Olist (121 MB)** - 最適合入門
   - ✅ 已完成下載
   - ✅ 多表結構（9 張表）
   - ✅ 真實業務邏輯
   - ✅ 完整文檔
   - 📍 **優先使用這個**

2. **Online Retail UCI (45 MB)** - RFM 分析經典
   - ✅ 已完成下載
   - ✅ 適合時間序列分析
   - ✅ 標準 RFM 分析資料集

3. **Store Sales (120 MB)** - 時間序列預測
   - ✅ 已完成下載
   - ✅ 時間序列數據
   - ✅ 包含假日、油價等外部因素

4. **eCommerce Behavior (13.7 GB)** - 大數據練習
   - ✅ 已完成下載
   - ⚠️  檔案很大，建議用 chunking 讀取
   - ✅ 用戶行為路徑分析

### Amazon Reviews 2023 下載監控

**監控命令：**
```bash
# 查看即時下載狀態
tail -f /tmp/amazon_download.log

# 查看已下載檔案數
ls -lh /mnt/data/datasets/ecommerce/amazon-reviews-2023/reviews/ | wc -l
ls -lh /mnt/data/datasets/ecommerce/amazon-reviews-2023/metadata/ | wc -l

# 查看已下載總大小
du -sh /mnt/data/datasets/ecommerce/amazon-reviews-2023/
```

**預計完成時間：** 根據當前速度（2 MB/s），大約需要 **6-8 小時**

### 失敗資料集處理

**Instacart 修復：**
```bash
# 使用正確的 dataset ID
kaggle datasets download -d psparks/instacart-market-basket-analysis -p /mnt/data/datasets/ecommerce/kaggle/instacart
```

**H&M 手動下載：**
1. 訪問 Kaggle 競賽頁面
2. 接受條款
3. 手動下載

---

## 📝 **資料集使用建議**

### Week 3-6: pandas 進階實戰

**資料集分配：**

- **Week 3（MultiIndex & GroupBy）：**
  - 使用：Olist（多表合併）
  - 練習：eCommerce Behavior（大數據 GroupBy）

- **Week 4（時間序列）：**
  - 使用：Store Sales（時間序列預測）
  - 練習：Online Retail（時間序列分析）

- **Week 5（Apply/Transform）：**
  - 使用：Olist（複雜計算）
  - 練習：Retail Rocket（推薦系統）

- **Week 6（效能優化）：**
  - 使用：eCommerce Behavior（13.7 GB，測試優化技巧）
  - 練習：Amazon Reviews（大數據處理）

### Week 12-14: 商業分析模型

**模型與資料集配對：**

- **RFM 分析：** Online Retail UCI
- **Cohort 分析：** Olist
- **CLV 計算：** Olist + Retail Rocket
- **Market Basket：** Instacart（修復後）或 Olist
- **推薦系統：** Amazon Reviews + Retail Rocket

---

## 🎉 **總結**

✅ **已準備好 9 個高品質資料集**（15 GB）
🔄 **Amazon Reviews 正在下載**（預計 6-8 小時完成）
⚠️  **1 個需要手動處理**
❌ **3 個失敗但可修復**

**你現在可以立即開始 Week 1-2 Excel 學習，同時讓 Amazon Reviews 在背景下載！**

---

**🚀 建議行動：**

1. ✅ **立即開始 Week 1 Excel 學習**（資料和教學都準備好了）
2. 🔄 **讓 Amazon Reviews 繼續下載**（背景執行，6-8 小時）
3. ⏳ **Week 3 開始前修復 Instacart**（接受競賽條款即可）
4. 📦 **Week 1-2 完成後就能直接進入 pandas 學習**（Olist 資料已就緒）
