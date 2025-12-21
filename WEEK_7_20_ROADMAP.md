# 📚 Week 7-20 完整學習路線圖

**規劃日期：** 2024-12-11
**總時數：** 280-320 小時
**總週數：** 14 週

---

## 🎯 整體架構

### 已完成（Week 1-6）✅
- Week 1-2: Excel 進階（20-25h）
- Week 3: MultiIndex & GroupBy（25-30h）
- Week 4: 時間序列 & 視窗函數（24h）
- Week 5: Apply/Transform/Agg（34-42h）
- Week 6: 效能優化 & Merge（28-35h）

**小計：** 131-156 小時

### 待創建（Week 7-20）⏳
- **Phase 3:** Week 7-8 openpyxl 完全掌握（40h）
- **Phase 4:** Week 9-11 自動化工作流程（60h）
- **Phase 5:** Week 12-14 商業分析模型（60h）
- **Phase 6:** Week 15-20 五大 Capstone 專案（120h）

**小計：** 280 小時

**總計：** 411-436 小時（約 4.5-5 個月密集學習）

---

## 📋 Phase 3: openpyxl 完全掌握（Week 7-8）

### Week 7: 格式化與樣式自動化（20h）

**學習目標：**
- 掌握 openpyxl 完整 API
- 生成「看起來像手工製作」的精美 Excel
- 自動化報表格式設定

**案例清單（8 個案例）：**

#### Case 1: 格式化月報自動生成（2.5h）
```python
# 功能：
- 讀取 pandas DataFrame
- 寫入 Excel 並自動格式化
- 標題列：粗體、藍底白字、置中
- 數值格式：千分位、小數位、百分比
- 自動調整欄寬
- 凍結窗格
```

**產出：** `case01_styled_monthly_report.py`（150 lines）

---

#### Case 2: 多工作表自動整合（2.5h）
```python
# 功能：
- 多個 DataFrame 寫入不同工作表
- 每個工作表自動格式化
- 建立目錄頁（超連結）
- 工作表標籤顏色管理
```

**產出：** `case02_multi_sheet_consolidation.py`（180 lines）

---

#### Case 3: 條件格式自動化（2.5h）
```python
# 功能：
- 業績達標：綠色
- 未達標：紅色
- 接近目標：黃色
- 資料條 (Data Bar)
- 色階 (Color Scale)
- 圖示集 (Icon Set)
```

**產出：** `case03_conditional_formatting.py`（200 lines）

---

#### Case 4: 動態圖表生成（3h）
```python
# 功能：
- 長條圖：產品銷售排名
- 折線圖：銷售趨勢
- 圓餅圖：類別佔比
- 組合圖：雙軸圖表（銷售額 + 成長率）
- 圖表標題、圖例、資料標籤
```

**產出：** `case04_dynamic_chart_generation.py`（250 lines）

---

#### Case 5: 公式自動插入（2.5h）
```python
# 功能：
- SUM、AVERAGE 公式
- VLOOKUP 公式
- 相對位址與絕對位址控制
- 公式拖曳複製
```

**產出：** `case05_formula_injection.py`（150 lines）

---

#### Case 6: 範本式報表（3h）
```python
# 功能：
- 讀取範本 Excel → 填入資料 → 保留格式
- 保留原有樣式
- 動態擴充資料範圍
- 圖表自動更新資料來源
```

**產出：** `case06_template_based_reports.py`（220 lines）

---

#### Case 7: 資料驗證規則（2h）
```python
# 功能：
- 下拉選單
- 數值範圍限制
- 日期範圍限制
- 自訂錯誤訊息
```

**產出：** `case07_data_validation.py`（120 lines）

---

#### Case 8: 高階主管摘要報表（2h）
```python
# 功能：
- 首頁：關鍵 KPI（大字體、配色）
- 趨勢圖表頁
- 明細資料頁
- 自動產生目錄與超連結
```

**產出：** `case08_executive_summary.py`（280 lines）

---

### Week 8: 進階技巧與整合（20h）

**案例清單（6 個進階案例）：**

#### Case 9: 儲存格合併與分割（2h）
```python
# 功能：
- merge_cells 合併儲存格
- 複雜表頭設計
- 分組小計合併
```

**產出：** `case09_cell_merging.py`（100 lines）

---

#### Case 10: 保護工作表與密碼（2h）
```python
# 功能：
- 工作表保護
- 部分儲存格可編輯
- 密碼設定
```

