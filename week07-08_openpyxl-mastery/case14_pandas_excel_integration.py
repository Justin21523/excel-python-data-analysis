"""
案例14：Pandas 和 Excel 完整整合
功能：
1. DataFrame 直接寫入 Excel
2. 範圍格式化應用
3. 樞紐表資料轉換
4. 高效資料轉換
5. 批量資料處理
6. 完整工作流程整合

Author: Week 7-8 openpyxl 完全掌握
Date: 2024-12-11
"""

import pandas as pd
from openpyxl import load_workbook, Workbook
from openpyxl.styles import Font, PatternFill, Alignment, Border, Side, numbers
from openpyxl.utils import get_column_letter
from openpyxl.utils.dataframe import dataframe_to_rows
from openpyxl.worksheet.table import Table, TableStyleInfo
import sys
from pathlib import Path
import warnings
from datetime import datetime

warnings.filterwarnings('ignore')

# 新增父路徑到 sys.path
sys.path.insert(0, str(Path(__file__).parent.parent / 'week03-06_pandas-advanced' / 'utils'))

from data_loader import load_olist_data


class PandasExcelIntegration:
    """
    Pandas 和 Excel 完整整合類別

    功能：
    - 高效資料轉換
    - 樞紐表生成
    - 格式化應用
    - 工作流程自動化
    """

    def __init__(self, output_dir=None):
        """初始化"""
        self.output_dir = output_dir or Path.cwd()
        self.wb = None
        self.style_config = self._init_styles()

    def _init_styles(self):
        """初始化樣式配置"""
        return {
            'title_font': Font(bold=True, size=14, color='FFFFFF'),
            'title_fill': PatternFill(start_color='1F4E78', end_color='1F4E78', fill_type='solid'),
            'header_font': Font(bold=True, color='FFFFFF', size=11),
            'header_fill': PatternFill(start_color='366092', end_color='366092', fill_type='solid'),
            'currency_format': '#,##0.00',
            'percent_format': '0.00%',
            'int_format': '#,##0',
            'border': Border(
                left=Side(style='thin', color='CCCCCC'),
                right=Side(style='thin', color='CCCCCC'),
                top=Side(style='thin', color='CCCCCC'),
                bottom=Side(style='thin', color='CCCCCC')
            )
        }

    def create_workbook(self):
        """建立工作簿"""
        self.wb = Workbook()
        self.wb.remove(self.wb.active)

    def write_dataframe(self, df, sheet_name, title=None, include_filter=True):
        """
        將 DataFrame 寫入工作表

        參數：
        - df：DataFrame 資料
        - sheet_name：工作表名稱
        - title：工作表標題
        - include_filter：是否包含自動篩選
        """
        ws = self.wb.create_sheet(sheet_name)

        # 標題行
        if title:
            ws.merge_cells('A1:F1')
            title_cell = ws['A1']
            title_cell.value = title
            title_cell.font = self.style_config['title_font']
            title_cell.fill = self.style_config['title_fill']
            title_cell.alignment = Alignment(horizontal='center', vertical='center')
            ws.row_dimensions[1].height = 25

            start_row = 3
        else:
            start_row = 1

        # 列標題
        for col_idx, header in enumerate(df.columns, start=1):
            cell = ws.cell(row=start_row, column=col_idx, value=header)
            cell.font = self.style_config['header_font']
            cell.fill = self.style_config['header_fill']
            cell.alignment = Alignment(horizontal='center', vertical='center', wrap_text=True)
            cell.border = self.style_config['border']

        # 資料行
        for row_idx, (_, row) in enumerate(df.iterrows(), start=start_row + 1):
            for col_idx, value in enumerate(row.values, start=1):
                cell = ws.cell(row=row_idx, column=col_idx, value=value)
                cell.border = self.style_config['border']

                # 自動格式化
                if isinstance(value, float):
                    if 'price' in df.columns[col_idx - 1].lower() or 'amount' in df.columns[col_idx - 1].lower():
                        cell.number_format = self.style_config['currency_format']
                    elif 'rate' in df.columns[col_idx - 1].lower() or 'percent' in df.columns[col_idx - 1].lower():
                        cell.number_format = self.style_config['percent_format']

                elif isinstance(value, int):
                    cell.number_format = self.style_config['int_format']

        # 調整欄寬
        for col_idx, col_letter in enumerate(get_column_letter(i) for i in range(1, len(df.columns) + 1)):
            ws.column_dimensions[col_letter].width = 15

        # 添加自動篩選
        if include_filter:
            ws.auto_filter.ref = f'A{start_row}:{get_column_letter(len(df.columns))}{start_row + len(df)}'

    def create_pivot_table(self, df, index, columns, values, aggfunc='sum', sheet_name=None):
        """
        建立樞紐表

        參數：
        - df：DataFrame 資料
        - index：行標籤欄位
        - columns：列標籤欄位
        - values：數值欄位
        - aggfunc：聚合函數
        - sheet_name：工作表名稱
        """
        if sheet_name is None:
            sheet_name = 'Pivot Table'

        # 建立樞紐表
        pivot_df = pd.pivot_table(
            df,
            index=index,
            columns=columns,
            values=values,
            aggfunc=aggfunc,
            fill_value=0
        )

        # 寫入工作表
        self.write_dataframe(
            pivot_df.reset_index(),
            sheet_name,
            title=f'樞紐表：{index} × {columns}',
            include_filter=False
        )

    def create_summary_dashboard(self, df, metrics_dict, sheet_name='儀表板'):
        """
        建立彙總儀表板

        參數：
        - df：DataFrame 資料
        - metrics_dict：指標字典 {指標名稱: (欄位名稱, 計算函數)}
        - sheet_name：工作表名稱
        """
        ws = self.wb.create_sheet(sheet_name)

        # 標題
        ws.merge_cells('A1:D1')
        title_cell = ws['A1']
        title_cell.value = '📊 彙總儀表板'
        title_cell.font = self.style_config['title_font']
        title_cell.fill = self.style_config['title_fill']
        title_cell.alignment = Alignment(horizontal='center', vertical='center')
        ws.row_dimensions[1].height = 25

        # 生成時間
        ws['A3'] = f'生成時間：{datetime.now().strftime("%Y-%m-%d %H:%M:%S")}'

        current_row = 5

        # 指標區域
        for metric_name, (column, func) in metrics_dict.items():
            # 標籤
            cell_label = ws.cell(row=current_row, column=1, value=metric_name)
            cell_label.font = Font(bold=True)

            # 數值
            if callable(func):
                value = func(df[column])
            else:
                value = df[column].agg(func)

            cell_value = ws.cell(row=current_row, column=2, value=value)
            cell_value.font = Font(bold=True, size=12)

            if isinstance(value, float):
                cell_value.number_format = self.style_config['currency_format']
            elif isinstance(value, int):
                cell_value.number_format = self.style_config['int_format']

            current_row += 1

        ws.column_dimensions['A'].width = 20
        ws.column_dimensions['B'].width = 20

    def save(self, filename):
        """保存工作簿"""
        output_path = Path(self.output_dir) / filename
        self.wb.save(output_path)
        print(f'✓ 工作簿已保存：{output_path}')
        return output_path


