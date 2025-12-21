"""
簡單 CLV 計算 - Week 13
功能：
1. 計算客戶生命週期價值（CLV）
2. 三種計算方法：Historical、Predictive、Simplified
3. 客戶價值分層
4. 利潤分析
5. 行動建議

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

# 設定路徑
sys.path.append(str(Path(__file__).parent.parent.parent / 'week03-06_pandas-advanced' / 'utils'))
from data_loader import load_olist_data


class SimpleCLVCalculator:
    """
    簡單客戶生命週期價值計算器
    """

    def __init__(self, df, customer_col, date_col, amount_col, analysis_date=None):
        """
        初始化計算器

        Parameters
        ----------
        df : DataFrame
            交易資料表
        customer_col : str
            客戶 ID 欄位名
        date_col : str
            交易日期欄位名
        amount_col : str
            交易金額欄位名
        analysis_date : datetime, optional
            分析基準日期
        """
        self.df = df.copy()
        self.customer_col = customer_col
        self.date_col = date_col
        self.amount_col = amount_col

        if not pd.api.types.is_datetime64_any_dtype(self.df[date_col]):
            self.df[date_col] = pd.to_datetime(self.df[date_col])

        self.analysis_date = analysis_date or self.df[date_col].max()
        self.clv_data = None

    def calculate_customer_metrics(self):
        """
        計算基礎客戶指標

        Returns
        -------
        DataFrame
            包含客戶指標的 DataFrame
        """
        print("計算客戶指標...")

        customer_metrics = self.df.groupby(self.customer_col).agg({
            self.date_col: ['min', 'max', 'count'],
            self.amount_col: ['sum', 'mean', 'std', 'min', 'max']
        }).reset_index()

        # 扁平化欄位名
        customer_metrics.columns = ['_'.join(col).strip('_') if col[1] else col[0]
                                   for col in customer_metrics.columns]

        customer_metrics = customer_metrics.rename(columns={
            f'{self.customer_col}_': self.customer_col,
            f'{self.date_col}_min': 'first_purchase_date',
            f'{self.date_col}_max': 'last_purchase_date',
            f'{self.date_col}_count': 'purchase_count',
            f'{self.amount_col}_sum': 'total_revenue',
            f'{self.amount_col}_mean': 'avg_purchase_value',
            f'{self.amount_col}_std': 'purchase_std',
            f'{self.amount_col}_min': 'min_purchase_value',
            f'{self.amount_col}_max': 'max_purchase_value'
        })

        # 計算衍生指標
        customer_metrics['customer_lifespan_days'] = (
            customer_metrics['last_purchase_date'] - customer_metrics['first_purchase_date']
        ).dt.days + 1

        customer_metrics['days_since_last_purchase'] = (
            self.analysis_date - customer_metrics['last_purchase_date']
        ).dt.days

        customer_metrics['customer_lifespan_years'] = customer_metrics['customer_lifespan_days'] / 365.25

        return customer_metrics

    def calculate_historical_clv(self, customer_metrics):
        """
        計算歷史 CLV

        CLV = 客戶迄今為止的總購買金額

        Parameters
        ----------
        customer_metrics : DataFrame
            客戶指標資料

        Returns
        -------
        Series
            歷史 CLV
        """
        print("計算歷史 CLV...")

        # 最簡單的方法：客戶的總營收
        historical_clv = customer_metrics['total_revenue']

        return historical_clv

    def calculate_predictive_clv(self, customer_metrics, future_years=3):
        """
        計算預測 CLV

        基於歷史購買行為預測未來營收
        Predictive CLV = 歷史 CLV + (年平均支出 * 預測年數)

        Parameters
        ----------
        customer_metrics : DataFrame
            客戶指標資料
        future_years : int
            預測的未來年份數

        Returns
        -------
        DataFrame
            包含預測 CLV 的 DataFrame
        """
        print(f"計算預測 CLV（未來 {future_years} 年）...")

        clv = customer_metrics.copy()

        # 計算年平均支出
        clv['annual_spend'] = clv['total_revenue'] / (clv['customer_lifespan_years'] + 1)

        # 預測未來收益
        clv['future_revenue'] = clv['annual_spend'] * future_years

        # 預測 CLV = 歷史 + 預測未來
        clv['predictive_clv'] = clv['total_revenue'] + clv['future_revenue']

        # 調整停流失客戶的預測（最後購買超過 90 天的客戶）
        clv.loc[clv['days_since_last_purchase'] > 90, 'predictive_clv'] = (
            clv.loc[clv['days_since_last_purchase'] > 90, 'predictive_clv'] * 0.5
        )

        return clv

    def calculate_simplified_clv(self, customer_metrics):
        """
        計算簡化 CLV

        使用平均客戶壽命和平均訂單價值估計
        Simplified CLV = 平均訂單價值 * 購買頻率 * 平均客戶壽命

        Parameters
        ----------
        customer_metrics : DataFrame
            客戶指標資料

        Returns
        -------
        Series
            簡化 CLV
        """
        print("計算簡化 CLV...")

        clv = customer_metrics.copy()

        # 購買頻率（次/年）
        clv['purchase_frequency'] = clv['purchase_count'] / (clv['customer_lifespan_years'] + 1)

        # 平均客戶壽命（年）
        # 假設新客戶的平均壽命為 5 年
        clv['avg_customer_lifetime'] = 5

        # 簡化 CLV = AOV * 頻率 * 壽命
        clv['simplified_clv'] = (
            clv['avg_purchase_value'] *
            clv['purchase_frequency'] *
            clv['avg_customer_lifetime']
        )

        return clv

    def segment_by_clv(self, clv_data):
        """
        按 CLV 進行客戶分層

        Parameters
        ----------
        clv_data : DataFrame
            包含 CLV 的客戶資料

        Returns
        -------
        DataFrame
            CLV 分層統計
        """
        print("按 CLV 進行客戶分層...")

        # 基於預測 CLV 的四分位數分層
        clv_quartiles = pd.qcut(clv_data['predictive_clv'], q=4,
                                labels=['Low', 'Medium', 'High', 'VIP'])

        clv_data['clv_segment'] = clv_quartiles

        # 統計分層資訊
        segment_stats = clv_data.groupby('clv_segment', observed=True).agg({
            self.customer_col: 'count',
            'predictive_clv': ['mean', 'min', 'max', 'sum'],
            'total_revenue': ['mean', 'sum'],
            'purchase_count': 'mean',
            'purchase_frequency': 'mean'
        }).round(2)

        segment_stats.columns = ['_'.join(col).strip() for col in segment_stats.columns]
        segment_stats = segment_stats.rename(columns={
            f'{self.customer_col}_count': 'customer_count'
        })

        # 計算百分比
        segment_stats['percentage'] = (
            segment_stats['customer_count'] / segment_stats['customer_count'].sum() * 100
        ).round(2)

        segment_stats['revenue_percentage'] = (
            segment_stats['predictive_clv_sum'] / segment_stats['predictive_clv_sum'].sum() * 100
        ).round(2)

        return clv_data, segment_stats

    def calculate_roi_metrics(self, clv_data, avg_cac=50):
        """
        計算 ROI 相關指標

        Parameters
        ----------
        clv_data : DataFrame
            CLV 資料
        avg_cac : float
            平均客戶獲取成本

        Returns
        -------
        DataFrame
            ROI 指標
        """
        print(f"計算 ROI 指標（假設平均 CAC: ${avg_cac}）...")

        roi_metrics = clv_data.copy()

        # CLV:CAC 比率
        roi_metrics['clv_cac_ratio'] = roi_metrics['predictive_clv'] / avg_cac

        # ROI（%）
        roi_metrics['roi_percentage'] = (
            (roi_metrics['predictive_clv'] - avg_cac) / avg_cac * 100
        )

        # 回本週期（月）
        roi_metrics['payback_period_months'] = (
            avg_cac / (roi_metrics['avg_purchase_value'] * roi_metrics['purchase_frequency'] / 12)
        ).replace([np.inf, -np.inf], np.nan)

        return roi_metrics

    def visualize_clv_analysis(self, clv_data, output_dir='./clv_outputs'):
        """
        視覺化 CLV 分析

        Parameters
        ----------
        clv_data : DataFrame
            CLV 資料
        output_dir : str
            輸出目錄路徑

        Returns
        -------
        Figure
            Matplotlib figure 物件
        """
        import os
        os.makedirs(output_dir, exist_ok=True)

        print("繪製 CLV 分析圖表...")

        fig, axes = plt.subplots(2, 2, figsize=(16, 12))
        fig.suptitle('Customer Lifetime Value Analysis', fontsize=16, fontweight='bold')

        # 1. CLV 分布
        axes[0, 0].hist(clv_data['predictive_clv'], bins=50, color='steelblue', edgecolor='black')
        axes[0, 0].axvline(clv_data['predictive_clv'].mean(), color='red', linestyle='--',
                          linewidth=2, label=f"Mean: ${clv_data['predictive_clv'].mean():.2f}")
        axes[0, 0].set_title('Distribution of CLV', fontweight='bold')
        axes[0, 0].set_xlabel('CLV ($)')
        axes[0, 0].set_ylabel('Number of Customers')
        axes[0, 0].legend()

        # 2. CLV 分層客戶數
        segment_counts = clv_data['clv_segment'].value_counts().sort_index()
        colors = ['#d62728', '#ff7f0e', '#2ca02c', '#1f77b4']
        axes[0, 1].bar(segment_counts.index, segment_counts.values, color=colors)
        axes[0, 1].set_title('Customer Count by CLV Segment', fontweight='bold')
        axes[0, 1].set_ylabel('Number of Customers')

        # 3. CLV 分層營收貢獻
        segment_revenue = clv_data.groupby('clv_segment')['predictive_clv'].sum().sort_index()
        axes[1, 0].bar(segment_revenue.index, segment_revenue.values, color=colors)
        axes[1, 0].set_title('Revenue Contribution by CLV Segment', fontweight='bold')
        axes[1, 0].set_ylabel('Total CLV ($)')

        # 4. 購買頻率 vs CLV
        scatter = axes[1, 1].scatter(
            clv_data['purchase_frequency'],
            clv_data['predictive_clv'],
            c=clv_data['avg_purchase_value'],
            s=100,
            alpha=0.6,
            cmap='viridis'
        )
        axes[1, 1].set_title('Purchase Frequency vs CLV', fontweight='bold')
        axes[1, 1].set_xlabel('Purchase Frequency (times/year)')
        axes[1, 1].set_ylabel('Predicted CLV ($)')
        plt.colorbar(scatter, ax=axes[1, 1], label='Avg Purchase Value')

        plt.tight_layout()
        fig.savefig(f'{output_dir}/clv_analysis.png', dpi=300, bbox_inches='tight')

        return fig

    def generate_report(self, output_dir='./clv_outputs', avg_cac=50):
        """
        生成完整報告

        Parameters
        ----------
        output_dir : str
            輸出目錄路徑
        avg_cac : float
            平均客戶獲取成本

        Returns
        -------
        tuple
            (clv_data, segment_stats, figure)
        """
        import os
        os.makedirs(output_dir, exist_ok=True)

        print("\n" + "="*60)
        print("開始簡單 CLV 計算")
        print("="*60 + "\n")

        # 計算基礎指標
        customer_metrics = self.calculate_customer_metrics()

        # 計算各種 CLV
        clv_data = self.calculate_predictive_clv(customer_metrics)
        clv_data['historical_clv'] = self.calculate_historical_clv(customer_metrics)
        temp = self.calculate_simplified_clv(customer_metrics)
        clv_data['simplified_clv'] = temp['simplified_clv']

        # 計算 ROI 指標
        clv_data = self.calculate_roi_metrics(clv_data, avg_cac)

        # 分層分析
        clv_data, segment_stats = self.segment_by_clv(clv_data)

        # 視覺化
        fig = self.visualize_clv_analysis(clv_data, output_dir)

        # 保存結果
        print("\n保存分析結果...")
        self.clv_data = clv_data

        # 保存完整資料
        output_cols = [
            self.customer_col, 'purchase_count', 'total_revenue',
            'avg_purchase_value', 'purchase_frequency',
            'historical_clv', 'simplified_clv', 'predictive_clv',
            'clv_segment', 'clv_cac_ratio', 'roi_percentage',
            'payback_period_months'
        ]

        clv_data[output_cols].to_csv(f'{output_dir}/customer_clv_analysis.csv', index=False)
        segment_stats.to_csv(f'{output_dir}/clv_segment_statistics.csv')

        print(f"✓ 已保存到 {output_dir}/")

        return clv_data, segment_stats, fig

    def print_analysis_summary(self, clv_data):
        """打印分析摘要"""
        print("\n" + "="*100)
        print("簡單 CLV 分析摘要")
        print("="*100)

        print(f"\n總客戶數: {len(clv_data):,}")

        print("\n【整體 CLV 統計】")
        print(f"  平均 CLV: ${clv_data['predictive_clv'].mean():,.2f}")
        print(f"  中位數 CLV: ${clv_data['predictive_clv'].median():,.2f}")
        print(f"  總 CLV: ${clv_data['predictive_clv'].sum():,.2f}")
        print(f"  最高 CLV: ${clv_data['predictive_clv'].max():,.2f}")

        print("\n【客戶分層】")
        segment_dist = clv_data['clv_segment'].value_counts().sort_index()
        for segment, count in segment_dist.items():
            pct = count / len(clv_data) * 100
            seg_revenue = clv_data[clv_data['clv_segment'] == segment]['predictive_clv'].sum()
            print(f"  {segment:10s}: {count:6,} 人 ({pct:5.2f}%) - 營收: ${seg_revenue:12,.2f}")

        print("\n【ROI 指標】")
        print(f"  平均 CLV:CAC 比率: {clv_data['clv_cac_ratio'].mean():.2f}x")
        print(f"  平均 ROI: {clv_data['roi_percentage'].mean():.2f}%")
        print(f"  平均回本週期: {clv_data['payback_period_months'].mean():.1f} 月")

        print("\n【關鍵洞察】")
        vip_count = len(clv_data[clv_data['clv_segment'] == 'VIP'])
        vip_revenue = clv_data[clv_data['clv_segment'] == 'VIP']['predictive_clv'].sum()
        total_revenue = clv_data['predictive_clv'].sum()
        print(f"  VIP 客戶（最高四分位）: {vip_count:,} 人")
        print(f"  VIP 營收佔比: {vip_revenue / total_revenue * 100:.1f}%")


# ==================== 使用範例 ====================

if __name__ == "__main__":
    print("加載 Olist 資料...")
    orders, order_items, products, customers, sellers, payments, reviews = load_olist_data()

    # 準備交易資料
    print("準備交易資料...")
    transactions = orders.merge(payments, on='order_id', how='left')

    # 執行計算
    calculator = SimpleCLVCalculator(
        df=transactions,
        customer_col='customer_id',
        date_col='order_purchase_timestamp',
        amount_col='payment_value'
    )

    # 生成報告
    clv_data, segment_stats, fig = calculator.generate_report(avg_cac=50)

    # 打印摘要
    calculator.print_analysis_summary(clv_data)

    # 打印分層統計
    print("\n" + "="*100)
    print("CLV 分層統計詳細表")
    print("="*100)
    print(segment_stats.to_string())

    print("\n" + "="*100)
    print("✓ 簡單 CLV 計算完成！")
    print("="*100)
