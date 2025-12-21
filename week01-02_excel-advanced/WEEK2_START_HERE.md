# 🚀 Week 2 完整學習系統 - 快速啟動指南

**恭喜完成 Week 1！** 現在進入 Excel 的終極技能：Pivot Tables + VBA Macros！

---

## 📦 Week 2 教材總覽

### **2 個核心模組 | 48-50 小時完整訓練**

#### **📊 Day 8-9: 樞紐分析表完全掌握（8-10h）**
- 檔案：`Day08_09_Pivot_Tables_Complete_Guide.md` (28KB)
- 內容：17 個練習 + 1 個完整儀表板專案
- 難度：⭐⭐⭐⭐

#### **💻 Day 10-12: VBA Macros 自動化（10-12h）**
- 檔案：`Day10_12_VBA_Macros_Complete_Guide.md` (35KB)
- 內容：5 個實用範例 + 1 個完整自動化系統
- 難度：⭐⭐⭐⭐⭐

---

## 🎯 學習路線

### **推薦路徑（完整學習，20-22h）**

```
Day 8 (4-5h)  → 樞紐分析表基礎 + 計算欄位
Day 9 (4-5h)  → 進階功能 + 完整儀表板專案
Day 10 (3-4h) → VBA 環境設定 + 巨集錄製 + 基礎語法
Day 11 (3-4h) → 5 個實用範例深入學習
Day 12 (4h)   → 完整自動化系統專案
```

### **快速通道（核心技能，12h）**

```
Day 8 (3h)  → 基礎樞紐 + 計算欄位 + Slicers
Day 9 (3h)  → 樞紐圖表 + 簡化版儀表板
Day 10 (2h) → 巨集錄製 + 基礎語法
Day 11-12 (4h) → 3 個最實用範例（清洗、匯入、報表）
```

---

## 📊 Day 8-9: 樞紐分析表學習指南

### **Part 1: 基礎樞紐（2h）**

**練習 1-3：**
- 單維度樞紐（產品類別銷售額）
- 雙維度交叉（類別 × 地區）
- 多值欄位（銷售額、訂單數、平均）

**執行步驟：**
1. 打開 `case01_realistic_sales_data.xlsx`
2. 選取「訂單明細」工作表任一儲存格
3. 插入 → 樞紐分析表
4. 跟著指南一步步操作

---

### **Part 2: 計算欄位（2h）**

**練習 4-6：**
- 建立「平均客單價」計算欄位
- 建立「毛利」計算欄位
- 建立「完成率」計算欄位

**關鍵概念：**
- 計算欄位 = 在樞紐表中自訂計算
- 公式使用欄位名稱，不是儲存格參照
- 例如：`= 訂單總額 * 0.3`

---

### **Part 3: 顯示值方式（2h）**

**10+ 種強大功能：**
- 百分比（佔總計、列、欄）
- 差異與差異百分比
- 累計總計
- 排名

**最實用：月度成長率**
```
設定：差異百分比 → 基底項目：（上一個）
結果：自動計算 MoM 成長率！
```

---

### **Part 4: 分組與互動（2h）**

**日期分組：**
- 右鍵日期 → 群組 → 選擇：月/季/年
- 自動建立階層式分組

**交叉分析篩選器（Slicers）：**
- 視覺化篩選按鈕
- 可連接多個樞紐表
- 建立互動式儀表板的關鍵！

**時間軸（Timeline）：**
- 拖曳選擇日期範圍
- 自動篩選樞紐表

---

### **Final Project: 銷售儀表板（4h）**

**需求：**
- 4 個樞紐分析表
- 4 個樞紐圖表
- 3 個 Slicers + 1 個 Timeline
- KPI 卡片（總銷售額、訂單數、平均客單價、成長率）

**結構：**
```
┌─────────────────────────────────────────────┐
│  銷售儀表板 - 2024年11月                     │
├───────┬───────┬───────┬───────────────────┤
│ KPI 1 │ KPI 2 │ KPI 3 │ Slicers + Timeline│
├───────┴───────┴───────┴───────────────────┤
│ 樞紐表 1       │ 圖表 1                    │
├────────────────┼───────────────────────────┤
│ 樞紐表 2       │ 圖表 2                    │
├────────────────┼───────────────────────────┤
│ 樞紐表 3       │ 圖表 3                    │
├────────────────┼───────────────────────────┤
│ 樞紐表 4       │ 圖表 4                    │
└────────────────┴───────────────────────────┘
```

