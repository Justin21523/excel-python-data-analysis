"""
Cohort Analyzer Module
群組分析模組 - 客戶生命週期分析
"""

import pandas as pd
import numpy as np
import logging
from datetime import datetime

logger = logging.getLogger(__name__)


class CohortAnalyzer:
    """群組分析類"""

    def __init__(self, config):
        """初始化"""
        self.config = config

    def create_cohort_table(self, orders_df, customers_df):
        """
        建立群組分析表

        Args:
            orders_df (pd.DataFrame): 訂單數據
            customers_df (pd.DataFrame): 客戶數據

        Returns:
            pd.DataFrame: 群組表
        """
        try:
            logger.info("建立群組分析表...")

            # 確保日期格式
            orders_df['order_date'] = pd.to_datetime(orders_df['order_date'])
            customers_df['registration_date'] = pd.to_datetime(customers_df['registration_date'])

            # 合併訂單和客戶數據
            merged = orders_df.merge(customers_df, on='customer_id', how='left')

            # 計算客戶生命週期（月份）
            merged['cohort_month'] = merged['registration_date'].dt.to_period('M')
            merged['order_month'] = merged['order_date'].dt.to_period('M')
            merged['cohort_index'] = (merged['order_month'] - merged['cohort_month']).apply(lambda x: x.n)

            # 建立群組表
            cohort_data = merged.groupby(['cohort_month', 'cohort_index']).agg({
                'customer_id': 'nunique',
                'order_amount': 'sum'
            }).rename(columns={'customer_id': 'customer_count', 'order_amount': 'revenue'})

            cohort_table = cohort_data.unstack(fill_value=0)

            logger.info(f"群組表建立完成: {len(cohort_table)} 個群組")
            return {
                'merged_data': merged,
                'cohort_table': cohort_table
            }

        except Exception as e:
            logger.error(f"群組表建立失敗: {e}")
            return {}

    def calculate_retention(self, cohort_data):
        """
        計算留存率

        Args:
            cohort_data (dict): 群組數據

        Returns:
            pd.DataFrame: 留存率表
        """
        try:
            logger.info("計算留存率...")

            if 'cohort_table' not in cohort_data:
                return pd.DataFrame()

            cohort_table = cohort_data['cohort_table']['customer_count']

            # 計算留存率（百分比）
            cohort_size = cohort_table.iloc[:, 0]
            retention_table = cohort_table.divide(cohort_size, axis=0) * 100

            logger.info("留存率計算完成")
            return retention_table.round(2)

        except Exception as e:
            logger.error(f"留存率計算失敗: {e}")
            return pd.DataFrame()

    def calculate_revenue_cohort(self, cohort_data):
        """
        計算收益群組

        Args:
            cohort_data (dict): 群組數據

        Returns:
            pd.DataFrame: 收益群組表
        """
        try:
            logger.info("計算收益群組...")

            if 'cohort_table' not in cohort_data:
                return pd.DataFrame()

            revenue_cohort = cohort_data['cohort_table']['revenue']

            logger.info("收益群組計算完成")
            return revenue_cohort.round(2)

        except Exception as e:
            logger.error(f"收益群組計算失敗: {e}")
            return pd.DataFrame()

    def analyze_cohort_behavior(self, cohort_data):
        """
        分析群組行為

        Args:
            cohort_data (dict): 群組數據

        Returns:
            dict: 行為分析結果
        """
        try:
            logger.info("分析群組行為...")

            if 'merged_data' not in cohort_data:
                return {}

            merged = cohort_data['merged_data']

            # 按群組計算平均指標
            behavior = {}

            for cohort in merged['cohort_month'].unique():
                cohort_members = merged[merged['cohort_month'] == cohort]

                behavior[str(cohort)] = {
                    'size': cohort_members['customer_id'].nunique(),
                    'avg_purchase_value': cohort_members['order_amount'].mean(),
                    'total_revenue': cohort_members['order_amount'].sum(),
                    'repeat_rate': (cohort_members.groupby('customer_id').size() > 1).sum() / cohort_members['customer_id'].nunique() * 100,
                    'churn_rate': 100 - ((cohort_members.groupby('customer_id').size() > 0).sum() / len(cohort_members) * 100)
                }

            logger.info(f"群組行為分析完成: {len(behavior)} 個群組")
            return behavior

        except Exception as e:
            logger.error(f"群組行為分析失敗: {e}")
            return {}

    def identify_best_cohort(self, cohort_data):
        """
        識別表現最好的群組

        Args:
            cohort_data (dict): 群組數據

        Returns:
            dict: 最佳群組信息
        """
        try:
            if 'cohort_table' not in cohort_data:
                return {}

            revenue_cohort = cohort_data['cohort_table']['revenue']

            # 找到總收入最高的群組
            best_cohort = revenue_cohort.sum(axis=1).idxmax()
            best_value = revenue_cohort.sum(axis=1).max()

            # 找到留存率最好的群組
            customer_cohort = cohort_data['cohort_table']['customer_count']
            retention_rate = (customer_cohort.iloc[:, 1:].mean(axis=1) / customer_cohort.iloc[:, 0] * 100)
            best_retention_cohort = retention_rate.idxmax()

            return {
                'highest_revenue_cohort': str(best_cohort),
                'highest_revenue': best_value,
                'best_retention_cohort': str(best_retention_cohort),
                'best_retention_rate': retention_rate.max()
            }

        except Exception as e:
            logger.error(f"最佳群組識別失敗: {e}")
            return {}

    def forecast_cohort_value(self, cohort_data, periods=6):
        """
        預測群組價值

        Args:
            cohort_data (dict): 群組數據
            periods (int): 預測期數

        Returns:
            pd.DataFrame: 預測結果
        """
        try:
            logger.info(f"預測群組價值（{periods}個月）...")

            if 'cohort_table' not in cohort_data:
                return pd.DataFrame()

            revenue_cohort = cohort_data['cohort_table']['revenue']

            # 使用簡單的線性趨勢預測
            forecast = {}

            for cohort in revenue_cohort.index:
                historical = revenue_cohort.loc[cohort].values
                if len(historical) > 1:
                    # 計算平均增長率
                    avg_growth = np.mean(np.diff(historical) / historical[:-1])
                    last_value = historical[-1]

                    # 預測未來值
                    forecast_values = [last_value]
                    for i in range(periods):
                        forecast_values.append(forecast_values[-1] * (1 + avg_growth))

                    forecast[str(cohort)] = forecast_values[1:]

            logger.info("群組價值預測完成")
            return pd.DataFrame(forecast).T

        except Exception as e:
            logger.error(f"群組價值預測失敗: {e}")
            return pd.DataFrame()

    def generate_cohort_summary(self, cohort_data):
        """
        生成群組摘要

        Args:
            cohort_data (dict): 群組數據

        Returns:
            dict: 摘要信息
        """
        try:
            summary = {}

            if 'cohort_table' in cohort_data:
                cohort_table = cohort_data['cohort_table']

                summary = {
                    'total_cohorts': len(cohort_table.index),
                    'total_customers': cohort_table['customer_count'].iloc[:, 0].sum(),
                    'total_revenue': cohort_table['revenue'].sum().sum(),
                    'avg_cohort_size': cohort_table['customer_count'].iloc[:, 0].mean(),
                    'avg_cohort_revenue': cohort_table['revenue'].sum(axis=1).mean()
                }

            return summary

        except Exception as e:
            logger.error(f"群組摘要生成失敗: {e}")
            return {}
