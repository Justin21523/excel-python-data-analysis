"""
資料清洗工具函數庫

包含常用的資料清洗函數，這些函數會在整個專案中重複使用。
"""

import pandas as pd
import numpy as np
from typing import List, Dict, Optional, Union


def remove_duplicates(
    df: pd.DataFrame,
    subset: Optional[List[str]] = None,
    keep: str = 'first'
) -> pd.DataFrame:
    """
    移除重複值

    Parameters:
    -----------
    df : DataFrame
        要處理的資料框
    subset : list, optional
        指定欄位來判斷重複，None 表示所有欄位
    keep : {'first', 'last', False}
        保留哪個重複值，False 表示全部移除

    Returns:
    --------
    DataFrame
        移除重複值後的資料框

    Example:
    --------
    >>> df_clean = remove_duplicates(df, subset=['訂單編號'])
    """
    initial_count = len(df)
    df_clean = df.drop_duplicates(subset=subset, keep=keep)
    removed_count = initial_count - len(df_clean)

    print(f"移除了 {removed_count} 筆重複資料 ({removed_count/initial_count*100:.2f}%)")

    return df_clean


def handle_missing_values(
    df: pd.DataFrame,
    strategy: Dict[str, Union[str, int, float]] = None,
    threshold: float = 0.5
) -> pd.DataFrame:
    """
    處理缺失值

    Parameters:
    -----------
    df : DataFrame
        要處理的資料框
    strategy : dict, optional
        欄位名稱對應處理策略的字典
        {'column_name': 'drop' | 'mean' | 'median' | 'mode' | 'ffill' | 'bfill' | value}
    threshold : float
        缺失率超過此閾值的欄位將被移除（預設 50%）

    Returns:
    --------
    DataFrame
        處理缺失值後的資料框

    Example:
    --------
    >>> strategy = {
    ...     '客戶名稱': '未知客戶',
    ...     '銷售額': 'mean',
    ...     '訂單日期': 'drop'
    ... }
    >>> df_clean = handle_missing_values(df, strategy=strategy)
    """
    df = df.copy()

    # 顯示缺失值摘要
    missing_summary = df.isnull().sum()
    missing_pct = (missing_summary / len(df) * 100).round(2)

    if missing_summary.sum() > 0:
        print("缺失值摘要：")
        for col in missing_summary[missing_summary > 0].index:
            print(f"  {col}: {missing_summary[col]} 筆 ({missing_pct[col]}%)")

    # 移除缺失率過高的欄位
    high_missing_cols = missing_pct[missing_pct > threshold * 100].index.tolist()
    if high_missing_cols:
        print(f"\n移除缺失率超過 {threshold*100}% 的欄位：{high_missing_cols}")
        df = df.drop(columns=high_missing_cols)

    # 根據策略處理缺失值
    if strategy:
        for col, method in strategy.items():
            if col not in df.columns:
                continue

            if method == 'drop':
                df = df.dropna(subset=[col])
            elif method == 'mean':
                df[col].fillna(df[col].mean(), inplace=True)
            elif method == 'median':
                df[col].fillna(df[col].median(), inplace=True)
            elif method == 'mode':
                df[col].fillna(df[col].mode()[0], inplace=True)
            elif method == 'ffill':
                df[col].fillna(method='ffill', inplace=True)
            elif method == 'bfill':
                df[col].fillna(method='bfill', inplace=True)
            else:  # 使用指定的值填充
                df[col].fillna(method, inplace=True)

    return df


def standardize_text(
    df: pd.DataFrame,
    columns: List[str],
    operations: List[str] = ['strip', 'lower']
) -> pd.DataFrame:
    """
    標準化文字欄位

    Parameters:
    -----------
    df : DataFrame
        要處理的資料框
    columns : list
        要標準化的欄位清單
    operations : list
        要執行的操作清單，可包含：
        - 'strip': 去除前後空白
        - 'lower': 轉小寫
        - 'upper': 轉大寫
        - 'title': 首字大寫

    Returns:
    --------
    DataFrame
        標準化後的資料框

    Example:
    --------
    >>> df_clean = standardize_text(df, columns=['產品名稱', '客戶名稱'])
    """
    df = df.copy()

    for col in columns:
        if col not in df.columns:
            print(f"警告：欄位 '{col}' 不存在")
            continue

        # 確保是字串類型
        df[col] = df[col].astype(str)

        for op in operations:
            if op == 'strip':
                df[col] = df[col].str.strip()
            elif op == 'lower':
                df[col] = df[col].str.lower()
            elif op == 'upper':
                df[col] = df[col].str.upper()
            elif op == 'title':
                df[col] = df[col].str.title()

    return df


