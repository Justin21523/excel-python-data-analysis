# Project 2: Customer Insights System
客戶洞察系統 - Week 16-17

## 項目概述

Customer Insights System 是一個全面的客戶分析平台，提供 RFM 分析、CLV 計算、客戶行為洞察、群組分析和個性化推薦。

## 主要功能

1. **RFM 分析**
   - Recency（最近性）
   - Frequency（購買頻率）
   - Monetary（消費金額）
   - 自動客戶分類

2. **客戶終身價值（CLV）**
   - 簡單 CLV 計算
   - 折現現金流 CLV
   - 潛在價值分析
   - CLV 分佈和帕累托分析

3. **群組分析**
   - 按月份建立客戶群組
   - 留存率計算
   - 收益追蹤
   - 群組行為分析

4. **行為分析**
   - 購買模式分析
   - 流失風險評估
   - 參與度指標
   - 季節性分析

5. **推薦引擎**
   - 留存活動建議
   - 增銷機會識別
   - 個性化優惠生成
   - 產品推薦
   - 客戶重啟策略

6. **客戶細分**
   - VIP 客戶識別
   - 風險客戶預警
   - 成長潛力客戶
   - 沉睡客戶激活

## 專案結構

```
project2_customer_insights/
├── main.py                  # 主程式（約 280 行）
├── rfm_analyzer.py          # RFM 分析模組（約 320 行）
├── cohort_analyzer.py       # 群組分析模組（約 280 行）
├── clv_calculator.py        # CLV 計算模組（約 360 行）
├── behavior_analyzer.py     # 行為分析模組（約 380 行）
├── recommendation_engine.py # 推薦引擎模組（約 420 行）
├── report_generator.py      # 報告生成模組（約 380 行）
├── config.yaml              # 配置檔
├── requirements.txt         # 依賴清單
└── README.md                # 專案說明
```

## 快速開始

### 1. 安裝依賴

```bash
cd project2_customer_insights
pip install -r requirements.txt
```

### 2. 準備數據

```
data/
├── orders.csv          # 訂單數據
└── customers.csv       # 客戶數據
```

### 3. 運行系統

```bash
python main.py --config config.yaml
```

## 模組說明

### RFMAnalyzer
- `calculate_rfm()`: 計算 RFM 分數
- `segment_customers()`: 客戶分類
- `identify_vip_customers()`: VIP 識別
- `identify_at_risk_customers()`: 風險客戶識別
- `calculate_customer_value_index()`: 客戶價值指數

### CLVCalculator
- `calculate_clv()`: 計算終身價值
- `segment_by_clv()`: 按 CLV 分類
- `analyze_clv_distribution()`: 分佈分析
- `forecast_clv()`: CLV 預測
- `calculate_customer_acquisition_roi()`: 獲取 ROI

### CohortAnalyzer
- `create_cohort_table()`: 建立群組表
- `calculate_retention()`: 留存率計算
- `calculate_revenue_cohort()`: 收益群組
- `analyze_cohort_behavior()`: 行為分析
- `forecast_cohort_value()`: 價值預測

### BehaviorAnalyzer
- `analyze_behavior()`: 行為分析
- `identify_loyal_customers()`: 忠誠客戶
- `identify_seasonal_customers()`: 季節性客戶

### RecommendationEngine
- `generate_recommendations()`: 生成推薦
- `_generate_retention_campaigns()`: 留存活動
- `_generate_upsell_opportunities()`: 增銷機會
- `_generate_personalized_offers()`: 個性化優惠
- `_generate_reactivation_targets()`: 重啟目標

## 數據格式

### orders.csv
```
order_id,customer_id,order_date,order_amount,product_category,payment_method
```

### customers.csv
```
customer_id,email,registration_date,segment,lifetime_value
```

## 輸出報告

系統生成以下報告：

1. **Excel 儀表板**
   - RFM 分析工作表
   - CLV 分析工作表
   - 群組分析工作表
   - 行為分析工作表
   - 推薦活動工作表
   - 客戶分類工作表
   - 摘要工作表

2. **PDF 報告**
   - 完整的分析報告

3. **JSON 數據**
   - 機器可讀的數據格式

## 關鍵指標

### RFM 指標
- **R 分數（1-5）**：最近購買距離，5 最佳
- **F 分數（1-5）**：購買頻率，5 最佳
- **M 分數（1-5）**：消費金額，5 最佳
- **RFM 總分（3-15）**：綜合得分

