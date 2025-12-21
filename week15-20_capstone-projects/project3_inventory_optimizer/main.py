"""
Project 3: Inventory Optimization System
庫存優化系統 - Week 18

功能：
1. 需求預測（Demand Forecasting）
2. 庫存優化（Inventory Optimization）
3. 安全庫存計算（Safety Stock）
4. 訂單點計算（Reorder Point）
5. ABC 庫存分類
6. 自動補充建議
7. 成本分析
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
        logging.FileHandler('inventory_optimizer.log'),
        logging.StreamHandler()
    ]
)
logger = logging.getLogger(__name__)


class InventoryOptimizationSystem:
    """庫存優化系統主類"""

    def __init__(self, config_file='config.yaml'):
        """初始化庫存優化系統"""
        try:
            with open(config_file) as f:
                self.config = yaml.safe_load(f)

            logger.info("Inventory Optimization System 初始化完成")
        except Exception as e:
            logger.error(f"初始化失敗: {e}")
            raise

    def load_inventory_data(self):
        """載入庫存數據"""
        logger.info("載入庫存數據...")

        try:
            # 建立示範數據
            np.random.seed(42)
            n_products = 200

            products = pd.DataFrame({
                'product_id': [f'SKU_{i:05d}' for i in range(1, n_products + 1)],
                'product_name': [f'Product_{i}' for i in range(1, n_products + 1)],
                'category': np.random.choice(['Electronics', 'Clothing', 'Food', 'Books'], n_products),
                'current_stock': np.random.randint(10, 1000, n_products),
                'reorder_point': np.random.randint(20, 200, n_products),
                'lead_time_days': np.random.randint(3, 30, n_products),
                'unit_cost': np.random.uniform(5, 500, n_products),
                'holding_cost_rate': 0.2,
                'ordering_cost': np.random.uniform(10, 100, n_products)
            })

            # 歷史銷售數據
            sales = pd.DataFrame({
                'product_id': np.random.choice(products['product_id'], 5000),
                'date': pd.date_range(start='2023-01-01', periods=5000, freq='3H'),
                'quantity_sold': np.random.randint(1, 20, 5000),
                'selling_price': np.random.uniform(10, 600, 5000)
            })

            return {'products': products, 'sales': sales}

        except Exception as e:
            logger.error(f"數據加載失敗: {e}")
            return {}

    def forecast_demand(self, data):
        """預測需求"""
        logger.info("執行需求預測...")

        try:
            sales = data['sales']
            sales['date'] = pd.to_datetime(sales['date'])

            daily_demand = sales.groupby(['product_id', sales['date'].dt.date])['quantity_sold'].sum().reset_index()
            daily_demand.columns = ['product_id', 'date', 'daily_demand']

            # 簡單移動平均預測
            forecasts = {}
            for product_id in daily_demand['product_id'].unique():
                product_sales = daily_demand[daily_demand['product_id'] == product_id]
                if len(product_sales) > 7:
                    # 7 日移動平均
                    avg = product_sales['daily_demand'].tail(7).mean()
                    # 標準差用於波動性
                    std = product_sales['daily_demand'].std()
                    forecasts[product_id] = {
                        'daily_average': avg,
                        'daily_std': std,
                        'trend': self._calculate_trend(product_sales['daily_demand'].values)
                    }

            logger.info(f"需求預測完成: {len(forecasts)} 個產品")
            return forecasts

        except Exception as e:
            logger.error(f"需求預測失敗: {e}")
            return {}

    def optimize_inventory(self, data, forecasts):
        """優化庫存"""
        logger.info("執行庫存優化...")

        try:
            products = data['products']

            optimizations = {}

            for idx, row in products.iterrows():
                product_id = row['product_id']

                if product_id in forecasts:
                    forecast = forecasts[product_id]
                    daily_demand = forecast['daily_average']
                    demand_std = forecast['daily_std']
                    lead_time = row['lead_time_days']

                    # 計算安全庫存
                    service_factor = 1.65  # 95% 服務水平
                    safety_stock = service_factor * demand_std * np.sqrt(lead_time)

                    # 計算訂單點
                    reorder_point = daily_demand * lead_time + safety_stock

                    # 計算經濟訂單量 (EOQ)
                    holding_cost = row['unit_cost'] * row['holding_cost_rate']
                    ordering_cost = row['ordering_cost']
                    eoq = np.sqrt((2 * daily_demand * 365 * ordering_cost) / holding_cost) if holding_cost > 0 else 0

                    optimizations[product_id] = {
                        'daily_demand': daily_demand,
                        'lead_time': lead_time,
                        'safety_stock': max(0, safety_stock),
                        'reorder_point': max(0, reorder_point),
                        'eoq': max(0, eoq),
                        'current_stock': row['current_stock'],
                        'status': self._determine_inventory_status(row['current_stock'], reorder_point)
                    }

            logger.info(f"庫存優化完成: {len(optimizations)} 個產品")
            return optimizations

        except Exception as e:
            logger.error(f"庫存優化失敗: {e}")
            return {}

    def analyze_inventory_costs(self, optimizations, data):
        """分析庫存成本"""
        logger.info("分析庫存成本...")

        try:
            products = data['products']
            cost_analysis = {}

            for product_id, opt in optimizations.items():
                product = products[products['product_id'] == product_id].iloc[0]

                # 持有成本
                avg_inventory = opt['safety_stock'] + opt['eoq'] / 2
                holding_cost = avg_inventory * product['unit_cost'] * product['holding_cost_rate']

                # 訂購成本
                annual_orders = (opt['daily_demand'] * 365) / opt['eoq'] if opt['eoq'] > 0 else 0
                ordering_cost = annual_orders * product['ordering_cost']

                # 缺貨成本（估計）
                stockout_cost = 0

                cost_analysis[product_id] = {
                    'holding_cost': holding_cost,
                    'ordering_cost': ordering_cost,
                    'total_cost': holding_cost + ordering_cost + stockout_cost,
                    'unit_cost': product['unit_cost']
                }

            logger.info("成本分析完成")
            return cost_analysis

        except Exception as e:
            logger.error(f"成本分析失敗: {e}")
            return {}

    def generate_replenishment_orders(self, optimizations, data):
        """生成補充建議"""
        logger.info("生成補充建議...")

        try:
            orders = []

            for product_id, opt in optimizations.items():
                if opt['current_stock'] <= opt['reorder_point']:
                    orders.append({
                        'product_id': product_id,
                        'quantity_to_order': int(opt['eoq']),
                        'urgency': 'HIGH' if opt['current_stock'] < opt['safety_stock'] else 'MEDIUM',
                        'recommended_order_date': datetime.now(),
                        'estimated_arrival': datetime.now() + pd.Timedelta(days=opt['lead_time'])
                    })

            logger.info(f"補充建議生成完成: {len(orders)} 個訂單")
            return pd.DataFrame(orders)

        except Exception as e:
            logger.error(f"補充建議生成失敗: {e}")
            return pd.DataFrame()

    def generate_report(self, data, optimizations, forecasts, costs):
        """產生報告"""
        logger.info("產生報告...")

        try:
            # 簡化的報告生成
            report_path = Path('outputs') / f'inventory_report_{datetime.now().strftime("%Y%m%d_%H%M%S")}.txt'
            report_path.parent.mkdir(exist_ok=True)

            with open(report_path, 'w', encoding='utf-8') as f:
                f.write("庫存優化報告\n")
                f.write("=" * 60 + "\n\n")

                f.write(f"生成時間: {datetime.now()}\n")
                f.write(f"分析產品數: {len(data['products'])}\n")
                f.write(f"優化建議: {len(optimizations)}\n\n")

                # 成本摘要
                total_holding = sum(c.get('holding_cost', 0) for c in costs.values())
                total_ordering = sum(c.get('ordering_cost', 0) for c in costs.values())

                f.write("成本摘要\n")
                f.write("-" * 60 + "\n")
                f.write(f"年度持有成本: ${total_holding:,.2f}\n")
                f.write(f"年度訂購成本: ${total_ordering:,.2f}\n")
                f.write(f"總成本: ${total_holding + total_ordering:,.2f}\n")

            logger.info(f"報告已生成: {report_path}")
            return str(report_path)

        except Exception as e:
            logger.error(f"報告生成失敗: {e}")
            return None

    def _calculate_trend(self, values):
        """計算趨勢"""
        if len(values) < 2:
            return 0
        return (values[-1] - values[0]) / len(values)

    def _determine_inventory_status(self, current_stock, reorder_point):
        """判斷庫存狀態"""
        if current_stock < reorder_point * 0.5:
            return 'CRITICAL'
        elif current_stock < reorder_point:
            return 'LOW'
        else:
            return 'NORMAL'

    def run(self):
        """執行完整流程"""
        try:
            logger.info("=" * 60)
            logger.info("Inventory Optimization System - 開始執行")
            logger.info("=" * 60)

            # 載入數據
            data = self.load_inventory_data()
            if not data:
                return {'status': 'failed', 'error': '數據加載失敗'}

            # 預測需求
            forecasts = self.forecast_demand(data)

            # 優化庫存
            optimizations = self.optimize_inventory(data, forecasts)

            # 分析成本
            costs = self.analyze_inventory_costs(optimizations, data)

            # 生成補充訂單
            replenishment = self.generate_replenishment_orders(optimizations, data)

            # 產生報告
            report_path = self.generate_report(data, optimizations, forecasts, costs)

            logger.info("=" * 60)
            logger.info("Inventory Optimization System - 執行完成！")
            logger.info("=" * 60)

            return {
                'status': 'success',
                'outputs': {
                    'report': report_path
                },
                'summary': {
                    'products_analyzed': len(data['products']),
                    'optimizations': len(optimizations),
                    'replenishment_orders': len(replenishment)
                }
            }

        except Exception as e:
            logger.error(f"執行失敗: {e}", exc_info=True)
            return {'status': 'failed', 'error': str(e)}


def main():
    """主函數"""
    try:
        system = InventoryOptimizationSystem('config.yaml')
        result = system.run()

        if result['status'] == 'success':
            print("\n✓ 庫存優化系統執行成功！")
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
