# Project 1: Sales Intelligence Dashboard
銷售智能儀表板系統 - Week 15

## 項目概述

Sales Intelligence Dashboard 是一個企業級的銷售分析系統，提供全面的銷售數據分析、可視化和自動報告生成功能。

### 主要功能

1. **銷售總覽** (Sales Overview)
   - 今日/本週/本月/本年銷售數據
   - 同期對比分析
   - 成長率計算（月環比、年同比）

2. **產品分析** (Product Analytics)
   - Top 10 熱銷產品
   - ABC 庫存分類
   - 分類表現分析

3. **地區分析** (Regional Analytics)
   - 各地區銷售排名
   - 城市級別銷售數據
   - 地理分佈熱圖

4. **異常檢測** (Anomaly Detection)
   - 銷售額異常偵測
   - 退貨率監控
   - 庫存問題預警

5. **自動報表** (Automated Reports)
   - Excel 儀表板
   - PDF 報告
   - JSON 數據匯出

6. **排程執行** (Scheduled Execution)
   - 每日自動執行
   - 郵件通知
   - 日誌記錄

## 專案結構

```
project1_sales_intelligence/
├── main.py                  # 主程式（約 320 行）
├── data_processor.py        # 數據處理模組（約 420 行）
├── analytics.py             # 分析模組（約 680 行）
├── visualizations.py        # 視覺化模組（約 520 行）
├── report_generator.py      # 報表生成模組（約 450 行）
├── config.yaml              # 配置檔
├── requirements.txt         # 依賴清單
├── README.md                # 專案說明（本檔案）
└── outputs/                 # 輸出目錄
    ├── charts/              # 圖表
    ├── reports/             # 報告
    └── logs/                # 日誌
```

## 快速開始

### 1. 環境設置

```bash
# 進入項目目錄
cd project1_sales_intelligence

# 建立虛擬環境
python -m venv venv
source venv/bin/activate  # Linux/Mac
# 或
venv\Scripts\activate  # Windows

# 安裝依賴
pip install -r requirements.txt
```

### 2. 準備數據

將數據文件放在 `data/` 目錄中：

```
data/
├── olist_orders_dataset.csv
├── olist_order_items_dataset.csv
├── olist_customers_dataset.csv
├── olist_products_dataset.csv
├── olist_order_reviews_dataset.csv
└── olist_sellers_dataset.csv
```

如果沒有真實數據，系統會自動生成示範數據。

### 3. 運行程式

```bash
# 執行單次分析
python main.py

# 指定配置文件
python main.py --config config.yaml

# 啟用排程模式
python main.py --schedule --hour 8
```

### 4. 查看輸出

輸出文件保存在 `outputs/` 目錄：

```
outputs/
├── sales_dashboard_20240115_143022.xlsx
├── sales_report_20240115_143022.pdf
├── analytics_20240115_143022.json
└── charts/
    ├── sales_trend.png
    ├── top_products.png
    ├── regional_heatmap.png
    └── abc_classification.png
```

## 模組說明

### 1. DataProcessor（data_processor.py）

負責數據加載、清洗和轉換。

**主要方法：**

- `load_olist_data()`: 加載 Olist 數據集
- `clean_and_transform()`: 清洗和轉換數據
- `create_time_features()`: 從日期列建立時間特徵
- `handle_missing_values()`: 處理缺失值
- `aggregate_daily_sales()`: 聚合日銷售數據
- `validate_data_quality()`: 驗證數據質量
- `export_to_excel()`: 匯出到 Excel

### 2. SalesAnalytics（analytics.py）

執行銷售分析和異常檢測。

**主要方法：**

- `calculate_daily_sales()`: 計算每日銷售
- `calculate_weekly_sales()`: 計算週銷售
- `calculate_monthly_sales()`: 計算月銷售
- `calculate_yearly_sales()`: 計算年銷售
- `calculate_growth_rates()`: 計算成長率
- `get_top_products()`: 獲取 Top N 產品
- `abc_analysis()`: ABC 分類分析
- `category_analysis()`: 分類分析
- `regional_sales_analysis()`: 地區銷售分析
- `get_top_cities()`: 獲取 Top N 城市
- `detect_sales_anomalies()`: 偵測銷售異常
- `check_return_rates()`: 檢查退貨率
- `check_inventory_issues()`: 檢查庫存問題

