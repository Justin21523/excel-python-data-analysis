"""
案例8：執行摘要（高級報表）
功能：
1. KPI 關鍵指標儀表板
2. 視覺化重點指標
3. 多色彩突出效果
4. 趨勢對比分析
5. 管理層報告設計

Author: Week 7-8 openpyxl 完全掌握
Date: 2024-12-11
"""

import pandas as pd
from openpyxl import Workbook
from openpyxl.styles import Font, PatternFill, Alignment, Border, Side
from openpyxl.utils import get_column_letter
from datetime import datetime
import sys
from pathlib import Path
import warnings

warnings.filterwarnings('ignore')

# 新增父路徑到 sys.path
sys.path.insert(0, str(Path(__file__).parent.parent / 'week03-06_pandas-advanced' / 'utils'))

from data_loader import load_olist_data


def create_executive_summary():
    """
    建立執行摘要報告

    流程：
    1. 載入資料
    2. 計算關鍵指標 (KPI)
    3. 建立儀表板
    4. 應用視覺化效果
    5. 添加管理層註釋
    """

    print("=" * 70)
    print("案例8：執行摘要（高級報表）")
    print("=" * 70)

    # 步驟1：載入資料
    print("\n[1/5] 載入 Olist 資料...")
    try:
        orders, order_items, products, customers, sellers, payments, reviews = load_olist_data(verbose=False)
    except Exception as e:
        print(f"資料載入失敗：{e}")
        return

    # 步驟2：計算 KPI
    print("[2/5] 計算關鍵指標...")

    # 計算各項指標
    total_revenue = order_items['price'].sum()
    total_orders = orders['order_id'].nunique()
    total_customers = customers['customer_id'].nunique()
    avg_order_value = total_revenue / total_orders if total_orders > 0 else 0

    delivered_orders = (orders['order_status'] == 'delivered').sum()
    delivery_rate = delivered_orders / total_orders * 100 if total_orders > 0 else 0

    avg_rating = reviews['review_score'].mean()
    satisfied_count = (reviews['review_score'] >= 4).sum()
    satisfaction_rate = satisfied_count / len(reviews) * 100 if len(reviews) > 0 else 0

    # 計算成長指標
    orders['purchase_date'] = pd.to_datetime(orders['order_purchase_timestamp'], errors='coerce').dt.date

    recent_orders = len(orders[orders['order_purchase_timestamp'].dt.date >= pd.to_datetime('2018-08-01').date()])
    early_orders = len(orders[orders['order_purchase_timestamp'].dt.date < pd.to_datetime('2018-08-01').date()])

    growth_rate = (recent_orders - early_orders) / early_orders * 100 if early_orders > 0 else 0

    # 按付款方式統計
    payment_summary = payments.groupby('payment_type')['payment_value'].sum()

    # 按州統計
    state_revenue = customers.merge(
        orders[['customer_id', 'order_id']],
        on='customer_id'
    ).merge(
        order_items[['order_id', 'price']],
        on='order_id'
    ).groupby('customer_state')['price'].sum().sort_values(ascending=False).head(5)

    # 步驟3：建立 Excel 工作簿
    print("[3/5] 建立 Excel 工作簿...")
    wb = Workbook()
    ws = wb.active
    ws.title = '執行摘要'

    # 設定頁面寬度
    ws.column_dimensions['A'].width = 25
    for col in range(2, 6):
        ws.column_dimensions[get_column_letter(col)].width = 18

    # 步驟4：設計報表佈局
    print("[4/5] 設計報表佈局...")

    # 標題區域
    ws.merge_cells('A1:E1')
    title = ws['A1']
    title.value = '執行摘要儀表板 - 2024年度'
    title.font = Font(bold=True, size=18, color='FFFFFF')
    title.fill = PatternFill(start_color='1F4E78', end_color='1F4E78', fill_type='solid')
    title.alignment = Alignment(horizontal='center', vertical='center')
    ws.row_dimensions[1].height = 35

    # 生成日期
    ws['A2'] = f'報告日期：{datetime.now().strftime("%Y-%m-%d %H:%M")}'
    ws['A2'].font = Font(italic=True, size=9)

    # 關鍵指標區域（KPI Cards）
    current_row = 4

    kpi_data = [
        {
            'title': '總營收',
            'value': f'R$ {total_revenue:,.2f}',
            'subtitle': '銷售總額',
            'color': '70AD47'  # 綠色
        },
        {
            'title': '訂單總數',
            'value': f'{total_orders:,}',
            'subtitle': '已完成訂單',
            'color': '4472C4'  # 藍色
        },
        {
            'title': '客戶總數',
            'value': f'{total_customers:,}',
            'subtitle': '獨立客戶',
            'color': 'C5504A'  # 紅色
        },
        {
            'title': '平均訂單值',
            'value': f'R$ {avg_order_value:.2f}',
            'subtitle': '客單價',
            'color': 'FFC000'  # 黃色
        }
    ]

    for idx, kpi in enumerate(kpi_data):
        # 計算列位置（2列 x 2行）
        col_offset = idx % 2
        row_offset = idx // 2

        start_row = current_row + row_offset * 5
        start_col = col_offset * 3 + 1

        # 繪製 KPI 卡片
        ws.merge_cells(
            start_row=start_row,
            start_column=start_col,
            end_row=start_row,
            end_column=start_col + 1
        )

        title_cell = ws.cell(row=start_row, column=start_col)
        title_cell.value = kpi['title']
        title_cell.font = Font(bold=True, size=11, color='FFFFFF')
        title_cell.fill = PatternFill(start_color=kpi['color'], end_color=kpi['color'], fill_type='solid')
        title_cell.alignment = Alignment(horizontal='center', vertical='center')
        ws.row_dimensions[start_row].height = 20

        # 數值
        ws.merge_cells(
            start_row=start_row + 1,
            start_column=start_col,
            end_row=start_row + 2,
            end_column=start_col + 1
        )

        value_cell = ws.cell(row=start_row + 1, column=start_col)
        value_cell.value = kpi['value']
        value_cell.font = Font(bold=True, size=14)
        value_cell.alignment = Alignment(horizontal='center', vertical='center')
        value_cell.fill = PatternFill(start_color='F0F0F0', end_color='F0F0F0', fill_type='solid')
        ws.row_dimensions[start_row + 1].height = 25
        ws.row_dimensions[start_row + 2].height = 15

        # 副標題
        ws.merge_cells(
            start_row=start_row + 3,
            start_column=start_col,
            end_row=start_row + 3,
            end_column=start_col + 1
        )

        subtitle_cell = ws.cell(row=start_row + 3, column=start_col)
        subtitle_cell.value = kpi['subtitle']
        subtitle_cell.font = Font(size=9, italic=True, color='666666')
        subtitle_cell.alignment = Alignment(horizontal='center', vertical='center')

    # 性能指標區域
    current_row = 14

    ws.merge_cells(f'A{current_row}:E{current_row}')
    performance_header = ws[f'A{current_row}']
    performance_header.value = '性能指標'
    performance_header.font = Font(bold=True, size=12, color='FFFFFF')
    performance_header.fill = PatternFill(start_color='366092', end_color='366092', fill_type='solid')
    performance_header.alignment = Alignment(horizontal='left', vertical='center')
    ws.row_dimensions[current_row].height = 20

    performance_data = [
        ['配送完成率', f'{delivery_rate:.1f}%'],
        ['平均評分', f'{avg_rating:.2f} / 5.0'],
        ['滿意度', f'{satisfaction_rate:.1f}%'],
        ['年度成長率', f'{growth_rate:.1f}%']
    ]

    for offset, (metric, value) in enumerate(performance_data):
        row = current_row + 1 + offset

        # 指標名稱
        cell_metric = ws.cell(row=row, column=1, value=metric)
        cell_metric.font = Font(bold=True)
        cell_metric.border = Border(
            bottom=Side(style='thin', color='CCCCCC')
        )

        # 指標值
        cell_value = ws.cell(row=row, column=2, value=value)
        cell_value.font = Font(bold=True, size=12)
        cell_value.alignment = Alignment(horizontal='right')
        cell_value.border = Border(
            bottom=Side(style='thin', color='CCCCCC')
        )

        # 進度條（視覺化）
        ws.merge_cells(start_row=row, start_column=3, end_row=row, end_column=5)
        cell_bar = ws.cell(row=row, column=3)

        # 設定顏色條寬度（根據百分比）
        if '%' in value:
            percentage = float(value.rstrip('%')) / 100
            if percentage > 0.8:
                bar_color = '70AD47'  # 綠色
            elif percentage > 0.6:
                bar_color = 'FFC000'  # 黃色
            else:
                bar_color = 'C5504A'  # 紅色

            cell_bar.fill = PatternFill(start_color=bar_color, end_color=bar_color, fill_type='solid')
        cell_bar.border = Border(
            bottom=Side(style='thin', color='CCCCCC')
        )

    # 收入來源區域
    current_row = 20

    ws.merge_cells(f'A{current_row}:E{current_row}')
    revenue_header = ws[f'A{current_row}']
    revenue_header.value = '地區收入排名'
    revenue_header.font = Font(bold=True, size=12, color='FFFFFF')
    revenue_header.fill = PatternFill(start_color='366092', end_color='366092', fill_type='solid')
    revenue_header.alignment = Alignment(horizontal='left', vertical='center')
    ws.row_dimensions[current_row].height = 20

    # 列標題
    headers = ['排名', '州', '收入 (R$)', '佔比']
    for col_idx, header in enumerate(headers, start=1):
        cell = ws.cell(row=current_row + 1, column=col_idx, value=header)
        cell.font = Font(bold=True, color='FFFFFF')
        cell.fill = PatternFill(start_color='4472C4', end_color='4472C4', fill_type='solid')

    # 填充資料
    total_state_revenue = state_revenue.sum()
    for rank, (state, revenue) in enumerate(state_revenue.items(), start=1):
        row = current_row + 1 + rank

        ws.cell(row=row, column=1, value=rank)
        ws.cell(row=row, column=2, value=state)
        cell_revenue = ws.cell(row=row, column=3, value=revenue)
        cell_revenue.number_format = '#,##0.00'
        cell_percent = ws.cell(row=row, column=4, value=revenue / total_state_revenue)
        cell_percent.number_format = '0.0%'

    # 步驟5：保存檔案
    print("[5/5] 保存檔案...")
    output_file = '/home/justin/web-projects/excel-python-data-analysis/week07-08_openpyxl-mastery/case08_executive_summary.xlsx'
    wb.save(output_file)

    # 輸出統計資訊
    print("\n" + "=" * 70)
    print("✅ 執行摘要已生成！")
    print("=" * 70)
    print(f"📊 檔案位置：{output_file}")
    print(f"\n✓ KPI 關鍵指標：")
    print(f"  • 總營收：R$ {total_revenue:,.2f}")
    print(f"  • 訂單總數：{total_orders:,}")
    print(f"  • 客戶總數：{total_customers:,}")
    print(f"  • 平均訂單值：R$ {avg_order_value:.2f}")
    print(f"\n✓ 性能指標：")
    print(f"  • 配送完成率：{delivery_rate:.1f}%")
    print(f"  • 平均評分：{avg_rating:.2f} / 5.0")
    print(f"  • 滿意度：{satisfaction_rate:.1f}%")
    print(f"  • 年度成長率：{growth_rate:.1f}%")
    print(f"\n✓ 報表特性：")
    print(f"  • KPI 卡片視覺化設計")
    print(f"  • 彩色編碼突出重點指標")
    print(f"  • 性能進度條視覺化")
    print(f"  • 地區收入排名分析")
    print(f"  • 管理層友善的佈局")


if __name__ == "__main__":
    create_executive_summary()
