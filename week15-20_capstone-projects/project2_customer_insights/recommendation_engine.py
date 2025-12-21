"""
Recommendation Engine Module
推薦引擎模組 - 生成個性化推薦
"""

import pandas as pd
import numpy as np
import logging
from collections import defaultdict

logger = logging.getLogger(__name__)


class RecommendationEngine:
    """推薦引擎類"""

    def __init__(self, config):
        """初始化"""
        self.config = config

    def generate_recommendations(self, orders_df, customers_df, analyses):
        """
        生成個性化推薦

        Args:
            orders_df (pd.DataFrame): 訂單數據
            customers_df (pd.DataFrame): 客戶數據
            analyses (dict): 分析結果

        Returns:
            dict: 推薦結果
        """
        try:
            logger.info("生成個性化推薦...")

            recommendations = {
                'retention_campaigns': self._generate_retention_campaigns(orders_df, analyses),
                'upsell_opportunities': self._generate_upsell_opportunities(orders_df, customers_df),
                'personalized_offers': self._generate_personalized_offers(orders_df, analyses),
                'product_recommendations': self._generate_product_recommendations(orders_df),
                'reactivation_targets': self._generate_reactivation_targets(orders_df, analyses)
            }

            logger.info("推薦生成完成")
            return recommendations

        except Exception as e:
            logger.error(f"推薦生成失敗: {e}")
            return {}

    def _generate_retention_campaigns(self, orders_df, analyses):
        """
        生成留存活動

        Args:
            orders_df (pd.DataFrame): 訂單數據
            analyses (dict): 分析結果

        Returns:
            dict: 留存活動建議
        """
        try:
            behavior = analyses.get('behavior', {})
            churn_risk = behavior.get('churn_risk', {})

            if not churn_risk or 'at_risk_customers' not in churn_risk:
                return {}

            at_risk_count = churn_risk.get('at_risk_customers', 0)

            campaigns = {
                'target_count': at_risk_count,
                'campaigns': [
                    {
                        'name': '忠誠客戶折扣',
                        'description': '向風險客戶提供 15% 折扣',
                        'discount': 0.15,
                        'validity_days': 30
                    },
                    {
                        'name': '免費運輸優惠',
                        'description': '下次購買免費運輸',
                        'discount': 0,
                        'validity_days': 60
                    },
                    {
                        'name': '購物點數獎勵',
                        'description': '獎勵購物積分以鼓勵回購',
                        'points': 100,
                        'validity_days': 90
                    }
                ]
            }

            return campaigns

        except Exception as e:
            logger.error(f"留存活動生成失敗: {e}")
            return {}

    def _generate_upsell_opportunities(self, orders_df, customers_df):
        """
        生成增銷機會

        Args:
            orders_df (pd.DataFrame): 訂單數據
            customers_df (pd.DataFrame): 客戶數據

        Returns:
            dict: 增銷建議
        """
        try:
            merged = orders_df.merge(customers_df, on='customer_id', how='left')

            # 按產品分類進行分析
            if 'product_category' not in merged.columns:
                return {}

            upsell_chances = {}

            # 分析購買歷史
            for customer_id in merged['customer_id'].unique():
                customer_purchases = merged[merged['customer_id'] == customer_id]

                # 購買金額最高的分類
                top_category = customer_purchases['product_category'].value_counts().index[0]
                avg_spend = customer_purchases['order_amount'].mean()

                # 建議相關的高價產品
                upsell_chances[customer_id] = {
                    'top_category': top_category,
                    'avg_spend': avg_spend,
                    'recommendation': f'在 {top_category} 分類中推薦高端產品'
                }

            return {
                'total_opportunities': len(upsell_chances),
                'customers': upsell_chances
            }

        except Exception as e:
            logger.error(f"增銷機會生成失敗: {e}")
            return {}

    def _generate_personalized_offers(self, orders_df, analyses):
        """
        生成個性化優惠

        Args:
            orders_df (pd.DataFrame): 訂單數據
            analyses (dict): 分析結果

        Returns:
            dict: 個性化優惠
        """
        try:
            clv = analyses.get('clv', {}).get('customer_clv', pd.DataFrame())

            if clv.empty or 'clv_segment' not in clv.columns:
                return {}

            offers = {}

            # 按客戶價值提供差異化優惠
            for segment in ['Low', 'Medium', 'High', 'Very High']:
                if segment in clv.get('clv_segment', []).values:
                    if segment == 'Very High':
                        offers[segment] = {
                            'discount': 0.20,
                            'free_shipping': True,
                            'exclusive_access': True,
                            'dedicated_support': True
                        }
                    elif segment == 'High':
                        offers[segment] = {
                            'discount': 0.15,
                            'free_shipping': True,
                            'exclusive_access': False,
                            'dedicated_support': False
                        }
                    elif segment == 'Medium':
                        offers[segment] = {
                            'discount': 0.10,
                            'free_shipping': False,
                            'exclusive_access': False,
                            'dedicated_support': False
                        }
                    else:
                        offers[segment] = {
                            'discount': 0.05,
                            'free_shipping': False,
                            'exclusive_access': False,
                            'dedicated_support': False
                        }

            return offers

        except Exception as e:
            logger.error(f"個性化優惠生成失敗: {e}")
            return {}

    def _generate_product_recommendations(self, orders_df):
        """
        生成產品推薦

        Args:
            orders_df (pd.DataFrame): 訂單數據

        Returns:
            dict: 產品推薦
        """
        try:
            # 基於購買共現分析（Association Rule）
            if 'product_category' not in orders_df.columns:
                return {}

            recommendations = {}

            # 計算產品共現矩陣
            product_cooccurrence = defaultdict(lambda: defaultdict(int))

            for order_id in orders_df['order_id'].unique():
                order_products = orders_df[orders_df['order_id'] == order_id]['product_category'].unique()

                for i, prod1 in enumerate(order_products):
                    for prod2 in order_products[i+1:]:
                        product_cooccurrence[prod1][prod2] += 1
                        product_cooccurrence[prod2][prod1] += 1

            # 生成推薦規則
            for product, related in dict(product_cooccurrence).items():
                if related:
                    top_related = sorted(related.items(), key=lambda x: x[1], reverse=True)[:3]
                    recommendations[product] = [
                        {'product': prod, 'confidence': count / len(orders_df)}
                        for prod, count in top_related
                    ]

            return recommendations

        except Exception as e:
            logger.error(f"產品推薦生成失敗: {e}")
            return {}

    def _generate_reactivation_targets(self, orders_df, analyses):
        """
        生成重啟目標客戶

        Args:
            orders_df (pd.DataFrame): 訂單數據
            analyses (dict): 分析結果

        Returns:
            dict: 重啟目標
        """
        try:
            behavior = analyses.get('behavior', {})
            churn_risk = behavior.get('churn_risk', {})

            if not churn_risk or 'churned_customers' not in churn_risk:
                return {}

            churned = churn_risk.get('churned_customers', 0)

            strategies = {
                'win_back_customers': {
                    'target_count': churned,
                    'strategies': [
                        {
                            'name': '特別回歸折扣',
                            'description': '為流失客戶提供 25% 特別折扣',
                            'discount': 0.25,
                            'message': '我們想念你！享受 25% 折扣'
                        },
                        {
                            'name': '驚喜禮物',
                            'description': '隨機選擇流失客戶提供免費禮物',
                            'discount': 0,
                            'message': '回來購物，獲得驚喜禮物'
                        },
                        {
                            'name': '限時優先訪問',
                            'description': '提供新產品的優先訪問',
                            'discount': 0,
                            'message': '回來客戶優先享受新產品'
                        }
                    ]
                }
            }

            return strategies

        except Exception as e:
            logger.error(f"重啟目標生成失敗: {e}")
            return {}

    def calculate_recommendation_roi(self, recommendations):
        """
        計算推薦的 ROI

        Args:
            recommendations (dict): 推薦結果

        Returns:
            dict: ROI 估計
        """
        try:
            # 基於歷史轉換率和平均訂單價值的粗略估計
            conversion_rates = {
                'retention': 0.15,  # 15% 轉換率
                'upsell': 0.10,     # 10% 轉換率
                'reactivation': 0.05  # 5% 轉換率
            }

            avg_order_value = 100  # 假設平均訂單價值

            roi_estimates = {}

            for campaign_type, conversion in conversion_rates.items():
                if campaign_type in recommendations:
                    campaign_data = recommendations[campaign_type]
                    if isinstance(campaign_data, dict) and 'target_count' in campaign_data:
                        expected_revenue = campaign_data['target_count'] * conversion * avg_order_value
                        campaign_cost = campaign_data['target_count'] * 5  # 假設每個客戶成本 $5

                        roi_estimates[campaign_type] = {
                            'expected_revenue': expected_revenue,
                            'campaign_cost': campaign_cost,
                            'estimated_roi': ((expected_revenue - campaign_cost) / campaign_cost * 100) if campaign_cost > 0 else 0
                        }

            return roi_estimates

        except Exception as e:
            logger.error(f"ROI 計算失敗: {e}")
            return {}

    def export_recommendations(self, recommendations, format='csv'):
        """
        匯出推薦結果

        Args:
            recommendations (dict): 推薦結果
            format (str): 輸出格式

        Returns:
            str: 檔案路徑
        """
        try:
            logger.info(f"以 {format} 格式匯出推薦結果...")

            # 轉換為 DataFrame
            export_data = {}

            for key, value in recommendations.items():
                if isinstance(value, dict):
                    export_data[key] = value

            logger.info("推薦結果匯出完成")
            return export_data

        except Exception as e:
            logger.error(f"推薦結果匯出失敗: {e}")
            return {}
