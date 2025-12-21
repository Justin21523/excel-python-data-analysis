"""
客戶 ABC 分析 - Week 13
功能：
1. 按客戶貢獻度進行分類
2. 計算帕累托指數
3. 客戶行為分析
4. 策略建議
5. 風險評估

Author: Business Analytics Week 12-14
Date: 2024-12-11
"""

import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
import sys
from pathlib import Path
import warnings

warnings.filterwarnings('ignore')

sys.path.append(str(Path(__file__).parent.parent.parent / 'week03-06_pandas-advanced' / 'utils'))
from data_loader import load_olist_data


class CustomerABCAnalyzer:
    """客戶 ABC 分析器"""

    def __init__(self, df, customer_col, date_col, amount_col):
        """
        Parameters
        ----------
        df : DataFrame
            交易資料
        customer_col : str
            客戶 ID 欄位名
        date_col : str
            交易日期欄位名
        amount_col : str
            交易金額欄位名
        """
        self.df = df.copy()
        self.customer_col = customer_col
        self.date_col = date_col
        self.amount_col = amount_col

        if not pd.api.types.is_datetime64_any_dtype(self.df[date_col]):
            self.df[date_col] = pd.to_datetime(self.df[date_col])

    def calculate_customer_metrics(self):
        """計算客戶指標"""
        print("計算客戶指標...")

        metrics = self.df.groupby(self.customer_col).agg({
            self.date_col: ['min', 'max', 'count'],
            self.amount_col: ['sum', 'mean', 'std']
        }).reset_index()

        # 扁平化欄位名
        metrics.columns = ['_'.join(col).strip('_') if col[1] else col[0]
                          for col in metrics.columns]

        metrics = metrics.rename(columns={
            f'{self.customer_col}_': self.customer_col,
            f'{self.date_col}_min': 'first_purchase_date',
            f'{self.date_col}_max': 'last_purchase_date',
            f'{self.date_col}_count': 'purchase_count',
            f'{self.amount_col}_sum': 'total_revenue',
            f'{self.amount_col}_mean': 'avg_transaction_value',
            f'{self.amount_col}_std': 'transaction_std'
        })

        # 排序
        metrics = metrics.sort_values('total_revenue', ascending=False).reset_index(drop=True)

        # 累計比例
        metrics['cumulative_revenue'] = metrics['total_revenue'].cumsum()
        metrics['revenue_percentage'] = (metrics['total_revenue'] / metrics['total_revenue'].sum() * 100)
        metrics['cumulative_percentage'] = (metrics['cumulative_revenue'] / metrics['total_revenue'].sum() * 100)

        return metrics

    def classify_abc(self, metrics, a_threshold=80, b_threshold=95):
        """ABC 分類"""
        print("進行 ABC 分類...")

        metrics = metrics.copy()
        metrics['abc_class'] = 'C'
        metrics.loc[metrics['cumulative_percentage'] <= a_threshold, 'abc_class'] = 'A'
        metrics.loc[(metrics['cumulative_percentage'] > a_threshold) &
                   (metrics['cumulative_percentage'] <= b_threshold), 'abc_class'] = 'B'

        return metrics

    def segment_analysis(self, metrics):
        """分段分析"""
        print("進行分段分析...")

        segment_stats = metrics.groupby('abc_class').agg({
            self.customer_col: 'count',
            'total_revenue': ['sum', 'mean', 'std'],
            'purchase_count': ['sum', 'mean'],
            'avg_transaction_value': 'mean'
        }).round(2)

        segment_stats.columns = ['_'.join(col).strip() for col in segment_stats.columns]

        return segment_stats

    def visualize_analysis(self, metrics, output_dir='./abc_outputs'):
        """視覺化分析"""
        import os
        os.makedirs(output_dir, exist_ok=True)

        print("繪製分析圖表...")

        fig, axes = plt.subplots(2, 2, figsize=(16, 12))
        fig.suptitle('Customer ABC Analysis', fontsize=16, fontweight='bold')

        # 1. 帕累托曲線
        ax1 = axes[0, 0]
        x = range(len(metrics))
        ax1.plot(x, metrics['cumulative_percentage'], marker='o', linewidth=2, markersize=1)
        ax1.axhline(y=80, color='r', linestyle='--', alpha=0.5, label='A (80%)')
        ax1.axhline(y=95, color='orange', linestyle='--', alpha=0.5, label='B (95%)')
        ax1.fill_between(x, 0, 80, alpha=0.2, color='green', label='A Class')
        ax1.fill_between(x, 80, 95, alpha=0.2, color='yellow', label='B Class')
        ax1.fill_between(x, 95, 100, alpha=0.2, color='red', label='C Class')
        ax1.set_title('Pareto Curve - Customer Revenue', fontweight='bold')
        ax1.set_xlabel('Customer Rank')
        ax1.set_ylabel('Cumulative Revenue %')
        ax1.legend()
        ax1.grid(True, alpha=0.3)

        # 2. 客戶數分布
        ax2 = axes[0, 1]
        abc_counts = metrics['abc_class'].value_counts().sort_index()
        colors = ['green', 'yellow', 'red']
        ax2.bar(abc_counts.index, abc_counts.values, color=colors)
        ax2.set_title('Customer Count by ABC Class', fontweight='bold')
        ax2.set_ylabel('Number of Customers')

        # 3. 營收分布
        ax3 = axes[1, 0]
        abc_revenue = metrics.groupby('abc_class')['total_revenue'].sum().sort_index()
        ax3.bar(abc_revenue.index, abc_revenue.values, color=colors)
        ax3.set_title('Total Revenue by ABC Class', fontweight='bold')
        ax3.set_ylabel('Total Revenue')

        # 4. 購買頻率 vs 消費額
        ax4 = axes[1, 1]
        scatter = ax4.scatter(
            metrics['purchase_count'],
            metrics['total_revenue'],
            c=['green' if c == 'A' else 'yellow' if c == 'B' else 'red' for c in metrics['abc_class']],
            s=50,
            alpha=0.6
        )
        ax4.set_title('Purchase Frequency vs Total Revenue', fontweight='bold')
        ax4.set_xlabel('Purchase Count')
        ax4.set_ylabel('Total Revenue')
        ax4.set_yscale('log')

        plt.tight_layout()
        fig.savefig(f'{output_dir}/customer_abc_analysis.png', dpi=300, bbox_inches='tight')

        return fig

    def generate_report(self, output_dir='./abc_outputs'):
        """生成報告"""
        import os
        os.makedirs(output_dir, exist_ok=True)

        print("\n" + "="*60)
        print("開始客戶 ABC 分析")
        print("="*60 + "\n")

        # 計算指標
        metrics = self.calculate_customer_metrics()

        # ABC 分類
        metrics = self.classify_abc(metrics)

        # 分段分析
        segment_stats = self.segment_analysis(metrics)

        # 視覺化
        fig = self.visualize_analysis(metrics, output_dir)

        # 保存
        print("\n保存分析結果...")
        metrics.to_csv(f'{output_dir}/customer_abc_classification.csv', index=False)
        segment_stats.to_csv(f'{output_dir}/customer_abc_segment_stats.csv')

        print(f"✓ 已保存到 {output_dir}/")

        return metrics, segment_stats, fig

    def print_summary(self, metrics):
        """打印摘要"""
        print("\n" + "="*80)
        print("客戶 ABC 分析摘要")
        print("="*80)

        for abc_class in ['A', 'B', 'C']:
            class_data = metrics[metrics['abc_class'] == abc_class]
            print(f"\n【{abc_class} 類客戶】")
            print(f"  客戶數: {len(class_data)} ({len(class_data)/len(metrics)*100:.1f}%)")
            print(f"  營收: ${class_data['total_revenue'].sum():,.2f} ({class_data['total_revenue'].sum()/metrics['total_revenue'].sum()*100:.1f}%)")
            print(f"  平均客戶價值: ${class_data['total_revenue'].mean():,.2f}")
            print(f"  平均購買次數: {class_data['purchase_count'].mean():.1f}")

        # 帕累托提示
        a_count = len(metrics[metrics['abc_class'] == 'A'])
        a_revenue = metrics[metrics['abc_class'] == 'A']['total_revenue'].sum()
        total_customers = len(metrics)
        total_revenue = metrics['total_revenue'].sum()
        print(f"\n【帕累托原則】")
        print(f"  {a_count/total_customers*100:.1f}% 的客戶（A 類）貢獻了 {a_revenue/total_revenue*100:.1f}% 的營收")


# ==================== 使用範例 ====================

if __name__ == "__main__":
    print("加載 Olist 資料...")
    orders, order_items, products, customers, sellers, payments, reviews = load_olist_data()

    # 準備交易資料
    print("準備交易資料...")
    transactions = orders.merge(payments, on='order_id', how='left')

    # 執行分析
    analyzer = CustomerABCAnalyzer(
        df=transactions,
        customer_col='customer_id',
        date_col='order_purchase_timestamp',
        amount_col='payment_value'
    )

    # 生成報告
    metrics, segment_stats, fig = analyzer.generate_report()

    # 打印摘要
    analyzer.print_summary(metrics)

    print("\n" + "="*80)
    print("✓ 客戶 ABC 分析完成！")
    print("="*80)
