"""
客戶 KPI 系統 - Week 14
功能：
1. 客戶獲取成本（CAC）
2. 客戶生命週期價值（LTV）
3. 客戶流失率
4. 客戶滿意度
5. 客戶健康評分

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


class CustomerKPISystem:
    """客戶 KPI 系統"""

    def __init__(self, orders, order_items, payments, reviews, customers):
        """初始化"""
        self.orders = orders
        self.order_items = order_items
        self.payments = payments
        self.reviews = reviews
        self.customers = customers

    def calculate_cac(self, total_marketing_spend=100000):
        """計算客戶獲取成本"""
        print("計算客戶獲取成本（CAC）...")

        new_customers_month = (
            self.orders.groupby(self.orders['order_purchase_timestamp'].dt.to_period('M'))
            ['customer_id'].nunique()
        )

        cac = total_marketing_spend / new_customers_month.sum()

        return cac, new_customers_month

    def calculate_ltv(self):
        """計算客戶生命週期價值"""
        print("計算客戶生命週期價值（LTV）...")

        merged = self.orders.merge(self.payments, on='order_id', how='left')

        ltv_data = merged.groupby('customer_id')['payment_value'].sum()

        return {
            'avg_ltv': ltv_data.mean(),
            'median_ltv': ltv_data.median(),
            'total_ltv': ltv_data.sum()
        }

    def calculate_churn_rate(self, observation_period_days=365, prediction_days=30):
        """計算流失率"""
        print("計算客戶流失率...")

        analysis_date = self.orders['order_purchase_timestamp'].max()

        customer_activity = self.orders.groupby('customer_id')['order_purchase_timestamp'].max()

        # 最後購買超過 30 天的客戶視為流失
        churned = (analysis_date - customer_activity).dt.days > prediction_days
        churn_rate = churned.sum() / len(churned) * 100

        return churn_rate, churned

    def calculate_customer_satisfaction(self):
        """計算客戶滿意度"""
        print("計算客戶滿意度...")

        if self.reviews is None or 'review_score' not in self.reviews.columns:
            return None

        avg_rating = self.reviews['review_score'].mean()
        rating_distribution = self.reviews['review_score'].value_counts().sort_index()

        return {
            'avg_rating': avg_rating,
            'rating_distribution': rating_distribution,
            'satisfied_rate': (self.reviews['review_score'] >= 4).sum() / len(self.reviews) * 100
        }

    def calculate_retention_rate(self):
        """計算保留率"""
        print("計算保留率...")

        customer_purchase_count = self.orders.groupby('customer_id').size()

        one_time = (customer_purchase_count == 1).sum()
        repeat = (customer_purchase_count > 1).sum()
        total = len(customer_purchase_count)

        retention_rate = repeat / total * 100

        return retention_rate

    def calculate_customer_health_score(self):
        """計算客戶健康評分"""
        print("計算客戶健康評分...")

        merged = self.orders.merge(self.payments, on='order_id', how='left')

        # 購買頻率
        purchase_freq = merged.groupby('customer_id').size()

        # 最近購買
        last_purchase = merged.groupby('customer_id')['order_purchase_timestamp'].max()
        analysis_date = merged['order_purchase_timestamp'].max()
        days_since_purchase = (analysis_date - last_purchase).dt.days

        # 消費金額
        customer_value = merged.groupby('customer_id')['payment_value'].sum()

        # 標準化和計算健康評分
        freq_score = (purchase_freq / purchase_freq.max() * 30)
        recency_score = (1 - (days_since_purchase / days_since_purchase.max())) * 30
        value_score = (customer_value / customer_value.max() * 40)

        health_score = freq_score + recency_score + value_score

        health_df = pd.DataFrame({
            'customer_id': health_score.index,
            'health_score': health_score.values,
            'purchase_frequency': purchase_freq.values,
            'days_since_purchase': days_since_purchase.values,
            'lifetime_value': customer_value.values
        })

        # 分級
        health_df['health_level'] = pd.cut(health_df['health_score'], bins=[0, 25, 50, 75, 100],
                                           labels=['Low', 'Medium', 'High', 'Excellent'])

        return health_df

    def visualize_dashboard(self, output_dir='./customer_kpi_outputs'):
        """可視化儀表板"""
        import os
        os.makedirs(output_dir, exist_ok=True)

        print("繪製客戶 KPI 儀表板...")

        fig, axes = plt.subplots(2, 3, figsize=(18, 10))
        fig.suptitle('Customer KPI Dashboard', fontsize=16, fontweight='bold')

        # 1. CAC 趨勢
        cac, new_cus_month = self.calculate_cac()
        ax1 = axes[0, 0]
        ax1.plot(range(len(new_cus_month)), new_cus_month.values, marker='o')
        ax1.set_title('New Customers per Month', fontweight='bold')
        ax1.set_ylabel('Count')

        # 2. LTV 分布
        ltv_stats = self.calculate_ltv()
        ax2 = axes[0, 1]
        ax2.text(0.5, 0.7, f"${ltv_stats['avg_ltv']:.2f}", ha='center', va='center',
                fontsize=20, fontweight='bold')
        ax2.text(0.5, 0.3, "Average LTV", ha='center', va='center', fontsize=12)
        ax2.axis('off')

        # 3. 流失率
        churn_rate, _ = self.calculate_churn_rate()
        ax3 = axes[0, 2]
        ax3.text(0.5, 0.7, f"{churn_rate:.1f}%", ha='center', va='center',
                fontsize=20, fontweight='bold', color='red')
        ax3.text(0.5, 0.3, "Churn Rate", ha='center', va='center', fontsize=12)
        ax3.axis('off')

        # 4. 滿意度
        satisfaction = self.calculate_customer_satisfaction()
        if satisfaction:
            ax4 = axes[1, 0]
            ax4.bar(satisfaction['rating_distribution'].index,
                   satisfaction['rating_distribution'].values)
            ax4.set_title('Rating Distribution', fontweight='bold')
            ax4.set_xlabel('Rating')
            ax4.set_ylabel('Count')

        # 5. 保留率
        retention_rate = self.calculate_retention_rate()
        ax5 = axes[1, 1]
        ax5.text(0.5, 0.7, f"{retention_rate:.1f}%", ha='center', va='center',
                fontsize=20, fontweight='bold', color='green')
        ax5.text(0.5, 0.3, "Retention Rate", ha='center', va='center', fontsize=12)
        ax5.axis('off')

        # 6. 健康評分分布
        health_df = self.calculate_customer_health_score()
        ax6 = axes[1, 2]
        health_dist = health_df['health_level'].value_counts()
        colors = ['red', 'orange', 'lightgreen', 'green']
        ax6.pie(health_dist.values, labels=health_dist.index, autopct='%1.1f%%',
               colors=colors[:len(health_dist)])
        ax6.set_title('Customer Health Score Distribution', fontweight='bold')

        plt.tight_layout()
        fig.savefig(f'{output_dir}/customer_kpi_dashboard.png', dpi=300, bbox_inches='tight')

        return fig

    def generate_report(self, output_dir='./customer_kpi_outputs'):
        """生成報告"""
        import os
        os.makedirs(output_dir, exist_ok=True)

        print("\n" + "="*60)
        print("開始客戶 KPI 系統")
        print("="*60 + "\n")

        # 計算各項指標
        cac, new_cus_month = self.calculate_cac()
        ltv_stats = self.calculate_ltv()
        churn_rate, _ = self.calculate_churn_rate()
        retention_rate = self.calculate_retention_rate()
        satisfaction = self.calculate_customer_satisfaction()
        health_df = self.calculate_customer_health_score()

        # 可視化
        fig = self.visualize_dashboard(output_dir)

        # 保存
        print("\n保存分析結果...")
        health_df.to_csv(f'{output_dir}/customer_health_scores.csv', index=False)

        print(f"✓ 已保存到 {output_dir}/")

        return {
            'cac': cac,
            'ltv_stats': ltv_stats,
            'churn_rate': churn_rate,
            'retention_rate': retention_rate,
            'satisfaction': satisfaction,
            'health_df': health_df
        }

    def print_summary(self, kpi_dict):
        """打印摘要"""
        print("\n" + "="*80)
        print("客戶 KPI 系統摘要")
        print("="*80)

        print(f"\n【主要指標】")
        print(f"  客戶獲取成本（CAC）: ${kpi_dict['cac']:.2f}")
        print(f"  平均客戶生命週期價值（LTV）: ${kpi_dict['ltv_stats']['avg_ltv']:.2f}")
        print(f"  LTV:CAC 比率: {kpi_dict['ltv_stats']['avg_ltv'] / kpi_dict['cac']:.2f}x")
        print(f"  客戶流失率: {kpi_dict['churn_rate']:.2f}%")
        print(f"  客戶保留率: {kpi_dict['retention_rate']:.2f}%")

        if kpi_dict['satisfaction']:
            print(f"\n【滿意度指標】")
            print(f"  平均評分: {kpi_dict['satisfaction']['avg_rating']:.2f}/5")
            print(f"  滿意客戶比率: {kpi_dict['satisfaction']['satisfied_rate']:.2f}%")

        print(f"\n【客戶健康評分】")
        health_dist = kpi_dict['health_df']['health_level'].value_counts()
        for level, count in health_dist.items():
            pct = count / len(kpi_dict['health_df']) * 100
            print(f"  {level}: {count} ({pct:.1f}%)")


# ==================== 使用範例 ====================

if __name__ == "__main__":
    print("加載 Olist 資料...")
    orders, order_items, products, customers, sellers, payments, reviews = load_olist_data()

    # 執行分析
    kpi_system = CustomerKPISystem(
        orders=orders,
        order_items=order_items,
        payments=payments,
        reviews=reviews,
        customers=customers
    )

    # 生成報告
    kpi_dict = kpi_system.generate_report()

    # 打印摘要
    kpi_system.print_summary(kpi_dict)

    print("\n" + "="*80)
    print("✓ 客戶 KPI 系統完成！")
    print("="*80)