### 3. SalesVisualizer（visualizations.py）

生成各種圖表。

**主要圖表：**

- 銷售趨勢圖：各時期銷售對比、訂單數、客戶數、平均訂單價值
- Top 產品圖：按收入和銷量排序
- 地區熱圖：地區銷售排名和分佈
- ABC 分類圖：產品分類和收入分布
- 客戶分佈圖：各地區客戶數
- 儀表板摘要：完整儀表板視圖

### 4. ReportGenerator（report_generator.py）

產生各種報告格式。

**輸出格式：**

- Excel 儀表板：多工作表報告
- PDF 報告：可打印的報告
- JSON 數據：機器可讀的數據格式
- 文字報告：純文字摘要
- 電子郵件：郵件摘要

## 配置說明

編輯 `config.yaml` 自訂系統行為：

### 數據配置

```yaml
data:
  path: './data'
  validation:
    check_duplicates: true
    check_missing_values: true
```

### 分析配置

```yaml
analytics:
  anomaly_detection:
    enabled: true
    std_threshold: 2.0
  abc_analysis:
    a_threshold: 80
    b_threshold: 95
```

### 視覺化配置

```yaml
visualizations:
  output_dir: './outputs/charts'
  dpi: 300
  color_scheme: 'default'
```

### 報表配置

```yaml
output:
  directory: './outputs'
  formats:
    - 'excel'
    - 'pdf'
    - 'json'
```

### 排程配置

```yaml
schedule:
  enabled: false
  run_time: '08:00'
  frequency: 'daily'
```

## 數據流程

```
原始數據 (CSV)
    ↓
[DataProcessor] - 加載、清洗、轉換
    ↓
清洗後數據 (DataFrame)
    ↓
[SalesAnalytics] - 執行分析
    ↓
分析結果
    ├─→ [SalesVisualizer] - 生成圖表
    │   └─→ PNG 圖表
    └─→ [ReportGenerator] - 產生報表
        ├─→ Excel 儀表板
        ├─→ PDF 報告
        └─→ JSON 數據
```

## 使用示例

### 基本使用

```python
from main import SalesIntelligenceDashboard

# 初始化儀表板
dashboard = SalesIntelligenceDashboard('config.yaml')

# 執行分析
result = dashboard.run()

# 查看結果
if result['status'] == 'success':
    print(f"Excel: {result['outputs']['excel']}")
    print(f"PDF: {result['outputs']['pdf']}")
else:
    print(f"錯誤: {result['error']}")
```

### 自訂分析

```python
from data_processor import DataProcessor
from analytics import SalesAnalytics

# 加載數據
processor = DataProcessor({'path': './data'})
data = processor.load_olist_data()
data = processor.clean_and_transform(data)

# 執行分析
analytics = SalesAnalytics()
top_products = analytics.get_top_products(data, n=15)
abc = analytics.abc_analysis(data)

print(top_products)
print(abc['statistics'])
```

## 異常檢測詳解

系統使用 Z-Score 方法偵測銷售異常：

1. **計算統計量**：
   - 平均銷售額 (mean)
   - 標準差 (std)

2. **設定閾值**：
   - 默認閾值：2.0 倍標準差
   - 超出範圍視為異常

3. **異常類型**：
   - 銷售額異常（過高/過低）
   - 退貨率異常
   - 庫存異常

## 性能優化建議

1. **批量處理**：
   ```yaml
   performance:
     batch_size: 10000
   ```

2. **平行處理**：
   ```yaml
   performance:
     parallel_processing: true
     num_workers: 4
   ```

3. **快取**：
   ```yaml
   performance:
     enable_cache: true
   ```

## 故障排除

### 問題 1：找不到數據文件

**解決方案**：
- 確認 `data/` 目錄存在
- 確認 CSV 文件名稱正確
- 檢查文件編碼（應為 UTF-8）

### 問題 2：缺少依賴包

**解決方案**：
```bash
pip install -r requirements.txt --upgrade
```

### 問題 3：無法生成 PDF

