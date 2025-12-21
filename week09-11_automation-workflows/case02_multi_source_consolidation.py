"""
案例2：多來源資料整合系統

功能概述：
- 支援多個資料源：API、資料庫、檔案系統、Web Scraping
- 統一的資料擷取介面
- 來源優先級管理
- 資料去重與衝突解決
- 增量更新支援
- 完整的轉換和對應

執行方式：
    python case02_multi_source_consolidation.py

作者：Data Engineering Team
版本：1.0.0
"""

import pandas as pd
import numpy as np
import logging
import sqlite3
import json
import requests
from pathlib import Path
from datetime import datetime, timedelta
from typing import Dict, List, Tuple, Optional, Any
from abc import ABC, abstractmethod
from dataclasses import dataclass, field, asdict
import hashlib
from enum import Enum
import re


# ============================================================================
# 日誌配置
# ============================================================================

def setup_logging(log_dir: str = "./logs") -> logging.Logger:
    """設定日誌系統"""
    Path(log_dir).mkdir(exist_ok=True)

    logger = logging.getLogger("MultiSourceConsolidation")
    logger.setLevel(logging.DEBUG)

    formatter = logging.Formatter(
        '%(asctime)s - %(name)s - %(levelname)s - [%(funcName)s:%(lineno)d] - %(message)s',
        datefmt='%Y-%m-%d %H:%M:%S'
    )

    file_handler = logging.FileHandler(
        f"{log_dir}/consolidation_{datetime.now().strftime('%Y%m%d')}.log"
    )
    file_handler.setLevel(logging.DEBUG)
    file_handler.setFormatter(formatter)
    logger.addHandler(file_handler)

    console_handler = logging.StreamHandler()
    console_handler.setLevel(logging.INFO)
    console_handler.setFormatter(formatter)
    logger.addHandler(console_handler)

    return logger


logger = setup_logging()


# ============================================================================
# 枚舉和數據類
# ============================================================================

class DataSourceType(Enum):
    """資料源類型"""
    CSV = "csv"
    EXCEL = "excel"
    JSON = "json"
    DATABASE = "database"
    API = "api"
    WEB_SCRAPE = "web_scrape"


class ConflictResolutionStrategy(Enum):
    """衝突解決策略"""
    FIRST_WIN = "first_win"  # 第一個來源勝出
    LAST_WIN = "last_win"  # 最後一個來源勝出
    MERGE = "merge"  # 合併（對複雜類型）
    HIGHEST_PRIORITY = "highest_priority"  # 優先級最高


@dataclass
class DataSourceConfig:
    """資料源配置"""
    source_id: str  # 來源唯一識別碼
    source_type: DataSourceType  # 來源類型
    name: str  # 來源名稱
    priority: int  # 優先級（1-100，數字越高優先級越高）

    # 來源特定配置
    location: str = ""  # 檔案路徑或 URL
    connection_string: str = ""  # 資料庫連接字符串

    # 轉換配置
    column_mapping: Dict[str, str] = field(default_factory=dict)  # 欄位對應 {源欄位: 目標欄位}
    transformations: Dict[str, callable] = field(default_factory=dict)  # 欄位轉換函數

    # 過濾配置
    filters: Dict[str, Any] = field(default_factory=dict)  # 過濾條件

    # 去重配置
    dedup_keys: List[str] = field(default_factory=list)  # 去重關鍵欄位


@dataclass
class ConsolidationStats:
    """整合統計信息"""
    start_time: datetime
    end_time: Optional[datetime] = None
    total_sources: int = 0
    total_records_read: int = 0
    records_by_source: Dict[str, int] = field(default_factory=dict)
    total_records_consolidated: int = 0
    duplicates_found: int = 0
    conflicts_resolved: int = 0
    errors: List[str] = field(default_factory=list)
    warnings: List[str] = field(default_factory=list)


# ============================================================================
# 資料源提取器基類和具體實現
# ============================================================================

