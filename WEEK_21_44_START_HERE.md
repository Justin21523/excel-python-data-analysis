# 🚀 Week 21-44: 研究級機器學習/深度學習課程

**環境：** ai_env (Python 3.10.18)
**GPU：** NVIDIA GeForce RTX 5080 (CUDA 12.8)
**期程：** 24 週（約 6 個月）
**投入：** 每週 25-30 小時
**總時數：** 600-720 小時

---

## ✅ 環境已就緒

### 核心深度學習框架
- ✅ **PyTorch 2.7.1** (CUDA 12.8 支援)
- ✅ **HuggingFace Transformers 4.49.0**
- ✅ **PyTorch Lightning 2.6.0**
- ✅ **Sentence Transformers 5.1.0**

### 經典機器學習
- ✅ **scikit-learn 1.7.1**
- ✅ **XGBoost 3.1.2**
- ✅ **LightGBM 4.6.0**
- ✅ **CatBoost 1.2.8**

### 推薦系統
- ✅ **Implicit 0.7.2** (ALS)
- ✅ **Surprise 1.1.4** (Collaborative Filtering)

### NLP 工具
- ✅ **spaCy 3.8.11**
- ✅ **Gensim 4.4.0** (Word2Vec, Doc2Vec)

### 時間序列
- ✅ **Prophet 1.2.1**
- ✅ **Statsmodels 0.14.6**
- ✅ **pmdarima** (Auto ARIMA)

### 實驗追蹤與優化
- ✅ **Weights & Biases 0.23.1**
- ✅ **MLflow 3.7.0**
- ✅ **Optuna 4.6.0**
- ✅ **SHAP 0.49.1**

---

## 📊 資料集狀態

### 已下載完成（10/14）
| 資料集 | 大小 | 記錄數 | 用途 |
|--------|------|--------|------|
| **Amazon Reviews 2023** | 88 GB | 571.54M | NLP, 推薦系統, 情感分析 |
| **eCommerce Behavior** | 4.29 GB | 285M events | 推薦系統, 用戶行為 |
| **Olist** | 121 MB | 99K orders | 完整電商分析, Churn Prediction |
| **Store Sales** | 21 MB | 3M records | 時間序列預測 |
| **Online Retail** | - | 541K | RFM, Market Basket |
| **ASOS** | - | 30K products | 時尚推薦 |
| **Retail Rocket** | 291 MB | - | 推薦系統 |
| **3 NLP Datasets** | - | - | Chatbot, FAQ, Conversations |

---

## 🗂️ 專案結構

```
excel-python-data-analysis/
├── week21-26_classical-ml/              # Phase 2A: 經典 ML (6 週)
│   ├── week21_ml_foundations/           # ML 基礎與特徵工程
│   ├── week22_supervised_learning/      # XGBoost, LightGBM, CatBoost
│   ├── week23_unsupervised_learning/    # Clustering, PCA, UMAP
│   ├── week24_recsys_classical/         # 協同過濾, Matrix Factorization
│   ├── week25_recsys_advanced/          # Factorization Machines
│   └── week26_nlp_fundamentals/         # TF-IDF, Word2Vec, LDA
│
├── week27-32_deep-learning-fundamentals/ # Phase 2B: DL 基礎 (6 週)
│   ├── week27_pytorch_basics/           # PyTorch 基礎與 MLP
│   ├── week28_rnn_lstm/                 # RNN, LSTM, GRU, Attention
│   ├── week29_timeseries_deep/          # LSTM for Time Series
│   ├── week30_cnn_embeddings/           # CNN, Entity Embeddings
│   ├── week31_deep_recsys/              # Neural CF, DeepFM, DCN
│   └── week32_classical_timeseries/     # ARIMA, Prophet
│
├── week33-38_advanced-architectures/     # Phase 2C: 進階架構 (6 週)
│   ├── week33_transformer_fundamentals/ # Transformer from Scratch
│   ├── week34_bert_nlp/                 # BERT Fine-tuning
│   ├── week35_temporal_fusion_transformer/ # TFT, N-BEATS
│   ├── week36_graph_neural_networks/    # GCN, LightGCN
│   ├── week37_customer_behavior_deep/   # Deep CLV, DeepSurv
│   └── week38_multimodal_learning/      # CLIP, Vision Transformers
│
├── week39-44_research-projects/         # Phase 2D: 研究專案 (6 週)
│   ├── week39_project_timeseries_system/    # 端到端時間序列系統
│   ├── week40_project_recsys_hybrid/        # GNN + Transformer 推薦
│   ├── week41_project_nlp_intelligence/     # 多任務 NLP
│   ├── week42_project_customer_analytics/   # 深度客戶分析
│   ├── week43_paper_reproductions/          # 論文複現
│   └── week44_capstone_integration/         # 統一 ML 平台
│
├── ml_utils/                            # 共用工具庫
│   ├── data_processing/                 # 資料載入、前處理
│   ├── modeling/                        # 訓練、優化
│   ├── evaluation/                      # 評估指標
│   ├── deployment/                      # 部署工具
│   └── visualization/                   # 視覺化
│
├── datasets/ml_preprocessed/            # ML 前處理資料
│   ├── amazon_reviews_sampled/          # 1M-10M 抽樣
│   ├── olist_ml_ready/                  # ML 就緒格式
│   ├── ecommerce_behavior_sampled/      # 行為資料抽樣
│   ├── embeddings/                      # 預計算 embeddings
│   └── sampling_scripts/                # 抽樣腳本
│
├── models/                              # 模型檢查點
│   ├── classical_ml/                    # XGBoost, LightGBM 等
│   ├── deep_learning/                   # PyTorch 模型
│   └── checkpoints/                     # 訓練檢查點
│
└── papers/                              # 研究論文庫
    ├── recommender_systems/             # RecSys 論文
    ├── nlp/                             # NLP 論文
    ├── time_series/                     # 時間序列論文
    └── customer_analytics/              # 客戶分析論文
```

