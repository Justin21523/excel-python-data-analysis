"""
Report Generator Module
報表生成模組 - 產出 Excel 和 PDF 報告
"""

import pandas as pd
import numpy as np
import logging
from pathlib import Path
from datetime import datetime
import json

logger = logging.getLogger(__name__)


class ReportGenerator:
    """報表生成類"""

    def __init__(self, config):
        """
        初始化報表生成器

        Args:
            config (dict): 配置字典
        """
        self.config = config
        self.output_dir = Path(config.get('directory', 'outputs'))
        self.output_dir.mkdir(parents=True, exist_ok=True)

    def create_excel_dashboard(self, overview, products, regions, anomalies, figures=None):
        """
        建立 Excel 儀表板

        Args:
            overview (dict): 銷售總覽
            products (dict): 產品分析
            regions (dict): 地區分析
            anomalies (dict): 異常檢測
            figures (dict): 圖表字典

        Returns:
            str: 報表路徑
        """
        try:
            timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
            filename = self.output_dir / f'sales_dashboard_{timestamp}.xlsx'

            logger.info(f"建立 Excel 報表: {filename}")

            with pd.ExcelWriter(filename, engine='openpyxl') as writer:
                # 1. 摘要頁面
                self._create_summary_sheet(writer, overview)

                # 2. 銷售概覽
                self._create_sales_overview_sheet(writer, overview)

                # 3. 產品分析
                self._create_products_sheet(writer, products)

                # 4. 地區分析
                self._create_regions_sheet(writer, regions)

                # 5. 異常檢測
                self._create_anomalies_sheet(writer, anomalies)

                # 6. 詳細數據
                self._create_detailed_data_sheets(writer, overview, products, regions)

            logger.info(f"Excel 報表已生成: {filename}")
            return str(filename)

        except Exception as e:
            logger.error(f"Excel 報表生成失敗: {e}", exc_info=True)
            return None

    def _create_summary_sheet(self, writer, overview):
        """
        建立摘要工作表

        Args:
            writer: Excel 寫入器
            overview (dict): 銷售總覽
        """
        try:
            data = {
                '指標': [],
                '今日': [],
                '本週': [],
                '本月': [],
                '本年': []
            }

            metrics = ['total_revenue', 'total_orders', 'avg_order_value', 'customer_count', 'products_sold']
            metric_names = ['銷售收入', '訂單數', '平均訂單價值', '客戶數', '銷售產品數']

            for metric, name in zip(metrics, metric_names):
                data['指標'].append(name)
                data['今日'].append(overview.get('today', {}).get(metric, 0))
                data['本週'].append(overview.get('this_week', {}).get(metric, 0))
                data['本月'].append(overview.get('this_month', {}).get(metric, 0))
                data['本年'].append(overview.get('this_year', {}).get(metric, 0))

            # 成長率
            growth = overview.get('growth_rates', {})
            growth_data = {
                '指標': ['月環比成長率', '年同比成長率'],
                '數值(%)': [growth.get('month_over_month', 0), growth.get('year_over_year', 0)]
            }

            df_summary = pd.DataFrame(data)
            df_growth = pd.DataFrame(growth_data)

            # 寫入工作表
            df_summary.to_excel(writer, sheet_name='摘要', index=False)
            df_growth.to_excel(writer, sheet_name='摘要', startrow=len(df_summary) + 3, index=False)

            logger.info("摘要工作表已建立")

        except Exception as e:
            logger.error(f"摘要工作表建立失敗: {e}")

    def _create_sales_overview_sheet(self, writer, overview):
        """
        建立銷售概覽工作表

        Args:
            writer: Excel 寫入器
            overview (dict): 銷售總覽
        """
        try:
            rows = []

            # 各時期數據
            periods = {
                '今日': overview.get('today', {}),
                '本週': overview.get('this_week', {}),
                '本月': overview.get('this_month', {}),
                '本年': overview.get('this_year', {})
            }

            for period_name, metrics in periods.items():
                rows.append({
                    '時期': period_name,
                    '銷售收入': metrics.get('total_revenue', 0),
                    '訂單數': metrics.get('total_orders', 0),
                    '平均訂單價值': metrics.get('avg_order_value', 0),
                    '客戶數': metrics.get('customer_count', 0),
                    '產品數': metrics.get('products_sold', 0)
                })

            df = pd.DataFrame(rows)
            df.to_excel(writer, sheet_name='銷售概覽', index=False)

            logger.info("銷售概覽工作表已建立")

        except Exception as e:
            logger.error(f"銷售概覽工作表建立失敗: {e}")

    def _create_products_sheet(self, writer, products):
        """
        建立產品分析工作表

        Args:
            writer: Excel 寫入器
            products (dict): 產品分析
        """
        try:
            # Top 10 產品
            if 'top_10' in products and products['top_10'] is not None:
                top_10 = products['top_10']
                if not top_10.empty:
                    top_10.to_excel(writer, sheet_name='Top 10產品', index=False)

            # ABC 分類
            if 'abc_classification' in products and products['abc_classification']:
                abc_stats = products['abc_classification'].get('statistics', {})
                abc_rows = []

                for category, stats in abc_stats.items():
                    abc_rows.append({
                        '分類': category,
                        '產品數': stats.get('count', 0),
                        '銷售收入': stats.get('revenue', 0),
                        '產品數量': len(stats.get('products', []))
                    })

                df_abc = pd.DataFrame(abc_rows)
                df_abc.to_excel(writer, sheet_name='ABC分類', index=False)

            # 分類分析
            if 'category_performance' in products and products['category_performance'] is not None:
                category_perf = products['category_performance']
                if not category_perf.empty:
                    category_perf.to_excel(writer, sheet_name='分類分析', index=False)

            logger.info("產品分析工作表已建立")

        except Exception as e:
            logger.error(f"產品分析工作表建立失敗: {e}")

    def _create_regions_sheet(self, writer, regions):
        """
        建立地區分析工作表

        Args:
            writer: Excel 寫入器
            regions (dict): 地區分析
        """
        try:
            # 地區銷售
            if 'regional_sales' in regions and regions['regional_sales'] is not None:
                regional = regions['regional_sales']
                if not regional.empty:
                    regional.to_excel(writer, sheet_name='地區銷售', index=False)

            # 城市排名
            if 'city_rankings' in regions and regions['city_rankings'] is not None:
                cities = regions['city_rankings']
                if not cities.empty:
                    cities.head(20).to_excel(writer, sheet_name='城市排名', index=False)

            logger.info("地區分析工作表已建立")

        except Exception as e:
            logger.error(f"地區分析工作表建立失敗: {e}")

    def _create_anomalies_sheet(self, writer, anomalies):
        """
        建立異常檢測工作表

        Args:
            writer: Excel 寫入器
            anomalies (dict): 異常檢測
        """
        try:
            # 銷售異常
            if 'sales_anomalies' in anomalies and anomalies['sales_anomalies']:
                anomaly_data = anomalies['sales_anomalies']
                if 'anomalies' in anomaly_data and anomaly_data['anomalies']:
                    df_anomalies = pd.DataFrame(anomaly_data['anomalies'])
                    df_anomalies.to_excel(writer, sheet_name='銷售異常', index=False)
                else:
                    # 如果沒有異常，建立空表
                    df_empty = pd.DataFrame({'訊息': ['未發現銷售異常']})
                    df_empty.to_excel(writer, sheet_name='銷售異常', index=False)

            logger.info("異常檢測工作表已建立")

        except Exception as e:
            logger.error(f"異常檢測工作表建立失敗: {e}")

    def _create_detailed_data_sheets(self, writer, overview, products, regions):
        """
        建立詳細數據工作表

        Args:
            writer: Excel 寫入器
            overview (dict): 銷售總覽
            products (dict): 產品分析
            regions (dict): 地區分析
        """
        try:
            # 建立統計摘要
            summary_data = {
                '報表項目': [
                    '銷售收入',
                    '訂單數',
                    '平均訂單價值',
                    '客戶數',
                    '回購客戶比例'
                ],
                '本年數值': [
                    overview.get('this_year', {}).get('total_revenue', 0),
                    overview.get('this_year', {}).get('total_orders', 0),
                    overview.get('this_year', {}).get('avg_order_value', 0),
                    overview.get('this_year', {}).get('customer_count', 0),
                    '計算中...'
                ]
            }

            df_summary = pd.DataFrame(summary_data)
            df_summary.to_excel(writer, sheet_name='統計摘要', index=False)

            logger.info("詳細數據工作表已建立")

        except Exception as e:
            logger.error(f"詳細數據工作表建立失敗: {e}")

    def create_pdf_report(self, analyses, figures=None):
        """
        建立 PDF 報告

        Args:
            analyses (dict): 分析結果
            figures (dict): 圖表字典

        Returns:
            str: 報表路徑
        """
        try:
            timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
            filename = self.output_dir / f'sales_report_{timestamp}.pdf'

            logger.info(f"建立 PDF 報告: {filename}")

            # 嘗試使用 reportlab
            try:
                from reportlab.lib.pagesizes import letter, A4
                from reportlab.lib import colors
                from reportlab.lib.styles import getSampleStyleSheet
                from reportlab.platypus import SimpleDocTemplate, Table, TableStyle, Paragraph, Spacer, PageBreak

                doc = SimpleDocTemplate(str(filename), pagesize=A4)
                elements = []
                styles = getSampleStyleSheet()

                # 標題
                title = Paragraph("銷售智能儀表板報告", styles['Title'])
                elements.append(title)
                elements.append(Spacer(1, 0.3 * 72))

                # 生成時間
                timestamp_str = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
                elements.append(Paragraph(f"生成時間: {timestamp_str}", styles['Normal']))
                elements.append(Spacer(1, 0.3 * 72))

                # 主要指標表
                overview = analyses.get('overview', {})
                metrics = overview.get('key_metrics', {})

                table_data = [
                    ['指標', '數值'],
                    ['總收入', f"${metrics.get('total_revenue', 0):,.2f}"],
                    ['訂單數', f"{metrics.get('total_orders', 0):,}"],
                    ['平均訂單價值', f"${metrics.get('avg_order_value', 0):,.2f}"],
                    ['客戶數', f"{metrics.get('customer_count', 0):,}"]
                ]

                table = Table(table_data)
                table.setStyle(TableStyle([
                    ('BACKGROUND', (0, 0), (-1, 0), colors.grey),
                    ('TEXTCOLOR', (0, 0), (-1, 0), colors.whitesmoke),
                    ('ALIGN', (0, 0), (-1, -1), 'CENTER'),
                    ('FONTNAME', (0, 0), (-1, 0), 'Helvetica-Bold'),
                    ('FONTSIZE', (0, 0), (-1, 0), 14),
                    ('BOTTOMPADDING', (0, 0), (-1, 0), 12),
                    ('BACKGROUND', (0, 1), (-1, -1), colors.beige),
                    ('GRID', (0, 0), (-1, -1), 1, colors.black)
                ]))

                elements.append(table)
                elements.append(Spacer(1, 0.5 * 72))

                # 生成 PDF
                doc.build(elements)

                logger.info(f"PDF 報告已生成: {filename}")
                return str(filename)

            except ImportError:
                logger.warning("reportlab 模組未安裝，使用簡化 PDF 生成")
                # 使用簡化的文字報告
                return self._create_text_report(analyses)

        except Exception as e:
            logger.error(f"PDF 報告生成失敗: {e}")
            return None

    def _create_text_report(self, analyses):
        """
        建立文字報告

        Args:
            analyses (dict): 分析結果

        Returns:
            str: 報表路徑
        """
        try:
            timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
            filename = self.output_dir / f'sales_report_{timestamp}.txt'

            with open(filename, 'w', encoding='utf-8') as f:
                f.write("=" * 60 + "\n")
                f.write("銷售智能儀表板報告\n")
                f.write("=" * 60 + "\n\n")

                # 生成時間
                f.write(f"生成時間: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}\n\n")

                # 主要指標
                overview = analyses.get('overview', {})
                metrics = overview.get('key_metrics', {})

                f.write("主要指標\n")
                f.write("-" * 60 + "\n")
                f.write(f"總收入: ${metrics.get('total_revenue', 0):,.2f}\n")
                f.write(f"訂單數: {metrics.get('total_orders', 0):,}\n")
                f.write(f"平均訂單價值: ${metrics.get('avg_order_value', 0):,.2f}\n")
                f.write(f"客戶數: {metrics.get('customer_count', 0):,}\n\n")

                # 成長率
                growth = overview.get('growth_rates', {})
                f.write("成長率\n")
                f.write("-" * 60 + "\n")
                f.write(f"月環比: {growth.get('month_over_month', 0):.2f}%\n")
                f.write(f"年同比: {growth.get('year_over_year', 0):.2f}%\n\n")

                # Top 產品
                products = analyses.get('products', {})
                top_10 = products.get('top_10')
                if top_10 is not None and len(top_10) > 0:
                    f.write("Top 10 產品\n")
                    f.write("-" * 60 + "\n")
                    for idx, row in top_10.head(10).iterrows():
                        f.write(f"{row['product_id']}: ${row['total_revenue']:,.2f}\n")

            logger.info(f"文字報告已生成: {filename}")
            return str(filename)

        except Exception as e:
            logger.error(f"文字報告生成失敗: {e}")
            return None

    def generate_email_summary(self, analyses):
        """
        產生電子郵件摘要

        Args:
            analyses (dict): 分析結果

        Returns:
            str: 電子郵件內容
        """
        try:
            overview = analyses.get('overview', {})
            metrics = overview.get('key_metrics', {})
            growth = overview.get('growth_rates', {})

            email_body = f"""
銷售智能儀表板 - 每日摘要

報告時間: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}

===== 主要指標 =====
總銷售收入: ${metrics.get('total_revenue', 0):,.2f}
訂單數: {metrics.get('total_orders', 0):,}
平均訂單價值: ${metrics.get('avg_order_value', 0):,.2f}
客戶數: {metrics.get('customer_count', 0):,}

===== 成長率 =====
月環比: {growth.get('month_over_month', 0):.2f}%
年同比: {growth.get('year_over_year', 0):.2f}%

===== 備註 =====
此為自動化系統生成的報告，如有任何疑問，請聯絡數據分析團隊。
            """

            return email_body.strip()

        except Exception as e:
            logger.error(f"電子郵件摘要生成失敗: {e}")
            return None

    def export_analytics_json(self, analyses):
        """
        匯出分析結果為 JSON

        Args:
            analyses (dict): 分析結果

        Returns:
            str: 檔案路徑
        """
        try:
            timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
            filename = self.output_dir / f'analytics_{timestamp}.json'

            # 轉換 DataFrame 為字典
            data_dict = {}

            for key, value in analyses.items():
                if isinstance(value, pd.DataFrame):
                    data_dict[key] = value.to_dict('records')
                elif isinstance(value, dict):
                    data_dict[key] = value
                else:
                    data_dict[key] = str(value)

            with open(filename, 'w', encoding='utf-8') as f:
                json.dump(data_dict, f, ensure_ascii=False, indent=2, default=str)

            logger.info(f"JSON 匯出已完成: {filename}")
            return str(filename)

        except Exception as e:
            logger.error(f"JSON 匯出失敗: {e}")
            return None
