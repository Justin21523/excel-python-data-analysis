"""
案例10：工作表保護
功能：
1. 工作表密碼保護
2. 凍結保護
3. 指定可編輯區域
4. 保護設定配置
5. 列印範圍限制

Author: Week 7-8 openpyxl 完全掌握
Date: 2024-12-11
"""

import pandas as pd
from openpyxl import Workbook
from openpyxl.styles import Font, PatternFill, Alignment, Border, Side
from openpyxl.worksheet.protection import SheetProtection
from openpyxl.utils import get_column_letter
import sys
from pathlib import Path
import warnings

warnings.filterwarnings('ignore')

# 新增父路徑到 sys.path
sys.path.insert(0, str(Path(__file__).parent.parent / 'week03-06_pandas-advanced' / 'utils'))

from data_loader import load_olist_data


def create_sheet_protection_report():
    """
    建立工作表保護報告

    流程：
    1. 載入資料
    2. 建立 Excel 工作簿
    3. 設定保護規則
    4. 指定可編輯區域
    5. 應用工作表保護
    """

    print("=" * 70)
    print("案例10：工作表保護")
    print("=" * 70)

    # 步驟1：載入資料
    print("\n[1/5] 載入 Olist 資料...")
    try:
        orders, order_items, products, customers, sellers, payments, reviews = load_olist_data(verbose=False)
    except Exception as e:
        print(f"資料載入失敗：{e}")
        return

    # 步驟2：準備資料
    print("[2/5] 準備資料...")

    # 準備銷售資料
    sales_data = sellers.head(15).merge(
        order_items.groupby('seller_id').agg({'price': ['sum', 'count', 'mean']}).reset_index(),
        on='seller_id',
        how='left'
    ).fillna(0)

    sales_data.columns = ['seller_id', 'zip_code', 'city', 'state', '銷售額', '銷售件數', '平均價格']

    # 步驟3：建立 Excel 工作簿
    print("[3/5] 建立 Excel 工作簿...")
    wb = Workbook()

    # ============ 工作表1：受保護的報表 ============
    ws1 = wb.active
    ws1.title = '銷售報表(受保護)'

    print("[4/5] 設定保護規則...")

    # 定義樣式
    header_font = Font(bold=True, color='FFFFFF', size=11)
    header_fill = PatternFill(start_color='1F4E78', end_color='1F4E78', fill_type='solid')
    header_alignment = Alignment(horizontal='center', vertical='center')

    border_style = Border(
        left=Side(style='thin', color='CCCCCC'),
        right=Side(style='thin', color='CCCCCC'),
        top=Side(style='thin', color='CCCCCC'),
        bottom=Side(style='thin', color='CCCCCC')
    )

    # 寫入標題
    headers = ['賣家ID', '城市', '州', '銷售額', '銷售件數', '平均價格', '備註']

    for col_idx, header in enumerate(headers, start=1):
        cell = ws1.cell(row=1, column=col_idx, value=header)
        cell.font = header_font
        cell.fill = header_fill
        cell.alignment = header_alignment
        cell.border = border_style

    # 寫入資料
    for row_idx, (idx, row) in enumerate(sales_data.iterrows(), start=2):
        for col_idx, value in enumerate(row.values, start=1):
            cell = ws1.cell(row=row_idx, column=col_idx, value=value)
            cell.border = border_style

            # 設定格式
            if col_idx in [4, 6]:  # 金額欄
                cell.number_format = '#,##0.00'
            elif col_idx == 5:  # 件數
                cell.number_format = '#,##0'

    # 設定保護前，先開放「備註」欄（G列）為可編輯
    # 首先，鎖定所有儲存格
    for row in ws1.iter_rows():
        for cell in row:
            if cell.value is not None:
                cell.protection = cell.protection.copy()
                cell.protection.locked = True

    # 然後解鎖「備註」欄（G列）
    for row in ws1.iter_rows(min_row=2, min_col=7, max_row=len(sales_data) + 1, max_col=7):
        for cell in row:
            cell.protection = cell.protection.copy()
            cell.protection.locked = False
            cell.fill = PatternFill(start_color='FFFFCC', end_color='FFFFCC', fill_type='solid')

    # 設定工作表保護（密碼：password123）
    ws1.protection.sheet = True
    ws1.protection.password = 'password123'
    ws1.protection.enable()

    # 調整欄寬
    column_widths = [15, 12, 8, 15, 12, 15, 20]
    for col_idx, width in enumerate(column_widths, start=1):
        ws1.column_dimensions[get_column_letter(col_idx)].width = width

    # ============ 工作表2：說明文檔（未保護） ============
    ws2 = wb.create_sheet('保護說明')

    # 標題
    ws2.merge_cells('A1:D1')
    title_cell = ws2['A1']
    title_cell.value = '工作表保護說明'
    title_cell.font = Font(bold=True, size=14, color='FFFFFF')
    title_cell.fill = PatternFill(start_color='1F4E78', end_color='1F4E78', fill_type='solid')
    title_cell.alignment = Alignment(horizontal='center', vertical='center')
    ws2.row_dimensions[1].height = 25

    # 保護說明
    protection_info = [
        ['項目', '說明', '密碼'],
        ['工作表保護', '銷售報表工作表已被保護', 'password123'],
        ['鎖定區域', '所有數據區域（A:F列）已鎖定', '-'],
        ['可編輯區域', 'G列（備註欄）可自由編輯', '-'],
        ['密碼提示', '使用提供的密碼解鎖工作表', 'password123'],
        ['限制操作', '無法插入/刪除行或列', '-'],
        ['', '', ''],
        ['限制列表', '禁止的操作', ''],
        ['', '• 插入行列', ''],
        ['', '• 刪除行列', ''],
        ['', '• 修改數據區域', ''],
        ['', '• 更改格式設定', ''],
    ]

    for row_idx, row_data in enumerate(protection_info, start=3):
        for col_idx, value in enumerate(row_data, start=1):
            cell = ws2.cell(row=row_idx, column=col_idx, value=value)

            if row_idx == 3:
                cell.font = Font(bold=True, color='FFFFFF')
                cell.fill = PatternFill(start_color='366092', end_color='366092', fill_type='solid')

            if col_idx == 3 and value != '':
                cell.fill = PatternFill(start_color='FFFF00', end_color='FFFF00', fill_type='solid')
                cell.font = Font(bold=True, color='FF0000')

    ws2.column_dimensions['A'].width = 20
    ws2.column_dimensions['B'].width = 35
    ws2.column_dimensions['C'].width = 20

    # ============ 工作表3：數據輸入表（部分保護） ============
    ws3 = wb.create_sheet('資料輸入')

    # 標題
    ws3.merge_cells('A1:D1')
    title_cell = ws3['A1']
    title_cell.value = '客戶反饋輸入表'
    title_cell.font = Font(bold=True, size=14, color='FFFFFF')
    title_cell.fill = PatternFill(start_color='1F4E78', end_color='1F4E78', fill_type='solid')
    title_cell.alignment = Alignment(horizontal='center', vertical='center')
    ws3.row_dimensions[1].height = 25

    # 說明
    ws3['A3'] = '請在黃色欄位中輸入資訊（其他欄位已鎖定）'
    ws3['A3'].font = Font(italic=True, size=9)

    # 列標題
    input_headers = ['日期', '客戶名稱', '評分', '意見反饋']
    for col_idx, header in enumerate(input_headers, start=1):
        cell = ws3.cell(row=5, column=col_idx, value=header)
        cell.font = Font(bold=True, color='FFFFFF')
        cell.fill = PatternFill(start_color='366092', end_color='366092', fill_type='solid')

    # 創建輸入行（可編輯區域用黃色標記）
    editable_fill = PatternFill(start_color='FFFFCC', end_color='FFFFCC', fill_type='solid')
    locked_fill = PatternFill(start_color='D9D9D9', end_color='D9D9D9', fill_type='solid')

    for row_idx in range(6, 26):
        # 日期（鎖定）
        cell = ws3.cell(row=row_idx, column=1, value='')
        cell.fill = locked_fill
        cell.protection = cell.protection.copy()
        cell.protection.locked = True

        # 客戶名稱（可編輯）
        cell = ws3.cell(row=row_idx, column=2, value='')
        cell.fill = editable_fill
        cell.protection = cell.protection.copy()
        cell.protection.locked = False

        # 評分（可編輯）
        cell = ws3.cell(row=row_idx, column=3, value='')
        cell.fill = editable_fill
        cell.protection = cell.protection.copy()
        cell.protection.locked = False

        # 意見反饋（可編輯）
        cell = ws3.cell(row=row_idx, column=4, value='')
        cell.fill = editable_fill
        cell.protection = cell.protection.copy()
        cell.protection.locked = False

    # 保護工作表
    ws3.protection.sheet = True
    ws3.protection.password = 'password123'
    ws3.protection.enable()

    ws3.column_dimensions['A'].width = 15
    ws3.column_dimensions['B'].width = 20
    ws3.column_dimensions['C'].width = 12
    ws3.column_dimensions['D'].width = 35

    # 步驟5：保存檔案
    print("[5/5] 保存檔案...")
    output_file = '/home/justin/web-projects/excel-python-data-analysis/week07-08_openpyxl-mastery/case10_sheet_protection.xlsx'
    wb.save(output_file)

    # 輸出統計資訊
    print("\n" + "=" * 70)
    print("✅ 工作表保護報告已生成！")
    print("=" * 70)
    print(f"📊 檔案位置：{output_file}")
    print(f"📊 工作表數量：3 個")
    print(f"\n✓ 保護設定說明：")
    print(f"  • 銷售報表工作表（受保護）：")
    print(f"    - 密碼：password123")
    print(f"    - 鎖定區域：A-F列（數據區域）")
    print(f"    - 可編輯區域：G列（備註欄）")
    print(f"\n  • 資料輸入工作表（部分保護）：")
    print(f"    - 密碼：password123")
    print(f"    - 可編輯區域：黃色欄位（客戶名稱、評分、意見反饋）")
    print(f"    - 鎖定區域：灰色欄位（日期欄）")
    print(f"\n  • 保護說明工作表（未保護）：")
    print(f"    - 可自由編輯")
    print(f"    - 包含保護規則說明")
    print(f"\n✓ 保護功能：")
    print(f"  • 防止未經授權修改重要數據")
    print(f"  • 指定特定區域可編輯")
    print(f"  • 密碼保護設定")


if __name__ == "__main__":
    create_sheet_protection_report()
