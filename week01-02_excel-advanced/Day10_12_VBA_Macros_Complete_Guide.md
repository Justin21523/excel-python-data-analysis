# Day 10-12: VBA Macros 完全自動化指南

**學習時間：** 10-12 小時
**資料檔案：** case01_realistic_sales_data.xlsx
**難度：** ⭐⭐⭐⭐⭐ (但非常實用！)

---

## 📋 學習目標

完成本階段後，你將能夠：

- ✅ 錄製和編輯巨集
- ✅ 理解 VBA 基礎語法
- ✅ 操作儲存格、範圍、工作表
- ✅ 使用迴圈和條件判斷
- ✅ 建立自動化資料處理流程
- ✅ 批次處理多個檔案
- ✅ 自動產生報表
- ✅ 寄送自動化 Email

---

## 🎯 什麼是 VBA？

**VBA (Visual Basic for Applications)**
- Excel 的程式語言
- 可以自動化所有 Excel 操作
- 錄製巨集 = 自動產生 VBA 代碼
- 可以手動編寫更複雜的邏輯

**為什麼要學 VBA？**
- ⚡ 自動化重複性工作（節省 90% 時間）
- 🔄 批次處理大量檔案
- 📊 一鍵生成複雜報表
- 📧 自動寄送 Email
- 🎯 建立自訂功能按鈕

---

## 📊 Part 1: VBA 環境設定（30 分鐘）

### **Step 1: 啟用「開發人員」功能區**

1. **檔案 → 選項 → 自訂功能區**
2. 右側「主要索引標籤」中勾選 **開發人員**
3. 點選「確定」

現在功能區會出現「開發人員」標籤！

---

### **Step 2: 開啟 VBA 編輯器（VBE）**

**三種方式：**
1. 開發人員 → Visual Basic
2. 按 `Alt + F11`
3. 右鍵工作表標籤 → 檢視程式碼

**VBE 介面：**
```
┌────────────────────────────────────────────┐
│ [檔案] [編輯] [檢視] [插入] [偵錯] [執行]  │
├──────────┬──────────────────┬──────────────┤
│ 專案視窗 │ 程式碼視窗       │ 屬性視窗     │
│          │                  │              │
│ VBA      │ Sub MyMacro()    │ Name:        │
│ Project  │   ' 程式碼      │ Workbook1    │
│  ├ 模組  │ End Sub          │              │
│  └ 表單  │                  │              │
└──────────┴──────────────────┴──────────────┘
```

---

### **Step 3: 第一個巨集 - Hello World**

1. 在 VBE 中：插入 → 模組
2. 輸入以下代碼：

```vba
Sub HelloWorld()
    MsgBox "Hello, VBA World!"
End Sub
```

3. 按 `F5` 或點擊 ▶️ 執行
4. 會彈出訊息方塊！

**恭喜！你寫出了第一個 VBA 程式！** 🎉

---

## 📊 Part 2: 巨集錄製（1 小時）

### **練習 1：錄製第一個巨集**

**任務：** 自動格式化標題列

**步驟：**

1. **開始錄製**
   - 開發人員 → 錄製巨集
   - 巨集名稱：`FormatHeader`
   - 快速鍵：`Ctrl + Shift + H`
   - 儲存在：此活頁簿

2. **執行操作**
   - 選取 A1:AN1（標題列）
   - 字體：粗體、14pt
   - 填滿顏色：深藍色
   - 字體顏色：白色
   - 對齊：置中
   - 自動調整欄寬

3. **停止錄製**
   - 開發人員 → 停止錄製

4. **查看生成的代碼**
   - Alt + F11 開啟 VBE
   - 找到「模組1」→ 雙擊

**生成的代碼：**
```vba
Sub FormatHeader()
    Range("A1:AN1").Select
    With Selection
        .Font.Bold = True
        .Font.Size = 14
        .Interior.Color = RGB(0, 51, 102)
        .Font.Color = RGB(255, 255, 255)
        .HorizontalAlignment = xlCenter
    End With
    Columns("A:AN").AutoFit
End Sub
```

---

### **練習 2：測試巨集**

1. 回到 Excel（Alt + F11）
2. 按 `Ctrl + Shift + H`
3. 標題列自動格式化！

**或使用按鈕：**
1. 插入 → 圖案 → 矩形
2. 右鍵 → 指定巨集 → FormatHeader
3. 輸入文字：「格式化標題」
4. 點擊按鈕執行！

