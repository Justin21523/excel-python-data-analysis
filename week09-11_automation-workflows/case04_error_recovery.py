"""
案例4：錯誤處理與恢復系統

功能概述：
- 全面的異常捕獲和分類
- 自動重試機制（指數退避）
- 檢查點和恢復
- 死信隊列（失敗記錄）
- 回滾機制
- 詳細的錯誤報告

執行方式：
    python case04_error_recovery.py

作者：Data Engineering Team
版本：1.0.0
"""

import pandas as pd
import logging
import sqlite3
import json
from pathlib import Path
from datetime import datetime, timedelta
from typing import Dict, List, Tuple, Optional, Callable, Any
from dataclasses import dataclass, field, asdict
from enum import Enum
import traceback
import time
from abc import ABC, abstractmethod


# ============================================================================
# 日誌配置
# ============================================================================

def setup_logging(log_dir: str = "./logs") -> logging.Logger:
    """設定日誌系統"""
    Path(log_dir).mkdir(exist_ok=True)

    logger = logging.getLogger("ErrorRecovery")
    logger.setLevel(logging.DEBUG)

    formatter = logging.Formatter(
        '%(asctime)s - %(name)s - %(levelname)s - [%(funcName)s:%(lineno)d] - %(message)s',
        datefmt='%Y-%m-%d %H:%M:%S'
    )

    file_handler = logging.FileHandler(
        f"{log_dir}/error_recovery_{datetime.now().strftime('%Y%m%d')}.log"
    )
    file_handler.setLevel(logging.DEBUG)
    file_handler.setFormatter(formatter)
    logger.addHandler(file_handler)

    error_handler = logging.FileHandler(
        f"{log_dir}/errors_{datetime.now().strftime('%Y%m%d')}.log"
    )
    error_handler.setLevel(logging.ERROR)
    error_handler.setFormatter(formatter)
    logger.addHandler(error_handler)

    console_handler = logging.StreamHandler()
    console_handler.setLevel(logging.INFO)
    console_handler.setFormatter(formatter)
    logger.addHandler(console_handler)

    return logger


logger = setup_logging()


# ============================================================================
# 枚舉和異常
# ============================================================================

class ErrorSeverity(Enum):
    """錯誤嚴重程度"""
    LOW = "low"  # 低：可以忽略或自動恢復
    MEDIUM = "medium"  # 中：可能需要人工介入
    HIGH = "high"  # 高：必須立即處理


class ErrorType(Enum):
    """錯誤類型"""
    VALIDATION_ERROR = "validation_error"  # 驗證錯誤
    DATA_ERROR = "data_error"  # 資料錯誤
    CONNECTION_ERROR = "connection_error"  # 連接錯誤
    TIMEOUT_ERROR = "timeout_error"  # 超時
    RESOURCE_ERROR = "resource_error"  # 資源錯誤（如磁盤滿）
    LOGIC_ERROR = "logic_error"  # 邏輯錯誤
    UNKNOWN_ERROR = "unknown_error"  # 未知錯誤


class RetryStrategy(Enum):
    """重試策略"""
    NO_RETRY = "no_retry"
    EXPONENTIAL_BACKOFF = "exponential_backoff"  # 指數退避
    LINEAR_BACKOFF = "linear_backoff"  # 線性退避
    FIXED_DELAY = "fixed_delay"  # 固定延遲


class ProcessingStatus(Enum):
    """處理狀態"""
    PENDING = "pending"  # 待處理
    PROCESSING = "processing"  # 處理中
    SUCCESS = "success"  # 成功
    FAILED = "failed"  # 失敗
    RETRY = "retry"  # 重試
    RECOVERED = "recovered"  # 已恢復


# ============================================================================
# 自定義異常
# ============================================================================

class ETLException(Exception):
    """ETL 基礎異常"""
    def __init__(self, message: str, error_type: ErrorType = ErrorType.UNKNOWN_ERROR):
        self.message = message
        self.error_type = error_type
        super().__init__(self.message)


class ValidationException(ETLException):
    """驗證異常"""
    def __init__(self, message: str):
        super().__init__(message, ErrorType.VALIDATION_ERROR)


class DataException(ETLException):
    """資料異常"""
    def __init__(self, message: str):
        super().__init__(message, ErrorType.DATA_ERROR)