def create_pandas_excel_integration():
    """
    建立 Pandas 和 Excel 完整整合報告

    流程：
    1. 載入資料
    2. 初始化整合系統
    3. 建立各類資料表
    4. 建立樞紐表
    5. 建立彙總儀表板
    6. 保存檔案
    """

    print("=" * 70)
    print("案例14：Pandas 和 Excel 完整整合")
    print("=" * 70)

    # 步驟1：載入資料
    print("\n[1/6] 載入 Olist 資料...")
    try:
        orders, order_items, products, customers, sellers, payments, reviews = load_olist_data(verbose=False)
    except Exception as e:
        print(f"資料載入失敗：{e}")
        return

    # 步驟2：初始化整合系統
    print("[2/6] 初始化整合系統...")
    output_dir = '/home/justin/web-projects/excel-python-data-analysis/week07-08_openpyxl-mastery'
    integration = PandasExcelIntegration(output_dir)
    integration.create_workbook()

    # 步驟3：準備資料
    print("[3/6] 準備資料...")

    # 資料1：訂單和訂單明細
    df_orders_detail = orders[['order_id', 'customer_id', 'order_purchase_timestamp', 'order_status']].copy()
    df_orders_detail = df_orders_detail.merge(
        order_items[['order_id', 'price', 'freight_value', 'product_id']],
        on='order_id'
    )
    df_orders_detail = df_orders_detail.merge(
        products[['product_id', 'product_category_name']],
        on='product_id'
    )

    df_orders_detail = df_orders_detail.rename(columns={
        'order_purchase_timestamp': '購買時間',
        'order_status': '訂單狀態',
        'price': '商品價格',
        'freight_value': '運費',
        'product_category_name': '產品類別'
    })

    # 資料2：賣家績效
    df_seller_performance = sellers.merge(
        order_items[['seller_id', 'price']].groupby('seller_id').agg({
            'price': ['sum', 'count', 'mean']
        }).reset_index(),
        on='seller_id',
        how='left'
    ).fillna(0)

    df_seller_performance.columns = ['seller_id', 'zip_code', 'city', 'state', '銷售額', '銷售件數', '平均價格']

    # 資料3：客戶分析
    df_customer_analysis = customers.merge(
        orders[['customer_id', 'order_id']],
        on='customer_id'
    ).merge(
        order_items[['order_id', 'price']],
        on='order_id'
    )

    df_customer_analysis = df_customer_analysis.groupby('customer_id').agg({
        'customer_unique_id': 'first',
        'customer_city': 'first',
        'customer_state': 'first',
        'price': ['sum', 'count', 'mean'],
        'order_id': 'nunique'
    }).reset_index()

    df_customer_analysis.columns = ['客戶ID', '唯一客戶', '城市', '州', '總消費', '購買件數', '平均消費', '訂單數']

    # 步驟4：寫入資料表
    print("[4/6] 寫入資料表...")

    integration.write_dataframe(
        df_orders_detail[['order_id', '購買時間', '訂單狀態', '商品價格', '運費', '產品類別']].head(100),
        '訂單詳情',
        title='📋 訂單詳情（前100行）'
    )

    integration.write_dataframe(
        df_seller_performance[['seller_id', 'city', 'state', '銷售額', '銷售件數', '平均價格']].head(50),
        '賣家績效',
        title='👤 賣家績效分析'
    )

    integration.write_dataframe(
        df_customer_analysis.head(50),
        '客戶分析',
        title='👥 客戶分析'
    )

    # 步驟5：建立樞紐表
    print("[5/6] 建立樞紐表...")

    # 樞紐表1：按類別和狀態統計
    pivot_category_status = df_orders_detail.pivot_table(
        index='產品類別',
        columns='訂單狀態',
        values='商品價格',
        aggfunc='sum',
        fill_value=0
    )

    integration.write_dataframe(
        pivot_category_status.reset_index(),
        '樞紐表_類別狀態',
        title='樞紐表：產品類別 × 訂單狀態'
    )

    # 樞紐表2：按州和類別統計
    df_location_category = df_orders_detail.merge(
        customers[['customer_id', 'customer_state']],
        on='customer_id',
        how='left'
    )

    pivot_state_category = df_location_category.pivot_table(
        index='customer_state',
        columns='產品類別',
        values='商品價格',
        aggfunc='sum',
        fill_value=0
    )

    integration.write_dataframe(
        pivot_state_category.reset_index().head(10),
        '樞紐表_州類別',
        title='樞紐表：州 × 產品類別（前10行）'
    )

    # 步驟6：建立彙總儀表板
    print("[6/6] 建立彙總儀表板...")

    metrics = {
        '訂單總數': ('order_id', 'nunique'),
        '銷售總額': ('商品價格', 'sum'),
        '平均訂單值': ('商品價格', 'mean'),
        '平均運費': ('運費', 'mean'),
        '客戶總數': ('customer_id', 'nunique'),
        '平均評分': ('review_score', 'mean') if 'review_score' in df_orders_detail.columns else ('order_id', lambda x: 4.5)
    }

    # 重新準備資料以便使用所有指標
    df_summary = orders[['order_id', 'customer_id']].merge(
        order_items[['order_id', 'price', 'freight_value']],
        on='order_id'
    )

    integration.create_summary_dashboard(
        df_summary,
        {
            '訂單總數': ('order_id', 'nunique'),
            '銷售總額': ('price', 'sum'),
            '平均訂單值': ('price', 'mean'),
            '平均運費': ('freight_value', 'mean'),
            '客戶總數': ('customer_id', 'nunique')
        },
        sheet_name='彙總儀表板'
    )

    # 保存
    output_file = integration.save('case14_pandas_excel_integration.xlsx')

    # 輸出統計資訊
    print("\n" + "=" * 70)
    print("✅ Pandas 和 Excel 完整整合報告已生成！")
    print("=" * 70)
    print(f"📊 檔案位置：{output_file}")
    print(f"📊 工作表數量：6 個")
    print(f"  1. 訂單詳情 - 訂單和訂單明細資料")
    print(f"  2. 賣家績效 - 賣家績效分析")
    print(f"  3. 客戶分析 - 客戶詳細分析")
    print(f"  4. 樞紐表_類別狀態 - 類別與訂單狀態交叉分析")
    print(f"  5. 樞紐表_州類別 - 州與產品類別交叉分析")
    print(f"  6. 彙總儀表板 - 關鍵指標彙總")
    print(f"\n✓ 整合特性：")
    print(f"  • DataFrame 直接寫入 Excel")
    print(f"  • 自動格式化：貨幣、百分比、整數")
    print(f"  • 樞紐表生成：多維度交叉分析")
    print(f"  • 彙總儀表板：KPI 指標展示")
    print(f"  • 自動篩選：便於資料查詢")
    print(f"  • 統一樣式：專業化報表設計")
    print(f"\n✓ 工作流程優勢：")
    print(f"  • 無需手動複製粘貼")
    print(f"  • 自動化資料轉換")
    print(f"  • 高效批量處理")
    print(f"  • 降低錯誤風險")


if __name__ == "__main__":
    create_pandas_excel_integration()