---

### **練習 3：錄製條件格式巨集**

**任務：** 自動為金額欄位加上資料橫條

**操作：**
1. 錄製巨集（名稱：`AddDataBars`）
2. 選取訂單總額欄位（AB:AB）
3. 常用 → 設定格式化的條件 → 資料橫條 → 綠色資料橫條
4. 停止錄製

**生成的代碼：**
```vba
Sub AddDataBars()
    Range("AB:AB").Select
    Selection.FormatConditions.AddDatabar
    With Selection.FormatConditions(1)
        .BarColor.Color = RGB(99, 190, 123)
        .ShowValue = True
        .Type = xlDatabar
    End With
End Sub
```

---

## 📊 Part 3: VBA 基礎語法（2 小時）

### **3.1 變數與資料類型**

```vba
Sub VariableExample()
    ' 宣告變數
    Dim 產品名稱 As String        ' 文字
    Dim 單價 As Double            ' 小數
    Dim 數量 As Integer           ' 整數（-32768 to 32767）
    Dim 金額 As Long              ' 長整數（更大範圍）
    Dim 是否完成 As Boolean       ' True/False
    Dim 訂單日期 As Date          ' 日期

    ' 賦值
    產品名稱 = "iPhone 15"
    單價 = 30000
    數量 = 2
    金額 = 單價 * 數量
    是否完成 = True
    訂單日期 = Date  ' 今天

    ' 顯示結果
    MsgBox "產品：" & 產品名稱 & vbCrLf & _
           "金額：NT$ " & Format(金額, "#,##0")
End Sub
```

**資料類型總覽：**
| 類型 | 說明 | 範例 |
|------|------|------|
| String | 文字 | "Hello" |
| Integer | 整數 | 100 |
| Long | 長整數 | 1000000 |
| Double | 小數 | 3.14159 |
| Boolean | 布林值 | True / False |
| Date | 日期 | #2024-11-15# |
| Range | 範圍 | Range("A1") |
| Worksheet | 工作表 | ActiveSheet |

---

### **3.2 儲存格操作**

```vba
Sub CellOperations()
    ' 方法 1: Range
    Range("A1").Value = "產品名稱"
    Range("B1").Value = 1000

    ' 方法 2: Cells (行, 列)
    Cells(1, 1).Value = "產品名稱"
    Cells(1, 2).Value = 1000

    ' 方法 3: 指定工作表
    Worksheets("訂單明細").Range("A1").Value = "測試"

    ' 讀取儲存格值
    Dim 產品 As String
    產品 = Range("A2").Value

    ' 選取範圍
    Range("A1:E100").Select

    ' 設定格式
    Range("A1").Font.Bold = True
    Range("A1").Font.Size = 14
    Range("A1").Font.Color = RGB(255, 0, 0)  ' 紅色
    Range("A1").Interior.Color = RGB(255, 255, 0)  ' 黃色

    ' 自動調整欄寬
    Columns("A:E").AutoFit

    ' 清除內容
    Range("A1").ClearContents

    ' 清除格式
    Range("A1").ClearFormats

    ' 全部清除
    Range("A1").Clear
End Sub
```

---

### **3.3 條件判斷（If-Then-Else）**

```vba
Sub IfExample()
    Dim 分數 As Integer
    Dim 等級 As String

    分數 = Range("A2").Value

    ' 單層判斷
    If 分數 >= 60 Then
        等級 = "及格"
    End If

    ' 雙層判斷
    If 分數 >= 60 Then
        等級 = "及格"
    Else
        等級 = "不及格"
    End If

    ' 多層判斷
    If 分數 >= 90 Then
        等級 = "優秀"
    ElseIf 分數 >= 80 Then
        等級 = "良好"
    ElseIf 分數 >= 60 Then
        等級 = "及格"
    Else
        等級 = "不及格"
    End If

    ' 單行判斷
    等級 = IIf(分數 >= 60, "及格", "不及格")

    Range("B2").Value = 等級
End Sub
```

---

### **3.4 迴圈（For / For Each / Do While）**

#### **For 迴圈**

