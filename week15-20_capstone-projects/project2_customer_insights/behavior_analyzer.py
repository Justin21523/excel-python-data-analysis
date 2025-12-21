"""
Behavior Analyzer Module
行為分析模組 - 客戶行為洞察
"""

import pandas as pd
import numpy as np
import logging
from datetime import datetime, timedelta

logger = logging.getLogger(__name__)


class BehaviorAnalyzer:
    """客戶行為分析類"""

    def __init__(self, config):
        """初始化"""
        self.config = config

    def analyze_behavior(self, orders_df, customers_df):
        """
        分析客戶行為

        Args:
            orders_df (pd.DataFrame): 訂單數據
            customers_df (pd.DataFrame): 客戶數據

        Returns:
            dict: 行為分析結果
        """
        try:
            logger.info("分析客戶行為...")

            # 確保日期格式
            orders_df['order_date'] = pd.to_datetime(orders_df['order_date'])
            customers_df['registration_date'] = pd.to_datetime(customers_df['registration_date'])

            behavior_results = {
                'patterns': self._analyze_purchase_patterns(orders_df, customers_df),
                'churn_risk': self._calculate_churn_risk(orders_df, customers_df),
                'engagement': self._calculate_engagement_metrics(orders_df, customers_df)
            }

            logger.info("行為分析完成")
            return behavior_results

        except Exception as e:
            logger.error(f"行為分析失敗: {e}")
            return {}

    def _analyze_purchase_patterns(self, orders_df, customers_df):
        """
        分析購買模式

        Args:
            orders_df (pd.DataFrame): 訂單數據
            customers_df (pd.DataFrame): 客戶數據

        Returns:
            dict: 購買模式分析
        """
        try:
            # 合併數據
            merged = orders_df.merge(customers_df, on='customer_id', how='left')

            patterns = {}

            # 1. 購買頻率分佈
            purchase_frequency = merged.groupby('customer_id').size()
            patterns['frequency_distribution'] = {
                'one_time': (purchase_frequency == 1).sum(),
                'repeat': (purchase_frequency > 1).sum(),
                'frequent': (purchase_frequency >= 5).sum(),
                'avg_frequency': purchase_frequency.mean(),
                'median_frequency': purchase_frequency.median()
            }

            # 2. 購買金額分佈
            purchase_values = merged.groupby('customer_id')['order_amount'].agg(['sum', 'mean', 'count'])
            patterns['value_distribution'] = {
                'total_avg': purchase_values['sum'].mean(),
                'total_median': purchase_values['sum'].median(),
                'avg_order_value': purchase_values['mean'].mean(),
                'high_spenders': (purchase_values['sum'] > purchase_values['sum'].quantile(0.75)).sum()
            }

            # 3. 購買週期
            customer_intervals = []
            for customer_id in merged['customer_id'].unique():
                customer_orders = merged[merged['customer_id'] == customer_id]['order_date'].sort_values()
                if len(customer_orders) > 1:
                    intervals = customer_orders.diff().dt.days.dropna()
                    if len(intervals) > 0:
                        customer_intervals.append(intervals.mean())

            if customer_intervals:
                patterns['purchase_cycle'] = {
                    'avg_days_between_purchases': np.mean(customer_intervals),
                    'median_days': np.median(customer_intervals)
                }

            # 4. 產品偏好
            product_preferences = merged['product_category'].value_counts().to_dict()
            patterns['product_preferences'] = product_preferences

            # 5. 支付方式偏好
            if 'payment_method' in merged.columns:
                payment_prefs = merged['payment_method'].value_counts().to_dict()
                patterns['payment_preferences'] = payment_prefs

            return patterns

        except Exception as e:
            logger.error(f"購買模式分析失敗: {e}")
            return {}

    def _calculate_churn_risk(self, orders_df, customers_df):
        """
        計算流失風險

        Args:
            orders_df (pd.DataFrame): 訂單數據
            customers_df (pd.DataFrame): 客戶數據

        Returns:
            dict: 流失風險分析
        """
        try:
            # 定義流失時間（90天無購買）
            churn_days = 90
            now = datetime.now()

            # 計算最後購買時間
            last_purchase = orders_df.groupby('customer_id')['order_date'].max()

            # 識別流失客戶
            days_since_purchase = (now - last_purchase).dt.days
            at_risk = (days_since_purchase >= churn_days / 2) & (days_since_purchase < churn_days)
            churned = days_since_purchase >= churn_days

            churn_risk = {
                'active_customers': (days_since_purchase < churn_days / 2).sum(),
                'at_risk_customers': at_risk.sum(),
                'churned_customers': churned.sum(),
                'churn_rate': churned.sum() / len(last_purchase) * 100,
                'at_risk_rate': at_risk.sum() / len(last_purchase) * 100
            }

            # 計算風險分數（0-100）
            churn_risk['risk_scores'] = self._calculate_individual_churn_risk(orders_df, customers_df)

            return churn_risk

        except Exception as e:
            logger.error(f"流失風險計算失敗: {e}")
            return {}

    def _calculate_individual_churn_risk(self, orders_df, customers_df):
        """
        計算個人流失風險分數

        Args:
            orders_df (pd.DataFrame): 訂單數據
            customers_df (pd.DataFrame): 客戶數據

        Returns:
            pd.Series: 風險分數
        """
        try:
            merged = orders_df.merge(customers_df, on='customer_id', how='left')
            merged['order_date'] = pd.to_datetime(merged['order_date'])

            now = datetime.now()

            risk_scores = {}

            for customer_id in merged['customer_id'].unique():
                customer_data = merged[merged['customer_id'] == customer_id]

                # 因子1：最後購買距離（權重40%）
                last_purchase = customer_data['order_date'].max()
                days_since = (now - last_purchase).days
                recency_score = min(100, days_since / 3)

                # 因子2：購買頻率（權重30%）
                frequency = len(customer_data)
                frequency_score = max(0, 100 - frequency * 10)

                # 因子3：購買金額（權重20%）
                avg_amount = customer_data['order_amount'].mean()
                monetary_score = max(0, 100 - avg_amount / 10)

                # 因子4：訂單穩定性（權重10%）
                if frequency > 1:
                    intervals = customer_data['order_date'].sort_values().diff().dt.days.dropna()
                    stability_score = 100 - (intervals.std() / intervals.mean() * 100 if intervals.mean() > 0 else 0)
                    stability_score = max(0, min(100, stability_score))
                else:
                    stability_score = 0

                # 計算加權風險分數
                risk_score = (recency_score * 0.4 + frequency_score * 0.3 +
                             monetary_score * 0.2 + stability_score * 0.1)

                risk_scores[customer_id] = min(100, max(0, risk_score))

            return risk_scores

        except Exception as e:
            logger.error(f"個人風險分數計算失敗: {e}")
            return {}

    def _calculate_engagement_metrics(self, orders_df, customers_df):
        """
        計算參與度指標

        Args:
            orders_df (pd.DataFrame): 訂單數據
            customers_df (pd.DataFrame): 客戶數據

        Returns:
            dict: 參與度指標
        """
        try:
            merged = orders_df.merge(customers_df, on='customer_id', how='left')
            merged['order_date'] = pd.to_datetime(merged['order_date'])

            engagement = {}

            # 1. 活躍客戶比例
            now = datetime.now()
            active_threshold = 30  # 30天內有購買
            active_customers = merged[merged['order_date'] >= (now - timedelta(days=active_threshold))]['customer_id'].nunique()
            total_customers = merged['customer_id'].nunique()
            engagement['active_rate'] = active_customers / total_customers * 100 if total_customers > 0 else 0

            # 2. 回購率
            repeat_customers = (merged.groupby('customer_id').size() > 1).sum()
            engagement['repeat_rate'] = repeat_customers / total_customers * 100 if total_customers > 0 else 0

            # 3. 平均訂單間隔
            order_intervals = []
            for customer_id in merged['customer_id'].unique():
                customer_orders = merged[merged['customer_id'] == customer_id]['order_date'].sort_values()
                if len(customer_orders) > 1:
                    intervals = customer_orders.diff().dt.days.dropna()
                    if len(intervals) > 0:
                        order_intervals.append(intervals.mean())

            if order_intervals:
                engagement['avg_order_interval_days'] = np.mean(order_intervals)

            # 4. 客戶終身
            customer_age = (now - merged['registration_date']).dt.days
            engagement['avg_customer_age_days'] = customer_age.mean()

            # 5. 購買季節性
            merged['month'] = merged['order_date'].dt.month
            seasonality = merged.groupby('month').size()
            engagement['seasonality'] = seasonality.to_dict()

            return engagement

        except Exception as e:
            logger.error(f"參與度指標計算失敗: {e}")
            return {}

    def identify_loyal_customers(self, orders_df, customers_df, threshold=3):
        """
        識別忠誠客戶

        Args:
            orders_df (pd.DataFrame): 訂單數據
            customers_df (pd.DataFrame): 客戶數據
            threshold (int): 最少購買次數

        Returns:
            list: 忠誠客戶列表
        """
        try:
            purchase_count = orders_df.groupby('customer_id').size()
            loyal = purchase_count[purchase_count >= threshold].index.tolist()
            logger.info(f"識別 {len(loyal)} 個忠誠客戶")
            return loyal

        except Exception as e:
            logger.error(f"忠誠客戶識別失敗: {e}")
            return []

    def identify_seasonal_customers(self, orders_df, customers_df):
        """
        識別季節性購買客戶

        Args:
            orders_df (pd.DataFrame): 訂單數據
            customers_df (pd.DataFrame): 客戶數據

        Returns:
            dict: 季節性客戶
        """
        try:
            orders_df['order_date'] = pd.to_datetime(orders_df['order_date'])
            orders_df['month'] = orders_df['order_date'].dt.month

            seasonal = {}
            for customer_id in orders_df['customer_id'].unique():
                customer_orders = orders_df[orders_df['customer_id'] == customer_id]
                purchase_months = customer_orders['month'].unique()

                if len(purchase_months) <= 3:  # 只在特定月份購買
                    seasonal[customer_id] = purchase_months.tolist()

            logger.info(f"識別 {len(seasonal)} 個季節性購買客戶")
            return seasonal

        except Exception as e:
            logger.error(f"季節性客戶識別失敗: {e}")
            return {}
