# Week 03: MultiIndex & GroupBy & Pivot - 完整教學指南

## 課程完成狀態

已成功創建 **Week 3 的 Day 02-04 完整教學指南**，共 3 個檔案，總計 **2,759 行**，約 **83 KB**。

---

## 文件清單

### Day 02: GroupBy 進階聚合 - 完全掌握分組運算
**檔案位置：** `/home/justin/web-projects/excel-python-data-analysis/week03-06_pandas-advanced/week03_multiindex_groupby/Day02_GroupBy_Advanced_Guide.md`

**文件大小：** 27 KB (803 行)

**課程內容：**
- **Part 1: GroupBy 基礎回顧（1h）** - 3 個案例
  - 案例 1: 單欄位分組 - 州別銷售額
  - 案例 2: 多欄位分組 - 州市組合分析
  - 案例 3: 多欄位 + 多欄值 - 產品類別×支付方式

- **Part 2: 命名聚合（Named Aggregation）（2h）** - 5 個案例
  - 案例 4: 產品類別銷售分析
  - 案例 5: 支付方式分析
  - 案例 6: 客戶分群分析
  - 案例 7: 時間維度分析
  - 案例 8: 多維度綜合分析

- **Part 3: Transform vs Aggregate vs Filter（2h）** - 6 個案例
  - 案例 9: 計算組內百分比排名
  - 案例 10: 計算組內標準化分數
  - 案例 11: Transform 廣播聚合結果
  - 案例 12: 篩選出熱銷產品
  - 案例 13: 篩選出活躍客戶
  - 案例 14: 篩選出 Top 類別

- **Part 4: 綜合實戰練習（3h）** - 3 個實踐項目
  - 練習 1: RFM 客戶價值分析
  - 練習 2: 產品 ABC 分類
  - 練習 3: 客戶分群報表

**特點：**
- 14 個完整的 Olist 真實資料案例
- Excel 與 pandas 對照
- 命名聚合的最佳實踐
- Transform/Aggregate/Filter 深度對比
- 詳細的代碼註釋

---

### Day 03: Pivot 與資料重塑 - 樞紐分析與形狀轉換
**檔案位置：** `/home/justin/web-projects/excel-python-data-analysis/week03-06_pandas-advanced/week03_multiindex_groupby/Day03_Pivot_Reshape_Guide.md`

**文件大小：** 29 KB (1,123 行)

**課程內容：**
- **Part 1: pivot_table 完全掌握（2h）** - 10 個案例
  - 案例 1: 簡單透視表 - 類別×支付方式
  - 案例 2: 二維透視表 - 類別×支付方式
  - 案例 3: 多值透視表
  - 案例 4: 使用 margins 計算總計
  - 案例 5: 複雜多維透視表
  - 案例 6: 多聚合函數透視表
  - 案例 7: 自訂聚合函數
  - 案例 8: 時間維度透視表
  - 案例 9: 排名與占比
  - 案例 10: 透視表轉為 DataFrame

- **Part 2: stack / unstack 深度理解（2h）** - 8 個案例
  - 案例 11: 基本 Stack 操作
  - 案例 12: 多層級 Stack
  - 案例 13: Stack 在資料重塑中的應用
  - 案例 14: 基本 Unstack 操作
  - 案例 15: 多層 Unstack
  - 案例 16: Fill Value 與缺失值處理
  - 案例 17: 轉換與合併多個透視表
  - 案例 18: 索引與欄位互換

- **Part 3: melt 寬表變長表（2h）** - 7 個案例
  - 案例 19: 簡單 Melt
  - 案例 20: 多 ID 欄位 Melt
  - 案例 21: 部分欄位 Melt
  - 案例 22: 多層級欄位名 Melt
  - 案例 23: Melt 後的資料聚合
  - 案例 24: 時間序列 Melt
  - 案例 25: Melt vs Stack 效果對比

- **Part 4: 綜合實戰練習（3h）** - 3 個實踐項目
  - 練習 1: 建立月度銷售透視表
  - 練習 2: 地區 × 類別交叉分析
  - 練習 3: 動態報表生成系統

**特點：**
- 25 個完整的 Olist 實資案例
- pivot_table、stack、unstack、melt 的全面覆蓋
- 多層級索引的深度理解
- 寬表與長表的互相轉換
- Excel Power Query 對照

---

### Day 04: 綜合實踐 - Olist 多維度分析系統
**檔案位置：** `/home/justin/web-projects/excel-python-data-analysis/week03-06_pandas-advanced/week03_multiindex_groupby/Day04_Practice_Integration.md`

**文件大小：** 27 KB (833 行)

**課程內容：**
- **Step 1: 資料載入與預處理（30min）**
  - 載入多個資料表
  - 資料清洗與驗證
  - 建立聯合資料集

- **Step 2: 建立 MultiIndex 結構（45min）**
  - 四維度基礎指標計算
  - 建立四層級 MultiIndex
  - 索引切片與查詢

- **Step 3: 計算各維度 KPI（1h）**
  - 時間維度 KPI（月度、季度、年度）
  - 地區維度 KPI（州別、城市）
  - 產品維度 KPI（類別、ABC 分類）
  - 綜合維度 KPI（多維交叉）

