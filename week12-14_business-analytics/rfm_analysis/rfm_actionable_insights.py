"""
行動導向 RFM 分析 - Week 12
功能：
1. 基礎 RFM 分析
2. 針對各分群的行動建議
3. 客戶流失風險評估
4. 優先級排序建議
5. ROI 預估

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


class ActionableRFMAnalysis:
    """
    行動導向的 RFM 分析
    為不同客戶分群提供具體的商業行動建議
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
        self.rfm = None
        self.action_plan = None

    def calculate_rfm(self):
        """計算 RFM 指標"""
        print("計算 RFM 指標...")

        rfm = self.df.groupby(self.customer_col).agg({
            self.date_col: lambda x: (self.analysis_date - x.max()).days,
            self.customer_col: 'count',
            self.amount_col: 'sum'
        }).reset_index()

        rfm.columns = [self.customer_col, 'Recency', 'Frequency', 'Monetary']
        rfm = rfm.set_index(self.customer_col)
        rfm = rfm.replace([np.inf, -np.inf], np.nan).dropna()

        return rfm

    def assign_rfm_scores(self, rfm):
        """分配 RFM 評分"""
        print("分配 RFM 評分...")

        rfm['R_Score'] = pd.qcut(rfm['Recency'], 5, labels=[5, 4, 3, 2, 1], duplicates='drop')
        rfm['F_Score'] = pd.qcut(rfm['Frequency'].rank(method='first'), 5,
                                  labels=[1, 2, 3, 4, 5], duplicates='drop')
        rfm['M_Score'] = pd.qcut(rfm['Monetary'], 5, labels=[1, 2, 3, 4, 5], duplicates='drop')

        rfm['R_Score'] = rfm['R_Score'].astype(int)
        rfm['F_Score'] = rfm['F_Score'].astype(int)
        rfm['M_Score'] = rfm['M_Score'].astype(int)

        rfm['RFM_Score'] = (rfm['R_Score'].astype(str) +
                             rfm['F_Score'].astype(str) +
                             rfm['M_Score'].astype(str))

        return rfm

    def segment_customers(self, rfm):
        """客戶分群"""
        print("進行客戶分群...")

        def rfm_segment(row):
            r, f, m = int(row['R_Score']), int(row['F_Score']), int(row['M_Score'])

            if r >= 4 and f >= 4 and m >= 4:
                return 'Champions'
            elif f >= 4 and r >= 3:
                return 'Loyal Customers'
            elif r >= 3 and f >= 3 and m >= 3:
                return 'Potential Loyalist'
            elif r >= 4 and f >= 2 and m >= 2:
                return 'Recent Customers'
            elif r >= 3 and f >= 2 and m <= 2:
                return 'Promising'
            elif r >= 2 and f >= 2 and m >= 2:
                return 'Need Attention'
            elif r == 2 and f >= 2:
                return 'About to Sleep'
            elif f >= 3 and r <= 2:
                return 'At Risk'
            elif f >= 4 and r <= 1:
                return 'Cannot Lose Them'
            elif r <= 2 and f <= 2:
                return 'Hibernating'
            else:
                return 'Lost'

        rfm['Segment'] = rfm.apply(rfm_segment, axis=1)
        return rfm

    def define_action_strategies(self):
        """
        定義各分群的行動策略

        Returns
        -------
        dict
            包含各分群的行動建議、預期 ROI 和優先級
        """
        strategies = {
            'Champions': {
                '描述': '最有價值的客戶，頻繁購買且購買額度大',
                '風險等級': '低',
                '行動建議': [
                    '提供 VIP 會員計劃和專屬優惠',
                    '定期邀請參加新產品發布會',
                    '提供卓越的客服支持',
                    '邀請作為品牌大使提供評價',
                    '定制化營銷活動'
                ],
                '預期效果': '維持高購買率，增加客戶終身價值',
                '預期ROI': '200-300%',
                '優先級': 'P0',
                '預算投入': '高'
            },
            'Loyal Customers': {
                '描述': '忠實客戶，購買頻率高但可能最近性一般',
                '風險等級': '低',
                '行動建議': [
                    '推送新品和獨家優惠',
                    '建立會員層級制度，鼓勵升級',
                    '推薦交叉銷售和向上銷售機會',
                    '提供積分獎勵計劃',
                    '邀請提供評價和反饋'
                ],
                '預期效果': '增加購買頻率，促進客戶升級',
                '預期ROI': '150-200%',
                '優先級': 'P1',
                '預算投入': '中等'
            },
            'Potential Loyalist': {
                '描述': '有潛力的客戶，最近購買且購買頻率較穩定',
                '風險等級': '低-中',
                '行動建議': [
                    '發送歡迎和感謝信息',
                    '推送精准的產品推薦',
                    '提供限時優惠以增加購買頻率',
                    '建立會員計劃，鼓勵重複購買',
                    '邀請參加社區活動或論壇'
                ],
                '預期效果': '轉化為忠實客戶',
                '預期ROI': '100-150%',
                '優先級': 'P1',
                '預算投入': '中等'
            },
            'Recent Customers': {
                '描述': '最近購買的新客戶，需要培養成忠實客戶',
                '風險等級': '中',
                '行動建議': [
                    '發送歡迎禮物或折扣碼',
                    '請求產品評價和反饋',
                    '推送產品教程和使用技巧',
                    '提供優惠以促進下次購買',
                    '建立郵件營銷序列'
                ],
                '預期效果': '提高重複購買率',
                '預期ROI': '80-120%',
                '優先級': 'P2',
                '預算投入': '中等'
            },
            'Promising': {
                '描述': '有前景的客戶，最近購買但消費額度較低',
                '風險等級': '中',
                '行動建議': [
                    '推送高價值產品的優惠',
                    '建立購買記錄，推薦相關產品',
                    '提供購買建議和對比',
                    '發送教育性內容',
                    '定期檢查是否有額外需求'
                ],
                '預期效果': '提升客戶均價',
                '預期ROI': '60-100%',
                '優先級': 'P2',
                '預算投入': '低-中'
            },
            'Need Attention': {
                '描述': '需要關注的客戶，活躍度開始下降',
                '風險等級': '中',
                '行動建議': [
                    '發送重新連接郵件',
                    '調查購買下降原因',
                    '提供重新啟動優惠',
                    '推送最新產品和特別優惠',
                    '進行客戶滿意度調查'
                ],
                '預期效果': '重新激活客戶',
                '預期ROI': '50-80%',
                '優先級': 'P2',
                '預算投入': '低-中'
            },
            'About to Sleep': {
                '描述': '準備流失的客戶，購買頻率明顯下降',
                '風險等級': '高',
                '行動建議': [
                    '發送流失挽留郵件序列',
                    '提供特殊折扣（可能達到 20-30%）',
                    '進行電話或短信溝通',
                    '提供退貨或換貨保證',
                    '詢問反饋和改進建議'
                ],
                '預期效果': '挽留高價值流失客戶',
                '預期ROI': '40-70%',
                '優先級': 'P1',
                '預算投入': '中等'
            },
            'At Risk': {
                '描述': '高風險客戶，曾經購買頻繁但現在長期未購買',
                '風險等級': '高',
                '行動建議': [
                    '發送緊急挽留信息',
                    '提供大幅折扣（可能達到 30-40%）',
                    '提供個性化產品推薦',
                    '進行 VIP 召回活動',
                    '提供免費送貨或其他優惠'
                ],
                '預期效果': '挽留高價值客戶',
                '預期ROI': '30-60%',
                '優先級': 'P0',
                '預算投入': '高'
            },
            'Cannot Lose Them': {
                '描述': '高價值但即將流失的客戶，必須立即採取行動',
                '風險等級': '非常高',
                '行動建議': [
                    '進行高管級別的個人溝通',
                    '提供定制化的大幅優惠',
                    '提供免費升級或額外服務',
                    '進行一對一的客戶服務',
                    '調查並解決潛在問題'
                ],
                '預期效果': '保留高價值客戶',
                '預期ROI': '200-400%',
                '優先級': 'P0',
                '預算投入': '非常高'
            },
            'Hibernating': {
                '描述': '休眠客戶，長期未購買且消費額度較低',
                '風險等級': '高',
                '行動建議': [
                    '發送「我們想念你」的郵件',
                    '提供重新激活優惠',
                    '推送新產品和創新內容',
                    '進行清單清理活動',
                    '嘗試贏回但預期不高'
                ],
                '預期效果': '嘗試重新激活，預期低',
                '預期ROI': '20-40%',
                '優先級': 'P3',
                '預算投入': '低'
            },
            'Lost': {
                '描述': '已流失客戶，需要重新評估',
                '風險等級': '非常高',
                '行動建議': [
                    '定期檢查是否有重新激活機會',
                    '進行低成本的邂逅式營銷',
                    '在年度促銷中重新邀請',
                    '分析流失原因',
                    '低優先級，集中資源在其他分群'
                ],
                '預期效果': '低，集中資源在其他分群',
                '預期ROI': '5-20%',
                '優先級': 'P4',
                '預算投入': '非常低'
            }
        }
        return strategies

    def generate_action_plan(self, rfm):
        """
        生成完整的行動計劃

        Parameters
        ----------
        rfm : DataFrame
            包含分群資訊的 DataFrame

        Returns
        -------
        DataFrame
            行動計劃表
        """
        print("生成行動計劃...")

        strategies = self.define_action_strategies()

        action_plan = []
        for segment, strategy in strategies.items():
            segment_rfm = rfm[rfm['Segment'] == segment]

            action_plan.append({
                '分群': segment,
                '客戶數': len(segment_rfm),
                '佔比': f"{len(segment_rfm) / len(rfm) * 100:.2f}%",
                '總營收': segment_rfm['Monetary'].sum(),
                '營收佔比': f"{segment_rfm['Monetary'].sum() / rfm['Monetary'].sum() * 100:.2f}%",
                '平均RFM': segment_rfm[['R_Score', 'F_Score', 'M_Score']].values.mean(),
                '風險等級': strategy['風險等級'],
                '優先級': strategy['優先級'],
                '預期ROI': strategy['預期ROI'],
                '預算投入': strategy['預算投入']
            })

        action_plan_df = pd.DataFrame(action_plan)
        self.action_plan = action_plan_df
        return action_plan_df

    def get_segment_insights(self, rfm, segment):
        """
        獲取特定分群的詳細洞察

        Parameters
        ----------
        rfm : DataFrame
            RFM 資料
        segment : str
            分群名稱

        Returns
        -------
        dict
            分群洞察
        """
        segment_data = rfm[rfm['Segment'] == segment]
        strategies = self.define_action_strategies()
        strategy = strategies.get(segment, {})

        insights = {
            '客戶數': len(segment_data),
            '平均最近性': segment_data['Recency'].mean(),
            '平均頻率': segment_data['Frequency'].mean(),
            '平均金額': segment_data['Monetary'].mean(),
            '總營收': segment_data['Monetary'].sum(),
            '營收佔比': segment_data['Monetary'].sum() / rfm['Monetary'].sum() * 100,
            '客戶滿意度風險': strategy.get('風險等級', '未知'),
            '推薦行動': strategy.get('行動建議', []),
            '預期ROI': strategy.get('預期ROI', '未知')
        }

        return insights

    def visualize_action_plan(self, rfm):
        """
        視覺化行動計劃

        Parameters
        ----------
        rfm : DataFrame
            RFM 資料

        Returns
        -------
        Figure
            Matplotlib figure 物件
        """
        print("視覺化行動計劃...")

        fig, axes = plt.subplots(2, 2, figsize=(16, 12))
        fig.suptitle('Actionable RFM Insights', fontsize=16, fontweight='bold')

        # 按優先級排序
        priority_order = {'P0': 0, 'P1': 1, 'P2': 2, 'P3': 3, 'P4': 4}
        segment_priority = []
        for segment in rfm['Segment'].unique():
            segment_data = rfm[rfm['Segment'] == segment]
            strategies = self.define_action_strategies()
            priority = strategies[segment]['優先級']
            segment_priority.append({
                'segment': segment,
                'count': len(segment_data),
                'revenue': segment_data['Monetary'].sum(),
                'priority': priority,
                'priority_order': priority_order[priority],
                'risk': strategies[segment]['風險等級']
            })

        segment_priority.sort(key=lambda x: x['priority_order'])

        # 1. 優先級 vs 客戶數
        segments = [x['segment'] for x in segment_priority]
        counts = [x['count'] for x in segment_priority]
        colors1 = ['#d62728' if x['priority'] == 'P0' else
                   '#ff7f0e' if x['priority'] == 'P1' else
                   '#2ca02c' if x['priority'] == 'P2' else
                   '#1f77b4' for x in segment_priority]

        axes[0, 0].barh(segments, counts, color=colors1)
        axes[0, 0].set_title('Customer Count by Segment Priority', fontweight='bold')
        axes[0, 0].set_xlabel('Number of Customers')

        # 2. 優先級 vs 營收
        revenues = [x['revenue'] for x in segment_priority]
        axes[0, 1].barh(segments, revenues, color=colors1)
        axes[0, 1].set_title('Revenue by Segment Priority', fontweight='bold')
        axes[0, 1].set_xlabel('Total Revenue')

        # 3. 風險等級分布
        risk_dist = pd.DataFrame(segment_priority).groupby('risk').size()
        risk_colors = {'低': 'green', '低-中': 'yellow', '中': 'orange',
                       '高': 'red', '非常高': 'darkred'}
        colors3 = [risk_colors.get(risk, 'gray') for risk in risk_dist.index]
        axes[1, 0].pie(risk_dist.values, labels=risk_dist.index, autopct='%1.1f%%',
                       colors=colors3, startangle=90)
        axes[1, 0].set_title('Customer Distribution by Risk Level', fontweight='bold')

        # 4. 優先級分布
        priority_dist = pd.DataFrame(segment_priority).groupby('priority').size()
        priority_colors = {'P0': '#d62728', 'P1': '#ff7f0e',
                          'P2': '#2ca02c', 'P3': '#1f77b4', 'P4': '#9467bd'}
        colors4 = [priority_colors.get(p, 'gray') for p in priority_dist.index]
        axes[1, 1].pie(priority_dist.values, labels=priority_dist.index, autopct='%1.1f%%',
                       colors=colors4, startangle=90)
        axes[1, 1].set_title('Action Priority Distribution', fontweight='bold')

        plt.tight_layout()
        return fig

    def generate_report(self, output_dir='./rfm_actionable_outputs'):
        """
        生成完整報告

        Parameters
        ----------
        output_dir : str
            輸出目錄路徑

        Returns
        -------
        tuple
            (rfm, action_plan, figure)
        """
        import os
        os.makedirs(output_dir, exist_ok=True)

        print("\n" + "="*60)
        print("開始行動導向 RFM 分析")
        print("="*60 + "\n")

        # 計算 RFM
        rfm = self.calculate_rfm()
        rfm = self.assign_rfm_scores(rfm)
        rfm = self.segment_customers(rfm)
        self.rfm = rfm

        # 生成行動計劃
        action_plan = self.generate_action_plan(rfm)

        # 視覺化
        fig = self.visualize_action_plan(rfm)

        # 保存結果
        print("\n保存分析結果...")
        rfm.to_csv(f'{output_dir}/rfm_with_actions.csv')
        action_plan.to_csv(f'{output_dir}/action_plan.csv', index=False)
        fig.savefig(f'{output_dir}/action_insights.png', dpi=300, bbox_inches='tight')

        print(f"✓ 已保存到 {output_dir}/")

        return rfm, action_plan, fig

    def print_detailed_insights(self, rfm):
        """
        打印詳細洞察

        Parameters
        ----------
        rfm : DataFrame
            RFM 資料
        """
        print("\n" + "="*100)
        print("行動導向 RFM 分析 - 詳細洞察")
        print("="*100)

        strategies = self.define_action_strategies()

        for segment in rfm['Segment'].unique():
            insights = self.get_segment_insights(rfm, segment)
            strategy = strategies.get(segment, {})

            print(f"\n【{segment}】")
            print(f"  客戶數: {insights['客戶數']:,} ({insights['客戶數']/len(rfm)*100:.2f}%)")
            print(f"  總營收: ${insights['總營收']:,.2f} ({insights['營收佔比']:.2f}%)")
            print(f"  平均 Recency: {insights['平均最近性']:.1f} 天")
            print(f"  平均 Frequency: {insights['平均頻率']:.1f} 次")
            print(f"  平均 Monetary: ${insights['平均金額']:.2f}")
            print(f"  風險等級: {strategy.get('風險等級', '未知')}")
            print(f"  預期 ROI: {strategy.get('預期ROI', '未知')}")
            print(f"  推薦行動:")
            for i, action in enumerate(strategy.get('行動建議', []), 1):
                print(f"    {i}. {action}")


# ==================== 使用範例 ====================

if __name__ == "__main__":
    print("加載 Olist 資料...")
    orders, order_items, products, customers, sellers, payments, reviews = load_olist_data()

    print("準備交易資料...")
    transactions = orders.merge(payments, on='order_id', how='left')

    # 執行分析
    analyzer = ActionableRFMAnalysis(
        df=transactions,
        customer_col='customer_id',
        date_col='order_purchase_timestamp',
        amount_col='payment_value'
    )

    # 生成報告
    rfm, action_plan, fig = analyzer.generate_report()

    # 打印詳細洞察
    analyzer.print_detailed_insights(rfm)

    # 打印行動計劃摘要
    print("\n" + "="*100)
    print("行動計劃摘要")
    print("="*100)
    print(action_plan.to_string(index=False))

    print("\n" + "="*100)
    print("✓ 行動導向 RFM 分析完成！")
    print("="*100)
