"""
客戶流失預警系統 - Week 12
功能：
1. 定義流失指標
2. 識別流失風險客戶
3. 計算流失概率評分
4. 生成流失預警報告
5. 製定挽留策略

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

# 設定路徑
sys.path.append(str(Path(__file__).parent.parent.parent / 'week03-06_pandas-advanced' / 'utils'))
from data_loader import load_olist_data


class ChurnPredictionAnalyzer:
    """
    客戶流失預警分析器
    識別可能流失的客戶並評估流失風險
    """

    def __init__(self, df, customer_col, date_col, amount_col, analysis_date=None):
        """
        初始化分析器

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
        self.churn_data = None

    def calculate_customer_metrics(self):
        """
        計算客戶指標

        Returns
        -------
        DataFrame
            包含客戶指標的 DataFrame
        """
        print("計算客戶指標...")

        # 按客戶分組統計
        customer_stats = self.df.groupby(self.customer_col).agg({
            self.date_col: [
                'min',  # 首次購買日期
                'max',  # 最後購買日期
                'count'  # 購買次數
            ],
            self.amount_col: [
                'sum',  # 累計消費
                'mean',  # 平均消費
                'std'  # 消費標準差
            ]
        }).reset_index()

        # 扁平化多層級欄位名
        customer_stats.columns = ['_'.join(col).strip('_')
                                  if col[1] else col[0]
                                  for col in customer_stats.columns]

        # 重新命名
        customer_stats = customer_stats.rename(columns={
            f'{self.customer_col}_': self.customer_col,
            f'{self.date_col}_min': 'first_purchase_date',
            f'{self.date_col}_max': 'last_purchase_date',
            f'{self.date_col}_count': 'purchase_count',
            f'{self.amount_col}_sum': 'total_spent',
            f'{self.amount_col}_mean': 'avg_purchase_value',
            f'{self.amount_col}_std': 'purchase_std'
        })

        customer_stats[self.customer_col] = customer_stats[self.customer_col]

        # 計算衍生指標
        customer_stats['days_since_first_purchase'] = (
            self.analysis_date - customer_stats['first_purchase_date']
        ).dt.days

        customer_stats['days_since_last_purchase'] = (
            self.analysis_date - customer_stats['last_purchase_date']
        ).dt.days

        customer_stats['average_days_between_purchases'] = (
            customer_stats['days_since_first_purchase'] /
            (customer_stats['purchase_count'] - 1)
        ).fillna(customer_stats['days_since_first_purchase'])

        customer_stats['purchase_frequency'] = (
            customer_stats['purchase_count'] /
            (customer_stats['days_since_first_purchase'] + 1) * 365
        ).fillna(0)

        return customer_stats

    def identify_at_risk_customers(self, customer_stats, recency_threshold=90):
        """
        識別高流失風險的客戶

        Parameters
        ----------
        customer_stats : DataFrame
            客戶統計資料
        recency_threshold : int
            最近性閾值（天），超過此值視為流失風險

        Returns
        -------
        DataFrame
            標記為流失風險的客戶
        """
        print(f"識別流失風險客戶（Recency 閾值: {recency_threshold} 天）...")

        # 複製資料
        at_risk = customer_stats.copy()

        # 定義流失指標
        # 基於 Recency（最後購買距今天數）
        at_risk['is_at_risk'] = at_risk['days_since_last_purchase'] > recency_threshold

        # 流失風險等級
        at_risk['churn_risk_level'] = 'Low'
        at_risk.loc[at_risk['days_since_last_purchase'] > recency_threshold, 'churn_risk_level'] = 'Medium'
        at_risk.loc[at_risk['days_since_last_purchase'] > recency_threshold * 1.5, 'churn_risk_level'] = 'High'
        at_risk.loc[at_risk['days_since_last_purchase'] > recency_threshold * 2, 'churn_risk_level'] = 'Critical'

        return at_risk

    def calculate_churn_risk_score(self, at_risk_customers):
        """
        計算流失風險評分（0-100）

        評分考慮：
        - Recency（最近性）：權重 50%，最後購買距今越遠，分數越低
        - Frequency（頻率）：權重 30%，購買頻率越低，分數越低
        - Monetary（金額）：權重 20%，消費金額越低，分數越低

        Parameters
        ----------
        at_risk_customers : DataFrame
            流失風險客戶資料

        Returns
        -------
        DataFrame
            添加了流失風險評分的 DataFrame
        """
        print("計算流失風險評分...")

        df = at_risk_customers.copy()

        # 標準化各指標到 0-100 範圍
        # Recency：最後購買距離越近，評分越高
        max_recency = df['days_since_last_purchase'].max()
        df['recency_score'] = (1 - df['days_since_last_purchase'] / max_recency) * 100

        # Frequency：購買頻率越高，評分越高
        max_frequency = df['purchase_frequency'].max()
        df['frequency_score'] = (df['purchase_frequency'] / max_frequency) * 100

        # Monetary：消費額度越高，評分越高
        max_monetary = df['total_spent'].max()
        df['monetary_score'] = (df['total_spent'] / max_monetary) * 100

        # 計算加權平均分（流失風險評分的反面 = 客戶價值評分）
        df['customer_value_score'] = (
            df['recency_score'] * 0.5 +
            df['frequency_score'] * 0.3 +
            df['monetary_score'] * 0.2
        )

        # 流失風險評分 = 100 - 客戶價值評分
        df['churn_risk_score'] = 100 - df['customer_value_score']

        # 取值範圍限制在 0-100
        df['churn_risk_score'] = df['churn_risk_score'].clip(0, 100)

        return df

    def define_retention_actions(self, df):
        """
        根據流失風險評分定義保留策略

        Parameters
        ----------
        df : DataFrame
            包含流失風險評分的 DataFrame

        Returns
        -------
        DataFrame
            添加了建議行動的 DataFrame
        """
        print("定義保留策略...")

        df = df.copy()

        def get_retention_action(row):
            """根據流失風險評分決定行動"""
            score = row['churn_risk_score']

            if score >= 75:
                return '立即聯絡 + 大幅折扣'
            elif score >= 60:
                return '定向營銷 + 優惠'
            elif score >= 45:
                return '定期郵件 + 輕微激勵'
            elif score >= 30:
                return '列入跟蹤名單'
            else:
                return '標準郵件營銷'

        def get_priority(row):
            """確定行動優先級"""
            score = row['churn_risk_score']
            value = row['customer_value_score']

            if score >= 75 and value >= 50:
                return 'P0 - Critical VIP'
            elif score >= 75:
                return 'P1 - Critical'
            elif score >= 60 and value >= 60:
                return 'P1 - High Value'
            elif score >= 60:
                return 'P2 - Medium'
            else:
                return 'P3 - Low'

        df['retention_action'] = df.apply(get_retention_action, axis=1)
        df['action_priority'] = df.apply(get_priority, axis=1)

        return df

    def segment_by_churn_risk(self, df):
        """
        按流失風險分段客戶

        Parameters
        ----------
        df : DataFrame
            包含流失風險評分的 DataFrame

        Returns
        -------
        DataFrame
            分段統計表
        """
        print("按流失風險進行客戶分段...")

        segments = {
            'Critical (75-100)': df[df['churn_risk_score'] >= 75],
            'High (60-75)': df[(df['churn_risk_score'] >= 60) & (df['churn_risk_score'] < 75)],
            'Medium (45-60)': df[(df['churn_risk_score'] >= 45) & (df['churn_risk_score'] < 60)],
            'Low (30-45)': df[(df['churn_risk_score'] >= 30) & (df['churn_risk_score'] < 45)],
            'Minimal (<30)': df[df['churn_risk_score'] < 30]
        }

        segment_stats = []
        for segment_name, segment_df in segments.items():
            if len(segment_df) > 0:
                segment_stats.append({
                    '分段': segment_name,
                    '客戶數': len(segment_df),
                    '佔比': f"{len(segment_df) / len(df) * 100:.2f}%",
                    '平均流失評分': segment_df['churn_risk_score'].mean(),
                    '平均客戶價值': segment_df['customer_value_score'].mean(),
                    '平均消費': segment_df['total_spent'].mean(),
                    '平均購買頻率': segment_df['purchase_frequency'].mean()
                })

        return pd.DataFrame(segment_stats)

    def visualize_churn_analysis(self, df, output_dir='./churn_outputs'):
        """
        視覺化流失分析

        Parameters
        ----------
        df : DataFrame
            包含流失評分的客戶資料
        output_dir : str
            輸出目錄路徑

        Returns
        -------
        Figure
            Matplotlib figure 物件
        """
        import os
        os.makedirs(output_dir, exist_ok=True)

        print("繪製流失風險分析圖表...")

        fig, axes = plt.subplots(2, 2, figsize=(16, 12))
        fig.suptitle('Customer Churn Risk Analysis', fontsize=16, fontweight='bold')

        # 1. 流失風險評分分布
        axes[0, 0].hist(df['churn_risk_score'], bins=30, color='steelblue', edgecolor='black')
        axes[0, 0].axvline(df['churn_risk_score'].mean(), color='red', linestyle='--', linewidth=2, label='Mean')
        axes[0, 0].set_title('Distribution of Churn Risk Scores', fontweight='bold')
        axes[0, 0].set_xlabel('Churn Risk Score')
        axes[0, 0].set_ylabel('Number of Customers')
        axes[0, 0].legend()

        # 2. 風險等級客戶數
        risk_dist = df['churn_risk_level'].value_counts().sort_index(
            key=lambda x: x.map({'Low': 0, 'Medium': 1, 'High': 2, 'Critical': 3})
        )
        colors = ['green', 'yellow', 'orange', 'red']
        axes[0, 1].bar(risk_dist.index, risk_dist.values, color=colors[:len(risk_dist)])
        axes[0, 1].set_title('Customer Count by Risk Level', fontweight='bold')
        axes[0, 1].set_ylabel('Number of Customers')

        # 3. Recency vs Churn Risk Score
        scatter = axes[1, 0].scatter(
            df['days_since_last_purchase'],
            df['churn_risk_score'],
            c=df['total_spent'],
            s=50,
            alpha=0.6,
            cmap='viridis'
        )
        axes[1, 0].set_title('Days Since Last Purchase vs Churn Risk Score', fontweight='bold')
        axes[1, 0].set_xlabel('Days Since Last Purchase')
        axes[1, 0].set_ylabel('Churn Risk Score')
        plt.colorbar(scatter, ax=axes[1, 0], label='Total Spent')

        # 4. 客戶價值 vs 流失風險
        scatter2 = axes[1, 1].scatter(
            df['customer_value_score'],
            df['churn_risk_score'],
            c=df['purchase_frequency'],
            s=50,
            alpha=0.6,
            cmap='plasma'
        )
        axes[1, 1].set_title('Customer Value vs Churn Risk', fontweight='bold')
        axes[1, 1].set_xlabel('Customer Value Score')
        axes[1, 1].set_ylabel('Churn Risk Score')
        plt.colorbar(scatter2, ax=axes[1, 1], label='Purchase Frequency')

        plt.tight_layout()
        fig.savefig(f'{output_dir}/churn_analysis.png', dpi=300, bbox_inches='tight')

        return fig

    def generate_report(self, output_dir='./churn_outputs', recency_threshold=90):
        """
        生成完整報告

        Parameters
        ----------
        output_dir : str
            輸出目錄路徑
        recency_threshold : int
            最近性閾值（天）

        Returns
        -------
        tuple
            (at_risk_customers, segment_stats, figure)
        """
        import os
        os.makedirs(output_dir, exist_ok=True)

        print("\n" + "="*60)
        print("開始客戶流失預警分析")
        print("="*60 + "\n")

        # 計算客戶指標
        customer_stats = self.calculate_customer_metrics()

        # 識別流失風險客戶
        at_risk = self.identify_at_risk_customers(customer_stats, recency_threshold)

        # 計算流失風險評分
        at_risk = self.calculate_churn_risk_score(at_risk)

        # 定義保留策略
        at_risk = self.define_retention_actions(at_risk)

        # 分段分析
        segment_stats = self.segment_by_churn_risk(at_risk)

        # 視覺化
        fig = self.visualize_churn_analysis(at_risk, output_dir)

        # 保存結果
        print("\n保存分析結果...")
        at_risk.to_csv(f'{output_dir}/churn_risk_assessment.csv', index=False)
        segment_stats.to_csv(f'{output_dir}/churn_segments.csv', index=False)

        # 保存高風險客戶名單（用於直接行動）
        critical_customers = at_risk[at_risk['churn_risk_score'] >= 75][
            [self.customer_col, 'churn_risk_score', 'days_since_last_purchase',
             'total_spent', 'retention_action', 'action_priority']
        ].sort_values('churn_risk_score', ascending=False)
        critical_customers.to_csv(f'{output_dir}/critical_action_list.csv', index=False)

        self.churn_data = at_risk

        print(f"✓ 已保存到 {output_dir}/")
        print(f"  - churn_risk_assessment.csv: 完整流失風險評估")
        print(f"  - churn_segments.csv: 分段統計")
        print(f"  - critical_action_list.csv: 需要立即行動的客戶")

        return at_risk, segment_stats, fig

    def print_analysis_summary(self, df):
        """打印分析摘要"""
        print("\n" + "="*100)
        print("客戶流失預警分析摘要")
        print("="*100)

        print(f"\n總客戶數: {len(df):,}")

        print("\n【流失風險等級分布】")
        risk_dist = df['churn_risk_level'].value_counts()
        for risk, count in risk_dist.items():
            pct = count / len(df) * 100
            print(f"  {risk:10s}: {count:6,} 人 ({pct:5.2f}%)")

        print("\n【行動優先級分布】")
        priority_dist = df['action_priority'].value_counts()
        for priority, count in priority_dist.items():
            pct = count / len(df) * 100
            print(f"  {priority:20s}: {count:6,} 人 ({pct:5.2f}%)")

        print("\n【關鍵指標】")
        print(f"  平均流失風險評分: {df['churn_risk_score'].mean():.2f}")
        print(f"  平均客戶價值評分: {df['customer_value_score'].mean():.2f}")
        print(f"  平均最後購買距離: {df['days_since_last_purchase'].mean():.0f} 天")
        print(f"  平均購買頻率: {df['purchase_frequency'].mean():.2f} 次/年")


# ==================== 使用範例 ====================

if __name__ == "__main__":
    print("加載 Olist 資料...")
    orders, order_items, products, customers, sellers, payments, reviews = load_olist_data()

    # 準備交易資料
    print("準備交易資料...")
    transactions = orders.merge(payments, on='order_id', how='left')

    # 執行分析
    analyzer = ChurnPredictionAnalyzer(
        df=transactions,
        customer_col='customer_id',
        date_col='order_purchase_timestamp',
        amount_col='payment_value'
    )

    # 生成報告
    at_risk, segment_stats, fig = analyzer.generate_report(recency_threshold=90)

    # 打印摘要
    analyzer.print_analysis_summary(at_risk)

    # 打印分段統計
    print("\n" + "="*100)
    print("分段統計詳細表")
    print("="*100)
    print(segment_stats.to_string(index=False))

    print("\n" + "="*100)
    print("✓ 客戶流失預警分析完成！")
    print("="*100)