---

## 📚 完整課程規劃

### **Phase 2A: 經典機器學習 (Week 21-26)**

#### Week 21: ML 基礎與特徵工程 ⭐⭐
**目標：** 從商業分析到機器學習的平滑過渡
**專案：** 客戶流失預測（Olist 99K 訂單）
**技術：** Train/Val/Test 分割, Cross-Validation, RFM → ML Features
**成功指標：** F1 > 0.70 (baseline)

#### Week 22: 監督式學習進階 ⭐⭐⭐
**目標：** 掌握 Gradient Boosting 系列
**專案：** 進階流失預測（eCommerce Behavior 285M events）
**技術：** XGBoost, LightGBM, CatBoost, Optuna 超參數優化, SMOTE
**成功指標：** F1 > 0.75, SHAP 解釋性分析

#### Week 23: 非監督式學習 ⭐⭐
**目標：** 客戶分群與降維
**專案：** 進階客戶分群（RFM + 行為特徵）
**技術：** K-Means, DBSCAN, Hierarchical, PCA, t-SNE, UMAP
**成功指標：** Silhouette Score > 0.5

#### Week 24: 經典推薦系統 - Part 1 ⭐⭐⭐
**目標：** 協同過濾與矩陣分解
**專案：** 電商產品推薦（Retail Rocket）
**技術：** User/Item CF, SVD, ALS
**論文：** Matrix Factorization Techniques (Koren 2009)
**成功指標：** NDCG@10 > 0.25

#### Week 25: 經典推薦系統 - Part 2 ⭐⭐⭐⭐
**目標：** Factorization Machines
**專案：** 混合推薦系統（Amazon Reviews + Metadata）
**技術：** Content-based Filtering, Factorization Machines
**論文：** Factorization Machines (Rendle 2010)
**成功指標：** NDCG@10 > 0.30

#### Week 26: NLP 基礎與文本挖掘 ⭐⭐⭐
**目標：** 傳統 NLP 方法
**專案：** 評論情感分析（Amazon Reviews 10M）
**技術：** TF-IDF, Word2Vec, GloVe, LDA, NMF
**論文：** Word2Vec (Mikolov 2013), LDA (Blei 2003)
**成功指標：** Accuracy > 0.80 (5-class sentiment)

---

### **Phase 2B: 深度學習基礎 (Week 27-32)**

#### Week 27: PyTorch 基礎與神經網路 ⭐⭐
**目標：** 掌握 PyTorch 基礎
**專案：** 客戶流失預測 with MLP（對比 Week 21 XGBoost）
**技術：** Tensors, Autograd, nn.Module, Training Loop, Early Stopping
**成功指標：** F1 > 0.72 (接近 XGBoost)

