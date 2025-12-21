"""
庫存 ABC 分析 - Week 13
功能：
1. 按銷售額對商品進行 ABC 分類
2. 計算帕累托指數
3. 分析庫存特徵
4. 提供管理建議
5. 視覺化分析結果

Author: Business Analytics Week 12-14
Date: 2024-12-11
"""

import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
from datetime import datetime
import sys
from pathlib import Path
import warnings

warnings.filterwarnings('ignore')

sys.path.append(str(Path(__file__).parent.parent.parent / 'week03-06_pandas-advanced' / 'utils'))
from data_loader import load_olist_data


class InventoryABCAnalyzer:
    """庫存 ABC 分析器"""

    def __init__(self, df, product_col, amount_col, quantity_col=None):
        """
        Parameters
        ----------
        df : DataFrame
            銷售資料
        product_col : str
            商品 ID 欄位名
        amount_col : str
            銷售金額欄位名
        quantity_col : str, optional
            銷售數量欄位名
        """
        self.df = df.copy()
        self.product_col = product_col
        self.amount_col = amount_col
        self.quantity_col = quantity_col

    def calculate_product_metrics(self):
        """計算商品銷售指標"""
        print("計算商品銷售指標...")

        metrics = self.df.groupby(self.product_col).agg({
            self.amount_col: ['sum', 'count', 'mean'],
        }).reset_index()

        if self.quantity_col:
            qty = self.df.groupby(self.product_col)[self.quantity_col].sum()
            metrics = metrics.merge(qty.to_frame('total_quantity'),
                                   left_on=self.product_col,
                                   right_index=True, how='left')

        # 扁平化欄位名
        metrics.columns = ['_'.join(col).strip('_') if col[1] else col[0]
                          for col in metrics.columns]

        metrics = metrics.rename(columns={
            f'{self.amount_col}_sum': 'total_sales',
            f'{self.amount_col}_count': 'transaction_count',
            f'{self.amount_col}_mean': 'avg_transaction_value'
        })

        # 排序
        metrics = metrics.sort_values('total_sales', ascending=False).reset_index(drop=True)

        # 計算累計比例
        metrics['cumulative_sales'] = metrics['total_sales'].cumsum()
        metrics['sales_percentage'] = (metrics['total_sales'] / metrics['total_sales'].sum() * 100)
        metrics['cumulative_percentage'] = metrics['cumulative_sales'] / metrics['total_sales'].sum() * 100

        return metrics

    def classify_abc(self, metrics, a_threshold=80, b_threshold=95):
        """按帕累托原則分類"""
        print("按 ABC 分類...")

        metrics = metrics.copy()
        metrics['abc_class'] = 'C'
        metrics.loc[metrics['cumulative_percentage'] <= a_threshold, 'abc_class'] = 'A'
        metrics.loc[(metrics['cumulative_percentage'] > a_threshold) &
                   (metrics['cumulative_percentage'] <= b_threshold), 'abc_class'] = 'B'

        return metrics

    def segment_analysis(self, metrics):
        """分段分析"""
        print("分段分析...")

        segment_stats = metrics.groupby('abc_class').agg({
            self.product_col: 'count',
            'total_sales': ['sum', 'mean'],
            'transaction_count': 'mean',
            'cumulative_percentage': ['min', 'max']
        }).round(2)

        segment_stats.columns = ['_'.join(col).strip() for col in segment_stats.columns]

        return segment_stats

    def visualize_analysis(self, metrics, output_dir='./abc_outputs'):
        """視覺化分析"""
        import os
        os.makedirs(output_dir, exist_ok=True)

        print("繪製 ABC 分析圖表...")

        fig, axes = plt.subplots(2, 2, figsize=(16, 12))
        fig.suptitle('Inventory ABC Analysis', fontsize=16, fontweight='bold')

        # 1. 帕累托曲線
        ax1 = axes[0, 0]
        x = range(len(metrics))
        ax1.plot(x, metrics['cumulative_percentage'], marker='o', linewidth=2, markersize=1)
        ax1.axhline(y=80, color='r', linestyle='--', alpha=0.5, label='A (80%)')
        ax1.axhline(y=95, color='orange', linestyle='--', alpha=0.5, label='B (95%)')
        ax1.fill_between(x, 0, 80, alpha=0.2, color='green', label='A Class')
        ax1.fill_between(x, 80, 95, alpha=0.2, color='yellow', label='B Class')
        ax1.fill_between(x, 95, 100, alpha=0.2, color='red', label='C Class')
        ax1.set_title('Pareto Curve', fontweight='bold')
        ax1.set_xlabel('Product Count')
        ax1.set_ylabel('Cumulative Sales %')
        ax1.legend()
        ax1.grid(True, alpha=0.3)

        # 2. ABC 分類商品數
        ax2 = axes[0, 1]
        abc_counts = metrics['abc_class'].value_counts().sort_index()
        colors = ['green', 'yellow', 'red']
        ax2.bar(abc_counts.index, abc_counts.values, color=colors)
        ax2.set_title('Product Count by ABC Class', fontweight='bold')
        ax2.set_ylabel('Number of Products')

        # 3. ABC 分類銷售額
        ax3 = axes[1, 0]
        abc_sales = metrics.groupby('abc_class')['total_sales'].sum().sort_index()
        ax3.bar(abc_sales.index, abc_sales.values, color=colors)
        ax3.set_title('Total Sales by ABC Class', fontweight='bold')
        ax3.set_ylabel('Total Sales')

        # 4. 銷售額分布（前 50 個商品）
        ax4 = axes[1, 1]
        top_products = metrics.head(50)
        ax4.barh(range(len(top_products)), top_products['total_sales'],
                color=[colors[['A', 'B', 'C'].index(c)] for c in top_products['abc_class']])
        ax4.set_yticks([])
        ax4.set_title('Top 50 Products by Sales', fontweight='bold')
        ax4.set_xlabel('Total Sales')

        plt.tight_layout()
        fig.savefig(f'{output_dir}/abc_analysis.png', dpi=300, bbox_inches='tight')

        return fig

    def generate_report(self, output_dir='./abc_outputs'):
        """生成報告"""
        import os
        os.makedirs(output_dir, exist_ok=True)

        print("\n" + "="*60)
        print("開始庫存 ABC 分析")
        print("="*60 + "\n")

        # 計算指標
        metrics = self.calculate_product_metrics()

        # ABC 分類
        metrics = self.classify_abc(metrics)

        # 分段分析
        segment_stats = self.segment_analysis(metrics)

        # 視覺化
        fig = self.visualize_analysis(metrics, output_dir)

        # 保存
        print("\n保存分析結果...")
        metrics.to_csv(f'{output_dir}/product_abc_classification.csv', index=False)
        segment_stats.to_csv(f'{output_dir}/abc_segment_stats.csv')

        print(f"✓ 已保存到 {output_dir}/")

        return metrics, segment_stats, fig

    def print_summary(self, metrics):
        """打印摘要"""
        print("\n" + "="*80)
        print("庫存 ABC 分析摘要")
        print("="*80)

        for abc_class in ['A', 'B', 'C']:
            class_data = metrics[metrics['abc_class'] == abc_class]
            print(f"\n【{abc_class} 類商品】")
            print(f"  商品數: {len(class_data)} ({len(class_data)/len(metrics)*100:.1f}%)")
            print(f"  銷售額: ${class_data['total_sales'].sum():,.2f} ({class_data['total_sales'].sum()/metrics['total_sales'].sum()*100:.1f}%)")
            print(f"  平均銷售額: ${class_data['total_sales'].mean():,.2f}")


# ==================== 使用範例 ====================

if __name__ == "__main__":
    print("加載 Olist 資料...")
    orders, order_items, products, customers, sellers, payments, reviews = load_olist_data()

    # 執行分析
    analyzer = InventoryABCAnalyzer(
        df=order_items,
        product_col='product_id',
        amount_col='price',
        quantity_col='order_item_id'
    )

    # 生成報告
    metrics, segment_stats, fig = analyzer.generate_report()

    # 打印摘要
    analyzer.print_summary(metrics)

    print("\n" + "="*80)
    print("✓ 庫存 ABC 分析完成！")
    print("="*80)