class DataSourceExtractor(ABC):
    """資料源提取器抽象基類"""

    def __init__(self, config: DataSourceConfig):
        """
        初始化提取器

        參數：
            config: 資料源配置
        """
        self.config = config
        self.data = None
        logger.info(f"初始化資料源提取器：{config.name}")

    @abstractmethod
    def extract(self) -> pd.DataFrame:
        """
        從來源提取資料

        返回值：
            DataFrame
        """
        pass

    def transform_columns(self, df: pd.DataFrame) -> pd.DataFrame:
        """
        執行欄位對應和轉換

        參數：
            df: 原始 DataFrame

        返回值：
            轉換後的 DataFrame
        """
        df_transformed = df.copy()

        # 1. 欄位對應
        if self.config.column_mapping:
            df_transformed = df_transformed.rename(
                columns=self.config.column_mapping
            )
            logger.info(f"應用欄位對應：{self.config.column_mapping}")

        # 2. 自定義轉換
        for col, transform_func in self.config.transformations.items():
            if col in df_transformed.columns:
                try:
                    df_transformed[col] = df_transformed[col].apply(transform_func)
                    logger.info(f"應用轉換到欄位：{col}")
                except Exception as e:
                    logger.warning(f"欄位 {col} 的轉換失敗：{e}")

        return df_transformed

    def apply_filters(self, df: pd.DataFrame) -> pd.DataFrame:
        """
        應用過濾條件

        參數：
            df: DataFrame

        返回值：
            過濾後的 DataFrame
        """
        if not self.config.filters:
            return df

        df_filtered = df.copy()

        for col, condition in self.config.filters.items():
            if col not in df_filtered.columns:
                logger.warning(f"過濾欄位 {col} 不存在")
                continue

            if isinstance(condition, (list, tuple)):
                # 值在列表中
                df_filtered = df_filtered[df_filtered[col].isin(condition)]
                logger.info(f"應用過濾：{col} in {condition}")
            elif isinstance(condition, dict) and 'min' in condition:
                # 範圍過濾
                df_filtered = df_filtered[
                    (df_filtered[col] >= condition['min']) &
                    (df_filtered[col] <= condition.get('max', float('inf')))
                ]
                logger.info(f"應用範圍過濾：{col}")
            else:
                # 相等條件
                df_filtered = df_filtered[df_filtered[col] == condition]
                logger.info(f"應用過濾：{col} == {condition}")

        return df_filtered


class CSVExtractor(DataSourceExtractor):
    """CSV 檔案提取器"""

    def extract(self) -> pd.DataFrame:
        """從 CSV 檔案提取資料"""
        try:
            logger.info(f"讀取 CSV 檔案：{self.config.location}")
            df = pd.read_csv(self.config.location, encoding='utf-8')
            logger.info(f"成功讀取 {len(df)} 行資料")
            return df
        except UnicodeDecodeError:
            logger.warning("UTF-8 讀取失敗，嘗試 latin-1 編碼")
            df = pd.read_csv(self.config.location, encoding='latin-1')
            return df
        except Exception as e:
            logger.error(f"CSV 讀取失敗：{e}")
            raise


class ExcelExtractor(DataSourceExtractor):
    """Excel 檔案提取器"""

    def extract(self) -> pd.DataFrame:
        """從 Excel 檔案提取資料"""
        try:
            logger.info(f"讀取 Excel 檔案：{self.config.location}")
            df = pd.read_excel(self.config.location)
            logger.info(f"成功讀取 {len(df)} 行資料")
            return df
        except Exception as e:
            logger.error(f"Excel 讀取失敗：{e}")
            raise


class JSONExtractor(DataSourceExtractor):
    """JSON 檔案提取器"""

    def extract(self) -> pd.DataFrame:
        """從 JSON 檔案提取資料"""
        try:
            logger.info(f"讀取 JSON 檔案：{self.config.location}")
            with open(self.config.location, 'r', encoding='utf-8') as f:
                data = json.load(f)

            # 處理不同的 JSON 結構
            if isinstance(data, list):
                df = pd.DataFrame(data)
            elif isinstance(data, dict):
                # 假設資料在特定鍵下
                if 'records' in data:
                    df = pd.DataFrame(data['records'])
                elif 'data' in data:
                    df = pd.DataFrame(data['data'])
                else:
                    df = pd.DataFrame([data])
            else:
                raise ValueError("不支援的 JSON 結構")

            logger.info(f"成功讀取 {len(df)} 行資料")
            return df
        except Exception as e:
            logger.error(f"JSON 讀取失敗：{e}")
            raise