#### Week 28: 序列模型 - RNN, LSTM, GRU ⭐⭐⭐⭐
**目標：** 深度理解序列模型
**專案：** 評論情感分析 with LSTM（Amazon Reviews）
**技術：** LSTM, GRU, Bidirectional, Attention Mechanism
**論文：** LSTM (Hochreiter 1997), Attention (Bahdanau 2015)
**成功指標：** Accuracy > 0.85 (beat Week 26 TF-IDF)

#### Week 29: 時間序列深度學習 ⭐⭐⭐⭐
**目標：** LSTM/GRU for Forecasting
**專案：** 銷售預測 with LSTM（Store Sales 3M records）
**技術：** Seq2Seq Encoder-Decoder, Multi-step Forecasting
**成功指標：** SMAPE < 20%

#### Week 30: CNN 與 Embeddings ⭐⭐⭐
**目標：** CNN for Text + Entity Embeddings
**專案：** Product Embedding Learning（Retail Rocket）
**技術：** 1D CNN, Entity Embeddings, Metric Learning (Triplet Loss)
**論文：** TextCNN (Kim 2014)
**成功指標：** Embedding quality evaluation

#### Week 31: 深度學習推薦系統 ⭐⭐⭐⭐⭐
**目標：** Neural Collaborative Filtering
**專案：** Neural CF 系統（Amazon Reviews 10M）
**技術：** GMF, MLP, NeuMF, Wide & Deep, DeepFM, DCN
**論文：** Neural CF (He 2017), DeepFM (Guo 2017)
**成功指標：** NDCG@10 > 0.35 (beat Week 24-25), 複現論文結果

#### Week 32: 經典時間序列模型 ⭐⭐⭐
**目標：** ARIMA, Prophet 深度理解
**專案：** 多店鋪銷售預測（Store Sales，對比 Week 29 LSTM）
**技術：** ARIMA, SARIMA, Prophet, Exponential Smoothing
**論文：** Prophet (Taylor & Letham 2017)
**成功指標：** SMAPE < 18% (beat LSTM on some metrics)

---

### **Phase 2C: 進階架構 (Week 33-38)**

#### Week 33: Transformer 架構基礎 ⭐⭐⭐⭐⭐
**目標：** 從零實現 Transformer
**專案：** Transformer from Scratch + 序列分類（Amazon Reviews）
**技術：** Self-Attention, Multi-Head Attention, Positional Encoding
**論文：** Attention Is All You Need (Vaswani 2017)
**成功指標：** 理解架構 + 可運行的實現

#### Week 34: BERT 與預訓練語言模型 ⭐⭐⭐⭐⭐
**目標：** BERT Fine-tuning 深度實戰
**專案：** 評論情感分析 with BERT（10M reviews）
**技術：** BERT, DistilBERT, RoBERTa, HuggingFace Transformers
**論文：** BERT (Devlin 2018), RoBERTa (Liu 2019)
**成功指標：** Accuracy > 0.90 (SOTA), Multi-GPU training

#### Week 35: Temporal Fusion Transformers 進階預測 ⭐⭐⭐⭐⭐
**目標：** 最先進的時間序列模型
**專案：** 多 Horizon 銷售預測 with TFT（Store Sales）
**技術：** TFT, Variable Selection Networks, N-BEATS, Autoformer
**論文：** TFT (Lim 2020), N-BEATS (Oreshkin 2019)
**成功指標：** SMAPE < 15% (beat all previous models)

#### Week 36: Graph Neural Networks for RecSys ⭐⭐⭐⭐⭐
**目標：** 圖神經網絡推薦系統
**專案：** Graph-based 推薦（Amazon Reviews user-item graph）
**技術：** GCN, GraphSAGE, GAT, NGCF, LightGCN
**論文：** Neural Graph CF (Wang 2019), LightGCN (He 2020)
**成功指標：** NDCG@10 > 0.40 (SOTA)

#### Week 37: 進階客戶行為建模 ⭐⭐⭐⭐
**目標：** Deep CLV, Survival Analysis
**專案：** 深度客戶分析系統（Olist + eCommerce Behavior）
**技術：** Deep CLV, DeepSurv, Uplift Modeling, Causal Inference
**論文：** DeepSurv (Katzman 2018)
**成功指標：** CLV prediction MAE < baseline

#### Week 38: Multi-Modal Learning ⭐⭐⭐⭐⭐
**目標：** 多模態融合
**專案：** 多模態產品搜索（ASOS + Amazon images + text）
**技術：** CLIP, Vision Transformers (ViT), Multi-modal Fusion
**成功指標：** NDCG@10 > 0.40 with images + text

