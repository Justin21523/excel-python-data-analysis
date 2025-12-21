# Week 7-8 openpyxl 完全掌握 - 快速開始指南

## 5 分鐘快速開始

### 1. 環境準備

```bash
# 安裝依賴
pip install pandas openpyxl matplotlib numpy

# 進入目錄
cd /home/justin/web-projects/excel-python-data-analysis/week07-08_openpyxl-mastery
```

### 2. 執行第一個案例

```bash
# 執行案例 1：格式化月報自動生成
python case01_styled_monthly_report.py

# 輸出檔案
# case01_monthly_report.xlsx
```

### 3. 查看結果

生成的 Excel 檔案包含：
- 已格式化的月度銷售報表
- 粗體標題列和藍色背景
- 自動調整的欄寬
- 凍結的標題行
- 千分位和百分比格式

---

## 10 個必學 openpyxl 技巧

### 技巧 1：基礎寫入

```python
from openpyxl import Workbook

wb = Workbook()
ws = wb.active
ws['A1'] = 'Hello'
wb.save('output.xlsx')
```

### 技巧 2：應用樣式

```python
from openpyxl.styles import Font, PatternFill, Alignment

ws['A1'].font = Font(bold=True, color='FFFFFF')
ws['A1'].fill = PatternFill(start_color='1F4E78', fill_type='solid')
ws['A1'].alignment = Alignment(horizontal='center', vertical='center')
```

### 技巧 3：數值格式化

```python
# 千分位格式
ws['A1'].number_format = '#,##0'

# 貨幣格式
ws['A1'].number_format = '#,##0.00'

# 百分比格式
ws['A1'].number_format = '0.00%'

# 日期格式
ws['A1'].number_format = 'YYYY-MM-DD'
```

### 技巧 4：批量操作

```python
# 遍歷所有儲存格
for row in ws.iter_rows(min_row=1, max_row=100):
    for cell in row:
        cell.font = Font(bold=True)
```

### 技巧 5：建立公式

```python
ws['C1'] = '=A1+B1'          # 加法
ws['C2'] = '=SUM(A1:A100)'   # 求和
ws['C3'] = '=AVERAGE(A1:A10)' # 平均值
ws['C4'] = '=IF(A1>100,"高","低")' # 條件判斷
```

### 技巧 6：插入圖表

```python
from openpyxl.chart import BarChart, Reference

chart = BarChart()
chart.title = "Sales"
data = Reference(ws, min_col=2, min_row=1, max_row=10)
chart.add_data(data)
ws.add_chart(chart, "E1")
```

### 技巧 7：合併儲存格

```python
ws.merge_cells('A1:D1')  # 合併 A1 到 D1
cell = ws['A1']
cell.value = 'Merged'
cell.alignment = Alignment(horizontal='center', vertical='center')
```

### 技巧 8：資料驗證

```python
from openpyxl.worksheet.datavalidation import DataValidation

dv = DataValidation(type='list', formula1='"選項1,選項2,選項3"')
dv.error = '請選擇有效的選項'
ws.add_data_validation(dv)
dv.add('A1:A100')
```

### 技巧 9：工作表保護

```python
ws.protection.sheet = True
ws.protection.password = 'password123'
ws.protection.enable()
```

### 技巧 10：超連結

```python
ws['A1'].value = 'Click Here'
ws['A1'].hyperlink = 'https://example.com'
# 或工作表內部超連結
ws['A1'].hyperlink = '#Sheet2!A1'
```

---

## 案例對照表

| 需求 | 推薦案例 | 執行命令 |
|-----|--------|--------|
| 基礎報表 | Case 1 | `python case01_styled_monthly_report.py` |
| 多工作表 | Case 2 | `python case02_multi_sheet_consolidation.py` |
| 條件格式 | Case 3 | `python case03_conditional_formatting.py` |
| 圖表製作 | Case 4 | `python case04_dynamic_chart_generation.py` |
| 公式應用 | Case 5 | `python case05_formula_injection.py` |
| 報表模板 | Case 6 | `python case06_template_based_reports.py` |
| 資料驗證 | Case 7 | `python case07_data_validation.py` |
| KPI 儀表板 | Case 8 | `python case08_executive_summary.py` |
| 複雜佈局 | Case 9 | `python case09_cell_merging.py` |
| 安全保護 | Case 10 | `python case10_sheet_protection.py` |
| 互動性增強 | Case 11 | `python case11_hyperlinks_comments.py` |
| 圖片整合 | Case 12 | `python case12_image_insertion.py` |
| 自動化系統 | Case 13 | `python case13_full_automation_system.py` |
| 完整集成 | Case 14 | `python case14_pandas_excel_integration.py` |

---

## 常用代碼片段

### 从 DataFrame 寫入 Excel

```python
import pandas as pd

df = pd.read_csv('data.csv')

# 方法 1：使用 pandas（簡單）
df.to_excel('output.xlsx', index=False)

# 方法 2：使用 openpyxl（進階）
from openpyxl import Workbook
from openpyxl.utils.dataframe import dataframe_to_rows

wb = Workbook()
ws = wb.active

for r_idx, row in enumerate(dataframe_to_rows(df, index=False, header=True), 1):
    for c_idx, value in enumerate(row, 1):
        ws.cell(row=r_idx, column=c_idx, value=value)

wb.save('output.xlsx')
```