class DatabaseExtractor(DataSourceExtractor):
    """資料庫提取器"""

    def extract(self) -> pd.DataFrame:
        """從資料庫提取資料"""
        try:
            logger.info(f"連接資料庫：{self.config.connection_string}")

            # 簡化示例，實際應支援 MySQL, PostgreSQL 等
            if self.config.connection_string.startswith('sqlite://'):
                db_path = self.config.connection_string.replace('sqlite:///', '')
                conn = sqlite3.connect(db_path)
            else:
                raise ValueError("暫不支援的資料庫類型")

            # 提取所有資料或基於位置 SQL
            if self.config.location:
                df = pd.read_sql_query(self.config.location, conn)
            else:
                # 假設 connection_string 包含表名
                df = pd.read_sql_query(f"SELECT * FROM {self.config.name}", conn)

            conn.close()
            logger.info(f"成功讀取 {len(df)} 行資料")
            return df
        except Exception as e:
            logger.error(f"資料庫讀取失敗：{e}")
            raise


class APIExtractor(DataSourceExtractor):
    """API 資料提取器"""

    def extract(self) -> pd.DataFrame:
        """從 API 提取資料"""
        try:
            logger.info(f"調用 API：{self.config.location}")

            response = requests.get(
                self.config.location,
                timeout=30
            )
            response.raise_for_status()

            data = response.json()

            # 處理不同的 API 回應格式
            if isinstance(data, list):
                df = pd.DataFrame(data)
            elif isinstance(data, dict):
                if 'records' in data:
                    df = pd.DataFrame(data['records'])
                elif 'data' in data:
                    df = pd.DataFrame(data['data'])
                else:
                    df = pd.DataFrame([data])
            else:
                raise ValueError("不支援的 API 回應格式")

            logger.info(f"成功讀取 {len(df)} 行資料")
            return df
        except Exception as e:
            logger.error(f"API 呼叫失敗：{e}")
            raise


# ============================================================================
# 提取器工廠
# ============================================================================

class ExtractorFactory:
    """提取器工廠"""

    _extractors = {
        DataSourceType.CSV: CSVExtractor,
        DataSourceType.EXCEL: ExcelExtractor,
        DataSourceType.JSON: JSONExtractor,
        DataSourceType.DATABASE: DatabaseExtractor,
        DataSourceType.API: APIExtractor,
    }

    @classmethod
    def create(cls, config: DataSourceConfig) -> DataSourceExtractor:
        """
        創建適當的提取器

        參數：
            config: 資料源配置

        返回值：
            提取器實例
        """
        extractor_class = cls._extractors.get(config.source_type)
        if not extractor_class:
            raise ValueError(f"不支援的來源類型：{config.source_type}")
        return extractor_class(config)


# ============================================================================
# 多來源整合引擎
# ============================================================================