**解決方案**：
- 確認 reportlab 已安裝
- 如果失敗，系統會自動使用文字報告

### 問題 4：排程不執行

**解決方案**：
- 確認 `config.yaml` 中 `schedule.enabled: true`
- 檢查系統時間設置
- 查看日誌文件確認執行狀態

## 日誌查看

```bash
# 查看實時日誌
tail -f sales_intelligence.log

# 查看特定級別的日誌
grep "ERROR" sales_intelligence.log
grep "WARNING" sales_intelligence.log
```

## 擴展功能

### 添加新的分析方法

```python
# 在 analytics.py 中添加
def custom_analysis(self, data):
    """自訂分析方法"""
    # 實現分析邏輯
    return result

# 在 main.py 中調用
analyses['custom'] = self.analytics.custom_analysis(self.data)
```

### 添加新的圖表

```python
# 在 visualizations.py 中添加
def plot_custom_chart(self, data, save=True):
    """自訂圖表"""
    # 實現繪圖邏輯
    if save:
        plt.savefig(...)
    return filepath
```

### 集成郵件通知

```python
# 配置 config.yaml
email:
  enabled: true
  smtp:
    server: 'smtp.gmail.com'
    port: 587
  sender_email: 'your-email@gmail.com'
  sender_password: 'app-password'
  recipients:
    - 'manager@company.com'
```

## API 文檔

### 主要類和方法

#### SalesIntelligenceDashboard

```python
class SalesIntelligenceDashboard:
    def __init__(self, config_file='config.yaml')
    def load_and_prepare_data() -> bool
    def analyze_sales_overview() -> dict
    def analyze_products() -> dict
    def analyze_regions() -> dict
    def detect_anomalies() -> dict
    def generate_visualizations(analyses) -> dict
    def generate_reports(analyses, figures) -> tuple[str, str]
    def run() -> dict
    def schedule_daily_run(hour=8, minute=0) -> schedule
```

## 常見指標解釋

- **總收入 (Total Revenue)**：所有訂單的總金額
- **訂單數 (Orders)**：訂單數量
- **平均訂單價值 (AOV)**：總收入 / 訂單數
- **客戶數 (Customers)**：去重後的客戶數量
- **月環比 (MoM)**：本月 vs 上月成長率
- **年同比 (YoY)**：本年 vs 去年成長率
- **ABC 分類**：
  - A 類（20% 產品，80% 收入）
  - B 類（30% 產品，15% 收入）
  - C 類（50% 產品，5% 收入）

## 系統要求

- Python 3.8+
- 4GB RAM（最小）
- 8GB 磁碟空間（用於數據和報告）
- 網絡連接（用於郵件通知）

## 支援的操作系統

- Windows 10+
- macOS 10.14+
- Linux（Ubuntu 18.04+）

## 許可證

MIT License

## 變更日誌

### v1.0.0 (2024-01-15)

- 初始版本發布
- 實現所有核心功能
- 支持 Excel、PDF、JSON 輸出
- 集成排程和郵件通知

## 常見問題

**Q: 如何連接到實時數據源？**
A: 修改 `DataProcessor.load_olist_data()` 方法，添加數據庫或 API 連接。

**Q: 如何自訂異常檢測閾值？**
A: 編輯 `config.yaml` 中的 `analytics.anomaly_detection.std_threshold`。

**Q: 是否支持多語言？**
A: 是的，編輯 `config.yaml` 中的 `system.language` 設置。

**Q: 如何擴展報表格式？**
A: 在 `report_generator.py` 中添加新的 `create_xxx_report()` 方法。

## 技術支援

如有問題，請檢查以下資源：

1. 查看 `sales_intelligence.log` 日誌文件
2. 確認所有依賴已正確安裝
3. 驗證 `config.yaml` 配置
4. 檢查數據文件格式和編碼

## 未來計劃

- [ ] 實時儀表板（Web UI）
- [ ] 預測分析（時間序列預測）
- [ ] 機器學習模型（客戶分段）
- [ ] 數據倉庫整合
- [ ] 移動應用支持
- [ ] 多語言支持改進

---

**作者**：Data Analytics Team
**版本**：1.0.0
**最後更新**：2024-01-15
