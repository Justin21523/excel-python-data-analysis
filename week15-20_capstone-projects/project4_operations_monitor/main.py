"""
Project 4: Operations Monitoring System
運營監控系統 - Week 19

功能：
1. 運營指標監控（KPI Monitoring）
2. 實時警告系統（Alert System）
3. 效率分析（Efficiency Analysis）
4. 流程監控（Process Monitoring）
5. 異常檢測（Anomaly Detection）
6. 儀表板視覺化
"""

import pandas as pd
import numpy as np
import logging
import yaml
from pathlib import Path
from datetime import datetime
import sys

logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    handlers=[
        logging.FileHandler('operations_monitor.log'),
        logging.StreamHandler()
    ]
)
logger = logging.getLogger(__name__)


class OperationsMonitoringSystem:
    """運營監控系統主類"""

    def __init__(self, config_file='config.yaml'):
        """初始化運營監控系統"""
        try:
            with open(config_file) as f:
                self.config = yaml.safe_load(f)

            logger.info("Operations Monitoring System 初始化完成")
        except Exception as e:
            logger.error(f"初始化失敗: {e}")
            raise

    def load_operations_data(self):
        """載入運營數據"""
        logger.info("載入運營數據...")

        try:
            np.random.seed(42)
            n_records = 1000

            # 訂單處理數據
            orders = pd.DataFrame({
                'order_id': [f'ORDER_{i:06d}' for i in range(1, n_records + 1)],
                'order_time': pd.date_range(start='2024-01-01', periods=n_records, freq='15min'),
                'processing_time_minutes': np.random.uniform(5, 120, n_records),
                'status': np.random.choice(['completed', 'pending', 'delayed'], n_records),
                'team': np.random.choice(['Team_A', 'Team_B', 'Team_C'], n_records)
            })

            # 客服數據
            support = pd.DataFrame({
                'ticket_id': [f'TICKET_{i:05d}' for i in range(1, 500 + 1)],
                'created_time': pd.date_range(start='2024-01-01', periods=500, freq='30min'),
                'resolved_time': pd.date_range(start='2024-01-02', periods=500, freq='30min'),
                'resolution_time_minutes': np.random.uniform(10, 480, 500),
                'satisfaction_score': np.random.uniform(1, 5, 500),
                'category': np.random.choice(['billing', 'technical', 'shipping'], 500)
            })

            # 庫存動作
            inventory = pd.DataFrame({
                'action_id': [f'INV_{i:05d}' for i in range(1, 300 + 1)],
                'timestamp': pd.date_range(start='2024-01-01', periods=300, freq='2H'),
                'action_type': np.random.choice(['receive', 'ship', 'adjustment'], 300),
                'quantity': np.random.randint(1, 100, 300),
                'warehouse': np.random.choice(['WH_A', 'WH_B', 'WH_C'], 300)
            })

            return {
                'orders': orders,
                'support': support,
                'inventory': inventory
            }

        except Exception as e:
            logger.error(f"運營數據加載失敗: {e}")
            return {}

    def monitor_kpis(self, data):
        """監控 KPI 指標"""
        logger.info("監控 KPI 指標...")

        try:
            kpis = {}

            # 訂單相關 KPI
            orders = data['orders']
            kpis['order_metrics'] = {
                'total_orders': len(orders),
                'avg_processing_time': orders['processing_time_minutes'].mean(),
                'completion_rate': (orders['status'] == 'completed').sum() / len(orders) * 100,
                'on_time_rate': (orders['processing_time_minutes'] < 60).sum() / len(orders) * 100,
                'delayed_count': (orders['status'] == 'delayed').sum()
            }

            # 客服相關 KPI
            support = data['support']
            support['resolved_time'] = pd.to_datetime(support['resolved_time'])
            support['created_time'] = pd.to_datetime(support['created_time'])

            kpis['support_metrics'] = {
                'total_tickets': len(support),
                'avg_resolution_time': support['resolution_time_minutes'].mean(),
                'avg_satisfaction': support['satisfaction_score'].mean(),
                'satisfaction_rate': (support['satisfaction_score'] >= 4).sum() / len(support) * 100
            }

            # 庫存相關 KPI
            inventory = data['inventory']
            kpis['inventory_metrics'] = {
                'total_actions': len(inventory),
                'avg_quantity_per_action': inventory['quantity'].mean(),
                'warehouse_utilization': inventory['warehouse'].value_counts().to_dict()
            }

            logger.info(f"KPI 監控完成: {len(kpis)} 個指標集")
            return kpis

        except Exception as e:
            logger.error(f"KPI 監控失敗: {e}")
            return {}

    def detect_anomalies(self, data):
        """檢測異常"""
        logger.info("檢測異常...")

        try:
            anomalies = []

            # 訂單異常
            orders = data['orders']
            processing_mean = orders['processing_time_minutes'].mean()
            processing_std = orders['processing_time_minutes'].std()

            outliers = orders[
                (orders['processing_time_minutes'] > processing_mean + 3 * processing_std) |
                (orders['processing_time_minutes'] < processing_mean - 3 * processing_std)
            ]

            for idx, row in outliers.iterrows():
                anomalies.append({
                    'type': 'order_processing_time',
                    'severity': 'HIGH' if row['processing_time_minutes'] > processing_mean + 3 * processing_std else 'MEDIUM',
                    'description': f"Order {row['order_id']} processing time: {row['processing_time_minutes']:.1f} minutes",
                    'timestamp': row['order_time']
                })

            # 客服異常
            support = data['support']
            resolution_mean = support['resolution_time_minutes'].mean()
            resolution_std = support['resolution_time_minutes'].std()

            slow_tickets = support[support['resolution_time_minutes'] > resolution_mean + 2 * resolution_std]

            for idx, row in slow_tickets.iterrows():
                anomalies.append({
                    'type': 'slow_ticket_resolution',
                    'severity': 'MEDIUM',
                    'description': f"Ticket {row['ticket_id']} took {row['resolution_time_minutes']:.1f} minutes",
                    'timestamp': row['created_time']
                })

            logger.info(f"異常檢測完成: {len(anomalies)} 個異常")
            return anomalies

        except Exception as e:
            logger.error(f"異常檢測失敗: {e}")
            return []

    def generate_alerts(self, kpis, anomalies):
        """生成警告"""
        logger.info("生成警告...")

        try:
            alerts = []

            # 基於 KPI 的警告
            order_kpis = kpis.get('order_metrics', {})

            if order_kpis.get('completion_rate', 100) < 95:
                alerts.append({
                    'level': 'WARNING',
                    'message': f"訂單完成率低: {order_kpis.get('completion_rate', 0):.1f}%",
                    'timestamp': datetime.now()
                })

            if order_kpis.get('on_time_rate', 100) < 90:
                alerts.append({
                    'level': 'ALERT',
                    'message': f"準時率低: {order_kpis.get('on_time_rate', 0):.1f}%",
                    'timestamp': datetime.now()
                })

            # 基於異常的警告
            for anomaly in anomalies:
                if anomaly['severity'] == 'HIGH':
                    alerts.append({
                        'level': 'CRITICAL',
                        'message': anomaly['description'],
                        'timestamp': anomaly['timestamp']
                    })

            logger.info(f"警告生成完成: {len(alerts)} 個警告")
            return alerts

        except Exception as e:
            logger.error(f"警告生成失敗: {e}")
            return []

    def analyze_efficiency(self, data, kpis):
        """分析效率"""
        logger.info("分析效率...")

        try:
            efficiency = {}

            # 訂單處理效率
            orders = data['orders']
            for team in orders['team'].unique():
                team_orders = orders[orders['team'] == team]
                efficiency[team] = {
                    'avg_processing_time': team_orders['processing_time_minutes'].mean(),
                    'completion_rate': (team_orders['status'] == 'completed').sum() / len(team_orders) * 100,
                    'total_orders': len(team_orders)
                }

            # 客服效率
            support = data['support']
            efficiency['support_center'] = {
                'avg_resolution_time': support['resolution_time_minutes'].mean(),
                'avg_satisfaction': support['satisfaction_score'].mean(),
                'high_satisfaction_rate': (support['satisfaction_score'] >= 4).sum() / len(support) * 100
            }

            logger.info("效率分析完成")
            return efficiency

        except Exception as e:
            logger.error(f"效率分析失敗: {e}")
            return {}

    def generate_report(self, kpis, anomalies, alerts, efficiency):
        """產生監控報告"""
        logger.info("產生監控報告...")

        try:
            report_path = Path('outputs') / f'operations_report_{datetime.now().strftime("%Y%m%d_%H%M%S")}.txt'
            report_path.parent.mkdir(exist_ok=True)

            with open(report_path, 'w', encoding='utf-8') as f:
                f.write("運營監控報告\n")
                f.write("=" * 60 + "\n\n")

                f.write(f"生成時間: {datetime.now()}\n\n")

                # KPI 摘要
                f.write("KPI 指標摘要\n")
                f.write("-" * 60 + "\n")

                order_kpis = kpis.get('order_metrics', {})
                f.write(f"訂單完成率: {order_kpis.get('completion_rate', 0):.1f}%\n")
                f.write(f"準時交付率: {order_kpis.get('on_time_rate', 0):.1f}%\n")
                f.write(f"平均處理時間: {order_kpis.get('avg_processing_time', 0):.1f} 分鐘\n\n")

                support_kpis = kpis.get('support_metrics', {})
                f.write(f"客服平均滿意度: {support_kpis.get('avg_satisfaction', 0):.2f}/5.0\n")
                f.write(f"平均解決時間: {support_kpis.get('avg_resolution_time', 0):.1f} 分鐘\n\n")

                # 異常檢測
                f.write("檢測到的異常\n")
                f.write("-" * 60 + "\n")
                f.write(f"總異常數: {len(anomalies)}\n")
                if anomalies:
                    for anomaly in anomalies[:5]:
                        f.write(f"  - {anomaly['description']}\n")

                # 警告
                f.write("\n警告信息\n")
                f.write("-" * 60 + "\n")
                f.write(f"總警告數: {len(alerts)}\n")
                if alerts:
                    for alert in alerts[:5]:
                        f.write(f"  [{alert['level']}] {alert['message']}\n")

            logger.info(f"報告已生成: {report_path}")
            return str(report_path)

        except Exception as e:
            logger.error(f"報告生成失敗: {e}")
            return None

    def run(self):
        """執行完整流程"""
        try:
            logger.info("=" * 60)
            logger.info("Operations Monitoring System - 開始執行")
            logger.info("=" * 60)

            # 載入數據
            data = self.load_operations_data()
            if not data:
                return {'status': 'failed', 'error': '數據加載失敗'}

            # 監控 KPI
            kpis = self.monitor_kpis(data)

            # 檢測異常
            anomalies = self.detect_anomalies(data)

            # 生成警告
            alerts = self.generate_alerts(kpis, anomalies)

            # 分析效率
            efficiency = self.analyze_efficiency(data, kpis)

            # 產生報告
            report_path = self.generate_report(kpis, anomalies, alerts, efficiency)

            logger.info("=" * 60)
            logger.info("Operations Monitoring System - 執行完成！")
            logger.info("=" * 60)

            return {
                'status': 'success',
                'outputs': {
                    'report': report_path
                },
                'summary': {
                    'kpis': len(kpis),
                    'anomalies': len(anomalies),
                    'alerts': len(alerts)
                }
            }

        except Exception as e:
            logger.error(f"執行失敗: {e}", exc_info=True)
            return {'status': 'failed', 'error': str(e)}


def main():
    """主函數"""
    try:
        system = OperationsMonitoringSystem('config.yaml')
        result = system.run()

        if result['status'] == 'success':
            print("\n✓ 運營監控系統執行成功！")
            print(f"  報告: {result['outputs']['report']}")
            return 0
        else:
            print(f"\n✗ 執行失敗: {result['error']}")
            return 1

    except Exception as e:
        logger.error(f"主程式執行失敗: {e}", exc_info=True)
        return 1


if __name__ == "__main__":
    sys.exit(main())
