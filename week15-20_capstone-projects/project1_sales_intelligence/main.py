"""
Project 1: Sales Intelligence Dashboard
銷售智能儀表板系統

功能：
1. 銷售總覽（今日/本週/本月/本年 vs 上期）
2. 產品分析（Top 10 熱銷、ABC 分類）
3. 地區分析（各地區銷售熱圖、排名）
4. 異常偵測（銷售額、庫存、退貨率異常）
5. 自動產生 Excel 報表
6. 每日排程執行
"""

import pandas as pd
import numpy as np
import logging
import yaml
from pathlib import Path
from datetime import datetime, timedelta
import sys
import json

# 導入自訂模組
try:
    from data_processor import DataProcessor
    from analytics import SalesAnalytics
    from visualizations import SalesVisualizer
    from report_generator import ReportGenerator
except ImportError:
    print("警告：某些模組未找到，請確保所有依賴已安裝")

# 設定日誌
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    handlers=[
        logging.FileHandler('sales_intelligence.log'),
        logging.StreamHandler()
    ]
)
logger = logging.getLogger(__name__)


class SalesIntelligenceDashboard:
    """銷售智能儀表板主類"""

    def __init__(self, config_file='config.yaml'):
        """
        初始化銷售儀表板

        Args:
            config_file (str): 配置文件路徑
        """
        try:
            with open(config_file) as f:
                self.config = yaml.safe_load(f)

            self.data_processor = DataProcessor(self.config.get('data', {}))
            self.analytics = SalesAnalytics()
            self.visualizer = SalesVisualizer()
            self.report_gen = ReportGenerator(self.config.get('output', {}))

            self.data = None
            self.analyses = {}
            self.figures = {}

            logger.info("Sales Intelligence Dashboard 初始化完成")
        except Exception as e:
            logger.error(f"初始化失敗: {e}")
            raise

    def load_and_prepare_data(self):
        """載入並準備資料"""
        logger.info("開始載入資料...")
        try:
            # 載入數據
            self.data = self.data_processor.load_olist_data()

            # 清洗和轉換
            self.data = self.data_processor.clean_and_transform(self.data)

            logger.info(f"資料載入完成，訂單數: {len(self.data.get('orders', pd.DataFrame())):,}")
            return True
        except Exception as e:
            logger.error(f"資料載入失敗: {e}")
            return False

    def analyze_sales_overview(self):
        """銷售總覽分析"""
        logger.info("計算銷售總覽指標...")

        try:
            overview = {}

            # 計算各時期銷售
            overview['today'] = self.analytics.calculate_daily_sales(self.data, days=1)
            overview['this_week'] = self.analytics.calculate_weekly_sales(self.data)
            overview['this_month'] = self.analytics.calculate_monthly_sales(self.data)
            overview['this_year'] = self.analytics.calculate_yearly_sales(self.data)

            # 計算成長率
            overview['growth_rates'] = self.analytics.calculate_growth_rates(self.data)

            # 主要指標
            overview['key_metrics'] = {
                'total_revenue': overview['this_year'].get('total_revenue', 0),
                'total_orders': overview['this_year'].get('total_orders', 0),
                'avg_order_value': overview['this_year'].get('avg_order_value', 0),
                'customer_count': overview['this_year'].get('customer_count', 0)
            }

            logger.info("銷售總覽分析完成")
            return overview
        except Exception as e:
            logger.error(f"銷售總覽分析失敗: {e}")
            return {}

    def analyze_products(self):
        """產品分析"""
        logger.info("分析產品表現...")

        try:
            products = {}

            # Top 10 產品
            products['top_10'] = self.analytics.get_top_products(self.data, n=10)

            # ABC 分類
            products['abc_classification'] = self.analytics.abc_analysis(self.data)

            # 產品分類分析
            products['category_performance'] = self.analytics.category_analysis(self.data)

            logger.info("產品分析完成")
            return products
        except Exception as e:
            logger.error(f"產品分析失敗: {e}")
            return {}

    def analyze_regions(self):
        """地區分析"""
        logger.info("分析地區表現...")

        try:
            regions = {}

            # 地區銷售分析
            regions['regional_sales'] = self.analytics.regional_sales_analysis(self.data)

            # 城市排名
            regions['city_rankings'] = self.analytics.get_top_cities(self.data, n=20)

            # 地理分佈
            regions['geographic_distribution'] = self.analytics.geo_distribution(self.data)

            logger.info("地區分析完成")
            return regions
        except Exception as e:
            logger.error(f"地區分析失敗: {e}")
            return {}

    def detect_anomalies(self):
        """異常檢測"""
        logger.info("執行異常檢測...")

        try:
            anomalies = {}

            # 銷售異常
            anomalies['sales_anomalies'] = self.analytics.detect_sales_anomalies(self.data)

            # 退貨率異常
            anomalies['return_rate_alerts'] = self.analytics.check_return_rates(self.data)

            # 庫存異常
            anomalies['inventory_alerts'] = self.analytics.check_inventory_issues(self.data)

            logger.info("異常檢測完成")
            return anomalies
        except Exception as e:
            logger.error(f"異常檢測失敗: {e}")
            return {}

    def generate_visualizations(self, analyses):
        """生成視覺化"""
        logger.info("生成視覺化圖表...")

        try:
            figures = {}

            # 銷售趨勢圖
            if analyses.get('overview'):
                figures['sales_trend'] = self.visualizer.plot_sales_trend(
                    analyses['overview']
                )

            # Top 10 產品圖
            if analyses.get('products', {}).get('top_10') is not None:
                figures['top_products'] = self.visualizer.plot_top_products(
                    analyses['products']['top_10']
                )

            # 地區熱圖
            if analyses.get('regions', {}).get('regional_sales') is not None:
                figures['regional_heatmap'] = self.visualizer.plot_regional_heatmap(
                    analyses['regions']['regional_sales']
                )

            # ABC 分類圖
            if analyses.get('products', {}).get('abc_classification') is not None:
                figures['abc_chart'] = self.visualizer.plot_abc_classification(
                    analyses['products']['abc_classification']
                )

            logger.info("視覺化生成完成")
            return figures
        except Exception as e:
            logger.error(f"視覺化生成失敗: {e}")
            return {}

    def generate_reports(self, analyses, figures):
        """產生報表"""
        logger.info("生成報表...")

        try:
            # 生成 Excel 儀表板
            excel_file = self.report_gen.create_excel_dashboard(
                overview=analyses.get('overview', {}),
                products=analyses.get('products', {}),
                regions=analyses.get('regions', {}),
                anomalies=analyses.get('anomalies', {}),
                figures=figures
            )

            # 生成 PDF 報告
            pdf_file = self.report_gen.create_pdf_report(analyses, figures)

            logger.info(f"報表已生成:")
            logger.info(f"  - Excel: {excel_file}")
            logger.info(f"  - PDF: {pdf_file}")

            return excel_file, pdf_file
        except Exception as e:
            logger.error(f"報表生成失敗: {e}")
            return None, None

    def run(self):
        """執行完整流程"""
        try:
            logger.info("=" * 60)
            logger.info("Sales Intelligence Dashboard - 開始執行")
            logger.info("=" * 60)

            # 1. 載入資料
            if not self.load_and_prepare_data():
                return {
                    'status': 'failed',
                    'error': '資料載入失敗'
                }

            # 2. 執行分析
            self.analyses = {
                'overview': self.analyze_sales_overview(),
                'products': self.analyze_products(),
                'regions': self.analyze_regions(),
                'anomalies': self.detect_anomalies()
            }

            # 3. 生成視覺化
            self.figures = self.generate_visualizations(self.analyses)

            # 4. 產生報表
            excel_file, pdf_file = self.generate_reports(self.analyses, self.figures)

            logger.info("=" * 60)
            logger.info("Sales Intelligence Dashboard - 執行完成！")
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
            return {
                'status': 'failed',
                'error': str(e)
            }

    def schedule_daily_run(self, hour=8, minute=0):
        """
        排程每日執行

        Args:
            hour (int): 執行小時
            minute (int): 執行分鐘
        """
        try:
            import schedule

            def job():
                logger.info(f"執行排程任務: {datetime.now()}")
                self.run()

            schedule.every().day.at(f"{hour:02d}:{minute:02d}").do(job)
            logger.info(f"已排程每日 {hour:02d}:{minute:02d} 執行")

            return schedule
        except ImportError:
            logger.warning("schedule 模組未安裝，無法設置排程")
            return None


def main():
    """主函數"""
    import sys
    import argparse

    parser = argparse.ArgumentParser(description='Sales Intelligence Dashboard')
    parser.add_argument('--config', default='config.yaml', help='配置文件路徑')
    parser.add_argument('--schedule', action='store_true', help='啟用排程模式')
    parser.add_argument('--hour', type=int, default=8, help='每日執行小時')

    args = parser.parse_args()

    try:
        dashboard = SalesIntelligenceDashboard(args.config)
        result = dashboard.run()

        if result['status'] == 'success':
            print("\n✓ 銷售智能儀表板執行成功！")
            print(f"  Excel 報表: {result['outputs']['excel']}")
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
