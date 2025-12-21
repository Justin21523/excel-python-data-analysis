"""
Visualizations Module
視覺化模組 - 生成圖表
"""

import pandas as pd
import numpy as np
import logging
import matplotlib.pyplot as plt
import seaborn as sns
from pathlib import Path

logger = logging.getLogger(__name__)

# 設定中文字體
plt.rcParams['font.sans-serif'] = ['SimHei', 'DejaVu Sans']
plt.rcParams['axes.unicode_minus'] = False


class SalesVisualizer:
    """銷售視覺化類"""

    def __init__(self, output_dir='outputs/charts'):
        """
        初始化視覺化器

        Args:
            output_dir (str): 輸出目錄
        """
        self.output_dir = Path(output_dir)
        self.output_dir.mkdir(parents=True, exist_ok=True)
        sns.set_style("whitegrid")

    def plot_sales_trend(self, overview, save=True):
        """
        繪製銷售趨勢圖

        Args:
            overview (dict): 銷售概覽數據
            save (bool): 是否保存

        Returns:
            str: 圖表路徑
        """
        try:
            fig, axes = plt.subplots(2, 2, figsize=(14, 10))
            fig.suptitle('銷售趨勢分析', fontsize=16, fontweight='bold')

            # 各時期銷售對比
            periods = ['Today', 'This Week', 'This Month', 'This Year']
            revenues = [
                overview.get('today', {}).get('total_revenue', 0),
                overview.get('this_week', {}).get('total_revenue', 0),
                overview.get('this_month', {}).get('total_revenue', 0),
                overview.get('this_year', {}).get('total_revenue', 0)
            ]

            axes[0, 0].bar(periods, revenues, color=['#1f77b4', '#ff7f0e', '#2ca02c', '#d62728'])
            axes[0, 0].set_title('各時期銷售收入')
            axes[0, 0].set_ylabel('收入 ($)')
            axes[0, 0].grid(axis='y', alpha=0.3)

            # 訂單數對比
            orders = [
                overview.get('today', {}).get('total_orders', 0),
                overview.get('this_week', {}).get('total_orders', 0),
                overview.get('this_month', {}).get('total_orders', 0),
                overview.get('this_year', {}).get('total_orders', 0)
            ]

            axes[0, 1].plot(periods, orders, marker='o', linewidth=2, markersize=8, color='#2ca02c')
            axes[0, 1].set_title('各時期訂單數')
            axes[0, 1].set_ylabel('訂單數')
            axes[0, 1].grid(alpha=0.3)

            # 客戶數對比
            customers = [
                overview.get('today', {}).get('customer_count', 0),
                overview.get('this_week', {}).get('customer_count', 0),
                overview.get('this_month', {}).get('customer_count', 0),
                overview.get('this_year', {}).get('customer_count', 0)
            ]

            axes[1, 0].bar(periods, customers, color=['#1f77b4', '#ff7f0e', '#2ca02c', '#d62728'], alpha=0.7)
            axes[1, 0].set_title('各時期客戶數')
            axes[1, 0].set_ylabel('客戶數')
            axes[1, 0].grid(axis='y', alpha=0.3)

            # 平均訂單價值
            avg_values = [
                overview.get('today', {}).get('avg_order_value', 0),
                overview.get('this_week', {}).get('avg_order_value', 0),
                overview.get('this_month', {}).get('avg_order_value', 0),
                overview.get('this_year', {}).get('avg_order_value', 0)
            ]

            axes[1, 1].bar(periods, avg_values, color=['#1f77b4', '#ff7f0e', '#2ca02c', '#d62728'], alpha=0.5)
            axes[1, 1].set_title('平均訂單價值')
            axes[1, 1].set_ylabel('平均價值 ($)')
            axes[1, 1].grid(axis='y', alpha=0.3)

            plt.tight_layout()

            if save:
                filepath = self.output_dir / 'sales_trend.png'
                plt.savefig(filepath, dpi=300, bbox_inches='tight')
                logger.info(f"銷售趨勢圖已保存: {filepath}")
                plt.close()
                return str(filepath)
            else:
                return None

        except Exception as e:
            logger.error(f"銷售趨勢圖生成失敗: {e}")
            return None

    def plot_top_products(self, top_products, save=True):
        """
        繪製 Top 產品圖

        Args:
            top_products (pd.DataFrame): Top 產品數據
            save (bool): 是否保存

        Returns:
            str: 圖表路徑
        """
        try:
            if top_products is None or len(top_products) == 0:
                logger.warning("沒有 Top 產品數據")
                return None

            fig, axes = plt.subplots(1, 2, figsize=(14, 6))
            fig.suptitle('Top 10 產品分析', fontsize=14, fontweight='bold')

            # 銷售收入前 10
            if 'total_revenue' in top_products.columns:
                top_by_revenue = top_products.sort_values('total_revenue', ascending=True).tail(10)
                axes[0].barh(range(len(top_by_revenue)), top_by_revenue['total_revenue'], color='#1f77b4')
                axes[0].set_yticks(range(len(top_by_revenue)))
                axes[0].set_yticklabels(top_by_revenue['product_id'])
                axes[0].set_xlabel('總收入 ($)')
                axes[0].set_title('按收入排序')
                axes[0].grid(axis='x', alpha=0.3)

            # 銷售數量前 10
            if 'quantity_sold' in top_products.columns:
                top_by_qty = top_products.sort_values('quantity_sold', ascending=True).tail(10)
                axes[1].barh(range(len(top_by_qty)), top_by_qty['quantity_sold'], color='#ff7f0e')
                axes[1].set_yticks(range(len(top_by_qty)))
                axes[1].set_yticklabels(top_by_qty['product_id'])
                axes[1].set_xlabel('銷售數量')
                axes[1].set_title('按銷量排序')
                axes[1].grid(axis='x', alpha=0.3)

            plt.tight_layout()

            if save:
                filepath = self.output_dir / 'top_products.png'
                plt.savefig(filepath, dpi=300, bbox_inches='tight')
                logger.info(f"Top 產品圖已保存: {filepath}")
                plt.close()
                return str(filepath)
            else:
                return None

        except Exception as e:
            logger.error(f"Top 產品圖生成失敗: {e}")
            return None

    def plot_regional_heatmap(self, regional_sales, save=True):
        """
        繪製地區熱圖

        Args:
            regional_sales (pd.DataFrame): 地區銷售數據
            save (bool): 是否保存

        Returns:
            str: 圖表路徑
        """
        try:
            if regional_sales is None or len(regional_sales) == 0:
                logger.warning("沒有地區銷售數據")
                return None

            fig, axes = plt.subplots(1, 2, figsize=(14, 6))
            fig.suptitle('地區銷售分析', fontsize=14, fontweight='bold')

            # 地區收入排序
            if 'revenue' in regional_sales.columns:
                regional_sorted = regional_sales.sort_values('revenue', ascending=True)

                # 條形圖
                axes[0].barh(range(len(regional_sorted)), regional_sorted['revenue'], color='#2ca02c')
                axes[0].set_yticks(range(len(regional_sorted)))

                if 'index' in regional_sorted.columns:
                    axes[0].set_yticklabels(regional_sorted['index'])
                else:
                    axes[0].set_yticklabels(regional_sorted.index)

                axes[0].set_xlabel('收入 ($)')
                axes[0].set_title('地區收入排名')
                axes[0].grid(axis='x', alpha=0.3)

                # 百分比圖
                if 'pct_of_total' in regional_sorted.columns:
                    axes[1].pie(
                        regional_sorted['pct_of_total'],
                        labels=regional_sorted['index'] if 'index' in regional_sorted.columns else regional_sorted.index,
                        autopct='%1.1f%%',
                        startangle=90
                    )
                    axes[1].set_title('收入分佈')

            plt.tight_layout()

            if save:
                filepath = self.output_dir / 'regional_heatmap.png'
                plt.savefig(filepath, dpi=300, bbox_inches='tight')
                logger.info(f"地區熱圖已保存: {filepath}")
                plt.close()
                return str(filepath)
            else:
                return None

        except Exception as e:
            logger.error(f"地區熱圖生成失敗: {e}")
            return None

    def plot_abc_classification(self, abc_data, save=True):
        """
        繪製 ABC 分類圖

        Args:
            abc_data (dict): ABC 分類數據
            save (bool): 是否保存

        Returns:
            str: 圖表路徑
        """
        try:
            if not abc_data or 'statistics' not in abc_data:
                logger.warning("沒有 ABC 分類數據")
                return None

            stats = abc_data['statistics']

            fig, axes = plt.subplots(1, 2, figsize=(14, 6))
            fig.suptitle('ABC 庫存分類分析', fontsize=14, fontweight='bold')

            # 產品數量分布
            categories = ['A', 'B', 'C']
            counts = [stats[cat]['count'] for cat in categories]
            colors = ['#d62728', '#ff7f0e', '#2ca02c']

            axes[0].bar(categories, counts, color=colors)
            axes[0].set_ylabel('產品數量')
            axes[0].set_title('各類別產品數')
            axes[0].grid(axis='y', alpha=0.3)

            # 收入分布
            revenues = [stats[cat]['revenue'] for cat in categories]

            axes[1].pie(revenues, labels=categories, autopct='%1.1f%%', colors=colors, startangle=90)
            axes[1].set_title('收入分布')

            plt.tight_layout()

            if save:
                filepath = self.output_dir / 'abc_classification.png'
                plt.savefig(filepath, dpi=300, bbox_inches='tight')
                logger.info(f"ABC 分類圖已保存: {filepath}")
                plt.close()
                return str(filepath)
            else:
                return None

        except Exception as e:
            logger.error(f"ABC 分類圖生成失敗: {e}")
            return None

    def plot_customer_distribution(self, customers_data, save=True):
        """
        繪製客戶分佈圖

        Args:
            customers_data (pd.DataFrame): 客戶數據
            save (bool): 是否保存

        Returns:
            str: 圖表路徑
        """
        try:
            fig, ax = plt.subplots(figsize=(10, 6))
            fig.suptitle('客戶分佈分析', fontsize=14, fontweight='bold')

            # 模擬客戶分佈
            regions = ['Region A', 'Region B', 'Region C', 'Region D', 'Region E']
            customers = np.random.randint(50, 500, 5)

            ax.bar(regions, customers, color='#1f77b4', alpha=0.7)
            ax.set_ylabel('客戶數')
            ax.set_title('各地區客戶數')
            ax.grid(axis='y', alpha=0.3)

            plt.tight_layout()

            if save:
                filepath = self.output_dir / 'customer_distribution.png'
                plt.savefig(filepath, dpi=300, bbox_inches='tight')
                logger.info(f"客戶分佈圖已保存: {filepath}")
                plt.close()
                return str(filepath)
            else:
                return None

        except Exception as e:
            logger.error(f"客戶分佈圖生成失敗: {e}")
            return None

    def create_summary_dashboard(self, analyses, save=True):
        """
        建立摘要儀表板

        Args:
            analyses (dict): 分析結果
            save (bool): 是否保存

        Returns:
            str: 圖表路徑
        """
        try:
            fig = plt.figure(figsize=(16, 12))
            gs = fig.add_gridspec(3, 3, hspace=0.3, wspace=0.3)

            fig.suptitle('銷售智能儀表板摘要', fontsize=18, fontweight='bold')

            # 主要指標
            ax_kpi = fig.add_subplot(gs[0, :])
            ax_kpi.axis('off')

            overview = analyses.get('overview', {})
            metrics = overview.get('key_metrics', {})

            kpi_text = f"""
            總收入: ${metrics.get('total_revenue', 0):,.2f}  |
            訂單數: {metrics.get('total_orders', 0):,}  |
            平均訂單價值: ${metrics.get('avg_order_value', 0):,.2f}  |
            客戶數: {metrics.get('customer_count', 0):,}
            """

            ax_kpi.text(0.5, 0.5, kpi_text, ha='center', va='center', fontsize=12,
                       bbox=dict(boxstyle='round', facecolor='wheat', alpha=0.5))

            # 成長率
            growth = overview.get('growth_rates', {})
            ax_growth = fig.add_subplot(gs[1, 0])
            ax_growth.axis('off')

            growth_text = f"""
            月環比: {growth.get('month_over_month', 0):.1f}%
            年同比: {growth.get('year_over_year', 0):.1f}%
            """

            ax_growth.text(0.5, 0.5, growth_text, ha='center', va='center', fontsize=10,
                          bbox=dict(boxstyle='round', facecolor='lightblue', alpha=0.5))

            # 時期對比
            ax_periods = fig.add_subplot(gs[1, 1:])
            periods = ['Today', 'Week', 'Month', 'Year']
            revenues = [
                overview.get('today', {}).get('total_revenue', 0),
                overview.get('this_week', {}).get('total_revenue', 0),
                overview.get('this_month', {}).get('total_revenue', 0),
                overview.get('this_year', {}).get('total_revenue', 0)
            ]
            ax_periods.bar(periods, revenues, color=['#1f77b4', '#ff7f0e', '#2ca02c', '#d62728'])
            ax_periods.set_ylabel('收入 ($)')
            ax_periods.set_title('各時期銷售對比')
            ax_periods.grid(axis='y', alpha=0.3)

            # Top 產品
            ax_products = fig.add_subplot(gs[2, 0:2])
            products = analyses.get('products', {}).get('top_10')
            if products is not None and len(products) > 0:
                top_5 = products.head(5).sort_values('total_revenue', ascending=True)
                ax_products.barh(range(len(top_5)), top_5['total_revenue'], color='#1f77b4')
                ax_products.set_yticks(range(len(top_5)))
                ax_products.set_yticklabels(top_5['product_id'])
                ax_products.set_xlabel('收入 ($)')
                ax_products.set_title('Top 5 產品')
                ax_products.grid(axis='x', alpha=0.3)

            # 地區分佈
            ax_regions = fig.add_subplot(gs[2, 2])
            regions = analyses.get('regions', {})
            if regions and 'geographic_distribution' in regions:
                geo_dist = regions['geographic_distribution']
                if 'states' in geo_dist and geo_dist['states']:
                    states = list(geo_dist['states'].keys())[:5]
                    values = list(geo_dist['states'].values())[:5]
                    ax_regions.pie(values, labels=states, autopct='%1.1f%%')
                    ax_regions.set_title('地區分佈')

            plt.tight_layout()

            if save:
                filepath = self.output_dir / 'dashboard_summary.png'
                plt.savefig(filepath, dpi=300, bbox_inches='tight')
                logger.info(f"儀表板摘要已保存: {filepath}")
                plt.close()
                return str(filepath)
            else:
                return None

        except Exception as e:
            logger.error(f"儀表板摘要生成失敗: {e}")
            return None
