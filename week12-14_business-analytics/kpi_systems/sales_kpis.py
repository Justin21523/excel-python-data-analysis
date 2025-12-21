"""
銷售 KPI 系統 - Week 14
功能：
1. 計算核心銷售 KPI
2. 同比和環比分析
3. KPI 目標設定和追蹤
4. 性能評級
5. 可視化儀表板

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


class SalesKPISystem:
    """銷售 KPI 系統"""

    def __init__(self, orders, order_items, payments):
        """
        Parameters
        ----------
        orders : DataFrame
            訂單資料
        order_items : DataFrame
            訂單項目資料
        payments : DataFrame
            付款資料
        """
        self.orders = orders
        self.order_items = order_items
        self.payments = payments
        self.kpi_data = None

    def calculate_daily_kpis(self):
        """計算日度 KPI"""
        print("計算日度 KPI...")

        # 合併資料
        merged = self.orders.merge(self.payments, on='order_id', how='left')

        # 按日期聚合
        daily_data = merged.groupby(merged['order_purchase_timestamp'].dt.date).agg({
            'order_id': 'nunique',  # 訂單數
            'customer_id': 'nunique',  # 新客戶數
            'payment_value': 'sum'  # 銷售額
        }).reset_index()

        daily_data.columns = ['date', 'orders', 'customers', 'revenue']

        # 計算日均訂單金額
        daily_data['aov'] = daily_data['revenue'] / daily_data['orders']

        # 計算同比數據（簡化版，假設有 1 年數據）
        daily_data['date'] = pd.to_datetime(daily_data['date'])

        return daily_data

    def calculate_monthly_kpis(self):
        """計算月度 KPI"""
        print("計算月度 KPI...")

        merged = self.orders.merge(self.payments, on='order_id', how='left')

        # 按月聚合
        monthly_data = merged.groupby(merged['order_purchase_timestamp'].dt.to_period('M')).agg({
            'order_id': 'nunique',
            'customer_id': 'nunique',
            'payment_value': 'sum'
        }).reset_index()

        monthly_data.columns = ['month', 'orders', 'customers', 'revenue']

        # 計算 KPI
        monthly_data['aov'] = monthly_data['revenue'] / monthly_data['orders']
        monthly_data['revenue_per_customer'] = monthly_data['revenue'] / monthly_data['customers']

        # 環比增長
        monthly_data['revenue_growth_mom'] = monthly_data['revenue'].pct_change() * 100
        monthly_data['order_growth_mom'] = monthly_data['orders'].pct_change() * 100

        return monthly_data

    def calculate_category_kpis(self):
        """計算分類 KPI"""
        print("計算分類 KPI...")

        from data_loader import load_olist_integrated
        df = load_olist_integrated(verbose=False)

        category_kpis = df.groupby('product_category_name_english').agg({
            'order_id': 'nunique',
            'price': 'sum',
            'review_score': 'mean'
        }).reset_index()

        category_kpis.columns = ['category', 'orders', 'revenue', 'avg_rating']
        category_kpis = category_kpis.sort_values('revenue', ascending=False)

        # 計算佔比
        category_kpis['revenue_pct'] = (category_kpis['revenue'] / category_kpis['revenue'].sum() * 100)
        category_kpis['order_pct'] = (category_kpis['orders'] / category_kpis['orders'].sum() * 100)

        return category_kpis

    def calculate_customer_kpis(self):
        """計算客戶相關 KPI"""
        print("計算客戶 KPI...")

        merged = self.orders.merge(self.payments, on='order_id', how='left')

        customer_data = merged.groupby('customer_id').agg({
            'order_id': 'count',
            'order_purchase_timestamp': ['min', 'max'],
            'payment_value': ['sum', 'mean']
        }).reset_index()

        # 計算客戶指標
        total_customers = merged['customer_id'].nunique()
        new_customers = merged.groupby(
            merged['order_purchase_timestamp'].dt.to_period('M')
        )['customer_id'].nunique()
        repeat_customer_rate = (
            len(customer_data[customer_data[('order_id', 'count')] > 1]) /
            total_customers * 100
        )

        kpis = {
            'total_customers': total_customers,
            'new_customers_this_month': new_customers.iloc[-1] if len(new_customers) > 0 else 0,
            'repeat_customer_rate': repeat_customer_rate,
            'avg_customer_value': customer_data[('payment_value', 'sum')].mean(),
        }

        return kpis

    def set_kpi_targets(self, targets=None):
        """設置 KPI 目標"""
        print("設置 KPI 目標...")

        if targets is None:
            # 默認目標（基於當前數據）
            targets = {
                'monthly_revenue': 500000,
                'monthly_orders': 1000,
                'monthly_customers': 500,
                'aov': 500,
                'repeat_rate': 25,
                'avg_rating': 4.5
            }

        return targets

    def evaluate_performance(self, monthly_kpis, targets):
        """評估性能"""
        print("評估性能...")

        latest_month = monthly_kpis.iloc[-1]

        performance = {
            'revenue_vs_target': (latest_month['revenue'] / targets['monthly_revenue'] - 1) * 100,
            'orders_vs_target': (latest_month['orders'] / targets['monthly_orders'] - 1) * 100,
            'aov_vs_target': (latest_month['aov'] / targets['aov'] - 1) * 100,
        }

        # 評級
        for key, value in performance.items():
            if value >= 10:
                performance[key + '_rating'] = 'Excellent'
            elif value >= 0:
                performance[key + '_rating'] = 'Good'
            elif value >= -10:
                performance[key + '_rating'] = 'Fair'
            else:
                performance[key + '_rating'] = 'Poor'

        return performance

    def visualize_dashboard(self, monthly_kpis, category_kpis, output_dir='./kpi_outputs'):
        """可視化 KPI 儀表板"""
        import os
        os.makedirs(output_dir, exist_ok=True)

        print("繪製 KPI 儀表板...")

        fig = plt.figure(figsize=(18, 12))
        gs = fig.add_gridspec(3, 3, hspace=0.3, wspace=0.3)

        # 1. 月度收入趨勢
        ax1 = fig.add_subplot(gs[0, :2])
        ax1.plot(range(len(monthly_kpis)), monthly_kpis['revenue'], marker='o', linewidth=2)
        ax1.fill_between(range(len(monthly_kpis)), monthly_kpis['revenue'], alpha=0.3)
        ax1.set_title('Monthly Revenue Trend', fontweight='bold')
        ax1.set_ylabel('Revenue')
        ax1.grid(True, alpha=0.3)

        # 2. 收入環比增長
        ax2 = fig.add_subplot(gs[0, 2])
        growth = monthly_kpis['revenue_growth_mom'].iloc[-1]
        color = 'green' if growth >= 0 else 'red'
        ax2.text(0.5, 0.5, f'{growth:.1f}%', ha='center', va='center',
                fontsize=24, fontweight='bold', color=color)
        ax2.set_title('Revenue Growth (MoM)', fontweight='bold')
        ax2.axis('off')

        # 3. AOV 趨勢
        ax3 = fig.add_subplot(gs[1, 0])
        ax3.plot(range(len(monthly_kpis)), monthly_kpis['aov'], marker='s', color='orange')
        ax3.set_title('Average Order Value', fontweight='bold')
        ax3.set_ylabel('AOV')
        ax3.grid(True, alpha=0.3)

        # 4. 訂單趨勢
        ax4 = fig.add_subplot(gs[1, 1])
        ax4.plot(range(len(monthly_kpis)), monthly_kpis['orders'], marker='^', color='green')
        ax4.set_title('Monthly Orders', fontweight='bold')
        ax4.set_ylabel('Orders')
        ax4.grid(True, alpha=0.3)

        # 5. 客戶數趨勢
        ax5 = fig.add_subplot(gs[1, 2])
        ax5.plot(range(len(monthly_kpis)), monthly_kpis['customers'], marker='d', color='purple')
        ax5.set_title('New Customers', fontweight='bold')
        ax5.set_ylabel('Customers')
        ax5.grid(True, alpha=0.3)

        # 6. 分類收入
        ax6 = fig.add_subplot(gs[2, :2])
        top_categories = category_kpis.head(10)
        ax6.barh(top_categories['category'], top_categories['revenue'])
        ax6.set_title('Top 10 Categories by Revenue', fontweight='bold')
        ax6.set_xlabel('Revenue')

        # 7. KPI 摘要
        ax7 = fig.add_subplot(gs[2, 2])
        latest = monthly_kpis.iloc[-1]
        summary_text = f"""
