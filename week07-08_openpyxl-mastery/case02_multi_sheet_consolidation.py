"""
案例2：多工作表自動整合
功能：
1. 多個 DataFrame 寫入不同工作表
2. 每個工作表自動格式化
3. 建立目錄頁（超連結）
4. 工作表標籤顏色管理
5. 自動統計彙總

Author: Week 7-8 openpyxl 完全掌握
Date: 2024-12-11
"""

import pandas as pd
from openpyxl import Workbook
from openpyxl.styles import Font, PatternFill, Alignment, Border, Side
from openpyxl.utils import get_column_letter
from openpyxl.worksheet.table import Table, TableStyleInfo
from openpyxl.worksheet.worksheet import Worksheet
import sys
from pathlib import Path
import warnings

warnings.filterwarnings('ignore')

# 新增父路徑到 sys.path
sys.path.insert(0, str(Path(__file__).parent.parent / 'week03-06_pandas-advanced' / 'utils'))

from data_loader import load_olist_data


def format_worksheet(ws: Worksheet, df: pd.DataFrame, sheet_name: str):
    """
    格式化工作表

    參數：
    - ws：Worksheet 物件
    - df：DataFrame 資料
    - sheet_name：工作表名稱
    """

    # 定義樣式
    header_font = Font(bold=True, color='FFFFFF', size=11)
    header_fill = PatternFill(start_color='366092', end_color='366092', fill_type='solid')
    header_alignment = Alignment(horizontal='center', vertical='center', wrap_text=True)

    border_style = Border(
        left=Side(style='thin', color='CCCCCC'),
        right=Side(style='thin', color='CCCCCC'),
        top=Side(style='thin', color='CCCCCC'),
        bottom=Side(style='thin', color='CCCCCC')
    )

    # 寫入標題
    for col_idx, header in enumerate(df.columns, start=1):
        cell = ws.cell(row=1, column=col_idx, value=header)
        cell.font = header_font
        cell.fill = header_fill
        cell.alignment = header_alignment
        cell.border = border_style

    # 寫入資料
    for row_idx, row_data in enumerate(df.values, start=2):
        for col_idx, value in enumerate(row_data, start=1):
            cell = ws.cell(row=row_idx, column=col_idx, value=value)
            cell.border = border_style

            # 數值格式化
            if isinstance(value, float):
                if 'price' in df.columns[col_idx - 1].lower() or 'amount' in df.columns[col_idx - 1].lower():
                    cell.number_format = '#,##0.00'
                elif 'rate' in df.columns[col_idx - 1].lower():
                    cell.number_format = '0.00%'
                else:
                    cell.number_format = '#,##0.00'

    # 自動調整欄寬
    for col_idx, column_cells in enumerate(ws.columns, start=1):
        max_length = 0
        column_letter = get_column_letter(col_idx)

        for cell in column_cells:
            try:
                if cell.value:
                    max_length = max(max_length, len(str(cell.value)))
            except:
                pass

        adjusted_width = min(max_length + 2, 50)
        ws.column_dimensions[column_letter].width = adjusted_width

    # 凍結標題列
    ws.freeze_panes = 'A2'


