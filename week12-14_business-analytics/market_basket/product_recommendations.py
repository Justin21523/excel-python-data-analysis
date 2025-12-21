"""
產品推薦系統 - Week 14
功能：
1. 基於協同過濾的推薦
2. 基於內容的推薦
3. 混合推薦算法
4. 推薦評估
5. 個性化推薦列表

Author: Business Analytics Week 12-14
Date: 2024-12-11
"""

import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
from sklearn.metrics.pairwise import cosine_similarity
from sklearn.feature_extraction.text import TfidfVectorizer
import sys
from pathlib import Path
import warnings

warnings.filterwarnings('ignore')

sys.path.append(str(Path(__file__).parent.parent.parent / 'week03-06_pandas-advanced' / 'utils'))
from data_loader import load_olist_data


class ProductRecommendationEngine:
    """產品推薦引擎"""

    def __init__(self, orders, order_items, products):
        """
        Parameters
        ----------
        orders : DataFrame
            訂單資料
        order_items : DataFrame
            訂單項目資料
        products : DataFrame
            商品資料
        """
        self.orders = orders
        self.order_items = order_items
        self.products = products
        self.user_product_matrix = None
        self.product_similarity = None

    def create_user_product_matrix(self):
        """創建用戶-商品交互矩陣"""
        print("創建用戶-商品交互矩陣...")

        # 合併訂單和商品
        merged = self.order_items.merge(self.orders[['order_id', 'customer_id']],
                                        on='order_id', how='left')

        # 創建交互矩陣（購買次數）
        user_product_matrix = merged.groupby(['customer_id', 'product_id']).size().unstack(fill_value=0)

        self.user_product_matrix = user_product_matrix

        print(f"✓ 矩陣大小: {user_product_matrix.shape}")

        return user_product_matrix

    def calculate_product_similarity(self):
        """計算商品相似度"""
        print("計算商品相似度...")

        # 基於用戶購買行為的相似度
        product_similarity = cosine_similarity(self.user_product_matrix.T)
        product_similarity_df = pd.DataFrame(
            product_similarity,
            index=self.user_product_matrix.columns,
            columns=self.user_product_matrix.columns
        )

        self.product_similarity = product_similarity_df

        return product_similarity_df

    def get_collaborative_recommendations(self, customer_id, n_recommendations=5):
        """協同過濾推薦"""
        if customer_id not in self.user_product_matrix.index:
            return pd.DataFrame()

        # 獲取該用戶購買過的商品
        customer_purchases = self.user_product_matrix.loc[customer_id]
        purchased_products = customer_purchases[customer_purchases > 0].index.tolist()

        # 查找相似商品
        similar_products = {}
        for product in purchased_products:
            similarities = self.product_similarity[product].copy()
            # 排除已購買的商品
            similarities = similarities[~similarities.index.isin(purchased_products)]
            similar_products.update(similarities.to_dict())

        # 排序並選擇前 N 個
        recommendations = sorted(similar_products.items(), key=lambda x: x[1], reverse=True)
        recommendations = [r[0] for r in recommendations[:n_recommendations]]

        return self.products[self.products['product_id'].isin(recommendations)]

    def get_category_recommendations(self, customer_id, n_recommendations=5):
        """基於類別的推薦"""
        if customer_id not in self.user_product_matrix.index:
            return pd.DataFrame()

        # 獲取客戶購買過的類別
        customer_purchases = self.user_product_matrix.loc[customer_id]
        purchased_products = customer_purchases[customer_purchases > 0].index.tolist()

        purchased_categories = self.products[
            self.products['product_id'].isin(purchased_products)
        ]['product_category_name'].unique()

        # 從相同類別推薦
        category_products = self.products[
            self.products['product_category_name'].isin(purchased_categories) &
            ~self.products['product_id'].isin(purchased_products)
        ]

        # 基於評分排序（如果有評分）
        if 'review_score' in category_products.columns:
            category_products = category_products.sort_values('review_score', ascending=False)

        return category_products.head(n_recommendations)

    def get_popularity_recommendations(self, n_recommendations=10):
        """熱門商品推薦"""
        popularity = self.order_items.groupby('product_id').size().reset_index(name='purchase_count')
        popular_products = popularity.nlargest(n_recommendations, 'purchase_count')['product_id'].tolist()

        return self.products[self.products['product_id'].isin(popular_products)]

    def generate_personalized_recommendations(self, customer_id, n_recommendations=10):
        """生成個性化推薦"""
        recommendations = []

        # 協同過濾
        collab_recs = self.get_collaborative_recommendations(customer_id, n_recommendations)
        if len(collab_recs) > 0:
            collab_recs['method'] = 'Collaborative Filtering'
            recommendations.append(collab_recs)

        # 類別推薦
        category_recs = self.get_category_recommendations(customer_id, n_recommendations)
        if len(category_recs) > 0:
            category_recs['method'] = 'Category Based'
            recommendations.append(category_recs)

        if recommendations:
            return pd.concat(recommendations, ignore_index=True).head(n_recommendations)
        else:
            # 返回熱門商品
            return self.get_popularity_recommendations(n_recommendations)

    def evaluate_recommendations(self, test_size=0.2):
        """評估推薦質量"""
        print("評估推薦質量...")

        # 簡單的評估指標：推薦命中率
        customer_ids = self.user_product_matrix.index.tolist()
        np.random.seed(42)
        test_customers = np.random.choice(customer_ids, size=int(len(customer_ids) * test_size),
                                         replace=False)

        hits = 0
        total = 0

        for customer in test_customers:
            recommendations = self.generate_personalized_recommendations(customer, n_recommendations=5)
            if len(recommendations) > 0:
                # 檢查是否有重複購買
                recommended_products = recommendations['product_id'].tolist()
                customer_future_purchases = self.user_product_matrix.loc[customer]
                overlap = len(set(recommended_products) & set(
                    customer_future_purchases[customer_future_purchases > 0].index
                ))
                if overlap > 0:
                    hits += 1
                total += 1

        hit_rate = hits / total if total > 0 else 0

        return {'hit_rate': hit_rate, 'evaluated_customers': total}

    def visualize_recommendations(self, output_dir='./recommendations_outputs'):
        """可視化推薦結果"""
        import os
        os.makedirs(output_dir, exist_ok=True)

        print("繪製推薦分析圖表...")

        fig, axes = plt.subplots(2, 2, figsize=(16, 12))
        fig.suptitle('Product Recommendation System', fontsize=16, fontweight='bold')

        # 1. 矩陣稀疏度
        ax1 = axes[0, 0]
        sparsity = (self.user_product_matrix == 0).sum().sum() / (
            self.user_product_matrix.shape[0] * self.user_product_matrix.shape[1]
        )
        ax1.text(0.5, 0.5, f'Matrix Sparsity: {sparsity:.2%}', ha='center', va='center',
                fontsize=20, bbox=dict(boxstyle='round', facecolor='wheat', alpha=0.5))
        ax1.set_title('User-Product Matrix Sparsity', fontweight='bold')
        ax1.axis('off')

        # 2. 購買分布
        ax2 = axes[0, 1]
        purchase_counts = self.user_product_matrix.sum(axis=1)
        ax2.hist(purchase_counts, bins=50, color='steelblue', edgecolor='black')
        ax2.set_title('Distribution of Purchases per Customer', fontweight='bold')
        ax2.set_xlabel('Number of Purchases')
        ax2.set_ylabel('Number of Customers')

        # 3. 商品受歡迎程度
        ax3 = axes[1, 0]
        product_popularity = self.user_product_matrix.sum(axis=0).nlargest(20)
        ax3.barh(range(len(product_popularity)), product_popularity.values)
        ax3.set_yticks([])
        ax3.set_title('Top 20 Most Popular Products', fontweight='bold')
        ax3.set_xlabel('Number of Purchases')

        # 4. 矩陣熱圖（前 20 個用戶和商品）
        ax4 = axes[1, 1]
        sample_matrix = self.user_product_matrix.iloc[:20, :20]
        sns.heatmap(sample_matrix, cmap='YlOrRd', ax=ax4, cbar_kws={'label': 'Purchase Count'})
        ax4.set_title('User-Product Matrix Sample (First 20x20)', fontweight='bold')

        plt.tight_layout()
        fig.savefig(f'{output_dir}/recommendation_analysis.png', dpi=300, bbox_inches='tight')

        return fig

    def generate_report(self, output_dir='./recommendations_outputs'):
        """生成報告"""
        import os
        os.makedirs(output_dir, exist_ok=True)

        print("\n" + "="*60)
        print("開始產品推薦系統分析")
        print("="*60 + "\n")

        # 創建矩陣
        matrix = self.create_user_product_matrix()

        # 計算相似度
        similarity = self.calculate_product_similarity()

        # 評估
        eval_results = self.evaluate_recommendations()

        # 可視化
        fig = self.visualize_recommendations(output_dir)

        # 保存
        print("\n保存分析結果...")

        # 保存示例推薦
        sample_customers = self.user_product_matrix.index[:10].tolist()
        with open(f'{output_dir}/sample_recommendations.txt', 'w', encoding='utf-8') as f:
            for customer in sample_customers:
                recs = self.generate_personalized_recommendations(customer, n_recommendations=5)
                f.write(f"\n客戶 {customer}:\n")
                if len(recs) > 0:
                    for _, product in recs.head(5).iterrows():
                        f.write(f"  - {product['product_id']}: {product['product_category_name']}\n")

        print(f"✓ 已保存到 {output_dir}/")

        return matrix, similarity, eval_results

    def print_summary(self, eval_results):
        """打印摘要"""
        print("\n" + "="*80)
        print("產品推薦系統摘要")
        print("="*80)

        print(f"\n【系統統計】")
        print(f"  用戶數: {self.user_product_matrix.shape[0]:,}")
        print(f"  商品數: {self.user_product_matrix.shape[1]:,}")
        sparsity = (self.user_product_matrix == 0).sum().sum() / (
            self.user_product_matrix.shape[0] * self.user_product_matrix.shape[1]
        )
        print(f"  矩陣稀疏度: {sparsity:.2%}")

        print(f"\n【推薦評估】")
        print(f"  評估客戶數: {eval_results['evaluated_customers']}")
        print(f"  命中率: {eval_results['hit_rate']:.2%}")


# ==================== 使用範例 ====================

if __name__ == "__main__":
    print("加載 Olist 資料...")
    orders, order_items, products, customers, sellers, payments, reviews = load_olist_data()

    # 執行分析
    engine = ProductRecommendationEngine(
        orders=orders,
        order_items=order_items,
        products=products
    )

    # 生成報告
    matrix, similarity, eval_results = engine.generate_report()

    # 打印摘要
    engine.print_summary(eval_results)

    print("\n" + "="*80)
    print("✓ 產品推薦系統分析完成！")
    print("="*80)
