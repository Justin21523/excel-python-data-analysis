"""
案例4：動態圖表生成
功能：
1. 長條圖：產品銷售排名
2. 折線圖：銷售趨勢
3. 圓餅圖：類別佔比
4. 組合圖：雙軸圖表（銷售額 + 成長率）

Author: Week 7-8 openpyxl 完全掌握
Date: 2024-12-11
"""

import pandas as pd
from openpyxl import Workbook
from openpyxl.styles import Font, PatternFill, Alignment, Border, Side
from openpyxl.chart import (
    BarChart, LineChart, PieChart, AreaChart,
    Reference, Series
)
from openpyxl.utils import get_column_letter
import sys
from pathlib import Path
import warnings

warnings.filterwarnings('ignore')

# 新增父路徑到 sys.path
sys.path.insert(0, str(Path(__file__).parent.parent / 'week03-06_pandas-advanced' / 'utils'))

from data_loader import load_olist_data


def format_data_worksheet(ws, df, headers=None):
    """
    格式化資料工作表

    參數：
    - ws：Worksheet 物件
    - df：DataFrame 資料
    - headers：欄位標題
    """

    header_font = Font(bold=True, color='FFFFFF', size=11)
    header_fill = PatternFill(start_color='366092', end_color='366092', fill_type='solid')
    header_alignment = Alignment(horizontal='center', vertical='center')

    border_style = Border(
        left=Side(style='thin', color='CCCCCC'),
        right=Side(style='thin', color='CCCCCC'),
        top=Side(style='thin', color='CCCCCC'),
        bottom=Side(style='thin', color='CCCCCC')
    )

    # 寫入標題
    if headers is None:
        headers = df.columns.tolist()

    for col_idx, header in enumerate(headers, start=1):
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

            # 格式化數值
            if isinstance(value, float):
                if col_idx > 1:
                    cell.number_format = '#,##0.00'

    # 自動調整欄寬
    for col_idx in range(1, len(headers) + 1):
        ws.column_dimensions[get_column_letter(col_idx)].width = 15

    return len(df) + 1