```vba
Sub ForLoop()
    Dim i As Integer

    ' 基本 For 迴圈
    For i = 1 To 10
        Cells(i, 1).Value = i
        Cells(i, 2).Value = i * 2
    Next i

    ' 指定步長
    For i = 2 To 100 Step 2  ' 偶數
        Cells(i/2, 3).Value = i
    Next i

    ' 倒數迴圈
    For i = 10 To 1 Step -1
        Cells(11-i, 4).Value = i
    Next i
End Sub
```

#### **For Each 迴圈**

```vba
Sub ForEachLoop()
    Dim 儲存格 As Range

    ' 遍歷範圍中的每個儲存格
    For Each 儲存格 In Range("A1:A10")
        儲存格.Value = 儲存格.Value * 1.1  ' 漲價 10%
    Next 儲存格

    ' 遍歷所有工作表
    Dim ws As Worksheet
    For Each ws In ThisWorkbook.Worksheets
        Debug.Print ws.Name
    Next ws
End Sub
```

#### **Do While 迴圈**

```vba
Sub DoWhileLoop()
    Dim i As Integer
    i = 1

    ' 當條件為真時持續執行
    Do While Cells(i, 1).Value <> ""
        Cells(i, 2).Value = Cells(i, 1).Value * 2
        i = i + 1
    Loop

    ' 或使用 Do Until（直到條件為真）
    i = 1
    Do Until Cells(i, 1).Value = ""
        Cells(i, 2).Value = Cells(i, 1).Value * 2
        i = i + 1
    Loop
End Sub
```

---

### **3.5 Select Case（多分支選擇）**

```vba
Sub SelectCaseExample()
    Dim 月份 As Integer
    Dim 季度 As String

    月份 = Month(Date)

    Select Case 月份
        Case 1, 2, 3
            季度 = "Q1"
        Case 4, 5, 6
            季度 = "Q2"
        Case 7, 8, 9
            季度 = "Q3"
        Case 10, 11, 12
            季度 = "Q4"
        Case Else
            季度 = "無效月份"
    End Select

    MsgBox "現在是 " & 季度
End Sub
```

---

## 📊 Part 4: 實用巨集範例（3 小時）

### **範例 1：自動資料清洗**

```vba
Sub AutoCleanData()
    Dim ws As Worksheet
    Dim 最後列 As Long
    Dim i As Long

    Set ws = Worksheets("訂單明細")
    最後列 = ws.Cells(ws.Rows.Count, 1).End(xlUp).Row

    ' 1. 移除空白列（從後往前刪除，避免索引錯誤）
    For i = 最後列 To 2 Step -1
        If Application.WorksheetFunction.CountA(ws.Rows(i)) = 0 Then
            ws.Rows(i).Delete
        End If
    Next i

    ' 2. 移除重複資料（根據訂單編號）
    ws.Range("A1").CurrentRegion.RemoveDuplicates Columns:=1, Header:=xlYes

    ' 3. 清除多餘空格
    更新最後列 = ws.Cells(ws.Rows.Count, 1).End(xlUp).Row
    For i = 2 To 最後列
        ws.Cells(i, 1).Value = Trim(ws.Cells(i, 1).Value)
    Next i

    ' 4. 統一地名格式（台北→臺北）
    ws.Range("E:E").Replace What:="台北", Replacement:="臺北", LookAt:=xlPart

    MsgBox "資料清洗完成！" & vbCrLf & "處理了 " & 最後列-1 & " 筆資料"
End Sub
```

**Python 對照：**
```python
# 移除空白列
df.dropna(how='all', inplace=True)

# 移除重複
df.drop_duplicates(subset=['訂單編號'], inplace=True)

# 清除空格
df['欄位'] = df['欄位'].str.strip()

# 取代
df['地址'] = df['地址'].str.replace('台北', '臺北')
```

---

### **範例 2：批次匯入 CSV 檔案**

