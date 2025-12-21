"""
RFM + K-Means 聚類分群 - Week 12
功能：
1. 計算 RFM 指標
2. 數據標準化處理
3. 使用 K-Means 算法進行自動分群
4. 通過 Elbow 方法確定最優簇數
5. 分群質量評估（輪廓係數、戴維斯-博爾頓指數）
6. 視覺化分群結果

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
from sklearn.preprocessing import StandardScaler
from sklearn.cluster import KMeans
from sklearn.metrics import silhouette_score, davies_bouldin_score
import warnings

warnings.filterwarnings('ignore')

# 設定路徑
sys.path.append(str(Path(__file__).parent.parent.parent / 'week03-06_pandas-advanced' / 'utils'))
from data_loader import load_olist_data


class RFMClusteringAnalyzer:
    """
    RFM + K-Means 聚類分析器
    使用機器學習方法進行客戶分群
    """

    def __init__(self, df, customer_col, date_col, amount_col, analysis_date=None):
        """
        初始化聚類分析器

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

        # 確保日期欄位是 datetime 類型
        if not pd.api.types.is_datetime64_any_dtype(self.df[date_col]):
            self.df[date_col] = pd.to_datetime(self.df[date_col])

        self.analysis_date = analysis_date or self.df[date_col].max()
        self.scaler = StandardScaler()
        self.kmeans = None
        self.optimal_k = None

    def calculate_rfm(self):
        """
        計算 RFM 指標

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

        rfm.columns = [self.customer_col, 'Recency', 'Frequency', 'Monetary']
        rfm = rfm.set_index(self.customer_col)

        # 替換異常值
        rfm = rfm.replace([np.inf, -np.inf], np.nan).dropna()

        return rfm

    def normalize_rfm(self, rfm):
        """
        對 RFM 數據進行標準化

        使用 StandardScaler 進行 Z-score 標準化，確保各指標在同一量綱

        Parameters
        ----------
        rfm : DataFrame
            原始 RFM 資料

        Returns
        -------
        array
            標準化後的 RFM 數據（numpy array）
        """
        print("對 RFM 數據進行標準化...")

        # 提取 RFM 欄位
        rfm_values = rfm[['Recency', 'Frequency', 'Monetary']].values

        # 標準化（Recency 反轉，因為小值更好）
        rfm_values_normalized = rfm_values.copy()
        rfm_values_normalized[:, 0] = -rfm_values_normalized[:, 0]  # Recency 反轉

        rfm_values_normalized = self.scaler.fit_transform(rfm_values_normalized)

        return rfm_values_normalized

    def find_optimal_clusters(self, rfm_normalized, max_k=10):
        """
        使用 Elbow 方法和輪廓係數確定最優簇數

        Parameters
        ----------
        rfm_normalized : array
            標準化的 RFM 數據
        max_k : int
            最大簇數

        Returns
        -------
        tuple
            (最優簇數, 慣性列表, 輪廓係數列表, 戴維斯-博爾頓指數列表)
        """
        print(f"尋找最優簇數（測試 K=2 到 {max_k}）...")

        inertias = []
        silhouette_scores = []
        davies_bouldin_scores = []
        k_range = range(2, max_k + 1)

        for k in k_range:
            kmeans = KMeans(n_clusters=k, random_state=42, n_init=10)
            kmeans.fit(rfm_normalized)

            inertias.append(kmeans.inertia_)
            silhouette_scores.append(silhouette_score(rfm_normalized, kmeans.labels_))
            davies_bouldin_scores.append(davies_bouldin_score(rfm_normalized, kmeans.labels_))

        # 確定最優簇數（基於輪廓係數最高）
        optimal_k = k_range[np.argmax(silhouette_scores)]
        self.optimal_k = optimal_k

        print(f"最優簇數：{optimal_k}")
        print(f"最優輪廓係數：{max(silhouette_scores):.4f}")

        return optimal_k, inertias, silhouette_scores, davies_bouldin_scores

    def perform_kmeans_clustering(self, rfm_normalized):
        """
        執行 K-Means 聚類

        Parameters
        ----------
        rfm_normalized : array
            標準化的 RFM 數據

        Returns
        -------
        array
            聚類標籤
        """
        print(f"執行 K-Means 聚類（K={self.optimal_k}）...")

        self.kmeans = KMeans(n_clusters=self.optimal_k, random_state=42, n_init=10)
        cluster_labels = self.kmeans.fit_predict(rfm_normalized)

        return cluster_labels

    def cluster_analysis(self, rfm, cluster_labels):
        """
        分群特徵分析

        Parameters
        ----------
        rfm : DataFrame
            RFM 資料
        cluster_labels : array
            聚類標籤

        Returns
        -------
        DataFrame
            分群統計表
        """
        print("分析各簇的特徵...")

        rfm_copy = rfm.copy()
        rfm_copy['Cluster'] = cluster_labels

        cluster_stats = rfm_copy.groupby('Cluster').agg({
            'Recency': ['count', 'mean', 'median', 'std'],
            'Frequency': ['mean', 'median', 'std'],
            'Monetary': ['mean', 'median', 'std', 'sum']
        }).round(2)

        cluster_stats.columns = ['_'.join(col).strip() for col in cluster_stats.columns]
        cluster_stats = cluster_stats.rename(columns={'Recency_count': 'Customer_Count'})

        # 計算百分比
        cluster_stats['Percentage'] = (
            cluster_stats['Customer_Count'] / cluster_stats['Customer_Count'].sum() * 100
        ).round(2)

        cluster_stats['Revenue_Percentage'] = (
            cluster_stats['Monetary_sum'] / cluster_stats['Monetary_sum'].sum() * 100
        ).round(2)

        return cluster_stats.sort_values('Monetary_sum', ascending=False)

    def visualize_elbow_curve(self, inertias, silhouette_scores, davies_bouldin_scores, max_k=10):
        """
        繪製 Elbow 曲線和聚類評估指標

        Parameters
        ----------
        inertias : list
            各簇數的慣性值
        silhouette_scores : list
            輪廓係數
        davies_bouldin_scores : list
            戴維斯-博爾頓指數
        max_k : int
            最大簇數

        Returns
        -------
        Figure
            Matplotlib figure 物件
        """
        print("繪製 Elbow 曲線...")

        fig, axes = plt.subplots(1, 3, figsize=(18, 5))

        k_range = list(range(2, max_k + 1))

        # 1. Elbow 曲線
        axes[0].plot(k_range, inertias, 'bo-', linewidth=2, markersize=8)
        axes[0].axvline(x=self.optimal_k, color='r', linestyle='--', label=f'Optimal K={self.optimal_k}')
        axes[0].set_xlabel('Number of Clusters (K)')
        axes[0].set_ylabel('Inertia')
        axes[0].set_title('Elbow Curve', fontweight='bold')
        axes[0].grid(True, alpha=0.3)
        axes[0].legend()

        # 2. 輪廓係數
        axes[1].plot(k_range, silhouette_scores, 'go-', linewidth=2, markersize=8)
        max_silhouette_idx = np.argmax(silhouette_scores)
        axes[1].axvline(x=k_range[max_silhouette_idx], color='r', linestyle='--',
                        label=f'Max at K={k_range[max_silhouette_idx]}')
        axes[1].set_xlabel('Number of Clusters (K)')
        axes[1].set_ylabel('Silhouette Score')
        axes[1].set_title('Silhouette Coefficient (Higher is Better)', fontweight='bold')
        axes[1].grid(True, alpha=0.3)
        axes[1].legend()

        # 3. 戴維斯-博爾頓指數
        axes[2].plot(k_range, davies_bouldin_scores, 'mo-', linewidth=2, markersize=8)
        min_db_idx = np.argmin(davies_bouldin_scores)
        axes[2].axvline(x=k_range[min_db_idx], color='r', linestyle='--',
                        label=f'Min at K={k_range[min_db_idx]}')
        axes[2].set_xlabel('Number of Clusters (K)')
        axes[2].set_ylabel('Davies-Bouldin Index')
        axes[2].set_title('Davies-Bouldin Index (Lower is Better)', fontweight='bold')
        axes[2].grid(True, alpha=0.3)
        axes[2].legend()

        plt.tight_layout()
        return fig

    def visualize_clusters(self, rfm, cluster_labels):
        """
        視覺化聚類結果

        Parameters
        ----------
        rfm : DataFrame
            RFM 資料
        cluster_labels : array
            聚類標籤

        Returns
        -------
        Figure
            Matplotlib figure 物件
        """
        print("繪製聚類結果圖表...")

        fig, axes = plt.subplots(2, 2, figsize=(16, 12))
        fig.suptitle('K-Means Clustering Results', fontsize=16, fontweight='bold')

        rfm_copy = rfm.copy()
        rfm_copy['Cluster'] = cluster_labels

        # 1. 聚類客戶數
        cluster_counts = rfm_copy['Cluster'].value_counts().sort_index()
        colors = plt.cm.Set3(np.linspace(0, 1, len(cluster_counts)))
        axes[0, 0].bar(cluster_counts.index, cluster_counts.values, color=colors)
        axes[0, 0].set_title('Customer Count by Cluster', fontweight='bold')
        axes[0, 0].set_xlabel('Cluster')
        axes[0, 0].set_ylabel('Number of Customers')
        axes[0, 0].grid(True, alpha=0.3, axis='y')

        # 2. 聚類營收
        cluster_revenue = rfm_copy.groupby('Cluster')['Monetary'].sum().sort_index()
        axes[0, 1].bar(cluster_revenue.index, cluster_revenue.values, color=colors)
        axes[0, 1].set_title('Total Revenue by Cluster', fontweight='bold')
        axes[0, 1].set_xlabel('Cluster')
        axes[0, 1].set_ylabel('Total Revenue')
        axes[0, 1].grid(True, alpha=0.3, axis='y')

        # 3. Recency vs Frequency（按 Cluster 著色）
        scatter = axes[1, 0].scatter(
            rfm_copy['Recency'],
            rfm_copy['Frequency'],
            c=rfm_copy['Cluster'],
            s=rfm_copy['Monetary'] / 50,
            alpha=0.6,
            cmap='tab10'
        )
        axes[1, 0].set_xlabel('Recency (Days)')
        axes[1, 0].set_ylabel('Frequency (Times)')
        axes[1, 0].set_title('Recency vs Frequency', fontweight='bold')
        axes[1, 0].grid(True, alpha=0.3)
        cbar = plt.colorbar(scatter, ax=axes[1, 0])
        cbar.set_label('Cluster')

        # 4. Frequency vs Monetary
        scatter2 = axes[1, 1].scatter(
            rfm_copy['Frequency'],
            rfm_copy['Monetary'],
            c=rfm_copy['Cluster'],
            s=100,
            alpha=0.6,
            cmap='tab10'
        )
        axes[1, 1].set_xlabel('Frequency (Times)')
        axes[1, 1].set_ylabel('Monetary Value')
        axes[1, 1].set_title('Frequency vs Monetary', fontweight='bold')
        axes[1, 1].grid(True, alpha=0.3)
        cbar2 = plt.colorbar(scatter2, ax=axes[1, 1])
        cbar2.set_label('Cluster')

        plt.tight_layout()
        return fig

    def generate_report(self, output_dir='./rfm_clustering_outputs'):
        """
        生成完整分析報告

        Parameters
        ----------
        output_dir : str
            輸出目錄路徑

        Returns
        -------
        tuple
            (rfm, cluster_labels, cluster_stats, fig1, fig2)
        """
        import os
        os.makedirs(output_dir, exist_ok=True)

        print("\n" + "="*60)
        print("開始 RFM K-Means 聚類分析")
        print("="*60 + "\n")

        # 1. 計算 RFM
        rfm = self.calculate_rfm()

        # 2. 標準化
        rfm_normalized = self.normalize_rfm(rfm)

        # 3. 尋找最優簇數
        optimal_k, inertias, silhouette_scores, davies_bouldin_scores = \
            self.find_optimal_clusters(rfm_normalized, max_k=10)

        # 4. 執行聚類
        cluster_labels = self.perform_kmeans_clustering(rfm_normalized)

        # 5. 分群分析
        cluster_stats = self.cluster_analysis(rfm, cluster_labels)

        # 6. 視覺化
        fig1 = self.visualize_elbow_curve(inertias, silhouette_scores, davies_bouldin_scores)
        fig2 = self.visualize_clusters(rfm, cluster_labels)

        # 7. 保存結果
        print("\n保存分析結果...")
        rfm_copy = rfm.copy()
        rfm_copy['Cluster'] = cluster_labels
        rfm_copy.to_csv(f'{output_dir}/rfm_clustering_results.csv')

        cluster_stats.to_csv(f'{output_dir}/cluster_statistics.csv')

        fig1.savefig(f'{output_dir}/elbow_and_metrics.png', dpi=300, bbox_inches='tight')
        fig2.savefig(f'{output_dir}/clustering_visualization.png', dpi=300, bbox_inches='tight')

        print(f"✓ 已保存到 {output_dir}/")

        return rfm_copy, cluster_labels, cluster_stats, fig1, fig2

    def print_cluster_summary(self, rfm, cluster_labels):
        """
        打印聚類摘要

        Parameters
        ----------
        rfm : DataFrame
            RFM 資料
        cluster_labels : array
            聚類標籤
        """
        rfm_copy = rfm.copy()
        rfm_copy['Cluster'] = cluster_labels

        print("\n" + "="*80)
        print("K-Means 聚類摘要")
        print("="*80)

        print(f"\n最優簇數：{self.optimal_k}")
        print(f"輪廓係數：{silhouette_score(self.scaler.transform(rfm[['Recency', 'Frequency', 'Monetary']].values), cluster_labels):.4f}")
        print(f"戴維斯-博爾頓指數：{davies_bouldin_score(self.scaler.transform(rfm[['Recency', 'Frequency', 'Monetary']].values), cluster_labels):.4f}")

        print("\n【各簇客戶數分布】")
        cluster_dist = rfm_copy['Cluster'].value_counts().sort_index()
        for cluster, count in cluster_dist.items():
            pct = count / len(rfm_copy) * 100
            print(f"  Cluster {cluster}: {count:6,} 人 ({pct:5.2f}%)")

        print("\n【各簇營收分布】")
        cluster_revenue = rfm_copy.groupby('Cluster')['Monetary'].sum().sort_index()
        total_revenue = cluster_revenue.sum()
        for cluster, revenue in cluster_revenue.items():
            pct = revenue / total_revenue * 100
            print(f"  Cluster {cluster}: ${revenue:12,.2f} ({pct:5.2f}%)")


# ==================== 使用範例 ====================

if __name__ == "__main__":
    print("加載 Olist 資料...")
    orders, order_items, products, customers, sellers, payments, reviews = load_olist_data()

    # 準備交易資料
    print("準備交易資料...")
    transactions = orders.merge(payments, on='order_id', how='left')

    # 執行分析
    analyzer = RFMClusteringAnalyzer(
        df=transactions,
        customer_col='customer_id',
        date_col='order_purchase_timestamp',
        amount_col='payment_value'
    )

    # 生成報告
    rfm, cluster_labels, stats, fig1, fig2 = analyzer.generate_report()

    # 打印摘要
    analyzer.print_cluster_summary(rfm, cluster_labels)

    # 打印統計表
    print("\n" + "="*80)
    print("聚類統計詳細表")
    print("="*80)
    print(stats.to_string())

    print("\n" + "="*80)
    print("✓ RFM K-Means 聚類分析完成！")
    print("="*80)
