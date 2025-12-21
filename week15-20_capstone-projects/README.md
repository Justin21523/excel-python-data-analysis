# Week 15-20: Five Capstone Projects
第 15-20 週：五大 Capstone 專案

## 項目概述

這是一套完整的企業級數據分析解決方案，包含五個相互關聯的 Capstone 專案，涵蓋銷售、客戶、庫存、運營和執行官層面的全方位業務分析。

## 項目清單

### Project 1: Sales Intelligence Dashboard (Week 15)
**銷售智能儀表板系統**

位置：`project1_sales_intelligence/`

**功能：**
- 銷售總覽（今日/本週/本月/本年）
- 產品分析（Top 10、ABC 分類）
- 地區分析（銷售排名、熱圖）
- 異常檢測
- Excel/PDF 自動報表
- 排程執行

**主要模組：**
- `main.py` (320 行) - 主程式
- `data_processor.py` (420 行) - 數據處理
- `analytics.py` (680 行) - 分析引擎
- `visualizations.py` (520 行) - 圖表生成
- `report_generator.py` (450 行) - 報表生成

**輸出：**
- Excel 儀表板（多工作表）
- PDF 報告
- JSON 數據
- PNG 圖表

---

### Project 2: Customer Insights System (Week 16-17)
**客戶洞察系統**

位置：`project2_customer_insights/`

**功能：**
- RFM 分析（Recency, Frequency, Monetary）
- 客戶終身價值（CLV）計算
- 群組分析（Cohort Analysis）
- 客戶行為分析
- 個性化推薦引擎
- 客戶細分

**主要模組：**
- `main.py` (280 行) - 主程式
- `rfm_analyzer.py` (320 行) - RFM 分析
- `clv_calculator.py` (360 行) - CLV 計算
- `cohort_analyzer.py` (280 行) - 群組分析
- `behavior_analyzer.py` (380 行) - 行為分析
- `recommendation_engine.py` (420 行) - 推薦引擎
- `report_generator.py` (380 行) - 報告生成

**客戶分類：**
- VIP 客戶
- 忠誠客戶
- 風險客戶
- 沉睡客戶
- 成長潛力客戶

**輸出：**
- Excel 分析報告
- RFM 分數和分類
- CLV 計算結果
- 推薦活動清單

---

### Project 3: Inventory Optimization System (Week 18)
**庫存優化系統**

位置：`project3_inventory_optimizer/`

**功能：**
- 需求預測（Demand Forecasting）
- 庫存優化（EOQ 計算）
- 安全庫存計算
- 訂單點（Reorder Point）計算
- ABC 庫存分類
- 自動補充建議
- 成本分析

**主要計算：**
- 經濟訂單量（EOQ）
- 安全庫存（Safety Stock）
- 訂單點（Reorder Point）
- 持有成本（Holding Cost）
- 訂購成本（Ordering Cost）

**輸出：**
- 補充建議清單
- 庫存優化報告
- 成本分析

---

### Project 4: Operations Monitoring System (Week 19)
**運營監控系統**

位置：`project4_operations_monitor/`

**功能：**
- KPI 監控
- 實時警告系統
- 效率分析
- 流程監控
- 異常檢測
- 儀表板

**監控指標：**
- 訂單完成率
- 準時交付率
- 客戶滿意度
- 平均處理時間
- 客服解決時間

**輸出：**
- 監控報告
- 警告提醒
- 效率分析
- 異常詳情

---

### Project 5: Executive Dashboard System (Week 20)
**執行官儀表板系統**

位置：`project5_executive_dashboard/`

**功能：**
- 整合所有項目數據
- 執行級別儀表板
- 實時洞察
- 戰略建議
- 高層報告

**整合內容：**
- 銷售數據（Project 1）
- 客戶數據（Project 2）
- 庫存數據（Project 3）
- 運營數據（Project 4）

**輸出：**
- HTML 互動儀表板
- PDF 執行報告
- 戰略洞察
- 建議清單

---

## 目錄結構

