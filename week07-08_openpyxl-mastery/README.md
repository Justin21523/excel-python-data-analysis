# Week 7-8: openpyxl 完全掌握

## 概述
本目錄包含 14 個完整的 Python 實作案例，深入講解 openpyxl 庫的各種功能和應用場景。

## 環境需求
```bash
pip install pandas openpyxl matplotlib numpy
```

## 案例列表

### Case 1: 格式化月報自動生成
**檔案:** `case01_styled_monthly_report.py`

**功能:**
- 讀取 pandas DataFrame
- 寫入 Excel 並自動格式化
- 標題列：粗體、藍底白字、置中
- 數值格式：千分位、小數位、百分比
- 自動調整欄寬
- 凍結窗格

**輸出:** `case01_monthly_report.xlsx`

**執行方式:**
```bash
python case01_styled_monthly_report.py
```

---

### Case 2: 多工作表自動整合
**檔案:** `case02_multi_sheet_consolidation.py`

**功能:**
- 多個 DataFrame 寫入不同工作表
- 每個工作表自動格式化
- 建立目錄頁（超連結）
- 工作表標籤顏色管理

**輸出:** `case02_multi_sheet_report.xlsx`

**執行方式:**
```bash
python case02_multi_sheet_consolidation.py
```

---

### Case 3: 條件格式自動化
**檔案:** `case03_conditional_formatting.py`

**功能:**
- 業績達標：綠色
- 未達標：紅色
- 接近目標：黃色
- 資料條 (Data Bar)
- 色階 (Color Scale)
- 圖示集 (Icon Set)

**輸出:** `case03_conditional_formatting.xlsx`

**執行方式:**
```bash
python case03_conditional_formatting.py
```

---

### Case 4: 動態圖表生成
**檔案:** `case04_dynamic_chart_generation.py`

**功能:**
- 長條圖：產品銷售排名
- 折線圖：銷售趨勢
- 圓餅圖：類別佔比
- 組合圖：雙軸圖表

**輸出:** `case04_dynamic_charts.xlsx`

**執行方式:**
```bash
python case04_dynamic_chart_generation.py
```

---

### Case 5: 公式注入
**檔案:** `case05_formula_injection.py`

**功能:**
- 動態公式計算
- SUM、AVERAGE、COUNT 函數
- IF 條件判斷
- 公式自動複製

**輸出:** `case05_formula_injection.xlsx`

**執行方式:**
```bash
python case05_formula_injection.py
```

---

### Case 6: 模板化報表
**檔案:** `case06_template_based_reports.py`

**功能:**
- 定義報表模板
- 動態填充資料
- 保持格式一致
- 可複用設計
- 批量生成報告

**輸出:** `case06_template_reports.xlsx`

**執行方式:**
```bash
python case06_template_based_reports.py
```

---

### Case 7: 資料驗證
**檔案:** `case07_data_validation.py`

**功能:**
- 下拉列表驗證
- 數值範圍驗證
- 日期範圍驗證
- 自訂驗證公式
- 錯誤提示設定

**輸出:** `case07_data_validation.xlsx`

**執行方式:**
```bash
python case07_data_validation.py
```

---

### Case 8: 執行摘要（高級報表）
**檔案:** `case08_executive_summary.py`

**功能:**
- KPI 關鍵指標儀表板
- 視覺化重點指標
- 多色彩突出效果
- 趨勢對比分析
- 管理層報告設計

**輸出:** `case08_executive_summary.xlsx`

**執行方式:**
```bash
python case08_executive_summary.py
```

---

### Case 9: 儲存格合併
**檔案:** `case09_cell_merging.py`

**功能:**
- 合併儲存格實作
- 多層級標題
- 複雜表格佈局
- 分組統計區域
- 對齐和邊框處理

**輸出:** `case09_cell_merging.xlsx`

**執行方式:**
```bash
python case09_cell_merging.py
```

---

### Case 10: 工作表保護
**檔案:** `case10_sheet_protection.py`

**功能:**
- 工作表密碼保護
- 凍結保護
- 指定可編輯區域
- 保護設定配置
- 列印範圍限制

**輸出:** `case10_sheet_protection.xlsx`

**執行方式:**
```bash
python case10_sheet_protection.py
```

密碼：`password123`

---

### Case 11: 超連結和註解
**檔案:** `case11_hyperlinks_comments.py`

**功能:**
- 工作表間超連結
- 外部超連結
- 儲存格註解
- 註解格式化
- 導航目錄

**輸出:** `case11_hyperlinks_comments.xlsx`

**執行方式:**
```bash
python case11_hyperlinks_comments.py
```

---

### Case 12: 圖片插入
**檔案:** `case12_image_insertion.py`

**功能:**
- 插入本地圖片
- 圖片大小調整
- 圖片位置設定
- 背景圖片設定
- 圖表圖片導出

