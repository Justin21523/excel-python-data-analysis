# Week 15-20 Capstone Projects - 安裝和執行指南

## 系統要求

- Python 3.8+
- pip 或 conda
- 4GB 以上 RAM
- 1GB 以上磁碟空間

## 安裝步驟

### 1. 克隆或下載專案

```bash
cd /home/justin/web-projects/excel-python-data-analysis
ls week15-20_capstone-projects/
```

### 2. 建立虛擬環境（推薦）

```bash
cd week15-20_capstone-projects

# Linux/Mac
python3 -m venv venv
source venv/bin/activate

# Windows
python -m venv venv
venv\Scripts\activate
```

### 3. 安裝依賴

**方式一：安裝所有項目的共同依賴**

```bash
pip install -r requirements_all.txt
```

**方式二：逐個項目安裝**

```bash
# Project 1
cd project1_sales_intelligence
pip install -r requirements.txt
cd ..

# Project 2
cd project2_customer_insights
pip install -r requirements.txt
cd ..

# 以此類推...
```

**方式三：使用 conda**

```bash
conda create -n capstone python=3.9
conda activate capstone
pip install -r requirements_all.txt
```

### 4. 驗證安裝

```bash
python -c "import pandas; print(f'Pandas {pandas.__version__}')"
python -c "import numpy; print(f'NumPy {numpy.__version__}')"
python -c "import yaml; print('YAML OK')"
```

## 執行專案

### 快速開始（執行所有項目）

```bash
# 方式一：順序執行
bash run_all.sh

# 方式二：Python 執行
python run_all.py

# 方式三：Docker 執行
docker run -v $(pwd):/app capstone-projects:latest
```

### 執行單個項目

```bash
# Project 1: Sales Intelligence
cd project1_sales_intelligence
python main.py

# Project 2: Customer Insights
cd project2_customer_insights
python main.py

# Project 3: Inventory Optimizer
cd project3_inventory_optimizer
python main.py

# Project 4: Operations Monitor
cd project4_operations_monitor
python main.py

# Project 5: Executive Dashboard
cd project5_executive_dashboard
python main.py
```

### 執行帶參數

```bash
# 指定配置文件
python main.py --config custom_config.yaml

# 設置日誌級別
python main.py --log-level DEBUG

# 設置輸出目錄
python main.py --output ./custom_output
```

## 數據準備

### Project 1-2：需要訂單和客戶數據

```
data/
├── olist_orders_dataset.csv
├── olist_customers_dataset.csv
├── olist_products_dataset.csv
├── olist_order_items_dataset.csv
└── olist_order_reviews_dataset.csv
```

### Project 3：需要庫存數據

```
data/
├── products.csv
├── inventory.csv
└── sales.csv
```

### Project 4：需要運營數據

```
data/
├── orders.csv
├── support_tickets.csv
└── inventory_transactions.csv
```

如果沒有數據，系統會自動生成示範數據。

## 輸出文件位置

執行完成後，輸出文件位於各項目的 `outputs/` 目錄：

```
project1_sales_intelligence/outputs/
├── sales_dashboard_YYYYMMDD_HHMMSS.xlsx
├── sales_report_YYYYMMDD_HHMMSS.pdf
├── analytics_YYYYMMDD_HHMMSS.json
└── charts/
    ├── sales_trend.png
    ├── top_products.png
    ├── regional_heatmap.png
    └── abc_classification.png

project2_customer_insights/outputs/
├── customer_insights_YYYYMMDD_HHMMSS.xlsx
├── customer_report_YYYYMMDD_HHMMSS.pdf
└── customer_insights_YYYYMMDD_HHMMSS.json

project3_inventory_optimizer/outputs/
└── inventory_report_YYYYMMDD_HHMMSS.txt

project4_operations_monitor/outputs/
└── operations_report_YYYYMMDD_HHMMSS.txt

project5_executive_dashboard/outputs/
├── executive_report_YYYYMMDD_HHMMSS.html
└── executive_report_YYYYMMDD_HHMMSS.json
```

## 故障排除

### 問題 1：ModuleNotFoundError

```bash
# 解決方案
pip install -r requirements_all.txt
```

### 問題 2：文件不存在

```bash
# 檢查數據目錄
ls -la data/

# 創建必要的目錄
mkdir -p data outputs
```

### 問題 3：權限錯誤（Linux/Mac）

```bash
# 授予執行權限
chmod +x run_all.sh
```

### 問題 4：Python 版本不符

```bash
# 檢查版本
python --version

# 使用指定版本
python3.9 main.py

# 升級 Python
conda install python=3.9
```

