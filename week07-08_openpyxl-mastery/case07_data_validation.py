"""
案例7：資料驗證
功能：
1. 下拉列表驗證
2. 數值範圍驗證
3. 日期範圍驗證
4. 自訂驗證公式
5. 錯誤提示設定

Author: Week 7-8 openpyxl 完全掌握
Date: 2024-12-11
"""

import pandas as pd
from openpyxl import Workbook
from openpyxl.styles import Font, PatternFill, Alignment, Border, Side
from openpyxl.worksheet.datavalidation import DataValidation
from openpyxl.utils import get_column_letter
import sys
from pathlib import Path
import warnings

warnings.filterwarnings('ignore')

# 新增父路徑到 sys.path
sys.path.insert(0, str(Path(__file__).parent.parent / 'week03-06_pandas-advanced' / 'utils'))

from data_loader import load_olist_data


def create_data_validation_report():
    """
    建立資料驗證報告

    流程：
    1. 載入資料
    2. 建立 Excel 工作簿
    3. 設定各種驗證規則
    4. 添加提示和錯誤訊息
    """

    print("=" * 70)
    print("案例7：資料驗證")
    print("=" * 70)

    # 步驟1：載入資料
    print("\n[1/4] 載入 Olist 資料...")
    try:
        orders, order_items, products, customers, sellers, payments, reviews = load_olist_data(verbose=False)
    except Exception as e:
        print(f"資料載入失敗：{e}")
        return

    # 步驟2：建立 Excel 工作簿
    print("[2/4] 建立 Excel 工作簿...")
    wb = Workbook()
    ws = wb.active
    ws.title = '資料輸入'

    # 定義樣式
    header_font = Font(bold=True, color='FFFFFF', size=12)
    header_fill = PatternFill(start_color='1F4E78', end_color='1F4E78', fill_type='solid')
    header_alignment = Alignment(horizontal='center', vertical='center', wrap_text=True)

    border_style = Border(
        left=Side(style='thin', color='CCCCCC'),
        right=Side(style='thin', color='CCCCCC'),
        top=Side(style='thin', color='CCCCCC'),
        bottom=Side(style='thin', color='CCCCCC')
    )

    input_fill = PatternFill(start_color='FFFFCC', end_color='FFFFCC', fill_type='solid')

    # 標題
    ws['A1'] = '訂單資料輸入表單'
    ws.merge_cells('A1:G1')
    title_cell = ws['A1']
    title_cell.font = Font(bold=True, size=14, color='FFFFFF')
    title_cell.fill = header_fill
    title_cell.alignment = Alignment(horizontal='center', vertical='center')
    ws.row_dimensions[1].height = 25

    # 步驟3：設定驗證規則
    print("[3/4] 設定驗證規則...")

    # 欄位定義
    headers = ['訂單ID', '客戶ID', '訂單日期', '產品類別', '銷售金額', '付款方式', '備註']

    for col_idx, header in enumerate(headers, start=1):
        cell = ws.cell(row=3, column=col_idx, value=header)
        cell.font = header_font
        cell.fill = header_fill
        cell.alignment = header_alignment
        cell.border = border_style

    # 設定可用的類別
    categories = products['product_category_name'].unique()[:20]
    category_list = ','.join(categories)

    # 設定可用的付款方式
    payment_types = payments['payment_type'].unique()
    payment_list = ','.join(payment_types)

    # 驗證規則1：訂單ID - 文字且必填
    dv_order_id = DataValidation(
        type='textLength',
        operator='greaterThan',
        formula1='0',
        allow_blank=False
    )
    dv_order_id.error = '訂單ID不能為空'
    dv_order_id.errorTitle = '輸入錯誤'
    dv_order_id.prompt = '請輸入訂單ID'
    dv_order_id.promptTitle = '訂單ID'
    ws.add_data_validation(dv_order_id)
    dv_order_id.add(f'A4:A1000')

    # 驗證規則2：客戶ID - 文字且必填
    dv_customer_id = DataValidation(
        type='textLength',
        operator='greaterThan',
        formula1='0',
        allow_blank=False
    )
    dv_customer_id.error = '客戶ID不能為空'
    dv_customer_id.errorTitle = '輸入錯誤'
    dv_customer_id.prompt = '請輸入客戶ID'
    dv_customer_id.promptTitle = '客戶ID'
    ws.add_data_validation(dv_customer_id)
    dv_customer_id.add(f'B4:B1000')

    # 驗證規則3：訂單日期 - 日期驗證
    dv_date = DataValidation(
        type='date',
        operator='between',
        formula1='2023-01-01',
        formula2='2024-12-31',
        allow_blank=False
    )
    dv_date.error = '日期必須在 2023-01-01 到 2024-12-31 之間'
    dv_date.errorTitle = '日期範圍錯誤'
    dv_date.prompt = '輸入日期格式：YYYY-MM-DD'
    dv_date.promptTitle = '訂單日期'
    ws.add_data_validation(dv_date)
    dv_date.add(f'C4:C1000')

    # 驗證規則4：產品類別 - 下拉列表
    dv_category = DataValidation(
        type='list',
        formula1=f'"{category_list}"',
        allow_blank=False
    )
    dv_category.error = '請選擇有效的產品類別'
    dv_category.errorTitle = '類別選擇錯誤'
    dv_category.prompt = '點擊下拉箭頭選擇產品類別'
    dv_category.promptTitle = '產品類別'
    ws.add_data_validation(dv_category)
    dv_category.add(f'D4:D1000')

    # 驗證規則5：銷售金額 - 數值範圍（0-10000）
    dv_amount = DataValidation(
        type='decimal',
        operator='between',
        formula1='0',
        formula2='10000',
        allow_blank=False
    )
    dv_amount.error = '銷售金額必須在 0 到 10000 之間'
    dv_amount.errorTitle = '金額範圍錯誤'
    dv_amount.prompt = '輸入銷售金額（0-10000）'
    dv_amount.promptTitle = '銷售金額'
    ws.add_data_validation(dv_amount)
    dv_amount.add(f'E4:E1000')

    # 驗證規則6：付款方式 - 下拉列表
    dv_payment = DataValidation(
        type='list',
        formula1=f'"{payment_list}"',
        allow_blank=False
    )
    dv_payment.error = '請選擇有效的付款方式'
    dv_payment.errorTitle = '付款方式選擇錯誤'
    dv_payment.prompt = '點擊下拉箭頭選擇付款方式'
    dv_payment.promptTitle = '付款方式'
    ws.add_data_validation(dv_payment)
    dv_payment.add(f'F4:F1000')

    # 驗證規則7：備註 - 文字長度限制
    dv_notes = DataValidation(
        type='textLength',
        operator='lessThanOrEqual',
        formula1='200'
    )
    dv_notes.prompt = '最多200個字'
    dv_notes.promptTitle = '備註'
    ws.add_data_validation(dv_notes)
    dv_notes.add(f'G4:G1000')

    # 步驟4：添加範例資料和樣式
    print("[4/4] 添加範例資料...")

    # 添加範例列（用戶可以參考）
    sample_data = [
        ['ORD001', 'CUST001', '2024-06-15', categories[0], 500, payment_types[0], '首次購買'],
        ['ORD002', 'CUST002', '2024-07-20', categories[1], 1500, payment_types[1], '大客戶訂單'],
    ]

    for row_idx, row_data in enumerate(sample_data, start=4):
        for col_idx, value in enumerate(row_data, start=1):
            cell = ws.cell(row=row_idx, column=col_idx, value=value)
            cell.border = border_style
            cell.fill = input_fill
            cell.alignment = Alignment(horizontal='left', vertical='center')

            # 設定數值格式
            if col_idx == 3:  # 日期
                cell.number_format = 'YYYY-MM-DD'
            elif col_idx == 5:  # 金額
                cell.number_format = '#,##0.00'

    # 設定空白輸入列的背景色
    for row in range(6, 20):
        for col in range(1, 8):
            cell = ws.cell(row=row, column=col)
            cell.fill = input_fill
            cell.border = border_style

    # 調整欄寬
    column_widths = [15, 15, 15, 20, 12, 12, 20]
    for col_idx, width in enumerate(column_widths, start=1):
        ws.column_dimensions[get_column_letter(col_idx)].width = width

    # 添加說明工作表
    print("\n[4/4] 添加驗證說明...")
    ws_help = wb.create_sheet('驗證說明', 1)

    help_data = [
        ['驗證欄位', '驗證類型', '驗證規則', '錯誤提示'],
        ['訂單ID', '文字', '必填', '訂單ID不能為空'],
        ['客戶ID', '文字', '必填', '客戶ID不能為空'],
        ['訂單日期', '日期', '2023-01-01 至 2024-12-31', '日期必須在指定範圍內'],
        ['產品類別', '下拉列表', f'20 個產品類別', '請選擇有效的產品類別'],
        ['銷售金額', '數值', '0 至 10000', '金額必須在 0 到 10000 之間'],
        ['付款方式', '下拉列表', f'{len(payment_types)} 種付款方式', '請選擇有效的付款方式'],
        ['備註', '文字', '最多 200 個字', '無'],
    ]

    for row_idx, row_data in enumerate(help_data, start=1):
        for col_idx, value in enumerate(row_data, start=1):
            cell = ws_help.cell(row=row_idx, column=col_idx, value=value)

            if row_idx == 1:
                cell.font = header_font
                cell.fill = header_fill
                cell.alignment = header_alignment
            else:
                cell.border = border_style
                cell.alignment = Alignment(horizontal='left', vertical='center')

    ws_help.column_dimensions['A'].width = 15
    ws_help.column_dimensions['B'].width = 15
    ws_help.column_dimensions['C'].width = 30
    ws_help.column_dimensions['D'].width = 30

    # 保存檔案
    output_file = '/home/justin/web-projects/excel-python-data-analysis/week07-08_openpyxl-mastery/case07_data_validation.xlsx'
    wb.save(output_file)

    # 輸出統計資訊
    print("\n" + "=" * 70)
    print("✅ 資料驗證報告已生成！")
    print("=" * 70)
    print(f"📊 檔案位置：{output_file}")
    print(f"📊 驗證規則：7 個")
    print(f"\n✓ 驗證規則說明：")
    print(f"  1. 訂單ID：文字必填")
    print(f"  2. 客戶ID：文字必填")
    print(f"  3. 訂單日期：日期範圍 (2023-01-01 至 2024-12-31)")
    print(f"  4. 產品類別：下拉列表選擇")
    print(f"  5. 銷售金額：數值範圍 (0-10000)")
    print(f"  6. 付款方式：下拉列表選擇")
    print(f"  7. 備註：文字長度限制 (≤200字)")
    print(f"\n✓ 特性說明：")
    print(f"  • 預設範例資料：可參考正確格式")
    print(f"  • 視覺化提示：黃色背景表示輸入區域")
    print(f"  • 自訂錯誤訊息：明確的驗證失敗提示")
    print(f"  • 驗證說明工作表：詳細的規則文檔")


if __name__ == "__main__":
    create_data_validation_report()