**輸出:** `case12_image_insertion.xlsx`, `sample_chart.png`

**執行方式:**
```bash
python case12_image_insertion.py
```

---

### Case 13: 完整自動化系統
**檔案:** `case13_full_automation_system.py`

**功能:**
- 批量報表生成
- 動態工作表創建
- 多層級驗證
- 自動編號系統
- 批量樣式應用
- 日誌記錄

**輸出:** `case13_full_automation_system.xlsx`

**執行方式:**
```bash
python case13_full_automation_system.py
```

---

### Case 14: Pandas 和 Excel 完整整合
**檔案:** `case14_pandas_excel_integration.py`

**功能:**
- DataFrame 直接寫入 Excel
- 範圍格式化應用
- 樞紐表資料轉換
- 高效資料轉換
- 批量資料處理
- 完整工作流程整合

**輸出:** `case14_pandas_excel_integration.xlsx`

**執行方式:**
```bash
python case14_pandas_excel_integration.py
```

---

## 快速開始

### 安裝依賴
```bash
pip install pandas openpyxl matplotlib numpy
```

### 執行所有案例
```bash
# 逐個執行
python case01_styled_monthly_report.py
python case02_multi_sheet_consolidation.py
python case03_conditional_formatting.py
# ... 以此類推

# 或建立批量執行腳本
bash run_all_cases.sh
```

---

## 主要 openpyxl 功能速查

| 功能 | 案例 | 關鍵代碼 |
|-----|------|--------|
| 基礎寫入 | Case 1, 2 | `ws.cell()`, `ws['A1']` |
| 樣式設定 | Case 1, 6 | `Font()`, `PatternFill()`, `Alignment()` |
| 條件格式 | Case 3 | `DataBarRule()`, `ColorScaleRule()` |
| 圖表 | Case 4 | `BarChart()`, `Reference()` |
| 公式 | Case 5 | `cell.value = '=SUM(...)'` |
| 資料驗證 | Case 7 | `DataValidation()` |
| 保護 | Case 10 | `SheetProtection()` |
| 超連結 | Case 11 | `cell.hyperlink` |
| 註解 | Case 11 | `cell.comment = Comment()` |
| 圖片 | Case 12 | `Image()`, `ws.add_image()` |
| 自動化 | Case 13, 14 | 類別設計, 批量操作 |

---

## 資料來源

所有案例使用 Olist 巴西電商平台真實資料集：
- 訂單數：99,441
- 訂單明細數：112,650
- 商品數：32,951
- 客戶數：99,441

資料位置：`/mnt/data/datasets/ecommerce/kaggle/olist/`

---

## 進階提示

### 效能優化
```python
# 使用生成器讀取大型 DataFrame
for batch in pd.read_csv('file.csv', chunksize=10000):
    # 處理每個批次
    pass

# 預分配列寬
ws.column_dimensions['A'].width = 20
```

### 記憶體優化
```python
# 使用適當的 dtype
df = pd.read_csv('file.csv', dtype={'id': 'int32', 'price': 'float32'})
```

### 常見問題

**Q: 如何處理大型 Excel 檔案？**
A: 使用 `write_only=True` 模式（需要重新計算公式）或分割資料。

**Q: 如何保留公式而不是計算結果？**
A: `cell.value = '=SUM(...)'` 不要使用 `=` 前綴之外的方式。

**Q: 如何在保護的工作表中編輯特定儲存格？**
A: 先 `unlocked = False` 解鎖儲存格，然後啟用保護。

---

## 學習路線

推薦按以下順序學習：

1. **基礎** → Case 1, 2
2. **樣式** → Case 3, 8, 9
3. **資料操作** → Case 4, 5, 7
4. **高級功能** → Case 6, 10, 11, 12
5. **自動化** → Case 13, 14

---

## 貢獻指南

如果您想添加新案例或改進現有案例，請遵循以下結構：

```python
"""
案例N：功能描述
功能：
- 項目1
- 項目2
- 項目N

Author: Week 7-8 openpyxl 完全掌握
Date: 2024-12-11
"""

# 導入
import pandas as pd
from openpyxl import Workbook
# ...

def main():
    """主函數"""
    # 第1步：載入資料
    # 第2步：準備資料
    # 第3步：建立工作簿
    # 第4步：應用格式
    # 第5步：保存檔案
    pass

if __name__ == "__main__":
    main()
```

---

## 參考資源

- [openpyxl 官方文檔](https://openpyxl.readthedocs.io/)
- [Pandas 官方文檔](https://pandas.pydata.org/)
- [Excel 條件格式指南](https://support.microsoft.com/en-us/office/apply-conditional-formatting-to-cells-in-a-spreadsheet-d3ad63ca-7f3d-4f19-a7b5-1e4aa60a3a20)

---

**最後更新:** 2024-12-11
**版本:** 1.0
