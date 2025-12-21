"""
基礎 RFM 客戶分析 - Week 12
功能：
1. 計算 Recency、Frequency、Monetary
2. 五等分評分（1-5分）
3. 客戶分群（11 種標準分群）
4. 各群特徵描述
5. 視覺化與報表輸出

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

# 設定路徑
sys.path.append(str(Path(__file__).parent.parent.parent / 'week03-06_pandas-advanced' / 'utils'))
from data_loader import load_olist_data


class RFMAnalyzer:
    """
    RFM 分析器類
    計算客戶的 Recency、Frequency、Monetary 指標，進行客戶分群
    """

    def __init__(self, df, customer_col, date_col, amount_col, analysis_date=None):
        """
        初始化 RFM 分析器

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
            分析基準日期，預設為資料中的最新日期

        Examples
        --------
        >>> analyzer = RFMAnalyzer(transactions, 'customer_id',
        ...                         'order_purchase_timestamp', 'payment_value')
        """
        self.df = df.copy()
        self.customer_col = customer_col
        self.date_col = date_col
        self.amount_col = amount_col

        # 確保日期欄位是 datetime 類型
        if not pd.api.types.is_datetime64_any_dtype(self.df[date_col]):
            self.df[date_col] = pd.to_datetime(self.df[date_col])

        # 設定分析基準日期（資料中的最新日期）
        self.analysis_date = analysis_date or self.df[date_col].max()

        # 儲存結果
        self.rfm = None
        self.segment_stats = None

    def calculate_rfm(self):
        """
        計算 RFM 指標

        - Recency (R): 最近一次購買至今天的天數（越小越好）
        - Frequency (F): 購買次數（越多越好）
        - Monetary (M): 累計消費金額（越高越好）

        Returns
        -------
        DataFrame
            包含 RFM 三個指標的 DataFrame
        """
        print("計算 RFM 指標...")

        rfm = self.df.groupby(self.customer_col).agg({
            self.date_col: lambda x: (self.analysis_date - x.max()).days,  # Recency
            self.customer_col: 'count',  # Frequency
            self.amount_col: 'sum'  # Monetary
        }).reset_index()

        # 重新命名欄位
        rfm.columns = [self.customer_col, 'Recency', 'Frequency', 'Monetary']
        rfm = rfm.set_index(self.customer_col)

        # 替換非數值
        rfm = rfm.replace([np.inf, -np.inf], np.nan).dropna()

        return rfm

    def assign_rfm_scores(self, rfm):
        """
        分配 RFM 評分（五分位：1-5分）

        - R 分數：最近性（Recency），越近越好，所以低值得高分
        - F 分數：頻率（Frequency），越高越好，高值得高分
        - M 分數：金額（Monetary），越高越好，高值得高分

        Parameters
        ----------
        rfm : DataFrame
            包含原始 RFM 值的 DataFrame

        Returns
        -------
        DataFrame
            添加了分數欄位的 DataFrame
        """
        print("分配 RFM 評分...")

        # Recency：最近性，越小越好（反轉評分）
        rfm['R_Score'] = pd.qcut(rfm['Recency'], 5, labels=[5, 4, 3, 2, 1], duplicates='drop')

        # Frequency：頻率，越多越好
        rfm['F_Score'] = pd.qcut(rfm['Frequency'].rank(method='first'), 5,
                                  labels=[1, 2, 3, 4, 5], duplicates='drop')

        # Monetary：金額，越高越好
        rfm['M_Score'] = pd.qcut(rfm['Monetary'], 5, labels=[1, 2, 3, 4, 5], duplicates='drop')

        # 轉換為整數方便後續使用
        rfm['R_Score'] = rfm['R_Score'].astype(int)
        rfm['F_Score'] = rfm['F_Score'].astype(int)
        rfm['M_Score'] = rfm['M_Score'].astype(int)

        # RFM 綜合評分（如 543 表示 R=5, F=4, M=3）
        rfm['RFM_Score'] = (rfm['R_Score'].astype(str) +
                             rfm['F_Score'].astype(str) +
                             rfm['M_Score'].astype(str))

        # 計算平均分
        rfm['RFM_Avg_Score'] = (rfm['R_Score'] + rfm['F_Score'] + rfm['M_Score']) / 3

        return rfm

    def segment_customers(self, rfm):
        """
        客戶分群（11 種標準分群）

        根據 RFM 分數將客戶分為 11 個群組，各群特點：

        1. Champions: R≥4, F≥4, M≥4 - 最有價值的客戶
        2. Loyal Customers: F≥4 - 高頻率購買客戶
        3. Potential Loyalist: R≥3, F≥3 - 潛在忠實客戶
        4. Recent Customers: R≥4 - 近期購買客戶
        5. Promising: R≥3, M≤2 - 有前景的客戶
        6. Need Attention: R=3, F=3 - 需要關注的客戶
        7. About to Sleep: R=2 - 準備離開的客戶
        8. At Risk: F≥3, R≤2 - 有風險的高價值客戶
        9. Cannot Lose Them: F≥4, R≤1 - 即將流失的高價值客戶
        10. Hibernating: R≤2, F≤2 - 休眠客戶
        11. Lost: 其他 - 已流失客戶

        Parameters
        ----------
        rfm : DataFrame
            包含 RFM 分數的 DataFrame

        Returns
        -------
        DataFrame
            添加了分群欄位的 DataFrame
        """
        print("進行客戶分群...")

        def rfm_segment(row):
            """根據 RFM 分數判定客戶分群"""
            r, f, m = int(row['R_Score']), int(row['F_Score']), int(row['M_Score'])

            # Champions: 最佳客戶
            if r >= 4 and f >= 4 and m >= 4:
                return 'Champions'

            # Loyal Customers: 忠實客戶
            elif f >= 4 and r >= 3:
                return 'Loyal Customers'

            # Potential Loyalist: 潛在忠實客戶
            elif r >= 3 and f >= 3 and m >= 3:
                return 'Potential Loyalist'

            # Recent Customers: 近期購買客戶
            elif r >= 4 and f >= 2 and m >= 2:
                return 'Recent Customers'

            # Promising: 有前景客戶
            elif r >= 3 and f >= 2 and m <= 2:
                return 'Promising'

            # Need Attention: 需要關注
            elif r >= 2 and f >= 2 and m >= 2:
                return 'Need Attention'

            # About to Sleep: 準備睡眠
            elif r == 2 and f >= 2:
                return 'About to Sleep'

            # At Risk: 高價值但有風險
            elif f >= 3 and r <= 2:
                return 'At Risk'

            # Cannot Lose Them: 即將流失的明星客戶
            elif f >= 4 and r <= 1:
                return 'Cannot Lose Them'

            # Hibernating: 休眠客戶
            elif r <= 2 and f <= 2:
                return 'Hibernating'

            # Lost: 已流失
            else:
                return 'Lost'

        rfm['Segment'] = rfm.apply(rfm_segment, axis=1)
        return rfm

    def segment_analysis(self, rfm):
        """
        各分群特徵分析

        計算每個分群的平均 RFM 值、客戶數、營收貢獻等指標

        Parameters
        ----------
        rfm : DataFrame
            包含分群資訊的 DataFrame

        Returns
        -------
        DataFrame
            分群統計表
        """
        print("分析各分群特徵...")

        segment_stats = rfm.groupby('Segment').agg({
            'Recency': ['count', 'mean', 'median'],
            'Frequency': ['mean', 'median'],
            'Monetary': ['mean', 'median', 'sum'],
            'RFM_Avg_Score': 'mean'
        }).round(2)

        # 扁平化多層級欄位
        segment_stats.columns = ['_'.join(col).strip() for col in segment_stats.columns]
        segment_stats = segment_stats.rename(columns={'Recency_count': 'Customer_Count'})

        # 計算百分比
        segment_stats['Percentage'] = (
            segment_stats['Customer_Count'] / segment_stats['Customer_Count'].sum() * 100
        ).round(2)

        # 計算營收百分比
        segment_stats['Revenue_Percentage'] = (
            segment_stats['Monetary_sum'] / segment_stats['Monetary_sum'].sum() * 100
        ).round(2)

        # 排序（按營收大小）
        segment_stats = segment_stats.sort_values('Monetary_sum', ascending=False)

        return segment_stats

    def visualize_segments(self, rfm):
        """
        視覺化分群結果

        生成 4 個視覺化圖表：
        1. 各分群客戶數
        2. 各分群營收貢獻
        3. RFM 分佈散點圖
        4. 各分群平均 RFM 熱圖

        Parameters
        ----------
        rfm : DataFrame
            包含分群資訊的 DataFrame

        Returns
        -------
        Figure
            Matplotlib figure 物件
        """
        print("繪製視覺化圖表...")

        # 設定中文字體
        plt.rcParams['font.sans-serif'] = ['DejaVu Sans']

        fig, axes = plt.subplots(2, 2, figsize=(16, 12))
        fig.suptitle('RFM Customer Segmentation Analysis', fontsize=16, fontweight='bold')

        # 1. 分群客戶數（橫向條形圖）
        segment_counts = rfm['Segment'].value_counts().sort_values()
        colors1 = plt.cm.Set3(np.linspace(0, 1, len(segment_counts)))
        axes[0, 0].barh(segment_counts.index, segment_counts.values, color=colors1)
        axes[0, 0].set_title('Customer Count by Segment', fontsize=12, fontweight='bold')
        axes[0, 0].set_xlabel('Number of Customers')
        for i, v in enumerate(segment_counts.values):
            axes[0, 0].text(v + 5, i, str(int(v)), va='center')

        # 2. 分群營收貢獻（橫向條形圖）
        segment_revenue = rfm.groupby('Segment')['Monetary'].sum().sort_values()
        colors2 = plt.cm.Spectral(np.linspace(0, 1, len(segment_revenue)))
        axes[0, 1].barh(segment_revenue.index, segment_revenue.values, color=colors2)
        axes[0, 1].set_title('Revenue Contribution by Segment', fontsize=12, fontweight='bold')
        axes[0, 1].set_xlabel('Total Revenue')

        # 3. RFM 分佈（散點圖）
        # 使用 Recency 和 Frequency 作為坐標，Monetary 作為點的大小，Segment 作為顏色
        segments = rfm['Segment'].unique()
        colors_map = plt.cm.tab20(np.linspace(0, 1, len(segments)))
        segment_color_map = {seg: colors_map[i] for i, seg in enumerate(segments)}

        for segment in segments:
            segment_data = rfm[rfm['Segment'] == segment]
            axes[1, 0].scatter(
                segment_data['Recency'],
                segment_data['Frequency'],
                s=segment_data['Monetary'] / 50,
                alpha=0.6,
                label=segment,
                color=segment_color_map[segment]
            )

        axes[1, 0].set_xlabel('Recency (Days)')
        axes[1, 0].set_ylabel('Frequency (Times)')
        axes[1, 0].set_title('RFM Distribution', fontsize=12, fontweight='bold')
        axes[1, 0].legend(loc='best', fontsize=8, ncol=2)
        axes[1, 0].grid(True, alpha=0.3)

        # 4. 分群平均 RFM 分數熱圖
        segment_avg = rfm.groupby('Segment')[['R_Score', 'F_Score', 'M_Score']].mean()
        segment_avg = segment_avg.loc[segment_revenue.index]  # 按營收順序排列

        sns.heatmap(segment_avg.T, annot=True, fmt='.2f', cmap='RdYlGn',
                    ax=axes[1, 1], cbar_kws={'label': 'Score'},
                    vmin=1, vmax=5)
        axes[1, 1].set_title('Average RFM Scores by Segment', fontsize=12, fontweight='bold')
        axes[1, 1].set_xlabel('Segment')
        axes[1, 1].set_ylabel('RFM Score')

        plt.tight_layout()
        return fig

    def generate_report(self, output_dir='./rfm_outputs'):
        """
        生成完整 RFM 分析報告

        Parameters
        ----------
        output_dir : str
            輸出目錄路徑

        Returns
        -------
        tuple
            (rfm DataFrame, segment_stats DataFrame, figure)
        """
        import os
        os.makedirs(output_dir, exist_ok=True)

        print("\n" + "="*60)
        print("開始 RFM 分析報告生成")
        print("="*60 + "\n")

        # 1. 計算 RFM
        rfm = self.calculate_rfm()

        # 2. 分配評分
        rfm = self.assign_rfm_scores(rfm)

        # 3. 客戶分群
        rfm = self.segment_customers(rfm)
        self.rfm = rfm

        # 4. 分群分析
        segment_stats = self.segment_analysis(rfm)
        self.segment_stats = segment_stats

        # 5. 視覺化
        fig = self.visualize_segments(rfm)

        # 6. 輸出結果
        print("\n保存分析結果...")
        rfm.to_csv(f'{output_dir}/rfm_results.csv')
        segment_stats.to_csv(f'{output_dir}/rfm_segment_stats.csv')
        fig.savefig(f'{output_dir}/rfm_visualization.png', dpi=300, bbox_inches='tight')

        print(f"✓ 已保存到 {output_dir}/")
        print("  - rfm_results.csv: 客戶 RFM 評分和分群")
        print("  - rfm_segment_stats.csv: 分群統計")
        print("  - rfm_visualization.png: 視覺化圖表")

        return rfm, segment_stats, fig

    def print_segment_summary(self, rfm):
        """
        打印分群摘要報告

        Parameters
        ----------
        rfm : DataFrame
            包含分群資訊的 DataFrame
        """
        print("\n" + "="*80)
        print("RFM 分群摘要")
        print("="*80)

        print("\n【分群客戶數分布】")
        segment_dist = rfm['Segment'].value_counts()
        for segment, count in segment_dist.items():
            pct = count / len(rfm) * 100
            print(f"  {segment:20s}: {count:6,} 人 ({pct:5.2f}%)")

        print("\n【分群營收分布】")
        segment_revenue = rfm.groupby('Segment')['Monetary'].sum().sort_values(ascending=False)
        total_revenue = segment_revenue.sum()
        for segment, revenue in segment_revenue.items():
            pct = revenue / total_revenue * 100
            print(f"  {segment:20s}: ${revenue:12,.2f} ({pct:5.2f}%)")

        print("\n【各分群平均指標】")
        segment_avg = rfm.groupby('Segment')[['Recency', 'Frequency', 'Monetary']].mean()
        segment_avg = segment_avg.loc[segment_revenue.index]
        print(segment_avg.to_string())


# ==================== 使用範例 ====================

if __name__ == "__main__":
    print("加載 Olist 資料...")
    orders, order_items, products, customers, sellers, payments, reviews = load_olist_data()

    # 準備交易資料（合併訂單和付款）
    print("準備交易資料...")
    transactions = orders.merge(payments, on='order_id', how='left')

    # 執行 RFM 分析
    analyzer = RFMAnalyzer(
        df=transactions,
        customer_col='customer_id',
        date_col='order_purchase_timestamp',
        amount_col='payment_value'
    )

    # 生成完整報告
    rfm, stats, fig = analyzer.generate_report()

    # 打印分群摘要
    analyzer.print_segment_summary(rfm)

    # 打印分群統計表
    print("\n" + "="*80)
    print("分群統計詳細表")
    print("="*80)
    print(stats.to_string())

    print("\n" + "="*80)
    print("✓ RFM 分析完成！")
    print("="*80)