```
week15-20_capstone-projects/
├── project1_sales_intelligence/
│   ├── main.py
│   ├── data_processor.py
│   ├── analytics.py
│   ├── visualizations.py
│   ├── report_generator.py
│   ├── config.yaml
│   ├── requirements.txt
│   ├── README.md
│   └── outputs/
│
├── project2_customer_insights/
│   ├── main.py
│   ├── rfm_analyzer.py
│   ├── clv_calculator.py
│   ├── cohort_analyzer.py
│   ├── behavior_analyzer.py
│   ├── recommendation_engine.py
│   ├── report_generator.py
│   ├── config.yaml
│   ├── requirements.txt
│   └── README.md
│
├── project3_inventory_optimizer/
│   ├── main.py
│   ├── config.yaml
│   ├── requirements.txt
│   └── README.md
│
├── project4_operations_monitor/
│   ├── main.py
│   ├── config.yaml
│   ├── requirements.txt
│   └── README.md
│
├── project5_executive_dashboard/
│   ├── main.py
│   ├── config.yaml
│   ├── requirements.txt
│   └── README.md
│
└── README.md (本檔案)
```

## 快速開始

### 1. 環境設置

```bash
# 進入主目錄
cd week15-20_capstone-projects

# 建立虛擬環境
python -m venv venv
source venv/bin/activate  # Linux/Mac
# 或
venv\Scripts\activate  # Windows
```

### 2. 安裝依賴

```bash
# 安裝所有項目的依賴
pip install pandas numpy openpyxl matplotlib seaborn scikit-learn scipy PyYAML reportlab

# 或個別安裝
cd project1_sales_intelligence
pip install -r requirements.txt
```

### 3. 運行項目

```bash
# 運行 Project 1: Sales Intelligence
cd project1_sales_intelligence
python main.py

# 運行 Project 2: Customer Insights
cd project2_customer_insights
python main.py

# 運行 Project 3: Inventory Optimization
cd project3_inventory_optimizer
python main.py

# 運行 Project 4: Operations Monitoring
cd project4_operations_monitor
python main.py

# 運行 Project 5: Executive Dashboard
cd project5_executive_dashboard
python main.py
```

## 數據流程

```
原始業務數據
    ↓
Project 1: 銷售分析 → 銷售洞察
    ↓                ↓
Project 2: 客戶分析 → 客戶洞察
    ↓                ↓
Project 3: 庫存優化 → 庫存建議
    ↓                ↓
Project 4: 運營監控 → 運營健康
    ↓                ↓
    └───→ Project 5: 執行官儀表板 → 戰略建議
            ↓
        高層決策支持
```

## 集成方案

### 按順序執行（推薦）

```bash
#!/bin/bash

echo "執行 Week 15-20 Capstone 專案..."

cd project1_sales_intelligence
python main.py && echo "✓ Project 1 完成"

cd ../project2_customer_insights
python main.py && echo "✓ Project 2 完成"

cd ../project3_inventory_optimizer
python main.py && echo "✓ Project 3 完成"

cd ../project4_operations_monitor
python main.py && echo "✓ Project 4 完成"

cd ../project5_executive_dashboard
python main.py && echo "✓ Project 5 完成"

echo "所有項目執行完成！"
```

### Python 集成

```python
import sys
from pathlib import Path

# Project 1
sys.path.insert(0, str(Path('project1_sales_intelligence')))
from main import SalesIntelligenceDashboard
sales_result = SalesIntelligenceDashboard().run()

# Project 2
sys.path.insert(0, str(Path('project2_customer_insights')))
from main import CustomerInsightsSystem
customer_result = CustomerInsightsSystem().run()

# Project 5
sys.path.insert(0, str(Path('project5_executive_dashboard')))
from main import ExecutiveDashboardSystem
executive_result = ExecutiveDashboardSystem().run()
```

## 配置說明

每個項目都有 `config.yaml` 配置文件：

### Project 1 配置示例

```yaml
data:
  path: './data'

analytics:
  anomaly_detection:
    enabled: true
    std_threshold: 2.0

output:
  formats:
    - 'excel'
    - 'pdf'
    - 'json'
```

### Project 2 配置示例

```yaml
rfm:
  recency_weight: 0.2
  frequency_weight: 0.3
  monetary_weight: 0.5

clv:
  discount_rate: 0.1
  projection_period: 36
```

## 輸出文件說明

### Excel 文件

- `sales_dashboard_YYYYMMDD_HHMMSS.xlsx` - 銷售儀表板
- `customer_insights_YYYYMMDD_HHMMSS.xlsx` - 客戶分析