---

## 💻 Day 10-12: VBA Macros 學習指南

### **Day 10: VBA 環境設定 + 基礎（3-4h）**

#### **Part 1: 環境設定（30min）**

1. **啟用「開發人員」標籤**
   - 檔案 → 選項 → 自訂功能區
   - 勾選「開發人員」

2. **開啟 VBA 編輯器（VBE）**
   - 按 `Alt + F11`
   - 或：開發人員 → Visual Basic

3. **第一個巨集**
   ```vba
   Sub HelloWorld()
       MsgBox "Hello, VBA!"
   End Sub
   ```
   - 按 F5 執行

---

#### **Part 2: 巨集錄製（1h）**

**練習 1：自動格式化標題**
1. 開發人員 → 錄製巨集
2. 設定快速鍵：`Ctrl + Shift + H`
3. 執行操作：格式化標題列
4. 停止錄製
5. Alt + F11 查看生成的代碼

**練習 2：建立按鈕**
1. 插入 → 圖案 → 矩形
2. 右鍵 → 指定巨集
3. 點擊按鈕執行！

---

#### **Part 3: VBA 基礎語法（2h）**

**變數與資料類型：**
```vba
Dim 產品名稱 As String
Dim 單價 As Double
Dim 數量 As Integer
Dim 金額 As Long
```

**儲存格操作：**
```vba
' 寫入
Range("A1").Value = "測試"
Cells(1, 1).Value = 1000

' 讀取
Dim 產品 As String
產品 = Range("A2").Value
```

**條件判斷：**
```vba
If 分數 >= 60 Then
    等級 = "及格"
Else
    等級 = "不及格"
End If
```

**迴圈：**
```vba
' For 迴圈
For i = 1 To 10
    Cells(i, 1).Value = i
Next i

' For Each 迴圈
For Each 儲存格 In Range("A1:A10")
    儲存格.Value = 儲存格.Value * 1.1
Next 儲存格
```

---

### **Day 11: 5 個實用範例（3-4h）**

#### **範例 1：自動資料清洗（1h）**

**功能：**
- 移除空白列
- 移除重複資料
- 清除多餘空格
- 統一格式

**代碼結構：**
```vba
Sub AutoCleanData()
    ' 1. 移除空白列（從後往前）
    ' 2. 移除重複（RemoveDuplicates）
    ' 3. 清除空格（Trim）
    ' 4. 取代文字（Replace）
End Sub
```

---

#### **範例 2：批次匯入 CSV（1h）**

**功能：**
- 從資料夾讀取所有 CSV
- 自動整合到單一工作表
- 跳過標題列

**關鍵代碼：**
```vba
檔案名稱 = Dir(檔案路徑 & "*.csv")

Do While 檔案名稱 <> ""
    ' 開啟、複製、關閉
    檔案名稱 = Dir()  ' 下一個檔案
Loop
```

---

#### **範例 3：自動產生月報（1h）**

**功能：**
- 建立新工作表
- 寫入 KPI 公式
- 程式化建立樞紐表
- 自動格式化

**建立樞紐表代碼：**
```vba
Set ptCache = ThisWorkbook.PivotCaches.Create(...)
Set pt = ptCache.CreatePivotTable(...)

With pt
    .PivotFields("產品類別").Orientation = xlRowField
    .AddDataField .PivotFields("訂單總額"), "銷售額", xlSum
End With
```

---

#### **範例 4：自動寄送 Email（30min）**

**功能：**
- 建立 Outlook 郵件
- 設定收件者、主旨、內容
- 附加檔案
- 發送或預覽

**關鍵代碼：**
```vba
Set OutlookApp = CreateObject("Outlook.Application")
Set OutlookMail = OutlookApp.CreateItem(0)

With OutlookMail
    .To = "manager@company.com"
    .Subject = "銷售報表"
    .Body = "請參閱附件..."
    .Attachments.Add 檔案路徑
    .Display  ' 或 .Send
End With
```