def create_dynamic_charts():
    """
    建立動態圖表報告

    流程：
    1. 載入資料
    2. 準備圖表資料
    3. 建立工作表
    4. 建立各種圖表
    5. 保存檔案
    """

    print("=" * 70)
    print("案例4：動態圖表生成")
    print("=" * 70)

    # 步驟1：載入資料
    print("\n[1/5] 載入 Olist 資料...")
    try:
        orders, order_items, products, customers, sellers, payments, reviews = load_olist_data(verbose=False)
    except Exception as e:
        print(f"資料載入失敗：{e}")
        return

    # 步驟2：準備圖表資料
    print("[2/5] 準備圖表資料...")

    # 圖表1：按類別統計銷售（長條圖）
    df_category = products.merge(
        order_items[['product_id', 'price']],
        on='product_id'
    ).groupby('product_category_name').agg({
        'price': ['sum', 'count']
    }).reset_index()

    df_category.columns = ['類別', '銷售額', '銷售件數']
    df_category = df_category.sort_values('銷售額', ascending=False).head(15)
    df_category = df_category.reset_index(drop=True)

    # 圖表2：月度銷售趨勢（折線圖）
    df_trend = orders[['order_id', 'order_purchase_timestamp']].copy()
    df_trend = df_trend.merge(
        order_items[['order_id', 'price']],
        on='order_id'
    )
    df_trend['year_month'] = pd.to_datetime(
        df_trend['order_purchase_timestamp'],
        errors='coerce'
    ).dt.to_period('M').astype(str)

    df_trend = df_trend.groupby('year_month').agg({
        'price': ['sum', 'count']
    }).reset_index()

    df_trend.columns = ['月份', '銷售額', '訂單數']
    df_trend = df_trend.tail(12)  # 取最後12個月
    df_trend = df_trend.reset_index(drop=True)

    # 圖表3：產品類別佔比（圓餅圖）
    df_pie = df_category.copy()

    # 圖表4：類別銷售與件數（組合圖）
    df_combo = df_category.head(10).copy()

    # 步驟3：建立 Excel 工作簿
    print("[3/5] 建立 Excel 工作簿...")
    wb = Workbook()
    wb.remove(wb.active)

    # 步驟4：建立工作表和圖表
    print("[4/5] 建立圖表...")

    # 工作表1：類別銷售資料 + 長條圖
    ws1 = wb.create_sheet('類別銷售')
    row_count = format_data_worksheet(ws1, df_category)

    # 建立長條圖
    chart1 = BarChart()
    chart1.type = 'col'
    chart1.title = '按類別統計銷售額'
    chart1.y_axis.title = '銷售額 (R$)'
    chart1.x_axis.title = '產品類別'

    # 引用資料
    data1 = Reference(ws1, min_col=2, min_row=1, max_row=row_count - 1)
    cats1 = Reference(ws1, min_col=1, min_row=2, max_row=row_count - 1)

    chart1.add_data(data1, titles_from_data=True)
    chart1.set_categories(cats1)
    chart1.height = 10
    chart1.width = 20

    ws1.add_chart(chart1, 'D2')

    # 工作表2：月度趨勢資料 + 折線圖
    ws2 = wb.create_sheet('銷售趨勢')
    row_count = format_data_worksheet(ws2, df_trend)

    # 建立折線圖
    chart2 = LineChart()
    chart2.title = '月度銷售趨勢'
    chart2.y_axis.title = '銷售額 (R$)'
    chart2.x_axis.title = '月份'

    # 引用資料
    data2 = Reference(ws2, min_col=2, min_row=1, max_row=row_count - 1)
    cats2 = Reference(ws2, min_col=1, min_row=2, max_row=row_count - 1)

    chart2.add_data(data2, titles_from_data=True)
    chart2.set_categories(cats2)
    chart2.height = 10
    chart2.width = 20

    ws2.add_chart(chart2, 'D2')

    # 工作表3：類別佔比資料 + 圓餅圖
    ws3 = wb.create_sheet('類別佔比')
    row_count = format_data_worksheet(ws3, df_pie[['類別', '銷售額']])

    # 建立圓餅圖
    chart3 = PieChart()
    chart3.title = '產品類別銷售額佔比'

    # 引用資料
    labels3 = Reference(ws3, min_col=1, min_row=2, max_row=row_count - 1)
    data3 = Reference(ws3, min_col=2, min_row=1, max_row=row_count - 1)

    chart3.add_data(data3, titles_from_data=True)
    chart3.set_categories(labels3)
    chart3.height = 12
    chart3.width = 15

    ws3.add_chart(chart3, 'D2')

    # 工作表4：組合圖資料 + 雙軸圖表
    ws4 = wb.create_sheet('銷售分析')

    # 寫入組合資料
    ws4['A1'] = '類別'
    ws4['B1'] = '銷售額'
    ws4['C1'] = '銷售件數'

    for idx, row in enumerate(df_combo.values, start=2):
        ws4[f'A{idx}'] = row[0]
        ws4[f'B{idx}'] = row[1]
        ws4[f'C{idx}'] = row[2]

    # 應用標題格式
    header_fill = PatternFill(start_color='366092', end_color='366092', fill_type='solid')
    header_font = Font(bold=True, color='FFFFFF')

    for cell in ws4['A1:C1'][0]:
        cell.fill = header_fill
        cell.font = header_font

    # 建立面積圖（組合圖）
    chart4 = AreaChart()
    chart4.title = '類別銷售額與件數'
    chart4.y_axis.title = '數值'
    chart4.x_axis.title = '產品類別'

    # 引用資料
    data4_left = Reference(ws4, min_col=2, min_row=1, max_row=len(df_combo) + 1)
    data4_right = Reference(ws4, min_col=3, min_row=1, max_row=len(df_combo) + 1)
    cats4 = Reference(ws4, min_col=1, min_row=2, max_row=len(df_combo) + 1)

    chart4.add_data(data4_left, titles_from_data=True)
    chart4.add_data(data4_right, titles_from_data=True)
    chart4.set_categories(cats4)
    chart4.height = 10
    chart4.width = 20

    ws4.add_chart(chart4, 'E2')

    # 步驟5：保存檔案
    print("[5/5] 保存檔案...")
    output_file = '/home/justin/web-projects/excel-python-data-analysis/week07-08_openpyxl-mastery/case04_dynamic_charts.xlsx'
    wb.save(output_file)

    # 輸出統計資訊
    print("\n" + "=" * 70)
    print("✅ 動態圖表報告已生成！")
    print("=" * 70)
    print(f"📊 檔案位置：{output_file}")
    print(f"📊 工作表數量：4 個")
    print(f"📊 圖表類型：")
    print(f"   1. 長條圖 - 按類別統計銷售額（{len(df_category)} 個類別）")
    print(f"   2. 折線圖 - 月度銷售趨勢（{len(df_trend)} 個月份）")
    print(f"   3. 圓餅圖 - 產品類別佔比（{len(df_pie)} 個類別）")
    print(f"   4. 面積圖 - 銷售分析（{len(df_combo)} 個類別）")
    print("\n✓ 圖表特性：")
    print("  • 長條圖：視覺化類別銷售額排名")
    print("  • 折線圖：展示時間序列銷售趨勢")
    print("  • 圓餅圖：顯示各類別銷售額佔比")
    print("  • 面積圖：多維度銷售分析")
    print("  • 所有圖表自動引用資料範圍")


if __name__ == "__main__":
    create_dynamic_charts()
