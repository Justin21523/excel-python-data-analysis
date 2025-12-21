"""
Cohort 留存率分析 - Week 12
功能：
1. 按首次購買月份將客戶分群
2. 計算各月份的留存率
3. 生成留存率熱圖
4. 計算流失率和回購率
5. 分析留存趨勢

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


class CohortRetentionAnalyzer:
    """
    Cohort 留存率分析器
    分析不同時期獲得的客戶的留存情況
    """

    def __init__(self, df, customer_col, date_col):
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
        """
        self.df = df.copy()
        self.customer_col = customer_col
        self.date_col = date_col

        if not pd.api.types.is_datetime64_any_dtype(self.df[date_col]):
            self.df[date_col] = pd.to_datetime(self.df[date_col])

        self.cohort_data = None
        self.retention_table = None

    def create_cohorts(self):
        """
        創建 Cohort（按首次購買月份）

        Returns
        -------
        DataFrame
            包含 cohort_month 的交易資料
        """
        print("創建 Cohort...")

        df = self.df.copy()

        # 獲取每個客戶的首次購買月份
        customer_cohort = df.groupby(self.customer_col)[self.date_col].min().reset_index()
        customer_cohort.columns = [self.customer_col, 'first_purchase_date']
        customer_cohort['cohort_month'] = customer_cohort['first_purchase_date'].dt.to_period('M')

        # 合併回原資料
        df = df.merge(customer_cohort, on=self.customer_col, how='left')

        # 為每個交易添加 transaction_month
        df['transaction_month'] = df[self.date_col].dt.to_period('M')

        # 計算客戶在 cohort 後的月份索引（0 表示首月，1 表示次月，等等）
        df['cohort_index'] = (df['transaction_month'] - df['cohort_month']).apply(lambda x: x.n)

        self.cohort_data = df

        print(f"✓ 創建了 {df['cohort_month'].nunique()} 個 cohort")

        return df

    def build_retention_table(self):
        """
        構建留存率表

        統計每個 cohort 在不同月份後的活躍客戶數

        Returns
        -------
        DataFrame
            留存率表（百分比）
        """
        print("構建留存率表...")

        # 計算每個 cohort 在每個月份的獨特客戶數
        cohort_size = self.cohort_data.groupby('cohort_month')[self.customer_col].nunique()

        # 創建 cohort 用戶表（按 cohort_month 和 cohort_index）
        cohort_user_counts = self.cohort_data.groupby(
            ['cohort_month', 'cohort_index']
        )[self.customer_col].nunique().unstack(fill_value=0)

        # 計算留存率（相對於 cohort 的初始大小）
        retention_table = cohort_user_counts.divide(cohort_size, axis=0) * 100

        # 重新命名列標題為友好的月份標籤
        retention_table.columns = [f'M{int(i)}' if i >= 0 else f'M{int(i)}' for i in retention_table.columns]

        self.retention_table = retention_table

        print(f"✓ 留存率表包含 {len(retention_table)} 個 cohort，最多 {retention_table.shape[1]} 個月份")

        return retention_table

    def calculate_retention_stats(self):
        """
        計算留存率統計

        Returns
        -------
        dict
            包含各種留存統計的字典
        """
        print("計算留存率統計...")

        retention_table = self.retention_table

        stats = {
            '首月保留': retention_table.iloc[:, 0].mean(),  # 應該接近 100%
            '次月保留': retention_table.iloc[:, 1].mean() if retention_table.shape[1] > 1 else 0,
            '第三月保留': retention_table.iloc[:, 2].mean() if retention_table.shape[1] > 2 else 0,
            '平均留存': retention_table.iloc[:, 1:].mean().mean() if retention_table.shape[1] > 1 else 0,
            '最穩定的Cohort': retention_table.iloc[:, 1:].mean(axis=1).idxmax() if retention_table.shape[1] > 1 else None,
        }

        return stats

    def visualize_retention_heatmap(self, output_dir='./cohort_outputs'):
        """
        視覺化留存率熱圖

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

        print("繪製留存率熱圖...")

        fig, axes = plt.subplots(2, 1, figsize=(16, 10))
        fig.suptitle('Cohort Retention Analysis', fontsize=16, fontweight='bold')

        retention_table = self.retention_table

        # 1. 留存率熱圖
        sns.heatmap(retention_table, annot=True, fmt='.1f', cmap='RdYlGn',
                    ax=axes[0], cbar_kws={'label': 'Retention Rate (%)'}, vmin=0, vmax=100)
        axes[0].set_title('Monthly Retention Rates by Cohort', fontweight='bold', fontsize=12)
        axes[0].set_xlabel('Months After First Purchase')
        axes[0].set_ylabel('Cohort Month')

        # 2. 各 cohort 的留存趨勢線
        cohort_indices = range(min(6, retention_table.shape[1]))  # 只顯示前 6 個月
        colors = plt.cm.viridis(np.linspace(0, 1, len(retention_table)))

        for idx, (cohort, row) in enumerate(retention_table.iterrows()):
            retention_values = [row[f'M{i}'] if f'M{i}' in row.index else np.nan
                               for i in range(len(row))]
            retention_values = retention_values[:min(6, len(retention_values))]

            axes[1].plot(range(len(retention_values)), retention_values,
                        marker='o', label=str(cohort), color=colors[idx], linewidth=2)

        axes[1].set_title('Retention Trend by Cohort (First 6 Months)', fontweight='bold', fontsize=12)
        axes[1].set_xlabel('Months After First Purchase')
        axes[1].set_ylabel('Retention Rate (%)')
        axes[1].legend(loc='best', bbox_to_anchor=(1.05, 1), ncol=1, fontsize=9)
        axes[1].grid(True, alpha=0.3)

        plt.tight_layout()
        fig.savefig(f'{output_dir}/retention_heatmap.png', dpi=300, bbox_inches='tight')

        return fig

    def calculate_churn_rates(self):
        """
        計算流失率

        Returns
        -------
        DataFrame
            各 cohort 的月度流失率
        """
        print("計算流失率...")

        retention_table = self.retention_table

        # 流失率 = 1 - 留存率
        churn_rates = 100 - retention_table.iloc[:, 1:]

        return churn_rates

    def calculate_repeat_purchase_rate(self):
        """
        計算回購率

        Returns
        -------
        DataFrame
            各 cohort 的回購率
        """
        print("計算回購率...")

        df = self.cohort_data

        # 識別重複購買的客戶
        repeat_purchasers = df.groupby(self.customer_col)['transaction_month'].nunique()
        repeat_purchasers = repeat_purchasers[repeat_purchasers > 1].index

        # 創建回購指示
        df['is_repeat'] = df[self.customer_col].isin(repeat_purchasers)

        # 計算每個 cohort 的回購率
        repeat_rate = df[df['cohort_index'] >= 1].groupby('cohort_month').apply(
            lambda x: x['is_repeat'].sum() / x[self.customer_col].nunique() * 100 if x[self.customer_col].nunique() > 0 else 0
        )

        return repeat_rate

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
            (cohort_data, retention_table, figure)
        """
        import os
        os.makedirs(output_dir, exist_ok=True)

        print("\n" + "="*60)
        print("開始 Cohort 留存率分析")
        print("="*60 + "\n")

        # 創建 cohort
        cohort_data = self.create_cohorts()

        # 構建留存表
        retention_table = self.build_retention_table()

        # 計算統計
        stats = self.calculate_retention_stats()

        # 計算流失率
        churn_rates = self.calculate_churn_rates()

        # 計算回購率
        repeat_rate = self.calculate_repeat_purchase_rate()

        # 視覺化
        fig = self.visualize_retention_heatmap(output_dir)

        # 保存結果
        print("\n保存分析結果...")
        retention_table.to_csv(f'{output_dir}/retention_rates.csv')
        churn_rates.to_csv(f'{output_dir}/churn_rates.csv')

        # 保存統計
        with open(f'{output_dir}/retention_statistics.txt', 'w', encoding='utf-8') as f:
            f.write("Cohort Retention Statistics\n")
            f.write("="*50 + "\n\n")
            for key, value in stats.items():
                f.write(f"{key}: {value}\n")

        print(f"✓ 已保存到 {output_dir}/")

        return cohort_data, retention_table, fig

    def print_analysis_summary(self):
        """打印分析摘要"""
        print("\n" + "="*80)
        print("Cohort 留存率分析摘要")
        print("="*80)

        retention_table = self.retention_table

        print(f"\n總 Cohort 數: {len(retention_table)}")
        print(f"最長追蹤期: {retention_table.shape[1]} 個月")

        print("\n【留存率趨勢（按 Cohort 平均）】")
        retention_trend = retention_table.mean()
        for month, rate in retention_trend.items():
            print(f"  {month}: {rate:.2f}%")

        print("\n【按 Cohort 的首月客戶數】")
        for cohort, row in retention_table.iterrows():
            first_month_rate = row.iloc[0] if len(row) > 0 else 0
            print(f"  {cohort}: 100% (Base = 100%)")

        print("\n【關鍵洞察】")
        stats = self.calculate_retention_stats()
        print(f"  次月平均留存率: {stats['次月保留']:.2f}%")
        print(f"  平均留存率: {stats['平均留存']:.2f}%")
        if stats['最穩定的Cohort']:
            print(f"  最穩定的 Cohort: {stats['最穩定的Cohort']}")


# ==================== 使用範例 ====================

if __name__ == "__main__":
    print("加載 Olist 資料...")
    orders, order_items, products, customers, sellers, payments, reviews = load_olist_data()

    # 執行分析
    analyzer = CohortRetentionAnalyzer(
        df=orders,
        customer_col='customer_id',
        date_col='order_purchase_timestamp'
    )

    # 生成報告
    cohort_data, retention_table, fig = analyzer.generate_report()

    # 打印摘要
    analyzer.print_analysis_summary()

    # 打印留存率表
    print("\n" + "="*80)
    print("留存率表（%）")
    print("="*80)
    print(retention_table.to_string())

    print("\n" + "="*80)
    print("✓ Cohort 留存率分析完成！")
    print("="*80)