---

### **Phase 2D: 研究專案與論文複現 (Week 39-44)**

#### Week 39: 研究專案 1 - 進階時間序列系統 ⭐⭐⭐⭐⭐
**專案範圍：** 端到端生產級時間序列預測系統
**技術：** Ensemble (ARIMA + Prophet + LSTM + TFT + N-BEATS)
**功能：** Hierarchical forecasting, Probabilistic forecasting, FastAPI 推理, Streamlit 儀表板
**產出：** 2000+ lines code, 10-15 頁研究論文
**時間：** 40-50 小時

#### Week 40: 研究專案 2 - SOTA 推薦系統 ⭐⭐⭐⭐⭐
**專案範圍：** GNN + Transformer 混合推薦系統
**技術：** LightGCN + BERT + Transformer Sequential
**功能：** Multi-task learning (CTR + rating + ranking), Cold-start handling
**產出：** 2500+ lines code, 12-18 頁研究論文
**時間：** 50-60 小時

#### Week 41: 研究專案 3 - NLP 電商智能系統 ⭐⭐⭐⭐⭐
**專案範圍：** 多任務 NLP for 評論分析
**技術：** Multi-task BERT (Sentiment + NER + Aspect + Summarization + QA)
**產出：** 2000+ lines code, 10-15 頁研究論文
**時間：** 40-50 小時

#### Week 42: 研究專案 4 - 客戶行為深度學習系統 ⭐⭐⭐⭐⭐
**專案範圍：** 端到端客戶分析
**技術：** Multi-task (CLV + Churn + Next Purchase), Shared LSTM Encoder
**產出：** 2200+ lines code, 12-16 頁研究論文
**時間：** 45-55 小時

#### Week 43: 論文複現 ⭐⭐⭐⭐⭐
**目標：** 複現 2-3 篇頂會論文（2022-2024）
**建議論文：** BERT4Rec, SASRec, TSMixer, PatchTST
**產出：** 3 個 paper reproduction repos, 複現報告
**時間：** 50-60 小時

#### Week 44: Capstone Integration 整合專案 ⭐⭐⭐⭐⭐
**專案範圍：** 統一 ML 平台整合 Week 39-42 所有系統
**技術：** Microservices, Docker, FastAPI, MLflow, CI/CD
**產出：** 5000+ lines integrated platform, 架構文件, Demo video, Blog 系列
**時間：** 50-60 小時

---

## 🎯 7 大作品集專案

### 1. Customer Churn Prediction with Explainable AI (Week 21-22)
- **資料集：** Olist (99K orders)
- **技術：** XGBoost, LightGBM, Neural Network, SHAP
- **目標：** F1 > 0.75, API latency < 100ms

### 2. Multi-Horizon Sales Forecasting System (Week 29, 32, 35, 39)
- **資料集：** Store Sales (3M records, 54 stores)
- **技術：** ARIMA, Prophet, LSTM, TFT, N-BEATS ensemble
- **目標：** SMAPE < 15%

### 3. Neural Collaborative Filtering (Week 24-25, 31, 40)
- **資料集：** Amazon Reviews (10M interactions)
- **技術：** GMF, MLP, NeuMF, LightGCN (PyTorch from scratch)
- **目標：** NDCG@10 > 0.35, reproduce He et al. 2017

### 4. BERT Sentiment Analysis on 10M Reviews (Week 26, 28, 34, 41)
- **資料集：** Amazon Reviews (10M)
- **技術：** BERT/DistilBERT fine-tuning, LDA, BERTopic
- **目標：** Accuracy > 90%, multi-GPU training

### 5. BERT4Rec Sequential Recommendation (Week 43)
- **資料集：** Instacart (3M orders)
- **技術：** BERT4Rec, SASRec comparison
- **目標：** NDCG@10 > 0.30, reproduce CIKM 2019

### 6. Multi-Modal Product Recommendations (Week 38)
- **資料集：** H&M Fashion (106K products with images)
- **技術：** ResNet/ViT + BERT + fusion
- **目標：** NDCG@10 > 0.40

### 7. End-to-End ML Platform with MLOps (Week 44)
- **整合：** All above projects
- **技術：** Docker, FastAPI, MLflow, CI/CD, monitoring
- **目標：** Production-ready deployment

---

