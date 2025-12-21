"""
CLV Calculator Module
客戶終身價值計算模組
"""

import pandas as pd
import numpy as np
import logging
from datetime import datetime, timedelta

logger = logging.getLogger(__name__)


class CLVCalculator:
    """客戶終身價值計算類"""

    def __init__(self, config):
        """初始化"""
        self.config = config
        self.discount_rate = config.get('discount_rate', 0.1)
        self.projection_period = config.get('projection_period', 36)  # 月數

    def calculate_clv(self, orders_df, customers_df):
        """
        計算客戶終身價值

        Args:
            orders_df (pd.DataFrame): 訂單數據
            customers_df (pd.DataFrame): 客戶數據

        Returns:
            pd.DataFrame: CLV 計算結果
        """
        try:
            logger.info("計算客戶終身價值...")

            # 確保日期格式
            orders_df['order_date'] = pd.to_datetime(orders_df['order_date'])
            customers_df['registration_date'] = pd.to_datetime(customers_df['registration_date'])

            # 合併數據
            merged = orders_df.merge(customers_df, on='customer_id', how='left')

            # 計算各客戶的歷史指標
            customer_metrics = merged.groupby('customer_id').agg({
                'order_id': 'count',
                'order_amount': ['sum', 'mean'],
                'order_date': ['max', 'min'],
                'registration_date': 'first'
            }).reset_index()

            customer_metrics.columns = ['customer_id', 'frequency', 'total_spent',
                                       'avg_purchase_value', 'last_purchase',
                                       'first_purchase', 'registration_date']

            # 計算客戶生命週期（月數）
            now = datetime.now()
            customer_metrics['customer_age_months'] = (
                (now - customer_metrics['registration_date']).dt.days / 30
            ).astype(int)

            # 計算重購率
            customer_metrics['repeat_rate'] = (
                customer_metrics['frequency'] / customer_metrics['customer_age_months'].clip(lower=1)
            )

            # 計算CLV（簡單模型）
            # CLV = (平均訂單價值 × 購買頻率 × 客戶生命週期) - 獲取成本
            customer_metrics['clv_simple'] = (
                customer_metrics['avg_purchase_value'] *
                customer_metrics['repeat_rate'] *
                self.projection_period
            )

            # 計算CLV（考慮折現率）
            customer_metrics['clv_discounted'] = self._calculate_discounted_clv(customer_metrics)

            # 計算過往價值（已實現）
            customer_metrics['historical_value'] = customer_metrics['total_spent']

            # 計算未來價值（預期）
            customer_metrics['future_value'] = customer_metrics['clv_discounted'] - customer_metrics['historical_value']

            # 計算潛在價值（基於留存概率）
            customer_metrics['potential_value'] = self._calculate_potential_value(customer_metrics)

            logger.info(f"CLV 計算完成: {len(customer_metrics)} 個客戶")
            return customer_metrics

        except Exception as e:
            logger.error(f"CLV 計算失敗: {e}")
            return pd.DataFrame()

    def _calculate_discounted_clv(self, customer_metrics):
        """
        計算折現現金流 CLV

        Args:
            customer_metrics (pd.DataFrame): 客戶指標

        Returns:
            pd.Series: 折現 CLV
        """
        try:
            clv_list = []

            for idx, row in customer_metrics.iterrows():
                monthly_revenue = row['avg_purchase_value'] * row['repeat_rate']
                clv = 0

                # 預測未來36個月的現金流
                for month in range(1, self.projection_period + 1):
                    # 應用折現率
                    discount_factor = (1 + self.discount_rate) ** (-month / 12)
                    clv += monthly_revenue * discount_factor

                clv_list.append(clv)

            return pd.Series(clv_list)

        except Exception as e:
            logger.error(f"折現 CLV 計算失敗: {e}")
            return pd.Series([0] * len(customer_metrics))

    def _calculate_potential_value(self, customer_metrics):
        """
        計算潛在價值

        Args:
            customer_metrics (pd.DataFrame): 客戶指標

        Returns:
            pd.Series: 潛在價值
        """
        try:
            # 基於同類客戶的平均價值
            avg_clv = customer_metrics['clv_discounted'].mean()

            # 計算潛在價值（與平均值的差距）
            potential = customer_metrics['clv_discounted'].apply(lambda x: max(0, avg_clv - x))

            return potential

        except Exception as e:
            logger.error(f"潛在價值計算失敗: {e}")
            return pd.Series()

    def segment_by_clv(self, clv_df):
        """
        按 CLV 進行客戶分類

        Args:
            clv_df (pd.DataFrame): CLV 數據

        Returns:
            dict: 分類結果
        """
        try:
            logger.info("按 CLV 進行客戶分類...")

            # 使用分位數進行分類
            clv_df['clv_segment'] = pd.qcut(
                clv_df['clv_discounted'],
                q=4,
                labels=['Low', 'Medium', 'High', 'Very High'],
                duplicates='drop'
            )

            segments = {}
            for segment in clv_df['clv_segment'].unique():
                segment_data = clv_df[clv_df['clv_segment'] == segment]
                segments[segment] = {
                    'count': len(segment_data),
                    'customers': segment_data['customer_id'].tolist(),
                    'avg_clv': segment_data['clv_discounted'].mean(),
                    'total_clv': segment_data['clv_discounted'].sum(),
                    'avg_frequency': segment_data['frequency'].mean(),
                    'avg_spend': segment_data['avg_purchase_value'].mean()
                }

            logger.info(f"客戶分類完成: {len(segments)} 個類別")
            return segments

        except Exception as e:
            logger.error(f"客戶分類失敗: {e}")
            return {}

    def analyze_clv_distribution(self, clv_df):
        """
        分析 CLV 分佈

        Args:
            clv_df (pd.DataFrame): CLV 數據

        Returns:
            dict: 分佈分析
        """
        try:
            logger.info("分析 CLV 分佈...")

            distribution = {
                'total_clv': clv_df['clv_discounted'].sum(),
                'avg_clv': clv_df['clv_discounted'].mean(),
                'median_clv': clv_df['clv_discounted'].median(),
                'std_clv': clv_df['clv_discounted'].std(),
                'min_clv': clv_df['clv_discounted'].min(),
                'max_clv': clv_df['clv_discounted'].max(),
                'percentiles': {
                    '25th': clv_df['clv_discounted'].quantile(0.25),
                    '50th': clv_df['clv_discounted'].quantile(0.50),
                    '75th': clv_df['clv_discounted'].quantile(0.75),
                    '90th': clv_df['clv_discounted'].quantile(0.90)
                },
                'pareto': self._calculate_pareto(clv_df)
            }

            return distribution

        except Exception as e:
            logger.error(f"CLV 分佈分析失敗: {e}")
            return {}

    def _calculate_pareto(self, clv_df):
        """
        計算帕累托分析（80/20 規則）

        Args:
            clv_df (pd.DataFrame): CLV 數據

        Returns:
            dict: 帕累托分析結果
        """
        try:
            sorted_clv = clv_df.sort_values('clv_discounted', ascending=False)
            cumsum = sorted_clv['clv_discounted'].cumsum()
            total = cumsum.iloc[-1]

            # 找到累積達到80%的客戶數
            cutoff_idx = (cumsum / total >= 0.8).idxmax()
            cutoff_idx_pos = sorted_clv.index.get_loc(cutoff_idx)

            top_20_pct = cutoff_idx_pos + 1
            total_customers = len(clv_df)

            return {
                'top_customers_for_80pct': top_20_pct,
                'percentage_of_customers': (top_20_pct / total_customers * 100),
                'revenue_contribution': 80.0
            }

        except Exception as e:
            logger.error(f"帕累托分析失敗: {e}")
            return {}

    def forecast_clv(self, clv_df, months=12):
        """
        預測未來 CLV

        Args:
            clv_df (pd.DataFrame): CLV 數據
            months (int): 預測月數

        Returns:
            pd.DataFrame: 預測結果
        """
        try:
            logger.info(f"預測未來 {months} 個月 CLV...")

            forecast_clv = clv_df[['customer_id', 'clv_discounted', 'repeat_rate']].copy()

            # 計算月度 CLV
            monthly_clv = []
            for idx, row in forecast_clv.iterrows():
                monthly_value = row['clv_discounted'] / self.projection_period
                monthly_forecast = [monthly_value * (1 + 0.05) ** month for month in range(1, months + 1)]
                monthly_clv.append(monthly_forecast)

            # 轉換為 DataFrame
            forecast_df = pd.DataFrame(monthly_clv)
            forecast_df.columns = [f'Month_{i}' for i in range(1, months + 1)]
            forecast_df['customer_id'] = forecast_clv['customer_id'].values

            logger.info("CLV 預測完成")
            return forecast_df

        except Exception as e:
            logger.error(f"CLV 預測失敗: {e}")
            return pd.DataFrame()

    def calculate_customer_acquisition_roi(self, clv_df, acquisition_cost=50):
        """
        計算客戶獲取 ROI

        Args:
            clv_df (pd.DataFrame): CLV 數據
            acquisition_cost (float): 平均獲取成本

        Returns:
            dict: ROI 計算結果
        """
        try:
            logger.info(f"計算客戶獲取 ROI（獲取成本: ${acquisition_cost}）...")

            roi = {
                'avg_clv': clv_df['clv_discounted'].mean(),
                'acquisition_cost': acquisition_cost,
                'avg_roi': ((clv_df['clv_discounted'].mean() - acquisition_cost) / acquisition_cost * 100),
                'profitable_customers': (clv_df['clv_discounted'] > acquisition_cost).sum(),
                'profitable_rate': (clv_df['clv_discounted'] > acquisition_cost).sum() / len(clv_df) * 100
            }

            return roi

        except Exception as e:
            logger.error(f"ROI 計算失敗: {e}")
            return {}
