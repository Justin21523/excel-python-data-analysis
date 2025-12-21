"""
案例9：儲存格合併
功能：
1. 合併儲存格實作
2. 多層級標題
3. 複雜表格佈局
4. 分組統計區域
5. 對齐和邊框處理

Author: Week 7-8 openpyxl 完全掌握
Date: 2024-12-11
"""

import pandas as pd
from openpyxl import Workbook
from openpyxl.styles import Font, PatternFill, Alignment, Border, Side
from openpyxl.utils import get_column_letter
import sys
from pathlib import Path
import warnings

warnings.filterwarnings('ignore')

# 新增父路徑到 sys.path
sys.path.insert(0, str(Path(__file__).parent.parent / 'week03-06_pandas-advanced' / 'utils'))

from data_loader import load_olist_data


def create_cell_merging_report():
    """
    建立儲存格合併報告

    流程：
    1. 載入資料
    2. 準備分層結構資料
    3. 建立多層級標題
    4. 應用合併儲存格
    5. 設計複雜表格佈局
    """

    print("=" * 70)
    print("案例9：儲存格合併")
    print("=" * 70)

    # 步驟1：載入資料
    print("\n[1/4] 載入 Olist 資料...")
    try:
        orders, order_items, products, customers, sellers, payments, reviews = load_olist_data(verbose=False)
    except Exception as e:
        print(f"資料載入失敗：{e}")
        return

    # 步驟2：準備資料
    print("[2/4] 準備分層統計資料...")

    # 按州和類別統計
    df_summary = customers.merge(
        orders[['customer_id', 'order_id']],
        on='customer_id'
    ).merge(
        order_items[['order_id', 'product_id', 'price']],
        on='order_id'
    ).merge(
        products[['product_id', 'product_category_name']],
        on='product_id'
    )

    # 按州、類別分組統計
    df_grouped = df_summary.groupby(
        ['customer_state', 'product_category_name']
    ).agg({
        'price': ['sum', 'count', 'mean']
    }).reset_index()

    df_grouped.columns = ['州', '類別', '銷售額', '銷售件數', '平均價格']
    df_grouped = df_grouped.sort_values(['州', '銷售額'], ascending=[True, False])

    # 步驟3：建立 Excel 工作簿
    print("[3/4] 建立 Excel 工作簿...")
    wb = Workbook()
    ws = wb.active
    ws.title = '分層統計'

    # 定義樣式
    main_header_font = Font(bold=True, size=14, color='FFFFFF')
    main_header_fill = PatternFill(start_color='1F4E78', end_color='1F4E78', fill_type='solid')

    group_header_font = Font(bold=True, size=11, color='FFFFFF')
    group_header_fill = PatternFill(start_color='366092', end_color='366092', fill_type='solid')

    sub_header_font = Font(bold=True, size=10, color='FFFFFF')
    sub_header_fill = PatternFill(start_color='4472C4', end_color='4472C4', fill_type='solid')

    border_style = Border(
        left=Side(style='thin', color='000000'),
        right=Side(style='thin', color='000000'),
        top=Side(style='thin', color='000000'),
        bottom=Side(style='thin', color='000000')
    )

    light_fill = PatternFill(start_color='E7E6E6', end_color='E7E6E6', fill_type='solid')

    # 步驟4：設計複雜表格佈局
    print("[4/4] 設計複雜表格佈局...")

    # 主標題（合併多列）
    ws.merge_cells('A1:E1')
    title_cell = ws['A1']
    title_cell.value = '地區與產品類別銷售分析'
    title_cell.font = main_header_font
    title_cell.fill = main_header_fill
    title_cell.alignment = Alignment(horizontal='center', vertical='center')
    ws.row_dimensions[1].height = 30

    # 副標題
    ws.merge_cells('A2:E2')
    subtitle_cell = ws['A2']
    subtitle_cell.value = '按州別和產品類別分層統計'
    subtitle_cell.font = Font(size=10, italic=True)
    ws.row_dimensions[2].height = 20

    # 列標題（多層級）
    # 第一層：主分類
    ws.merge_cells('A4:A5')
    cell = ws['A4']
    cell.value = '州'
    cell.font = sub_header_font
    cell.fill = sub_header_fill
    cell.alignment = Alignment(horizontal='center', vertical='center', wrap_text=True)
    cell.border = border_style

    ws.merge_cells('B4:B5')
    cell = ws['B4']
    cell.value = '類別'
    cell.font = sub_header_font
    cell.fill = sub_header_fill
    cell.alignment = Alignment(horizontal='center', vertical='center', wrap_text=True)
    cell.border = border_style

    # 第二層：銷售額、件數、價格
    ws.merge_cells('C4:E4')
    cell = ws['C4']
    cell.value = '銷售指標'
    cell.font = sub_header_font
    cell.fill = sub_header_fill
    cell.alignment = Alignment(horizontal='center', vertical='center')
    cell.border = border_style
    ws.row_dimensions[4].height = 18

    # 細項標題
    for col_idx, header in enumerate(['銷售額', '銷售件數', '平均價格'], start=3):
        cell = ws.cell(row=5, column=col_idx, value=header)
        cell.font = sub_header_font
        cell.fill = sub_header_fill
        cell.alignment = Alignment(horizontal='center', vertical='center')
        cell.border = border_style
    ws.row_dimensions[5].height = 18

    # 填充資料，按州分組
    current_row = 6
    prev_state = None
    state_start_row = 6

    for idx, row_data in df_grouped.iterrows():
        state = row_data['州']
        category = row_data['類別']
        sales = row_data['銷售額']
        count = row_data['銷售件數']
        avg_price = row_data['平均價格']

        # 新的州，需要合併
        if state != prev_state:
            if prev_state is not None:
                # 合併前一個州的儲存格
                if current_row - 1 > state_start_row:
                    ws.merge_cells(f'A{state_start_row}:A{current_row - 1}')
                    merged_cell = ws.cell(row=state_start_row, column=1)
                    merged_cell.value = prev_state
                    merged_cell.font = Font(bold=True, size=10)
                    merged_cell.fill = light_fill
                    merged_cell.alignment = Alignment(
                        horizontal='center',
                        vertical='center',
                        wrap_text=True
                    )
                    merged_cell.border = border_style

            prev_state = state
            state_start_row = current_row

        # 類別列
        cell_category = ws.cell(row=current_row, column=2, value=category)
        cell_category.border = border_style
        cell_category.alignment = Alignment(horizontal='left', vertical='center')

        # 銷售額
        cell_sales = ws.cell(row=current_row, column=3, value=sales)
        cell_sales.number_format = '#,##0.00'
        cell_sales.border = border_style
        cell_sales.alignment = Alignment(horizontal='right', vertical='center')

        # 銷售件數
        cell_count = ws.cell(row=current_row, column=4, value=int(count))
        cell_count.number_format = '#,##0'
        cell_count.border = border_style
        cell_count.alignment = Alignment(horizontal='right', vertical='center')

        # 平均價格
        cell_avg = ws.cell(row=current_row, column=5, value=avg_price)
        cell_avg.number_format = '#,##0.00'
        cell_avg.border = border_style
        cell_avg.alignment = Alignment(horizontal='right', vertical='center')

        current_row += 1

    # 合併最後一個州
    if current_row - 1 > state_start_row:
        ws.merge_cells(f'A{state_start_row}:A{current_row - 1}')
        merged_cell = ws.cell(row=state_start_row, column=1)
        merged_cell.value = prev_state
        merged_cell.font = Font(bold=True, size=10)
        merged_cell.fill = light_fill
        merged_cell.alignment = Alignment(
            horizontal='center',
            vertical='center',
            wrap_text=True
        )
        merged_cell.border = border_style

    # 添加統計總計行
    total_row = current_row + 1

    ws.merge_cells(f'A{total_row}:B{total_row}')
    cell_total_label = ws.cell(row=total_row, column=1, value='統計總計')
    cell_total_label.font = Font(bold=True, color='FFFFFF')
    cell_total_label.fill = group_header_fill
    cell_total_label.alignment = Alignment(horizontal='center', vertical='center')
    cell_total_label.border = border_style

    # 總銷售額
    cell_total_sales = ws.cell(row=total_row, column=3, value=df_grouped['銷售額'].sum())
    cell_total_sales.number_format = '#,##0.00'
    cell_total_sales.font = Font(bold=True, color='FFFFFF')
    cell_total_sales.fill = group_header_fill
    cell_total_sales.alignment = Alignment(horizontal='right', vertical='center')
    cell_total_sales.border = border_style

    # 總件數
    cell_total_count = ws.cell(row=total_row, column=4, value=int(df_grouped['銷售件數'].sum()))
    cell_total_count.number_format = '#,##0'
    cell_total_count.font = Font(bold=True, color='FFFFFF')
    cell_total_count.fill = group_header_fill
    cell_total_count.alignment = Alignment(horizontal='right', vertical='center')
    cell_total_count.border = border_style

    # 平均價格
    cell_total_avg = ws.cell(row=total_row, column=5, value=df_grouped['平均價格'].mean())
    cell_total_avg.number_format = '#,##0.00'
    cell_total_avg.font = Font(bold=True, color='FFFFFF')
    cell_total_avg.fill = group_header_fill
    cell_total_avg.alignment = Alignment(horizontal='right', vertical='center')
    cell_total_avg.border = border_style

    # 調整欄寬
    ws.column_dimensions['A'].width = 12
    ws.column_dimensions['B'].width = 20
    ws.column_dimensions['C'].width = 15
    ws.column_dimensions['D'].width = 15
    ws.column_dimensions['E'].width = 15

    # 保存檔案
    output_file = '/home/justin/web-projects/excel-python-data-analysis/week07-08_openpyxl-mastery/case09_cell_merging.xlsx'
    wb.save(output_file)

    # 輸出統計資訊
    print("\n" + "=" * 70)
    print("✅ 儲存格合併報告已生成！")
    print("=" * 70)
    print(f"📊 檔案位置：{output_file}")
    print(f"📊 資料筆數：{len(df_grouped)} 個類別")
    print(f"📊 州數：{df_grouped['州'].nunique()} 個")
    print(f"\n✓ 合併儲存格應用：")
    print(f"  • 主標題：合併 A1:E1")
    print(f"  • 副標題：合併 A2:E2")
    print(f"  • 列標題：多層級合併（A4:A5, B4:B5, C4:E4）")
    print(f"  • 州分組：垂直合併州別欄")
    print(f"  • 統計總計：合併 A{total_row}:B{total_row}")
    print(f"\n✓ 複雜佈局特性：")
    print(f"  • 多層級標題結構")
    print(f"  • 分組統計區域")
    print(f"  • 垂直和水平合併結合")
    print(f"  • 彩色編碼層級區分")
    print(f"  • 統計總計行")


if __name__ == "__main__":
    create_cell_merging_report()
