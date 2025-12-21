"""
Analytics Module
分析模組 - 執行銷售分析、異常檢測等
"""

import pandas as pd
import numpy as np
import logging
from datetime import datetime, timedelta
from scipy import stats

logger = logging.getLogger(__name__)


class SalesAnalytics:
    """銷售分析類"""

    def __init__(self):
        """初始化"""
        self.data = None

    def calculate_daily_sales(self, data, days=1):
        """
        計算每日銷售

        Args:
            data (dict): 數據字典
            days (int): 天數

        Returns:
            dict: 銷售指標
        """
        try:
            if 'order_summary' not in data:
                return self._create_empty_metrics()

            summary = data['order_summary'].copy()
            summary['date'] = pd.to_datetime(summary['order_date']).dt.date

            end_date = summary['date'].max()
            start_date = end_date - timedelta(days=days)

            filtered = summary[summary['date'] >= start_date]

            if len(filtered) == 0:
                return self._create_empty_metrics()

            metrics = {
                'total_revenue': filtered['order_total'].sum(),
                'total_orders': filtered['order_id'].nunique(),
                'avg_order_value': filtered['order_total'].sum() / filtered['order_id'].nunique() if filtered['order_id'].nunique() > 0 else 0,
                'customer_count': filtered['customer_id'].nunique(),
                'products_sold': len(filtered),
                'avg_rating': filtered.get('review_score', pd.Series()).mean() if 'review_score' in filtered else 0
            }

            return metrics
        except Exception as e:
            logger.error(f"日銷售計算失敗: {e}")
            return self._create_empty_metrics()

    def calculate_weekly_sales(self, data):
        """
        計算本週銷售

        Args:
            data (dict): 數據字典

        Returns:
            dict: 銷售指標
        """
        try:
            if 'order_summary' not in data:
                return self._create_empty_metrics()

            summary = data['order_summary'].copy()
            summary['date'] = pd.to_datetime(summary['order_date']).dt.date

            end_date = summary['date'].max()
            start_date = end_date - timedelta(days=7)

            filtered = summary[summary['date'] >= start_date]

            if len(filtered) == 0:
                return self._create_empty_metrics()

            metrics = {
                'total_revenue': filtered['order_total'].sum(),
                'total_orders': filtered['order_id'].nunique(),
                'avg_order_value': filtered['order_total'].sum() / filtered['order_id'].nunique() if filtered['order_id'].nunique() > 0 else 0,
                'customer_count': filtered['customer_id'].nunique(),
                'products_sold': len(filtered),
                'daily_breakdown': filtered.groupby('date').agg({
                    'order_total': 'sum',
                    'order_id': 'nunique'
                }).to_dict()
            }

            return metrics
        except Exception as e:
            logger.error(f"週銷售計算失敗: {e}")
            return self._create_empty_metrics()

    def calculate_monthly_sales(self, data):
        """
        計算本月銷售

        Args:
            data (dict): 數據字典

        Returns:
            dict: 銷售指標
        """
        try:
            if 'order_summary' not in data:
                return self._create_empty_metrics()

            summary = data['order_summary'].copy()
            summary['date'] = pd.to_datetime(summary['order_date']).dt.date

            today = summary['date'].max()
            month_start = today.replace(day=1)

            filtered = summary[summary['date'] >= month_start]

            if len(filtered) == 0:
                return self._create_empty_metrics()

            metrics = {
                'total_revenue': filtered['order_total'].sum(),
                'total_orders': filtered['order_id'].nunique(),
                'avg_order_value': filtered['order_total'].sum() / filtered['order_id'].nunique() if filtered['order_id'].nunique() > 0 else 0,
                'customer_count': filtered['customer_id'].nunique(),
                'products_sold': len(filtered),
                'daily_average': filtered['order_total'].sum() / (today - month_start).days if (today - month_start).days > 0 else 0
            }

            return metrics
        except Exception as e:
            logger.error(f"月銷售計算失敗: {e}")
            return self._create_empty_metrics()

    def calculate_yearly_sales(self, data):
        """
        計算年銷售

        Args:
            data (dict): 數據字典

        Returns:
            dict: 銷售指標
        """
        try:
            if 'order_summary' not in data:
                return self._create_empty_metrics()

            summary = data['order_summary'].copy()
            summary['date'] = pd.to_datetime(summary['order_date']).dt.date

            metrics = {
                'total_revenue': summary['order_total'].sum(),
                'total_orders': summary['order_id'].nunique(),
                'avg_order_value': summary['order_total'].sum() / summary['order_id'].nunique() if summary['order_id'].nunique() > 0 else 0,
                'customer_count': summary['customer_id'].nunique(),
                'products_sold': len(summary),
                'avg_rating': summary.get('review_score', pd.Series()).mean() if 'review_score' in summary else 0,
                'repeat_customers': self._calculate_repeat_customers(summary)
            }

            return metrics
        except Exception as e:
            logger.error(f"年銷售計算失敗: {e}")
            return self._create_empty_metrics()

    def calculate_growth_rates(self, data):
        """
        計算成長率

        Args:
            data (dict): 數據字典

        Returns:
            dict: 成長率
        """
        try:
            if 'order_summary' not in data:
                return {}

            summary = data['order_summary'].copy()
            summary['date'] = pd.to_datetime(summary['order_date']).dt.date

            today = summary['date'].max()

            # 本月 vs 上月
            month_start = today.replace(day=1)
            last_month_end = month_start - timedelta(days=1)
            last_month_start = last_month_end.replace(day=1)

            this_month = summary[summary['date'] >= month_start]['order_total'].sum()
            last_month = summary[(summary['date'] >= last_month_start) & (summary['date'] < month_start)]['order_total'].sum()

            mom_growth = ((this_month - last_month) / last_month * 100) if last_month > 0 else 0

            # 本年 vs 去年
            year_start = today.replace(month=1, day=1)
            last_year_end = year_start - timedelta(days=1)
            last_year_start = last_year_end.replace(year=last_year_end.year)

            this_year = summary[summary['date'] >= year_start]['order_total'].sum()
            last_year = summary[(summary['date'] >= last_year_start) & (summary['date'] < year_start)]['order_total'].sum()

            yoy_growth = ((this_year - last_year) / last_year * 100) if last_year > 0 else 0

            return {
                'month_over_month': round(mom_growth, 2),
                'year_over_year': round(yoy_growth, 2)
            }

        except Exception as e:
            logger.error(f"成長率計算失敗: {e}")
            return {}

    def get_top_products(self, data, n=10):
        """
        獲取 Top N 產品

        Args:
            data (dict): 數據字典
            n (int): 產品數量

        Returns:
            pd.DataFrame: Top N 產品
        """
        try:
            if 'order_summary' not in data:
                return pd.DataFrame()

            summary = data['order_summary'].copy()

            top_products = summary.groupby('product_id').agg({
                'order_total': 'sum',
                'order_id': 'count',
                'price': 'mean'
            }).rename(columns={
                'order_total': 'total_revenue',
                'order_id': 'quantity_sold',
                'price': 'avg_price'
            }).sort_values('total_revenue', ascending=False).head(n)

            top_products['rank'] = range(1, len(top_products) + 1)

            return top_products.reset_index()
        except Exception as e:
            logger.error(f"Top 產品計算失敗: {e}")
            return pd.DataFrame()

    def abc_analysis(self, data):
        """
        進行 ABC 分類分析

        Args:
            data (dict): 數據字典

        Returns:
            dict: ABC 分類結果
        """
        try:
            if 'order_summary' not in data:
                return {}

            summary = data['order_summary'].copy()

            # 計算每個產品的銷售額
            product_sales = summary.groupby('product_id').agg({
                'order_total': 'sum',
                'order_id': 'count'
            }).rename(columns={
                'order_total': 'revenue',
                'order_id': 'quantity'
            }).sort_values('revenue', ascending=False)

            # 計算累積百分比
            total_revenue = product_sales['revenue'].sum()
            product_sales['cumulative_pct'] = product_sales['revenue'].cumsum() / total_revenue * 100

            # 分類
            def categorize(pct):
                if pct <= 80:
                    return 'A'
                elif pct <= 95:
                    return 'B'
                else:
                    return 'C'

            product_sales['category'] = product_sales['cumulative_pct'].apply(categorize)

            # 統計
            stats_dict = {
                'A': {
                    'count': (product_sales['category'] == 'A').sum(),
                    'revenue': product_sales[product_sales['category'] == 'A']['revenue'].sum(),
                    'products': product_sales[product_sales['category'] == 'A'].index.tolist()
                },
                'B': {
                    'count': (product_sales['category'] == 'B').sum(),
                    'revenue': product_sales[product_sales['category'] == 'B']['revenue'].sum(),
                    'products': product_sales[product_sales['category'] == 'B'].index.tolist()
                },
                'C': {
                    'count': (product_sales['category'] == 'C').sum(),
                    'revenue': product_sales[product_sales['category'] == 'C']['revenue'].sum(),
                    'products': product_sales[product_sales['category'] == 'C'].index.tolist()
                }
            }

            return {
                'classification': product_sales.reset_index(),
                'statistics': stats_dict
            }
        except Exception as e:
            logger.error(f"ABC 分析失敗: {e}")
            return {}

    def category_analysis(self, data):
        """
        分類分析

        Args:
            data (dict): 數據字典

        Returns:
            pd.DataFrame: 分類分析結果
        """
        try:
            if 'order_summary' not in data:
                return pd.DataFrame()

            summary = data['order_summary'].copy()

            # 如果有 product_category_name，則使用它
            if 'product_category_name' in summary.columns:
                category_analysis = summary.groupby('product_category_name').agg({
                    'order_total': 'sum',
                    'order_id': 'count',
                    'customer_id': 'nunique'
                }).rename(columns={
                    'order_total': 'revenue',
                    'order_id': 'orders',
                    'customer_id': 'customers'
                }).sort_values('revenue', ascending=False)
            else:
                # 如果沒有分類列，則使用產品 ID 的前綴
                summary['category'] = summary['product_id'].str.extract(r'(PROD_\d+)', expand=False)
                category_analysis = summary.groupby('category').agg({
                    'order_total': 'sum',
                    'order_id': 'count'
                }).rename(columns={
                    'order_total': 'revenue',
                    'order_id': 'orders'
                }).sort_values('revenue', ascending=False)

            category_analysis['pct_of_total'] = (
                category_analysis['revenue'] / category_analysis['revenue'].sum() * 100
            )

            return category_analysis.reset_index()
        except Exception as e:
            logger.error(f"分類分析失敗: {e}")
            return pd.DataFrame()

    def regional_sales_analysis(self, data):
        """
        地區銷售分析

        Args:
            data (dict): 數據字典

        Returns:
            pd.DataFrame: 地區分析結果
        """
        try:
            if 'order_summary' not in data:
                return pd.DataFrame()

            summary = data['order_summary'].copy()

            if 'customer_state' in summary.columns:
                regional = summary.groupby('customer_state').agg({
                    'order_total': 'sum',
                    'order_id': 'count',
                    'customer_id': 'nunique'
                }).rename(columns={
                    'order_total': 'revenue',
                    'order_id': 'orders',
                    'customer_id': 'customers'
                }).sort_values('revenue', ascending=False)
            else:
                # 模擬地區數據
                regional = pd.DataFrame({
                    'region': ['North', 'South', 'East', 'West', 'Central'],
                    'revenue': np.random.uniform(10000, 100000, 5),
                    'orders': np.random.randint(100, 1000, 5),
                    'customers': np.random.randint(50, 500, 5)
                }).set_index('region')

            regional['avg_order_value'] = regional['revenue'] / regional['orders']
            regional['pct_of_total'] = regional['revenue'] / regional['revenue'].sum() * 100

            return regional.reset_index()
        except Exception as e:
            logger.error(f"地區分析失敗: {e}")
            return pd.DataFrame()

    def get_top_cities(self, data, n=20):
        """
        獲取 Top N 城市

        Args:
            data (dict): 數據字典
            n (int): 城市數量

        Returns:
            pd.DataFrame: Top N 城市
        """
        try:
            if 'order_summary' not in data:
                return pd.DataFrame()

            summary = data['order_summary'].copy()

            if 'customer_city' in summary.columns:
                cities = summary.groupby('customer_city').agg({
                    'order_total': 'sum',
                    'order_id': 'count',
                    'customer_id': 'nunique'
                }).rename(columns={
                    'order_total': 'revenue',
                    'order_id': 'orders',
                    'customer_id': 'customers'
                }).sort_values('revenue', ascending=False).head(n)
            else:
                return pd.DataFrame()

            return cities.reset_index()
        except Exception as e:
            logger.error(f"城市分析失敗: {e}")
            return pd.DataFrame()

    def geo_distribution(self, data):
        """
        地理分佈分析

        Args:
            data (dict): 數據字典

        Returns:
            dict: 分佈數據
        """
        try:
            if 'order_summary' not in data:
                return {}

            summary = data['order_summary'].copy()

            dist = {
                'states': {},
                'cities': {}
            }

            if 'customer_state' in summary.columns:
                state_dist = summary['customer_state'].value_counts()
                dist['states'] = state_dist.to_dict()

            if 'customer_city' in summary.columns:
                city_dist = summary['customer_city'].value_counts().head(20)
                dist['cities'] = city_dist.to_dict()

            return dist
        except Exception as e:
            logger.error(f"地理分佈分析失敗: {e}")
            return {}

    def detect_sales_anomalies(self, data, threshold=2.0):
        """
        偵測銷售異常

        Args:
            data (dict): 數據字典
            threshold (float): 標準差閾值

        Returns:
            dict: 異常數據
        """
        try:
            if 'order_summary' not in data:
                return {}

            summary = data['order_summary'].copy()
            summary['date'] = pd.to_datetime(summary['order_date']).dt.date

            daily_sales = summary.groupby('date').agg({
                'order_total': 'sum',
                'order_id': 'count'
            }).rename(columns={
                'order_total': 'revenue',
                'order_id': 'orders'
            })

            # 計算統計
            mean_revenue = daily_sales['revenue'].mean()
            std_revenue = daily_sales['revenue'].std()

            # 檢測異常
            anomalies = daily_sales[
                (daily_sales['revenue'] > mean_revenue + threshold * std_revenue) |
                (daily_sales['revenue'] < mean_revenue - threshold * std_revenue)
            ]

            return {
                'mean': mean_revenue,
                'std': std_revenue,
                'anomalies': anomalies.reset_index().to_dict('records') if len(anomalies) > 0 else []
            }
        except Exception as e:
            logger.error(f"異常檢測失敗: {e}")
            return {}

    def check_return_rates(self, data, warning_threshold=5.0):
        """
        檢查退貨率

        Args:
            data (dict): 數據字典
            warning_threshold (float): 警告閾值（%）

        Returns:
            dict: 退貨率警告
        """
        try:
            # 模擬退貨率檢查
            return {
                'warning_threshold': warning_threshold,
                'high_return_products': [],
                'alerts': []
            }
        except Exception as e:
            logger.error(f"退貨率檢查失敗: {e}")
            return {}

    def check_inventory_issues(self, data):
        """
        檢查庫存問題

        Args:
            data (dict): 數據字典

        Returns:
            dict: 庫存警告
        """
        try:
            # 模擬庫存檢查
            return {
                'low_stock_products': [],
                'overstock_products': [],
                'alerts': []
            }
        except Exception as e:
            logger.error(f"庫存檢查失敗: {e}")
            return {}

    def _calculate_repeat_customers(self, summary):
        """計算重複客戶數量"""
        if 'customer_id' not in summary.columns:
            return 0

        customer_orders = summary['customer_id'].value_counts()
        return (customer_orders > 1).sum()

    def _create_empty_metrics(self):
        """建立空指標字典"""
        return {
            'total_revenue': 0,
            'total_orders': 0,
            'avg_order_value': 0,
            'customer_count': 0,
            'products_sold': 0,
            'avg_rating': 0
        }
