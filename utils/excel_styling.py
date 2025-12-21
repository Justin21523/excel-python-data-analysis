"""
Excel 樣式設定工具函數庫

包含常用的 openpyxl 樣式設定函數，讓產生精美 Excel 報表更容易。
"""

from openpyxl.styles import Font, PatternFill, Alignment, Border, Side
from openpyxl.utils import get_column_letter
from openpyxl.worksheet.worksheet import Worksheet
from typing import Optional


# ===== 預定義配色方案 =====
COLOR_SCHEMES = {
    'blue': {
        'header_fill': 'HEADER:
header_fill': '366092',  # 深藍色
        'header_font': 'FFFFFF',  # 白色
        'accent': '4472C4',
        'light': 'D9E2F3',
    },
    'green': {
        'header_fill': '548235',  # 深綠色
        'header_font': 'FFFFFF',
        'accent': '70AD47',
        'light': 'E2EFDA',
    },
    'orange': {
        'header_fill': 'C65911',  # 深橘色
        'header_font': 'FFFFFF',
        'accent': 'ED7D31',
        'light': 'FCE4D6',
    },
    'purple': {
        'header_fill': '5B9BD5',  # 紫藍色
        'header_font': 'FFFFFF',
        'accent': '7030A0',
        'light': 'E7E6FA',
    }
}


def apply_header_style(
    ws: Worksheet,
    row: int = 1,
    start_col: int = 1,
    end_col: Optional[int] = None,
    color_scheme: str = 'blue'
) -> None:
    """
    套用標題列樣式

    Parameters:
    -----------
    ws : Worksheet
        要設定的工作表
    row : int
        標題列位置（預設第 1 列）
    start_col : int
        起始欄（預設第 1 欄）
    end_col : int, optional
        結束欄（None 表示到最後一欄）
    color_scheme : str
        配色方案 {'blue', 'green', 'orange', 'purple'}

    Example:
    --------
    >>> apply_header_style(ws, row=1, color_scheme='blue')
    """
    if end_col is None:
        end_col = ws.max_column

    colors = COLOR_SCHEMES.get(color_scheme, COLOR_SCHEMES['blue'])

    header_fill = PatternFill(
        start_color=colors['header_fill'],
        end_color=colors['header_fill'],
        fill_type='solid'
    )
    header_font = Font(
        color=colors['header_font'],
        bold=True,
        size=11
    )
    alignment = Alignment(
        horizontal='center',
        vertical='center'
    )

    for col in range(start_col, end_col + 1):
        cell = ws.cell(row=row, column=col)
        cell.fill = header_fill
        cell.font = header_font
        cell.alignment = alignment


def apply_number_format(
    ws: Worksheet,
    column: int,
    format_type: str = 'number',
    start_row: int = 2
) -> None:
    """
    套用數值格式

    Parameters:
    -----------
    ws : Worksheet
        要設定的工作表
    column : int
        要設定的欄位編號
    format_type : str
        格式類型：
        - 'number': 千分位（1,234）
        - 'decimal': 千分位 + 小數（1,234.56）
        - 'percentage': 百分比（12.34%）
        - 'currency': 貨幣（$1,234.56）
        - 'currency_twd': 新台幣（NT$1,234）
    start_row : int
        起始列（預設第 2 列，跳過標題）

    Example:
    --------
    >>> apply_number_format(ws, column=3, format_type='currency')
    """
    format_codes = {
        'number': '#,##0',
        'decimal': '#,##0.00',
        'percentage': '0.00%',
        'currency': '$#,##0.00',
        'currency_twd': '"NT$"#,##0',
    }

    number_format = format_codes.get(format_type, '#,##0')

    for row in range(start_row, ws.max_row + 1):
        cell = ws.cell(row=row, column=column)
        cell.number_format = number_format


def auto_adjust_column_width(
    ws: Worksheet,
    start_col: int = 1,
    end_col: Optional[int] = None,
    min_width: int = 10,
    max_width: int = 50
) -> None:
    """
    自動調整欄寬

    Parameters:
    -----------
    ws : Worksheet
        要調整的工作表
    start_col : int
        起始欄
    end_col : int, optional
        結束欄（None 表示到最後一欄）
    min_width : int
        最小寬度
    max_width : int
        最大寬度

    Example:
    --------
    >>> auto_adjust_column_width(ws)
    """
    if end_col is None:
        end_col = ws.max_column

    for col in range(start_col, end_col + 1):
        column_letter = get_column_letter(col)
        max_length = 0

        for cell in ws[column_letter]:
            try:
                if cell.value:
                    max_length = max(max_length, len(str(cell.value)))
            except:
                pass

        adjusted_width = max(min_width, min(max_length + 2, max_width))
        ws.column_dimensions[column_letter].width = adjusted_width