---

#### **範例 5：進度條（30min）**

**功能：**
- 在狀態列顯示處理進度
- 讓使用者知道程式在執行

**代碼：**
```vba
For i = 1 To 1000
    Application.StatusBar = "處理中... " & Format(i/1000, "0%")
    ' 你的處理邏輯
    DoEvents  ' 允許 Excel 更新顯示
Next i

Application.StatusBar = False
```

---

### **Day 12: 完整自動化系統（4h）**

#### **專案：一鍵式報表系統**

**功能流程：**
```
1. 批次匯入資料
   ↓
2. 自動清洗資料
   ↓
3. 產生分析報表
   ↓
4. 建立樞紐儀表板
   ↓
5. 匯出 PDF
   ↓
6. 寄送 Email
```

**主控制巨集：**
```vba
Sub 一鍵執行全部()
    Application.ScreenUpdating = False

    Call 匯入所有CSV檔案
    Call 自動清洗資料
    Call 產生月報
    Call 建立儀表板
    Call 匯出PDF
    Call 寄送報表Email

    Application.ScreenUpdating = True
    MsgBox "✅ 全部完成！"
End Sub
```

**建立控制按鈕：**
- 大按鈕：「🚀 一鍵執行全部」
- 小按鈕：各個子功能

---

## 🎓 學習檢核清單

### **Day 8-9: 樞紐分析表**

**基礎技能：**
- [ ] 能建立單維度樞紐表
- [ ] 能建立多維度交叉分析
- [ ] 能設定多個值欄位
- [ ] 理解 4 大區域（篩選/列/欄/值）

**計算欄位：**
- [ ] 能建立計算欄位
- [ ] 理解計算欄位 vs 一般公式
- [ ] 能建立複雜計算邏輯

**顯示值方式：**
- [ ] 能計算各種百分比
- [ ] 能計算差異與成長率
- [ ] 能計算累計總計

**互動功能：**
- [ ] 能新增 Slicers
- [ ] 能連接多個樞紐表
- [ ] 能新增 Timeline

**視覺化：**
- [ ] 能建立樞紐圖表
- [ ] 能選擇適當圖表類型
- [ ] 能建立組合圖

**專案：**
- [ ] 能建立完整儀表板
- [ ] 能整合多個元素
- [ ] 能建立 KPI 卡片

---

### **Day 10-12: VBA Macros**

**基礎技能：**
- [ ] 能錄製和執行巨集
- [ ] 能開啟 VBE 查看代碼
- [ ] 理解 Sub 和 Function
- [ ] 能宣告變數

**語法掌握：**
- [ ] 能操作儲存格（Range/Cells）
- [ ] 能使用 If-Then-Else
- [ ] 能使用 For 迴圈
- [ ] 能使用 For Each
- [ ] 能使用 Select Case

**實用技能：**
- [ ] 能批次處理檔案
- [ ] 能自動清洗資料
- [ ] 能程式化建立樞紐表
- [ ] 能寄送自動化 Email
- [ ] 能處理錯誤

**專案：**
- [ ] 能建立完整自動化流程
- [ ] 能設計使用者介面
- [ ] 能優化代碼效能

---

## 💡 學習建議

### **DO ✅**

**樞紐分析表：**
- ✅ 資料源使用「表格」格式
- ✅ 定期重新整理樞紐表
- ✅ 使用 Slicers 而非手動篩選
- ✅ 設定數值格式

**VBA：**
- ✅ 為巨集取有意義的名稱
- ✅ 加上註解說明
- ✅ 使用縮排增加可讀性
- ✅ 使用錯誤處理
- ✅ 測試前先備份檔案

### **DON'T ❌**

**樞紐分析表：**
- ❌ 資料源有空白列或欄
- ❌ 在樞紐表中直接修改數值
- ❌ 過度複雜的計算欄位

**VBA：**
- ❌ 在迴圈中使用 Select（慢）
- ❌ 過度使用 ActiveSheet/ActiveCell
- ❌ 忽略錯誤處理
- ❌ 沒有註解的複雜邏輯

---

## 🚀 立即開始

