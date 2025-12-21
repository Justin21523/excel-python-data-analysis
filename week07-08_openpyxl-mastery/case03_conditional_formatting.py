"""
案例3：條件格式自動化
功能：
1. 業績達標：綠色
2. 未達標：紅色
3. 接近目標：黃色
4. 資料條 (Data Bar)
5. 色階 (Color Scale)
6. 圖示集 (Icon Set)

Author: Week 7-8 openpyxl 完全掌握
Date: 2024-12-11
"""

import pandas as pd
from openpyxl import Workbook
from openpyxl.styles import Font, PatternFill, Alignment, Border, Side
from openpyxl.formatting.rule import CellIsRule, ColorScaleRule, DataBarRule, IconSetRule
from openpyxl.utils import get_column_letter
import sys
from pathlib import Path
import warnings

warnings.filterwarnings('ignore')

# 新增父路徑到 sys.path
sys.path.insert(0, str(Path(__file__).parent.parent / 'week03-06_pandas-advanced' / 'utils'))

from data_loader import load_olist_data


def create_conditional_formatting_report():
    """
    建立條件格式自動化報告

    流程：
    1. 載入 Olist 資料
    2. 準備銷售業績資料
    3. 建立 Excel 工作簿
    4. 應用各種條件格式
    5. 添加圖表
    """

    print("=" * 70)
    print("案例3：條件格式自動化")
    print("=" * 70)

    # 步驟1：載入資料
    print("\n[1/5] 載入 Olist 資料...")
    try:
        orders, order_items, products, customers, sellers, payments, reviews = load_olist_data(verbose=False)
    except Exception as e:
        print(f"資料載入失敗：{e}")
        return

    # 步驟2：準備銷售業績資料
    print("[2/5] 準備銷售業績資料...")

    # 計算賣家業績
    seller_performance = sellers.merge(
        order_items[['seller_id', 'price']],
        on='seller_id'
    ).groupby(['seller_id', 'seller_city']).agg({
        'price': ['sum', 'count', 'mean']
    }).reset_index()

    seller_performance.columns = ['賣家ID', '城市', '銷售額', '銷售件數', '平均商品價格']
    seller_performance = seller_performance.sort_values('銷售額', ascending=False).head(30).reset_index(drop=True)

    # 計算業績目標（中位數）
    target = seller_performance['銷售額'].median()
    seller_performance['達標狀態'] = seller_performance['銷售額'] >= target
    seller_performance['達成率%'] = (seller_performance['銷售額'] / target * 100).round(2)

    # 計算評分
    seller_reviews = reviews.merge(
        orders[['order_id', 'seller_id']],
        on='order_id',
        how='left'
    ).groupby('seller_id').agg({
        'review_score': 'mean'
    }).reset_index()
    seller_reviews.columns = ['seller_id', '平均評分']

    seller_performance = seller_performance.merge(
        seller_reviews,
        on='seller_id',
        how='left'
    ).fillna(0)

    # 步驟3：建立 Excel 工作簿
    print("[3/5] 建立 Excel 工作簿...")
    wb = Workbook()
    ws = wb.active
    ws.title = '業績達標分析'

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

    # 寫入標題
    print("[4/5] 應用條件格式...")
    headers = seller_performance.columns.tolist()
    for col_idx, header in enumerate(headers, start=1):
        cell = ws.cell(row=1, column=col_idx, value=header)
        cell.font = header_font
        cell.fill = header_fill
        cell.alignment = header_alignment
        cell.border = border_style

    # 寫入資料
    for row_idx, row_data in enumerate(seller_performance.values, start=2):
        for col_idx, value in enumerate(row_data, start=1):
            cell = ws.cell(row=row_idx, column=col_idx, value=value)
            cell.border = border_style

            # 設定數值格式
            if col_idx in [3, 5]:  # 金額欄
                cell.number_format = '#,##0.00'
            elif col_idx == 4:  # 件數
                cell.number_format = '#,##0'
            elif col_idx in [6, 7]:  # 達成率、評分
                cell.number_format = '0.00'

    # 步驟4：應用條件格式
    print("[4/5] 應用條件格式...")

    # 條件格式1：銷售額 - 資料條 (Data Bar)
    data_bar_rule = DataBarRule(
        start_type='min',
        start_value=None,
        end_type='max',
        end_value=None,
        color='FF0070C0'
    )
    ws.conditional_formatting.add(
        f'C2:C{len(seller_performance) + 1}',
        data_bar_rule
    )

    # 條件格式2：達成率 - 色階 (Color Scale)
    color_scale_rule = ColorScaleRule(
        start_type='min',
        start_color='FFF8696B',  # 紅色
        mid_type='percentile',
        mid_value=50,
        mid_color='FFFFFF00',  # 黃色
        end_type='max',
        end_color='FF63BE7B'   # 綠色
    )
    ws.conditional_formatting.add(
        f'G2:G{len(seller_performance) + 1}',
        color_scale_rule
    )

    # 條件格式3：評分 - 圖示集 (Icon Set)
    icon_rule = IconSetRule(
        icon_style='3TrafficLights',
        formula=['=IF(H2<3,1,IF(H2<4,2,3))']
    )
    ws.conditional_formatting.add(
        f'H2:H{len(seller_performance) + 1}',
        icon_rule
    )

    # 條件格式4：達標狀態 - 紅綠格式化
    green_fill = PatternFill(start_color='C6EFCE', end_color='C6EFCE', fill_type='solid')
    green_font = Font(color='006100')
    red_fill = PatternFill(start_color='FFC7CE', end_color='FFC7CE', fill_type='solid')
    red_font = Font(color='9C0006')

    green_rule = CellIsRule(
        operator='equal',
        formula=['TRUE'],
        stopIfTrue=False,
        fill=green_fill,
        font=green_font
    )

    red_rule = CellIsRule(
        operator='equal',
        formula=['FALSE'],
        stopIfTrue=False,
        fill=red_fill,
        font=red_font
    )

    ws.conditional_formatting.add(f'F2:F{len(seller_performance) + 1}', green_rule)
    ws.conditional_formatting.add(f'F2:F{len(seller_performance) + 1}', red_rule)

    # 調整欄寬
    column_widths = [12, 12, 15, 12, 15, 12, 12, 12]
    for col_idx, width in enumerate(column_widths, start=1):
        ws.column_dimensions[get_column_letter(col_idx)].width = width

    # 凍結標題列
    ws.freeze_panes = 'A2'

    # 步驟5：保存檔案
    print("[5/5] 保存檔案...")
    output_file = '/home/justin/web-projects/excel-python-data-analysis/week07-08_openpyxl-mastery/case03_conditional_formatting.xlsx'
    wb.save(output_file)

    # 輸出統計資訊
    print("\n" + "=" * 70)
    print("✅ 條件格式報告已生成！")
    print("=" * 70)
    print(f"📊 檔案位置：{output_file}")
    print(f"📊 資料筆數：{len(seller_performance)} 個賣家")
    print(f"📊 業績目標：R$ {target:,.2f}")
    print(f"📊 達標賣家數：{seller_performance['達標狀態'].sum()} 個")
    print(f"📊 未達標賣家數：{(~seller_performance['達標狀態']).sum()} 個")
    print(f"📊 平均評分：{seller_performance['平均評分'].mean():.2f} / 5.0")
    print("\n✓ 條件格式說明：")
    print("  • 銷售額欄（C欄）：資料條 (Data Bar) - 視覺化銷售額大小")
    print("  • 達成率欄（G欄）：色階 (Color Scale) - 紅→黃→綠漸變")
    print("  • 評分欄（H欄）：圖示集 (Icon Set) - 3個信號燈")
    print("  • 達標狀態欄（F欄）：條件格式 - 達標綠色，未達標紅色")


if __name__ == "__main__":
    create_conditional_formatting_report()
