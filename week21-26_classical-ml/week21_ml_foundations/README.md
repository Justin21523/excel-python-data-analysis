# Week 21: ML 基礎與特徵工程

**難度：** ⭐⭐ (適合已完成 Week 1-20 的學員)
**時間投入：** 25-30 小時
**核心目標：** 從商業分析平滑過渡到機器學習

---

## 📚 本週學習目標

### 1. 機器學習基礎概念
- Train/Validation/Test 分割策略
- Cross-Validation 深度理解
- 過擬合與欠擬合
- Bias-Variance Trade-off
- 評估指標選擇（Classification vs Regression）

### 2. 特徵工程
- 從 RFM 商業分析到 ML 特徵
- 類別變數編碼（Label Encoding, One-Hot, Target Encoding）
- 數值特徵標準化與正規化
- 特徵交互與多項式特徵
- 時間特徵提取

### 3. 實戰專案：客戶流失預測
- **資料集：** Olist Brazilian E-Commerce (99,441 訂單)
- **任務：** 預測客戶是否會流失
- **目標：** F1 Score > 0.70 (baseline)
- **技術棧：** scikit-learn, pandas, matplotlib

---

## 🗂️ 檔案結構

```
week21_ml_foundations/
├── README.md (本檔案)
├── notebooks/
│   ├── Day01_ML_Basics.ipynb              # ML 基礎概念
│   ├── Day02_Feature_Engineering.ipynb     # 特徵工程技巧
│   ├── Day03_Churn_Prediction_Part1.ipynb  # 流失預測 (EDA + 特徵)
│   ├── Day04_Churn_Prediction_Part2.ipynb  # 流失預測 (建模 + 評估)
│   └── Day05_Model_Comparison.ipynb        # 模型比較與選擇
├── scripts/
│   ├── data_preparation.py                 # 資料準備腳本
│   ├── feature_engineering.py              # 特徵工程函數
│   ├── model_training.py                   # 訓練腳本
│   └── evaluation.py                       # 評估工具
├── data/
│   ├── raw/                                # 原始 Olist 資料
│   ├── processed/                          # 處理後資料
│   └── features/                           # 特徵工程結果
├── models/
│   └── baseline_models/                    # 基線模型檢查點
└── docs/
    ├── ML_Glossary.md                      # ML 術語表
    ├── Feature_Engineering_Checklist.md    # 特徵工程檢查清單
    └── Evaluation_Metrics_Guide.md         # 評估指標指南
```

---

## 📖 每日課程安排

### **Day 1: ML 基礎概念（6-8 小時）**

#### 理論學習（2-3 小時）
1. **監督式學習 vs 非監督式學習**
   - 分類 vs 迴歸
   - 何時使用何種方法

2. **Train/Val/Test 分割**
   - 為何需要三組資料？
   - 分割比例選擇（60/20/20 vs 70/15/15 vs 80/10/10）
   - Time-series 資料的特殊處理

3. **Cross-Validation**
   - K-Fold CV
   - Stratified K-Fold
   - Time Series Split
   - 何時使用 CV vs Hold-out

4. **過擬合與欠擬合**
   - Learning Curves 解讀
   - Regularization 概念（L1, L2）
   - Early Stopping

5. **評估指標**
   - **分類：** Accuracy, Precision, Recall, F1, ROC-AUC
   - **迴歸：** MAE, RMSE, R², MAPE
   - 不平衡資料的指標選擇

#### 實作練習（4-5 小時）
- ✅ Notebook: `Day01_ML_Basics.ipynb`
- 練習 train_test_split 不同比例
- 實作 K-Fold Cross-Validation
- 繪製 Learning Curves
- 比較不同評估指標

---

### **Day 2: 特徵工程（6-8 小時）**

#### 理論學習（2-3 小時）
1. **從商業分析到 ML 特徵**
   - Week 12-14 的 RFM → ML features
   - 如何將領域知識轉化為特徵

2. **類別變數編碼**
   - **Label Encoding:** 順序類別（low/medium/high）
   - **One-Hot Encoding:** 名義類別（城市、產品類別）
   - **Target Encoding:** 高基數類別
   - **Frequency Encoding:** 基於出現頻率
   - Scikit-learn encoders vs pandas.get_dummies

3. **數值特徵轉換**
   - **標準化（Standardization）:** (x - mean) / std
   - **正規化（Normalization）:** (x - min) / (max - min)
   - **Log 轉換:** 處理偏態分佈
   - **Box-Cox / Yeo-Johnson:** 自動化轉換

4. **特徵生成**
   - 特徵交互（Feature Interactions）
   - 多項式特徵
   - 時間特徵分解（年、月、週、日、小時）
   - 聚合特徵（每客戶統計量）

5. **特徵選擇**
   - 相關性分析（Correlation Matrix）
   - Feature Importance (Tree-based models)
   - Recursive Feature Elimination (RFE)

