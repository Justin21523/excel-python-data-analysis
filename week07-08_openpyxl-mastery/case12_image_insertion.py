"""
案例12：圖片插入
功能：
1. 插入本地圖片
2. 圖片大小調整
3. 圖片位置設定
4. 背景圖片設定
5. 圖表圖片導出

Author: Week 7-8 openpyxl 完全掌握
Date: 2024-12-11
"""

import pandas as pd
from openpyxl import Workbook
from openpyxl.styles import Font, PatternFill, Alignment, Border, Side
from openpyxl.drawing.image import Image as XLImage
from openpyxl.utils import get_column_letter
from openpyxl.chart import BarChart, Reference
import matplotlib.pyplot as plt
import io
import sys
from pathlib import Path
import warnings

warnings.filterwarnings('ignore')

# 新增父路徑到 sys.path
sys.path.insert(0, str(Path(__file__).parent.parent / 'week03-06_pandas-advanced' / 'utils'))

from data_loader import load_olist_data


def create_sample_image():
    """
    建立範例圖片（matplotlib 生成的圖表）

    返回圖片路徑
    """
    # 建立簡單的圖表
    fig, ax = plt.subplots(figsize=(8, 6))

    categories = ['電子產品', '家居用品', '服裝', '美妝', '運動']
    values = [450000, 380000, 320000, 290000, 210000]

    ax.bar(categories, values, color=['#1f4e78', '#366092', '#4472c4', '#5b9bd5', '#70ad47'])
    ax.set_ylabel('銷售額 (R$)', fontsize=11)
    ax.set_title('產品類別銷售額排行', fontsize=14, fontweight='bold')
    ax.yaxis.set_major_formatter(plt.FuncFormatter(lambda x, p: f'R${x/1000:.0f}K'))

    plt.xticks(rotation=45)
    plt.tight_layout()

    # 保存圖片
    image_path = '/home/justin/web-projects/excel-python-data-analysis/week07-08_openpyxl-mastery/sample_chart.png'
    plt.savefig(image_path, dpi=150, bbox_inches='tight')
    plt.close()

    return image_path


