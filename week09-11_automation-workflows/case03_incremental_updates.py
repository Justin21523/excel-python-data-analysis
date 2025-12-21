"""
案例3：增量更新 vs 全量更新系統

功能概述：
- 支援增量更新（Incremental Updates）
  * 只更新新增和修改的記錄
  * 使用時間戳追蹤變化
  * 減少網路流量和資料庫負載

- 支援全量更新（Full Updates）
  * 完全替換資料集
  * 用於定期完整重新整理

- 增量與全量的智能切換
- 變更日誌和版本管理
- 衝突檢測和解決

執行方式：
    python case03_incremental_updates.py

作者：Data Engineering Team
版本：1.0.0
"""

import pandas as pd
import numpy as np
import logging
import sqlite3
import json
from pathlib import Path
from datetime import datetime, timedelta
from typing import Dict, List, Tuple, Optional, Any
from dataclasses import dataclass, field, asdict
from enum import Enum
import hashlib


# ============================================================================
# 日誌配置
# ============================================================================

def setup_logging(log_dir: str = "./logs") -> logging.Logger:
    """設定日誌系統"""
    Path(log_dir).mkdir(exist_ok=True)

    logger = logging.getLogger("IncrementalUpdates")
    logger.setLevel(logging.DEBUG)

    formatter = logging.Formatter(
        '%(asctime)s - %(name)s - %(levelname)s - [%(funcName)s:%(lineno)d] - %(message)s',
        datefmt='%Y-%m-%d %H:%M:%S'
    )

    file_handler = logging.FileHandler(
        f"{log_dir}/incremental_{datetime.now().strftime('%Y%m%d')}.log"
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

class UpdateType(Enum):
    """更新類型"""
    FULL = "full"  # 全量更新
    INCREMENTAL = "incremental"  # 增量更新


class ChangeType(Enum):
    """變更類型"""
    INSERT = "insert"  # 新增
    UPDATE = "update"  # 更新
    DELETE = "delete"  # 刪除


@dataclass
class UpdateConfig:
    """更新配置"""
    update_type: UpdateType  # 更新類型
    key_columns: List[str]  # 主鍵欄位
    timestamp_column: str  # 時間戳欄位
    track_deletes: bool = True  # 是否追蹤刪除
    auto_switch_threshold: int = 100  # 自動切換到全量的變更數量閾值（百分比）


@dataclass
class ChangeRecord:
    """單條變更記錄"""
    change_type: ChangeType  # 變更類型
    record_id: str  # 記錄 ID
    key_values: Dict[str, Any]  # 鍵值
    before_data: Optional[Dict[str, Any]] = None  # 更新前資料
    after_data: Optional[Dict[str, Any]] = None  # 更新後資料
    change_timestamp: datetime = field(default_factory=datetime.now)
    change_hash: str = ""  # 變更內容哈希值


@dataclass
class UpdateStats:
    """更新統計信息"""
    update_type: UpdateType
    start_time: datetime
    end_time: Optional[datetime] = None
    total_source_records: int = 0
    total_target_records: int = 0
    inserts: int = 0
    updates: int = 0
    deletes: int = 0
    no_changes: int = 0
    conflicts: int = 0
    errors: List[str] = field(default_factory=list)


# ============================================================================
# 增量更新引擎
# ============================================================================

class IncrementalUpdateEngine:
    """
    增量與全量更新引擎

    核心功能：
    1. 監測資料變化
    2. 追蹤插入、更新、刪除
    3. 變更日誌記錄
    4. 版本管理
    5. 衝突偵測和解決
    """

    def __init__(
        self,
        database_path: str = "./update_tracking.db",
        config: Optional[UpdateConfig] = None
    ):
        """
        初始化更新引擎

        參數：
            database_path: 資料庫路徑
            config: 更新配置
        """
        self.database_path = database_path
        self.config = config or UpdateConfig(
            update_type=UpdateType.INCREMENTAL,
            key_columns=['id'],
            timestamp_column='updated_at'
        )

        self.stats = None
        self._init_database()

        logger.info("增量更新引擎初始化完成")

    def _init_database(self) -> None:
        """初始化追蹤資料庫"""
        try:
            conn = sqlite3.connect(self.database_path)
            cursor = conn.cursor()

            # 變更日誌表
            cursor.execute("""
                CREATE TABLE IF NOT EXISTS change_log (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    table_name TEXT NOT NULL,
                    record_id TEXT NOT NULL,
                    change_type TEXT NOT NULL,
                    before_data TEXT,
                    after_data TEXT,
                    change_timestamp TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                    change_hash TEXT,
                    user TEXT DEFAULT 'system'
                )
            """)

            # 更新歷史表
            cursor.execute("""
                CREATE TABLE IF NOT EXISTS update_history (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    update_id TEXT UNIQUE NOT NULL,
                    table_name TEXT NOT NULL,
                    update_type TEXT NOT NULL,
                    update_timestamp TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                    source_records INTEGER,
                    target_records INTEGER,
                    inserts INTEGER,
                    updates INTEGER,
                    deletes INTEGER,
                    conflicts INTEGER,
                    duration_seconds REAL,
                    status TEXT DEFAULT 'pending'
                )
            """)

            # 版本控制表
            cursor.execute("""
                CREATE TABLE IF NOT EXISTS version_control (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    table_name TEXT NOT NULL,
                    version_number INTEGER,
                    version_date TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                    snapshot_hash TEXT,
                    description TEXT
                )
            """)

            conn.commit()
            conn.close()
            logger.info("追蹤資料庫初始化完成")

        except Exception as e:
            logger.error(f"資料庫初始化失敗：{e}")
            raise

    def _calculate_record_hash(self, row: pd.Series, exclude_cols: List[str] = None) -> str:
        """
        計算記錄的哈希值（用於偵測更新）

        參數：
            row: DataFrame 行
            exclude_cols: 要排除的欄位

        返回值：
            哈希值
        """
        exclude_cols = exclude_cols or [self.config.timestamp_column, '_hash']

        # 準備用於哈希的資料
        data_for_hash = {
            k: v for k, v in row.items()
            if k not in exclude_cols and pd.notna(v)
        }

        # 轉換為字符串並排序以確保一致性
        data_str = json.dumps(data_for_hash, sort_keys=True, default=str)
        return hashlib.md5(data_str.encode()).hexdigest()

    def compare_dataframes(
        self,
        source_df: pd.DataFrame,
        target_df: pd.DataFrame
    ) -> Dict[str, pd.DataFrame]:
        """
        比較源和目標 DataFrame，識別變化

        參數：
            source_df: 源 DataFrame（新資料）
            target_df: 目標 DataFrame（舊資料）

        返回值：
            包含新增、更新、刪除記錄的字典
        """
        logger.info("開始比較資料...")

        # 創建副本
        source = source_df.copy()
        target = target_df.copy()

        # 確保鍵欄位存在
        for key_col in self.config.key_columns:
            if key_col not in source.columns or key_col not in target.columns:
                logger.error(f"鍵欄位 {key_col} 不存在")
                raise ValueError(f"鍵欄位 {key_col} 不存在")

        # 為兩個 DataFrame 添加哈希值
        source['_hash'] = source.apply(self._calculate_record_hash, axis=1)
        target['_hash'] = target.apply(self._calculate_record_hash, axis=1)

        # 合併鍵値
        source['_key'] = source[self.config.key_columns].astype(str).agg('_'.join, axis=1)
        target['_key'] = target[self.config.key_columns].astype(str).agg('_'.join, axis=1)

        # 識別新增
        new_keys = set(source['_key']) - set(target['_key'])
        inserts = source[source['_key'].isin(new_keys)].drop(columns=['_key', '_hash'])

        # 識別刪除
        deleted_keys = set(target['_key']) - set(source['_key'])
        deletes = target[target['_key'].isin(deleted_keys)].drop(columns=['_key', '_hash'])

        # 識別更新
        common_keys = set(source['_key']) & set(target['_key'])
        source_common = source[source['_key'].isin(common_keys)].sort_values('_key')
        target_common = target[target['_key'].isin(common_keys)].sort_values('_key')

        # 比較哈希值找出更新
        update_mask = source_common['_hash'].values != target_common['_hash'].values
        updates = source_common[update_mask].drop(columns=['_key', '_hash'])

        # 沒有變化的記錄
        no_change_mask = source_common['_hash'].values == target_common['_hash'].values
        no_changes = source_common[no_change_mask].drop(columns=['_key', '_hash'])

        logger.info(f"比較結果：")
        logger.info(f"  - 新增：{len(inserts)}")
        logger.info(f"  - 更新：{len(updates)}")
        logger.info(f"  - 刪除：{len(deletes)}")
        logger.info(f"  - 無變化：{len(no_changes)}")

        return {
            'inserts': inserts,
            'updates': updates,
            'deletes': deletes,
            'no_changes': no_changes
        }

    def apply_incremental_update(
        self,
        source_df: pd.DataFrame,
        target_df: pd.DataFrame
    ) -> Tuple[pd.DataFrame, UpdateStats]:
        """
        執行增量更新

        參數：
            source_df: 源 DataFrame
            target_df: 目標 DataFrame

        返回值：
            (更新後的 DataFrame, 統計信息)
        """
        logger.info("\n" + "=" * 60)
        logger.info("執行增量更新")
        logger.info("=" * 60)

        self.stats = UpdateStats(
            update_type=UpdateType.INCREMENTAL,
            start_time=datetime.now(),
            total_source_records=len(source_df),
            total_target_records=len(target_df)
        )

        try:
            # 比較資料
            changes = self.compare_dataframes(source_df, target_df)

            self.stats.inserts = len(changes['inserts'])
            self.stats.updates = len(changes['updates'])
            self.stats.deletes = len(changes['deletes'])
            self.stats.no_changes = len(changes['no_changes'])

            # 決定更新策略
            total_changes = self.stats.inserts + self.stats.updates + self.stats.deletes
            change_percentage = (total_changes / max(len(target_df), 1)) * 100

            if change_percentage > self.config.auto_switch_threshold:
                logger.warning(f"變更率 {change_percentage:.2f}% 超過閾值，建議使用全量更新")
                self.stats.errors.append(
                    f"變更率過高 ({change_percentage:.2f}%)，建議使用全量更新"
                )

            # 應用變化
            result_df = target_df.copy()

            # 1. 添加新記錄
            if not changes['inserts'].empty:
                result_df = pd.concat([result_df, changes['inserts']], ignore_index=True)
                logger.info(f"已添加 {len(changes['inserts'])} 條新記錄")

            # 2. 更新現有記錄
            if not changes['updates'].empty:
                for idx, update_row in changes['updates'].iterrows():
                    key_match = pd.Series(True, index=result_df.index)
                    for key_col in self.config.key_columns:
                        key_match &= result_df[key_col] == update_row[key_col]

                    if key_match.any():
                        result_df.loc[key_match, :] = update_row
                logger.info(f"已更新 {len(changes['updates'])} 條記錄")

            # 3. 刪除記錄（可選）
            if not changes['deletes'].empty and self.config.track_deletes:
                for idx, delete_row in changes['deletes'].iterrows():
                    key_match = pd.Series(True, index=result_df.index)
                    for key_col in self.config.key_columns:
                        key_match &= result_df[key_col] == delete_row[key_col]

                    result_df = result_df[~key_match]
                logger.info(f"已刪除 {len(changes['deletes'])} 條記錄")

            # 記錄變更
            self._log_changes(changes)

            self.stats.end_time = datetime.now()

            logger.info("\n增量更新完成")
            logger.info(f"最終記錄數：{len(result_df)}")

            return result_df, self.stats

        except Exception as e:
            logger.error(f"增量更新失敗：{e}")
            self.stats.errors.append(str(e))
            self.stats.end_time = datetime.now()
            raise

    def apply_full_update(
        self,
        source_df: pd.DataFrame,
        target_df: Optional[pd.DataFrame] = None
    ) -> Tuple[pd.DataFrame, UpdateStats]:
        """
        執行全量更新

        參數：
            source_df: 源 DataFrame（新完整資料集）
            target_df: 目標 DataFrame（舊資料，可選）

        返回值：
            (更新後的 DataFrame, 統計信息)
        """
        logger.info("\n" + "=" * 60)
        logger.info("執行全量更新")
        logger.info("=" * 60)

        self.stats = UpdateStats(
            update_type=UpdateType.FULL,
            start_time=datetime.now(),
            total_source_records=len(source_df),
            total_target_records=len(target_df) if target_df is not None else 0
        )

        try:
            # 全量更新就是直接替換
            result_df = source_df.copy()

            if target_df is not None:
                # 計算變化統計
                changes = self.compare_dataframes(source_df, target_df)
                self.stats.inserts = len(changes['inserts'])
                self.stats.updates = len(changes['updates'])
                self.stats.deletes = len(changes['deletes'])

                # 記錄變更
                self._log_changes(changes)

            self.stats.end_time = datetime.now()

            logger.info("\n全量更新完成")
            logger.info(f"最終記錄數：{len(result_df)}")

            return result_df, self.stats

        except Exception as e:
            logger.error(f"全量更新失敗：{e}")
            self.stats.errors.append(str(e))
            self.stats.end_time = datetime.now()
            raise

    def smart_update(
        self,
        source_df: pd.DataFrame,
        target_df: Optional[pd.DataFrame] = None,
        force_type: Optional[UpdateType] = None
    ) -> Tuple[pd.DataFrame, UpdateStats]:
        """
        智能選擇更新策略

        根據資料量和變化量智能選擇增量或全量更新

        參數：
            source_df: 源 DataFrame
            target_df: 目標 DataFrame
            force_type: 強制使用的更新類型

        返回值：
            (更新後的 DataFrame, 統計信息)
        """
        logger.info("\n" + "=" * 60)
        logger.info("執行智能更新")
        logger.info("=" * 60)

        if force_type:
            logger.info(f"使用強制指定的更新類型：{force_type.value}")
            update_type = force_type
        else:
            # 判斷是否應使用全量更新
            if target_df is None or len(target_df) == 0:
                update_type = UpdateType.FULL
                logger.info("目標資料為空或不存在，使用全量更新")
            else:
                # 計算變更比例
                changes = self.compare_dataframes(source_df, target_df)
                total_changes = len(changes['inserts']) + len(changes['updates']) + len(changes['deletes'])
                change_percentage = (total_changes / len(target_df)) * 100

                if change_percentage > self.config.auto_switch_threshold:
                    update_type = UpdateType.FULL
                    logger.info(f"變更率 {change_percentage:.2f}% > {self.config.auto_switch_threshold}%，使用全量更新")
                else:
                    update_type = UpdateType.INCREMENTAL
                    logger.info(f"變更率 {change_percentage:.2f}% < {self.config.auto_switch_threshold}%，使用增量更新")

        # 執行選定的更新
        if update_type == UpdateType.INCREMENTAL:
            if target_df is None or len(target_df) == 0:
                return self.apply_full_update(source_df)
            return self.apply_incremental_update(source_df, target_df)
        else:
            return self.apply_full_update(source_df, target_df)

    def _log_changes(self, changes: Dict[str, pd.DataFrame]) -> None:
        """
        記錄所有變更到變更日誌

        參數：
            changes: 變更字典
        """
        try:
            conn = sqlite3.connect(self.database_path)

            # 記錄插入
            for idx, row in changes['inserts'].iterrows():
                self._insert_change_log(
                    conn,
                    'data_table',
                    str(row.get(self.config.key_columns[0], '')),
                    ChangeType.INSERT,
                    None,
                    row.to_dict()
                )

            # 記錄更新
            for idx, row in changes['updates'].iterrows():
                self._insert_change_log(
                    conn,
                    'data_table',
                    str(row.get(self.config.key_columns[0], '')),
                    ChangeType.UPDATE,
                    None,
                    row.to_dict()
                )

            # 記錄刪除
            for idx, row in changes['deletes'].iterrows():
                self._insert_change_log(
                    conn,
                    'data_table',
                    str(row.get(self.config.key_columns[0], '')),
                    ChangeType.DELETE,
                    row.to_dict(),
                    None
                )

            conn.commit()
            conn.close()

            logger.info(f"變更已記錄到日誌")

        except Exception as e:
            logger.error(f"記錄變更失敗：{e}")

    def _insert_change_log(
        self,
        conn,
        table_name: str,
        record_id: str,
        change_type: ChangeType,
        before_data: Optional[Dict],
        after_data: Optional[Dict]
    ) -> None:
        """插入變更日誌"""
        cursor = conn.cursor()

        change_hash = hashlib.md5(
            json.dumps(after_data or before_data, default=str).encode()
        ).hexdigest()

        cursor.execute("""
            INSERT INTO change_log
            (table_name, record_id, change_type, before_data, after_data, change_hash)
            VALUES (?, ?, ?, ?, ?, ?)
        """, (
            table_name,
            record_id,
            change_type.value,
            json.dumps(before_data) if before_data else None,
            json.dumps(after_data) if after_data else None,
            change_hash
        ))

    def get_change_log(
        self,
        table_name: str = None,
        since: Optional[datetime] = None
    ) -> pd.DataFrame:
        """
        獲取變更日誌

        參數：
            table_name: 表名（可選）
            since: 從此時間開始（可選）

        返回值：
            變更日誌 DataFrame
        """
        conn = sqlite3.connect(self.database_path)

        query = "SELECT * FROM change_log WHERE 1=1"
        params = []

        if table_name:
            query += " AND table_name = ?"
            params.append(table_name)

        if since:
            query += " AND change_timestamp > ?"
            params.append(since.isoformat())

        query += " ORDER BY change_timestamp DESC"

        df = pd.read_sql_query(query, conn, params=params)
        conn.close()

        return df

    def generate_update_report(self) -> Dict:
        """
        生成更新報告

        返回值：
            報告字典
        """
        if self.stats is None:
            return {}

        processing_time = (
            (self.stats.end_time - self.stats.start_time).total_seconds()
            if self.stats.end_time else 0
        )

        report = {
            'report_date': datetime.now().isoformat(),
            'update_type': self.stats.update_type.value,
            'processing_time_seconds': processing_time,
            'data_statistics': {
                'source_records': self.stats.total_source_records,
                'target_records': self.stats.total_target_records,
                'result_records': self.stats.inserts + self.stats.no_changes + (
                    self.stats.total_target_records - len(set())
                ) if self.stats.deletes > 0 else 0
            },
            'changes': {
                'inserts': self.stats.inserts,
                'updates': self.stats.updates,
                'deletes': self.stats.deletes,
                'no_changes': self.stats.no_changes,
                'total_changes': self.stats.inserts + self.stats.updates + self.stats.deletes
            },
            'performance': {
                'change_rate_percent': f"{((self.stats.inserts + self.stats.updates + self.stats.deletes) / max(self.stats.total_target_records, 1) * 100):.2f}%"
            },
            'errors': self.stats.errors
        }

        return report


# ============================================================================
# 主函數和示例用法
# ============================================================================

def main():
    """主函數 - 執行增量更新示例"""

    logger.info("\n" + "=" * 80)
    logger.info("增量與全量更新系統 - 示例執行")
    logger.info("=" * 80 + "\n")

    # 創建示例資料
    old_data = {
        'id': ['A001', 'A002', 'A003', 'A004'],
        'name': ['Alice', 'Bob', 'Charlie', 'David'],
        'amount': [100, 200, 300, 400],
        'updated_at': [
            '2025-12-01', '2025-12-01', '2025-12-01', '2025-12-01'
        ]
    }

    new_data = {
        'id': ['A001', 'A002', 'A003', 'A005'],  # A004 被刪除，A005 被添加
        'name': ['Alice', 'Bobby', 'Charlie', 'Eve'],  # Bob 改為 Bobby
        'amount': [100, 250, 300, 500],  # Bob 的金額從 200 改為 250
        'updated_at': [
            '2025-12-01', '2025-12-05', '2025-12-01', '2025-12-05'
        ]
    }

    old_df = pd.DataFrame(old_data)
    new_df = pd.DataFrame(new_data)

    logger.info("舊資料：")
    logger.info(old_df)
    logger.info("\n新資料：")
    logger.info(new_df)

    # 創建更新引擎
    config = UpdateConfig(
        update_type=UpdateType.INCREMENTAL,
        key_columns=['id'],
        timestamp_column='updated_at',
        auto_switch_threshold=50
    )

    engine = IncrementalUpdateEngine(config=config)

    # 執行智能更新
    result_df, stats = engine.smart_update(new_df, old_df)

    logger.info("\n更新後的資料：")
    logger.info(result_df)

    # 生成報告
    report = engine.generate_update_report()
    logger.info("\n" + "=" * 60)
    logger.info("更新報告：")
    logger.info(json.dumps(report, indent=2, ensure_ascii=False))
    logger.info("=" * 60)

    # 獲取變更日誌
    change_log = engine.get_change_log()
    if not change_log.empty:
        logger.info("\n變更日誌：")
        logger.info(change_log)


if __name__ == "__main__":
    main()
