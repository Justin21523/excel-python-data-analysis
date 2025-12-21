"""
創建 Week 2 VBA 實戰練習工作簿
包含所有可執行的巨集範例
"""

import openpyxl
from openpyxl.styles import Font, PatternFill, Alignment, Border, Side
from openpyxl.utils import get_column_letter
import random
from datetime import datetime, timedelta

def create_vba_practice_workbook():
    """創建 VBA 練習工作簿"""

    wb = openpyxl.Workbook()

    # 移除預設工作表
    if 'Sheet' in wb.sheetnames:
        del wb['Sheet']

    # ========================================
    # 工作表 1: 說明頁
    # ========================================
    ws_intro = wb.create_sheet("00_使用說明", 0)

    # 標題
    ws_intro['A1'] = "Week 2 VBA Macros 實戰練習工作簿"
    ws_intro['A1'].font = Font(size=20, bold=True, color="FFFFFF")
    ws_intro['A1'].fill = PatternFill(start_color="0066CC", end_color="0066CC", fill_type="solid")
    ws_intro['A1'].alignment = Alignment(horizontal='center', vertical='center')
    ws_intro.merge_cells('A1:H1')
    ws_intro.row_dimensions[1].height = 40

    # 說明內容
    instructions = [
        ["", ""],
        ["📚 本工作簿包含內容：", ""],
        ["", ""],
        ["1. 使用說明（本頁）", ""],
        ["2. 巨集練習資料 - 提供測試資料", ""],
        ["3. 空白練習區 - 供你練習寫 VBA", ""],
        ["", ""],
        ["🎯 學習步驟：", ""],
        ["", ""],
        ["Step 1: 啟用巨集", ""],
        ["  • 開啟檔案時選擇「啟用內容」", ""],
        ["", ""],
        ["Step 2: 啟用「開發人員」標籤", ""],
        ["  • 檔案 → 選項 → 自訂功能區", ""],
        ["  • 勾選「開發人員」→ 確定", ""],
        ["", ""],
        ["Step 3: 開啟 VBA 編輯器", ""],
        ["  • 按 Alt + F11", ""],
        ["  • 或：開發人員 → Visual Basic", ""],
        ["", ""],
        ["Step 4: 插入模組", ""],
        ["  • VBA 編輯器中：插入 → 模組", ""],
        ["  • 在模組中貼上範例代碼", ""],
        ["", ""],
        ["Step 5: 執行巨集", ""],
        ["  • 在 VBA 編輯器中按 F5", ""],
        ["  • 或：開發人員 → 巨集 → 選擇巨集 → 執行", ""],
        ["", ""],
        ["💡 提示：", ""],
        ["", ""],
        ["• 所有巨集範例都在教學文件中（Day10_12_VBA_Macros_Complete_Guide.md）", ""],
        ["• 可以先錄製巨集，再查看生成的代碼", ""],
        ["• 建議從簡單的範例開始練習", ""],
        ["• 執行前先備份檔案！", ""],
        ["", ""],
        ["📁 相關檔案：", ""],
        ["", ""],
        ["• Day10_12_VBA_Macros_Complete_Guide.md - 完整教學", ""],
        ["• WEEK2_START_HERE.md - 快速啟動指南", ""],
        ["• case01_realistic_sales_data.xlsx - 主要資料檔", ""],
    ]

    for i, row in enumerate(instructions, start=3):
        ws_intro[f'A{i}'] = row[0]
        if "📚" in row[0] or "🎯" in row[0] or "💡" in row[0] or "📁" in row[0]:
            ws_intro[f'A{i}'].font = Font(size=14, bold=True, color="0066CC")
        elif "Step" in row[0]:
            ws_intro[f'A{i}'].font = Font(size=11, bold=True)
        elif "  •" in row[0]:
            ws_intro[f'A{i}'].font = Font(size=10, color="666666")

    # 調整欄寬
    ws_intro.column_dimensions['A'].width = 80

    # ========================================
    # 工作表 2: 巨集練習資料
    # ========================================
    ws_data = wb.create_sheet("01_巨集練習資料", 1)

    # 標題
    ws_data['A1'] = "巨集練習資料（可用於測試各種 VBA 範例）"
    ws_data['A1'].font = Font(size=14, bold=True, color="FFFFFF")
    ws_data['A1'].fill = PatternFill(start_color="FF6600", end_color="FF6600", fill_type="solid")
    ws_data['A1'].alignment = Alignment(horizontal='center')
    ws_data.merge_cells('A1:F1')

    # 產生測試資料
    headers = ["產品名稱", "數量", "單價", "金額", "狀態", "備註"]
    for col, header in enumerate(headers, start=1):
        cell = ws_data.cell(row=3, column=col, value=header)
        cell.font = Font(bold=True, color="FFFFFF")
        cell.fill = PatternFill(start_color="4472C4", end_color="4472C4", fill_type="solid")
        cell.alignment = Alignment(horizontal='center')

    # 產品列表
    products = [
        "iPhone 15", "iPad Pro", "MacBook Air", "AirPods", "Apple Watch",
        "Samsung Galaxy", "小米手機", "華碩筆電", "羅技滑鼠", "機械鍵盤"
    ]

    statuses = ["已完成", "處理中", "已取消", "待確認"]

    # 生成 50 筆測試資料
    for row in range(4, 54):
        product = random.choice(products)
        quantity = random.randint(1, 10)
        price = random.randint(500, 50000)
        amount = quantity * price
        status = random.choice(statuses)
        note = random.choice(["正常", "急件", "補貨中", "", "VIP客戶"])

        ws_data.cell(row=row, column=1, value=product)
        ws_data.cell(row=row, column=2, value=quantity)
        ws_data.cell(row=row, column=3, value=price)
        ws_data.cell(row=row, column=4, value=amount)
        ws_data.cell(row=row, column=5, value=status)
        ws_data.cell(row=row, column=6, value=note)

    # 設定數值格式
    for row in range(4, 54):
        ws_data.cell(row=row, column=3).number_format = '#,##0'
        ws_data.cell(row=row, column=4).number_format = '#,##0'

    # 調整欄寬
    ws_data.column_dimensions['A'].width = 15
    ws_data.column_dimensions['B'].width = 8
    ws_data.column_dimensions['C'].width = 12
    ws_data.column_dimensions['D'].width = 12
    ws_data.column_dimensions['E'].width = 10
    ws_data.column_dimensions['F'].width = 12

    # ========================================
    # 工作表 3: VBA 範例代碼清單
    # ========================================
    ws_examples = wb.create_sheet("02_VBA範例清單", 2)

    # 標題
    ws_examples['A1'] = "VBA 巨集範例清單"
    ws_examples['A1'].font = Font(size=14, bold=True, color="FFFFFF")
    ws_examples['A1'].fill = PatternFill(start_color="70AD47", end_color="70AD47", fill_type="solid")
    ws_examples['A1'].alignment = Alignment(horizontal='center')
    ws_examples.merge_cells('A1:D1')

    # 範例清單
    examples = [
        ["", "", "", ""],
        ["編號", "範例名稱", "難度", "說明"],
        ["1", "格式化標題列", "⭐", "自動設定標題格式（粗體、顏色、對齊）"],
        ["2", "新增資料橫條", "⭐", "為數值欄位加上條件格式"],
        ["3", "Hello World", "⭐", "第一個 VBA 程式"],
        ["4", "儲存格操作", "⭐⭐", "讀取和寫入儲存格"],
        ["5", "迴圈遍歷", "⭐⭐", "使用 For 迴圈處理資料"],
        ["6", "條件判斷", "⭐⭐", "使用 If-Then-Else"],
        ["7", "自動資料清洗", "⭐⭐⭐", "移除空白列、重複資料、清除空格"],
        ["8", "批次匯入 CSV", "⭐⭐⭐⭐", "從資料夾讀取所有 CSV 並整合"],
        ["9", "自動產生月報", "⭐⭐⭐⭐", "建立新工作表、寫入 KPI、建立樞紐表"],
        ["10", "寄送 Email", "⭐⭐⭐", "自動產生 Outlook 郵件並附加檔案"],
        ["11", "進度條顯示", "⭐⭐", "在狀態列顯示處理進度"],
        ["12", "一鍵自動化系統", "⭐⭐⭐⭐⭐", "整合所有功能的完整系統"],
    ]

    for i, row in enumerate(examples, start=2):
        for j, value in enumerate(row, start=1):
            cell = ws_examples.cell(row=i, column=j, value=value)
            if i == 3:  # 標題列
                cell.font = Font(bold=True, color="FFFFFF")
                cell.fill = PatternFill(start_color="70AD47", end_color="70AD47", fill_type="solid")
                cell.alignment = Alignment(horizontal='center')

    # 調整欄寬
    ws_examples.column_dimensions['A'].width = 8
    ws_examples.column_dimensions['B'].width = 25
    ws_examples.column_dimensions['C'].width = 10
    ws_examples.column_dimensions['D'].width = 50

    # ========================================
    # 工作表 4: 空白練習區
    # ========================================
    ws_practice = wb.create_sheet("03_空白練習區", 3)

    ws_practice['A1'] = "空白練習區（在此測試你的 VBA 巨集）"
    ws_practice['A1'].font = Font(size=14, bold=True, color="FFFFFF")
    ws_practice['A1'].fill = PatternFill(start_color="9966FF", end_color="9966FF", fill_type="solid")
    ws_practice['A1'].alignment = Alignment(horizontal='center')
    ws_practice.merge_cells('A1:H1')

    ws_practice['A3'] = "提示："
    ws_practice['A3'].font = Font(bold=True)
    ws_practice['A4'] = "1. 在這個工作表中測試各種巨集"
    ws_practice['A5'] = "2. 可以複製「巨集練習資料」工作表的資料到這裡"
    ws_practice['A6'] = "3. 執行巨集後觀察結果"
    ws_practice['A7'] = "4. 如果結果不理想，可以按 Ctrl+Z 復原"

    # ========================================
    # 工作表 5: VBA 語法速查
    # ========================================
    ws_syntax = wb.create_sheet("04_VBA語法速查", 4)

    ws_syntax['A1'] = "VBA 語法速查表"
    ws_syntax['A1'].font = Font(size=14, bold=True, color="FFFFFF")
    ws_syntax['A1'].fill = PatternFill(start_color="FF3333", end_color="FF3333", fill_type="solid")
    ws_syntax['A1'].alignment = Alignment(horizontal='center')
    ws_syntax.merge_cells('A1:C1')

    syntax_items = [
        ["", "", ""],
        ["類別", "語法", "說明"],
        ["變數宣告", "Dim x As Integer", "宣告整數變數"],
        ["", "Dim name As String", "宣告文字變數"],
        ["", "Dim price As Double", "宣告小數變數"],
        ["儲存格操作", "Range(\"A1\").Value = 100", "寫入儲存格"],
        ["", "x = Range(\"A1\").Value", "讀取儲存格"],
        ["", "Cells(1, 1).Value = 100", "用行列索引寫入"],
        ["條件判斷", "If x > 10 Then ... End If", "單行判斷"],
        ["", "If...Then...Else...End If", "多行判斷"],
        ["迴圈", "For i = 1 To 10 ... Next i", "For 迴圈"],
        ["", "For Each cell In Range(...)", "For Each 迴圈"],
        ["", "Do While ... Loop", "While 迴圈"],
        ["訊息方塊", "MsgBox \"Hello\"", "顯示訊息"],
        ["", "MsgBox \"錯誤\", vbCritical", "顯示錯誤訊息"],
        ["工作表操作", "Worksheets(\"Sheet1\").Activate", "切換工作表"],
        ["", "Worksheets.Add", "新增工作表"],
        ["格式設定", "Range(\"A1\").Font.Bold = True", "粗體"],
        ["", "Range(\"A1\").Font.Size = 14", "字體大小"],
        ["", "Range(\"A1\").Font.Color = RGB(255,0,0)", "紅色字體"],
    ]

    for i, row in enumerate(syntax_items, start=2):
        for j, value in enumerate(row, start=1):
            cell = ws_syntax.cell(row=i, column=j, value=value)
            if i == 3:  # 標題列
                cell.font = Font(bold=True, color="FFFFFF")
                cell.fill = PatternFill(start_color="FF3333", end_color="FF3333", fill_type="solid")

    ws_syntax.column_dimensions['A'].width = 15
    ws_syntax.column_dimensions['B'].width = 35
    ws_syntax.column_dimensions['C'].width = 30

    # ========================================
    # 工作表 6: 常見錯誤與解決
    # ========================================
    ws_errors = wb.create_sheet("05_常見錯誤", 5)

    ws_errors['A1'] = "VBA 常見錯誤與解決方法"
    ws_errors['A1'].font = Font(size=14, bold=True, color="FFFFFF")
    ws_errors['A1'].fill = PatternFill(start_color="FFC000", end_color="FFC000", fill_type="solid")
    ws_errors['A1'].alignment = Alignment(horizontal='center')
    ws_errors.merge_cells('A1:C1')

    errors = [
        ["", "", ""],
        ["錯誤類型", "原因", "解決方法"],
        ["編譯錯誤：找不到 Sub 或 Function", "巨集名稱拼寫錯誤", "檢查巨集名稱拼寫"],
        ["執行階段錯誤 1004", "範圍無效", "檢查儲存格範圍是否正確"],
        ["執行階段錯誤 9", "找不到工作表", "確認工作表名稱正確"],
        ["執行階段錯誤 13", "類型不符", "檢查變數資料類型"],
        ["物件變數未設定", "沒有使用 Set 指派物件", "使用 Set 物件 = ..."],
        ["巨集無法執行", "巨集被停用", "啟用巨集：檔案→選項→信任中心"],
        ["代碼跑很慢", "頻繁更新畫面", "加上 ScreenUpdating = False"],
        ["", "", ""],
        ["偵錯技巧", "", ""],
        ["", "1. 使用 Debug.Print 輸出變數值到立即視窗", ""],
        ["", "2. 按 F8 逐行執行代碼", ""],
        ["", "3. 使用中斷點（點擊行號左側）", ""],
        ["", "4. 使用 On Error Resume Next 忽略錯誤", ""],
        ["", "5. 使用 On Error GoTo ErrorHandler 處理錯誤", ""],
    ]

    for i, row in enumerate(errors, start=2):
        for j, value in enumerate(row, start=1):
            cell = ws_errors.cell(row=i, column=j, value=value)
            if i == 3:  # 標題列
                cell.font = Font(bold=True, color="FFFFFF")
                cell.fill = PatternFill(start_color="FFC000", end_color="FFC000", fill_type="solid")
            elif "偵錯技巧" in str(value):
                cell.font = Font(bold=True, size=12)

    ws_errors.column_dimensions['A'].width = 30
    ws_errors.column_dimensions['B'].width = 30
    ws_errors.column_dimensions['C'].width = 30

    # 保存工作簿
    output_path = "Week2_VBA_Practice_Workbook.xlsx"
    wb.save(output_path)
    print(f"✅ 已創建：{output_path}")
    print(f"📊 包含 6 個工作表")
    print(f"📚 包含 50 筆測試資料")
    print(f"💡 包含 12 個 VBA 範例說明")

    return output_path

if __name__ == "__main__":
    create_vba_practice_workbook()