### CLV 指標
- **簡單 CLV**：基於歷史平均的簡單計算
- **折現 CLV**：考慮時間價值的精確計算
- **歷史價值**：已實現的客戶價值
- **未來價值**：預期未來收入

### 行為指標
- **活躍率**：最近 30 天有購買的客戶比例
- **回購率**：購買超過一次的客戶比例
- **流失率**：90 天未購買的客戶比例
- **風險率**：45-90 天未購買的客戶比例

## 使用示例

### 基本使用

```python
from main import CustomerInsightsSystem

system = CustomerInsightsSystem('config.yaml')
result = system.run()

if result['status'] == 'success':
    print(f"Excel: {result['outputs']['excel']}")
    print(f"PDF: {result['outputs']['pdf']}")
```

### 自訂分析

```python
from rfm_analyzer import RFMAnalyzer
import pandas as pd

# 加載數據
orders = pd.read_csv('data/orders.csv')
customers = pd.read_csv('data/customers.csv')

# 執行 RFM 分析
analyzer = RFMAnalyzer({})
rfm_scores = analyzer.calculate_rfm(orders, customers)
segments = analyzer.segment_customers(rfm_scores)

print(segments)
```

## 客戶分類說明

### RFM 分類
- **VIP**：高 R、高 F、高 M - 價值最高的客戶
- **Loyal（忠誠）**：高 F、高 M - 穩定的高價值客戶
- **Big Spender（大客戶）**：高 M - 單次消費高但不頻繁
- **Active（活躍）**：高 F - 頻繁購買但金額不高
- **New（新客）**：低 R - 最近加入的新客戶
- **At Risk（風險）**：低 R、低 F - 面臨流失風險
- **Dormant（沉睡）**：低 R、低 M - 長時間未購買
- **Regular（普通）**：中等 - 普通客戶

### CLV 分類
- **Very High（非常高）**：$750+
- **High（高）**：$500-749
- **Medium（中等）**：$250-499
- **Low（低）**：$0-249

## 推薦活動

系統建議的推薦活動包括：

1. **留存活動**
   - 針對風險客戶的折扣優惠
   - 免費運輸促銷
   - 購物積分獎勵

2. **增銷機會**
   - 推薦相關高端產品
   - 套裝促銷
   - 量購優惠

3. **個性化優惠**
   - 基於客戶價值的差異化優惠
   - VIP 客戶獨家特權
   - 分類客戶定向優惠

4. **客戶重啟**
   - 特別回歸折扣
   - 驚喜禮物
   - 優先訪問新產品

## 配置說明

編輯 `config.yaml` 自訂系統：

```yaml
clv:
  discount_rate: 0.1          # 10% 折現率
  projection_period: 36       # 36個月預測

behavior:
  churn_threshold_days: 90    # 90天無購買視為流失
  active_threshold_days: 30   # 30天內有購買視為活躍
```

## 常見問題

**Q：如何處理缺失數據？**
A：系統自動處理缺失值，可在配置中調整策略。

**Q：如何自訂 RFM 權重？**
A：編輯 config.yaml 中的 rfm 部分。

**Q：支持實時計算嗎？**
A：當前支持批量處理，實時功能可通過修改主程序實現。

**Q：如何集成到現有系統？**
A：通過 API 接口或數據庫連接，詳見集成指南。

## 性能優化

1. **批量處理**：系統自動優化大型數據集的處理
2. **快取機制**：常用計算結果自動快取
3. **並行處理**：支持多進程加速

## 擴展功能

### 添加新分析

```python
def custom_analysis(orders_df, customers_df):
    """自訂分析"""
    # 實現分析邏輯
    return result

system.analyses['custom'] = custom_analysis(orders, customers)
```

### 集成機器學習

```python
from sklearn.cluster import KMeans

# 使用 KMeans 進行客戶聚類
kmeans = KMeans(n_clusters=5)
clusters = kmeans.fit_predict(rfm_scores[['r_score', 'f_score', 'm_score']])
```

## 技術支援

- 查看 `customer_insights.log` 了解執行詳情
- 檢查數據格式和編碼
- 驗證配置文件語法

## 許可證

MIT License

---

**版本**：1.0.0
**最後更新**：2024-01-15