**產出：** `case10_sheet_protection.py`（80 lines）

---

#### Case 11: 超連結與註釋（2h）
```python
# 功能：
- 儲存格超連結（外部 URL、內部工作表）
- 儲存格註釋（Comment）
- 批次處理
```

**產出：** `case11_hyperlinks_comments.py`（120 lines）

---

#### Case 12: 圖片插入與調整（2.5h）
```python
# 功能：
- 插入圖片（Logo、產品圖）
- 圖片大小調整
- 圖片定位
```

**產出：** `case12_image_insertion.py`（100 lines）

---

#### Case 13: 完整自動化報表系統（5.5h）
```python
# 功能：
- 整合 Week 7-8 所有技能
- 從髒資料 → 清洗 → 分析 → 格式化報表
- 一鍵生成多份不同報表
```

**產出：** `case13_full_automation_system.py`（400 lines）

---

#### Case 14: Excel 與 pandas 無縫整合（6h）
```python
# 功能：
- pandas → Excel（保留格式）
- Excel → pandas（讀取格式資訊）
- 雙向同步
- 範本更新自動化
```

**產出：** `case14_pandas_excel_integration.py`（350 lines）

---

**Week 7-8 總計：**
- 14 個完整案例
- 2,300+ 行代碼
- 40 小時學習時間
- 所有代碼可重複使用

---

## 📋 Phase 4: 自動化工作流程（Week 9-11）

### Week 9: ETL Pipeline 設計（20h）

#### Case 1: 每日訂單 ETL（5h）
```python
# 流程：
1. 從資料夾讀取新訂單檔案（多格式：xlsx, csv）
2. 資料驗證（必填欄位、格式檢查）
3. 清洗轉換
4. 寫入資料庫/資料倉儲
5. 產生日報

# 技巧：
- pathlib 檔案管理
- 異常處理
- 資料驗證
```

**產出：** `case01_daily_orders_etl.py`（500 lines）

---

#### Case 2: 多來源資料整合（5h）
```python
# 情境：
整合「線上訂單、線下門市、電話訂購」三來源

# 挑戰：
- 欄位名稱不一致
- 缺失值處理策略不同
- 時區轉換
- 重複訂單識別

# 產出：
統一格式的完整訂單表
```

**產出：** `case02_multi_source_consolidation.py`（600 lines）

---

#### Case 3: 增量更新 vs 全量更新（4h）
```python
# 功能：
- 識別新增/修改/刪除記錄
- 增量更新策略
- 版本控制
- 歷史資料保存
```

**產出：** `case03_incremental_updates.py`（400 lines）

---

#### Case 4: 錯誤處理與恢復（3h）
```python
# 功能：
- try-except 精細化處理
- 錯誤訊息記錄
- 發生錯誤時的恢復策略
- 斷點續傳
```

**產出：** `case04_error_recovery.py`（300 lines）

---

#### Case 5: 完整日誌系統（3h）
```python
# 功能：
- 不同等級日誌（DEBUG、INFO、WARNING、ERROR）
- 同時輸出到檔案與 console
- 日誌輪替（避免檔案過大）
- 每日執行摘要
```

**產出：** `case05_logging_system.py`（250 lines）

---

### Week 10: 資料品質與監控（20h）

#### Case 6: 資料品質自動檢查（5h）
```python
# 功能：
- 檢查缺失率
- 檢查重複率
- 檢查異常值（3σ 法則）
- 檢查格式正確性
- 產生品質報告
```

**產出：** `case06_data_quality_checks.py`（450 lines）

---

#### Case 7: 資料驗證規則引擎（5h）
```python
# 功能：
- 可設定的驗證規則
- YAML 配置檔
- 批次驗證
- 詳細錯誤報告
```

**產出：** `case07_validation_engine.py`（500 lines）

---

#### Case 8: 效能監控系統（4h）
```python
# 功能：
- 執行時間追蹤
- 記憶體使用監控
- 瓶頸識別
- 效能報告生成
```

**產出：** `case08_performance_monitoring.py`（350 lines）

---

#### Case 9: Email 通知機制（3h）
```python
# 功能：
- 成功/失敗 Email 通知
- 附件寄送（報表）
- HTML 格式化 Email
- 多收件者管理
```

**產出：** `case09_email_notifications.py`（280 lines）

---

#### Case 10: Slack/Teams 整合（3h）
```python
# 功能：
- Webhook 通知
- 結果摘要推送
- 異常警報
```