### PDF 文件

- `sales_report_YYYYMMDD_HHMMSS.pdf` - 銷售報告
- `customer_report_YYYYMMDD_HHMMSS.pdf` - 客戶報告

### HTML 文件

- `executive_report_YYYYMMDD_HHMMSS.html` - 執行官儀表板

### 圖表文件

- `sales_trend.png` - 銷售趨勢
- `top_products.png` - Top 產品
- `regional_heatmap.png` - 地區熱圖
- `abc_classification.png` - ABC 分類

## 學習成果

完成這五個 Capstone 專案後，你將掌握：

### 技能
- Excel/Python 數據分析和轉換
- 統計分析和預測建模
- 數據視覺化和報告生成
- 系統設計和整合
- 項目管理和部署

### 知識
- 銷售分析方法論
- 客戶價值評估（RFM, CLV）
- 庫存優化理論（EOQ, 安全庫存）
- KPI 監控和異常檢測
- 執行級別決策支持

### 工具
- Pandas, NumPy - 數據處理
- Matplotlib, Seaborn - 數據可視化
- Scikit-learn - 機器學習
- ReportLab - 報告生成
- Openpyxl - Excel 操作

## 常見問題

**Q: 如何處理大型數據集？**
A: 使用批量處理、數據分片和優化的查詢方法。

**Q: 能否實時更新數據？**
A: 可以通過添加數據庫連接和排程任務實現。

**Q: 如何自訂分析指標？**
A: 編輯對應模組的 Python 代碼或配置文件。

**Q: 支持多語言嗎？**
A: 當前為中文，可通過修改文本字符串支持其他語言。

**Q: 如何部署到生產環境？**
A: 使用 Docker, Kubernetes 或云服務進行部署。

## 擴展建議

1. **數據庫集成**
   - 連接 MySQL, PostgreSQL 或 MongoDB
   - 實現實時數據同步

2. **實時儀表板**
   - 使用 Dash, Streamlit 或 Power BI
   - 構建交互式 Web 應用

3. **機器學習**
   - 添加需求預測模型
   - 實現客戶流失預測
   - 產品推薦算法

4. **自動化**
   - 使用 Airflow 進行 ETL 排程
   - 實現郵件自動通知
   - API 集成

5. **移動應用**
   - 開發移動儀表板
   - 實時警告通知
   - 離線數據存儲

## 性能優化

### 數據處理
```python
# 使用 Dask 進行並行處理
import dask.dataframe as dd
ddf = dd.read_csv('large_file.csv')
result = ddf.groupby('column').sum().compute()
```

### 查詢優化
```python
# 使用索引加速查詢
df.set_index('customer_id')
df.loc[customer_id]
```

### 內存管理
```python
# 使用數據類型優化
df['amount'] = df['amount'].astype('float32')
df['category'] = df['category'].astype('category')
```

## 故障排除

### 常見錯誤

1. **ModuleNotFoundError**
   ```bash
   pip install -r requirements.txt
   ```

2. **文件編碼問題**
   ```python
   pd.read_csv('file.csv', encoding='utf-8')
   ```

3. **日期解析問題**
   ```python
   pd.to_datetime(df['date'], format='%Y-%m-%d')
   ```

4. **內存溢出**
   ```python
   # 分批處理
   for chunk in pd.read_csv('file.csv', chunksize=10000):
       process(chunk)
   ```

## 技術支援

- 查看各項目的 `README.md`
- 查看日誌文件：`.log` 文件
- 檢查配置文件語法
- 驗證輸入數據格式

## 許可證

MIT License

## 作者

Data Analysis Training Program

## 版本歷史

### v1.0.0 (2024-01-15)
- 初始版本發布
- 完成所有五個項目
- 支持 Excel、PDF、JSON 輸出
- 集成項目間的數據流

## 相關資源

- Python 官方文檔：https://docs.python.org
- Pandas 文檔：https://pandas.pydata.org
- Matplotlib 文檔：https://matplotlib.org
- Scikit-learn 文檔：https://scikit-learn.org

---

**總行數：** 約 4,500+ 行代碼
**模組數：** 25+ 個模組
**功能數：** 100+ 項功能
**配置項：** 50+ 個配置參數

祝你學習愉快！