#### 實作練習（4-5 小時）
- ✅ Notebook: `Day02_Feature_Engineering.ipynb`
- 對 Olist 資料進行完整特徵工程
- 比較不同編碼方法的效果
- 生成 30+ 個新特徵
- 特徵重要性分析

---

### **Day 3: 客戶流失預測 Part 1 - EDA & 特徵（6-8 小時）**

#### 專案背景
**業務問題：** Olist 平台希望預測哪些客戶會流失，以便提前採取行動

**流失定義：**
- 距離最後一次購買超過 6 個月
- 或：只購買一次且超過 3 個月未回購

**資料集：**
- `olist_orders_dataset.csv` (99,441 訂單)
- `olist_customers_dataset.csv` (99,441 客戶)
- `olist_order_items_dataset.csv` (112,650 項目)
- `olist_order_payments_dataset.csv` (103,886 支付)
- `olist_order_reviews_dataset.csv` (99,224 評論)

#### 任務流程
1. **資料載入與整合**（1-2 小時）
   - 合併 5 張表
   - 處理缺失值
   - 資料型態轉換

2. **探索性資料分析（EDA）**（2-3 小時）
   - 流失率統計
   - 特徵分佈視覺化
   - 流失客戶 vs 留存客戶對比
   - 相關性分析

3. **特徵工程**（3-4 小時）
   - **RFM 特徵：** Recency, Frequency, Monetary
   - **訂單特徵：** 平均訂單金額、訂單數、商品數
   - **支付特徵：** 支付方式偏好、分期付款比例
   - **評論特徵：** 平均評分、評論數
   - **時間特徵：** 首購日期、最後購買日期、客戶年齡
   - **行為特徵：** 購買頻率、回購間隔

#### 產出
- ✅ Notebook: `Day03_Churn_Prediction_Part1.ipynb`
- 處理後資料：`data/processed/olist_customers_features.csv`
- 特徵說明文件：`data/features/feature_descriptions.md`

---

### **Day 4: 客戶流失預測 Part 2 - 建模與評估（6-8 小時）**

#### 建模流程
1. **資料分割**（30 分鐘）
   - Train/Val/Test: 70/15/15
   - Stratified split（保持流失率比例）

2. **Baseline 模型**（1-2 小時）
   - **Logistic Regression:** 簡單快速，可解釋性強
   - **Decision Tree:** 非線性，視覺化決策規則
   - 建立性能基準

3. **進階模型**（2-3 小時）
   - **Random Forest:** 集成方法，減少過擬合
   - **Gradient Boosting (scikit-learn):** 高性能
   - 超參數初步調整

4. **模型評估**（2-3 小時）
   - **混淆矩陣（Confusion Matrix）**
   - **Precision-Recall Curve**
   - **ROC-AUC Curve**
   - **特徵重要性分析**
   - **錯誤案例分析**

#### 評估指標
- **主要指標：** F1 Score（平衡 Precision & Recall）
- **次要指標：** Precision（避免誤報）, Recall（捕獲流失客戶）, ROC-AUC
- **業務指標：** 成本效益分析（挽留成本 vs 流失損失）

#### 目標性能
- ✅ F1 Score > 0.70（基線目標）
- ✅ Precision > 0.65（至少 65% 預測正確）
- ✅ Recall > 0.70（捕獲至少 70% 流失客戶）
- ✅ ROC-AUC > 0.80

#### 產出
- ✅ Notebook: `Day04_Churn_Prediction_Part2.ipynb`
- 訓練好的模型：`models/baseline_models/`
- 評估報告：`docs/Model_Evaluation_Report.md`

---

### **Day 5: 模型比較與選擇（4-6 小時）**

#### 任務
1. **模型比較表格**（1-2 小時）
   - 整理所有模型的性能指標
   - 訓練時間對比
   - 記憶體使用量
   - 可解釋性評分

2. **交叉驗證確認**（2-3 小時）
   - 5-Fold CV 驗證最佳模型
   - 檢查模型穩定性
   - Learning Curves 分析

3. **最終模型選擇**（1 小時）
   - 根據業務需求選擇模型
   - 記錄決策理由
   - 準備 Week 22 改進計劃

#### 產出
- ✅ Notebook: `Day05_Model_Comparison.ipynb`
- 模型比較報告：`docs/Model_Comparison_Report.md`
- Week 22 改進計劃：`docs/Week22_Improvement_Plan.md`

---

## 🎯 學習成果檢核

完成 Week 21 後，你應該能夠：

### 理論理解
- ✅ 解釋 Train/Val/Test 分割的必要性
- ✅ 理解 Cross-Validation 的原理與應用時機
- ✅ 辨識過擬合與欠擬合的症狀
- ✅ 根據業務需求選擇合適的評估指標