Latest Month KPIs:
Revenue: ${latest['revenue']:,.0f}
Orders: {latest['orders']:,.0f}
AOV: ${latest['aov']:,.2f}
"""
        ax7.text(0.1, 0.5, summary_text, ha='left', va='center',
                fontsize=12, family='monospace',
                bbox=dict(boxstyle='round', facecolor='wheat', alpha=0.5))
        ax7.axis('off')

        fig.suptitle('Sales KPI Dashboard', fontsize=16, fontweight='bold')
        fig.savefig(f'{output_dir}/sales_kpi_dashboard.png', dpi=300, bbox_inches='tight')

        return fig

    def generate_report(self, output_dir='./kpi_outputs'):
        """生成報告"""
        import os
        os.makedirs(output_dir, exist_ok=True)

        print("\n" + "="*60)
        print("開始銷售 KPI 系統")
        print("="*60 + "\n")

        # 計算 KPI
        daily_kpis = self.calculate_daily_kpis()
        monthly_kpis = self.calculate_monthly_kpis()
        category_kpis = self.calculate_category_kpis()
        customer_kpis = self.calculate_customer_kpis()

        # 設置目標
        targets = self.set_kpi_targets()

        # 評估性能
        performance = self.evaluate_performance(monthly_kpis, targets)

        # 可視化
        fig = self.visualize_dashboard(monthly_kpis, category_kpis, output_dir)

        # 保存
        print("\n保存分析結果...")
        daily_kpis.to_csv(f'{output_dir}/daily_kpis.csv', index=False)
        monthly_kpis.to_csv(f'{output_dir}/monthly_kpis.csv', index=False)
        category_kpis.to_csv(f'{output_dir}/category_kpis.csv', index=False)

        print(f"✓ 已保存到 {output_dir}/")

        return monthly_kpis, category_kpis, customer_kpis, performance

    def print_summary(self, monthly_kpis, category_kpis, customer_kpis):
        """打印摘要"""
        print("\n" + "="*80)
        print("銷售 KPI 系統摘要")
        print("="*80)

        latest = monthly_kpis.iloc[-1]
        print(f"\n【本月 KPI】")
        print(f"  訂單總數: {latest['orders']:,.0f}")
        print(f"  新客戶數: {latest['customers']:,.0f}")
        print(f"  銷售額: ${latest['revenue']:,.2f}")
        print(f"  平均訂單價值: ${latest['aov']:,.2f}")

        print(f"\n【環比增長】")
        if len(monthly_kpis) > 1:
            print(f"  收入增長: {latest['revenue_growth_mom']:.2f}%")
            print(f"  訂單增長: {latest['order_growth_mom']:.2f}%")

        print(f"\n【分類表現】")
        for _, row in category_kpis.head(5).iterrows():
            print(f"  {row['category']}: ${row['revenue']:,.2f} ({row['revenue_pct']:.1f}%)")

        print(f"\n【客戶指標】")
        print(f"  總客戶數: {customer_kpis['total_customers']:,.0f}")
        print(f"  回購率: {customer_kpis['repeat_customer_rate']:.2f}%")
        print(f"  平均客戶價值: ${customer_kpis['avg_customer_value']:,.2f}")


# ==================== 使用範例 ====================

if __name__ == "__main__":
    print("加載 Olist 資料...")
    orders, order_items, products, customers, sellers, payments, reviews = load_olist_data()

    # 執行分析
    kpi_system = SalesKPISystem(
        orders=orders,
        order_items=order_items,
        payments=payments
    )

    # 生成報告
    monthly_kpis, category_kpis, customer_kpis, performance = kpi_system.generate_report()

    # 打印摘要
    kpi_system.print_summary(monthly_kpis, category_kpis, customer_kpis)

    print("\n" + "="*80)
    print("✓ 銷售 KPI 系統完成！")
    print("="*80)
