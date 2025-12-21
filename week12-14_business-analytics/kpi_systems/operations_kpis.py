"""
營運 KPI 系統 - Week 14
功能：
1. 訂單履行 KPI
2. 配送效率
3. 退貨和售後服務
4. 庫存效率
5. 供應鏈性能

Author: Business Analytics Week 12-14
Date: 2024-12-11
"""

import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
from datetime import datetime, timedelta
import sys
from pathlib import Path
import warnings

warnings.filterwarnings('ignore')

sys.path.append(str(Path(__file__).parent.parent.parent / 'week03-06_pandas-advanced' / 'utils'))
from data_loader import load_olist_data


class OperationsKPISystem:
    """營運 KPI 系統"""

    def __init__(self, orders, order_items, products, sellers):
        """初始化"""
        self.orders = orders
        self.order_items = order_items
        self.products = products
        self.sellers = sellers

    def calculate_fulfillment_kpis(self):
        """計算訂單履行 KPI"""
        print("計算訂單履行 KPI...")

        # 確保日期列是 datetime 類型
        date_cols = ['order_purchase_timestamp', 'order_approved_at',
                    'order_delivered_carrier_date', 'order_delivered_customer_date',
                    'order_estimated_delivery_date']

        for col in date_cols:
            if col in self.orders.columns:
                self.orders[col] = pd.to_datetime(self.orders[col], errors='coerce')

        # 計算各個週期
        kpis = {}

        # 審批時間（購買到審批）
        if 'order_approved_at' in self.orders.columns:
            approval_time = (self.orders['order_approved_at'] -
                           self.orders['order_purchase_timestamp']).dt.total_seconds() / 3600
            kpis['avg_approval_time_hours'] = approval_time.mean()

        # 配送時間（審批到配送）
        if 'order_delivered_carrier_date' in self.orders.columns:
            shipping_time = (self.orders['order_delivered_carrier_date'] -
                           self.orders['order_approved_at']).dt.total_seconds() / 3600
            kpis['avg_shipping_time_hours'] = shipping_time.mean()

        # 交付時間（購買到交付）
        if 'order_delivered_customer_date' in self.orders.columns:
            delivered = self.orders[self.orders['order_delivered_customer_date'].notna()]
            fulfillment_time = (delivered['order_delivered_customer_date'] -
                              delivered['order_purchase_timestamp']).dt.days
            kpis['avg_fulfillment_days'] = fulfillment_time.mean()

        # 準時交付率
        if 'order_estimated_delivery_date' in self.orders.columns and 'order_delivered_customer_date' in self.orders.columns:
            delivered = self.orders[self.orders['order_delivered_customer_date'].notna() &
                                   self.orders['order_estimated_delivery_date'].notna()]
            on_time = (delivered['order_delivered_customer_date'] <=
                      delivered['order_estimated_delivery_date']).sum()
            kpis['on_time_delivery_rate'] = (on_time / len(delivered) * 100) if len(delivered) > 0 else 0

        # 訂單狀態分布
        kpis['order_status_distribution'] = self.orders['order_status'].value_counts()

        return kpis

    def calculate_seller_performance(self):
        """計算賣家性能"""
        print("計算賣家性能...")

        seller_perf = self.order_items.merge(
            self.orders[['order_id', 'order_status', 'order_delivered_customer_date']],
            on='order_id', how='left'
        )

        seller_stats = seller_perf.groupby('seller_id').agg({
            'order_id': 'count',
            'price': 'sum'
        }).reset_index()

        seller_stats.columns = ['seller_id', 'total_orders', 'total_revenue']

        seller_stats = seller_stats.sort_values('total_revenue', ascending=False)

        # 賣家等級
        seller_stats['tier'] = pd.qcut(seller_stats['total_revenue'], q=4,
                                      labels=['Bronze', 'Silver', 'Gold', 'Platinum'],
                                      duplicates='drop')

        return seller_stats

    def calculate_product_performance(self):
        """計算商品性能"""
        print("計算商品性能...")

        prod_perf = self.order_items.copy()

        product_stats = prod_perf.groupby('product_id').agg({
            'order_item_id': 'count',
            'price': 'sum'
        }).reset_index()

        product_stats.columns = ['product_id', 'units_sold', 'total_revenue']

        product_stats = product_stats.sort_values('total_revenue', ascending=False)

        return product_stats

    def calculate_return_rates(self):
        """計算退貨率"""
        print("計算退貨率...")

        # 假設 cancelled 和 unavailable 狀態為退貨
        return_statuses = ['cancelled', 'unavailable']
        total_orders = len(self.orders)
        returned_orders = len(self.orders[self.orders['order_status'].isin(return_statuses)])

        return_rate = (returned_orders / total_orders * 100) if total_orders > 0 else 0

        return {
            'return_rate': return_rate,
            'total_orders': total_orders,
            'returned_orders': returned_orders
        }

    def calculate_inventory_metrics(self):
        """計算庫存指標"""
        print("計算庫存指標...")

        # 商品多樣性
        unique_products = self.products['product_id'].nunique()

        # 活躍商品（被銷售過）
        sold_products = self.order_items['product_id'].nunique()

        # 商品周轉率
        product_turnover = self.order_items.groupby('product_id').size().describe()

        metrics = {
            'total_products': len(self.products),
            'unique_products': unique_products,
            'sold_products': sold_products,
            'active_product_ratio': (sold_products / unique_products * 100) if unique_products > 0 else 0,
            'avg_product_sales': product_turnover['mean'],
            'median_product_sales': product_turnover['50%']
        }

        return metrics

    def visualize_dashboard(self, output_dir='./operations_kpi_outputs'):
        """可視化儀表板"""
        import os
        os.makedirs(output_dir, exist_ok=True)

        print("繪製營運 KPI 儀表板...")

        fig, axes = plt.subplots(2, 3, figsize=(18, 10))
        fig.suptitle('Operations KPI Dashboard', fontsize=16, fontweight='bold')

        # 1. 訂單狀態分布
        fulfillment = self.calculate_fulfillment_kpis()
        ax1 = axes[0, 0]
        status_dist = fulfillment['order_status_distribution']
        ax1.pie(status_dist.values, labels=status_dist.index, autopct='%1.1f%%')
        ax1.set_title('Order Status Distribution', fontweight='bold')

        # 2. 準時交付率
        ax2 = axes[0, 1]
        on_time_rate = fulfillment.get('on_time_delivery_rate', 0)
        ax2.text(0.5, 0.7, f"{on_time_rate:.1f}%", ha='center', va='center',
                fontsize=20, fontweight='bold', color='green' if on_time_rate > 90 else 'red')
        ax2.text(0.5, 0.3, "On-Time Delivery Rate", ha='center', va='center', fontsize=12)
        ax2.axis('off')

        # 3. 平均履行時間
        ax3 = axes[0, 2]
        fulfillment_days = fulfillment.get('avg_fulfillment_days', 0)
        ax3.text(0.5, 0.7, f"{fulfillment_days:.1f}", ha='center', va='center',
                fontsize=20, fontweight='bold')
        ax3.text(0.5, 0.3, "Avg Fulfillment (Days)", ha='center', va='center', fontsize=12)
        ax3.axis('off')

        # 4. 賣家分級
        ax4 = axes[1, 0]
        seller_perf = self.calculate_seller_performance()
        tier_dist = seller_perf['tier'].value_counts()
        ax4.bar(tier_dist.index, tier_dist.values)
        ax4.set_title('Seller Distribution by Tier', fontweight='bold')
        ax4.set_ylabel('Count')

        # 5. 退貨率
        ax5 = axes[1, 1]
        return_rate = self.calculate_return_rates()['return_rate']
        ax5.text(0.5, 0.7, f"{return_rate:.2f}%", ha='center', va='center',
                fontsize=20, fontweight='bold', color='orange' if return_rate > 5 else 'green')
        ax5.text(0.5, 0.3, "Return Rate", ha='center', va='center', fontsize=12)
        ax5.axis('off')

        # 6. 商品性能
        ax6 = axes[1, 2]
        inventory = self.calculate_inventory_metrics()
        labels = [f"Total: {inventory['total_products']}", f"Sold: {inventory['sold_products']}"]
        sizes = [inventory['total_products'], inventory['sold_products']]
        ax6.bar(range(len(labels)), sizes, color=['lightblue', 'darkblue'])
        ax6.set_xticks(range(len(labels)))
        ax6.set_xticklabels(labels)
        ax6.set_title('Product Metrics', fontweight='bold')
        ax6.set_ylabel('Count')

        plt.tight_layout()
        fig.savefig(f'{output_dir}/operations_kpi_dashboard.png', dpi=300, bbox_inches='tight')

        return fig

    def generate_report(self, output_dir='./operations_kpi_outputs'):
        """生成報告"""
        import os
        os.makedirs(output_dir, exist_ok=True)

        print("\n" + "="*60)
        print("開始營運 KPI 系統")
        print("="*60 + "\n")

        # 計算各項指標
        fulfillment_kpis = self.calculate_fulfillment_kpis()
        seller_perf = self.calculate_seller_performance()
        product_perf = self.calculate_product_performance()
        return_rates = self.calculate_return_rates()
        inventory_metrics = self.calculate_inventory_metrics()

        # 可視化
        fig = self.visualize_dashboard(output_dir)

        # 保存
        print("\n保存分析結果...")
        seller_perf.to_csv(f'{output_dir}/seller_performance.csv', index=False)
        product_perf.to_csv(f'{output_dir}/product_performance.csv', index=False)

        print(f"✓ 已保存到 {output_dir}/")

        return {
            'fulfillment': fulfillment_kpis,
            'sellers': seller_perf,
            'products': product_perf,
            'returns': return_rates,
            'inventory': inventory_metrics
        }

    def print_summary(self, kpi_dict):
        """打印摘要"""
        print("\n" + "="*80)
        print("營運 KPI 系統摘要")
        print("="*80)

        print(f"\n【訂單履行指標】")
        fulfillment = kpi_dict['fulfillment']
        print(f"  平均審批時間: {fulfillment.get('avg_approval_time_hours', 0):.2f} 小時")
        print(f"  平均配送時間: {fulfillment.get('avg_shipping_time_hours', 0):.2f} 小時")
        print(f"  平均履行時間: {fulfillment.get('avg_fulfillment_days', 0):.2f} 天")
        print(f"  準時交付率: {fulfillment.get('on_time_delivery_rate', 0):.2f}%")

        print(f"\n【售後服務】")
        returns = kpi_dict['returns']
        print(f"  退貨率: {returns['return_rate']:.2f}%")
        print(f"  已退貨訂單: {returns['returned_orders']} / {returns['total_orders']}")

        print(f"\n【賣家性能】")
        sellers = kpi_dict['sellers']
        print(f"  活躍賣家數: {len(sellers)}")
        print(f"  平均賣家收入: ${sellers['total_revenue'].mean():,.2f}")

        print(f"\n【庫存指標】")
        inventory = kpi_dict['inventory']
        print(f"  總商品數: {inventory['total_products']}")
        print(f"  已銷售商品: {inventory['sold_products']}")
        print(f"  活躍率: {inventory['active_product_ratio']:.2f}%")


# ==================== 使用範例 ====================

if __name__ == "__main__":
    print("加載 Olist 資料...")
    orders, order_items, products, customers, sellers, payments, reviews = load_olist_data()

    # 執行分析
    kpi_system = OperationsKPISystem(
        orders=orders,
        order_items=order_items,
        products=products,
        sellers=sellers
    )

    # 生成報告
    kpi_dict = kpi_system.generate_report()

    # 打印摘要
    kpi_system.print_summary(kpi_dict)

    print("\n" + "="*80)
    print("✓ 營運 KPI 系統完成！")
    print("="*80)