**產出：** `case10_slack_integration.py`（200 lines）

---

### Week 11: 排程與部署（20h）

#### Case 11: 排程執行（6h）
```python
# 工具：
- schedule 套件（Python 內）
- cron (Linux)
- Task Scheduler (Windows)

# 功能：
- 每日定時執行
- 每週/每月執行
- 條件觸發執行
```

**產出：** `case11_scheduling.py`（300 lines）

---

#### Case 12: 配置管理（4h）
```python
# 功能：
- YAML/JSON 配置檔
- 環境變數管理
- 敏感資訊加密
- 多環境配置（dev/staging/prod）
```

**產出：** `case12_config_management.py`（250 lines）

---

#### Case 13: 容器化部署（5h）
```python
# 功能：
- Dockerfile 撰寫
- docker-compose 設定
- 環境一致性
```

**產出：** `Dockerfile`, `docker-compose.yml`

---

#### Case 14: 端到端 Pipeline（5h）
```python
# 整合 Week 9-11 所有功能：
1. 排程執行（每天早上 8:00）
2. 讀取多來源資料
3. 資料品質檢查
4. 清洗轉換
5. 分析計算
6. 產生 Excel 報表
7. Email 通知
8. 日誌記錄
9. 錯誤處理
```

**產出：** `case14_end_to_end_pipeline.py`（800 lines）

---

**Week 9-11 總計：**
- 14 個完整系統
- 5,180+ 行代碼
- 60 小時學習時間
- 可部署的生產級系統

---

## 📋 Phase 5: 商業分析模型（Week 12-14）

### Week 12: 客戶分析（20h）

#### RFM 分析（3 個深度案例，8h）

**案例 1：基礎 RFM**（2.5h）
```python
# 計算 Recency、Frequency、Monetary
# 五等分評分
# 客戶分群（11 種標準分群）
```

**案例 2：RFM + Clustering**（3h）
```python
# RFM 作為特徵
# K-Means 分群
# 3D 視覺化
# 各群特徵描述
```

**案例 3：行動導向 RFM**（2.5h）
```python
# 為每個客戶群設計行銷策略
# 計算各群預期回報
# 產生行銷建議書
```

---

#### Cohort 留存分析（3 個案例，7h）

**案例 1：基礎留存率**（2h）
```python
# 世代定義（首購月份）
# 計算各世代留存率
# 留存熱圖視覺化
```

**案例 2：留存率 Revenue 分析**（2.5h）
```python
# 不只看留存「人數」，更看留存「營收」
# 計算各世代的 LTV
# 識別高價值世代
```

**案例 3：流失預警**（2.5h）
```python
# 識別「即將流失」的客戶
# 計算流失機率
# 產生挽回優先清單
```

---

#### CLV 計算（2 個案例，5h）

**案例 1：簡單 CLV**（2h）
```python
# CLV = 平均客單價 × 購買頻率 × 客戶壽命
# 歷史 CLV 計算
```

**案例 2：進階 CLV**（3h）
```python
# 考慮折現率
# 預測未來 CLV
# CLV / CAC 比率
```

---

### Week 13: 產品與營運分析（20h）

#### ABC 分析（2 個案例，4h）

**案例 1：庫存 ABC**（2h）
```python
# 根據銷售額將產品分成 A、B、C 類
# 帕雷托圖
# 庫存策略建議
```

**案例 2：客戶 ABC**（2h）
```python
# 根據貢獻度分類客戶
# 80/20 法則驗證
# 資源配置建議
```

---

#### 購物籃分析（2 個案例，6h）

**案例 1：關聯規則**（3h）
```python
# 使用 mlxtend 套件
# 計算 Support、Confidence、Lift
# 識別「經常一起購買」的產品組合
```

**案例 2：產品推薦**（3h）
```python
# 基於購物籃分析建立推薦系統
# 「買了 A 的人也買了 B」
# 產出推薦清單
```

---

#### 需求預測（2 個案例，6h）

**案例 1：移動平均法**（2.5h）
```python
# 簡單移動平均
# 加權移動平均
# 指數平滑
```

**案例 2：季節性預測**（3.5h）
```python
# 季節性分解
# 趨勢+季節+殘差
# 未來 3 個月預測
```

---

#### KPI 系統（3 個系統，4h）

**系統 1：銷售 KPIs**（1.5h）
```python
# 總營收、成長率、平均客單價
# 轉換率、退貨率
# 各產品/類別/地區表現
```

