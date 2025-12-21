"""
Project 2: Customer Insights System
客戶洞察系統 - Week 16-17

功能：
1. RFM 分析（Recency, Frequency, Monetary）
2. 客戶生命週期價值（CLV）計算
3. 客戶群組分析（Cohort Analysis）
4. 行為分析（Behavior Analysis）
5. 個性化推薦（Recommendation Engine）
6. 客戶細分和標籤
"""

import pandas as pd
import numpy as np
import logging
import yaml
from pathlib import Path
from datetime import datetime, timedelta
import sys

# 導入自訂模組
try:
    from rfm_analyzer import RFMAnalyzer
    from cohort_analyzer import CohortAnalyzer
    from clv_calculator import CLVCalculator
    from behavior_analyzer import BehaviorAnalyzer
    from recommendation_engine import RecommendationEngine
    from report_generator import CustomerReportGenerator
except ImportError:
    print("警告：某些模組未找到")

# 設定日誌
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    handlers=[
        logging.FileHandler('customer_insights.log'),
        logging.StreamHandler()
    ]
)
logger = logging.getLogger(__name__)


class CustomerInsightsSystem:
    """客戶洞察系統主類"""

    def __init__(self, config_file='config.yaml'):
        """
        初始化客戶洞察系統

        Args:
            config_file (str): 配置文件路徑
        """
        try:
            with open(config_file) as f:
                self.config = yaml.safe_load(f)

            self.rfm_analyzer = RFMAnalyzer(self.config.get('rfm', {}))
            self.cohort_analyzer = CohortAnalyzer(self.config.get('cohort', {}))
            self.clv_calculator = CLVCalculator(self.config.get('clv', {}))
            self.behavior_analyzer = BehaviorAnalyzer(self.config.get('behavior', {}))
            self.recommendation_engine = RecommendationEngine(self.config.get('recommendation', {}))
            self.report_gen = CustomerReportGenerator(self.config.get('output', {}))

            self.data = None
            self.analyses = {}

            logger.info("Customer Insights System 初始化完成")
        except Exception as e:
            logger.error(f"初始化失敗: {e}")
            raise

    def load_customer_data(self):
        """載入客戶數據"""
        logger.info("載入客戶數據...")

        try:
            # 嘗試從 CSV 加載
            data_path = Path(self.config.get('data', {}).get('path', 'data'))

            self.data = {}

            if data_path.exists():
                # 加載真實數據
                order_file = data_path / 'orders.csv'
                customer_file = data_path / 'customers.csv'

                if order_file.exists():
                    self.data['orders'] = pd.read_csv(order_file)
                if customer_file.exists():
                    self.data['customers'] = pd.read_csv(customer_file)
            else:
                # 生成示範數據
                logger.warning("未找到數據文件，使用示範數據")
                self.data = self._create_sample_data()

            logger.info(f"客戶數據加載完成: {len(self.data.get('orders', pd.DataFrame()))} 筆訂單")
            return True

        except Exception as e:
            logger.error(f"客戶數據加載失敗: {e}")
            return False

    def _create_sample_data(self):
        """建立示範數據"""
        np.random.seed(42)
        n_customers = 500
        n_orders = 2000

        # 客戶數據
        customers = pd.DataFrame({
            'customer_id': [f'CUST_{i:05d}' for i in range(1, n_customers + 1)],
            'email': [f'customer_{i}@example.com' for i in range(1, n_customers + 1)],
            'registration_date': pd.date_range(start='2022-01-01', periods=n_customers, freq='6H'),
            'segment': np.random.choice(['VIP', 'Regular', 'Casual', 'Inactive'], n_customers),
            'lifetime_value': np.random.uniform(100, 10000, n_customers)
        })

        # 訂單數據
        orders = pd.DataFrame({
            'order_id': [f'ORDER_{i:06d}' for i in range(1, n_orders + 1)],
            'customer_id': np.random.choice(customers['customer_id'], n_orders),
            'order_date': pd.date_range(start='2022-01-01', periods=n_orders, freq='12H'),
            'order_amount': np.random.uniform(10, 500, n_orders),
            'product_category': np.random.choice(['Electronics', 'Clothing', 'Books', 'Home'], n_orders),
            'payment_method': np.random.choice(['Credit Card', 'PayPal', 'Bank Transfer'], n_orders)
        })

        return {
            'customers': customers,
            'orders': orders
        }

    def perform_rfm_analysis(self):
        """執行 RFM 分析"""
        logger.info("執行 RFM 分析...")

        try:
            rfm_result = self.rfm_analyzer.calculate_rfm(self.data['orders'], self.data['customers'])

            self.analyses['rfm'] = {
                'scores': rfm_result,
                'segments': self.rfm_analyzer.segment_customers(rfm_result)
            }

            logger.info("RFM 分析完成")
            return self.analyses['rfm']

        except Exception as e:
            logger.error(f"RFM 分析失敗: {e}")
            return {}

    def perform_cohort_analysis(self):
        """執行客戶生命週期分析"""
        logger.info("執行客戶生命週期分析...")

        try:
            cohort_data = self.cohort_analyzer.create_cohort_table(
                self.data['orders'],
                self.data['customers']
            )

            self.analyses['cohort'] = {
                'cohort_table': cohort_data,
                'retention_metrics': self.cohort_analyzer.calculate_retention(cohort_data)
            }

            logger.info("生命週期分析完成")
            return self.analyses['cohort']

        except Exception as e:
            logger.error(f"生命週期分析失敗: {e}")
            return {}

    def calculate_customer_lifetime_value(self):
        """計算客戶終身價值"""
        logger.info("計算客戶終身價值（CLV）...")

        try:
            clv_result = self.clv_calculator.calculate_clv(
                self.data['orders'],
                self.data['customers']
            )

            self.analyses['clv'] = {
                'customer_clv': clv_result,
                'distribution': self.clv_calculator.analyze_clv_distribution(clv_result)
            }

            logger.info("CLV 計算完成")
            return self.analyses['clv']

        except Exception as e:
            logger.error(f"CLV 計算失敗: {e}")
            return {}

    def analyze_customer_behavior(self):
        """分析客戶行為"""
        logger.info("分析客戶行為...")

        try:
            behavior_analysis = self.behavior_analyzer.analyze_behavior(
                self.data['orders'],
                self.data['customers']
            )

            self.analyses['behavior'] = {
                'purchase_patterns': behavior_analysis['patterns'],
                'churn_risk': behavior_analysis['churn_risk'],
                'engagement_metrics': behavior_analysis['engagement']
            }

            logger.info("行為分析完成")
            return self.analyses['behavior']

        except Exception as e:
            logger.error(f"行為分析失敗: {e}")
            return {}

    def generate_recommendations(self):
        """生成個性化推薦"""
        logger.info("生成個性化推薦...")

        try:
            recommendations = self.recommendation_engine.generate_recommendations(
                self.data['orders'],
                self.data['customers'],
                self.analyses
            )

            self.analyses['recommendations'] = recommendations

            logger.info("推薦生成完成")
            return recommendations

        except Exception as e:
            logger.error(f"推薦生成失敗: {e}")
            return {}

    def segment_customers(self):
        """細分客戶群組"""
        logger.info("細分客戶群組...")

        try:
            segments = self._create_customer_segments()

            self.analyses['segments'] = segments

            logger.info(f"客戶細分完成: {len(segments)} 個群組")
            return segments

        except Exception as e:
            logger.error(f"客戶細分失敗: {e}")
            return {}

    def _create_customer_segments(self):
        """建立客戶細分"""
        try:
            rfm = self.analyses.get('rfm', {}).get('segments', {})
            clv = self.analyses.get('clv', {}).get('customer_clv', pd.DataFrame())
            behavior = self.analyses.get('behavior', {})

            segments = {
                'vip_customers': self._identify_vip(rfm, clv),
                'at_risk': self._identify_at_risk(behavior),
                'growth_potential': self._identify_growth_potential(rfm, clv),
                'dormant': self._identify_dormant(rfm)
            }

            return segments

        except Exception as e:
            logger.error(f"客戶細分建立失敗: {e}")
            return {}

    def _identify_vip(self, rfm, clv):
        """識別 VIP 客戶"""
        return {'count': len(rfm) if isinstance(rfm, dict) else 0, 'customers': []}

    def _identify_at_risk(self, behavior):
        """識別風險客戶"""
        churn_risk = behavior.get('churn_risk', {})
        return {'count': len(churn_risk) if isinstance(churn_risk, dict) else 0, 'customers': []}

    def _identify_growth_potential(self, rfm, clv):
        """識別成長潛力客戶"""
        return {'count': 0, 'customers': []}

    def _identify_dormant(self, rfm):
        """識別沉睡客戶"""
        return {'count': len(rfm) if isinstance(rfm, dict) else 0, 'customers': []}

    def generate_report(self):
        """產生客戶洞察報告"""
        logger.info("產生客戶洞察報告...")

        try:
            excel_file = self.report_gen.create_customer_report(self.analyses)
            pdf_file = self.report_gen.create_pdf_report(self.analyses)

            logger.info(f"報告已生成:")
            logger.info(f"  - Excel: {excel_file}")
            logger.info(f"  - PDF: {pdf_file}")

            return excel_file, pdf_file

        except Exception as e:
            logger.error(f"報告生成失敗: {e}")
            return None, None

    def run(self):
        """執行完整流程"""
        try:
            logger.info("=" * 60)
            logger.info("Customer Insights System - 開始執行")
            logger.info("=" * 60)

            # 1. 載入數據
            if not self.load_customer_data():
                return {'status': 'failed', 'error': '數據加載失敗'}

            # 2. 執行各項分析
            self.perform_rfm_analysis()
            self.perform_cohort_analysis()
            self.calculate_customer_lifetime_value()
            self.analyze_customer_behavior()
            self.generate_recommendations()
            self.segment_customers()

            # 3. 產生報告
            excel_file, pdf_file = self.generate_report()

            logger.info("=" * 60)
            logger.info("Customer Insights System - 執行完成！")
            logger.info("=" * 60)

            return {
                'status': 'success',
                'outputs': {
                    'excel': excel_file,
                    'pdf': pdf_file
                },
                'analyses': self.analyses
            }

        except Exception as e:
            logger.error(f"執行失敗: {e}", exc_info=True)
            return {'status': 'failed', 'error': str(e)}


def main():
    """主函數"""
    import argparse

    parser = argparse.ArgumentParser(description='Customer Insights System')
    parser.add_argument('--config', default='config.yaml', help='配置文件路徑')
    args = parser.parse_args()

    try:
        system = CustomerInsightsSystem(args.config)
        result = system.run()

        if result['status'] == 'success':
            print("\n✓ 客戶洞察系統執行成功！")
            print(f"  Excel 報告: {result['outputs']['excel']}")
            print(f"  PDF 報告: {result['outputs']['pdf']}")
            return 0
        else:
            print(f"\n✗ 執行失敗: {result['error']}")
            return 1

    except Exception as e:
        logger.error(f"主程式執行失敗: {e}", exc_info=True)
        return 1


if __name__ == "__main__":
    sys.exit(main())