def apply_borders(
    ws: Worksheet,
    start_row: int = 1,
    start_col: int = 1,
    end_row: Optional[int] = None,
    end_col: Optional[int] = None,
    border_style: str = 'thin'
) -> None:
    """
    套用框線

    Parameters:
    -----------
    ws : Worksheet
        要設定的工作表
    start_row : int
        起始列
    start_col : int
        起始欄
    end_row : int, optional
        結束列（None 表示到最後一列）
    end_col : int, optional
        結束欄（None 表示到最後一欄）
    border_style : str
        框線樣式 {'thin', 'medium', 'thick'}

    Example:
    --------
    >>> apply_borders(ws, start_row=1, end_row=10)
    """
    if end_row is None:
        end_row = ws.max_row
    if end_col is None:
        end_col = ws.max_column

    side = Side(border_style=border_style, color='000000')
    border = Border(left=side, right=side, top=side, bottom=side)

    for row in range(start_row, end_row + 1):
        for col in range(start_col, end_col + 1):
            cell = ws.cell(row=row, column=col)
            cell.border = border


def freeze_panes(
    ws: Worksheet,
    row: int = 2,
    col: int = 1
) -> None:
    """
    凍結窗格

    Parameters:
    -----------
    ws : Worksheet
        要設定的工作表
    row : int
        凍結列數（從第幾列開始可捲動）
    col : int
        凍結欄數（從第幾欄開始可捲動）

    Example:
    --------
    >>> freeze_panes(ws, row=2, col=1)  # 凍結第一列（標題列）
    """
    cell_position = f"{get_column_letter(col)}{row}"
    ws.freeze_panes = cell_position


def apply_alternating_rows(
    ws: Worksheet,
    start_row: int = 2,
    end_row: Optional[int] = None,
    color: str = 'F2F2F2'
) -> None:
    """
    套用交替列底色（斑馬紋）

    Parameters:
    -----------
    ws : Worksheet
        要設定的工作表
    start_row : int
        起始列（通常是資料列，跳過標題）
    end_row : int, optional
        結束列（None 表示到最後一列）
    color : str
        底色（淺灰色預設）

    Example:
    --------
    >>> apply_alternating_rows(ws, start_row=2)
    """
    if end_row is None:
        end_row = ws.max_row

    fill = PatternFill(start_color=color, end_color=color, fill_type='solid')

    for row in range(start_row, end_row + 1):
        if row % 2 == 0:  # 偶數列
            for col in range(1, ws.max_column + 1):
                ws.cell(row=row, column=col).fill = fill


def apply_table_style(
    ws: Worksheet,
    color_scheme: str = 'blue',
    freeze_header: bool = True,
    auto_width: bool = True,
    borders: bool = True,
    alternating_rows: bool = True
) -> None:
    """
    一鍵套用完整表格樣式

    這個函數整合了多個樣式設定，一次完成專業表格美化。

    Parameters:
    -----------
    ws : Worksheet
        要設定的工作表
    color_scheme : str
        配色方案
    freeze_header : bool
        是否凍結標題列
    auto_width : bool
        是否自動調整欄寬
    borders : bool
        是否套用框線
    alternating_rows : bool
        是否套用交替列底色

    Example:
    --------
    >>> apply_table_style(ws, color_scheme='blue')
    """
    # 1. 標題列樣式
    apply_header_style(ws, color_scheme=color_scheme)

    # 2. 凍結窗格
    if freeze_header:
        freeze_panes(ws, row=2)

    # 3. 自動調整欄寬
    if auto_width:
        auto_adjust_column_width(ws)

    # 4. 套用框線
    if borders:
        apply_borders(ws)

    # 5. 交替列底色
    if alternating_rows:
        apply_alternating_rows(ws)


def highlight_cells(
    ws: Worksheet,
    condition: str,
    column: int,
    color: str = 'FFFF00',  # 黃色
    start_row: int = 2
) -> None:
    """
    根據條件高亮儲存格

    Parameters:
    -----------
    ws : Worksheet
        要設定的工作表
    condition : str
        條件表達式，例如 '>1000', '==0', '<0'
    column : int
        要檢查的欄位
    color : str
        高亮顏色
    start_row : int
        起始列

    Example:
    --------
    >>> highlight_cells(ws, condition='>10000', column=3, color='FFFF00')
    """
    fill = PatternFill(start_color=color, end_color=color, fill_type='solid')

    for row in range(start_row, ws.max_row + 1):
        cell = ws.cell(row=row, column=column)
        if cell.value is not None:
            try:
                # 評估條件
                if eval(f"{cell.value} {condition}"):
                    cell.fill = fill
            except:
                pass


if __name__ == "__main__":
    print("Excel 樣式工具函數庫")
    print("使用範例請參考各函數的 docstring")
