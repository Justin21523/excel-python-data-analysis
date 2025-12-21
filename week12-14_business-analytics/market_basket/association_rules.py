"""
購物籃分析 - 關聯規則挖掘 - Week 14
功能：
1. 創建交易矩陣
2. 使用 Apriori 算法挖掘頻繁項集
3. 計算關聯規則（Support、Confidence、Lift）
4. 識別強關聯規則
5. 可視化和分析

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

try:
    from mlxtend.frequent_patterns import apriori, association_rules
    from mlxtend.preprocessing import TransactionEncoder
    MLXTEND_AVAILABLE = True
except ImportError:
    MLXTEND_AVAILABLE = False
    print("Warning: mlxtend not installed. Install with: pip install mlxtend")


class MarketBasketAnalyzer:
    """購物籃分析器"""

    def __init__(self, df, order_col, product_col):
        """
        Parameters
        ----------
        df : DataFrame
            訂單-商品資料
        order_col : str
            訂單 ID 欄位名
        product_col : str
            商品 ID 欄位名
        """
        self.df = df.copy()
        self.order_col = order_col
        self.product_col = product_col
        self.transaction_data = None
        self.frequent_itemsets = None
        self.rules = None

    def prepare_transaction_data(self):
        """準備交易資料"""
        print("準備交易資料...")

        # 每個訂單的商品列表
        transactions = self.df.groupby(self.order_col)[self.product_col].apply(list).values.tolist()

        print(f"✓ 共有 {len(transactions)} 個交易")

        # 轉換為交易矩陣
        te = TransactionEncoder()
        te_ary = te.fit(transactions).transform(transactions)
        transaction_matrix = pd.DataFrame(te_ary, columns=te.columns_)

        self.transaction_data = transaction_matrix

        return transaction_matrix

    def find_frequent_itemsets(self, min_support=0.01):
        """尋找頻繁項集"""
        print(f"尋找頻繁項集 (min_support={min_support})...")

        frequent_itemsets = apriori(
            self.transaction_data,
            min_support=min_support,
            use_colnames=True,
            max_len=3  # 最多 3 個項的組合
        )

        # 添加項數欄位
        frequent_itemsets['length'] = frequent_itemsets['itemsets'].apply(lambda x: len(x))

        # 排序
        frequent_itemsets = frequent_itemsets.sort_values('support', ascending=False)

        self.frequent_itemsets = frequent_itemsets

        print(f"✓ 找到 {len(frequent_itemsets)} 個頻繁項集")

        return frequent_itemsets

    def generate_association_rules(self, min_confidence=0.3, metric='confidence'):
        """生成關聯規則"""
        print(f"生成關聯規則 (min_confidence={min_confidence})...")

        if self.frequent_itemsets is None or len(self.frequent_itemsets) == 0:
            print("警告：沒有找到頻繁項集")
            return pd.DataFrame()

        rules = association_rules(
            self.frequent_itemsets,
            metric=metric,
            min_threshold=min_confidence
        )

        if len(rules) > 0:
            # 轉換為字符串表示
            rules['antecedents'] = rules['antecedents'].apply(lambda x: ','.join(list(x)))
            rules['consequents'] = rules['consequents'].apply(lambda x: ','.join(list(x)))

            # 排序
            rules = rules.sort_values('lift', ascending=False)

        self.rules = rules

        print(f"✓ 生成了 {len(rules)} 條規則")

        return rules

    def get_strong_rules(self, min_lift=1.2, min_confidence=0.5):
        """獲取強規則"""
        print(f"篩選強規則 (min_lift={min_lift}, min_confidence={min_confidence})...")

        if self.rules is None or len(self.rules) == 0:
            return pd.DataFrame()

        strong_rules = self.rules[
            (self.rules['lift'] >= min_lift) &
            (self.rules['confidence'] >= min_confidence)
        ].sort_values('lift', ascending=False)

        print(f"✓ 找到 {len(strong_rules)} 條強規則")

        return strong_rules

    def visualize_rules(self, rules, output_dir='./basket_outputs'):
        """可視化規則"""
        import os
        os.makedirs(output_dir, exist_ok=True)

        print("繪製規則分析圖表...")

        if len(rules) == 0:
            print("警告：沒有規則可視化")
            return None

        fig, axes = plt.subplots(2, 2, figsize=(16, 12))
        fig.suptitle('Association Rules Analysis', fontsize=16, fontweight='bold')

        # 限制規則數量用於可視化
        viz_rules = rules.head(20)

        # 1. Support vs Confidence
        ax1 = axes[0, 0]
        scatter = ax1.scatter(viz_rules['support'], viz_rules['confidence'],
                             s=viz_rules['lift']*100, c=viz_rules['lift'],
                             cmap='viridis', alpha=0.6)
        ax1.set_title('Support vs Confidence', fontweight='bold')
        ax1.set_xlabel('Support')
        ax1.set_ylabel('Confidence')
        plt.colorbar(scatter, ax=ax1, label='Lift')

        # 2. Lift 分布
        ax2 = axes[0, 1]
        ax2.hist(rules['lift'], bins=30, color='steelblue', edgecolor='black')
        ax2.axvline(rules['lift'].mean(), color='red', linestyle='--', linewidth=2)
        ax2.set_title('Distribution of Lift', fontweight='bold')
        ax2.set_xlabel('Lift')
        ax2.set_ylabel('Count')

        # 3. Support vs Lift
        ax3 = axes[1, 0]
        scatter2 = ax3.scatter(viz_rules['support'], viz_rules['lift'],
                              s=100, c=viz_rules['confidence'],
                              cmap='plasma', alpha=0.6)
        ax3.set_title('Support vs Lift', fontweight='bold')
        ax3.set_xlabel('Support')
        ax3.set_ylabel('Lift')
        plt.colorbar(scatter2, ax=ax3, label='Confidence')

        # 4. 前 10 條規則（按 Lift）
        ax4 = axes[1, 1]
        top_rules = rules.head(10)
        rule_labels = [f"{r['antecedents']}\n→\n{r['consequents']}"
                      for _, r in top_rules.iterrows()]
        ax4.barh(range(len(top_rules)), top_rules['lift'], color='coral')
        ax4.set_yticks(range(len(top_rules)))
        ax4.set_yticklabels(rule_labels, fontsize=8)
        ax4.set_title('Top 10 Rules by Lift', fontweight='bold')
        ax4.set_xlabel('Lift')

        plt.tight_layout()
        fig.savefig(f'{output_dir}/association_rules_analysis.png', dpi=300, bbox_inches='tight')

        return fig

    def generate_report(self, output_dir='./basket_outputs', min_support=0.01,
                       min_confidence=0.3, min_lift=1.2):
        """生成完整報告"""
        import os
        os.makedirs(output_dir, exist_ok=True)

        if not MLXTEND_AVAILABLE:
            print("Error: mlxtend library not available. Install with: pip install mlxtend")
            return None, None, None

        print("\n" + "="*60)
        print("開始購物籃關聯規則分析")
        print("="*60 + "\n")

        # 準備資料
        transaction_data = self.prepare_transaction_data()

        # 尋找頻繁項集
        frequent_itemsets = self.find_frequent_itemsets(min_support=min_support)

        # 生成規則
        rules = self.generate_association_rules(min_confidence=min_confidence)

        # 強規則
        strong_rules = self.get_strong_rules(min_lift=min_lift, min_confidence=min_confidence)

        # 可視化
        fig = self.visualize_rules(strong_rules, output_dir)

        # 保存
        print("\n保存分析結果...")
        if len(rules) > 0:
            rules.to_csv(f'{output_dir}/association_rules.csv', index=False)
        if len(strong_rules) > 0:
            strong_rules.to_csv(f'{output_dir}/strong_association_rules.csv', index=False)

        frequent_itemsets.to_csv(f'{output_dir}/frequent_itemsets.csv', index=False)

        print(f"✓ 已保存到 {output_dir}/")

        return frequent_itemsets, rules, strong_rules

    def print_summary(self, rules, strong_rules):
        """打印摘要"""
        print("\n" + "="*80)
        print("購物籃關聯規則分析摘要")
        print("="*80)

        print(f"\n【規則統計】")
        print(f"  所有規則數: {len(rules)}")
        print(f"  強規則數: {len(strong_rules)}")

        if len(rules) > 0:
            print(f"\n【規則質量指標】")
            print(f"  平均 Support: {rules['support'].mean():.4f}")
            print(f"  平均 Confidence: {rules['confidence'].mean():.4f}")
            print(f"  平均 Lift: {rules['lift'].mean():.4f}")

        if len(strong_rules) > 0:
            print(f"\n【強規則示例（前 5 條）】")
            for idx, rule in strong_rules.head(5).iterrows():
                print(f"  {rule['antecedents']} → {rule['consequents']}")
                print(f"    Support: {rule['support']:.4f}, Confidence: {rule['confidence']:.4f}, Lift: {rule['lift']:.4f}")


# ==================== 使用範例 ====================

if __name__ == "__main__":
    if not MLXTEND_AVAILABLE:
        print("Please install mlxtend: pip install mlxtend")
        sys.exit(1)

    print("加載 Olist 資料...")
    orders, order_items, products, customers, sellers, payments, reviews = load_olist_data()

    # 執行分析
    analyzer = MarketBasketAnalyzer(
        df=order_items,
        order_col='order_id',
        product_col='product_id'
    )

    # 生成報告
    frequent_itemsets, rules, strong_rules = analyzer.generate_report(
        min_support=0.01,
        min_confidence=0.3,
        min_lift=1.2
    )

    # 打印摘要
    if rules is not None:
        analyzer.print_summary(rules, strong_rules)

    print("\n" + "="*80)
    print("✓ 購物籃關聯規則分析完成！")
    print("="*80)
