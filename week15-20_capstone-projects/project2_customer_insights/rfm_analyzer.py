"""
RFM Analyzer Module
RFM 分析模組 - Recency, Frequency, Monetary
"""

import pandas as pd
import numpy as np
import logging
from datetime import datetime, timedelta

logger = logging.getLogger(__name__)


class RFMAnalyzer:
    """RFM 分析類"""

    def __init__(self, config):
        """初始化"""
        self.config = config
        self.reference_date = datetime.now()

    def calculate_rfm(self, orders_df, customers_df):
        """
        計算 RFM 指標

        Args:
            orders_df (pd.DataFrame): 訂單數據
            customers_df (pd.DataFrame): 客戶數據

        Returns:
            pd.DataFrame: RFM 分數
        """
        try:
            logger.info("計算 RFM 指標...")

            # 確保 order_date 是日期類型
            orders_df['order_date'] = pd.to_datetime(orders_df['order_date'])

            # 計算 Recency（最後一次購買距今天數）
            latest_purchase = orders_df.groupby('customer_id')['order_date'].max()
            recency = (self.reference_date - latest_purchase).dt.days

            # 計算 Frequency（購買次數）
            frequency = orders_df.groupby('customer_id').size()

            # 計算 Monetary（總消費金額）
            monetary = orders_df.groupby('customer_id')['order_amount'].sum()

            # 合併為 DataFrame
            rfm_df = pd.DataFrame({
                'customer_id': recency.index,
                'recency': recency.values,
                'frequency': frequency[recency.index].values,
                'monetary': monetary[recency.index].values
            })

            # 計算 RFM 分數（1-5）
            rfm_df['r_score'] = pd.qcut(rfm_df['recency'], 5, labels=[5, 4, 3, 2, 1], duplicates='drop')
            rfm_df['f_score'] = pd.qcut(rfm_df['frequency'].rank(method='first'), 5, labels=[1, 2, 3, 4, 5], duplicates='drop')
            rfm_df['m_score'] = pd.qcut(rfm_df['monetary'], 5, labels=[1, 2, 3, 4, 5], duplicates='drop')

            # 轉換為數值型
            rfm_df['r_score'] = rfm_df['r_score'].astype(int)
            rfm_df['f_score'] = rfm_df['f_score'].astype(int)
            rfm_df['m_score'] = rfm_df['m_score'].astype(int)

            # 計算總分
            rfm_df['rfm_score'] = rfm_df['r_score'] + rfm_df['f_score'] + rfm_df['m_score']

            logger.info(f"RFM 計算完成: {len(rfm_df)} 個客戶")
            return rfm_df

        except Exception as e:
            logger.error(f"RFM 計算失敗: {e}")
            return pd.DataFrame()

    def segment_customers(self, rfm_df):
        """
        根據 RFM 分數進行客戶分類

        Args:
            rfm_df (pd.DataFrame): RFM 分數數據

        Returns:
            dict: 客戶分類
        """
        try:
            logger.info("進行客戶分類...")

            segments = {}

            def get_segment(row):
                r, f, m = row['r_score'], row['f_score'], row['m_score']

                # VIP：高 R、高 F、高 M
                if r >= 4 and f >= 4 and m >= 4:
                    return 'VIP'
                # 忠誠客：高 F、高 M
                elif f >= 4 and m >= 4:
                    return 'Loyal'
                # 大客戶：高 M
                elif m >= 4:
                    return 'Big Spender'
                # 活躍客：高 F
                elif f >= 4:
                    return 'Active'
                # 新客：低 R
                elif r >= 4:
                    return 'New'
                # 風險客：低 R、低 F
                elif r <= 2 and f <= 2:
                    return 'At Risk'
                # 沉睡客：低 R、低 M
                elif r <= 2 and m <= 2:
                    return 'Dormant'
                # 普通客：中等
                else:
                    return 'Regular'

            rfm_df['segment'] = rfm_df.apply(get_segment, axis=1)

            # 統計各分類
            for segment in rfm_df['segment'].unique():
                segment_data = rfm_df[rfm_df['segment'] == segment]
                segments[segment] = {
                    'count': len(segment_data),
                    'customers': segment_data['customer_id'].tolist(),
                    'avg_recency': segment_data['recency'].mean(),
                    'avg_frequency': segment_data['frequency'].mean(),
                    'avg_monetary': segment_data['monetary'].mean(),
                    'total_value': segment_data['monetary'].sum()
                }

            logger.info(f"客戶分類完成: {len(segments)} 個類別")
            return segments

        except Exception as e:
            logger.error(f"客戶分類失敗: {e}")
            return {}

    def identify_vip_customers(self, rfm_df, threshold=12):
        """
        識別 VIP 客戶

        Args:
            rfm_df (pd.DataFrame): RFM 分數
            threshold (int): 分數閾值

        Returns:
            pd.DataFrame: VIP 客戶
        """
        try:
            vip = rfm_df[rfm_df['rfm_score'] >= threshold]
            logger.info(f"識別 {len(vip)} 個 VIP 客戶")
            return vip

        except Exception as e:
            logger.error(f"VIP 識別失敗: {e}")
            return pd.DataFrame()

    def identify_at_risk_customers(self, rfm_df):
        """
        識別風險客戶

        Args:
            rfm_df (pd.DataFrame): RFM 分數

        Returns:
            pd.DataFrame: 風險客戶
        """
        try:
            # 低頻率、低金額的客戶
            at_risk = rfm_df[(rfm_df['recency'] > 180) & (rfm_df['frequency'] < 2)]
            logger.info(f"識別 {len(at_risk)} 個風險客戶")
            return at_risk

        except Exception as e:
            logger.error(f"風險識別失敗: {e}")
            return pd.DataFrame()

    def get_segment_metrics(self, rfm_df):
        """
        獲取各分類的詳細指標

        Args:
            rfm_df (pd.DataFrame): RFM 分數

        Returns:
            pd.DataFrame: 分類指標
        """
        try:
            metrics = rfm_df.groupby('segment').agg({
                'customer_id': 'count',
                'recency': ['mean', 'median'],
                'frequency': ['mean', 'median'],
                'monetary': ['mean', 'median', 'sum']
            }).round(2)

            return metrics

        except Exception as e:
            logger.error(f"獲取分類指標失敗: {e}")
            return pd.DataFrame()

    def calculate_customer_value_index(self, rfm_df):
        """
        計算客戶價值指數

        Args:
            rfm_df (pd.DataFrame): RFM 分數

        Returns:
            pd.Series: 客戶價值指數
        """
        try:
            # 標準化分數
            r_norm = (rfm_df['r_score'] - rfm_df['r_score'].min()) / (rfm_df['r_score'].max() - rfm_df['r_score'].min())
            f_norm = (rfm_df['f_score'] - rfm_df['f_score'].min()) / (rfm_df['f_score'].max() - rfm_df['f_score'].min())
            m_norm = (rfm_df['m_score'] - rfm_df['m_score'].min()) / (rfm_df['m_score'].max() - rfm_df['m_score'].min())

            # 加權計算（可調整權重）
            cvi = r_norm * 0.2 + f_norm * 0.3 + m_norm * 0.5

            return cvi

        except Exception as e:
            logger.error(f"客戶價值指數計算失敗: {e}")
            return pd.Series()

    def generate_rfm_summary(self, rfm_df):
        """
        生成 RFM 摘要

        Args:
            rfm_df (pd.DataFrame): RFM 分數

        Returns:
            dict: 摘要數據
        """
        try:
            summary = {
                'total_customers': len(rfm_df),
                'recency': {
                    'mean': rfm_df['recency'].mean(),
                    'median': rfm_df['recency'].median(),
                    'min': rfm_df['recency'].min(),
                    'max': rfm_df['recency'].max()
                },
                'frequency': {
                    'mean': rfm_df['frequency'].mean(),
                    'median': rfm_df['frequency'].median(),
                    'min': rfm_df['frequency'].min(),
                    'max': rfm_df['frequency'].max()
                },
                'monetary': {
                    'mean': rfm_df['monetary'].mean(),
                    'median': rfm_df['monetary'].median(),
                    'min': rfm_df['monetary'].min(),
                    'max': rfm_df['monetary'].max(),
                    'total': rfm_df['monetary'].sum()
                },
                'score_distribution': rfm_df['rfm_score'].describe().to_dict()
            }

            return summary

        except Exception as e:
            logger.error(f"摘要生成失敗: {e}")
            return {}