class ConnectionException(ETLException):
    """連接異常"""
    def __init__(self, message: str):
        super().__init__(message, ErrorType.CONNECTION_ERROR)


class TimeoutException(ETLException):
    """超時異常"""
    def __init__(self, message: str):
        super().__init__(message, ErrorType.TIMEOUT_ERROR)


# ============================================================================
# 數據類
# ============================================================================

@dataclass
class ErrorRecord:
    """錯誤記錄"""
    error_id: str
    timestamp: datetime
    error_type: ErrorType
    severity: ErrorSeverity
    message: str
    source_data: Optional[Dict[str, Any]] = None
    stack_trace: Optional[str] = None
    retry_count: int = 0
    status: ProcessingStatus = ProcessingStatus.PENDING


@dataclass
class Checkpoint:
    """檢查點"""
    checkpoint_id: str
    timestamp: datetime
    process_name: str
    state: Dict[str, Any]  # 保存的狀態
    records_processed: int = 0
    is_valid: bool = True


# ============================================================================
# 重試管理器
# ============================================================================

class RetryManager:
    """
    重試管理器

    功能：
    - 管理重試策略
    - 計算重試延遲
    - 追蹤重試次數
    """

    def __init__(
        self,
        max_retries: int = 3,
        strategy: RetryStrategy = RetryStrategy.EXPONENTIAL_BACKOFF,
        base_delay: float = 1.0,
        max_delay: float = 60.0
    ):
        """
        初始化重試管理器

        參數：
            max_retries: 最大重試次數
            strategy: 重試策略
            base_delay: 基礎延遲（秒）
            max_delay: 最大延遲（秒）
        """
        self.max_retries = max_retries
        self.strategy = strategy
        self.base_delay = base_delay
        self.max_delay = max_delay

    def should_retry(self, retry_count: int) -> bool:
        """是否應該重試"""
        return retry_count < self.max_retries

    def get_delay(self, retry_count: int) -> float:
        """
        計算延遲時間

        參數：
            retry_count: 重試次數

        返回值：
            延遲時間（秒）
        """
        if self.strategy == RetryStrategy.NO_RETRY:
            return 0

        elif self.strategy == RetryStrategy.EXPONENTIAL_BACKOFF:
            delay = self.base_delay * (2 ** retry_count)

        elif self.strategy == RetryStrategy.LINEAR_BACKOFF:
            delay = self.base_delay * (retry_count + 1)

        elif self.strategy == RetryStrategy.FIXED_DELAY:
            delay = self.base_delay

        else:
            delay = 0

        # 限制最大延遲
        return min(delay, self.max_delay)

    def wait(self, retry_count: int) -> None:
        """等待指定時間"""
        delay = self.get_delay(retry_count)
        if delay > 0:
            logger.info(f"等待 {delay:.2f} 秒後重試...")
            time.sleep(delay)


# ============================================================================
# 錯誤恢復引擎
# ============================================================================