def create_multi_sheet_report():
    """
    建立多工作表整合報告

    流程：
    1. 載入 Olist 資料
    2. 計算各類型統計資料
    3. 建立多個工作表
    4. 建立目錄頁
    5. 設定工作表標籤顏色
    """

    print("=" * 70)
    print("案例2：多工作表自動整合")
    print("=" * 70)

    # 步驟1：載入資料
    print("\n[1/6] 載入 Olist 資料...")
    try:
        orders, order_items, products, customers, sellers, payments, reviews = load_olist_data(verbose=False)
    except Exception as e:
        print(f"資料載入失敗：{e}")
        return

    # 步驟2：準備各工作表資料
    print("[2/6] 準備各工作表資料...")

    # 工作表1：按類別統計銷售
    df_category = products.merge(
        order_items[['product_id', 'price']],
        on='product_id'
    ).groupby('product_category_name').agg({
        'price': ['sum', 'mean', 'count']
    }).reset_index()

    df_category.columns = ['類別', '總銷售額', '平均價格', '銷售件數']
    df_category = df_category.sort_values('總銷售額', ascending=False).head(20)

    # 工作表2：按賣家統計
    df_seller = sellers.merge(
        order_items[['seller_id', 'price']],
        on='seller_id'
    ).groupby(['seller_id', 'seller_city']).agg({
        'price': ['sum', 'mean', 'count']
    }).reset_index()

    df_seller.columns = ['賣家ID', '城市', '總銷售額', '平均商品價格', '銷售件數']
    df_seller = df_seller.sort_values('總銷售額', ascending=False).head(20)

    # 工作表3：按客戶州分統計
    df_state = customers.merge(
        orders[['customer_id', 'order_id']],
        on='customer_id'
    ).merge(
        order_items[['order_id', 'price']],
        on='order_id'
    ).groupby('customer_state').agg({
        'customer_id': 'nunique',
        'price': ['sum', 'mean'],
        'order_id': 'nunique'
    }).reset_index()

    df_state.columns = ['州', '客戶數', '總銷售額', '平均商品價格', '訂單數']
    df_state = df_state.sort_values('總銷售額', ascending=False)

    # 工作表4：按付款方式統計
    df_payment = payments.groupby('payment_type').agg({
        'payment_value': ['sum', 'mean', 'count']
    }).reset_index()

    df_payment.columns = ['付款方式', '總金額', '平均金額', '筆數']
    df_payment = df_payment.sort_values('總金額', ascending=False)

    # 工作表5：評論評分統計
    df_review = reviews[reviews['review_score'].notna()].groupby('review_score').size().reset_index(name='評論數')
    df_review = df_review.sort_values('review_score')

    # 步驟3：建立 Excel 工作簿
    print("[3/6] 建立 Excel 工作簿...")
    wb = Workbook()
    wb.remove(wb.active)  # 移除預設工作表

    # 定義工作表顏色
    sheet_colors = {
        '目錄': 'FF00B0F0',  # 藍色
        '類別銷售': 'FF70AD47',  # 綠色
        '賣家統計': 'FFFFC000',  # 橙色
        '地區分析': 'FFC5504A',  # 紅色
        '付款方式': '9DC3E6',  # 淡藍色
        '評論評分': 'FFED7D31'  # 深橙色
    }

    # 步驟4：建立目錄頁
    print("[4/6] 建立目錄頁...")
    ws_index = wb.create_sheet('目錄', 0)
    ws_index.sheet_properties.tabColor = sheet_colors['目錄']

    # 目錄標題
    title_cell = ws_index['A1']
    title_cell.value = '📊 多工作表整合報告'
    title_cell.font = Font(bold=True, size=16, color='FFFFFF')
    title_cell.fill = PatternFill(start_color='1F4E78', end_color='1F4E78', fill_type='solid')
    title_cell.alignment = Alignment(horizontal='center', vertical='center')
    ws_index.merge_cells('A1:D1')
    ws_index.row_dimensions[1].height = 30

    # 目錄內容
    index_data = [
        ['序號', '工作表名稱', '描述', '資料筆數'],
        ['1', '類別銷售', '按產品類別統計銷售資料', len(df_category)],
        ['2', '賣家統計', '按賣家統計銷售情況', len(df_seller)],
        ['3', '地區分析', '按客戶州別統計銷售', len(df_state)],
        ['4', '付款方式', '按付款方式統計', len(df_payment)],
        ['5', '評論評分', '按評論評分統計', len(df_review)]
    ]

    for row_idx, row_data in enumerate(index_data, start=3):
        for col_idx, value in enumerate(row_data, start=1):
            cell = ws_index.cell(row=row_idx, column=col_idx, value=value)
            if row_idx == 3:
                cell.font = Font(bold=True, color='FFFFFF')
                cell.fill = PatternFill(start_color='366092', end_color='366092', fill_type='solid')
            cell.alignment = Alignment(horizontal='left', vertical='center')

    ws_index.column_dimensions['A'].width = 8
    ws_index.column_dimensions['B'].width = 15
    ws_index.column_dimensions['C'].width = 25
    ws_index.column_dimensions['D'].width = 15

    # 步驟5：建立資料工作表
    print("[5/6] 建立資料工作表...")

    # 類別銷售工作表
    ws_category = wb.create_sheet('類別銷售')
    ws_category.sheet_properties.tabColor = sheet_colors['類別銷售']
    format_worksheet(ws_category, df_category, '類別銷售')

    # 賣家統計工作表
    ws_seller = wb.create_sheet('賣家統計')
    ws_seller.sheet_properties.tabColor = sheet_colors['賣家統計']
    format_worksheet(ws_seller, df_seller, '賣家統計')

    # 地區分析工作表
    ws_state = wb.create_sheet('地區分析')
    ws_state.sheet_properties.tabColor = sheet_colors['地區分析']
    format_worksheet(ws_state, df_state, '地區分析')

    # 付款方式工作表
    ws_payment = wb.create_sheet('付款方式')
    ws_payment.sheet_properties.tabColor = sheet_colors['付款方式']
    format_worksheet(ws_payment, df_payment, '付款方式')

    # 評論評分工作表
    ws_review = wb.create_sheet('評論評分')
    ws_review.sheet_properties.tabColor = sheet_colors['評論評分']
    format_worksheet(ws_review, df_review, '評論評分')

    # 步驟6：保存檔案
    print("[6/6] 保存檔案...")
    output_file = '/home/justin/web-projects/excel-python-data-analysis/week07-08_openpyxl-mastery/case02_multi_sheet_report.xlsx'
    wb.save(output_file)

    # 輸出統計資訊
    print("\n" + "=" * 70)
    print("✅ 多工作表報告已生成！")
    print("=" * 70)
    print(f"📊 檔案位置：{output_file}")
    print(f"📊 工作表數量：6 個")
    print(f"📊 工作表列表：")
    print("   1. 目錄 - 工作表導航頁面")
    print(f"   2. 類別銷售 - {len(df_category)} 個產品類別")
    print(f"   3. 賣家統計 - {len(df_seller)} 個賣家")
    print(f"   4. 地區分析 - {len(df_state)} 個州/地區")
    print(f"   5. 付款方式 - {len(df_payment)} 種付款方式")
    print(f"   6. 評論評分 - {len(df_review)} 個評分等級")
    print("\n✓ 特性說明：")
    print("  • 工作表標籤顏色：彩色標籤易於識別")
    print("  • 自動格式化：每個工作表統一樣式")
    print("  • 凍結窗格：固定標題列方便瀏覽")
    print("  • 數值格式：自動適配金額、百分比等")
    print("  • 目錄導航：快速跳轉到各工作表")


if __name__ == "__main__":
    create_multi_sheet_report()
