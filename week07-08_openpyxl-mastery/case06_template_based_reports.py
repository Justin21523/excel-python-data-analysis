"""
案例6：模板化報表
功能：
1. 定義報表模板
2. 動態填充資料
3. 保持格式一致
4. 可複用設計
5. 批量生成報告

Author: Week 7-8 openpyxl 完全掌握
Date: 2024-12-11
"""

import pandas as pd
from openpyxl import Workbook
from openpyxl.styles import Font, PatternFill, Alignment, Border, Side, numbers
from openpyxl.utils import get_column_letter
from datetime import datetime
import sys
from pathlib import Path
import warnings

warnings.filterwarnings('ignore')

# 新增父路徑到 sys.path
sys.path.insert(0, str(Path(__file__).parent.parent / 'week03-06_pandas-advanced' / 'utils'))

from data_loader import load_olist_data


class ReportTemplate:
    """
    報表模板類別

    提供標準化的報表格式和樣式
    """

    def __init__(self):
        """初始化樣式配置"""
        self.title_font = Font(bold=True, size=16, color='FFFFFF')
        self.title_fill = PatternFill(start_color='1F4E78', end_color='1F4E78', fill_type='solid')
        self.title_alignment = Alignment(horizontal='center', vertical='center', wrap_text=True)

        self.header_font = Font(bold=True, color='FFFFFF', size=11)
        self.header_fill = PatternFill(start_color='366092', end_color='366092', fill_type='solid')
        self.header_alignment = Alignment(horizontal='center', vertical='center', wrap_text=True)

        self.subheader_font = Font(bold=True, size=10, color='FFFFFF')
        self.subheader_fill = PatternFill(start_color='4472C4', end_color='4472C4', fill_type='solid')

        self.border = Border(
            left=Side(style='thin', color='CCCCCC'),
            right=Side(style='thin', color='CCCCCC'),
            top=Side(style='thin', color='CCCCCC'),
            bottom=Side(style='thin', color='CCCCCC')
        )

        self.light_fill = PatternFill(start_color='D9E1F2', end_color='D9E1F2', fill_type='solid')
        self.summary_fill = PatternFill(start_color='E2EFDA', end_color='E2EFDA', fill_type='solid')

    def add_title(self, ws, title, subtitle=None):
        """添加標題"""
        ws.merge_cells('A1:H1')
        title_cell = ws['A1']
        title_cell.value = title
        title_cell.font = self.title_font
        title_cell.fill = self.title_fill
        title_cell.alignment = self.title_alignment
        ws.row_dimensions[1].height = 30

        if subtitle:
            ws.merge_cells('A2:H2')
            subtitle_cell = ws['A2']
            subtitle_cell.value = subtitle
            subtitle_cell.font = Font(size=10, italic=True)
            ws.row_dimensions[2].height = 20

        return 4 if subtitle else 3

    def add_metadata(self, ws, start_row, metadata_dict):
        """添加元資訊（生成日期、資料來源等）"""
        meta_font = Font(size=9, italic=True)
        for offset, (key, value) in enumerate(metadata_dict.items()):
            row = start_row + offset
            ws.cell(row=row, column=1, value=f"{key}：").font = meta_font
            ws.cell(row=row, column=2, value=value).font = meta_font

        return start_row + len(metadata_dict) + 1

    def add_table(self, ws, df, start_row, title=None):
        """添加資料表"""
        if title:
            ws.merge_cells(f'A{start_row}:H{start_row}')
            title_cell = ws.cell(row=start_row, column=1, value=title)
            title_cell.font = self.subheader_font
            title_cell.fill = self.subheader_fill
            title_cell.alignment = Alignment(horizontal='left', vertical='center')
            ws.row_dimensions[start_row].height = 20
            start_row += 1

        # 寫入標題
        for col_idx, header in enumerate(df.columns, start=1):
            cell = ws.cell(row=start_row, column=col_idx, value=header)
            cell.font = self.header_font
            cell.fill = self.header_fill
            cell.alignment = self.header_alignment
            cell.border = self.border

        # 寫入資料
        for row_offset, (idx, row_data) in enumerate(df.iterrows(), start=1):
            row_idx = start_row + row_offset
            for col_idx, value in enumerate(row_data, start=1):
                cell = ws.cell(row=row_idx, column=col_idx, value=value)
                cell.border = self.border

                # 設定格式
                if isinstance(value, float):
                    if col_idx > 1:
                        cell.number_format = '#,##0.00'

        # 調整欄寬
        for col_idx in range(1, len(df.columns) + 1):
            ws.column_dimensions[get_column_letter(col_idx)].width = 15

        return start_row + len(df) + 2

    def add_summary(self, ws, start_row, summary_data):
        """添加統計摘要"""
        ws.merge_cells(f'A{start_row}:H{start_row}')
        summary_title = ws.cell(row=start_row, column=1, value='統計摘要')
        summary_title.font = self.subheader_font
        summary_title.fill = self.subheader_fill
        ws.row_dimensions[start_row].height = 20

        start_row += 1

        for offset, (key, value) in enumerate(summary_data.items()):
            row = start_row + offset
            key_cell = ws.cell(row=row, column=1, value=key)
            value_cell = ws.cell(row=row, column=2, value=value)

            key_cell.font = Font(bold=True)
            key_cell.fill = self.light_fill
            key_cell.border = self.border

            if isinstance(value, float):
                value_cell.number_format = '#,##0.00'
            elif isinstance(value, int):
                value_cell.number_format = '#,##0'

            value_cell.border = self.border

        return start_row + len(summary_data) + 1