```vba
Sub BatchImportCSV()
    Dim 檔案路徑 As String
    Dim 檔案名稱 As String
    Dim wb As Workbook
    Dim wsTarget As Worksheet
    Dim 目標列 As Long

    ' 設定目標工作表
    Set wsTarget = ThisWorkbook.Worksheets("彙總")
    目標列 = 2  ' 從第 2 列開始（第 1 列是標題）

    ' 設定資料夾路徑
    檔案路徑 = "C:\Users\你的名字\Desktop\銷售資料\"
    檔案名稱 = Dir(檔案路徑 & "*.csv")

    ' 迴圈處理所有 CSV 檔案
    Do While 檔案名稱 <> ""
        ' 開啟 CSV
        Set wb = Workbooks.Open(檔案路徑 & 檔案名稱)

        ' 找到最後一列
        Dim 來源最後列 As Long
        來源最後列 = wb.Sheets(1).Cells(wb.Sheets(1).Rows.Count, 1).End(xlUp).Row

        ' 複製資料（跳過標題列）
        If 來源最後列 > 1 Then
            wb.Sheets(1).Range("A2:Z" & 來源最後列).Copy
            wsTarget.Cells(目標列, 1).PasteSpecial xlPasteValues
            目標列 = 目標列 + (來源最後列 - 1)
        End If

        ' 關閉檔案（不儲存）
        wb.Close SaveChanges:=False

        ' 下一個檔案
        檔案名稱 = Dir()
    Loop

    MsgBox "匯入完成！共 " & (目標列 - 2) & " 筆資料"
End Sub
```

**Python 對照：**
```python
import glob
import pandas as pd

dfs = []
for file in glob.glob('銷售資料/*.csv'):
    df = pd.read_csv(file)
    dfs.append(df)

result = pd.concat(dfs, ignore_index=True)
```

---

### **範例 3：自動產生月報**

```vba
Sub GenerateMonthlyReport()
    Dim wsReport As Worksheet
    Dim 報表名稱 As String

    ' 建立新工作表
    報表名稱 = "月報_" & Format(Date, "yyyymm")
    Set wsReport = ThisWorkbook.Worksheets.Add
    wsReport.Name = 報表名稱

    ' 寫入標題
    With wsReport
        .Range("A1").Value = Format(Date, "yyyy年mm月") & " 銷售報表"
        .Range("A1").Font.Size = 18
        .Range("A1").Font.Bold = True

        ' 寫入 KPI
        .Range("A3").Value = "總營收"
        .Range("B3").Formula = "=SUM(訂單明細!AB:AB)"

        .Range("A4").Value = "訂單數"
        .Range("B4").Formula = "=COUNTA(訂單明細!A:A)-1"

        .Range("A5").Value = "平均客單價"
        .Range("B5").Formula = "=B3/B4"

        ' 格式化數值
        .Range("B3").NumberFormat = "NT$#,##0"
        .Range("B5").NumberFormat = "NT$#,##0"

        ' 建立樞紐分析表（程式化方式）
        CreatePivotTable wsReport
    End With

    MsgBox "月報已生成：" & 報表名稱
End Sub

Sub CreatePivotTable(wsTarget As Worksheet)
    Dim wsSource As Worksheet
    Dim ptCache As PivotCache
    Dim pt As PivotTable

    Set wsSource = Worksheets("訂單明細")

    ' 建立樞紐快取
    Set ptCache = ThisWorkbook.PivotCaches.Create( _
        SourceType:=xlDatabase, _
        SourceData:=wsSource.Range("A1").CurrentRegion)

    ' 建立樞紐分析表
    Set pt = ptCache.CreatePivotTable( _
        TableDestination:=wsTarget.Range("A10"), _
        TableName:="產品銷售")

    ' 設定欄位
    With pt
        .PivotFields("產品類別").Orientation = xlRowField
        .AddDataField .PivotFields("訂單總額"), "銷售額", xlSum
    End With
End Sub
```

---

### **範例 4：自動寄送 Email**

```vba
Sub SendReportEmail()
    Dim OutlookApp As Object
    Dim OutlookMail As Object
    Dim 收件者 As String
    Dim 主旨 As String
    Dim 內容 As String
    Dim 附件路徑 As String

    ' 建立 Outlook 物件
    Set OutlookApp = CreateObject("Outlook.Application")
    Set OutlookMail = OutlookApp.CreateItem(0)

    ' 設定郵件內容
    收件者 = "manager@company.com"
    主旨 = Format(Date, "yyyy年mm月dd日") & " 銷售報表"
    內容 = "您好，" & vbCrLf & vbCrLf & _
           "附件為本日銷售報表，請參閱。" & vbCrLf & vbCrLf & _
           "主要數據：" & vbCrLf & _
           "• 總銷售額：NT$ " & Format(Range("B3").Value, "#,##0") & vbCrLf & _
           "• 訂單數：" & Range("B4").Value & vbCrLf & _
           "• 平均客單價：NT$ " & Format(Range("B5").Value, "#,##0") & vbCrLf & vbCrLf & _
           "此郵件由系統自動發送。"

    附件路徑 = ThisWorkbook.Path & "\" & ThisWorkbook.Name

    ' 設定郵件
    With OutlookMail
        .To = 收件者
        .CC = "team@company.com"
        .Subject = 主旨
        .Body = 內容
        .Attachments.Add 附件路徑

        ' .Send  ' 直接發送
        .Display  ' 顯示預覽（建議先預覽）
    End With

    ' 清理物件
    Set OutlookMail = Nothing
    Set OutlookApp = Nothing

    MsgBox "郵件已準備完成！"
End Sub
```

