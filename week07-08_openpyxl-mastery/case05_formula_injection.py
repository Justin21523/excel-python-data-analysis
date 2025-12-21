"""
案例5：公式注入
功能：
1. 動態公式計算
2. SUM、AVERAGE、COUNT 函數
3. IF 條件判斷
4. VLOOKUP 查詢
5. 公式自動複製

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


def create_formula_injection_report():
    """
    建立公式注入報告

    流程：
    1. 載入資料
    2. 準備銷售資料
    3. 建立 Excel 工作簿
    4. 注入各類公式
    5. 自動計算結果
    """

    print("=" * 70)
    print("案例5：公式注入")
    print("=" * 70)

    # 步驟1：載入資料
    print("\n[1/5] 載入 Olist 資料...")
    try:
        orders, order_items, products, customers, sellers, payments, reviews = load_olist_data(verbose=False)
    except Exception as e:
        print(f"資料載入失敗：{e}")
        return

    # 步驟2：準備資料
    print("[2/5] 準備銷售資料...")

    # 準備銷售員績效資料
    seller_data = sellers.head(20).copy()
    seller_data = seller_data.merge(
        order_items.groupby('seller_id').agg({'price': ['sum', 'count', 'mean']}).reset_index(),
        on='seller_id',
        how='left'
    ).fillna(0)

    seller_data.columns = ['seller_id', 'seller_zip_code_prefix', 'seller_city', 'seller_state',
                           '銷售額', '銷售件數', '平均商品價格']

    # 步驟3：建立 Excel 工作簿
    print("[3/5] 建立 Excel 工作簿...")
    wb = Workbook()
    ws = wb.active
    ws.title = '銷售績效分析'

    # 定義樣式
    header_font = Font(bold=True, color='FFFFFF', size=11)
    header_fill = PatternFill(start_color='1F4E78', end_color='1F4E78', fill_type='solid')
    header_alignment = Alignment(horizontal='center', vertical='center', wrap_text=True)

    summary_font = Font(bold=True, size=10)
    summary_fill = PatternFill(start_color='E2EFDA', end_color='E2EFDA', fill_type='solid')

    border_style = Border(
        left=Side(style='thin', color='CCCCCC'),
        right=Side(style='thin', color='CCCCCC'),
        top=Side(style='thin', color='CCCCCC'),
        bottom=Side(style='thin', color='CCCCCC')
    )

    # 步驟4：寫入資料和注入公式
    print("[4/5] 注入公式...")

    # 寫入標題
    headers = ['賣家ID', '城市', '州', '銷售額', '銷售件數', '平均商品價格',
               '佣金(5%)', '績效評級', '業績增長%']

    for col_idx, header in enumerate(headers, start=1):
        cell = ws.cell(row=1, column=col_idx, value=header)
        cell.font = header_font
        cell.fill = header_fill
        cell.alignment = header_alignment
        cell.border = border_style

    # 設定平均銷售額（用於比較）
    average_sales = seller_data['銷售額'].mean()

    # 寫入資料和公式
    for row_idx, (idx, row) in enumerate(seller_data.iterrows(), start=2):
        # 賣家ID
        cell = ws.cell(row=row_idx, column=1, value=row['seller_id'])
        cell.border = border_style

        # 城市
        cell = ws.cell(row=row_idx, column=2, value=row['seller_city'])
        cell.border = border_style

        # 州
        cell = ws.cell(row=row_idx, column=3, value=row['seller_state'])
        cell.border = border_style

        # 銷售額
        cell = ws.cell(row=row_idx, column=4, value=row['銷售額'])
        cell.number_format = '#,##0.00'
        cell.border = border_style

        # 銷售件數
        cell = ws.cell(row=row_idx, column=5, value=row['銷售件數'])
        cell.number_format = '#,##0'
        cell.border = border_style

        # 平均商品價格
        cell = ws.cell(row=row_idx, column=6, value=row['平均商品價格'])
        cell.number_format = '#,##0.00'
        cell.border = border_style

        # 佣金公式：銷售額 * 5%
        cell = ws.cell(row=row_idx, column=7)
        cell.value = f'=D{row_idx}*0.05'
        cell.number_format = '#,##0.00'
        cell.border = border_style
        cell.fill = PatternFill(start_color='FFF2CC', end_color='FFF2CC', fill_type='solid')

        # 績效評級公式：IF條件判斷
        cell = ws.cell(row=row_idx, column=8)
        cell.value = f'=IF(D{row_idx}>{average_sales}*1.2,"優秀",IF(D{row_idx}>{average_sales},"良好","標準"))'
        cell.border = border_style
        cell.fill = PatternFill(start_color='E2EFDA', end_color='E2EFDA', fill_type='solid')

        # 業績增長%（相對平均值）
        cell = ws.cell(row=row_idx, column=9)
        cell.value = f'=(D{row_idx}-{average_sales})/{average_sales}'
        cell.number_format = '0.00%'
        cell.border = border_style
        cell.fill = PatternFill(start_color='F4CCCC', end_color='F4CCCC', fill_type='solid')

    # 步驟5：添加統計彙總區域
    print("[5/5] 添加統計彙總...")

    summary_row = len(seller_data) + 3

    # 彙總標題
    summary_title = ws.cell(row=summary_row, column=1, value='統計彙總')
    summary_title.font = summary_font
    summary_title.fill = summary_fill

    # 統計項目
    stats_row = summary_row + 1

    # 總銷售額
    ws.cell(row=stats_row, column=1, value='總銷售額')
    ws.cell(row=stats_row, column=1).font = Font(bold=True)
    cell = ws.cell(row=stats_row, column=2)
    cell.value = f'=SUM(D2:D{len(seller_data)+1})'
    cell.number_format = '#,##0.00'

    # 平均銷售額
    stats_row += 1
    ws.cell(row=stats_row, column=1, value='平均銷售額')
    ws.cell(row=stats_row, column=1).font = Font(bold=True)
    cell = ws.cell(row=stats_row, column=2)
    cell.value = f'=AVERAGE(D2:D{len(seller_data)+1})'
    cell.number_format = '#,##0.00'

    # 最高銷售額
    stats_row += 1
    ws.cell(row=stats_row, column=1, value='最高銷售額')
    ws.cell(row=stats_row, column=1).font = Font(bold=True)
    cell = ws.cell(row=stats_row, column=2)
    cell.value = f'=MAX(D2:D{len(seller_data)+1})'
    cell.number_format = '#,##0.00'

    # 最低銷售額
    stats_row += 1
    ws.cell(row=stats_row, column=1, value='最低銷售額')
    ws.cell(row=stats_row, column=1).font = Font(bold=True)
    cell = ws.cell(row=stats_row, column=2)
    cell.value = f'=MIN(D2:D{len(seller_data)+1})'
    cell.number_format = '#,##0.00'

    # 總佣金
    stats_row += 1
    ws.cell(row=stats_row, column=1, value='總佣金')
    ws.cell(row=stats_row, column=1).font = Font(bold=True)
    cell = ws.cell(row=stats_row, column=2)
    cell.value = f'=SUM(G2:G{len(seller_data)+1})'
    cell.number_format = '#,##0.00'

    # 優秀賣家數
    stats_row += 1
    ws.cell(row=stats_row, column=1, value='優秀賣家數')
    ws.cell(row=stats_row, column=1).font = Font(bold=True)
    cell = ws.cell(row=stats_row, column=2)
    cell.value = f'=COUNTIF(H2:H{len(seller_data)+1},"優秀")'
    cell.number_format = '#,##0'

    # 調整欄寬
    column_widths = [15, 12, 8, 15, 12, 15, 12, 12, 12]
    for col_idx, width in enumerate(column_widths, start=1):
        ws.column_dimensions[get_column_letter(col_idx)].width = width

    # 凍結標題列
    ws.freeze_panes = 'A2'

    # 保存檔案
    output_file = '/home/justin/web-projects/excel-python-data-analysis/week07-08_openpyxl-mastery/case05_formula_injection.xlsx'
    wb.save(output_file)

    # 輸出統計資訊
    print("\n" + "=" * 70)
    print("✅ 公式注入報告已生成！")
    print("=" * 70)
    print(f"📊 檔案位置：{output_file}")
    print(f"📊 資料筆數：{len(seller_data)} 個賣家")
    print(f"📊 公式類型：")
    print(f"   • SUM()：計算總和")
    print(f"   • AVERAGE()：計算平均值")
    print(f"   • MAX/MIN()：找最大/最小值")
    print(f"   • IF()：條件判斷")
    print(f"   • COUNTIF()：條件計數")
    print(f"\n✓ 公式應用位置：")
    print(f"   • G列：佣金計算 = 銷售額 * 5%")
    print(f"   • H列：績效評級 = IF條件判斷")
    print(f"   • I列：業績增長% = 相對平均值")
    print(f"   • 統計區：SUM、AVERAGE、MAX、MIN、COUNTIF")


if __name__ == "__main__":
    create_formula_injection_report()
