# Week 2: Day 10-12 VBA 完整代碼範例集

> 🎯 **本檔案包含所有可直接執行的 VBA 代碼**
>
> 每個範例都可以直接複製到 VBA 編輯器中執行

---

## 📋 目錄

1. [環境設定](#1-環境設定)
2. [基礎範例](#2-基礎範例)
3. [實戰範例](#3-實戰範例)
4. [進階自動化](#4-進階自動化)
5. [完整專案](#5-完整專案)

---

## 1. 環境設定

### 1.1 啟用開發人員標籤

**步驟：**
```
檔案 → 選項 → 自訂功能區 → 勾選「開發人員」→ 確定
```

### 1.2 開啟 VBA 編輯器

**方法 1：** 按 `Alt + F11`

**方法 2：** 開發人員標籤 → Visual Basic

### 1.3 插入新模組

在 VBA 編輯器中：
```
插入 → 模組
```

### 1.4 執行巨集

**方法 1：** 在 VBA 編輯器中按 `F5`

**方法 2：** Excel 中：開發人員 → 巨集 → 選擇巨集 → 執行

---

## 2. 基礎範例

### 範例 1: Hello World

```vba
Sub HelloWorld()
    ' 第一個 VBA 程式
    MsgBox "Hello, World!"
End Sub
```

**執行結果：** 彈出訊息視窗顯示 "Hello, World!"

---

### 範例 2: 儲存格基本操作

```vba
Sub 儲存格操作()
    ' 寫入單一儲存格
    Range("A1").Value = "產品名稱"
    Range("B1").Value = "數量"
    Range("C1").Value = "單價"

    ' 寫入資料
    Range("A2").Value = "iPhone 15"
    Range("B2").Value = 10
    Range("C2").Value = 30000

    ' 使用 Cells (行, 列) 方式
    Cells(3, 1).Value = "iPad Pro"
    Cells(3, 2).Value = 5
    Cells(3, 3).Value = 35000

    ' 讀取儲存格
    Dim 產品名稱 As String
    產品名稱 = Range("A2").Value

    MsgBox "第一個產品是：" & 產品名稱
End Sub
```

**執行結果：**
- A1:C1 寫入標題
- A2:C3 寫入兩筆產品資料
- 彈出訊息顯示 "第一個產品是：iPhone 15"

---

### 範例 3: 變數與資料類型

```vba
Sub 變數範例()
    ' 宣告各種類型的變數
    Dim 產品名稱 As String      ' 文字
    Dim 數量 As Integer         ' 整數（-32768 ~ 32767）
    Dim 單價 As Double          ' 小數
    Dim 金額 As Long            ' 大整數
    Dim 是否完成 As Boolean     ' True/False
    Dim 訂單日期 As Date        ' 日期

    ' 賦值
    產品名稱 = "MacBook Air"
    數量 = 3
    單價 = 35000.5
    金額 = 數量 * 單價
    是否完成 = True
    訂單日期 = Date  ' 今天日期

    ' 輸出結果
    Debug.Print "產品：" & 產品名稱
    Debug.Print "數量：" & 數量
    Debug.Print "單價：" & 單價
    Debug.Print "金額：" & 金額
    Debug.Print "是否完成：" & 是否完成
    Debug.Print "訂單日期：" & 訂單日期

    ' 提示：Debug.Print 會輸出到「立即視窗」（Ctrl+G 查看）
End Sub
```

**查看結果：** 在 VBA 編輯器按 `Ctrl + G` 開啟立即視窗

---

### 範例 4: For 迴圈

```vba
Sub For迴圈範例()
    Dim i As Integer

    ' 在 A 欄寫入 1~10
    For i = 1 To 10
        Cells(i, 1).Value = i
    Next i

    ' 在 B 欄寫入 2 的倍數
    For i = 1 To 10
        Cells(i, 2).Value = i * 2
    Next i

    ' 在 C 欄寫入平方
    For i = 1 To 10
        Cells(i, 3).Value = i * i
    Next i

    MsgBox "已完成 1~10 的數列生成"
End Sub
```

---

### 範例 5: For Each 迴圈

```vba
Sub ForEach迴圈範例()
    Dim 儲存格 As Range

    ' 遍歷 A1:A10，將所有數值 +100
    For Each 儲存格 In Range("A1:A10")
        If IsNumeric(儲存格.Value) Then
            儲存格.Value = 儲存格.Value + 100
        End If
    Next 儲存格

    MsgBox "A1:A10 的所有數值已 +100"
End Sub
```

---

### 範例 6: Do While 迴圈

```vba
Sub DoWhile迴圈範例()
    Dim i As Integer
    i = 1

    ' 從第 1 列開始，直到遇到空白儲存格
    Do While Cells(i, 1).Value <> ""
        ' 在 B 欄寫入「已處理」
        Cells(i, 2).Value = "已處理"
        i = i + 1
    Loop

    MsgBox "共處理了 " & (i - 1) & " 列資料"
End Sub
```

---

### 範例 7: If-Then-Else 條件判斷

```vba
Sub 條件判斷範例()
    Dim 分數 As Integer
    Dim 等級 As String

    分數 = Range("A1").Value

    ' 多層 If 判斷
    If 分數 >= 90 Then
        等級 = "優秀"
    ElseIf 分數 >= 80 Then
        等級 = "良好"
    ElseIf 分數 >= 60 Then
        等級 = "及格"
    Else
        等級 = "不及格"
    End If

    Range("B1").Value = 等級
    MsgBox "分數：" & 分數 & "，等級：" & 等級
End Sub
```

---

### 範例 8: Select Case 多分支判斷

```vba
Sub SelectCase範例()
    Dim 月份 As Integer
    Dim 季度 As String

    月份 = Month(Date)  ' 取得當前月份

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
            季度 = "錯誤"
    End Select

    MsgBox "現在是 " & 月份 & " 月，屬於 " & 季度
End Sub
```

---

## 3. 實戰範例

### 範例 9: 格式化標題列 ⭐

```vba
Sub 格式化標題列()
    ' 設定標題範圍
    Dim 標題範圍 As Range
    Set 標題範圍 = Range("A1:F1")

    With 標題範圍
        ' 粗體
        .Font.Bold = True

        ' 字體大小
        .Font.Size = 12

        ' 字體顏色（白色）
        .Font.Color = RGB(255, 255, 255)

        ' 背景顏色（藍色）
        .Interior.Color = RGB(68, 114, 196)

        ' 水平置中對齊
        .HorizontalAlignment = xlCenter

        ' 垂直置中對齊
        .VerticalAlignment = xlCenter

        ' 加上框線
        .Borders.LineStyle = xlContinuous
        .Borders.Weight = xlThin
    End With

    ' 自動調整欄寬
    Columns("A:F").AutoFit

    MsgBox "標題列格式化完成！"
End Sub
```

**Python 等價代碼：**
```python
import openpyxl
from openpyxl.styles import Font, PatternFill, Alignment

# 讀取工作簿
wb = openpyxl.load_workbook('data.xlsx')
ws = wb.active

# 設定標題格式
for cell in ws[1]:
    cell.font = Font(bold=True, size=12, color="FFFFFF")
    cell.fill = PatternFill(start_color="4472C4", end_color="4472C4", fill_type="solid")
    cell.alignment = Alignment(horizontal='center', vertical='center')

wb.save('data.xlsx')
```

---

### 範例 10: 自動資料清洗 ⭐⭐⭐

```vba
Sub 自動資料清洗()
    Application.ScreenUpdating = False  ' 關閉畫面更新加速

    Dim ws As Worksheet
    Set ws = ActiveSheet

    Dim 最後列 As Long
    最後列 = ws.Cells(ws.Rows.Count, 1).End(xlUp).Row

    Dim i As Long

    ' 步驟 1: 刪除空白列（從後往前刪除很重要！）
    For i = 最後列 To 2 Step -1
        If WorksheetFunction.CountA(ws.Rows(i)) = 0 Then
            ws.Rows(i).Delete
        End If
    Next i

    ' 更新最後列
    最後列 = ws.Cells(ws.Rows.Count, 1).End(xlUp).Row

    ' 步驟 2: 移除重複資料（以第一欄為準）
    ws.Range("A1").CurrentRegion.RemoveDuplicates Columns:=1, Header:=xlYes

    ' 更新最後列
    最後列 = ws.Cells(ws.Rows.Count, 1).End(xlUp).Row

    ' 步驟 3: 清除所有儲存格的前後空格
    For i = 2 To 最後列
        Dim j As Integer
        For j = 1 To 10  ' 假設有 10 欄
            If Not IsEmpty(ws.Cells(i, j).Value) Then
                ws.Cells(i, j).Value = Trim(ws.Cells(i, j).Value)
            End If
        Next j
    Next i

    ' 步驟 4: 統一地名（台北 → 臺北）
    ws.Columns("D:D").Replace What:="台北", Replacement:="臺北", LookAt:=xlPart
    ws.Columns("D:D").Replace What:="台中", Replacement:="臺中", LookAt:=xlPart
    ws.Columns("D:D").Replace What:="台南", Replacement:="臺南", LookAt:=xlPart
    ws.Columns("D:D").Replace What:="台東", Replacement:="臺東", LookAt:=xlPart

    Application.ScreenUpdating = True

    MsgBox "資料清洗完成！" & vbCrLf & _
           "處理列數：" & 最後列 - 1, vbInformation
End Sub
```

**關鍵技巧：**
1. **從後往前刪除**：`Step -1` 避免刪除後列號變動
2. **CountA()**：計算非空儲存格數量
3. **RemoveDuplicates**：內建去重功能
4. **Trim()**：移除前後空格
5. **Replace()**：批次取代

**Python 等價代碼：**
```python
import pandas as pd

# 讀取資料
df = pd.read_excel('data.xlsx')

# 1. 刪除全空白列
df = df.dropna(how='all')

# 2. 移除重複資料
df = df.drop_duplicates(subset=['產品名稱'])

# 3. 清除前後空格
df = df.apply(lambda x: x.str.strip() if x.dtype == "object" else x)

# 4. 統一地名
df['地區'] = df['地區'].str.replace('台北', '臺北')

# 儲存
df.to_excel('data_cleaned.xlsx', index=False)
```

---

### 範例 11: 批次匯入 CSV 檔案 ⭐⭐⭐⭐

```vba
Sub 批次匯入CSV檔案()
    Application.ScreenUpdating = False
    Application.DisplayAlerts = False

    Dim 檔案路徑 As String
    Dim 檔案名稱 As String
    Dim wb As Workbook
    Dim 目標工作表 As Worksheet
    Dim 來源工作表 As Worksheet
    Dim 最後列 As Long
    Dim 目標列 As Long
    Dim 檔案計數 As Integer

    ' 設定資料夾路徑（請修改為你的路徑）
    檔案路徑 = "C:\Users\YourName\Documents\CSV檔案\"

    ' 建立目標工作表
    Set 目標工作表 = ThisWorkbook.Worksheets.Add
    目標工作表.Name = "整合資料"

    目標列 = 1
    檔案計數 = 0

    ' 取得第一個 CSV 檔案
    檔案名稱 = Dir(檔案路徑 & "*.csv")

    ' 迴圈處理所有 CSV
    Do While 檔案名稱 <> ""
        ' 開啟 CSV
        Set wb = Workbooks.Open(檔案路徑 & 檔案名稱)
        Set 來源工作表 = wb.Worksheets(1)

        ' 找到來源資料的最後列
        最後列 = 來源工作表.Cells(來源工作表.Rows.Count, 1).End(xlUp).Row

        ' 如果是第一個檔案，複製標題
        If 檔案計數 = 0 Then
            來源工作表.Rows(1).Copy Destination:=目標工作表.Rows(目標列)
            目標列 = 目標列 + 1
        End If

        ' 複製資料（跳過標題）
        If 最後列 > 1 Then
            來源工作表.Range(來源工作表.Rows(2), 來源工作表.Rows(最後列)).Copy _
                Destination:=目標工作表.Rows(目標列)
            目標列 = 目標列 + 最後列 - 1
        End If

        ' 關閉 CSV（不儲存）
        wb.Close SaveChanges:=False

        檔案計數 = 檔案計數 + 1

        ' 取得下一個檔案
        檔案名稱 = Dir()
    Loop

    ' 自動調整欄寬
    目標工作表.Columns.AutoFit

    Application.ScreenUpdating = True
    Application.DisplayAlerts = True

    MsgBox "批次匯入完成！" & vbCrLf & _
           "共匯入 " & 檔案計數 & " 個 CSV 檔案" & vbCrLf & _
           "總計 " & (目標列 - 2) & " 列資料", vbInformation
End Sub
```

**關鍵技巧：**
1. **Dir() 函數**：列出資料夾中的檔案
2. **Do While...Loop**：持續處理直到沒有檔案
3. **Workbooks.Open()**：開啟外部檔案
4. **Close SaveChanges:=False**：關閉不儲存

**Python 等價代碼：**
```python
import pandas as pd
from pathlib import Path

# 資料夾路徑
folder_path = Path("C:/Users/YourName/Documents/CSV檔案/")

# 讀取所有 CSV
all_files = folder_path.glob("*.csv")
df_list = [pd.read_csv(file) for file in all_files]

# 合併
df_combined = pd.concat(df_list, ignore_index=True)

# 儲存
df_combined.to_excel("整合資料.xlsx", index=False)
print(f"共匯入 {len(df_list)} 個 CSV，總計 {len(df_combined)} 列資料")
```

---

### 範例 12: 自動產生月報 ⭐⭐⭐⭐

```vba
Sub 自動產生月報()
    Application.ScreenUpdating = False

    Dim ws報表 As Worksheet
    Dim ws資料 As Worksheet
    Dim 年月 As String

    ' 取得當前年月
    年月 = Format(Date, "yyyymm")

    ' 建立新工作表
    Set ws報表 = ThisWorkbook.Worksheets.Add
    ws報表.Name = "月報_" & 年月

    ' 設定原始資料工作表（請修改為你的工作表名稱）
    Set ws資料 = ThisWorkbook.Worksheets("訂單明細")

    ' ========================================
    ' Part 1: 標題區
    ' ========================================
    With ws報表.Range("A1")
        .Value = 年月 & " 月度銷售報表"
        .Font.Size = 18
        .Font.Bold = True
        .Font.Color = RGB(255, 255, 255)
        .Interior.Color = RGB(68, 114, 196)
        .HorizontalAlignment = xlCenter
    End With
    ws報表.Range("A1:F1").Merge
    ws報表.Rows(1).RowHeight = 40

    ' ========================================
    ' Part 2: KPI 卡片區
    ' ========================================
    Dim 列 As Integer
    列 = 3

    ' KPI 1: 總營收
    ws報表.Cells(列, 1).Value = "總營收"
    ws報表.Cells(列, 2).Formula = "=SUM(訂單明細!AB:AB)"
    ws報表.Cells(列, 2).NumberFormat = "NT$ #,##0"

    ' KPI 2: 訂單數
    ws報表.Cells(列 + 1, 1).Value = "總訂單數"
    ws報表.Cells(列 + 1, 2).Formula = "=COUNTA(訂單明細!A:A)-1"
    ws報表.Cells(列 + 1, 2).NumberFormat = "#,##0"

    ' KPI 3: 平均客單價
    ws報表.Cells(列 + 2, 1).Value = "平均客單價"
    ws報表.Cells(列 + 2, 2).Formula = "=AVERAGE(訂單明細!AB:AB)"
    ws報表.Cells(列 + 2, 2).NumberFormat = "NT$ #,##0"

    ' KPI 4: 客戶數
    ws報表.Cells(列 + 3, 1).Value = "客戶數"
    ws報表.Cells(列 + 3, 2).Formula = "=COUNTA(UNIQUE(訂單明細!E:E))-1"
    ws報表.Cells(列 + 3, 2).NumberFormat = "#,##0"

    ' 格式化 KPI 區域
    Dim kpi範圍 As Range
    Set kpi範圍 = ws報表.Range("A3:B6")
    With kpi範圍
        .Font.Size = 12
        .Borders.LineStyle = xlContinuous
        .Interior.Color = RGB(242, 242, 242)
    End With

    ws報表.Range("A3:A6").Font.Bold = True
    ws報表.Range("B3:B6").Font.Size = 14
    ws報表.Range("B3:B6").Font.Color = RGB(68, 114, 196)

    ' ========================================
    ' Part 3: 建立樞紐分析表
    ' ========================================
    Dim ptCache As PivotCache
    Dim pt As PivotTable
    Dim 資料範圍 As Range

    ' 設定資料範圍
    Set 資料範圍 = ws資料.Range("A1").CurrentRegion

    ' 建立樞紐快取
    Set ptCache = ThisWorkbook.PivotCaches.Create( _
        SourceType:=xlDatabase, _
        SourceData:=資料範圍)

    ' 建立樞紐表（放在 D3）
    Set pt = ptCache.CreatePivotTable( _
        TableDestination:=ws報表.Range("D3"), _
        TableName:="產品類別銷售")

    ' 設定樞紐表欄位
    With pt
        .PivotFields("產品類別").Orientation = xlRowField
        .PivotFields("產品類別").Position = 1

        With .PivotFields("訂單總額")
            .Orientation = xlDataField
            .Function = xlSum
            .Caption = "銷售額"
            .NumberFormat = "#,##0"
        End With

        With .PivotFields("訂單總額")
            .Orientation = xlDataField
            .Function = xlCount
            .Caption = "訂單數"
            .NumberFormat = "#,##0"
        End With
    End With

    ' ========================================
    ' Part 4: 格式美化
    ' ========================================
    ws報表.Columns.AutoFit
    ws報表.Rows.AutoFit

    ' 設定列印範圍
    ws報表.PageSetup.PrintArea = "$A$1:$F$30"
    ws報表.PageSetup.Orientation = xlPortrait
    ws報表.PageSetup.Zoom = False
    ws報表.PageSetup.FitToPagesWide = 1
    ws報表.PageSetup.FitToPagesTall = 1

    Application.ScreenUpdating = True

    MsgBox "月報已自動產生！" & vbCrLf & _
           "工作表名稱：月報_" & 年月, vbInformation
End Sub
```

**Python 等價代碼：**
```python
import pandas as pd
from openpyxl import load_workbook
from openpyxl.styles import Font, PatternFill, Alignment

# 讀取資料
df = pd.read_excel('訂單明細.xlsx')

# 計算 KPI
總營收 = df['訂單總額'].sum()
訂單數 = len(df)
平均客單價 = df['訂單總額'].mean()
客戶數 = df['客戶ID'].nunique()

# 建立報表
with pd.ExcelWriter('月報.xlsx', engine='openpyxl') as writer:
    # KPI 摘要
    kpi_df = pd.DataFrame({
        'KPI': ['總營收', '總訂單數', '平均客單價', '客戶數'],
        '數值': [總營收, 訂單數, 平均客單價, 客戶數]
    })
    kpi_df.to_excel(writer, sheet_name='月報', index=False, startrow=2)

    # 產品類別銷售（樞紐分析）
    pivot = df.pivot_table(
        values='訂單總額',
        index='產品類別',
        aggfunc=['sum', 'count']
    )
    pivot.to_excel(writer, sheet_name='月報', startrow=2, startcol=3)
```

---

### 範例 13: 自動寄送 Email ⭐⭐⭐

```vba
Sub 自動寄送Email()
    On Error GoTo ErrorHandler

    Dim OutlookApp As Object
    Dim OutlookMail As Object

    ' 建立 Outlook 物件
    Set OutlookApp = CreateObject("Outlook.Application")
    Set OutlookMail = OutlookApp.CreateItem(0)  ' 0 = olMailItem

    ' 設定郵件內容
    With OutlookMail
        ' 收件人（多個用分號分隔）
        .To = "manager@company.com; team@company.com"

        ' 副本
        .CC = "assistant@company.com"

        ' 主旨
        .Subject = Format(Date, "yyyymm") & " 月度銷售報表"

        ' 郵件內文（支援 HTML）
        .HTMLBody = "<h2>各位主管好：</h2>" & _
                    "<p>附件為本月銷售報表，請查收。</p>" & _
                    "<p><b>本月重點：</b></p>" & _
                    "<ul>" & _
                    "<li>總營收：NT$ 5,000,000</li>" & _
                    "<li>訂單數：1,234 筆</li>" & _
                    "<li>客戶數：567 位</li>" & _
                    "</ul>" & _
                    "<p>如有任何問題，請隨時與我聯繫。</p>" & _
                    "<p>祝安好<br>資料分析部</p>"

        ' 附加檔案
        .Attachments.Add ThisWorkbook.Path & "\月報_" & Format(Date, "yyyymm") & ".xlsx"

        ' 發送郵件（如果只想預覽，用 .Display 代替 .Send）
        .Send
        ' .Display  ' 只顯示不發送
    End With

    ' 釋放物件
    Set OutlookMail = Nothing
    Set OutlookApp = Nothing

    MsgBox "郵件已成功發送！", vbInformation
    Exit Sub

ErrorHandler:
    MsgBox "發送郵件時發生錯誤：" & vbCrLf & Err.Description, vbCritical
End Sub
```

**Python 等價代碼：**
```python
import smtplib
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from email.mime.base import MIMEBase
from email import encoders

# 建立郵件
msg = MIMEMultipart()
msg['From'] = "your_email@gmail.com"
msg['To'] = "manager@company.com"
msg['Subject'] = "202411 月度銷售報表"

# 郵件內文
body = """
各位主管好：

附件為本月銷售報表，請查收。

本月重點：
- 總營收：NT$ 5,000,000
- 訂單數：1,234 筆
- 客戶數：567 位

祝安好
資料分析部
"""
msg.attach(MIMEText(body, 'plain'))

# 附加檔案
filename = "月報_202411.xlsx"
with open(filename, "rb") as attachment:
    part = MIMEBase('application', 'octet-stream')
    part.set_payload(attachment.read())
    encoders.encode_base64(part)
    part.add_header('Content-Disposition', f"attachment; filename= {filename}")
    msg.attach(part)

# 發送郵件
server = smtplib.SMTP('smtp.gmail.com', 587)
server.starttls()
server.login("your_email@gmail.com", "your_password")
server.send_message(msg)
server.quit()

print("郵件已成功發送！")
```

---

### 範例 14: 進度條顯示 ⭐⭐

```vba
Sub 進度條範例()
    Dim i As Long
    Dim 總筆數 As Long

    總筆數 = 10000

    For i = 1 To 總筆數
        ' 你的處理邏輯
        ' ...

        ' 更新進度條（每 100 筆更新一次）
        If i Mod 100 = 0 Then
            Application.StatusBar = "處理中... " & Format(i / 總筆數, "0%") & " 完成"
            DoEvents  ' 讓 Excel 有機會更新畫面
        End If
    Next i

    ' 清除狀態列
    Application.StatusBar = False

    MsgBox "處理完成！共處理 " & 總筆數 & " 筆資料"
End Sub
```

---

## 4. 進階自動化

### 範例 15: 自動條件格式 ⭐⭐⭐

```vba
Sub 新增條件格式()
    Dim 資料範圍 As Range

    ' 設定資料範圍（假設金額在 D 欄）
    Set 資料範圍 = Range("D2:D1000")

    ' 清除現有條件格式
    資料範圍.FormatConditions.Delete

    ' 新增資料橫條（Data Bar）
    With 資料範圍.FormatConditions.AddDatabar
        .BarColor.Color = RGB(99, 142, 198)
        .ShowValue = True
        .BarBorder.Type = xlDataBarBorderSolid
        .BarBorder.ColorType = xlDataBarColor
        .BarBorder.Color.Color = RGB(68, 114, 196)
    End With

    MsgBox "條件格式新增完成！"
End Sub
```

---

### 範例 16: 自動建立圖表 ⭐⭐⭐

```vba
Sub 自動建立圖表()
    Dim ws As Worksheet
    Dim 圖表物件 As ChartObject
    Dim 資料範圍 As Range

    Set ws = ActiveSheet

    ' 設定資料範圍
    Set 資料範圍 = ws.Range("A1:B10")  ' 產品名稱 + 銷售額

    ' 建立圖表
    Set 圖表物件 = ws.ChartObjects.Add(Left:=300, Top:=50, Width:=400, Height:=300)

    With 圖表物件.Chart
        ' 設定資料來源
        .SetSourceData Source:=資料範圍

        ' 圖表類型（長條圖）
        .ChartType = xlColumnClustered

        ' 圖表標題
        .HasTitle = True
        .ChartTitle.Text = "產品銷售排名"

        ' 座標軸標題
        .Axes(xlCategory, xlPrimary).HasTitle = True
        .Axes(xlCategory, xlPrimary).AxisTitle.Text = "產品"

        .Axes(xlValue, xlPrimary).HasTitle = True
        .Axes(xlValue, xlPrimary).AxisTitle.Text = "銷售額（萬元）"

        ' 圖例位置
        .HasLegend = True
        .Legend.Position = xlLegendPositionBottom
    End With

    MsgBox "圖表建立完成！"
End Sub
```

---

### 範例 17: 自動保護工作表 ⭐⭐

```vba
Sub 保護工作表()
    Dim ws As Worksheet

    For Each ws In ThisWorkbook.Worksheets
        ' 保護工作表（允許選取、允許篩選、允許排序）
        ws.Protect Password:="1234", _
                   AllowFiltering:=True, _
                   AllowSorting:=True, _
                   AllowUsingPivotTables:=True
    Next ws

    MsgBox "所有工作表已保護！密碼：1234"
End Sub

Sub 解除保護工作表()
    Dim ws As Worksheet

    For Each ws In ThisWorkbook.Worksheets
        ws.Unprotect Password:="1234"
    Next ws

    MsgBox "所有工作表保護已解除！"
End Sub
```

---

## 5. 完整專案

### 範例 18: 一鍵自動化系統 ⭐⭐⭐⭐⭐

這是一個完整的自動化系統，整合所有功能：

```vba
'========================================
' 主程式：一鍵執行全部
'========================================
Sub 一鍵執行全部()
    On Error GoTo ErrorHandler

    Application.ScreenUpdating = False
    Application.DisplayAlerts = False
    Application.Calculation = xlCalculationManual

    Dim 開始時間 As Double
    開始時間 = Timer

    ' 顯示開始訊息
    Application.StatusBar = "自動化流程啟動中..."
    DoEvents

    ' ========================================
    ' 步驟 1: 匯入所有 CSV 檔案
    ' ========================================
    Application.StatusBar = "步驟 1/6：匯入 CSV 檔案..."
    DoEvents
    Call 匯入所有CSV檔案

    ' ========================================
    ' 步驟 2: 自動清洗資料
    ' ========================================
    Application.StatusBar = "步驟 2/6：清洗資料..."
    DoEvents
    Call 自動清洗資料

    ' ========================================
    ' 步驟 3: 產生月報
    ' ========================================
    Application.StatusBar = "步驟 3/6：產生月報..."
    DoEvents
    Call 產生月報

    ' ========================================
    ' 步驟 4: 建立儀表板
    ' ========================================
    Application.StatusBar = "步驟 4/6：建立儀表板..."
    DoEvents
    Call 建立儀表板

    ' ========================================
    ' 步驟 5: 匯出 PDF
    ' ========================================
    Application.StatusBar = "步驟 5/6：匯出 PDF..."
    DoEvents
    Call 匯出PDF

    ' ========================================
    ' 步驟 6: 寄送報表
    ' ========================================
    Application.StatusBar = "步驟 6/6：寄送報表..."
    DoEvents
    Call 寄送報表Email

    ' 恢復設定
    Application.ScreenUpdating = True
    Application.DisplayAlerts = True
    Application.Calculation = xlCalculationAutomatic
    Application.StatusBar = False

    ' 計算執行時間
    Dim 執行時間 As Double
    執行時間 = Timer - 開始時間

    ' 顯示完成訊息
    MsgBox "🎉 自動化流程執行完成！" & vbCrLf & vbCrLf & _
           "執行時間：" & Format(執行時間, "0.0") & " 秒" & vbCrLf & _
           "已完成：" & vbCrLf & _
           "  ✓ 資料匯入與清洗" & vbCrLf & _
           "  ✓ 月報產生" & vbCrLf & _
           "  ✓ 儀表板建立" & vbCrLf & _
           "  ✓ PDF 匯出" & vbCrLf & _
           "  ✓ Email 寄送", vbInformation, "執行成功"

    Exit Sub

ErrorHandler:
    Application.ScreenUpdating = True
    Application.DisplayAlerts = True
    Application.Calculation = xlCalculationAutomatic
    Application.StatusBar = False

    MsgBox "執行過程中發生錯誤：" & vbCrLf & vbCrLf & _
           "錯誤訊息：" & Err.Description & vbCrLf & _
           "錯誤編號：" & Err.Number, vbCritical, "執行錯誤"
End Sub

'========================================
' 子程式 1: 匯入所有 CSV 檔案
'========================================
Sub 匯入所有CSV檔案()
    ' （參考範例 11 的完整代碼）
    ' ...
End Sub

'========================================
' 子程式 2: 自動清洗資料
'========================================
Sub 自動清洗資料()
    ' （參考範例 10 的完整代碼）
    ' ...
End Sub

'========================================
' 子程式 3: 產生月報
'========================================
Sub 產生月報()
    ' （參考範例 12 的完整代碼）
    ' ...
End Sub

'========================================
' 子程式 4: 建立儀表板
'========================================
Sub 建立儀表板()
    Dim ws As Worksheet
    Set ws = ThisWorkbook.Worksheets.Add
    ws.Name = "儀表板_" & Format(Date, "yyyymm")

    ' 在這裡加入你的儀表板建立邏輯
    ' 可以包含：KPI 卡片、樞紐表、圖表、切片篩選器等
End Sub

'========================================
' 子程式 5: 匯出 PDF
'========================================
Sub 匯出PDF()
    Dim 檔案路徑 As String
    檔案路徑 = ThisWorkbook.Path & "\月報_" & Format(Date, "yyyymm") & ".pdf"

    ' 匯出指定工作表為 PDF
    ThisWorkbook.Worksheets("月報_" & Format(Date, "yyyymm")).ExportAsFixedFormat _
        Type:=xlTypePDF, _
        Filename:=檔案路徑, _
        Quality:=xlQualityStandard
End Sub

'========================================
' 子程式 6: 寄送報表 Email
'========================================
Sub 寄送報表Email()
    ' （參考範例 13 的完整代碼）
    ' ...
End Sub
```

---

## 6. 實用工具函數

### 工具函數 1: 找到最後一列

```vba
Function 找到最後一列(ws As Worksheet, 欄號 As Integer) As Long
    找到最後一列 = ws.Cells(ws.Rows.Count, 欄號).End(xlUp).Row
End Function

' 使用範例：
' Dim 最後列 As Long
' 最後列 = 找到最後一列(ActiveSheet, 1)  ' 找 A 欄最後一列
```

---

### 工具函數 2: 找到最後一欄

```vba
Function 找到最後一欄(ws As Worksheet, 列號 As Integer) As Integer
    找到最後一欄 = ws.Cells(列號, ws.Columns.Count).End(xlToLeft).Column
End Function
```

---

### 工具函數 3: 儲存格是否為空

```vba
Function 儲存格是空的(儲存格 As Range) As Boolean
    儲存格是空的 = (IsEmpty(儲存格.Value) Or Trim(儲存格.Value) = "")
End Function
```

---

### 工具函數 4: 檢查工作表是否存在

```vba
Function 工作表存在(工作表名稱 As String) As Boolean
    On Error Resume Next
    工作表存在 = Not (ThisWorkbook.Worksheets(工作表名稱) Is Nothing)
    On Error GoTo 0
End Function
```

---

## 7. 快捷鍵列表

| 快捷鍵 | 功能 |
|--------|------|
| `Alt + F11` | 開啟 VBA 編輯器 |
| `F5` | 執行巨集 |
| `F8` | 逐行執行（偵錯） |
| `Ctrl + G` | 開啟立即視窗 |
| `Ctrl + R` | 專案總管 |
| `Ctrl + Break` | 中斷執行 |
| `Alt + Q` | 離開 VBA 編輯器 |

---

## 8. 常見錯誤處理

### 錯誤處理範本

```vba
Sub 有錯誤處理的巨集()
    On Error GoTo ErrorHandler

    ' 你的代碼
    ' ...

    Exit Sub

ErrorHandler:
    MsgBox "發生錯誤：" & vbCrLf & _
           "錯誤編號：" & Err.Number & vbCrLf & _
           "錯誤描述：" & Err.Description, vbCritical

    ' 可選：記錄到日誌
    Debug.Print "錯誤時間：" & Now
    Debug.Print "錯誤編號：" & Err.Number
    Debug.Print "錯誤描述：" & Err.Description
End Sub
```

---

## 9. 效能優化技巧

```vba
Sub 效能優化範本()
    ' ========================================
    ' 開始前：關閉不必要的功能
    ' ========================================
    Application.ScreenUpdating = False      ' 關閉畫面更新
    Application.DisplayAlerts = False       ' 關閉警告訊息
    Application.Calculation = xlCalculationManual  ' 關閉自動計算
    Application.EnableEvents = False        ' 關閉事件觸發

    ' ========================================
    ' 你的代碼
    ' ========================================
    ' ...

    ' ========================================
    ' 結束後：恢復設定
    ' ========================================
    Application.ScreenUpdating = True
    Application.DisplayAlerts = True
    Application.Calculation = xlCalculationAutomatic
    Application.EnableEvents = True
End Sub
```

---

## 10. 學習建議

### 初學者路徑

1. ✅ **Week 1（2 小時）**
   - 範例 1-8：基礎語法
   - 練習：修改範例中的變數和條件

2. ✅ **Week 2（3 小時）**
   - 範例 9-11：實戰應用
   - 練習：在自己的資料上測試

3. ✅ **Week 3（3 小時）**
   - 範例 12-14：自動化工作流程
   - 練習：組合多個範例

4. ✅ **Week 4（4 小時）**
   - 範例 15-18：完整專案
   - 最終專案：建立自己的自動化系統

---

## 📚 下一步

完成 VBA 學習後，建議：

1. **實際應用**：在日常工作中找機會使用 VBA
2. **Python 轉換**：學習 Week 3-6 的 pandas 課程
3. **深入學習**：研究 Power Automate、Power BI

---

## 🎓 結語

VBA 是 Excel 自動化的強大工具，雖然 Python 正在取代某些應用場景，但 VBA 在：
- **即時操作**：直接在 Excel 中執行
- **無需安裝**：只要有 Excel 就能用
- **簡單任務**：快速錄製巨集

這些方面仍然非常實用！

掌握 VBA 後，再學習 Python 會更容易理解程式邏輯。

**祝學習順利！💪**