### 問題 5：內存不足

```bash
# 減少批量大小
# 編輯 config.yaml
performance:
  batch_size: 5000  # 從 10000 減少到 5000
```

## 配置調整

### 修改分析參數

編輯各項目的 `config.yaml`：

```yaml
# Project 1：銷售分析
analytics:
  anomaly_detection:
    std_threshold: 2.0  # 調整異常檢測敏感度

# Project 2：客戶分析
clv:
  discount_rate: 0.1    # 調整折現率
  projection_period: 36 # 調整預測期限

# Project 3：庫存優化
optimization:
  service_level: 0.95   # 調整服務水平

# Project 4：運營監控
monitoring:
  thresholds:
    order_completion_rate: 95  # 調整完成率閾值
```

## 日誌查看

```bash
# 查看最近的日誌
tail -f project1_sales_intelligence/sales_intelligence.log

# 查看特定級別的日誌
grep "ERROR" project*/*/log/*.log

# 整合所有日誌
cat project*/*/*.log | sort -r | head -100
```

## 性能優化

### 1. 並行執行

```bash
# 同時執行多個項目
(cd project1_sales_intelligence && python main.py) &
(cd project2_customer_insights && python main.py) &
(cd project3_inventory_optimizer && python main.py) &
wait
```

### 2. 數據快取

```python
# 在 Python 中啟用快取
import functools

@functools.lru_cache(maxsize=128)
def expensive_function():
    pass
```

### 3. 批量處理

```python
# 分批處理大型數據集
for chunk in pd.read_csv('large_file.csv', chunksize=10000):
    process(chunk)
```

## Docker 部署

### 建立 Docker 映像

```dockerfile
FROM python:3.9-slim

WORKDIR /app
COPY . /app
RUN pip install -r requirements_all.txt

CMD ["python", "run_all.py"]
```

### 執行

```bash
# 建立映像
docker build -t capstone-projects:latest .

# 執行容器
docker run -v $(pwd)/outputs:/app/outputs capstone-projects:latest

# 執行單個項目
docker run capstone-projects:latest \
  bash -c "cd project1_sales_intelligence && python main.py"
```

## 排程執行

### Linux Cron

```bash
# 編輯 crontab
crontab -e

# 每天上午 8 點執行
0 8 * * * cd /path/to/capstone && bash run_all.sh >> /var/log/capstone.log 2>&1
```

### Windows Task Scheduler

```batch
REM 建立批次文件 run_capstone.bat
cd C:\path\to\capstone
python run_all.py
```

## 監控和告警

### 執行狀態監控

```python
import logging
import sys

# 設置日誌級別
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# 記錄執行進度
logger.info("開始執行 Project 1")

try:
    # 執行代碼
    pass
except Exception as e:
    logger.error(f"執行失敗: {e}")
    sys.exit(1)

logger.info("執行完成")
```

### 郵件通知

```python
import smtplib
from email.mime.text import MIMEText

def send_notification(subject, message):
    # 配置郵件參數
    sender = "admin@company.com"
    recipients = ["manager@company.com"]

    msg = MIMEText(message)
    msg['Subject'] = subject
    msg['From'] = sender
    msg['To'] = ', '.join(recipients)

    # 發送郵件
    with smtplib.SMTP('smtp.gmail.com', 587) as server:
        server.starttls()
        server.login(sender, 'password')
        server.send_message(msg)
```

## 版本管理

### 檢查版本

```bash
python -c "import importlib; print(importlib.import_module('module').__version__)"
```

### 升級依賴

```bash
# 升級所有套件
pip install --upgrade -r requirements_all.txt

# 升級特定套件
pip install --upgrade pandas numpy
```

## 備份和恢復

### 備份輸出

```bash
# 建立備份
tar -czf capstone_outputs_$(date +%Y%m%d).tar.gz project*/outputs/

# 恢復備份
tar -xzf capstone_outputs_20240115.tar.gz
```

### 版本控制

```bash
# 初始化 Git
git init
git add .
git commit -m "Initial commit: Capstone projects"

# 標記版本
git tag -a v1.0.0 -m "Release version 1.0.0"
```

## 支援和幫助

### 查看幫助信息

```bash
python main.py --help
```

### 檢查依賴

```bash
pip check
```

### 診斷信息

```bash
python -c "import sys, platform; print(f'Python {sys.version}'); print(f'Platform {platform.platform()}')"
```

### 常見問題解決

查看各項目的 README.md 和故障排除部分。

---

**上次更新**：2024-01-15