class MultiSourceConsolidationEngine:
    """
    多來源資料整合引擎

    核心功能：
    1. 管理多個資料源
    2. 執行資料提取
    3. 去重和衝突解決
    4. 統一的資料輸出
    """

    def __init__(
        self,
        conflict_strategy: ConflictResolutionStrategy = ConflictResolutionStrategy.HIGHEST_PRIORITY,
        output_dir: str = "./consolidation_output"
    ):
        """
        初始化整合引擎

        參數：
            conflict_strategy: 衝突解決策略
            output_dir: 輸出目錄
        """
        self.sources: Dict[str, DataSourceConfig] = {}
        self.conflict_strategy = conflict_strategy
        self.output_dir = Path(output_dir)
        self.output_dir.mkdir(parents=True, exist_ok=True)

        self.stats = ConsolidationStats(start_time=datetime.now())
        logger.info(f"初始化多來源整合引擎，衝突策略：{conflict_strategy.value}")

    def add_source(self, config: DataSourceConfig) -> None:
        """
        添加資料源

        參數：
            config: 資料源配置
        """
        self.sources[config.source_id] = config
        logger.info(f"添加資料源：{config.name}（優先級：{config.priority}）")

    def add_sources_from_config(self, config_file: str) -> None:
        """
        從配置檔案載入資料源

        參數：
            config_file: YAML 或 JSON 配置檔案路徑
        """
        try:
            with open(config_file, 'r', encoding='utf-8') as f:
                if config_file.endswith('.json'):
                    config_data = json.load(f)
                else:
                    import yaml
                    config_data = yaml.safe_load(f)

            for source_config in config_data.get('sources', []):
                config = DataSourceConfig(
                    source_id=source_config['source_id'],
                    source_type=DataSourceType[source_config['type']],
                    name=source_config['name'],
                    priority=source_config.get('priority', 50),
                    location=source_config.get('location', ''),
                    column_mapping=source_config.get('column_mapping', {}),
                    filters=source_config.get('filters', {}),
                    dedup_keys=source_config.get('dedup_keys', [])
                )
                self.add_source(config)

            logger.info(f"從配置檔案載入 {len(self.sources)} 個資料源")
        except Exception as e:
            logger.error(f"載入配置檔案失敗：{e}")
            raise

    def extract_from_source(self, source_id: str) -> Tuple[pd.DataFrame, bool]:
        """
        從單個資料源提取資料

        參數：
            source_id: 資料源 ID

        返回值：
            (DataFrame, 是否成功)
        """
        if source_id not in self.sources:
            logger.error(f"資料源 {source_id} 不存在")
            return pd.DataFrame(), False

        config = self.sources[source_id]

        try:
            logger.info(f"\n開始從 {config.name} 提取資料...")

            extractor = ExtractorFactory.create(config)
            df = extractor.extract()

            # 應用轉換
            df = extractor.transform_columns(df)

            # 應用過濾
            df = extractor.apply_filters(df)

            # 添加來源標記
            df['_source'] = source_id
            df['_extracted_at'] = datetime.now().isoformat()

            self.stats.records_by_source[source_id] = len(df)
            self.stats.total_records_read += len(df)

            logger.info(f"成功提取 {len(df)} 行資料")
            return df, True

        except Exception as e:
            error_msg = f"從 {config.name} 提取失敗：{e}"
            logger.error(error_msg)
            self.stats.errors.append(error_msg)
            return pd.DataFrame(), False

    def extract_all_sources(self) -> pd.DataFrame:
        """
        從所有資料源提取資料

        返回值：
            合併後的 DataFrame
        """
        logger.info("=" * 80)
        logger.info("開始從所有資料源提取資料")
        logger.info("=" * 80)

        self.stats.total_sources = len(self.sources)

        dataframes = []
        for source_id in self.sources:
            df, success = self.extract_from_source(source_id)
            if success and not df.empty:
                dataframes.append(df)

        if not dataframes:
            logger.warning("沒有成功提取任何資料")
            return pd.DataFrame()

        # 合併所有 DataFrame
        combined_df = pd.concat(dataframes, ignore_index=True)
        logger.info(f"\n合併完成，總計 {len(combined_df)} 行資料")

        return combined_df

    def find_duplicates(
        self,
        df: pd.DataFrame,
        dedup_columns: Optional[List[str]] = None
    ) -> Tuple[pd.DataFrame, int]:
        """
        找出重複記錄

        參數：
            df: DataFrame
            dedup_columns: 用於去重的欄位列表

        返回值：
            (去重後的 DataFrame, 移除的重複行數)
        """
        logger.info("\n開始去重...")

        if dedup_columns is None:
            # 使用所有資料源定義的去重鍵
            all_dedup_keys = set()
            for config in self.sources.values():
                all_dedup_keys.update(config.dedup_keys)
            dedup_columns = list(all_dedup_keys) if all_dedup_keys else []

        if not dedup_columns:
            logger.warning("未指定去重欄位，跳過去重")
            return df, 0

        # 過濾存在的欄位
        dedup_columns = [col for col in dedup_columns if col in df.columns]

        if not dedup_columns:
            logger.warning("沒有有效的去重欄位")
            return df, 0

        before_dedup = len(df)
        df_deduped = df.drop_duplicates(subset=dedup_columns, keep='first')
        duplicates_removed = before_dedup - len(df_deduped)

        self.stats.duplicates_found = duplicates_removed

        logger.info(f"去重欄位：{dedup_columns}")
        logger.info(f"移除重複行數：{duplicates_removed}")

        return df_deduped, duplicates_removed

    def resolve_conflicts(
        self,
        df: pd.DataFrame,
        key_columns: Optional[List[str]] = None
    ) -> pd.DataFrame:
        """
        解決衝突記錄

        當同一鍵有多個來源的資料時，根據衝突策略解決

        參數：
            df: DataFrame
            key_columns: 鍵欄位列表

        返回值：
            衝突解決後的 DataFrame
        """
        logger.info("\n開始衝突解決...")

        if key_columns is None:
            # 自動判斷鍵欄位（如訂單 ID、客戶 ID 等）
            key_columns = [
                col for col in df.columns
                if 'id' in col.lower() and col != '_source'
            ]

        if not key_columns:
            logger.warning("未找到鍵欄位，跳過衝突解決")
            return df

        logger.info(f"衝突解決鍵欄位：{key_columns}")

        df_resolved = df.copy()

        # 按鍵分組
        grouped = df_resolved.groupby(key_columns, as_index=False)

        conflicts_found = 0

        for name, group in grouped:
            if len(group) > 1:
                conflicts_found += 1

                if self.conflict_strategy == ConflictResolutionStrategy.FIRST_WIN:
                    # 保留第一條
                    df_resolved = df_resolved[
                        ~(df_resolved[key_columns] == group[key_columns].iloc[0]).all(axis=1) |
                        (df_resolved.index == group.index[0])
                    ]

                elif self.conflict_strategy == ConflictResolutionStrategy.LAST_WIN:
                    # 保留最後一條
                    df_resolved = df_resolved[
                        ~(df_resolved[key_columns] == group[key_columns].iloc[0]).all(axis=1) |
                        (df_resolved.index == group.index[-1])
                    ]

                elif self.conflict_strategy == ConflictResolutionStrategy.HIGHEST_PRIORITY:
                    # 根據優先級保留最高優先級的
                    group_with_priority = group.copy()
                    group_with_priority['_priority'] = group_with_priority['_source'].map(
                        lambda x: self.sources[x].priority if x in self.sources else 0
                    )
                    highest_priority_idx = group_with_priority['_priority'].idxmax()

                    # 移除該鍵的所有記錄，然後添加最高優先級的
                    mask = (df_resolved[key_columns] == group[key_columns].iloc[0]).all(axis=1)
                    df_resolved = df_resolved[~mask]
                    df_resolved = pd.concat([df_resolved, group.loc[[highest_priority_idx]]], ignore_index=True)

        self.stats.conflicts_resolved = conflicts_found

        logger.info(f"解決了 {conflicts_found} 個衝突")

        return df_resolved

    def consolidate(
        self,
        dedup_columns: Optional[List[str]] = None,
        key_columns: Optional[List[str]] = None
    ) -> pd.DataFrame:
        """
        執行完整的整合流程

        參數：
            dedup_columns: 去重欄位
            key_columns: 衝突解決鍵欄位

        返回值：
            整合後的 DataFrame
        """
        try:
            # 1. 提取
            df_combined = self.extract_all_sources()
            if df_combined.empty:
                logger.warning("沒有資料可進行整合")
                return df_combined

            # 2. 去重
            df_deduped, _ = self.find_duplicates(df_combined, dedup_columns)

            # 3. 衝突解決
            df_resolved = self.resolve_conflicts(df_deduped, key_columns)

            self.stats.total_records_consolidated = len(df_resolved)
            self.stats.end_time = datetime.now()

            logger.info("\n" + "=" * 80)
            logger.info("整合完成")
            logger.info(f"最終記錄數：{len(df_resolved)}")
            logger.info("=" * 80)

            return df_resolved

        except Exception as e:
            logger.error(f"整合失敗：{e}")
            self.stats.errors.append(str(e))
            self.stats.end_time = datetime.now()
            raise

    def save_consolidated_data(
        self,
        df: pd.DataFrame,
        format: str = 'csv'
    ) -> Path:
        """
        保存整合後的資料

        參數：
            df: DataFrame
            format: 格式（csv, excel, json）

        返回值：
            保存的檔案路徑
        """
        logger.info(f"保存整合後的資料（格式：{format}）...")

        timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')

        if format == 'csv':
            file_path = self.output_dir / f"consolidated_{timestamp}.csv"
            df.to_csv(file_path, index=False, encoding='utf-8')

        elif format == 'excel':
            file_path = self.output_dir / f"consolidated_{timestamp}.xlsx"
            df.to_excel(file_path, index=False)

        elif format == 'json':
            file_path = self.output_dir / f"consolidated_{timestamp}.json"
            df.to_json(file_path, orient='records', force_ascii=False, indent=2)

        else:
            raise ValueError(f"不支援的格式：{format}")

        logger.info(f"檔案已保存：{file_path}")
        return file_path

    def generate_consolidation_report(self) -> Dict:
        """
        生成整合報告

        返回值：
            報告字典
        """
        processing_time = (
            (self.stats.end_time - self.stats.start_time).total_seconds()
            if self.stats.end_time else 0
        )

        report = {
            'report_date': datetime.now().isoformat(),
            'processing_time_seconds': processing_time,
            'total_sources': self.stats.total_sources,
            'records_by_source': self.stats.records_by_source,
            'total_records_read': self.stats.total_records_read,
            'duplicates_found': self.stats.duplicates_found,
            'conflicts_resolved': self.stats.conflicts_resolved,
            'final_records': self.stats.total_records_consolidated,
            'data_quality': {
                'deduplication_rate': f"{(self.stats.duplicates_found / max(self.stats.total_records_read, 1) * 100):.2f}%",
                'conflict_rate': f"{(self.stats.conflicts_resolved / max(self.stats.total_records_read, 1) * 100):.2f}%"
            },
            'errors': self.stats.errors,
            'warnings': self.stats.warnings
        }

        return report

    def save_report(self, report: Dict) -> Path:
        """
        保存整合報告

        參數：
            report: 報告字典

        返回值：
            報告檔案路徑
        """
        timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
        report_file = self.output_dir / f"consolidation_report_{timestamp}.json"

        with open(report_file, 'w', encoding='utf-8') as f:
            json.dump(report, f, ensure_ascii=False, indent=2)

        logger.info(f"報告已保存：{report_file}")
        return report_file


