# Week 7-8 openpyxl 完全掌握 - 執行指南

## 目錄

1. [環境設置](#環境設置)
2. [執行方式](#執行方式)
3. [單個案例執行](#單個案例執行)
4. [批量執行](#批量執行)
5. [輸出檔案說明](#輸出檔案說明)
6. [故障排除](#故障排除)

---

## 環境設置

### 系統要求
- Python 3.7+
- 可訪問的 Olist 資料集（位置：`/mnt/data/datasets/ecommerce/kaggle/olist/`）

### 安裝依賴庫

```bash
# 使用 pip
pip install pandas openpyxl matplotlib numpy

# 或使用 conda
conda install pandas openpyxl matplotlib numpy
```

### 驗證環境

```bash
# 檢查 Python 版本
python --version

# 檢查必要庫是否安裝
python -c "import pandas, openpyxl, matplotlib; print('所有庫已安裝')"
```

---

## 執行方式

### 方式 1：使用 Python 直接執行

**執行單個案例：**
```bash
cd /home/justin/web-projects/excel-python-data-analysis/week07-08_openpyxl-mastery

# 執行 Case 1
python case01_styled_monthly_report.py

# 執行 Case 2
python case02_multi_sheet_consolidation.py
```

### 方式 2：使用 python3（推薦）

```bash
python3 case01_styled_monthly_report.py
```

### 方式 3：批量執行所有案例

```bash
# 使用提供的批量執行腳本
bash run_all_cases.sh
```

---

## 單個案例執行

### Case 1: 格式化月報自動生成
```bash
python case01_styled_monthly_report.py
```

**預期輸出：**
- 檔案：`case01_monthly_report.xlsx`
- 工作表：1 個
- 資料筆數：約 40 個月份
- 執行時間：5-10 秒

**輸出示例：**
```
======================================================================
案例1：格式化月報自動生成
======================================================================

[1/5] 載入 Olist 資料...
[2/5] 準備資料...
[3/5] 計算月度統計...
[4/5] 建立 Excel 工作簿...
[5/5] 應用格式和樣式...

======================================================================
✅ 月報已生成！
======================================================================
📊 檔案位置：.../case01_monthly_report.xlsx
📊 資料筆數：40 個月份
📊 總訂單數：99,441
📊 總銷售額：R$ 15,200,000.00
📊 總客戶數：99,441
📊 平均毛利率：78.50%

✓ Excel 格式化特性：
  • 標題列：粗體、藍底白字、置中
  • 邊框：所有儲存格有邊框
  • 數值格式：千分位、小數位、百分比
  • 自動調整欄寬：根據內容最適化
  • 凍結窗格：固定標題列
```

### Case 2: 多工作表自動整合
```bash
python case02_multi_sheet_consolidation.py
```

**預期輸出：**
- 檔案：`case02_multi_sheet_report.xlsx`
- 工作表：6 個（目錄 + 5 個資料工作表）
- 執行時間：10-15 秒

### Case 3: 條件格式自動化
```bash
python case03_conditional_formatting.py
```

**預期輸出：**
- 檔案：`case03_conditional_formatting.xlsx`
- 工作表：1 個
- 行數：30 行賣家資料
- 執行時間：5-8 秒

### Case 4: 動態圖表生成
```bash
python case04_dynamic_chart_generation.py
```

**預期輸出：**
- 檔案：`case04_dynamic_charts.xlsx`
- 工作表：4 個（3 個圖表 + 1 個資料）
- 圖表類型：長條圖、折線圖、圓餅圖、面積圖
- 執行時間：10-15 秒

### Case 5: 公式注入
```bash
python case05_formula_injection.py
```

**預期輸出：**
- 檔案：`case05_formula_injection.xlsx`
- 工作表：1 個
- 公式數：每行 3 個公式 + 統計區域 5 個公式
- 執行時間：5-8 秒

### Case 6: 模板化報表
```bash
python case06_template_based_reports.py
```

**預期輸出：**
- 檔案：`case06_template_reports.xlsx`
- 工作表：3 個（銷售、客戶、供應商報告）
- 執行時間：10-12 秒

### Case 7: 資料驗證
```bash
python case07_data_validation.py
```

**預期輸出：**
- 檔案：`case07_data_validation.xlsx`
- 工作表：2 個（資料輸入 + 驗證說明）
- 驗證規則：7 個
- 執行時間：8-10 秒

### Case 8: 執行摘要（高級報表）
```bash
python case08_executive_summary.py
```

**預期輸出：**
- 檔案：`case08_executive_summary.xlsx`
- 工作表：1 個
- KPI 指標：6 個
- 執行時間：8-10 秒

### Case 9: 儲存格合併
```bash
python case09_cell_merging.py
```

**預期輸出：**
- 檔案：`case09_cell_merging.xlsx`
- 工作表：1 個
- 合併儲存格：多個分層結構
- 執行時間：5-8 秒

### Case 10: 工作表保護
```bash
python case10_sheet_protection.py
```

**預期輸出：**
- 檔案：`case10_sheet_protection.xlsx`
- 工作表：3 個（受保護報表 + 保護說明 + 資料輸入）
- 密碼：`password123`
- 執行時間：8-10 秒

### Case 11: 超連結和註解
```bash
python case11_hyperlinks_comments.py
```

**預期輸出：**
- 檔案：`case11_hyperlinks_comments.xlsx`
- 工作表：4 個（目錄 + 3 個資料工作表）
- 超連結：4 個
- 註解：多個
- 執行時間：10-12 秒

### Case 12: 圖片插入
```bash
python case12_image_insertion.py
```

**預期輸出：**
- 檔案：`case12_image_insertion.xlsx`、`sample_chart.png`
- 工作表：1 個
- 圖片：matplotlib 生成的圖表
- 圖表：openpyxl 內建圖表
- 執行時間：12-15 秒

### Case 13: 完整自動化系統
```bash
python case13_full_automation_system.py
```

**預期輸出：**
- 檔案：`case13_full_automation_system.xlsx`
- 工作表：6 個（目錄 + 5 個統計報表）
- 日誌記錄：詳細的執行日誌
- 執行時間：15-20 秒

### Case 14: Pandas 和 Excel 完整整合
```bash
python case14_pandas_excel_integration.py
```

**預期輸出：**
- 檔案：`case14_pandas_excel_integration.xlsx`
- 工作表：6 個（數據表 + 樞紐表 + 儀表板）
- 樞紐表：2 個
- 執行時間：15-20 秒

---

## 批量執行

### 使用批量執行腳本

```bash
cd /home/justin/web-projects/excel-python-data-analysis/week07-08_openpyxl-mastery

# 給予執行權限
chmod +x run_all_cases.sh

# 執行所有案例
./run_all_cases.sh
```

### 批量執行預期輸出

```
==========================================
Week 7-8: openpyxl 完全掌握
批量執行所有案例
==========================================

[1/14] 執行 case01_styled_monthly_report.py...
----------------------------------------
✓ case01_styled_monthly_report.py 執行成功

[2/14] 執行 case02_multi_sheet_consolidation.py...
----------------------------------------
✓ case02_multi_sheet_consolidation.py 執行成功

... (以此類推)

==========================================
執行統計摘要
==========================================
總案例數：14
成功數：14
失敗數：0
執行時間：2分30秒

✅ 所有案例執行完成！
```

---

## 輸出檔案說明

### 生成的 Excel 檔案

| 案例 | 輸出檔案 | 工作表數 | 主要內容 |
|-----|--------|--------|--------|
| 1 | case01_monthly_report.xlsx | 1 | 月度銷售報表 |
| 2 | case02_multi_sheet_report.xlsx | 6 | 多維度銷售分析 |
| 3 | case03_conditional_formatting.xlsx | 1 | 條件格式示例 |
| 4 | case04_dynamic_charts.xlsx | 4 | 各類圖表展示 |
| 5 | case05_formula_injection.xlsx | 1 | 公式應用示例 |
| 6 | case06_template_reports.xlsx | 3 | 部門報告模板 |
| 7 | case07_data_validation.xlsx | 2 | 資料驗證規則 |
| 8 | case08_executive_summary.xlsx | 1 | KPI 儀表板 |
| 9 | case09_cell_merging.xlsx | 1 | 分層統計表 |
| 10 | case10_sheet_protection.xlsx | 3 | 保護工作表 |
| 11 | case11_hyperlinks_comments.xlsx | 4 | 超連結導航 |
| 12 | case12_image_insertion.xlsx | 1 | 圖片和圖表 |
| 13 | case13_full_automation_system.xlsx | 6 | 自動化系統報告 |
| 14 | case14_pandas_excel_integration.xlsx | 6 | Pandas 整合報告 |

**總生成檔案數：14 個 Excel + 1 個 PNG 圖片 = 15 個檔案**

### 檔案大小參考

| 檔案 | 預期大小 |
|-----|--------|
| case01_monthly_report.xlsx | 50-100 KB |
| case02_multi_sheet_report.xlsx | 100-150 KB |
| case03_conditional_formatting.xlsx | 80-120 KB |
| case04_dynamic_charts.xlsx | 150-200 KB |
| case05_formula_injection.xlsx | 60-100 KB |
| case06_template_reports.xlsx | 100-150 KB |
| case07_data_validation.xlsx | 80-120 KB |
| case08_executive_summary.xlsx | 100-150 KB |
| case09_cell_merging.xlsx | 70-110 KB |
| case10_sheet_protection.xlsx | 100-150 KB |
| case11_hyperlinks_comments.xlsx | 120-170 KB |
| case12_image_insertion.xlsx | 300-400 KB |
| case13_full_automation_system.xlsx | 150-200 KB |
| case14_pandas_excel_integration.xlsx | 200-300 KB |
| sample_chart.png | 50-80 KB |

---

## 故障排除

### 問題 1：找不到 Olist 資料集

**症狀：**
```
資料載入失敗：[Errno 2] No such file or directory
```

**解決方案：**
1. 檢查資料位置：`ls /mnt/data/datasets/ecommerce/kaggle/olist/`
2. 確保資料集已正確挂載
3. 檢查讀取權限

### 問題 2：缺少依賴庫

**症狀：**
```
ModuleNotFoundError: No module named 'pandas'
```

**解決方案：**
```bash
pip install pandas openpyxl matplotlib numpy
```

### 問題 3：記憶體不足

**症狀：**
```
MemoryError: Unable to allocate ...
```

**解決方案：**
- 減少資料量（修改 `.head()` 的數字）
- 分批處理大型資料集
- 增加系統交換空間

### 問題 4：執行超時

**症狀：**
- 腳本執行超過 5 分鐘

**解決方案：**
1. 檢查系統性能
2. 確保沒有其他資源密集型程序運行
3. 減少資料量進行測試

### 問題 5：無法生成某些圖表

**症狀：**
```
Exception: Cannot add chart to worksheet
```

**解決方案：**
- 檢查 openpyxl 版本（推薦 3.0+）
- 確保圖表數據不為空
- 驗證儲存格引用是否正確

---

## 性能優化建議

### 1. 大型檔案處理

```python
# 使用 write_only 模式
from openpyxl import Workbook
wb = Workbook(write_only=True)
```

### 2. 分批處理資料

```python
# 使用 chunksize 讀取大型 CSV
for chunk in pd.read_csv('file.csv', chunksize=10000):
    # 處理每個批次
    pass
```

### 3. 記憶體優化

```python
# 使用適當的 dtype
df = pd.read_csv('file.csv', dtype={'id': 'int32', 'price': 'float32'})
```

---

## 常見問題 (FAQ)

**Q: 需要多長時間執行所有 14 個案例？**
A: 通常 3-5 分鐘（取決於系統性能和網路速度）

**Q: 生成的 Excel 檔案可以用 LibreOffice/Google Sheets 打開嗎？**
A: 是的，openpyxl 生成的檔案是標準 XLSX 格式

**Q: 我可以修改案例代碼嗎？**
A: 完全可以！建議在修改後創建副本以保持原始案例

**Q: 如何將案例集成到自己的項目中？**
A: 複製相關代碼並根據需要調整資料源和格式

---

## 額外資源

### 官方文檔
- [openpyxl 文檔](https://openpyxl.readthedocs.io/)
- [Pandas 文檔](https://pandas.pydata.org/docs/)

### 相關教程
- Excel 條件格式指南
- openpyxl 最佳實踐
- Pandas 資料轉換技巧

---

**最後更新：** 2024-12-11
**版本：** 1.0