**系統 2：客戶 KPIs**（1.5h）
```python
# 新客數、活躍客戶數、流失率
# CAC、LTV、LTV/CAC
# 客戶滿意度追蹤
```

**系統 3：營運 KPIs**（1h）
```python
# 訂單處理時間、準時交付率
# 庫存週轉率、缺貨率
# 退貨處理時間
```

---

### Week 14: 視覺化與報告（20h）

#### 視覺化系統（6h）
```python
# matplotlib 進階技巧
# seaborn 統計圖表
# plotly 互動式圖表
# 顏色選擇與配色
```

---

#### 報告撰寫（6h）
```python
# 資料故事敘述
# 洞察提煉
# 建議提出
# 簡報製作
```

---

#### 完整分析專案（8h）
```python
# 整合 Week 12-14 所有模型
# 從原始資料 → 分析 → 報告
# 產出：完整商業分析報告
```

---

**Week 12-14 總計：**
- 18 個商業分析模型
- 60 小時學習時間
- 可直接應用於企業

---

## 📋 Phase 6: 五大 Capstone 專案（Week 15-20）

### Project 1: Sales Intelligence Dashboard（Week 15，25h）

**專案目標：**
建立即時銷售智能儀表板，提供管理層快速決策支援

**資料來源：**
- Kaggle: Brazilian E-Commerce (Olist)
- 100,000 筆訂單資料

**核心功能：**
1. 銷售總覽（今日/本週/本月/本年 vs 上期）
2. 產品分析（Top 10 熱銷、ABC 分類）
3. 地區分析（各地區銷售熱圖、排名）
4. 異常偵測（銷售額、庫存、退貨率異常）

**技術棧：**
- pandas: 資料處理與計算
- matplotlib/seaborn: 圖表視覺化
- openpyxl: 自動產生 Excel 儀表板
- logging: 執行日誌

**預期成果：**
1. Python 分析腳本（可排程執行）
2. Excel 互動式儀表板
3. 每日自動更新 PDF 報告
4. 專案文件與 README

---

### Project 2: Customer Insights System（Week 16-17，35h）

**專案目標：**
深度分析客戶行為，提供精準行銷策略

**資料來源：**
- Kaggle: Online Retail Dataset
- 500,000+ 筆交易資料

**核心功能：**
1. RFM 客戶分群（11 種分群 + 行銷建議）
2. Cohort 留存分析（熱圖 + 營收分析）
3. CLV 計算（歷史 + 預測）
4. 行為模式分析（購買頻率、時段偏好）
5. 行動建議（優先聯繫清單、預期 ROI）

**技術棧：**
- pandas: 複雜資料分析
- sklearn: K-Means 分群
- seaborn: 熱圖與統計視覺化
- openpyxl: 多工作表報表

**預期成果：**
1. Jupyter Notebook 完整分析
2. Excel 客戶分群報告
3. 行銷策略建議書（PowerPoint）
4. 可重複執行的客戶分析系統

---

### Project 3: Inventory Optimization System（Week 18，28h）

**專案目標：**
優化庫存管理，降低庫存成本，避免缺貨

**資料來源：**
- 模擬庫存與銷售資料（3 年歷史）
- 10,000+ SKU

**核心功能：**
1. ABC 分類（產品重要性分級）
2. 安全庫存計算（服務水準 95%/98%/99%）
3. 庫存週轉率分析（呆滯庫存識別）
4. 需求預測（移動平均、季節性調整）
5. 補貨建議（EOQ、再訂購點）

**技術棧：**
- pandas: 時間序列處理
- numpy: 統計計算
- matplotlib: 視覺化
- openpyxl: 補貨清單自動生成

**預期成果：**
1. 庫存優化分析報告
2. 每週自動補貨建議表
3. 庫存健康度儀表板
4. 節省成本估算

---

### Project 4: Operations Monitoring System（Week 19，28h）

**專案目標：**
監控營運效率，識別瓶頸，提升服務品質

**資料來源：**
- 訂單處理資料
- 物流配送資料
- 客服資料

**核心功能：**
1. 訂單處理分析（平均時間、瓶頸識別）
2. 配送效率分析（準時率、延遲原因）
3. 品質監控（退貨率、客訴分析）
4. 資源使用率（人力、車輛、倉儲）
5. 異常警示（Email/SMS 通知）