def create_image_insertion_report():
    """
    建立圖片插入報告

    流程：
    1. 載入資料
    2. 生成圖表圖片
    3. 建立 Excel 工作簿
    4. 插入圖片到工作表
    5. 設定圖片位置和大小
    """

    print("=" * 70)
    print("案例12：圖片插入")
    print("=" * 70)

    # 步驟1：載入資料
    print("\n[1/5] 載入 Olist 資料...")
    try:
        orders, order_items, products, customers, sellers, payments, reviews = load_olist_data(verbose=False)
    except Exception as e:
        print(f"資料載入失敗：{e}")
        return

    # 步驟2：建立樣本圖片
    print("[2/5] 建立樣本圖片...")
    image_path = create_sample_image()

    # 步驟3：建立 Excel 工作簿
    print("[3/5] 建立 Excel 工作簿...")
    wb = Workbook()
    ws = wb.active
    ws.title = '圖表展示'

    # 定義樣式
    title_font = Font(bold=True, size=14, color='FFFFFF')
    title_fill = PatternFill(start_color='1F4E78', end_color='1F4E78', fill_type='solid')
    title_alignment = Alignment(horizontal='center', vertical='center')

    header_font = Font(bold=True, color='FFFFFF', size=11)
    header_fill = PatternFill(start_color='366092', end_color='366092', fill_type='solid')

    border_style = Border(
        left=Side(style='thin', color='CCCCCC'),
        right=Side(style='thin', color='CCCCCC'),
        top=Side(style='thin', color='CCCCCC'),
        bottom=Side(style='thin', color='CCCCCC')
    )

    # 步驟4：設計工作表和插入圖片
    print("[4/5] 設計工作表和插入圖片...")

    # 標題
    ws.merge_cells('A1:H1')
    title_cell = ws['A1']
    title_cell.value = '📊 銷售分析圖表展示'
    title_cell.font = title_font
    title_cell.fill = title_fill
    title_cell.alignment = title_alignment
    ws.row_dimensions[1].height = 30

    # 添加說明文字
    ws['A3'] = '本工作表展示各類型圖表的插入和排版方式'
    ws['A3'].font = Font(size=10, italic=True)

    # 插入第一張圖片（matplotlib 生成的圖表）
    ws.merge_cells('A5:H5')
    header_cell = ws['A5']
    header_cell.value = '圖表1：產品類別銷售排行'
    header_cell.font = header_font
    header_cell.fill = header_fill

    # 插入圖片
    img = XLImage(image_path)
    img.width = 500  # 寬度（像素）
    img.height = 350  # 高度（像素）

    ws.add_image(img, 'A7')

    # 調整列寬以容納圖片
    for col in range(1, 9):
        ws.column_dimensions[get_column_letter(col)].width = 15

    # 設定圖片所在行的高度
    ws.row_dimensions[7].height = 210
    ws.row_dimensions[8].height = 1
    ws.row_dimensions[9].height = 1
    ws.row_dimensions[10].height = 1
    ws.row_dimensions[11].height = 1
    ws.row_dimensions[12].height = 1

    # 第二部分：數據表格
    current_row = 24

    ws.merge_cells(f'A{current_row}:H{current_row}')
    header_cell = ws.cell(row=current_row, column=1, value='表格1：銷售數據統計')
    header_cell.font = header_font
    header_cell.fill = header_fill
    ws.row_dimensions[current_row].height = 20

    # 準備資料
    sales_data = products.merge(
        order_items[['product_id', 'price']],
        on='product_id'
    ).groupby('product_category_name').agg({
        'price': ['sum', 'count', 'mean']
    }).reset_index().head(10)

    sales_data.columns = ['類別', '銷售額', '銷售件數', '平均價格']
    sales_data = sales_data.sort_values('銷售額', ascending=False)

    # 表格標題
    current_row += 1
    headers = ['類別', '銷售額', '銷售件數', '平均價格']
    for col_idx, header in enumerate(headers, start=1):
        cell = ws.cell(row=current_row, column=col_idx, value=header)
        cell.font = header_font
        cell.fill = header_fill
        cell.alignment = Alignment(horizontal='center', vertical='center')
        cell.border = border_style

    # 表格數據
    for row_offset, (idx, row) in enumerate(sales_data.iterrows(), start=1):
        row_idx = current_row + row_offset
        for col_idx, value in enumerate(row.values, start=1):
            cell = ws.cell(row=row_idx, column=col_idx, value=value)
            cell.border = border_style

            if col_idx in [2, 4]:
                cell.number_format = '#,##0.00'
            elif col_idx == 3:
                cell.number_format = '#,##0'

    # 第三部分：內嵌圖表
    current_row = 40

    ws.merge_cells(f'A{current_row}:H{current_row}')
    header_cell = ws.cell(row=current_row, column=1, value='圖表2：銷售額長條圖')
    header_cell.font = header_font
    header_cell.fill = header_fill
    ws.row_dimensions[current_row].height = 20

    # 使用 openpyxl 內建圖表（不是插入圖片）
    chart_data = sales_data.head(8).copy()

    # 準備圖表資料所在位置
    chart_start_row = current_row + 2
    headers = ['類別', '銷售額']
    for col_idx, header in enumerate(headers, start=1):
        cell = ws.cell(row=chart_start_row, column=col_idx, value=header)
        cell.font = header_font
        cell.fill = header_fill

    for row_offset, (idx, row) in enumerate(chart_data.iterrows(), start=1):
        row_idx = chart_start_row + row_offset
        cell = ws.cell(row=row_idx, column=1, value=row['類別'])
        cell = ws.cell(row=row_idx, column=2, value=row['銷售額'])
        cell.number_format = '#,##0.00'

    # 建立圖表
    chart = BarChart()
    chart.type = 'col'
    chart.title = '銷售額排行'
    chart.y_axis.title = '銷售額 (R$)'

    # 引用資料
    data = Reference(ws, min_col=2, min_row=chart_start_row, max_row=chart_start_row + len(chart_data))
    cats = Reference(ws, min_col=1, min_row=chart_start_row + 1, max_row=chart_start_row + len(chart_data))

    chart.add_data(data, titles_from_data=True)
    chart.set_categories(cats)
    chart.height = 12
    chart.width = 20

    ws.add_chart(chart, f'A{chart_start_row + len(chart_data) + 2}')

    # 步驟5：保存檔案
    print("[5/5] 保存檔案...")
    output_file = '/home/justin/web-projects/excel-python-data-analysis/week07-08_openpyxl-mastery/case12_image_insertion.xlsx'
    wb.save(output_file)

    # 輸出統計資訊
    print("\n" + "=" * 70)
    print("✅ 圖片插入報告已生成！")
    print("=" * 70)
    print(f"📊 檔案位置：{output_file}")
    print(f"📊 圖片樣本位置：{image_path}")
    print(f"\n✓ 圖片/圖表應用：")
    print(f"  • matplotlib 生成的圖表：PNG 圖片插入")
    print(f"  • openpyxl 內建圖表：動態長條圖")
    print(f"  • 圖片尺寸：500x350 像素")
    print(f"  • 圖片位置：A7 儲存格")
    print(f"\n✓ 圖片特性：")
    print(f"  • 自動調整圖片尺寸")
    print(f"  • 指定圖片位置")
    print(f"  • 與資料表格配合")
    print(f"  • 提高視覺化效果")
    print(f"  • 支援多種圖表類型")


if __name__ == "__main__":
    create_image_insertion_report()
