"""
Data Processor Module
資料處理模組 - 負責加載、清洗、轉換銷售數據
"""

import pandas as pd
import numpy as np
import logging
from datetime import datetime, timedelta
from pathlib import Path

logger = logging.getLogger(__name__)


class DataProcessor:
    """資料處理類"""

    def __init__(self, config):
        """
        初始化資料處理器

        Args:
            config (dict): 配置字典
        """
        self.config = config
        self.data = {}

    def load_olist_data(self):
        """
        加載 Olist 數據集或示範數據

        Returns:
            dict: 包含各種 DataFrame 的字典
        """
        logger.info("載入數據...")

        try:
            # 嘗試從本地加載真實數據
            data_path = Path(self.config.get('path', '.'))

            if data_path.exists():
                data = self._load_real_data(data_path)
            else:
                # 使用示範數據
                logger.warning("未找到數據文件，使用示範數據")
                data = self._create_sample_data()

            return data
        except Exception as e:
            logger.error(f"數據加載失敗: {e}")
            return self._create_sample_data()

    def _load_real_data(self, data_path):
        """
        加載真實 CSV 數據

        Args:
            data_path (Path): 數據目錄

        Returns:
            dict: 數據字典
        """
        logger.info(f"從 {data_path} 加載真實數據...")

        data = {}

        # CSV 文件映射
        csv_files = {
            'orders': 'olist_orders_dataset.csv',
            'order_items': 'olist_order_items_dataset.csv',
            'customers': 'olist_customers_dataset.csv',
            'products': 'olist_products_dataset.csv',
            'order_reviews': 'olist_order_reviews_dataset.csv',
            'sellers': 'olist_sellers_dataset.csv'
        }

        for key, filename in csv_files.items():
            filepath = data_path / filename
            if filepath.exists():
                data[key] = pd.read_csv(filepath)
                logger.info(f"已加載 {key}: {len(data[key])} 筆記錄")
            else:
                logger.warning(f"未找到文件: {filename}")

        return data

    def _create_sample_data(self):
        """
        建立示範數據

        Returns:
            dict: 示範數據字典
        """
        logger.info("建立示範數據...")

        np.random.seed(42)
        n_records = 1000

        # 建立訂單數據
        orders = pd.DataFrame({
            'order_id': [f'ORDER_{i:06d}' for i in range(n_records)],
            'customer_id': [f'CUST_{np.random.randint(1, 500)}' for _ in range(n_records)],
            'order_date': pd.date_range(start='2023-01-01', periods=n_records, freq='H'),
            'order_status': np.random.choice(['delivered', 'shipped', 'processing'], n_records),
            'purchase_timestamp': pd.date_range(start='2023-01-01', periods=n_records, freq='H'),
            'estimated_delivery_date': pd.date_range(start='2023-01-05', periods=n_records, freq='H'),
            'actual_delivery_date': pd.date_range(start='2023-01-04', periods=n_records, freq='H')
        })

        # 建立訂單項目
        order_items = pd.DataFrame({
            'order_id': [f'ORDER_{np.random.randint(0, n_records):06d}' for _ in range(n_records * 2)],
            'order_item_id': np.repeat(range(n_records), 2),
            'product_id': [f'PROD_{np.random.randint(1, 100)}' for _ in range(n_records * 2)],
            'seller_id': [f'SELLER_{np.random.randint(1, 50)}' for _ in range(n_records * 2)],
            'shipping_limit_date': pd.date_range(start='2023-01-02', periods=n_records * 2, freq='12H'),
            'price': np.random.uniform(10, 500, n_records * 2),
            'freight_value': np.random.uniform(5, 100, n_records * 2)
        })

        # 建立客戶數據
        customers = pd.DataFrame({
            'customer_id': [f'CUST_{i}' for i in range(1, 501)],
            'customer_unique_id': [f'UNIQUE_CUST_{i}' for i in range(1, 501)],
            'customer_zip_code_prefix': np.random.randint(1000, 99999, 500),
            'customer_city': np.random.choice(['São Paulo', 'Rio de Janeiro', 'Belo Horizonte'], 500),
            'customer_state': np.random.choice(['SP', 'RJ', 'MG', 'BA', 'SC'], 500)
        })

        # 建立產品數據
        products = pd.DataFrame({
            'product_id': [f'PROD_{i}' for i in range(1, 101)],
            'product_name': [f'Product_{i}' for i in range(1, 101)],
            'product_category_name': np.random.choice(
                ['Electronics', 'Books', 'Fashion', 'Home & Garden', 'Sports'], 100
            ),
            'product_name_lenght': np.random.randint(10, 100, 100),
            'product_description_lenght': np.random.randint(50, 500, 100),
            'product_photos_qty': np.random.randint(1, 10, 100),
            'product_weight_g': np.random.randint(100, 5000, 100),
            'product_length_cm': np.random.randint(5, 50, 100),
            'product_height_cm': np.random.randint(5, 50, 100),
            'product_width_cm': np.random.randint(5, 50, 100)
        })

        # 建立評論數據
        order_reviews = pd.DataFrame({
            'review_id': [f'REV_{i:06d}' for i in range(n_records)],
            'order_id': [f'ORDER_{np.random.randint(0, n_records):06d}' for _ in range(n_records)],
            'review_score': np.random.randint(1, 6, n_records),
            'review_comment_title': ['Good' if np.random.rand() > 0.3 else 'Bad' for _ in range(n_records)],
            'review_comment_message': ['Great product!' if np.random.rand() > 0.3 else 'Not satisfied'
                                       for _ in range(n_records)],
            'review_creation_date': pd.date_range(start='2023-01-01', periods=n_records, freq='H'),
            'review_answer_timestamp': pd.date_range(start='2023-01-02', periods=n_records, freq='H')
        })

        # 建立賣家數據
        sellers = pd.DataFrame({
            'seller_id': [f'SELLER_{i}' for i in range(1, 51)],
            'seller_zip_code_prefix': np.random.randint(1000, 99999, 50),
            'seller_city': np.random.choice(['São Paulo', 'Rio de Janeiro', 'Belo Horizonte'], 50),
            'seller_state': np.random.choice(['SP', 'RJ', 'MG', 'BA', 'SC'], 50)
        })

        return {
            'orders': orders,
            'order_items': order_items,
            'customers': customers,
            'products': products,
            'order_reviews': order_reviews,
            'sellers': sellers
        }

    def clean_and_transform(self, data):
        """
        清洗和轉換數據

        Args:
            data (dict): 原始數據字典

        Returns:
            dict: 清洗後的數據字典
        """
        logger.info("清洗和轉換數據...")

        try:
            # 複製數據
            cleaned = {k: v.copy() for k, v in data.items()}

            # 轉換日期列
            date_columns = {
                'orders': ['order_date', 'purchase_timestamp', 'estimated_delivery_date',
                          'actual_delivery_date'],
                'order_reviews': ['review_creation_date', 'review_answer_timestamp'],
                'order_items': ['shipping_limit_date']
            }

            for table, cols in date_columns.items():
                if table in cleaned:
                    for col in cols:
                        if col in cleaned[table].columns:
                            cleaned[table][col] = pd.to_datetime(
                                cleaned[table][col], errors='coerce'
                            )

            # 清理空值
            for table in cleaned:
                original_len = len(cleaned[table])
                cleaned[table] = cleaned[table].dropna(subset=cleaned[table].columns[0])
                if len(cleaned[table]) < original_len:
                    logger.warning(f"{table}: 移除 {original_len - len(cleaned[table])} 筆空記錄")

            # 添加衍生欄位
            if 'order_items' in cleaned and 'orders' in cleaned:
                # 合併訂單和訂單項目
                merged = cleaned['orders'].merge(
                    cleaned['order_items'],
                    on='order_id',
                    how='left'
                )

                # 計算總金額
                merged['order_total'] = merged['price'] + merged['freight_value']

                # 計算交貨時間（天數）
                merged['delivery_days'] = (
                    merged['actual_delivery_date'] - merged['order_date']
                ).dt.days

                cleaned['order_summary'] = merged

            logger.info("數據清洗完成")
            return cleaned

        except Exception as e:
            logger.error(f"數據清洗失敗: {e}")
            return data

    def create_time_features(self, df, date_col):
        """
        從日期列建立時間特徵

        Args:
            df (pd.DataFrame): 數據框
            date_col (str): 日期列名稱

        Returns:
            pd.DataFrame: 增加時間特徵的數據框
        """
        df_copy = df.copy()

        if date_col not in df_copy.columns:
            logger.warning(f"列 {date_col} 不存在")
            return df_copy

        # 確保是日期類型
        df_copy[date_col] = pd.to_datetime(df_copy[date_col], errors='coerce')

        # 建立時間特徵
        df_copy[f'{date_col}_year'] = df_copy[date_col].dt.year
        df_copy[f'{date_col}_month'] = df_copy[date_col].dt.month
        df_copy[f'{date_col}_day'] = df_copy[date_col].dt.day
        df_copy[f'{date_col}_dayofweek'] = df_copy[date_col].dt.dayofweek
        df_copy[f'{date_col}_quarter'] = df_copy[date_col].dt.quarter
        df_copy[f'{date_col}_weekofyear'] = df_copy[date_col].dt.isocalendar().week

        return df_copy

    def handle_missing_values(self, df, strategy='drop'):
        """
        處理缺失值

        Args:
            df (pd.DataFrame): 數據框
            strategy (str): 策略 ('drop', 'forward_fill', 'backward_fill', 'mean')

        Returns:
            pd.DataFrame: 處理後的數據框
        """
        df_copy = df.copy()

        missing_info = df_copy.isnull().sum()
        if missing_info.sum() > 0:
            logger.info(f"發現 {missing_info.sum()} 個缺失值")

            if strategy == 'drop':
                df_copy = df_copy.dropna()
            elif strategy == 'forward_fill':
                df_copy = df_copy.fillna(method='ffill')
            elif strategy == 'backward_fill':
                df_copy = df_copy.fillna(method='bfill')
            elif strategy == 'mean':
                numeric_cols = df_copy.select_dtypes(include=[np.number]).columns
                df_copy[numeric_cols] = df_copy[numeric_cols].fillna(df_copy[numeric_cols].mean())

        return df_copy

    def aggregate_daily_sales(self, data):
        """
        聚合日銷售數據

        Args:
            data (dict): 數據字典

        Returns:
            pd.DataFrame: 日銷售匯總
        """
        if 'order_summary' not in data:
            logger.warning("order_summary 不存在")
            return None

        try:
            summary = data['order_summary'].copy()
            summary['date'] = pd.to_datetime(summary['order_date']).dt.date

            daily_sales = summary.groupby('date').agg({
                'order_id': 'count',
                'order_total': 'sum',
                'price': 'sum'
            }).rename(columns={
                'order_id': 'order_count',
                'order_total': 'total_revenue',
                'price': 'product_revenue'
            })

            return daily_sales
        except Exception as e:
            logger.error(f"日銷售聚合失敗: {e}")
            return None

    def validate_data_quality(self, data):
        """
        驗證數據質量

        Args:
            data (dict): 數據字典

        Returns:
            dict: 質量報告
        """
        report = {
            'total_tables': len(data),
            'tables': {}
        }

        for table_name, df in data.items():
            if isinstance(df, pd.DataFrame):
                report['tables'][table_name] = {
                    'rows': len(df),
                    'columns': len(df.columns),
                    'missing_values': df.isnull().sum().sum(),
                    'duplicates': df.duplicated().sum(),
                    'dtypes': df.dtypes.to_dict()
                }

        logger.info(f"數據質量報告: {report}")
        return report

    def export_to_excel(self, data, filepath):
        """
        匯出數據到 Excel

        Args:
            data (dict): 數據字典
            filepath (str): 輸出路徑
        """
        try:
            with pd.ExcelWriter(filepath) as writer:
                for table_name, df in data.items():
                    if isinstance(df, pd.DataFrame):
                        df.to_excel(writer, sheet_name=table_name[:31], index=False)
            logger.info(f"數據已匯出到 {filepath}")
        except Exception as e:
            logger.error(f"匯出失敗: {e}")