### **Step 1: 閱讀完整指南**

```bash
cd /home/justin/web-projects/excel-python-data-analysis/week01-02_excel-advanced

# Day 8-9: 樞紐分析表
cat Day08_09_Pivot_Tables_Complete_Guide.md

# Day 10-12: VBA Macros
cat Day10_12_VBA_Macros_Complete_Guide.md
```

---

### **Step 2: 打開練習檔案**

```bash
# 使用 Week 1 的資料檔案
explorer.exe case01_realistic_sales_data.xlsx
```

---

### **Step 3: 開始實作**

**Day 8（建議從這裡開始）：**
1. 打開 Excel
2. 選取「訂單明細」工作表
3. 插入 → 樞紐分析表
4. 跟著指南練習 1-17

**Day 10（VBA 入門）：**
1. 啟用「開發人員」標籤
2. 寫第一個 Hello World 巨集
3. 錄製第一個巨集
4. 學習基礎語法

---

## 📚 學習資源

### **官方文件**
- [Excel 樞紐分析表說明](https://support.microsoft.com/zh-tw/office/pivot-table)
- [VBA 語言參考](https://docs.microsoft.com/zh-tw/office/vba/api/overview/excel)

### **推薦影片教學**
- YouTube: ExcelIsFun - Pivot Table 系列
- YouTube: Wise Owl Tutorials - VBA 教學

### **推薦書籍**
- 《Excel VBA 實戰寶典》
- 《樞紐分析完全攻略》
- 《Power Query 資料整理》

---

## 🎯 完成後的能力

### **樞紐分析表**
- ✅ 能快速彙總大量資料
- ✅ 能進行多維度交叉分析
- ✅ 能建立互動式儀表板
- ✅ 能使用計算欄位進行進階計算
- ✅ 能視覺化呈現分析結果

### **VBA Macros**
- ✅ 能自動化所有 Excel 操作
- ✅ 能批次處理多個檔案
- ✅ 能建立一鍵式報表系統
- ✅ 能寄送自動化 Email
- ✅ 能設計使用者介面

### **職場應用**
- ✅ 每日銷售報表全自動化（節省 90% 時間）
- ✅ 月度分析儀表板自動更新
- ✅ 批次處理分店資料
- ✅ 自動寄送報表給管理層

---

## 📖 下一步：Week 3-6 pandas 進階

**Week 2 完成後，你已具備：**
- ✅ Excel 所有進階技能
- ✅ 資料處理思維
- ✅ 自動化流程設計能力
- ✅ 視覺化呈現能力

**這些技能將完美轉換到 pandas！**

**Week 3-6 預告：**
- 使用 Olist 真實電商資料（121MB）
- MultiIndex 多層索引（類似樞紐分析表）
- GroupBy 進階聚合（類似計算欄位）
- 時間序列分析（類似日期分組）
- 完整 ETL 流程（類似 VBA 自動化）
- 40+ 小時密集實戰

**已準備好：**
- ✅ Jupyter Lab 運行中（port 8888）
- ✅ Olist 資料集已下載（121MB）
- ✅ Amazon Reviews 資料集（88GB）
- ✅ case01_olist_complete_analysis.ipynb 範本

---

## 🎊 恭喜！

**你已經完成 Week 1-2 的所有教材！**

**總學習時數：** 40-50 小時
**總教材數量：**
- Week 1: 22 個檔案（872KB）
- Week 2: 2 個核心模組（63KB）
**練習數量：** 90+ 個實戰練習

**現在選擇你的下一步：**

**選項 A：開始 Week 2 實戰練習** ⭐
- 完成樞紐分析表儀表板
- 完成 VBA 自動化系統

**選項 B：直接進入 Week 3-6 pandas**
- 使用 Jupyter Lab（已運行）
- 分析 Olist 真實資料
- 學習 pandas 進階技巧

**選項 C：複習 Week 1-2 核心概念**
- 確保完全理解所有函數
- 確保能獨立完成專案

---

**準備好了嗎？開始你的 Week 2 學習之旅！** 🚀

```bash
cat Day08_09_Pivot_Tables_Complete_Guide.md
```

**Good luck! 💪**