# ============================================================================
# 主函數和示例用法
# ============================================================================

def main():
    """主函數 - 執行多來源整合示例"""

    logger.info("\n" + "=" * 80)
    logger.info("多來源資料整合系統 - 示例執行")
    logger.info("=" * 80 + "\n")

    # 創建整合引擎
    engine = MultiSourceConsolidationEngine(
        conflict_strategy=ConflictResolutionStrategy.HIGHEST_PRIORITY,
        output_dir="./consolidation_output"
    )

    # 添加資料源示例
    # 來源1：銷售訂單 CSV
    sales_config = DataSourceConfig(
        source_id="sales_csv",
        source_type=DataSourceType.CSV,
        name="銷售訂單系統",
        priority=90,
        location="/home/justin/web-projects/excel-python-data-analysis/week09-11_automation-workflows/data/sample_sales.csv",
        column_mapping={
            'customer_id': 'customer_id',
            'product': 'product_id',
            'sales_amount': 'amount'
        },
        filters={'status': ['completed', 'pending']},
        dedup_keys=['order_id']
    )

    # 來源2：庫存 Excel
    inventory_config = DataSourceConfig(
        source_id="inventory_excel",
        source_type=DataSourceType.EXCEL,
        name="庫存管理系統",
        priority=80,
        location="/home/justin/web-projects/excel-python-data-analysis/week09-11_automation-workflows/data/sample_inventory.xlsx",
        column_mapping={
            'sku': 'product_id',
            'on_hand': 'quantity'
        },
        dedup_keys=['product_id']
    )

    engine.add_source(sales_config)
    engine.add_source(inventory_config)

    # 執行整合
    df_consolidated = engine.consolidate(
        dedup_columns=['order_id'],
        key_columns=['customer_id', 'product_id']
    )

    # 保存結果
    if not df_consolidated.empty:
        engine.save_consolidated_data(df_consolidated, format='csv')
        engine.save_consolidated_data(df_consolidated, format='excel')

        # 生成報告
        report = engine.generate_consolidation_report()
        engine.save_report(report)

        logger.info("\n整合完成！")
        logger.info(f"最終資料行數：{len(df_consolidated)}")
    else:
        logger.warning("沒有整合任何資料")


if __name__ == "__main__":
    main()
