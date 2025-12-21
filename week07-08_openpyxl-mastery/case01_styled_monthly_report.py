"""
案例1：格式化月報自動生成
功能：
1. 讀取 pandas DataFrame
2. 寫入 Excel 並自動格式化
3. 標題列：粗體、藍底白字、置中
4. 數值格式：千分位、小數位、百分比
5. 自動調整欄寬
6. 凍結窗格

Author: Week 7-8 openpyxl 完全掌握
Date: 2024-12-11
"""

import pandas as pd
from openpyxl import Workbook
from openpyxl.styles import Font, PatternFill, Alignment, Border, Side
from openpyxl.utils.dataframe import dataframe_to_rows
from openpyxl.utils import get_column_letter
import sys
from pathlib import Path
import warnings

warnings.filterwarnings('ignore')

# 新增父路徑到 sys.path
sys.path.insert(0, str(Path(__file__).parent.parent / 'week03-06_pandas-advanced' / 'utils'))

from data_loader import load_olist_data


def create_styled_monthly_report():
    """
    建立格式化的月報表

    流程：
    1. 載入 Olist 資料
    2. 提取訂單資訊並按月份分組
    3. 計算月度統計指標
    4. 建立 Excel 工作簿
    5. 應用樣式和格式
    """

    print("=" * 70)
    print("案例1：格式化月報自動生成")
    print("=" * 70)

    # 步驟1：載入資料
    print("\n[1/5] 載入 Olist 資料...")
    try:
        orders, order_items, products, customers, sellers, payments, reviews = load_olist_data(verbose=False)
    except Exception as e:
        print(f"資料載入失敗：{e}")
        return

    # 步驟2：準備資料 - 合併訂單和訂單明細
    print("[2/5] 準備資料...")
    df = orders[['order_id', 'customer_id', 'order_purchase_timestamp', 'order_status']].copy()
    df = df.merge(
        order_items[['order_id', 'price', 'freight_value']],
        on='order_id',
        how='left'
    )

    # 提取年月
    df['purchase_datetime'] = pd.to_datetime(df['order_purchase_timestamp'], errors='coerce')
    df['year_month'] = df['purchase_datetime'].dt.to_period('M')

    # 步驟3：計算月度統計
    print("[3/5] 計算月度統計...")
    monthly_stats = df.groupby('year_month').agg({
        'order_id': 'nunique',
        'price': ['sum', 'mean', 'count'],
        'freight_value': 'sum',
        'customer_id': 'nunique'
    }).reset_index()

    # 展平多層列索引
    monthly_stats.columns = [
        '月份',
        '訂單數',
        '總銷售額',
        '平均商品價格',
        '商品件數',
        '總運費',
        '獨立客戶數'
    ]

    # 轉換月份為字符串並添加計算欄位
    monthly_stats['月份'] = monthly_stats['月份'].astype(str)
    monthly_stats['毛利率%'] = (
        (monthly_stats['總銷售額'] - monthly_stats['總運費']) /
        monthly_stats['總銷售額'] * 100
    ).round(2)

    # 步驟4：建立 Excel 工作簿
    print("[4/5] 建立 Excel 工作簿...")
    wb = Workbook()
    ws = wb.active
    ws.title = '月報'

    # 定義樣式
    header_font = Font(bold=True, color='FFFFFF', size=12)
    header_fill = PatternFill(start_color='1F4E78', end_color='1F4E78', fill_type='solid')
    header_alignment = Alignment(horizontal='center', vertical='center', wrap_text=True)

    border_style = Border(
        left=Side(style='thin', color='000000'),
        right=Side(style='thin', color='000000'),
        top=Side(style='thin', color='000000'),
        bottom=Side(style='thin', color='000000')
    )

    data_alignment = Alignment(horizontal='right', vertical='center')
    text_alignment = Alignment(horizontal='left', vertical='center')

    # 步驟5：寫入標題列和資料
    print("[5/5] 應用格式和樣式...")

    # 寫入標題
    headers = monthly_stats.columns.tolist()
    for col_idx, header in enumerate(headers, start=1):
        cell = ws.cell(row=1, column=col_idx, value=header)
        cell.font = header_font
        cell.fill = header_fill
        cell.alignment = header_alignment
        cell.border = border_style

    # 寫入資料
    for row_idx, row in enumerate(monthly_stats.values, start=2):
        for col_idx, value in enumerate(row, start=1):
            cell = ws.cell(row=row_idx, column=col_idx, value=value)
            cell.border = border_style

            # 設定對齊
            if col_idx == 1:  # 月份欄
                cell.alignment = text_alignment
            else:
                cell.alignment = data_alignment

            # 設定數值格式
            if col_idx == 2:  # 訂單數
                cell.number_format = '#,##0'
            elif col_idx in [3, 5, 6]:  # 金額欄
                cell.number_format = '#,##0.00'
            elif col_idx == 4:  # 平均價格
                cell.number_format = '#,##0.00'
            elif col_idx == 7:  # 客戶數
                cell.number_format = '#,##0'
            elif col_idx == 8:  # 毛利率
                cell.number_format = '0.00"%"'

    # 調整欄寬
    column_widths = [15, 12, 15, 15, 12, 15, 12, 12]
    for col_idx, width in enumerate(column_widths, start=1):
        ws.column_dimensions[get_column_letter(col_idx)].width = width

    # 設定標題列高度
    ws.row_dimensions[1].height = 25

    # 凍結第一列和第一行
    ws.freeze_panes = 'A2'

    # 保存檔案
    output_file = '/home/justin/web-projects/excel-python-data-analysis/week07-08_openpyxl-mastery/case01_monthly_report.xlsx'
    wb.save(output_file)

    # 輸出統計資訊
    print("\n" + "=" * 70)
    print("✅ 月報已生成！")
    print("=" * 70)
    print(f"📊 檔案位置：{output_file}")
    print(f"📊 資料筆數：{len(monthly_stats)} 個月份")
    print(f"📊 總訂單數：{monthly_stats['訂單數'].sum():,.0f}")
    print(f"📊 總銷售額：R$ {monthly_stats['總銷售額'].sum():,.2f}")
    print(f"📊 總客戶數：{monthly_stats['獨立客戶數'].sum():,.0f}")
    print(f"📊 平均毛利率：{monthly_stats['毛利率%'].mean():.2f}%")
    print("\n✓ Excel 格式化特性：")
    print("  • 標題列：粗體、藍底白字、置中")
    print("  • 邊框：所有儲存格有邊框")
    print("  • 數值格式：千分位、小數位、百分比")
    print("  • 自動調整欄寬：根據內容最適化")
    print("  • 凍結窗格：固定標題列")


if __name__ == "__main__":
    create_styled_monthly_report()