def detect_outliers(
    df: pd.DataFrame,
    column: str,
    method: str = 'iqr',
    threshold: float = 3.0
) -> pd.Series:
    """
    偵測異常值

    Parameters:
    -----------
    df : DataFrame
        要處理的資料框
    column : str
        要檢查的欄位
    method : {'iqr', 'zscore'}
        偵測方法
        - 'iqr': 使用四分位距（預設）
        - 'zscore': 使用 Z-score
    threshold : float
        - IQR 方法：倍數（預設 1.5）
        - Z-score 方法：標準差倍數（預設 3.0）

    Returns:
    --------
    Series
        布林序列，True 表示異常值

    Example:
    --------
    >>> outliers = detect_outliers(df, '銷售額', method='iqr')
    >>> df_clean = df[~outliers]
    """
    if method == 'iqr':
        Q1 = df[column].quantile(0.25)
        Q3 = df[column].quantile(0.75)
        IQR = Q3 - Q1
        lower_bound = Q1 - threshold * IQR
        upper_bound = Q3 + threshold * IQR

        outliers = (df[column] < lower_bound) | (df[column] > upper_bound)

    elif method == 'zscore':
        mean = df[column].mean()
        std = df[column].std()
        z_scores = np.abs((df[column] - mean) / std)
        outliers = z_scores > threshold

    else:
        raise ValueError(f"不支援的方法：{method}")

    outlier_count = outliers.sum()
    print(f"偵測到 {outlier_count} 個異常值 ({outlier_count/len(df)*100:.2f}%)")

    return outliers


def convert_dtypes(
    df: pd.DataFrame,
    dtype_mapping: Dict[str, str] = None,
    date_columns: List[str] = None,
    categorical_columns: List[str] = None
) -> pd.DataFrame:
    """
    轉換資料型態

    Parameters:
    -----------
    df : DataFrame
        要處理的資料框
    dtype_mapping : dict, optional
        欄位名稱對應型態的字典
    date_columns : list, optional
        要轉換成日期型態的欄位清單
    categorical_columns : list, optional
        要轉換成類別型態的欄位清單（節省記憶體）

    Returns:
    --------
    DataFrame
        轉換型態後的資料框

    Example:
    --------
    >>> df_clean = convert_dtypes(
    ...     df,
    ...     date_columns=['訂單日期', '出貨日期'],
    ...     categorical_columns=['產品類別', '地區']
    ... )
    """
    df = df.copy()

    # 根據 dtype_mapping 轉換
    if dtype_mapping:
        for col, dtype in dtype_mapping.items():
            if col in df.columns:
                df[col] = df[col].astype(dtype)

    # 轉換日期欄位
    if date_columns:
        for col in date_columns:
            if col in df.columns:
                df[col] = pd.to_datetime(df[col], errors='coerce')
                print(f"欄位 '{col}' 已轉換為日期型態")

    # 轉換類別欄位（節省記憶體）
    if categorical_columns:
        for col in categorical_columns:
            if col in df.columns:
                df[col] = df[col].astype('category')
                print(f"欄位 '{col}' 已轉換為類別型態")

    return df


def clean_data_pipeline(
    df: pd.DataFrame,
    remove_duplicates_config: Dict = None,
    missing_values_config: Dict = None,
    text_columns: List[str] = None,
    date_columns: List[str] = None,
    categorical_columns: List[str] = None,
    outlier_columns: List[str] = None
) -> pd.DataFrame:
    """
    完整的資料清洗流程

    這個函數整合了所有清洗步驟，提供一站式清洗服務。

    Parameters:
    -----------
    df : DataFrame
        要清洗的資料框
    remove_duplicates_config : dict, optional
        remove_duplicates 的參數
    missing_values_config : dict, optional
        handle_missing_values 的參數
    text_columns : list, optional
        要標準化的文字欄位
    date_columns : list, optional
        要轉換的日期欄位
    categorical_columns : list, optional
        要轉換的類別欄位
    outlier_columns : list, optional
        要檢查異常值的欄位

    Returns:
    --------
    DataFrame
        清洗後的資料框

    Example:
    --------
    >>> df_clean = clean_data_pipeline(
    ...     df,
    ...     remove_duplicates_config={'subset': ['訂單編號']},
    ...     missing_values_config={'strategy': {'客戶名稱': '未知客戶'}},
    ...     text_columns=['產品名稱'],
    ...     date_columns=['訂單日期'],
    ...     categorical_columns=['產品類別']
    ... )
    """
    print("=" * 50)
    print("開始資料清洗流程")
    print("=" * 50)

    initial_shape = df.shape
    print(f"\n原始資料：{initial_shape[0]} 列 × {initial_shape[1]} 行")

    # 1. 移除重複值
    if remove_duplicates_config:
        print("\n[1/6] 移除重複值...")
        df = remove_duplicates(df, **remove_duplicates_config)

    # 2. 處理缺失值
    if missing_values_config:
        print("\n[2/6] 處理缺失值...")
        df = handle_missing_values(df, **missing_values_config)

    # 3. 標準化文字
    if text_columns:
        print("\n[3/6] 標準化文字欄位...")
        df = standardize_text(df, text_columns)

    # 4. 轉換型態
    print("\n[4/6] 轉換資料型態...")
    df = convert_dtypes(df, date_columns=date_columns, categorical_columns=categorical_columns)

    # 5. 處理異常值
    if outlier_columns:
        print("\n[5/6] 偵測異常值...")
        for col in outlier_columns:
            if col in df.columns:
                outliers = detect_outliers(df, col)
                print(f"  {col}: 發現 {outliers.sum()} 個異常值")

    # 6. 最終摘要
    print("\n[6/6] 清洗完成！")
    final_shape = df.shape
    print(f"最終資料：{final_shape[0]} 列 × {final_shape[1]} 行")
    print(f"移除了 {initial_shape[0] - final_shape[0]} 列 ({(initial_shape[0] - final_shape[0])/initial_shape[0]*100:.2f}%)")

    print("\n" + "=" * 50)

    return df


if __name__ == "__main__":
    # 測試範例
    print("資料清洗工具函數庫")
    print("使用範例請參考各函數的 docstring")
