"""
案例13：完整自動化系統
功能：
1. 批量報表生成
2. 動態工作表創建
3. 多層級驗證
4. 自動編號系統
5. 批量樣式應用
6. 日誌記錄

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
import logging

warnings.filterwarnings('ignore')

# 新增父路徑到 sys.path
sys.path.insert(0, str(Path(__file__).parent.parent / 'week03-06_pandas-advanced' / 'utils'))

from data_loader import load_olist_data


# 配置日誌
logging.basicConfig(
    level=logging.INFO,
    format='[%(asctime)s] %(levelname)s: %(message)s',
    handlers=[
        logging.StreamHandler()
    ]
)
logger = logging.getLogger(__name__)


class ExcelReportAutomation:
    """
    Excel 報表自動化系統

    功能：
    - 批量生成報表
    - 動態工作表管理
    - 自動樣式應用
    - 日誌記錄
    """

    def __init__(self, output_dir=None):
        """
        初始化系統

        參數：
        - output_dir：輸出目錄
        """
        self.output_dir = output_dir or Path.cwd()
        self.wb = Workbook()
        self.wb.remove(self.wb.active)
        self.ws_index = self.wb.create_sheet('目錄', 0)
        self.sheet_list = []
        self.style_config = self._init_styles()
        logger.info('Excel 自動化系統初始化完成')

    def _init_styles(self):
        """初始化樣式配置"""
        return {
            'title': {
                'font': Font(bold=True, size=14, color='FFFFFF'),
                'fill': PatternFill(start_color='1F4E78', end_color='1F4E78', fill_type='solid'),
                'alignment': Alignment(horizontal='center', vertical='center')
            },
            'header': {
                'font': Font(bold=True, color='FFFFFF', size=11),
                'fill': PatternFill(start_color='366092', end_color='366092', fill_type='solid'),
                'alignment': Alignment(horizontal='center', vertical='center', wrap_text=True)
            },
            'subheader': {
                'font': Font(bold=True, size=10, color='FFFFFF'),
                'fill': PatternFill(start_color='4472C4', end_color='4472C4', fill_type='solid'),
                'alignment': Alignment(horizontal='left', vertical='center')
            },
            'border': Border(
                left=Side(style='thin', color='CCCCCC'),
                right=Side(style='thin', color='CCCCCC'),
                top=Side(style='thin', color='CCCCCC'),
                bottom=Side(style='thin', color='CCCCCC')
            ),
            'light': PatternFill(start_color='F0F0F0', end_color='F0F0F0', fill_type='solid'),
            'summary': PatternFill(start_color='E2EFDA', end_color='E2EFDA', fill_type='solid')
        }

    def add_sheet(self, sheet_name, df, title=None, include_summary=True):
        """
        添加工作表

        參數：
        - sheet_name：工作表名稱
        - df：DataFrame 資料
        - title：工作表標題
        - include_summary：是否包含統計摘要
        """
        logger.info(f'添加工作表：{sheet_name}')

        # 建立工作表
        ws = self.wb.create_sheet(sheet_name)
        self.sheet_list.append(sheet_name)

        # 標題
        if title:
            ws.merge_cells('A1:H1')
            title_cell = ws['A1']
            title_cell.value = title
            title_cell.font = self.style_config['title']['font']
            title_cell.fill = self.style_config['title']['fill']
            title_cell.alignment = self.style_config['title']['alignment']
            ws.row_dimensions[1].height = 25

            start_row = 3
        else:
            start_row = 1

        # 列標題
        for col_idx, header in enumerate(df.columns, start=1):
            cell = ws.cell(row=start_row, column=col_idx, value=header)
            cell.font = self.style_config['header']['font']
            cell.fill = self.style_config['header']['fill']
            cell.alignment = self.style_config['header']['alignment']
            cell.border = self.style_config['border']

        # 資料
        for row_offset, (idx, row) in enumerate(df.iterrows(), start=1):
            row_idx = start_row + row_offset
            for col_idx, value in enumerate(row.values, start=1):
                cell = ws.cell(row=row_idx, column=col_idx, value=value)
                cell.border = self.style_config['border']

                if isinstance(value, float):
                    cell.number_format = '#,##0.00'

        # 統計摘要
        if include_summary and len(df) > 0:
            summary_row = start_row + len(df) + 2

            ws.merge_cells(f'A{summary_row}:H{summary_row}')
            summary_title = ws.cell(row=summary_row, column=1, value='統計摘要')
            summary_title.font = Font(bold=True)
            summary_title.fill = self.style_config['summary']

            # 統計項目
            stats_row = summary_row + 1

            # 記錄數
            ws.cell(row=stats_row, column=1, value='記錄數：')
            ws.cell(row=stats_row, column=2, value=len(df))

            # 數值欄統計
            numeric_cols = df.select_dtypes(include=['float64', 'int64']).columns
            for col in numeric_cols:
                stats_row += 1
                ws.cell(row=stats_row, column=1, value=f'{col}（合計）：')
                cell = ws.cell(row=stats_row, column=2, value=df[col].sum())
                cell.number_format = '#,##0.00'

                ws.cell(row=stats_row, column=3, value=f'{col}（平均）：')
                cell = ws.cell(row=stats_row, column=4, value=df[col].mean())
                cell.number_format = '#,##0.00'

        # 調整欄寬
        for col_idx in range(1, len(df.columns) + 1):
            ws.column_dimensions[get_column_letter(col_idx)].width = 15

        logger.info(f'工作表 {sheet_name} 添加完成（{len(df)} 行）')

    def create_index(self, title='報告索引'):
        """建立目錄工作表"""
        logger.info('建立目錄工作表')

        # 標題
        self.ws_index.merge_cells('A1:C1')
        title_cell = self.ws_index['A1']
        title_cell.value = title
        title_cell.font = self.style_config['title']['font']
        title_cell.fill = self.style_config['title']['fill']
        title_cell.alignment = self.style_config['title']['alignment']
        self.ws_index.row_dimensions[1].height = 25

        # 說明
        self.ws_index['A3'] = f'生成時間：{datetime.now().strftime("%Y-%m-%d %H:%M:%S")}'
        self.ws_index['A4'] = f'報告版本：1.0'

        # 列標題
        headers = ['序號', '工作表名稱', '描述']
        for col_idx, header in enumerate(headers, start=1):
            cell = self.ws_index.cell(row=6, column=col_idx, value=header)
            cell.font = self.style_config['header']['font']
            cell.fill = self.style_config['header']['fill']
            cell.alignment = self.style_config['header']['alignment']
            cell.border = self.style_config['border']

        # 工作表列表
        for row_offset, sheet_name in enumerate(self.sheet_list, start=1):
            row_idx = 6 + row_offset
            cell1 = self.ws_index.cell(row=row_idx, column=1, value=row_offset)
            cell1.border = self.style_config['border']
            cell1.alignment = Alignment(horizontal='center')

            cell2 = self.ws_index.cell(row=row_idx, column=2, value=sheet_name)
            cell2.border = self.style_config['border']

            cell3 = self.ws_index.cell(row=row_idx, column=3, value=f'{sheet_name} 詳細資料')
            cell3.border = self.style_config['border']

        self.ws_index.column_dimensions['A'].width = 8
        self.ws_index.column_dimensions['B'].width = 20
        self.ws_index.column_dimensions['C'].width = 30

    def save(self, filename):
        """保存工作簿"""
        output_path = Path(self.output_dir) / filename
        self.wb.save(output_path)
        logger.info(f'工作簿已保存：{output_path}')
        return output_path


def create_full_automation_report():
    """
    建立完整自動化系統報告

    流程：
    1. 載入資料
    2. 初始化自動化系統
    3. 為不同維度生成報表
    4. 建立目錄
    5. 保存檔案
    """

    print("=" * 70)
    print("案例13：完整自動化系統")
    print("=" * 70)

    # 步驟1：載入資料
    print("\n[1/5] 載入 Olist 資料...")
    try:
        orders, order_items, products, customers, sellers, payments, reviews = load_olist_data(verbose=False)
    except Exception as e:
        logger.error(f"資料載入失敗：{e}")
        return

    # 步驟2：初始化自動化系統
    print("[2/5] 初始化自動化系統...")
    output_dir = '/home/justin/web-projects/excel-python-data-analysis/week07-08_openpyxl-mastery'
    automation = ExcelReportAutomation(output_dir)

    # 步驟3：為不同維度生成報表
    print("[3/5] 生成多維度報表...")

    # 報表1：按類別統計
    logger.info('生成類別統計報告')
    df_category = products.merge(
        order_items[['product_id', 'price']],
        on='product_id'
    ).groupby('product_category_name').agg({
        'price': ['sum', 'count', 'mean']
    }).reset_index()

    df_category.columns = ['類別', '銷售額', '銷售件數', '平均價格']
    df_category = df_category.sort_values('銷售額', ascending=False).head(15)
    automation.add_sheet(
        '類別統計',
        df_category,
        title='📊 產品類別銷售統計',
        include_summary=True
    )

    # 報表2：按賣家統計
    logger.info('生成賣家統計報告')
    df_seller = sellers.merge(
        order_items[['seller_id', 'price']],
        on='seller_id'
    ).groupby('seller_id').agg({
        'price': ['sum', 'count', 'mean']
    }).reset_index()

    df_seller.columns = ['賣家ID', '銷售額', '銷售件數', '平均價格']
    df_seller = df_seller.sort_values('銷售額', ascending=False).head(20)
    automation.add_sheet(
        '賣家統計',
        df_seller,
        title='👤 賣家績效統計',
        include_summary=True
    )

    # 報表3：按州分統計
    logger.info('生成地區統計報告')
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

    df_state.columns = ['州', '客戶數', '銷售額', '平均消費', '訂單數']
    df_state = df_state.sort_values('銷售額', ascending=False)
    automation.add_sheet(
        '地區分析',
        df_state,
        title='📍 地區銷售分析',
        include_summary=True
    )

    # 報表4：按付款方式統計
    logger.info('生成付款方式統計報告')
    df_payment = payments.groupby('payment_type').agg({
        'payment_value': ['sum', 'mean', 'count']
    }).reset_index()

    df_payment.columns = ['付款方式', '總金額', '平均金額', '筆數']
    df_payment = df_payment.sort_values('總金額', ascending=False)
    automation.add_sheet(
        '付款統計',
        df_payment,
        title='💳 付款方式分析',
        include_summary=True
    )

    # 報表5：評論評分統計
    logger.info('生成評論統計報告')
    df_review = reviews[reviews['review_score'].notna()].copy()
    df_review['評分等級'] = df_review['review_score'].apply(
        lambda x: '★★★★★' if x == 5 else '★★★★' if x == 4 else '★★★' if x == 3 else '★★' if x == 2 else '★'
    )

    df_review_stats = df_review.groupby(['review_score', '評分等級']).size().reset_index(name='評論數')
    df_review_stats = df_review_stats.sort_values('review_score', ascending=False)
    automation.add_sheet(
        '評論統計',
        df_review_stats,
        title='⭐ 評論評分統計',
        include_summary=True
    )

    # 步驟4：建立目錄
    print("[4/5] 建立目錄工作表...")
    automation.create_index(title='📄 報告導航目錄')

    # 步驟5：保存檔案
    print("[5/5] 保存檔案...")
    output_file = automation.save('case13_full_automation_system.xlsx')

    # 輸出統計資訊
    print("\n" + "=" * 70)
    print("✅ 完整自動化系統報告已生成！")
    print("=" * 70)
    print(f"📊 檔案位置：{output_file}")
    print(f"📊 工作表數量：{len(automation.sheet_list)} 個")
    print(f"📊 工作表列表：")
    for idx, sheet_name in enumerate(automation.sheet_list, start=1):
        print(f"   {idx}. {sheet_name}")
    print(f"\n✓ 自動化系統特性：")
    print(f"  • 批量工作表生成")
    print(f"  • 統一樣式應用")
    print(f"  • 自動統計摘要")
    print(f"  • 日誌記錄")
    print(f"  • 可擴展架構")


if __name__ == "__main__":
    create_full_automation_report()
