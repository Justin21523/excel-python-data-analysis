"""
Customer Report Generator Module
客戶報告生成模組
"""

import pandas as pd
import numpy as np
import logging
from pathlib import Path
from datetime import datetime
import json

logger = logging.getLogger(__name__)


class CustomerReportGenerator:
    """客戶報告生成類"""

    def __init__(self, config):
        """初始化"""
        self.config = config
        self.output_dir = Path(config.get('directory', 'outputs'))
        self.output_dir.mkdir(parents=True, exist_ok=True)

    def create_customer_report(self, analyses):
        """
        建立客戶洞察 Excel 報告

        Args:
            analyses (dict): 分析結果

        Returns:
            str: 報告路徑
        """
        try:
            timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
            filename = self.output_dir / f'customer_insights_{timestamp}.xlsx'

            logger.info(f"建立 Excel 報告: {filename}")

            with pd.ExcelWriter(filename, engine='openpyxl') as writer:
                # 1. RFM 分析
                self._write_rfm_sheet(writer, analyses.get('rfm', {}))

                # 2. CLV 分析
                self._write_clv_sheet(writer, analyses.get('clv', {}))

                # 3. 群組分析
                self._write_cohort_sheet(writer, analyses.get('cohort', {}))

                # 4. 行為分析
                self._write_behavior_sheet(writer, analyses.get('behavior', {}))

                # 5. 推薦
                self._write_recommendations_sheet(writer, analyses.get('recommendations', {}))

                # 6. 客戶分類
                self._write_segments_sheet(writer, analyses.get('segments', {}))

                # 7. 摘要
                self._write_summary_sheet(writer, analyses)

            logger.info(f"Excel 報告已生成: {filename}")
            return str(filename)

        except Exception as e:
            logger.error(f"Excel 報告生成失敗: {e}")
            return None

    def _write_rfm_sheet(self, writer, rfm_data):
        """寫入 RFM 工作表"""
        try:
            if not rfm_data or 'scores' not in rfm_data:
                return

            scores = rfm_data['scores']
            if isinstance(scores, pd.DataFrame):
                scores.to_excel(writer, sheet_name='RFM分析', index=False)
                logger.info("RFM 工作表已寫入")
        except Exception as e:
            logger.error(f"RFM 工作表寫入失敗: {e}")

    def _write_clv_sheet(self, writer, clv_data):
        """寫入 CLV 工作表"""
        try:
            if not clv_data or 'customer_clv' not in clv_data:
                return

            clv_df = clv_data['customer_clv']
            if isinstance(clv_df, pd.DataFrame):
                # 選擇主要列進行展示
                display_cols = ['customer_id', 'frequency', 'total_spent',
                               'avg_purchase_value', 'clv_simple', 'clv_discounted']
                available_cols = [col for col in display_cols if col in clv_df.columns]

                if available_cols:
                    clv_df[available_cols].to_excel(writer, sheet_name='CLV分析', index=False)
                    logger.info("CLV 工作表已寫入")
        except Exception as e:
            logger.error(f"CLV 工作表寫入失敗: {e}")

    def _write_cohort_sheet(self, writer, cohort_data):
        """寫入群組工作表"""
        try:
            if not cohort_data:
                return

            # 寫入群組表
            if 'cohort_table' in cohort_data:
                cohort_table = cohort_data['cohort_table']
                if isinstance(cohort_table, dict) and 'customer_count' in cohort_table:
                    customer_counts = cohort_table['customer_count']
                    if isinstance(customer_counts, pd.DataFrame):
                        customer_counts.to_excel(writer, sheet_name='群組分析')
                        logger.info("群組工作表已寫入")
        except Exception as e:
            logger.error(f"群組工作表寫入失敗: {e}")

    def _write_behavior_sheet(self, writer, behavior_data):
        """寫入行為工作表"""
        try:
            if not behavior_data:
                return

            rows = []

            # 購買模式
            if 'purchase_patterns' in behavior_data:
                patterns = behavior_data['purchase_patterns']
                if 'frequency_distribution' in patterns:
                    freq = patterns['frequency_distribution']
                    rows.append({
                        '指標': '一次性購買客戶',
                        '數值': freq.get('one_time', 0)
                    })
                    rows.append({
                        '指標': '重複購買客戶',
                        '數值': freq.get('repeat', 0)
                    })

            # 流失風險
            if 'churn_risk' in behavior_data:
                churn = behavior_data['churn_risk']
                rows.append({
                    '指標': '流失客戶數',
                    '數值': churn.get('churned_customers', 0)
                })
                rows.append({
                    '指標': '風險客戶數',
                    '數值': churn.get('at_risk_customers', 0)
                })

            if rows:
                df = pd.DataFrame(rows)
                df.to_excel(writer, sheet_name='行為分析', index=False)
                logger.info("行為工作表已寫入")

        except Exception as e:
            logger.error(f"行為工作表寫入失敗: {e}")

    def _write_recommendations_sheet(self, writer, recommendations):
        """寫入推薦工作表"""
        try:
            if not recommendations:
                return

            rows = []

            for campaign_type, data in recommendations.items():
                if isinstance(data, dict):
                    if 'target_count' in data:
                        rows.append({
                            '活動': campaign_type,
                            '目標客戶數': data.get('target_count', 0),
                            '狀態': '計劃中'
                        })

            if rows:
                df = pd.DataFrame(rows)
                df.to_excel(writer, sheet_name='推薦活動', index=False)
                logger.info("推薦工作表已寫入")

        except Exception as e:
            logger.error(f"推薦工作表寫入失敗: {e}")

    def _write_segments_sheet(self, writer, segments):
        """寫入客戶分類工作表"""
        try:
            if not segments:
                return

            rows = []

            for segment_type, data in segments.items():
                if isinstance(data, dict) and 'count' in data:
                    rows.append({
                        '分類': segment_type,
                        '客戶數': data.get('count', 0),
                        '佔比': f"{data.get('count', 0) / max(1, sum(d.get('count', 0) for d in segments.values())) * 100:.1f}%"
                    })

            if rows:
                df = pd.DataFrame(rows)
                df.to_excel(writer, sheet_name='客戶分類', index=False)
                logger.info("分類工作表已寫入")

        except Exception as e:
            logger.error(f"分類工作表寫入失敗: {e}")

    def _write_summary_sheet(self, writer, analyses):
        """寫入摘要工作表"""
        try:
            summary_rows = []

            # RFM 摘要
            rfm = analyses.get('rfm', {})
            if rfm and 'scores' in rfm:
                scores = rfm['scores']
                if isinstance(scores, pd.DataFrame):
                    summary_rows.append(['RFM分析', '', ''])
                    summary_rows.append(['總客戶數', len(scores), ''])

            # CLV 摘要
            clv = analyses.get('clv', {})
            if clv and 'customer_clv' in clv:
                clv_df = clv['customer_clv']
                if isinstance(clv_df, pd.DataFrame) and 'clv_discounted' in clv_df.columns:
                    summary_rows.append(['CLV分析', '', ''])
                    summary_rows.append(['平均CLV', f"${clv_df['clv_discounted'].mean():.2f}", ''])
                    summary_rows.append(['總CLV', f"${clv_df['clv_discounted'].sum():.2f}", ''])

            # 行為摘要
            behavior = analyses.get('behavior', {})
            churn_risk = behavior.get('churn_risk', {})
            if churn_risk:
                summary_rows.append(['行為分析', '', ''])
                summary_rows.append(['流失率', f"{churn_risk.get('churn_rate', 0):.1f}%", ''])
                summary_rows.append(['風險率', f"{churn_risk.get('at_risk_rate', 0):.1f}%", ''])

            if summary_rows:
                df = pd.DataFrame(summary_rows, columns=['指標', '數值', '備註'])
                df.to_excel(writer, sheet_name='摘要', index=False)
                logger.info("摘要工作表已寫入")

        except Exception as e:
            logger.error(f"摘要工作表寫入失敗: {e}")

    def create_pdf_report(self, analyses):
        """
        建立 PDF 報告

        Args:
            analyses (dict): 分析結果

        Returns:
            str: 報告路徑
        """
        try:
            timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
            filename = self.output_dir / f'customer_report_{timestamp}.txt'

            logger.info(f"建立文字報告: {filename}")

            with open(filename, 'w', encoding='utf-8') as f:
                f.write("=" * 60 + "\n")
                f.write("客戶洞察分析報告\n")
                f.write("=" * 60 + "\n\n")

                f.write(f"生成時間: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}\n\n")

                # RFM 分析摘要
                f.write("RFM 分析\n")
                f.write("-" * 60 + "\n")
                rfm = analyses.get('rfm', {})
                if rfm and 'scores' in rfm:
                    scores = rfm['scores']
                    if isinstance(scores, pd.DataFrame):
                        f.write(f"客戶總數: {len(scores)}\n")
                        if 'rfm_score' in scores.columns:
                            f.write(f"平均 RFM 分數: {scores['rfm_score'].mean():.2f}\n")
                f.write("\n")

                # CLV 分析摘要
                f.write("客戶終身價值（CLV）\n")
                f.write("-" * 60 + "\n")
                clv = analyses.get('clv', {})
                if clv and 'customer_clv' in clv:
                    clv_df = clv['customer_clv']
                    if isinstance(clv_df, pd.DataFrame) and 'clv_discounted' in clv_df.columns:
                        f.write(f"平均 CLV: ${clv_df['clv_discounted'].mean():.2f}\n")
                        f.write(f"總 CLV: ${clv_df['clv_discounted'].sum():.2f}\n")
                f.write("\n")

                # 行為分析摘要
                f.write("行為分析\n")
                f.write("-" * 60 + "\n")
                behavior = analyses.get('behavior', {})
                churn_risk = behavior.get('churn_risk', {})
                if churn_risk:
                    f.write(f"流失客戶: {churn_risk.get('churned_customers', 0)}\n")
                    f.write(f"風險客戶: {churn_risk.get('at_risk_customers', 0)}\n")
                    f.write(f"流失率: {churn_risk.get('churn_rate', 0):.1f}%\n")
                f.write("\n")

                # 推薦摘要
                f.write("推薦活動\n")
                f.write("-" * 60 + "\n")
                recommendations = analyses.get('recommendations', {})
                if recommendations:
                    for campaign, data in recommendations.items():
                        if isinstance(data, dict) and 'target_count' in data:
                            f.write(f"{campaign}: {data['target_count']} 個客戶\n")

            logger.info(f"文字報告已生成: {filename}")
            return str(filename)

        except Exception as e:
            logger.error(f"PDF 報告生成失敗: {e}")
            return None

    def export_json_report(self, analyses):
        """
        匯出 JSON 報告

        Args:
            analyses (dict): 分析結果

        Returns:
            str: 報告路徑
        """
        try:
            timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
            filename = self.output_dir / f'customer_insights_{timestamp}.json'

            logger.info(f"匯出 JSON 報告: {filename}")

            # 轉換為可序列化的格式
            json_data = {}

            for key, value in analyses.items():
                if isinstance(value, pd.DataFrame):
                    json_data[key] = value.to_dict('records')
                elif isinstance(value, dict):
                    json_data[key] = value
                else:
                    json_data[key] = str(value)

            with open(filename, 'w', encoding='utf-8') as f:
                json.dump(json_data, f, ensure_ascii=False, indent=2, default=str)

            logger.info(f"JSON 報告已生成: {filename}")
            return str(filename)

        except Exception as e:
            logger.error(f"JSON 報告生成失敗: {e}")
            return None
