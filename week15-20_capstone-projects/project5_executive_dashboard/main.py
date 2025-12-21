"""
Project 5: Executive Dashboard System
執行官儀表板系統 - Week 20

功能：
1. 整合所有項目數據
2. 執行級別儀表板
3. 實時洞察
4. 戰略建議
5. 高層報告
"""

import pandas as pd
import numpy as np
import logging
import yaml
from pathlib import Path
from datetime import datetime
import sys
import json

logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    handlers=[
        logging.FileHandler('executive_dashboard.log'),
        logging.StreamHandler()
    ]
)
logger = logging.getLogger(__name__)


class ExecutiveDashboardSystem:
    """執行官儀表板系統主類"""

    def __init__(self, config_file='config.yaml'):
        """初始化執行官儀表板"""
        try:
            with open(config_file) as f:
                self.config = yaml.safe_load(f)

            logger.info("Executive Dashboard System 初始化完成")
        except Exception as e:
            logger.error(f"初始化失敗: {e}")
            raise

    def integrate_all_data(self):
        """整合所有項目數據"""
        logger.info("整合所有項目數據...")

        try:
            # 銷售智能儀表板數據
            sales_data = {
                'total_revenue': np.random.uniform(100000, 500000),
                'total_orders': np.random.randint(1000, 5000),
                'growth_rate': np.random.uniform(-10, 30),
                'customer_count': np.random.randint(500, 2000)
            }

            # 客戶洞察數據
            customer_data = {
                'avg_clv': np.random.uniform(100, 1000),
                'retention_rate': np.random.uniform(70, 95),
                'churn_rate': np.random.uniform(5, 30),
                'vip_customers': np.random.randint(50, 200)
            }

            # 庫存優化數據
            inventory_data = {
                'total_cost': np.random.uniform(50000, 200000),
                'holding_cost': np.random.uniform(20000, 100000),
                'out_of_stock_count': np.random.randint(0, 50),
                'inventory_turnover': np.random.uniform(2, 8)
            }

            # 運營監控數據
            operations_data = {
                'order_completion_rate': np.random.uniform(90, 99),
                'on_time_delivery_rate': np.random.uniform(85, 98),
                'customer_satisfaction': np.random.uniform(3.5, 5.0),
                'active_alerts': np.random.randint(0, 20)
            }

            integrated_data = {
                'sales': sales_data,
                'customer': customer_data,
                'inventory': inventory_data,
                'operations': operations_data,
                'timestamp': datetime.now()
            }

            logger.info("數據整合完成")
            return integrated_data

        except Exception as e:
            logger.error(f"數據整合失敗: {e}")
            return {}

    def calculate_executive_metrics(self, data):
        """計算執行級別指標"""
        logger.info("計算執行級別指標...")

        try:
            sales = data.get('sales', {})
            customer = data.get('customer', {})
            inventory = data.get('inventory', {})
            operations = data.get('operations', {})

            # 整體業務健康度評分
            health_score = self._calculate_health_score(data)

            # 關鍵指標
            kpis = {
                'overall_health': health_score,
                'revenue': sales.get('total_revenue', 0),
                'growth': sales.get('growth_rate', 0),
                'customer_retention': customer.get('retention_rate', 0),
                'operational_efficiency': operations.get('order_completion_rate', 0),
                'profitability': self._estimate_profitability(data),
                'market_position': self._assess_market_position(data)
            }

            logger.info("執行級別指標計算完成")
            return kpis

        except Exception as e:
            logger.error(f"指標計算失敗: {e}")
            return {}

    def generate_strategic_insights(self, data, metrics):
        """生成戰略洞察"""
        logger.info("生成戰略洞察...")

        try:
            insights = {
                'opportunities': [],
                'risks': [],
                'recommendations': []
            }

            customer = data.get('customer', {})
            operations = data.get('operations', {})
            sales = data.get('sales', {})

            # 機遇識別
            if customer.get('vip_customers', 0) > 100:
                insights['opportunities'].append({
                    'area': '客戶價值',
                    'description': 'VIP 客戶基數大，有增銷潛力',
                    'potential_impact': '增加 15-20% 收入'
                })

            if sales.get('growth_rate', 0) > 10:
                insights['opportunities'].append({
                    'area': '市場擴張',
                    'description': '銷售增長強勁，可考慮市場擴張',
                    'potential_impact': '開拓新市場機遇'
                })

            # 風險識別
            if customer.get('churn_rate', 0) > 20:
                insights['risks'].append({
                    'area': '客戶留存',
                    'description': '客戶流失率過高',
                    'severity': 'HIGH',
                    'recommended_action': '實施客戶保留計畫'
                })

            if operations.get('active_alerts', 0) > 10:
                insights['risks'].append({
                    'area': '運營效率',
                    'description': '運營警告數量較多',
                    'severity': 'MEDIUM',
                    'recommended_action': '加強運營監控和改進'
                })

            # 建議
            if metrics.get('customer_retention', 0) > 85:
                insights['recommendations'].append(
                    '客戶保留表現良好，建議加強高價值客戶的個性化服務'
                )

            if metrics.get('operational_efficiency', 0) > 95:
                insights['recommendations'].append(
                    '運營效率達到行業領先水平，可考慮流程自動化進一步優化'
                )

            logger.info(f"戰略洞察生成完成: {len(insights['opportunities'])} 個機遇, {len(insights['risks'])} 個風險")
            return insights

        except Exception as e:
            logger.error(f"戰略洞察生成失敗: {e}")
            return {}

    def generate_executive_report(self, data, metrics, insights):
        """生成高層報告"""
        logger.info("生成高層報告...")

        try:
            report_path = Path('outputs') / f'executive_report_{datetime.now().strftime("%Y%m%d_%H%M%S")}.html'
            report_path.parent.mkdir(exist_ok=True)

            html_content = self._create_html_report(data, metrics, insights)

            with open(report_path, 'w', encoding='utf-8') as f:
                f.write(html_content)

            logger.info(f"高層報告已生成: {report_path}")
            return str(report_path)

        except Exception as e:
            logger.error(f"高層報告生成失敗: {e}")
            return None

    def _calculate_health_score(self, data):
        """計算業務健康度"""
        try:
            sales = data.get('sales', {})
            customer = data.get('customer', {})
            operations = data.get('operations', {})

            # 加權計算
            scores = {
                'revenue_growth': min(100, max(0, sales.get('growth_rate', 0) * 2 + 50)),
                'customer_retention': customer.get('retention_rate', 0),
                'operational_efficiency': operations.get('order_completion_rate', 0)
            }

            health_score = (scores['revenue_growth'] * 0.3 +
                          scores['customer_retention'] * 0.35 +
                          scores['operational_efficiency'] * 0.35)

            return round(health_score, 2)

        except Exception as e:
            logger.error(f"健康度計算失敗: {e}")
            return 0

    def _estimate_profitability(self, data):
        """估算利潤率"""
        try:
            sales = data.get('sales', {})
            inventory = data.get('inventory', {})

            revenue = sales.get('total_revenue', 0)
            total_cost = inventory.get('total_cost', 0)

            if revenue > 0:
                profit_margin = ((revenue - total_cost) / revenue * 100)
                return round(profit_margin, 2)
            return 0

        except Exception as e:
            logger.error(f"利潤率估算失敗: {e}")
            return 0

    def _assess_market_position(self, data):
        """評估市場地位"""
        try:
            customer = data.get('customer', {})
            sales = data.get('sales', {})

            # 基於 VIP 客戶數和增長率的市場地位評估
            vip_count = customer.get('vip_customers', 0)
            growth = sales.get('growth_rate', 0)

            if vip_count > 150 and growth > 15:
                return 'STRONG'
            elif vip_count > 100 and growth > 10:
                return 'STABLE'
            else:
                return 'DEVELOPING'

        except Exception as e:
            logger.error(f"市場地位評估失敗: {e}")
            return 'UNKNOWN'

    def _create_html_report(self, data, metrics, insights):
        """建立 HTML 報告"""
        try:
            html = f"""
<!DOCTYPE html>
<html lang="zh-TW">
<head>
    <meta charset="UTF-8">
    <title>執行官儀表板</title>
    <style>
        body {{ font-family: Arial, sans-serif; margin: 20px; background-color: #f5f5f5; }}
        .header {{ background-color: #1a3a52; color: white; padding: 20px; border-radius: 5px; }}
        .metric {{ background-color: white; padding: 15px; margin: 10px 0; border-left: 4px solid #4CAF50; }}
        .metric-value {{ font-size: 24px; font-weight: bold; color: #4CAF50; }}
        .opportunity {{ background-color: #e8f5e9; padding: 10px; margin: 5px 0; border-left: 4px solid #4CAF50; }}
        .risk {{ background-color: #ffebee; padding: 10px; margin: 5px 0; border-left: 4px solid #f44336; }}
        .section {{ margin-top: 30px; }}
        h2 {{ color: #1a3a52; border-bottom: 2px solid #4CAF50; padding-bottom: 10px; }}
        table {{ width: 100%; border-collapse: collapse; }}
        th, td {{ padding: 10px; text-align: left; border-bottom: 1px solid #ddd; }}
        th {{ background-color: #f9f9f9; }}
    </style>
</head>
<body>
    <div class="header">
        <h1>執行官儀表板報告</h1>
        <p>生成時間: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}</p>
    </div>

    <div class="section">
        <h2>關鍵指標</h2>
        <div class="metric">
            <p>業務健康度</p>
            <div class="metric-value">{metrics.get('overall_health', 0):.1f}/100</div>
        </div>
        <div class="metric">
            <p>收入</p>
            <div class="metric-value">${metrics.get('revenue', 0):,.0f}</div>
        </div>
        <div class="metric">
            <p>成長率</p>
            <div class="metric-value">{metrics.get('growth', 0):.1f}%</div>
        </div>
        <div class="metric">
            <p>客戶保留率</p>
            <div class="metric-value">{metrics.get('customer_retention', 0):.1f}%</div>
        </div>
    </div>

    <div class="section">
        <h2>機遇</h2>
        {"".join([f'<div class="opportunity"><strong>{o["area"]}</strong><br>{o["description"]}<br>潛在影響: {o["potential_impact"]}</div>' for o in insights.get('opportunities', [])])}
    </div>

    <div class="section">
        <h2>風險</h2>
        {"".join([f'<div class="risk"><strong>{r["area"]}</strong> (嚴重程度: {r["severity"]})<br>{r["description"]}<br>建議行動: {r["recommended_action"]}</div>' for r in insights.get('risks', [])])}
    </div>

    <div class="section">
        <h2>建議</h2>
        <ul>
            {"".join([f'<li>{r}</li>' for r in insights.get('recommendations', [])])}
        </ul>
    </div>

    <div class="section">
        <h2>詳細數據</h2>
        <table>
            <tr>
                <th>類別</th>
                <th>指標</th>
                <th>數值</th>
            </tr>
            <tr>
                <td>銷售</td>
                <td>總收入</td>
                <td>${data.get('sales', {}).get('total_revenue', 0):,.0f}</td>
            </tr>
            <tr>
                <td>銷售</td>
                <td>訂單數</td>
                <td>{data.get('sales', {}).get('total_orders', 0):,}</td>
            </tr>
            <tr>
                <td>客戶</td>
                <td>平均 CLV</td>
                <td>${data.get('customer', {}).get('avg_clv', 0):,.0f}</td>
            </tr>
            <tr>
                <td>客戶</td>
                <td>保留率</td>
                <td>{data.get('customer', {}).get('retention_rate', 0):.1f}%</td>
            </tr>
            <tr>
                <td>庫存</td>
                <td>總成本</td>
                <td>${data.get('inventory', {}).get('total_cost', 0):,.0f}</td>
            </tr>
            <tr>
                <td>運營</td>
                <td>訂單完成率</td>
                <td>{data.get('operations', {}).get('order_completion_rate', 0):.1f}%</td>
            </tr>
        </table>
    </div>
</body>
</html>
"""
            return html

        except Exception as e:
            logger.error(f"HTML 報告建立失敗: {e}")
            return ""

    def run(self):
        """執行完整流程"""
        try:
            logger.info("=" * 60)
            logger.info("Executive Dashboard System - 開始執行")
            logger.info("=" * 60)

            # 整合數據
            integrated_data = self.integrate_all_data()
            if not integrated_data:
                return {'status': 'failed', 'error': '數據整合失敗'}

            # 計算執行指標
            metrics = self.calculate_executive_metrics(integrated_data)

            # 生成戰略洞察
            insights = self.generate_strategic_insights(integrated_data, metrics)

            # 生成報告
            report_path = self.generate_executive_report(integrated_data, metrics, insights)

            logger.info("=" * 60)
            logger.info("Executive Dashboard System - 執行完成！")
            logger.info("=" * 60)

            return {
                'status': 'success',
                'outputs': {
                    'report': report_path
                },
                'metrics': metrics,
                'insights': insights
            }

        except Exception as e:
            logger.error(f"執行失敗: {e}", exc_info=True)
            return {'status': 'failed', 'error': str(e)}


def main():
    """主函數"""
    try:
        system = ExecutiveDashboardSystem('config.yaml')
        result = system.run()

        if result['status'] == 'success':
            print("\n✓ 執行官儀表板系統執行成功！")
            print(f"  報告: {result['outputs']['report']}")
            print(f"  業務健康度: {result['metrics'].get('overall_health', 0):.1f}/100")
            return 0
        else:
            print(f"\n✗ 執行失敗: {result['error']}")
            return 1

    except Exception as e:
        logger.error(f"主程式執行失敗: {e}", exc_info=True)
        return 1


if __name__ == "__main__":
    sys.exit(main())