### 批量格式化

```python
from openpyxl.styles import Border, Side

thin_border = Border(
    left=Side(style='thin'),
    right=Side(style='thin'),
    top=Side(style='thin'),
    bottom=Side(style='thin')
)

for row in ws.iter_rows(min_row=1, max_row=100, min_col=1, max_col=5):
    for cell in row:
        cell.border = thin_border
```

### 條件式格式化

```python
from openpyxl.formatting.rule import CellIsRule
from openpyxl.styles import PatternFill

# 大於 100 則綠色
green_fill = PatternFill(start_color='C6EFCE', fill_type='solid')
rule = CellIsRule(operator='greaterThan', formula=['100'], fill=green_fill)
ws.conditional_formatting.add('A1:A100', rule)
```

---

## 常見錯誤和解決方案

### 錯誤 1：Module not found

```
ModuleNotFoundError: No module named 'pandas'
```

**解決：**
```bash
pip install pandas openpyxl
```

### 錯誤 2：路徑不存在

```
FileNotFoundError: [Errno 2] No such file or directory
```

**解決：**
```bash
# 確保在正確的目錄
pwd
cd /home/justin/web-projects/excel-python-data-analysis/week07-08_openpyxl-mastery
```

### 錯誤 3：無法保存檔案

```
PermissionError: [Errno 13] Permission denied
```

**解決：**
```bash
# 檢查目錄權限
ls -ld .
# 確保有寫入權限
chmod 755 .
```

### 錯誤 4：圖表無法添加

```
Exception: Cannot add chart to worksheet
```

**解決：**
- 確保圖表有資料
- 檢查資料範圍是否正確
- 確認 openpyxl 版本 >= 3.0

---

## 性能提示

### 處理大型資料集

```python
# ✅ 高效：使用 write_only 模式
wb = Workbook(write_only=True)

# ❌ 低效：直接操作大量儲存格
for i in range(100000):
    ws.cell(row=i, column=1, value=i)
```

### 優化記憶體使用

```python
# 使用適當的 dtype
df = pd.read_csv('data.csv', dtype={'id': 'int32', 'price': 'float32'})

# 只讀取需要的欄位
df = pd.read_csv('data.csv', usecols=['col1', 'col2'])

# 分批處理
for chunk in pd.read_csv('data.csv', chunksize=10000):
    # 處理每個批次
    pass
```

---

## 進階主題預覽

### VBA 巨集整合
```python
# openpyxl 可以保留 VBA，但不能執行
# 如需執行，需要配合 Xlwings
```

### 條件格式高級用法
```python
from openpyxl.formatting.rule import DataBarRule, ColorScaleRule

# 資料條
rule = DataBarRule(start_type='min', end_type='max', color='FF0070C0')

# 色階
rule = ColorScaleRule(
    start_type='min', start_color='FFF8696B',
    end_type='max', end_color='FF63BE7B'
)
```

### 樞紐表（使用 Pandas）
```python
import pandas as pd

df = pd.read_csv('data.csv')
pivot = df.pivot_table(index='A', columns='B', values='C', aggfunc='sum')
pivot.to_excel('pivot.xlsx')
```

---

## 在線資源

### 官方文檔
- [openpyxl 文檔](https://openpyxl.readthedocs.io/)
- [Pandas 文檔](https://pandas.pydata.org/)

### 相關教程
- Excel 函數指南
- VBA 教程
- Pandas 最佳實踐

---

## 後續步驟

1. **執行所有 14 個案例**
   ```bash
   bash run_all_cases.sh
   ```

2. **深入學習特定案例**
   ```bash
   python case01_styled_monthly_report.py
   # 然後查看生成的 Excel 檔案
   ```

3. **修改代碼進行實驗**
   - 改變顏色方案
   - 添加新的公式
   - 創建自己的圖表

4. **應用到實際項目**
   - 使用自己的資料
   - 自訂報表格式
   - 自動化工作流程

---

## 支持和幫助

### 如果卡住了

1. **檢查文檔**
   - 查看 README.md 完整說明
   - 查看 EXECUTION_GUIDE.md 執行指南

2. **查看案例代碼**
   - 查找類似的案例
   - 參考其中的實現方式

3. **測試環境**
   ```bash
   python -c "import pandas, openpyxl; print('OK')"
   ```

4. **查看日誌輸出**
   - 運行時會打印詳細訊息
   - 關注錯誤提示

---

## 現在就開始！

```bash
# 第 1 步：進入目錄
cd /home/justin/web-projects/excel-python-data-analysis/week07-08_openpyxl-mastery

# 第 2 步：執行第一個案例
python case01_styled_monthly_report.py

# 第 3 步：打開生成的 Excel 檔案
# 使用 Excel、LibreOffice 或 Google Sheets 打開 case01_monthly_report.xlsx

# 第 4 步：學習代碼並進行實驗
# 修改代碼並重新執行，看看會發生什麼

# 第 5 步：探索其他案例
python case02_multi_sheet_consolidation.py
# ...以此類推
```

---

**祝您學習愉快！** 🚀

**版本：** 1.0
**最後更新：** 2024-12-11