- **Step 4: 生成透視表報表（1h）**
  - 報表 1: 月度類別表現（MoM 成長率）
  - 報表 2: 地區類別矩陣（熱力圖資料）
  - 報表 3: Top 產品排行（動態排名）

- **Step 5: 格式化與輸出（45min）**
  - 建立綜合報表資料結構
  - 數據格式化與驗證
  - 匯出到 Excel
  - 生成執行摘要

**特點：**
- 完整的專案結構（5 個步驟）
- Day 1-3 技能的全面整合
- 實際的商業分析場景
- 自動化報表生成
- 評估標準與進階擴展方向

---

## 課程統計

| 指標 | 數值 |
|------|------|
| **總文件數** | 3 |
| **總行數** | 2,759 |
| **總大小** | 83 KB |
| **案例數量** | 25+ |
| **代碼塊** | 100+ |
| **使用資料** | Olist 真實數據 |
| **學習時間** | ~12 小時 |

---

## 課程重點內容

### Part 1: GroupBy 進階技巧
- **命名聚合（Named Aggregation）** - 提高代碼可讀性的最佳實踐
- **Transform 廣播** - 保持原始行數，計算組內指標
- **Filter 篩選** - 按組條件篩選，保留原始行
- **派生指標計算** - 回購率、客單價、占比等

### Part 2: Pivot Table 與資料重塑
- **pivot_table 完全掌握** - 多層級索引、多值聚合、margins 總計
- **Stack/Unstack** - 寬表與長表的互相轉換
- **Melt 操作** - 部分欄位轉換、多層級處理
- **性能優化** - 大規模透視表的處理

### Part 3: 多維度分析系統
- **MultiIndex 建立** - 四維度分析結構
- **KPI 計算體系** - 銷售額、訂單數、客戶數、成長率
- **報表自動生成** - 透視表、增長率、占比
- **Excel 匯出** - 多 Sheet 結構化輸出

---

## 適用對象

- 已完成 Day 01 MultiIndex 學習的學生
- 需要進行多維度數據分析的商務分析師
- 想要自動化報表生成的數據分析師
- 需要從 Excel 遷移到 Python 的用戶

---

## 必備環境

- Python 3.8+
- pandas 1.3.0+
- numpy 1.20.0+
- openpyxl 3.0+（用於 Excel 匯出）

```bash
pip install pandas>=1.3.0 numpy>=1.20.0 openpyxl>=3.0.0
```

---

## 快速導航

### 按學習順序
1. Day 02: GroupBy 進階聚合
2. Day 03: Pivot 與資料重塑
3. Day 04: 綜合實踐

### 按技術主題
- **聚合運算** → Day 02 Part 1-2
- **資料轉換** → Day 03 Part 1-3
- **實戰應用** → Day 04 全部

### 按難度等級
- **基礎** → Day 02 Part 1, Day 03 Part 1
- **進階** → Day 02 Part 2-3, Day 03 Part 2-3
- **精通** → Day 04 全部

---

## 學習成果評估

完成本課程後，您應該能夠：

- [ ] 使用命名聚合提高代碼可讀性
- [ ] 掌握 Transform、Aggregate、Filter 三者區別
- [ ] 建立複雜多層級的 pivot_table
- [ ] 熟練使用 stack/unstack/melt 進行資料轉換
- [ ] 建立和維護 MultiIndex 結構
- [ ] 計算各維度的關鍵 KPI（成長率、占比等）
- [ ] 自動生成結構化的 Excel 報表
- [ ] 使用 pandas 解決實際的商業分析問題

---

## 相關資源

### 官方文檔
- [pandas GroupBy Documentation](https://pandas.pydata.org/docs/user_guide/groupby.html)
- [pandas Pivot Tables](https://pandas.pydata.org/docs/user_guide/reshaping.html)
- [pandas MultiIndex](https://pandas.pydata.org/docs/user_guide/advanced.html)

### 延伸閱讀
- Day 01: MultiIndex Complete Guide
- Week 04: 時間序列與窗口函數
- Week 05: Apply、Transform、Aggregate 深度探討

---

## 常見問題解答

**Q: 這三個檔案的學習順序是否必須？**
A: 建議按 Day 02 → 03 → 04 的順序，但如果已熟悉基礎 GroupBy，可先看 Day 03-04。

**Q: 代碼是否可以直接運行？**
A: 可以！所有代碼都基於 Olist 資料集，但需要正確的資料載入器設置。

**Q: 這些文件與 Day 01 的關係？**
A: Day 02-04 延續 Day 01 的內容，Day 04 整合所有技能進行專案實戰。

**Q: 是否包含習題答案？**
A: 習題及答案位於 `exercises/` 目錄下的專門檔案中。

---

**版本信息：**
- 更新日期：2024年12月11日
- 課程狀態：完成
- 質量等級：高級（Advanced）
- 適用版本：pandas 1.3.0+

---

## 後續學習路徑

完成 Week 03 後，建議進行：
1. Week 04: 時間序列與窗口函數（rolling, expanding）
2. Week 05: Apply、Transform、Aggregate 深度探討
3. Week 06: 性能優化與大規模資料處理
4. Week 12-14: 商業分析實戰項目