**Python 對照：**
```python
import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from email.mime.base import MIMEBase
from email import encoders

msg = MIMEMultipart()
msg['From'] = 'sender@company.com'
msg['To'] = 'manager@company.com'
msg['Subject'] = '銷售報表'

body = '您好，\n\n附件為銷售報表...'
msg.attach(MIMEText(body, 'plain'))

# 附加檔案
attachment = open('report.xlsx', 'rb')
part = MIMEBase('application', 'octet-stream')
part.set_payload(attachment.read())
encoders.encode_base64(part)
part.add_header('Content-Disposition', 'attachment; filename=report.xlsx')
msg.attach(part)

# 發送
server = smtplib.SMTP('smtp.gmail.com', 587)
server.starttls()
server.login('sender@company.com', 'password')
server.send_message(msg)
server.quit()
```

---

### **範例 5：進度條顯示**

```vba
Sub ProgressBarExample()
    Dim i As Long
    Dim 總筆數 As Long

    總筆數 = 1000

    ' 處理資料
    For i = 1 To 總筆數
        ' 更新進度條
        Application.StatusBar = "處理中... " & Format(i / 總筆數, "0%") & " 完成"

        ' 你的處理邏輯
        Cells(i, 1).Value = i * 2

        ' 允許 Excel 更新顯示
        DoEvents
    Next i

    ' 清除進度條
    Application.StatusBar = False

    MsgBox "處理完成！"
End Sub
```

---

## 📊 Part 5: 錯誤處理（1 小時）

### **基礎錯誤處理**

```vba
Sub ErrorHandlingBasic()
    On Error GoTo ErrorHandler

    ' 可能產生錯誤的代碼
    Dim 數值 As Double
    數值 = Range("A1").Value / Range("B1").Value  ' 如果 B1 是 0，會報錯

    MsgBox "結果：" & 數值
    Exit Sub

ErrorHandler:
    MsgBox "發生錯誤：" & Err.Description
End Sub
```

### **進階錯誤處理**

```vba
Sub ErrorHandlingAdvanced()
    On Error Resume Next  ' 忽略錯誤，繼續執行

    Dim ws As Worksheet
    Set ws = Worksheets("不存在的工作表")

    If Err.Number <> 0 Then
        MsgBox "工作表不存在，將建立新的工作表"
        Set ws = ThisWorkbook.Worksheets.Add
        ws.Name = "新工作表"
        Err.Clear
    End If

    On Error GoTo 0  ' 恢復正常錯誤處理
End Sub
```

### **記錄錯誤日誌**

```vba
Sub LogError()
    Dim wsLog As Worksheet
    Dim 下一列 As Long

    ' 確保有日誌工作表
    On Error Resume Next
    Set wsLog = Worksheets("錯誤日誌")
    If wsLog Is Nothing Then
        Set wsLog = ThisWorkbook.Worksheets.Add
        wsLog.Name = "錯誤日誌"
        wsLog.Range("A1:D1").Value = Array("時間", "錯誤編號", "錯誤描述", "位置")
    End If
    On Error GoTo 0

    ' 記錄錯誤
    下一列 = wsLog.Cells(wsLog.Rows.Count, 1).End(xlUp).Row + 1
    wsLog.Cells(下一列, 1).Value = Now
    wsLog.Cells(下一列, 2).Value = Err.Number
    wsLog.Cells(下一列, 3).Value = Err.Description
    wsLog.Cells(下一列, 4).Value = "Sub XXX"
End Sub
```

---

## 🎯 Final Project: 完整自動化系統（4 小時）

### **專案需求**

建立一個一鍵式自動化銷售報表系統，包含：

1. 批次匯入資料
2. 自動資料清洗
3. 產生分析報表
4. 建立樞紐分析儀表板
5. 匯出 PDF
6. 自動寄送 Email

---

