"""
Cohort 營收分析 - Week 12
功能：
1. 按首次購買月份將客戶分群
2. 計算各月份的累計營收
3. 計算平均客戶生命週期價值（LTV）
4. 生成營收趨勢分析
5. 計算客戶獲取成本回收週期

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


class CohortRevenueAnalyzer:
    """
    Cohort 營收分析器
    分析不同時期獲得的客戶的營收情況
    """

    def __init__(self, df, customer_col, date_col, amount_col):
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
        """
        self.df = df.copy()
        self.customer_col = customer_col
        self.date_col = date_col
        self.amount_col = amount_col

        if not pd.api.types.is_datetime64_any_dtype(self.df[date_col]):
            self.df[date_col] = pd.to_datetime(self.df[date_col])

        self.cohort_data = None
        self.revenue_table = None

    def create_cohorts(self):
        """
        創建 Cohort（按首次購買月份）

        Returns
        -------
        DataFrame
            包含 cohort 資訊的交易資料
        """
        print("創建 Cohort...")

        df = self.df.copy()

        # 獲取每個客戶的首次購買月份和首次購買金額
        customer_cohort = df.groupby(self.customer_col).agg({
            self.date_col: 'min',
            self.amount_col: 'first'  # 首次購買金額
        }).reset_index()
        customer_cohort.columns = [self.customer_col, 'first_purchase_date', 'first_purchase_amount']
        customer_cohort['cohort_month'] = customer_cohort['first_purchase_date'].dt.to_period('M')

        # 合併回原資料
        df = df.merge(customer_cohort, on=self.customer_col, how='left')

        # 添加月份資訊
        df['transaction_month'] = df[self.date_col].dt.to_period('M')
        df['cohort_index'] = (df['transaction_month'] - df['cohort_month']).apply(lambda x: x.n)

        self.cohort_data = df

        print(f"✓ 創建了 {df['cohort_month'].nunique()} 個 cohort")

        return df

    def build_revenue_table(self):
        """
        構建營收表

        統計每個 cohort 在不同月份後的累計營收

        Returns
        -------
        DataFrame
            營收表（金額）
        """
        print("構建營收表...")

        # 計算每個 cohort 在每個月份的總營收
        revenue_table = self.cohort_data.groupby(
            ['cohort_month', 'cohort_index']
        )[self.amount_col].sum().unstack(fill_value=0)

        # 重新命名列標題
        revenue_table.columns = [f'M{int(i)}' if i >= 0 else f'M{int(i)}' for i in revenue_table.columns]

        self.revenue_table = revenue_table

        print(f"✓ 營收表包含 {len(revenue_table)} 個 cohort，最多 {revenue_table.shape[1]} 個月份")

        return revenue_table

    def build_cumulative_revenue_table(self):
        """
        構建累計營收表

        每個月份的營收是從首次購買到該月份的累計營收

        Returns
        -------
        DataFrame
            累計營收表
        """
        print("構建累計營收表...")

        revenue_table = self.revenue_table.copy()

        # 計算累計營收（沿著行方向累加）
        cumulative_revenue_table = revenue_table.cumsum(axis=1)

        return cumulative_revenue_table

    def calculate_ltv_by_cohort(self):
        """
        計算每個 Cohort 的平均 LTV

        Returns
        -------
        Series
            每個 cohort 的平均客戶生命週期價值
        """
        print("計算 Cohort 平均 LTV...")

        df = self.cohort_data

        # 計算每個客戶的總營收
        customer_revenue = df.groupby(self.customer_col)[self.amount_col].sum()

        # 計算每個客戶的首個 cohort
        customer_cohort = df.groupby(self.customer_col)['cohort_month'].first()

        # 合併並計算每個 cohort 的平均 LTV
        ltv_by_cohort = pd.DataFrame({
            'customer_id': customer_revenue.index,
            'ltv': customer_revenue.values,
            'cohort_month': [customer_cohort[cid] for cid in customer_revenue.index]
        }).groupby('cohort_month')['ltv'].agg(['mean', 'median', 'std', 'count'])

        ltv_by_cohort.columns = ['Average_LTV', 'Median_LTV', 'Std_LTV', 'Customer_Count']

        return ltv_by_cohort

    def calculate_revenue_per_customer(self):
        """
        計算每個 Cohort 的人均營收

        Returns
        -------
        DataFrame
            人均營收表
        """
        print("計算人均營收...")

        # 獲取每個 cohort 的客戶數
        cohort_size = self.cohort_data.groupby('cohort_month')[self.customer_col].nunique()

        # 計算人均營收
        revenue_per_customer = self.revenue_table.divide(cohort_size, axis=0)

        return revenue_per_customer

    def visualize_revenue_analysis(self, output_dir='./cohort_outputs'):
        """
        視覺化營收分析

        Parameters
        ----------
        output_dir : str
            輸出目錄路徑

        Returns
        -------
        Figure
            Matplotlib figure 物件
        """
        import os
        os.makedirs(output_dir, exist_ok=True)

        print("繪製營收分析圖表...")

        fig = plt.figure(figsize=(18, 12))
        gs = fig.add_gridspec(3, 2, hspace=0.3, wspace=0.3)

        # 1. 月度營收熱圖
        ax1 = fig.add_subplot(gs[0, :])
        sns.heatmap(self.revenue_table, annot=True, fmt='.0f', cmap='YlGn',
                    ax=ax1, cbar_kws={'label': 'Revenue'})
        ax1.set_title('Monthly Revenue by Cohort', fontweight='bold', fontsize=12)
        ax1.set_xlabel('Months After First Purchase')
        ax1.set_ylabel('Cohort Month')

        # 2. 累計營收熱圖
        cumulative_revenue_table = self.build_cumulative_revenue_table()
        ax2 = fig.add_subplot(gs[1, :])
        sns.heatmap(cumulative_revenue_table, annot=True, fmt='.0f', cmap='Blues',
                    ax=ax2, cbar_kws={'label': 'Cumulative Revenue'})
        ax2.set_title('Cumulative Revenue by Cohort', fontweight='bold', fontsize=12)
        ax2.set_xlabel('Months After First Purchase')
        ax2.set_ylabel('Cohort Month')

        # 3. 人均營收
        revenue_per_customer = self.calculate_revenue_per_customer()
        ax3 = fig.add_subplot(gs[2, 0])
        sns.heatmap(revenue_per_customer, annot=True, fmt='.2f', cmap='Spectral',
                    ax=ax3, cbar_kws={'label': 'Revenue per Customer'})
        ax3.set_title('Revenue per Customer by Cohort', fontweight='bold', fontsize=12)
        ax3.set_xlabel('Months After First Purchase')
        ax3.set_ylabel('Cohort Month')

        # 4. Cohort LTV 分布
        ltv_by_cohort = self.calculate_ltv_by_cohort()
        ax4 = fig.add_subplot(gs[2, 1])
        ax4.bar(range(len(ltv_by_cohort)), ltv_by_cohort['Average_LTV'].values,
                color=plt.cm.viridis(np.linspace(0, 1, len(ltv_by_cohort))))
        ax4.set_title('Average LTV by Cohort', fontweight='bold', fontsize=12)
        ax4.set_xlabel('Cohort Month')
        ax4.set_ylabel('Average LTV')
        ax4.set_xticks(range(len(ltv_by_cohort)))
        ax4.set_xticklabels([str(cohort) for cohort in ltv_by_cohort.index], rotation=45)

        fig.suptitle('Cohort Revenue Analysis', fontsize=16, fontweight='bold')
        fig.savefig(f'{output_dir}/revenue_analysis.png', dpi=300, bbox_inches='tight')

        return fig

    def generate_report(self, output_dir='./cohort_outputs'):
        """
        生成完整報告

        Parameters
        ----------
        output_dir : str
            輸出目錄路徑

        Returns
        -------
        tuple
            (revenue_table, ltv_by_cohort, figure)
        """
        import os
        os.makedirs(output_dir, exist_ok=True)

        print("\n" + "="*60)
        print("開始 Cohort 營收分析")
        print("="*60 + "\n")

        # 創建 cohort
        cohort_data = self.create_cohorts()

        # 構建營收表
        revenue_table = self.build_revenue_table()

        # 累計營收表
        cumulative_revenue_table = self.build_cumulative_revenue_table()

        # 計算 LTV
        ltv_by_cohort = self.calculate_ltv_by_cohort()

        # 人均營收
        revenue_per_customer = self.calculate_revenue_per_customer()

        # 視覺化
        fig = self.visualize_revenue_analysis(output_dir)

        # 保存結果
        print("\n保存分析結果...")
        revenue_table.to_csv(f'{output_dir}/revenue_by_cohort.csv')
        cumulative_revenue_table.to_csv(f'{output_dir}/cumulative_revenue_by_cohort.csv')
        ltv_by_cohort.to_csv(f'{output_dir}/ltv_by_cohort.csv')
        revenue_per_customer.to_csv(f'{output_dir}/revenue_per_customer.csv')

        print(f"✓ 已保存到 {output_dir}/")

        return revenue_table, ltv_by_cohort, fig

    def print_analysis_summary(self):
        """打印分析摘要"""
        print("\n" + "="*80)
        print("Cohort 營收分析摘要")
        print("="*80)

        revenue_table = self.revenue_table
        ltv_by_cohort = self.calculate_ltv_by_cohort()
        revenue_per_customer = self.calculate_revenue_per_customer()

        print(f"\n總 Cohort 數: {len(revenue_table)}")
        print(f"最長追蹤期: {revenue_table.shape[1]} 個月")

        print("\n【Cohort 級別平均 LTV】")
        for cohort, row in ltv_by_cohort.iterrows():
            print(f"  {cohort}: ${row['Average_LTV']:.2f} (中位數: ${row['Median_LTV']:.2f}, 客戶數: {row['Customer_Count']:.0f})")

        print("\n【月度營收趨勢（所有 Cohort 平均）】")
        monthly_avg = revenue_table.mean()
        for month, revenue in monthly_avg.items():
            print(f"  {month}: ${revenue:.2f}")

        print("\n【人均營收趨勢（所有 Cohort 平均）】")
        per_customer_avg = revenue_per_customer.mean()
        for month, per_customer in per_customer_avg.items():
            print(f"  {month}: ${per_customer:.2f}")

        print("\n【關鍵洞察】")
        total_revenue = revenue_table.sum().sum()
        print(f"  總營收: ${total_revenue:,.2f}")
        print(f"  平均首月營收: ${revenue_table.iloc[:, 0].mean():.2f}")
        print(f"  最高 LTV Cohort: {ltv_by_cohort['Average_LTV'].idxmax()} (${ltv_by_cohort['Average_LTV'].max():.2f})")
        print(f"  最低 LTV Cohort: {ltv_by_cohort['Average_LTV'].idxmin()} (${ltv_by_cohort['Average_LTV'].min():.2f})")


# ==================== 使用範例 ====================

if __name__ == "__main__":
    print("加載 Olist 資料...")
    orders, order_items, products, customers, sellers, payments, reviews = load_olist_data()

    # 準備交易資料
    print("準備交易資料...")
    transactions = orders.merge(payments, on='order_id', how='left')

    # 執行分析
    analyzer = CohortRevenueAnalyzer(
        df=transactions,
        customer_col='customer_id',
        date_col='order_purchase_timestamp',
        amount_col='payment_value'
    )

    # 生成報告
    revenue_table, ltv_by_cohort, fig = analyzer.generate_report()

    # 打印摘要
    analyzer.print_analysis_summary()

    print("\n" + "="*80)
    print("✓ Cohort 營收分析完成！")
    print("="*80)
