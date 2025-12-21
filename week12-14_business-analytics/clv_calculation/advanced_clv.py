"""
進階 CLV 計算（考慮折現率） - Week 13
功能：
1. 使用折現現金流（DCF）計算 CLV
2. 利潤邊際分析
3. 考慮客戶流失率
4. 考慮成本結構
5. 敏感性分析

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


class AdvancedCLVCalculator:
    """
    進階客戶生命週期價值計算器
    使用折現現金流和成本分析
    """

    def __init__(self, df, customer_col, date_col, amount_col, cost_col=None, analysis_date=None):
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
        cost_col : str, optional
            成本欄位名
        analysis_date : datetime, optional
            分析基準日期
        """
        self.df = df.copy()
        self.customer_col = customer_col
        self.date_col = date_col
        self.amount_col = amount_col
        self.cost_col = cost_col

        if not pd.api.types.is_datetime64_any_dtype(self.df[date_col]):
            self.df[date_col] = pd.to_datetime(self.df[date_col])

        self.analysis_date = analysis_date or self.df[date_col].max()
        self.clv_data = None

    def calculate_customer_metrics(self):
        """計算客戶基礎指標"""
        print("計算客戶指標...")

        customer_metrics = self.df.groupby(self.customer_col).agg({
            self.date_col: ['min', 'max', 'count'],
            self.amount_col: ['sum', 'mean', 'std']
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
            f'{self.amount_col}_std': 'purchase_std'
        })

        # 衍生指標
        customer_metrics['customer_lifespan_days'] = (
            customer_metrics['last_purchase_date'] - customer_metrics['first_purchase_date']
        ).dt.days + 1

        customer_metrics['customer_lifespan_years'] = customer_metrics['customer_lifespan_days'] / 365.25

        customer_metrics['purchase_frequency_yearly'] = (
            customer_metrics['purchase_count'] / (customer_metrics['customer_lifespan_years'] + 1)
        )

        return customer_metrics

    def estimate_churn_rate(self, customer_metrics):
        """
        估計客戶流失率

        基於購買頻率和最後購買時間

        Parameters
        ----------
        customer_metrics : DataFrame
            客戶指標資料

        Returns
        -------
        Series
            每個客戶的估計流失率
        """
        print("估計客戶流失率...")

        churn = customer_metrics.copy()

        # 計算購買間隔（天）
        churn['avg_days_between_purchases'] = (
            churn['customer_lifespan_days'] / (churn['purchase_count'] - 1)
        ).fillna(churn['customer_lifespan_days'])

        # 計算最後購買後的天數
        churn['days_since_last_purchase'] = (
            self.analysis_date - churn['last_purchase_date']
        ).dt.days

        # 流失率估計：如果距上次購買的日期超過平均購買間隔，流失風險增加
        # 使用簡單的線性模型
        churn['churn_probability'] = (
            churn['days_since_last_purchase'] / churn['avg_days_between_purchases']
        ).clip(0, 1)  # 限制在 0-1 之間

        # 年度留存率 = 1 - 流失率
        churn['annual_retention_rate'] = 1 - churn['churn_probability']

        return churn

    def calculate_dcf_clv(
        self,
        customer_metrics,
        discount_rate=0.10,
        prediction_years=5,
        gross_margin=0.30
    ):
        """
        使用折現現金流（DCF）計算 CLV

        CLV = Σ (年淨利潤 / (1 + 折現率)^年份) - 客戶獲取成本

        Parameters
        ----------
        customer_metrics : DataFrame
            客戶指標資料
        discount_rate : float
            折現率（默認 10%）
        prediction_years : int
            預測年數（默認 5 年）
        gross_margin : float
            毛利率（默認 30%）

        Returns
        -------
        DataFrame
            包含 DCF CLV 的 DataFrame
        """
        print(f"計算 DCF CLV（折現率: {discount_rate*100:.1f}%, 預測期: {prediction_years} 年）...")

        clv = customer_metrics.copy()

        # 估計流失率
        churn_data = self.estimate_churn_rate(customer_metrics)
        clv['annual_retention_rate'] = churn_data['annual_retention_rate']

        # 計算每年的預期營收
        annual_revenues = []
        for year in range(1, prediction_years + 1):
            # 每年的基礎營收 = 平均購買值 * 年度購買頻率
            base_revenue = clv['avg_purchase_value'] * clv['purchase_frequency_yearly']

            # 考慮流失率（每年的留存概率遞減）
            retention_factor = clv['annual_retention_rate'] ** year

            year_revenue = base_revenue * retention_factor

            # 計算淨利潤（營收 * 毛利率）
            net_profit = year_revenue * gross_margin

            # 計算現值（折現）
            present_value = net_profit / ((1 + discount_rate) ** year)

            annual_revenues.append(present_value)

        # 累加所有年份的現值
        clv['dcf_clv'] = pd.DataFrame(annual_revenues).sum(axis=0).values

        return clv

    def incorporate_costs(self, clv, cac=50, annual_service_cost=10):
        """
        納入成本因素

        Parameters
        ----------
        clv : DataFrame
            CLV 資料
        cac : float
            客戶獲取成本
        annual_service_cost : float
            年度服務成本

        Returns
        -------
        DataFrame
            納入成本後的 CLV
        """
        print(f"納入成本因素（CAC: ${cac}, 年服務成本: ${annual_service_cost}）...")

        clv = clv.copy()

        # 5 年的總服務成本
        clv['total_service_cost'] = annual_service_cost * 5

        # 實際 CLV = DCF CLV - CAC - 服務成本
        clv['net_clv'] = clv['dcf_clv'] - cac - clv['total_service_cost']

        # CLV:CAC 比率
        clv['clv_cac_ratio'] = clv['net_clv'] / cac

        # ROI (%)
        clv['roi_percentage'] = (clv['net_clv'] / (cac + clv['total_service_cost'])) * 100

        return clv

    def segment_by_clv(self, clv_data):
        """按 CLV 進行客戶分層"""
        print("按 CLV 進行客戶分層...")

        # 排除負 CLV（不盈利的客戶）
        clv_positive = clv_data[clv_data['net_clv'] > 0].copy()

        # 基於 CLV 的四分位數分層
        clv_quartiles = pd.qcut(
            clv_positive['net_clv'],
            q=4,
            labels=['Platinum', 'Gold', 'Silver', 'Bronze'],
            duplicates='drop'
        )

        clv_positive['clv_segment'] = clv_quartiles

        # 統計分層資訊
        segment_stats = clv_positive.groupby('clv_segment', observed=True).agg({
            self.customer_col: 'count',
            'net_clv': ['mean', 'min', 'max', 'sum'],
            'dcf_clv': ['mean', 'sum'],
            'total_revenue': ['mean', 'sum'],
            'purchase_frequency_yearly': 'mean',
            'annual_retention_rate': 'mean'
        }).round(2)

        segment_stats.columns = ['_'.join(col).strip() for col in segment_stats.columns]
        segment_stats = segment_stats.rename(columns={f'{self.customer_col}_count': 'customer_count'})

        # 計算百分比
        segment_stats['customer_percentage'] = (
            segment_stats['customer_count'] / segment_stats['customer_count'].sum() * 100
        ).round(2)

        segment_stats['revenue_percentage'] = (
            segment_stats['net_clv_sum'] / segment_stats['net_clv_sum'].sum() * 100
        ).round(2)

        return clv_positive, segment_stats

    def sensitivity_analysis(self, clv_data, base_discount_rate=0.10, base_margin=0.30):
        """
        進行敏感性分析

        分析折現率和毛利率變化對 CLV 的影響

        Parameters
        ----------
        clv_data : DataFrame
            CLV 資料
        base_discount_rate : float
            基礎折現率
        base_margin : float
            基礎毛利率

        Returns
        -------
        tuple
            (折現率敏感性, 毛利率敏感性)
        """
        print("進行敏感性分析...")

        discount_rates = np.arange(0.05, 0.21, 0.05)
        margins = np.arange(0.1, 0.51, 0.1)

        avg_clv_base = clv_data['dcf_clv'].mean()

        # 折現率敏感性
        discount_sensitivity = []
        for dr in discount_rates:
            temp_clv = self.calculate_dcf_clv(
                self.calculate_customer_metrics(),
                discount_rate=dr,
                prediction_years=5,
                gross_margin=base_margin
            )
            avg_clv = temp_clv['dcf_clv'].mean()
            sensitivity = (avg_clv - avg_clv_base) / avg_clv_base * 100
            discount_sensitivity.append({
                'discount_rate': dr,
                'average_clv': avg_clv,
                'sensitivity_percentage': sensitivity
            })

        # 毛利率敏感性
        margin_sensitivity = []
        for margin in margins:
            temp_clv = self.calculate_dcf_clv(
                self.calculate_customer_metrics(),
                discount_rate=base_discount_rate,
                prediction_years=5,
                gross_margin=margin
            )
            avg_clv = temp_clv['dcf_clv'].mean()
            sensitivity = (avg_clv - avg_clv_base) / avg_clv_base * 100
            margin_sensitivity.append({
                'gross_margin': margin,
                'average_clv': avg_clv,
                'sensitivity_percentage': sensitivity
            })

        return pd.DataFrame(discount_sensitivity), pd.DataFrame(margin_sensitivity)

    def visualize_advanced_clv(self, clv_data, output_dir='./advanced_clv_outputs'):
        """視覺化進階 CLV 分析"""
        import os
        os.makedirs(output_dir, exist_ok=True)

        print("繪製進階 CLV 分析圖表...")

        fig = plt.figure(figsize=(18, 12))
        gs = fig.add_gridspec(3, 2, hspace=0.3, wspace=0.3)

        # 1. CLV 分布
        ax1 = fig.add_subplot(gs[0, 0])
        ax1.hist(clv_data['net_clv'], bins=50, color='steelblue', edgecolor='black')
        ax1.axvline(clv_data['net_clv'].mean(), color='red', linestyle='--', linewidth=2)
        ax1.set_title('Distribution of Net CLV', fontweight='bold')
        ax1.set_xlabel('Net CLV ($)')
        ax1.set_ylabel('Number of Customers')

        # 2. 折現率影響
        ax2 = fig.add_subplot(gs[0, 1])
        discount_sens, _ = self.sensitivity_analysis(clv_data)
        ax2.plot(discount_sens['discount_rate'] * 100, discount_sens['sensitivity_percentage'],
                marker='o', linewidth=2, markersize=8)
        ax2.axhline(y=0, color='r', linestyle='--', alpha=0.5)
        ax2.set_title('Sensitivity to Discount Rate', fontweight='bold')
        ax2.set_xlabel('Discount Rate (%)')
        ax2.set_ylabel('CLV Change (%)')
        ax2.grid(True, alpha=0.3)

        # 3. 毛利率影響
        ax3 = fig.add_subplot(gs[1, 0])
        _, margin_sens = self.sensitivity_analysis(clv_data)
        ax3.plot(margin_sens['gross_margin'] * 100, margin_sens['sensitivity_percentage'],
                marker='s', linewidth=2, markersize=8, color='green')
        ax3.axhline(y=0, color='r', linestyle='--', alpha=0.5)
        ax3.set_title('Sensitivity to Gross Margin', fontweight='bold')
        ax3.set_xlabel('Gross Margin (%)')
        ax3.set_ylabel('CLV Change (%)')
        ax3.grid(True, alpha=0.3)

        # 4. CLV vs 客戶生命週期
        ax4 = fig.add_subplot(gs[1, 1])
        scatter = ax4.scatter(
            clv_data['customer_lifespan_years'],
            clv_data['net_clv'],
            c=clv_data['purchase_frequency_yearly'],
            s=100,
            alpha=0.6,
            cmap='viridis'
        )
        ax4.set_title('Customer Lifespan vs Net CLV', fontweight='bold')
        ax4.set_xlabel('Customer Lifespan (Years)')
        ax4.set_ylabel('Net CLV ($)')
        plt.colorbar(scatter, ax=ax4, label='Purchase Frequency')

        # 5. CLV vs 留存率
        ax5 = fig.add_subplot(gs[2, 0])
        scatter2 = ax5.scatter(
            clv_data['annual_retention_rate'],
            clv_data['net_clv'],
            c=clv_data['total_revenue'],
            s=100,
            alpha=0.6,
            cmap='plasma'
        )
        ax5.set_title('Retention Rate vs Net CLV', fontweight='bold')
        ax5.set_xlabel('Annual Retention Rate')
        ax5.set_ylabel('Net CLV ($)')
        plt.colorbar(scatter2, ax=ax5, label='Total Revenue')

        # 6. CLV 分層
        ax6 = fig.add_subplot(gs[2, 1])
        clv_positive, segment_stats = self.segment_by_clv(clv_data)
        segment_counts = clv_positive['clv_segment'].value_counts().sort_index()
        colors = ['#1f77b4', '#2ca02c', '#ff7f0e', '#d62728']
        ax6.bar(segment_counts.index, segment_counts.values, color=colors[:len(segment_counts)])
        ax6.set_title('Customer Count by CLV Segment', fontweight='bold')
        ax6.set_ylabel('Number of Customers')

        fig.suptitle('Advanced CLV Analysis with Discount Rate', fontsize=16, fontweight='bold')
        fig.savefig(f'{output_dir}/advanced_clv_analysis.png', dpi=300, bbox_inches='tight')

        return fig

    def generate_report(self, output_dir='./advanced_clv_outputs',
                       discount_rate=0.10, gross_margin=0.30, cac=50):
        """生成完整報告"""
        import os
        os.makedirs(output_dir, exist_ok=True)

        print("\n" + "="*60)
        print("開始進階 CLV 計算")
        print("="*60 + "\n")

        # 計算基礎指標
        customer_metrics = self.calculate_customer_metrics()

        # 計算 DCF CLV
        clv_data = self.calculate_dcf_clv(
            customer_metrics,
            discount_rate=discount_rate,
            prediction_years=5,
            gross_margin=gross_margin
        )

        # 納入成本
        clv_data = self.incorporate_costs(clv_data, cac=cac, annual_service_cost=10)

        # 分層分析
        clv_positive, segment_stats = self.segment_by_clv(clv_data)

        # 視覺化
        fig = self.visualize_advanced_clv(clv_data, output_dir)

        # 保存結果
        print("\n保存分析結果...")
        self.clv_data = clv_data

        output_cols = [
            self.customer_col, 'purchase_count', 'total_revenue',
            'avg_purchase_value', 'purchase_frequency_yearly',
            'annual_retention_rate', 'dcf_clv', 'net_clv',
            'clv_cac_ratio', 'roi_percentage'
        ]

        clv_data[output_cols].to_csv(f'{output_dir}/advanced_clv_analysis.csv', index=False)
        segment_stats.to_csv(f'{output_dir}/clv_segment_statistics.csv')

        print(f"✓ 已保存到 {output_dir}/")

        return clv_data, segment_stats, fig

    def print_analysis_summary(self, clv_data):
        """打印分析摘要"""
        print("\n" + "="*100)
        print("進階 CLV 分析摘要（考慮折現率）")
        print("="*100)

        print(f"\n總客戶數: {len(clv_data):,}")

        print("\n【CLV 統計】")
        print(f"  平均 DCF CLV: ${clv_data['dcf_clv'].mean():,.2f}")
        print(f"  平均淨 CLV: ${clv_data['net_clv'].mean():,.2f}")
        print(f"  總淨 CLV: ${clv_data['net_clv'].sum():,.2f}")

        print("\n【成本和回報】")
        print(f"  平均 CLV:CAC 比率: {clv_data['clv_cac_ratio'].mean():.2f}x")
        print(f"  平均 ROI: {clv_data['roi_percentage'].mean():.2f}%")

        print("\n【客戶質量】")
        positive_pct = (clv_data['net_clv'] > 0).sum() / len(clv_data) * 100
        print(f"  盈利客戶佔比: {positive_pct:.1f}%")
        print(f"  平均留存率: {clv_data['annual_retention_rate'].mean():.2%}")

        clv_positive, segment_stats = self.segment_by_clv(clv_data)
        print("\n【客戶分層營收貢獻】")
        for idx, row in segment_stats.iterrows():
            print(f"  {idx}: {row['customer_count']:.0f} 人 - " +
                 f"營收: ${row['net_clv_sum']:,.2f} ({row['revenue_percentage']:.1f}%)")


# ==================== 使用範例 ====================

if __name__ == "__main__":
    print("加載 Olist 資料...")
    orders, order_items, products, customers, sellers, payments, reviews = load_olist_data()

    # 準備交易資料
    print("準備交易資料...")
    transactions = orders.merge(payments, on='order_id', how='left')

    # 執行計算
    calculator = AdvancedCLVCalculator(
        df=transactions,
        customer_col='customer_id',
        date_col='order_purchase_timestamp',
        amount_col='payment_value'
    )

    # 生成報告
    clv_data, segment_stats, fig = calculator.generate_report(
        discount_rate=0.10,
        gross_margin=0.30,
        cac=50
    )

    # 打印摘要
    calculator.print_analysis_summary(clv_data)

    print("\n" + "="*100)
    print("✓ 進階 CLV 計算完成！")
    print("="*100)