### **完整代碼**

```vba
' ============================================
' 主控制模組
' ============================================
Sub 一鍵執行全部()
    Application.ScreenUpdating = False
    Application.DisplayAlerts = False

    On Error GoTo ErrorHandler

    ' 步驟 1: 匯入資料
    Application.StatusBar = "步驟 1/6: 匯入資料..."
    Call 匯入所有CSV檔案

    ' 步驟 2: 清洗資料
    Application.StatusBar = "步驟 2/6: 清洗資料..."
    Call 自動清洗資料

    ' 步驟 3: 產生報表
    Application.StatusBar = "步驟 3/6: 產生報表..."
    Call 產生月報

    ' 步驟 4: 建立儀表板
    Application.StatusBar = "步驟 4/6: 建立儀表板..."
    Call 建立儀表板

    ' 步驟 5: 匯出 PDF
    Application.StatusBar = "步驟 5/6: 匯出 PDF..."
    Call 匯出PDF

    ' 步驟 6: 寄送 Email
    Application.StatusBar = "步驟 6/6: 寄送 Email..."
    Call 寄送報表Email

    Application.StatusBar = False
    Application.ScreenUpdating = True
    Application.DisplayAlerts = True

    MsgBox "✅ 全部完成！" & vbCrLf & vbCrLf & _
           "報表已產生並寄出。", vbInformation, "成功"

    Exit Sub

ErrorHandler:
    Application.StatusBar = False
    Application.ScreenUpdating = True
    Application.DisplayAlerts = True
    MsgBox "❌ 發生錯誤：" & Err.Description, vbCritical, "錯誤"
End Sub

' ============================================
' 子模組 1: 匯入資料
' ============================================
Sub 匯入所有CSV檔案()
    ' （使用範例 2 的代碼）
End Sub

' ============================================
' 子模組 2: 清洗資料
' ============================================
Sub 自動清洗資料()
    ' （使用範例 1 的代碼）
End Sub

' ============================================
' 子模組 3: 產生報表
' ============================================
Sub 產生月報()
    ' （使用範例 3 的代碼）
End Sub

' ============================================
' 子模組 4: 建立儀表板
' ============================================
Sub 建立儀表板()
    Dim wsDash As Worksheet

    ' 建立儀表板工作表
    On Error Resume Next
    Set wsDash = Worksheets("儀表板")
    If wsDash Is Nothing Then
        Set wsDash = ThisWorkbook.Worksheets.Add
        wsDash.Name = "儀表板"
    Else
        wsDash.Cells.Clear
    End If
    On Error GoTo 0

    ' 設定標題
    With wsDash.Range("A1:F1")
        .Merge
        .Value = "銷售儀表板 - " & Format(Date, "yyyy年mm月dd日")
        .Font.Size = 20
        .Font.Bold = True
        .HorizontalAlignment = xlCenter
        .VerticalAlignment = xlCenter
        .RowHeight = 40
    End With

    ' KPI 卡片（簡化版）
    With wsDash
        .Range("A3").Value = "總銷售額"
        .Range("B3").Formula = "=SUM(訂單明細!AB:AB)"
        .Range("B3").NumberFormat = "NT$#,##0"

        .Range("C3").Value = "訂單數"
        .Range("D3").Formula = "=COUNTA(訂單明細!A:A)-1"

        .Range("E3").Value = "平均客單價"
        .Range("F3").Formula = "=B3/D3"
        .Range("F3").NumberFormat = "NT$#,##0"
    End With

    ' 建立樞紐分析表
    Call 建立樞紐表(wsDash)

    ' 美化格式
    wsDash.Columns.AutoFit
End Sub

Sub 建立樞紐表(wsTarget As Worksheet)
    ' 建立產品類別銷售樞紐表
    Dim wsSource As Worksheet
    Dim ptCache As PivotCache
    Dim pt As PivotTable

    Set wsSource = Worksheets("訂單明細")

    Set ptCache = ThisWorkbook.PivotCaches.Create( _
        SourceType:=xlDatabase, _
        SourceData:=wsSource.Range("A1").CurrentRegion)

    Set pt = ptCache.CreatePivotTable( _
        TableDestination:=wsTarget.Range("A6"), _
        TableName:="產品銷售分析")

    With pt
        .PivotFields("產品類別").Orientation = xlRowField
        .AddDataField .PivotFields("訂單總額"), "銷售額", xlSum
        .PivotFields("銷售額").NumberFormat = "NT$#,##0"
    End With
End Sub

' ============================================
' 子模組 5: 匯出 PDF
' ============================================
Sub 匯出PDF()
    Dim 檔案名稱 As String
    Dim 路徑 As String

    路徑 = ThisWorkbook.Path & "\"
    檔案名稱 = "銷售報表_" & Format(Date, "yyyymmdd") & ".pdf"

    ' 匯出儀表板工作表為 PDF
    Worksheets("儀表板").ExportAsFixedFormat _
        Type:=xlTypePDF, _
        Filename:=路徑 & 檔案名稱, _
        Quality:=xlQualityStandard, _
        IncludeDocProperties:=True, _
        IgnorePrintAreas:=False, _
        OpenAfterPublish:=False
End Sub

' ============================================
' 子模組 6: 寄送 Email
' ============================================
Sub 寄送報表Email()
    ' （使用範例 4 的代碼）
End Sub
```