## 📊 評估框架

### 標準化評估指標

#### 客戶分析
- Classification: `accuracy, precision, recall, f1, roc_auc`
- Clustering: `silhouette_score, calinski_harabasz, davies_bouldin`
- Regression: `mae, rmse, r2, mape`

#### 時間序列
- Point Forecast: `mae, rmse, mape, smape`
- Probabilistic: `crps, quantile_loss`
- Trend: `direction_accuracy`

#### NLP
- Classification: `accuracy, f1_weighted, f1_macro`
- Topic Modeling: `coherence_score, perplexity`
- Generation: `bleu, rouge, meteor`

#### 推薦系統
- Ranking: `ndcg@k, map@k, mrr, precision@k, recall@k`
- Rating: `rmse, mae`
- Diversity: `coverage, gini_index, novelty`

### 實驗追蹤

**主要工具：** Weights & Biases (W&B)
- 原因：研究級工作流、超參數掃描、協作友好
- 替代：MLflow（本地優先）

**可重現性協議：**
```python
SEED = 42  # 固定所有隨機種子
# 記錄：Git commit, Python 版本, PyTorch 版本, 資料版本
```

---

## 🚀 快速開始

### 1. 啟動 Jupyter Lab (使用 ai_env)

```bash
# 激活 ai_env 環境
conda activate ai_env

# 啟動 Jupyter Lab
jupyter lab --no-browser --port=8889
```

### 2. 開始 Week 21

```bash
cd week21-26_classical-ml/week21_ml_foundations
```

### 3. 查看完整規劃

```bash
cat ~/.llm_provider/plans/distributed-cooking-wadler.md
```

---

## 📖 論文複現清單

| 論文 | 領域 | 年份 | 引用數 | 難度 | 週次 |
|------|------|------|--------|------|------|
| Neural Collaborative Filtering | RecSys | 2017 | 3,000+ | ⭐⭐⭐ | Week 31 |
| BERT4Rec | RecSys | 2019 | 500+ | ⭐⭐⭐⭐ | Week 43 |
| SASRec | RecSys | 2018 | 800+ | ⭐⭐⭐⭐ | Week 43 |
| BERT (Fine-tuning) | NLP | 2018 | 80,000+ | ⭐⭐⭐ | Week 34 |
| Temporal Fusion Transformer | Time Series | 2021 | 300+ | ⭐⭐⭐⭐⭐ | Week 35 |
| DeepFM | CTR Prediction | 2017 | 1,500+ | ⭐⭐⭐ | Week 31 |
| LightGCN | GNN RecSys | 2020 | 800+ | ⭐⭐⭐⭐⭐ | Week 36 |

---

## 🎓 學習建議

### 逐步推進策略

1. **Week 21-23**: 建立 ML 基礎，複習 sklearn，了解完整 pipeline
2. **Week 24-26**: 深入推薦系統與 NLP 傳統方法，打好基礎
3. **Week 27-29**: 掌握 PyTorch，熟悉深度學習訓練流程
4. **Week 30-32**: 專精各類深度學習架構（CNN, RNN, 推薦系統）
5. **Week 33-35**: 挑戰 Transformer 系列，理解 attention mechanism
6. **Week 36-38**: 探索前沿架構（GNN, Multi-modal）
7. **Week 39-44**: 整合所有技能，完成研究級專案

### 時間分配建議

- **理論學習：** 20-25% (閱讀論文、理解架構)
- **編碼實踐：** 50-60% (實作模型、調試訓練)
- **實驗調優：** 15-20% (超參數、模型比較)
- **文檔撰寫：** 10-15% (README, 技術博客)

### GPU 使用建議

您有 **RTX 5080**，可以：
- 訓練較大的 BERT 模型（10M+ 樣本）
- 使用 batch size 32-128（視模型大小）
- Multi-GPU 實驗（如果未來擴展）
- 快速迭代實驗（縮短訓練時間）

---

## 📝 下一步行動

1. ✅ **環境已就緒** - ai_env 包含所有套件
2. ⏭️ **開始 Week 21** - ML 基礎與特徵工程
3. 📚 **閱讀完整計劃** - `~/.llm_provider/plans/distributed-cooking-wadler.md`
4. 🎯 **設定 W&B 帳號** - https://wandb.ai/
5. 📖 **準備論文** - 下載到 `papers/` 目錄

---

讓我們開始這段研究級機器學習之旅！🚀💪
