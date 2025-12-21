"""
案例11：超連結和註解
功能：
1. 工作表間超連結
2. 外部超連結
3. 儲存格註解
4. 註解格式化
5. 導航目錄

Author: Week 7-8 openpyxl 完全掌握
Date: 2024-12-11
"""

import pandas as pd
from openpyxl import Workbook
from openpyxl.styles import Font, PatternFill, Alignment, Border, Side
from openpyxl.comments import Comment
from openpyxl.utils import get_column_letter
import sys
from pathlib import Path
import warnings

warnings.filterwarnings('ignore')

# 新增父路徑到 sys.path
sys.path.insert(0, str(Path(__file__).parent.parent / 'week03-06_pandas-advanced' / 'utils'))

from data_loader import load_olist_data


def create_hyperlinks_comments_report():
    """
    建立超連結和註解報告

    流程：
    1. 載入資料
    2. 建立導航目錄工作表
    3. 添加工作表間超連結
    4. 添加外部超連結
    5. 添加詳細的儲存格註解
    """

    print("=" * 70)
    print("案例11：超連結和註解")
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

    # 準備各工作表資料
    sales_summary = products.merge(
        order_items[['product_id', 'price']],
        on='product_id'
    ).groupby('product_category_name').agg({
        'price': ['sum', 'count']
    }).reset_index().head(10)

    sales_summary.columns = ['類別', '銷售額', '銷售件數']

    customer_summary = customers.merge(
        orders[['customer_id', 'order_id']],
        on='customer_id'
    ).merge(
        order_items[['order_id', 'price']],
        on='order_id'
    ).groupby('customer_state').agg({
        'customer_id': 'nunique',
        'price': 'sum'
    }).reset_index().head(10)

    customer_summary.columns = ['州', '客戶數', '銷售額']

    # 步驟3：建立 Excel 工作簿
    print("[3/5] 建立 Excel 工作簿...")
    wb = Workbook()
    wb.remove(wb.active)

    # 定義樣式
    title_font = Font(bold=True, size=14, color='FFFFFF')
    title_fill = PatternFill(start_color='1F4E78', end_color='1F4E78', fill_type='solid')
    title_alignment = Alignment(horizontal='center', vertical='center')

    header_font = Font(bold=True, color='FFFFFF', size=11)
    header_fill = PatternFill(start_color='366092', end_color='366092', fill_type='solid')
    header_alignment = Alignment(horizontal='center', vertical='center')

    border_style = Border(
        left=Side(style='thin', color='CCCCCC'),
        right=Side(style='thin', color='CCCCCC'),
        top=Side(style='thin', color='CCCCCC'),
        bottom=Side(style='thin', color='CCCCCC')
    )

    link_font = Font(underline='single', color='0563C1')

    # 步驟4：建立導航目錄工作表
    print("[4/5] 建立導航目錄...")

    ws_index = wb.create_sheet('目錄')

    # 標題
    ws_index.merge_cells('A1:D1')
    title_cell = ws_index['A1']
    title_cell.value = '📊 報告導航目錄'
    title_cell.font = title_font
    title_cell.fill = title_fill
    title_cell.alignment = title_alignment
    ws_index.row_dimensions[1].height = 30

    # 說明
    ws_index['A3'] = '點擊下方連結跳轉到對應報告'
    ws_index['A3'].font = Font(italic=True)

    # 導航列表
    nav_items = [
        ('銷售報告', '銷售分析', 'A1'),
        ('客戶報告', '客戶分析', 'A1'),
        ('資料說明', '資料定義', 'A1'),
    ]

    current_row = 5
    for sheet_name, display_name, cell_ref in nav_items:
        # 項目名稱
        cell = ws_index.cell(row=current_row, column=1, value=display_name)
        cell.font = Font(bold=True, size=11)
        cell.border = border_style

        # 超連結
        link_cell = ws_index.cell(row=current_row, column=2, value='點擊進入')
        link_cell.font = link_font
        link_cell.alignment = Alignment(horizontal='center', vertical='center')
        link_cell.border = border_style

        # 添加超連結（指向特定工作表）
        link_cell.hyperlink = f'#{sheet_name}!{cell_ref}'

        # 添加註解（滑鼠懸停顯示）
        comment = Comment(f'跳轉到 {sheet_name} 工作表', 'Admin')
        comment.width = 250
        comment.height = 60
        link_cell.comment = comment

        current_row += 1

    # 添加外部連結示例
    current_row += 1
    ws_index.cell(row=current_row, column=1, value='外部資源').font = Font(bold=True)

    current_row += 1
    external_link_cell = ws_index.cell(row=current_row, column=2, value='Olist 官方網站')
    external_link_cell.font = link_font
    external_link_cell.hyperlink = 'https://www.olist.com'
    external_link_cell.border = border_style

    comment = Comment('打開 Olist 官方網站', 'Admin')
    external_link_cell.comment = comment

    ws_index.column_dimensions['A'].width = 20
    ws_index.column_dimensions['B'].width = 25

    # 步驟5：建立工作表和添加註解
    print("[5/5] 建立工作表和添加註解...")

    # ============ 銷售分析工作表 ============
    ws_sales = wb.create_sheet('銷售分析')

    # 標題
    ws_sales.merge_cells('A1:D1')
    title_cell = ws_sales['A1']
    title_cell.value = '銷售分析報告'
    title_cell.font = title_font
    title_cell.fill = title_fill
    title_cell.alignment = title_alignment
    ws_sales.row_dimensions[1].height = 25

    # 返回導航
    back_link = ws_sales['A3']
    back_link.value = '← 返回目錄'
    back_link.font = link_font
    back_link.hyperlink = '#目錄!A1'

    # 列標題
    headers = ['類別', '銷售額', '銷售件數', '平均價格']
    for col_idx, header in enumerate(headers, start=1):
        cell = ws_sales.cell(row=5, column=col_idx, value=header)
        cell.font = header_font
        cell.fill = header_fill
        cell.alignment = header_alignment
        cell.border = border_style

    # 添加欄位說明註解
    comment_category = Comment('產品的分類名稱', 'Data Team')
    comment_category.width = 250
    comment_category.height = 60
    ws_sales.cell(row=5, column=1).comment = comment_category

    comment_sales = Comment('該類別的總銷售額\n計算公式：各件銷售價格之和', 'Finance')
    comment_sales.width = 250
    comment_sales.height = 80
    ws_sales.cell(row=5, column=2).comment = comment_sales

    comment_count = Comment('該類別的總銷售件數', 'Sales')
    ws_sales.cell(row=5, column=3).comment = comment_count

    # 寫入資料
    for row_idx, (idx, row) in enumerate(sales_summary.iterrows(), start=6):
        for col_idx, value in enumerate(row.values, start=1):
            cell = ws_sales.cell(row=row_idx, column=col_idx, value=value)
            cell.border = border_style

            if col_idx in [2, 4]:
                cell.number_format = '#,##0.00'
            elif col_idx == 3:
                cell.number_format = '#,##0'

        # 為特殊資料行添加註解
        if row_idx == 6:  # 第一行
            comment = Comment(f'最高銷售額的類別', 'System')
            ws_sales.cell(row=row_idx, column=2).comment = comment

    ws_sales.column_dimensions['A'].width = 20
    ws_sales.column_dimensions['B'].width = 15
    ws_sales.column_dimensions['C'].width = 15
    ws_sales.column_dimensions['D'].width = 15

    # ============ 客戶分析工作表 ============
    ws_customer = wb.create_sheet('客戶分析')

    # 標題
    ws_customer.merge_cells('A1:D1')
    title_cell = ws_customer['A1']
    title_cell.value = '客戶分析報告'
    title_cell.font = title_font
    title_cell.fill = title_fill
    title_cell.alignment = title_alignment
    ws_customer.row_dimensions[1].height = 25

    # 返回導航
    back_link = ws_customer['A3']
    back_link.value = '← 返回目錄'
    back_link.font = link_font
    back_link.hyperlink = '#目錄!A1'

    # 列標題
    headers = ['州', '客戶數', '銷售額']
    for col_idx, header in enumerate(headers, start=1):
        cell = ws_customer.cell(row=5, column=col_idx, value=header)
        cell.font = header_font
        cell.fill = header_fill
        cell.alignment = header_alignment
        cell.border = border_style

    # 添加列說明註解
    comment_state = Comment('巴西州代碼\n例：SP、RJ、MG等', 'Geo Team')
    comment_state.width = 250
    comment_state.height = 80
    ws_customer.cell(row=5, column=1).comment = comment_state

    comment_customers = Comment('該州的客戶總數', 'CRM')
    ws_customer.cell(row=5, column=2).comment = comment_customers

    # 寫入資料
    for row_idx, (idx, row) in enumerate(customer_summary.iterrows(), start=6):
        for col_idx, value in enumerate(row.values, start=1):
            cell = ws_customer.cell(row=row_idx, column=col_idx, value=value)
            cell.border = border_style

            if col_idx == 3:
                cell.number_format = '#,##0.00'
            elif col_idx == 2:
                cell.number_format = '#,##0'

    ws_customer.column_dimensions['A'].width = 12
    ws_customer.column_dimensions['B'].width = 15
    ws_customer.column_dimensions['C'].width = 15

    # ============ 資料定義工作表 ============
    ws_definition = wb.create_sheet('資料定義')

    # 標題
    ws_definition.merge_cells('A1:C1')
    title_cell = ws_definition['A1']
    title_cell.value = '資料定義'
    title_cell.font = title_font
    title_cell.fill = title_fill
    title_cell.alignment = title_alignment
    ws_definition.row_dimensions[1].height = 25

    # 返回導航
    back_link = ws_definition['A3']
    back_link.value = '← 返回目錄'
    back_link.font = link_font
    back_link.hyperlink = '#目錄!A1'

    # 列標題
    headers = ['欄位名稱', '資料類型', '說明']
    for col_idx, header in enumerate(headers, start=1):
        cell = ws_definition.cell(row=5, column=col_idx, value=header)
        cell.font = header_font
        cell.fill = header_fill
        cell.alignment = header_alignment
        cell.border = border_style

    # 資料定義
    definitions = [
        ['類別', 'String', '產品的分類名稱'],
        ['銷售額', 'Decimal', '該類別/州的總銷售額（巴西雷亞爾）'],
        ['銷售件數', 'Integer', '該類別/州的銷售商品件數'],
        ['平均價格', 'Decimal', '該類別的平均商品價格'],
        ['客戶數', 'Integer', '該州的客戶總數'],
    ]

    for row_idx, definition in enumerate(definitions, start=6):
        for col_idx, value in enumerate(definition, start=1):
            cell = ws_definition.cell(row=row_idx, column=col_idx, value=value)
            cell.border = border_style

    ws_definition.column_dimensions['A'].width = 15
    ws_definition.column_dimensions['B'].width = 15
    ws_definition.column_dimensions['C'].width = 40

    # 保存檔案
    output_file = '/home/justin/web-projects/excel-python-data-analysis/week07-08_openpyxl-mastery/case11_hyperlinks_comments.xlsx'
    wb.save(output_file)

    # 輸出統計資訊
    print("\n" + "=" * 70)
    print("✅ 超連結和註解報告已生成！")
    print("=" * 70)
    print(f"📊 檔案位置：{output_file}")
    print(f"📊 工作表數量：4 個")
    print(f"\n✓ 超連結應用：")
    print(f"  • 內部超連結：目錄 → 各工作表")
    print(f"  • 返回超連結：各工作表 → 目錄")
    print(f"  • 外部超連結：Olist 官方網站")
    print(f"\n✓ 註解應用：")
    print(f"  • 欄位說明註解：解釋每一欄的含義")
    print(f"  • 計算說明註解：說明數值的計算方式")
    print(f"  • 資料源註解：標註特殊資料行")
    print(f"  • 導航提示註解：超連結功能說明")
    print(f"\n✓ 互動功能：")
    print(f"  • 點擊超連結快速導航")
    print(f"  • 滑鼠懸停查看詳細說明")
    print(f"  • 提高報表可讀性和易用性")


if __name__ == "__main__":
    create_hyperlinks_comments_report()