---

### **建立使用者介面**

**在儀表板工作表新增控制按鈕：**

1. **插入 → 圖案 → 矩形圓角**
2. **格式化按鈕：**
   - 填滿：藍色漸層
   - 文字：「🚀 一鍵執行全部」，18pt, 白色, 粗體
   - 大小：8cm × 3cm
3. **指定巨集：** 右鍵 → 指定巨集 → 一鍵執行全部
4. **新增其他按鈕：**
   - 「📥 匯入資料」
   - 「🧹 清洗資料」
   - 「📊 產生報表」
   - 「📧 寄送Email」

---

## 🎓 學習檢核清單

### **基礎技能**
- [ ] 能錄製和執行巨集
- [ ] 能開啟 VBE 並查看代碼
- [ ] 理解 Sub 和 Function 的差異
- [ ] 能宣告變數並賦值

### **語法掌握**
- [ ] 能操作儲存格（Range, Cells）
- [ ] 能使用 If-Then-Else 判斷
- [ ] 能使用 For 迴圈
- [ ] 能使用 For Each 遍歷
- [ ] 能使用 Select Case

### **實用技能**
- [ ] 能批次處理檔案
- [ ] 能自動清洗資料
- [ ] 能程式化建立樞紐表
- [ ] 能寄送自動化 Email
- [ ] 能處理錯誤

### **進階技能**
- [ ] 能建立完整自動化流程
- [ ] 能設計使用者介面
- [ ] 能優化代碼效能
- [ ] 能除錯和維護代碼

---

## 💡 VBA 最佳實踐

### **DO ✅**
- ✅ 為巨集取有意義的名稱
- ✅ 加上註解說明（' 這是註解）
- ✅ 使用縮排增加可讀性
- ✅ 使用 Application.ScreenUpdating = False 加速
- ✅ 使用錯誤處理（On Error）
- ✅ 測試前先備份檔案

### **DON'T ❌**
- ❌ 不要在迴圈中使用 Select（慢）
- ❌ 不要過度使用 ActiveSheet/ActiveCell
- ❌ 不要忽略錯誤處理
- ❌ 不要在沒有註解的情況下寫複雜邏輯
- ❌ 不要直接修改重要資料（先備份）

---

## 🚀 Week 2 完成！

**恭喜！你已經完成 Week 1-2 的所有內容：**

✅ Week 1: Excel 進階函數 (24-28h)
- Day 1-2: 動態陣列
- Day 3: UNIQUE/XLOOKUP
- Day 4-5: TEXT/DATE/LET/LAMBDA
- Day 6-7: Power Query ETL

✅ Week 2: Pivot Tables + VBA (24h)
- Day 8-9: 樞紐分析表完全掌握
- Day 10-12: VBA Macros 自動化

---

## 📖 下一步：Week 3-6 pandas 進階實戰

**你已準備好進入 Python 資料分析！**

現在你具備：
- ✅ Excel 資料處理思維
- ✅ 函數組合邏輯
- ✅ 樞紐分析概念
- ✅ 自動化流程設計

**這些技能將完美轉換到 pandas！**

**Week 3-6 預告：**
- MultiIndex 多層索引
- GroupBy 進階聚合
- 時間序列分析
- 效能優化技巧
- 使用 Olist 真實資料集
- 40+ 小時實戰練習

---

**準備好進入 Python 資料分析的世界了嗎？** 🐍🚀