class ErrorRecoveryEngine:
    """
    錯誤恢復引擎

    核心功能：
    1. 錯誤捕獲和分類
    2. 自動重試
    3. 檢查點管理
    4. 死信隊列
    5. 恢復機制
    """

    def __init__(
        self,
        database_path: str = "./error_recovery.db",
        checkpoint_dir: str = "./checkpoints"
    ):
        """
        初始化錯誤恢復引擎

        參數：
            database_path: 資料庫路徑
            checkpoint_dir: 檢查點目錄
        """
        self.database_path = database_path
        self.checkpoint_dir = Path(checkpoint_dir)
        self.checkpoint_dir.mkdir(parents=True, exist_ok=True)

        self.retry_manager = RetryManager()
        self.error_records: List[ErrorRecord] = []
        self.checkpoints: Dict[str, Checkpoint] = {}

        self._init_database()

        logger.info("錯誤恢復引擎初始化完成")

    def _init_database(self) -> None:
        """初始化錯誤追蹤資料庫"""
        try:
            conn = sqlite3.connect(self.database_path)
            cursor = conn.cursor()

            # 錯誤日誌表
            cursor.execute("""
                CREATE TABLE IF NOT EXISTS error_log (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    error_id TEXT UNIQUE,
                    timestamp TIMESTAMP,
                    error_type TEXT,
                    severity TEXT,
                    message TEXT,
                    source_data TEXT,
                    stack_trace TEXT,
                    retry_count INTEGER,
                    status TEXT,
                    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
                )
            """)

            # 死信隊列表
            cursor.execute("""
                CREATE TABLE IF NOT EXISTS dead_letter_queue (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    error_id TEXT,
                    record_data TEXT,
                    reason TEXT,
                    received_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
                )
            """)

            # 檢查點表
            cursor.execute("""
                CREATE TABLE IF NOT EXISTS checkpoints (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    checkpoint_id TEXT UNIQUE,
                    timestamp TIMESTAMP,
                    process_name TEXT,
                    state TEXT,
                    records_processed INTEGER,
                    is_valid BOOLEAN,
                    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
                )
            """)

            # 恢復歷史表
            cursor.execute("""
                CREATE TABLE IF NOT EXISTS recovery_history (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    recovery_id TEXT UNIQUE,
                    source_checkpoint_id TEXT,
                    recovery_timestamp TIMESTAMP,
                    records_recovered INTEGER,
                    status TEXT,
                    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
                )
            """)

            conn.commit()
            conn.close()
            logger.info("錯誤追蹤資料庫初始化完成")

        except Exception as e:
            logger.error(f"資料庫初始化失敗：{e}")
            raise

    def save_checkpoint(
        self,
        process_name: str,
        state: Dict[str, Any],
        records_processed: int = 0
    ) -> str:
        """
        保存檢查點

        參數：
            process_name: 進程名稱
            state: 狀態字典
            records_processed: 已處理的記錄數

        返回值：
            檢查點 ID
        """
        checkpoint_id = f"{process_name}_{datetime.now().strftime('%Y%m%d%H%M%S')}"
        checkpoint = Checkpoint(
            checkpoint_id=checkpoint_id,
            timestamp=datetime.now(),
            process_name=process_name,
            state=state,
            records_processed=records_processed
        )

        # 保存到內存
        self.checkpoints[checkpoint_id] = checkpoint

        # 保存到資料庫
        try:
            conn = sqlite3.connect(self.database_path)
            cursor = conn.cursor()

            cursor.execute("""
                INSERT INTO checkpoints
                (checkpoint_id, timestamp, process_name, state, records_processed, is_valid)
                VALUES (?, ?, ?, ?, ?, ?)
            """, (
                checkpoint_id,
                checkpoint.timestamp.isoformat(),
                process_name,
                json.dumps(checkpoint.state, default=str),
                records_processed,
                checkpoint.is_valid
            ))

            conn.commit()
            conn.close()

            logger.info(f"檢查點已保存：{checkpoint_id}")

        except Exception as e:
            logger.error(f"檢查點保存失敗：{e}")

        return checkpoint_id

    def load_checkpoint(self, checkpoint_id: str) -> Optional[Checkpoint]:
        """
        載入檢查點

        參數：
            checkpoint_id: 檢查點 ID

        返回值：
            檢查點對象或 None
        """
        # 先從內存查找
        if checkpoint_id in self.checkpoints:
            return self.checkpoints[checkpoint_id]

        # 從資料庫查找
        try:
            conn = sqlite3.connect(self.database_path)
            cursor = conn.cursor()

            cursor.execute("""
                SELECT checkpoint_id, timestamp, process_name, state, records_processed, is_valid
                FROM checkpoints
                WHERE checkpoint_id = ?
            """, (checkpoint_id,))

            row = cursor.fetchone()
            conn.close()

            if row:
                checkpoint = Checkpoint(
                    checkpoint_id=row[0],
                    timestamp=datetime.fromisoformat(row[1]),
                    process_name=row[2],
                    state=json.loads(row[3]),
                    records_processed=row[4],
                    is_valid=bool(row[5])
                )
                self.checkpoints[checkpoint_id] = checkpoint
                logger.info(f"檢查點已載入：{checkpoint_id}")
                return checkpoint

        except Exception as e:
            logger.error(f"檢查點載入失敗：{e}")

        return None

    def get_latest_checkpoint(self, process_name: str) -> Optional[Checkpoint]:
        """
        獲取最新的檢查點

        參數：
            process_name: 進程名稱

        返回值：
            最新的檢查點
        """
        try:
            conn = sqlite3.connect(self.database_path)
            cursor = conn.cursor()

            cursor.execute("""
                SELECT checkpoint_id, timestamp, process_name, state, records_processed, is_valid
                FROM checkpoints
                WHERE process_name = ? AND is_valid = 1
                ORDER BY timestamp DESC
                LIMIT 1
            """, (process_name,))

            row = cursor.fetchone()
            conn.close()

            if row:
                checkpoint = Checkpoint(
                    checkpoint_id=row[0],
                    timestamp=datetime.fromisoformat(row[1]),
                    process_name=row[2],
                    state=json.loads(row[3]),
                    records_processed=row[4],
                    is_valid=bool(row[5])
                )
                return checkpoint

        except Exception as e:
            logger.error(f"查詢檢查點失敗：{e}")

        return None

    def record_error(
        self,
        error_type: ErrorType,
        severity: ErrorSeverity,
        message: str,
        source_data: Optional[Dict] = None,
        stack_trace: Optional[str] = None
    ) -> str:
        """
        記錄錯誤

        參數：
            error_type: 錯誤類型
            severity: 嚴重程度
            message: 錯誤信息
            source_data: 源資料
            stack_trace: 堆棧跟蹤

        返回值：
            錯誤 ID
        """
        error_id = f"ERR_{datetime.now().strftime('%Y%m%d%H%M%S_%f')}"

        error_record = ErrorRecord(
            error_id=error_id,
            timestamp=datetime.now(),
            error_type=error_type,
            severity=severity,
            message=message,
            source_data=source_data,
            stack_trace=stack_trace
        )

        self.error_records.append(error_record)

        # 保存到資料庫
        try:
            conn = sqlite3.connect(self.database_path)
            cursor = conn.cursor()

            cursor.execute("""
                INSERT INTO error_log
                (error_id, timestamp, error_type, severity, message, source_data, stack_trace, retry_count, status)
                VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?)
            """, (
                error_id,
                error_record.timestamp.isoformat(),
                error_type.value,
                severity.value,
                message,
                json.dumps(source_data) if source_data else None,
                stack_trace,
                error_record.retry_count,
                ProcessingStatus.PENDING.value
            ))

            conn.commit()
            conn.close()

            logger.error(f"錯誤已記錄：{error_id} - [{severity.value}] {message}")

        except Exception as e:
            logger.error(f"錯誤記錄失敗：{e}")

        return error_id

    def send_to_dead_letter_queue(
        self,
        error_id: str,
        record_data: Dict,
        reason: str
    ) -> None:
        """
        發送到死信隊列

        參數：
            error_id: 錯誤 ID
            record_data: 記錄資料
            reason: 原因
        """
        try:
            conn = sqlite3.connect(self.database_path)
            cursor = conn.cursor()

            cursor.execute("""
                INSERT INTO dead_letter_queue
                (error_id, record_data, reason)
                VALUES (?, ?, ?)
            """, (
                error_id,
                json.dumps(record_data, default=str),
                reason
            ))

            conn.commit()
            conn.close()

            logger.warning(f"記錄已發送到死信隊列：{error_id}")

        except Exception as e:
            logger.error(f"發送到死信隊列失敗：{e}")

    def recover_from_checkpoint(
        self,
        checkpoint_id: str,
        recovery_func: Callable
    ) -> bool:
        """
        從檢查點恢復

        參數：
            checkpoint_id: 檢查點 ID
            recovery_func: 恢復函數

        返回值：
            是否恢復成功
        """
        logger.info(f"\n開始從檢查點恢復：{checkpoint_id}")

        checkpoint = self.load_checkpoint(checkpoint_id)
        if not checkpoint:
            logger.error(f"檢查點不存在：{checkpoint_id}")
            return False

        try:
            # 調用恢復函數
            result = recovery_func(checkpoint.state)

            if result:
                logger.info(f"恢復成功：已恢復 {checkpoint.records_processed} 條記錄")
                return True
            else:
                logger.warning("恢復函數返回 False")
                return False

        except Exception as e:
            logger.error(f"恢復失敗：{e}")
            return False

    def retry_with_strategy(
        self,
        operation: Callable,
        *args,
        **kwargs
    ) -> Tuple[bool, Any]:
        """
        使用重試策略執行操作

        參數：
            operation: 要執行的操作
            *args, **kwargs: 操作的參數

        返回值：
            (是否成功, 結果或異常)
        """
        retry_count = 0

        while retry_count <= self.retry_manager.max_retries:
            try:
                logger.info(f"執行操作（嘗試 {retry_count + 1}/{self.retry_manager.max_retries + 1}）...")
                result = operation(*args, **kwargs)
                return True, result

            except Exception as e:
                retry_count += 1

                if self.retry_manager.should_retry(retry_count):
                    logger.warning(f"操作失敗，準備重試：{str(e)}")
                    self.retry_manager.wait(retry_count - 1)
                else:
                    logger.error(f"操作在 {retry_count} 次嘗試後失敗：{str(e)}")
                    return False, e

        return False, Exception("未知錯誤")

    def get_error_summary(self) -> Dict:
        """
        獲取錯誤摘要

        返回值：
            錯誤摘要字典
        """
        try:
            conn = sqlite3.connect(self.database_path)
            cursor = conn.cursor()

            # 按類型統計錯誤
            cursor.execute("""
                SELECT error_type, COUNT(*) as count
                FROM error_log
                GROUP BY error_type
            """)

            error_by_type = {row[0]: row[1] for row in cursor.fetchall()}

            # 按嚴重程度統計
            cursor.execute("""
                SELECT severity, COUNT(*) as count
                FROM error_log
                GROUP BY severity
            """)

            error_by_severity = {row[0]: row[1] for row in cursor.fetchall()}

            # 死信隊列大小
            cursor.execute("SELECT COUNT(*) FROM dead_letter_queue")
            dlq_count = cursor.fetchone()[0]

            conn.close()

            summary = {
                'total_errors': len(self.error_records),
                'errors_by_type': error_by_type,
                'errors_by_severity': error_by_severity,
                'dead_letter_queue_size': dlq_count,
                'timestamp': datetime.now().isoformat()
            }

            return summary

        except Exception as e:
            logger.error(f"查詢錯誤摘要失敗：{e}")
            return {}