**技術棧：**
- pandas: 資料分析
- matplotlib: 甘特圖、時間線
- openpyxl: 每日營運報表
- smtplib: 自動寄送 Email

**預期成果：**
1. 即時營運監控儀表板
2. 每日營運簡報（自動生成）
3. 異常警示系統
4. 改善建議報告

---

### Project 5: Executive Dashboard（Week 20，34h）

**專案目標：**
整合前四個專案，建立高階主管綜合儀表板

**整合內容：**
1. 銷售總覽（Project 1）
2. 客戶健康度（Project 2）
3. 庫存狀況（Project 3）
4. 營運效率（Project 4）

**核心功能：**
1. 一頁式總覽（關鍵 KPI、紅綠燈警示）
2. 鑽取功能（點擊 KPI 查看明細）
3. 自動化更新（每日執行、異常處理）
4. 多格式輸出（Excel + PDF + PowerPoint）

**技術棧：**
- pandas: 資料整合
- openpyxl: Excel 儀表板
- python-pptx: PowerPoint 自動化
- reportlab: PDF 生成
- schedule: 排程執行

**預期成果：**
1. 整合式儀表板系統
2. 每日自動報告（Excel + PDF + PPT）
3. 完整專案文件
4. 作品集展示網站（GitHub Pages）

---

**Week 15-20 總計：**
- 5 個完整專案
- 150 小時實作時間
- 可放入作品集的高品質成果

---

## 🎯 總體時間規劃

| 階段 | 週次 | 內容 | 時數 |
|------|------|------|------|
| **Phase 1-2** | Week 1-6 | Excel + pandas 基礎進階 | 131-156h |
| **Phase 3** | Week 7-8 | openpyxl 完全掌握 | 40h |
| **Phase 4** | Week 9-11 | 自動化工作流程 | 60h |
| **Phase 5** | Week 12-14 | 商業分析模型 | 60h |
| **Phase 6** | Week 15-20 | 五大 Capstone 專案 | 150h |
| **總計** | **20 週** | **完整課程** | **441-466h** |

---

## 📅 建議學習時間表

### 密集模式（每週 20-25 小時）

| 月份 | 週次 | 內容 |
|------|------|------|
| **Month 1** | Week 1-4 | Excel + Week 3-4 pandas |
| **Month 2** | Week 5-8 | Week 5-6 pandas + openpyxl |
| **Month 3** | Week 9-12 | 自動化 + 客戶分析 |
| **Month 4** | Week 13-16 | 產品分析 + Project 1-2 |
| **Month 5** | Week 17-20 | Project 3-5 |

**總計：** 5 個月密集學習

---

### 標準模式（每週 12-15 小時）

| 月份 | 週次 | 內容 |
|------|------|------|
| **Month 1-2** | Week 1-6 | Excel + pandas 基礎進階 |
| **Month 3** | Week 7-8 | openpyxl |
| **Month 4** | Week 9-11 | 自動化 |
| **Month 5** | Week 12-14 | 商業分析 |
| **Month 6-7** | Week 15-20 | Capstone 專案 |

**總計：** 7 個月標準學習

---

## 🚀 下一步行動

### 立即開始（Week 1-6 已完成）✅

你已經完成了基礎部分，現在可以：

1. **複習鞏固 Week 3-6**
   - 完成所有 138 道練習題
   - 重新實作 4 個整合專案

2. **準備進入 Week 7-8**
   - 安裝 openpyxl: `pip install openpyxl`
   - 準備範本 Excel 檔案
   - 複習 Excel 基礎操作

3. **規劃個人時間表**
   - 決定密集模式或標準模式
   - 設定每週學習目標
   - 建立進度追蹤表

---

## 💡 學習建議

### 如何高效學習

1. **按順序學習** - 不要跳過，每個階段都很重要
2. **實作為主** - 80% 時間寫代碼，20% 時間看教學
3. **建立筆記** - 記錄常用代碼片段
4. **定期複習** - 每完成一個 Phase 就回顧一次
5. **應用到工作** - 嘗試用學到的技能解決實際問題

### 如何驗證學習成果

- ✅ 能獨立完成所有練習題
- ✅ 能解釋代碼的每一行
- ✅ 能根據需求改寫代碼
- ✅ 能優化代碼效能
- ✅ 能處理實際業務問題

---

**準備好繼續你的學習之旅了嗎？** 🚀

接下來我會為你創建 Week 7-8 的完整內容！