def create_template_based_reports():
    """
    建立模板化報表

    流程：
    1. 載入資料
    2. 初始化模板
    3. 為不同部門生成報告
    4. 保持格式一致
    """

    print("=" * 70)
    print("案例6：模板化報表")
    print("=" * 70)

    # 步驟1：載入資料
    print("\n[1/4] 載入 Olist 資料...")
    try:
        orders, order_items, products, customers, sellers, payments, reviews = load_olist_data(verbose=False)
    except Exception as e:
        print(f"資料載入失敗：{e}")
        return

    # 步驟2：初始化模板
    print("[2/4] 初始化報表模板...")
    template = ReportTemplate()

    # 步驟3：準備各部門報告資料
    print("[3/4] 準備報告資料...")

    # 銷售部報告
    sales_df = products.merge(
        order_items[['product_id', 'price']],
        on='product_id'
    ).groupby('product_category_name').agg({
        'price': ['sum', 'count', 'mean']
    }).reset_index()

    sales_df.columns = ['類別', '銷售額', '銷售件數', '平均價格']
    sales_df = sales_df.sort_values('銷售額', ascending=False).head(10)

    # 客戶部報告
    customer_df = customers.merge(
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

    customer_df.columns = ['州', '客戶數', '總銷售額', '平均消費', '訂單數']
    customer_df = customer_df.sort_values('總銷售額', ascending=False).head(10)

    # 供應商部報告
    supplier_df = sellers.merge(
        order_items[['seller_id', 'price']],
        on='seller_id'
    ).groupby(['seller_id', 'seller_city']).agg({
        'price': ['sum', 'count', 'mean']
    }).reset_index()

    supplier_df.columns = ['供應商ID', '城市', '銷售額', '訂單數', '平均商品價格']
    supplier_df = supplier_df.sort_values('銷售額', ascending=False).head(10)

    # 步驟4：生成報告
    print("[4/4] 生成報告...")

    # 建立工作簿
    wb = Workbook()
    wb.remove(wb.active)

    # 銷售部報告
    ws_sales = wb.create_sheet('銷售報告')
    current_row = template.add_title(ws_sales, '📊 銷售部月度報告', '2024年12月')
    current_row = template.add_metadata(
        ws_sales,
        current_row,
        {
            '報告日期': datetime.now().strftime('%Y-%m-%d'),
            '資料來源': 'Olist 電商平台',
            '統計週期': '全年度'
        }
    )
    current_row += 1
    current_row = template.add_table(ws_sales, sales_df, current_row, '產品類別銷售排名')
    current_row = template.add_summary(
        ws_sales,
        current_row,
        {
            '總銷售額': sales_df['銷售額'].sum(),
            '總銷售件數': int(sales_df['銷售件數'].sum()),
            '平均商品價格': sales_df['平均價格'].mean(),
            '最高銷售額': sales_df['銷售額'].max(),
            '平均每類銷售額': sales_df['銷售額'].mean()
        }
    )

    # 客戶部報告
    ws_customer = wb.create_sheet('客戶報告')
    current_row = template.add_title(ws_customer, '👥 客戶部月度報告', '2024年12月')
    current_row = template.add_metadata(
        ws_customer,
        current_row,
        {
            '報告日期': datetime.now().strftime('%Y-%m-%d'),
            '資料來源': 'Olist 客戶資料庫',
            '統計週期': '全年度'
        }
    )
    current_row += 1
    current_row = template.add_table(ws_customer, customer_df, current_row, '地區客戶統計')
    current_row = template.add_summary(
        ws_customer,
        current_row,
        {
            '總客戶數': int(customer_df['客戶數'].sum()),
            '總銷售額': customer_df['總銷售額'].sum(),
            '平均消費金額': customer_df['平均消費'].mean(),
            '訂單總數': int(customer_df['訂單數'].sum()),
            '平均客戶消費': customer_df['總銷售額'].sum() / customer_df['客戶數'].sum()
        }
    )

    # 供應商部報告
    ws_supplier = wb.create_sheet('供應商報告')
    current_row = template.add_title(ws_supplier, '🏢 供應商部月度報告', '2024年12月')
    current_row = template.add_metadata(
        ws_supplier,
        current_row,
        {
            '報告日期': datetime.now().strftime('%Y-%m-%d'),
            '資料來源': 'Olist 供應商系統',
            '統計週期': '全年度'
        }
    )
    current_row += 1
    current_row = template.add_table(ws_supplier, supplier_df, current_row, '供應商績效排名')
    current_row = template.add_summary(
        ws_supplier,
        current_row,
        {
            '總供應商數': int(supplier_df['供應商ID'].nunique()),
            '總銷售額': supplier_df['銷售額'].sum(),
            '平均商品價格': supplier_df['平均商品價格'].mean(),
            '訂單總數': int(supplier_df['訂單數'].sum()),
            '最高銷售額': supplier_df['銷售額'].max()
        }
    )

    # 保存檔案
    output_file = '/home/justin/web-projects/excel-python-data-analysis/week07-08_openpyxl-mastery/case06_template_reports.xlsx'
    wb.save(output_file)

    # 輸出統計資訊
    print("\n" + "=" * 70)
    print("✅ 模板化報表已生成！")
    print("=" * 70)
    print(f"📊 檔案位置：{output_file}")
    print(f"📊 報告數量：3 份（銷售、客戶、供應商）")
    print(f"\n✓ 模板特性：")
    print(f"  • 統一的視覺風格")
    print(f"  • 標準化的報表結構")
    print(f"  • 可複用的設計")
    print(f"  • 自動元資訊填充")
    print(f"  • 彙總統計自動計算")


if __name__ == "__main__":
    create_template_based_reports()