# ============================================================================
# 使用示例和演示
# ============================================================================

def example_operation_that_may_fail() -> str:
    """示例操作（可能失敗）"""
    import random
    if random.random() < 0.5:
        raise ConnectionException("模擬連接失敗")
    return "操作成功"


def example_recovery_function(state: Dict) -> bool:
    """示例恢復函數"""
    logger.info(f"恢復函數接收的狀態：{state}")
    # 模擬恢復操作
    return True


def main():
    """主函數 - 演示錯誤恢復"""

    logger.info("\n" + "=" * 80)
    logger.info("錯誤處理與恢復系統 - 演示")
    logger.info("=" * 80 + "\n")

    engine = ErrorRecoveryEngine()

    # 1. 保存檢查點
    logger.info("【1】保存檢查點...")
    checkpoint_state = {
        'process_id': 'proc_001',
        'last_record_id': 1000,
        'status': 'processing'
    }
    checkpoint_id = engine.save_checkpoint(
        process_name='etl_process',
        state=checkpoint_state,
        records_processed=1000
    )

    # 2. 記錄錯誤
    logger.info("\n【2】記錄錯誤...")
    error_id = engine.record_error(
        error_type=ErrorType.CONNECTION_ERROR,
        severity=ErrorSeverity.HIGH,
        message="無法連接到資料庫",
        source_data={'host': 'localhost', 'port': 5432},
        stack_trace=traceback.format_exc()
    )

    # 3. 發送到死信隊列
    logger.info("\n【3】發送失敗的記錄到死信隊列...")
    engine.send_to_dead_letter_queue(
        error_id=error_id,
        record_data={'id': 1, 'name': 'Test', 'value': 100},
        reason="驗證失敗"
    )

    # 4. 使用重試策略
    logger.info("\n【4】測試重試機制...")
    success, result = engine.retry_with_strategy(
        example_operation_that_may_fail
    )
    logger.info(f"操作結果：{'成功' if success else '失敗'}")

    # 5. 從檢查點恢復
    logger.info("\n【5】從檢查點恢復...")
    engine.recover_from_checkpoint(
        checkpoint_id=checkpoint_id,
        recovery_func=example_recovery_function
    )

    # 6. 獲取錯誤摘要
    logger.info("\n【6】錯誤摘要...")
    summary = engine.get_error_summary()
    logger.info(json.dumps(summary, indent=2, ensure_ascii=False))


if __name__ == "__main__":
    main()