### 實作技能
- ✅ 使用 scikit-learn 進行資料分割與 CV
- ✅ 對類別變數進行多種編碼
- ✅ 標準化/正規化數值特徵
- ✅ 從商業邏輯創造新特徵
- ✅ 訓練與評估分類模型
- ✅ 解讀混淆矩陣與 ROC 曲線

### 專案產出
- ✅ 完整的客戶流失預測系統
- ✅ 30+ 個工程特徵
- ✅ 4-5 個訓練好的模型
- ✅ 詳細的評估報告
- ✅ 可重現的程式碼

---

## 🔧 工具與套件

### 必備套件
```python
# 資料處理
import pandas as pd
import numpy as np

# 視覺化
import matplotlib.pyplot as plt
import seaborn as sns

# 機器學習
from sklearn.model_selection import train_test_split, cross_val_score, StratifiedKFold
from sklearn.preprocessing import StandardScaler, LabelEncoder, OneHotEncoder
from sklearn.linear_model import LogisticRegression
from sklearn.tree import DecisionTreeClassifier
from sklearn.ensemble import RandomForestClassifier, GradientBoostingClassifier

# 評估
from sklearn.metrics import (
    accuracy_score, precision_score, recall_score, f1_score,
    confusion_matrix, classification_report, roc_auc_score, roc_curve
)
```

### 推薦 IDE 設定
- **Jupyter Lab:** 互動式開發（使用 ai_env 環境）
- **VS Code:** 腳本開發與除錯
- **Git:** 版本控制（記錄每個實驗）

---

## 📊 資料集準備

### Olist 資料集載入

```python
import pandas as pd

# 載入資料
orders = pd.read_csv('/mnt/data/datasets/ecommerce/kaggle/olist/olist_orders_dataset.csv')
customers = pd.read_csv('/mnt/data/datasets/ecommerce/kaggle/olist/olist_customers_dataset.csv')
items = pd.read_csv('/mnt/data/datasets/ecommerce/kaggle/olist/olist_order_items_dataset.csv')
payments = pd.read_csv('/mnt/data/datasets/ecommerce/kaggle/olist/olist_order_payments_dataset.csv')
reviews = pd.read_csv('/mnt/data/datasets/ecommerce/kaggle/olist/olist_order_reviews_dataset.csv')

print(f"訂單數: {len(orders):,}")
print(f"客戶數: {len(customers):,}")
print(f"訂單項目數: {len(items):,}")
```

---

## 🚀 快速開始

### 1. 環境設定

```bash
# 激活環境
conda activate ai_env

# 進入 Week 21 目錄
cd week21-26_classical-ml/week21_ml_foundations

# 啟動 Jupyter Lab
jupyter lab
```

### 2. 開始 Day 1

打開 `notebooks/Day01_ML_Basics.ipynb` 開始學習！

---

## 📚 延伸閱讀

### 必讀文章
1. **Cross-Validation:**
   - [Scikit-learn User Guide: Cross-validation](https://scikit-learn.org/stable/modules/cross_validation.html)

2. **Feature Engineering:**
   - [Feature Engineering for Machine Learning (Kaggle)](https://www.kaggle.com/learn/feature-engineering)

3. **Evaluation Metrics:**
   - [Classification Metrics (Scikit-learn)](https://scikit-learn.org/stable/modules/model_evaluation.html#classification-metrics)

### 推薦書籍
- "Hands-On Machine Learning with Scikit-Learn, Keras, and TensorFlow" by Aurélien Géron
  - Chapter 2: End-to-End Machine Learning Project
  - Chapter 3: Classification

---

## ❓ 常見問題

### Q1: 為什麼需要 Validation Set？
**A:** Test Set 只能在最後用一次，Validation Set 用於調整超參數和模型選擇，避免 Test Set leakage。

### Q2: One-Hot Encoding vs Label Encoding 如何選擇？
**A:**
- **Label Encoding:** 有順序的類別（如教育程度：小學 < 中學 < 大學）
- **One-Hot Encoding:** 無順序的類別（如城市、產品類別）

### Q3: 為什麼 F1 Score 比 Accuracy 更重要？
**A:** 當資料不平衡時（如流失率只有 10%），即使模型預測所有人都不流失，Accuracy 也能達到 90%，但 F1 Score 會是 0，更能反映真實性能。

### Q4: 如何處理高基數類別變數（如 100+ 城市）？
**A:**
1. Target Encoding
2. Frequency Encoding
3. 分組為 Top N + Other
4. Embedding（Week 30 學習）

---

## 🎓 Week 22 預告

下週將學習：
- **XGBoost, LightGBM, CatBoost** 進階集成方法
- **Optuna** 自動化超參數優化
- **SMOTE** 處理不平衡資料
- **SHAP** 模型可解釋性

目標：將 F1 Score 從 0.70 提升到 0.75+！

---

**準備好開始 ML 之旅了嗎？打開 Day01_ML_Basics.ipynb 開始吧！🚀**
