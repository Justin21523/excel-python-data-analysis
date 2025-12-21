"""
案例5：完整日誌系統

功能概述：
- 多層次日誌（DEBUG, INFO, WARNING, ERROR, CRITICAL）
- 結構化日誌（JSON 格式）
- 日誌旋轉和存檔
- 日誌分析和查詢
- 性能追蹤
- 審計日誌

執行方式：
    python case05_logging_system.py

作者：Data Engineering Team
版本：1.0.0
"""

import logging
import logging.handlers
import json
import sqlite3
from pathlib import Path
from datetime import datetime, timedelta
from typing import Dict, List, Optional, Any
from dataclasses import dataclass, asdict
from enum import Enum
import traceback
import time
from functools import wraps
import sys


# ============================================================================
# 日誌級別和類型定義
# ============================================================================

class LogLevel(Enum):
    """日誌級別"""
    DEBUG = logging.DEBUG  # 10
    INFO = logging.INFO  # 20
    WARNING = logging.WARNING  # 30
    ERROR = logging.ERROR  # 40
    CRITICAL = logging.CRITICAL  # 50


class LogCategory(Enum):
    """日誌分類"""
    SYSTEM = "system"  # 系統日誌
    BUSINESS = "business"  # 業務日誌
    SECURITY = "security"  # 安全日誌
    AUDIT = "audit"  # 審計日誌
    PERFORMANCE = "performance"  # 性能日誌


# ============================================================================
# 自定義日誌格式器
# ============================================================================

class JSONFormatter(logging.Formatter):
    """JSON 格式的日誌格式器"""

    def format(self, record: logging.LogRecord) -> str:
        """格式化日誌記錄為 JSON"""
        log_data = {
            'timestamp': datetime.fromtimestamp(record.created).isoformat(),
            'level': record.levelname,
            'logger': record.name,
            'module': record.module,
            'function': record.funcName,
            'line': record.lineno,
            'message': record.getMessage(),
            'process_id': record.process,
            'thread_id': record.thread,
        }

        # 添加異常信息
        if record.exc_info:
            log_data['exception'] = self.formatException(record.exc_info)

        # 添加額外信息
        if hasattr(record, 'extra_data'):
            log_data['extra'] = record.extra_data

        return json.dumps(log_data, ensure_ascii=False, default=str)


class ColoredFormatter(logging.Formatter):
    """帶顏色的控制台日誌格式器"""

    # ANSI 顏色代碼
    COLORS = {
        'DEBUG': '\033[36m',  # 青色
        'INFO': '\033[32m',  # 綠色
        'WARNING': '\033[33m',  # 黃色
        'ERROR': '\033[31m',  # 紅色
        'CRITICAL': '\033[35m',  # 紫色
    }
    RESET = '\033[0m'  # 重置

    def format(self, record: logging.LogRecord) -> str:
        """格式化日誌記錄（帶顏色）"""
        levelname = record.levelname
        color = self.COLORS.get(levelname, self.RESET)

        # 修改記錄的消息
        record.levelname = f"{color}{levelname}{self.RESET}"

        # 使用父類的格式化
        return super().format(record)


# ============================================================================
# 結構化日誌記錄器
# ============================================================================

class StructuredLogger:
    """
    結構化日誌記錄器

    提供統一的日誌記錄介面，支持：
    - 多層次日誌
    - 結構化信息
    - 上下文追蹤
    - 性能監控
    - 審計日誌
    """

    def __init__(
        self,
        name: str,
        log_dir: str = "./logs",
        enable_json: bool = True,
        enable_console: bool = True,
        enable_db: bool = True
    ):
        """
        初始化結構化日誌記錄器

        參數：
            name: 日誌記錄器名稱
            log_dir: 日誌目錄
            enable_json: 是否啟用 JSON 日誌
            enable_console: 是否啟用控制台輸出
            enable_db: 是否啟用資料庫存儲
        """
        self.name = name
        self.log_dir = Path(log_dir)
        self.log_dir.mkdir(parents=True, exist_ok=True)

        self.logger = logging.getLogger(name)
        self.logger.setLevel(logging.DEBUG)

        # 清除現有的處理器
        self.logger.handlers.clear()

        # 添加處理器
        if enable_console:
            self._add_console_handler()

        if enable_json:
            self._add_json_file_handler()

        self._add_text_file_handler()

        if enable_db:
            self.db_path = self.log_dir / f"{name}_logs.db"
            self._init_log_database()

        self.context = {}  # 上下文變量

    def _add_console_handler(self) -> None:
        """添加控制台處理器"""
        handler = logging.StreamHandler(sys.stdout)
        handler.setLevel(logging.INFO)

        formatter = ColoredFormatter(
            '%(levelname)s - %(name)s - [%(funcName)s:%(lineno)d] - %(message)s',
            datefmt='%Y-%m-%d %H:%M:%S'
        )
        handler.setFormatter(formatter)
        self.logger.addHandler(handler)

    def _add_text_file_handler(self) -> None:
        """添加文本文件處理器（帶旋轉）"""
        log_file = self.log_dir / f"{self.name}.log"

        handler = logging.handlers.RotatingFileHandler(
            log_file,
            maxBytes=10 * 1024 * 1024,  # 10 MB
            backupCount=10
        )
        handler.setLevel(logging.DEBUG)

        formatter = logging.Formatter(
            '%(asctime)s - %(name)s - %(levelname)s - [%(funcName)s:%(lineno)d] - %(message)s',
            datefmt='%Y-%m-%d %H:%M:%S'
        )
        handler.setFormatter(formatter)
        self.logger.addHandler(handler)

    def _add_json_file_handler(self) -> None:
        """添加 JSON 文件處理器"""
        log_file = self.log_dir / f"{self.name}_json.log"

        handler = logging.handlers.RotatingFileHandler(
            log_file,
            maxBytes=50 * 1024 * 1024,  # 50 MB
            backupCount=5
        )
        handler.setLevel(logging.DEBUG)

        formatter = JSONFormatter()
        handler.setFormatter(formatter)
        self.logger.addHandler(handler)

    def _init_log_database(self) -> None:
        """初始化日誌資料庫"""
        try:
            conn = sqlite3.connect(str(self.db_path))
            cursor = conn.cursor()

            cursor.execute("""
                CREATE TABLE IF NOT EXISTS logs (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    timestamp TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                    level TEXT NOT NULL,
                    category TEXT,
                    logger_name TEXT,
                    message TEXT,
                    context TEXT,
                    duration_ms REAL,
                    extra_data TEXT
                )
            """)

            # 創建索引以提高查詢性能
            cursor.execute("""
                CREATE INDEX IF NOT EXISTS idx_timestamp ON logs(timestamp)
            """)
            cursor.execute("""
                CREATE INDEX IF NOT EXISTS idx_level ON logs(level)
            """)
            cursor.execute("""
                CREATE INDEX IF NOT EXISTS idx_category ON logs(category)
            """)

            conn.commit()
            conn.close()

        except Exception as e:
            self.logger.error(f"日誌資料庫初始化失敗：{e}")

    def set_context(self, **kwargs) -> None:
        """
        設定日誌上下文

        參數：
            **kwargs: 上下文變量
        """
        self.context.update(kwargs)
        self.logger.info(f"日誌上下文已更新：{list(kwargs.keys())}")

    def clear_context(self) -> None:
        """清除日誌上下文"""
        self.context.clear()

    def _log_to_db(
        self,
        level: str,
        category: str,
        message: str,
        duration_ms: Optional[float] = None,
        extra_data: Optional[Dict] = None
    ) -> None:
        """將日誌記錄到資料庫"""
        try:
            conn = sqlite3.connect(str(self.db_path))
            cursor = conn.cursor()

            cursor.execute("""
                INSERT INTO logs (level, category, logger_name, message, context, duration_ms, extra_data)
                VALUES (?, ?, ?, ?, ?, ?, ?)
            """, (
                level,
                category,
                self.name,
                message,
                json.dumps(self.context, default=str),
                duration_ms,
                json.dumps(extra_data, default=str) if extra_data else None
            ))

            conn.commit()
            conn.close()

        except Exception as e:
            self.logger.error(f"日誌記錄到資料庫失敗：{e}")

    def debug(self, message: str, category: str = LogCategory.SYSTEM.value, **kwargs) -> None:
        """記錄 DEBUG 級別"""
        self.logger.debug(message)
        self._log_to_db(LogLevel.DEBUG.name, category, message, extra_data=kwargs)

    def info(self, message: str, category: str = LogCategory.SYSTEM.value, **kwargs) -> None:
        """記錄 INFO 級別"""
        self.logger.info(message)
        self._log_to_db(LogLevel.INFO.name, category, message, extra_data=kwargs)

    def warning(self, message: str, category: str = LogCategory.SYSTEM.value, **kwargs) -> None:
        """記錄 WARNING 級別"""
        self.logger.warning(message)
        self._log_to_db(LogLevel.WARNING.name, category, message, extra_data=kwargs)

    def error(self, message: str, category: str = LogCategory.SYSTEM.value, exc_info: bool = False, **kwargs) -> None:
        """記錄 ERROR 級別"""
        self.logger.error(message, exc_info=exc_info)
        self._log_to_db(LogLevel.ERROR.name, category, message, extra_data=kwargs)

    def critical(self, message: str, category: str = LogCategory.SYSTEM.value, **kwargs) -> None:
        """記錄 CRITICAL 級別"""
        self.logger.critical(message)
        self._log_to_db(LogLevel.CRITICAL.name, category, message, extra_data=kwargs)

    def audit(self, action: str, user: str, resource: str, result: str, **details) -> None:
        """
        記錄審計日誌

        參數：
            action: 動作（如 CREATE, UPDATE, DELETE）
            user: 用戶
            resource: 資源
            result: 結果（SUCCESS, FAILED）
            **details: 其他詳情
        """
        audit_msg = f"[AUDIT] 用戶 {user} 執行 {action} 操作在 {resource}，結果：{result}"
        self.logger.info(audit_msg)

        self._log_to_db(
            LogLevel.INFO.name,
            LogCategory.AUDIT.value,
            audit_msg,
            extra_data={
                'action': action,
                'user': user,
                'resource': resource,
                'result': result,
                **details
            }
        )

    def performance(self, operation: str, duration_ms: float, **details) -> None:
        """
        記錄性能日誌

        參數：
            operation: 操作名稱
            duration_ms: 耗時（毫秒）
            **details: 其他詳情
        """
        perf_msg = f"[PERFORMANCE] {operation} 耗時 {duration_ms:.2f}ms"
        level = LogLevel.WARNING.name if duration_ms > 1000 else LogLevel.INFO.name

        if duration_ms > 1000:
            self.logger.warning(perf_msg)
        else:
            self.logger.info(perf_msg)

        self._log_to_db(
            level,
            LogCategory.PERFORMANCE.value,
            perf_msg,
            duration_ms=duration_ms,
            extra_data={'operation': operation, **details}
        )

    def track_performance(self, operation_name: str):
        """
        性能追蹤裝飾器

        使用示例：
            @logger.track_performance("資料讀取")
            def read_data():
                pass
        """
        def decorator(func):
            @wraps(func)
            def wrapper(*args, **kwargs):
                start_time = time.time()
                try:
                    result = func(*args, **kwargs)
                    return result
                finally:
                    duration_ms = (time.time() - start_time) * 1000
                    self.performance(
                        operation=operation_name or func.__name__,
                        duration_ms=duration_ms
                    )
            return wrapper
        return decorator

    def query_logs(
        self,
        level: Optional[str] = None,
        category: Optional[str] = None,
        since: Optional[datetime] = None,
        limit: int = 100
    ) -> List[Dict]:
        """
        查詢日誌

        參數：
            level: 日誌級別（可選）
            category: 日誌分類（可選）
            since: 從此時間開始（可選）
            limit: 限制記錄數

        返回值：
            日誌記錄列表
        """
        try:
            conn = sqlite3.connect(str(self.db_path))
            conn.row_factory = sqlite3.Row
            cursor = conn.cursor()

            query = "SELECT * FROM logs WHERE 1=1"
            params = []

            if level:
                query += " AND level = ?"
                params.append(level)

            if category:
                query += " AND category = ?"
                params.append(category)

            if since:
                query += " AND timestamp > ?"
                params.append(since.isoformat())

            query += " ORDER BY timestamp DESC LIMIT ?"
            params.append(limit)

            cursor.execute(query, params)

            logs = []
            for row in cursor.fetchall():
                log_dict = dict(row)
                if log_dict['extra_data']:
                    log_dict['extra_data'] = json.loads(log_dict['extra_data'])
                logs.append(log_dict)

            conn.close()
            return logs

        except Exception as e:
            self.logger.error(f"查詢日誌失敗：{e}")
            return []

    def get_statistics(self, hours: int = 24) -> Dict:
        """
        獲取日誌統計信息

        參數：
            hours: 過去幾小時的統計

        返回值：
            統計信息字典
        """
        try:
            conn = sqlite3.connect(str(self.db_path))
            cursor = conn.cursor()

            since = (datetime.now() - timedelta(hours=hours)).isoformat()

            # 按級別統計
            cursor.execute("""
                SELECT level, COUNT(*) as count
                FROM logs
                WHERE timestamp > ?
                GROUP BY level
            """, (since,))

            level_stats = {row[0]: row[1] for row in cursor.fetchall()}

            # 按分類統計
            cursor.execute("""
                SELECT category, COUNT(*) as count
                FROM logs
                WHERE timestamp > ? AND category IS NOT NULL
                GROUP BY category
            """, (since,))

            category_stats = {row[0]: row[1] for row in cursor.fetchall()}

            # 性能統計
            cursor.execute("""
                SELECT
                    AVG(duration_ms) as avg_duration,
                    MAX(duration_ms) as max_duration,
                    MIN(duration_ms) as min_duration
                FROM logs
                WHERE timestamp > ? AND duration_ms IS NOT NULL
            """, (since,))

            perf_row = cursor.fetchone()
            perf_stats = {
                'avg_duration_ms': perf_row[0],
                'max_duration_ms': perf_row[1],
                'min_duration_ms': perf_row[2]
            }

            conn.close()

            return {
                'time_range_hours': hours,
                'level_statistics': level_stats,
                'category_statistics': category_stats,
                'performance_statistics': perf_stats
            }

        except Exception as e:
            self.logger.error(f"獲取統計信息失敗：{e}")
            return {}


# ============================================================================
# 示例和測試
# ============================================================================

def main():
    """主函數 - 演示日誌系統"""

    logger = StructuredLogger(
        name="etl_system",
        enable_json=True,
        enable_console=True,
        enable_db=True
    )

    logger.info("\n" + "=" * 80)
    logger.info("完整日誌系統 - 演示")
    logger.info("=" * 80 + "\n")

    # 設定上下文
    logger.set_context(
        user="admin",
        session_id="sess_12345",
        environment="production"
    )

    # 記錄各級別的日誌
    logger.debug("這是一條 DEBUG 日誌", category=LogCategory.SYSTEM.value)
    logger.info("這是一條 INFO 日誌", category=LogCategory.BUSINESS.value, order_id="ORD123")
    logger.warning("這是一條 WARNING 日誌", category=LogCategory.SYSTEM.value)
    logger.error("這是一條 ERROR 日誌", category=LogCategory.BUSINESS.value, error_code="ERR_001")

    # 審計日誌
    logger.audit(
        action="UPDATE",
        user="admin",
        resource="/orders/123",
        result="SUCCESS",
        fields_modified=["status", "amount"]
    )

    # 性能日誌
    logger.performance(
        operation="資料庫查詢",
        duration_ms=45.5,
        table="orders",
        record_count=1000
    )

    # 使用裝飾器追蹤性能
    @logger.track_performance("模擬操作")
    def slow_operation():
        """模擬一個耗時的操作"""
        time.sleep(0.5)
        return "完成"

    result = slow_operation()
    logger.info(f"操作結果：{result}")

    # 查詢日誌
    logger.info("\n【查詢日誌】")
    logs = logger.query_logs(limit=5)
    for log in logs:
        logger.info(f"  - [{log['level']}] {log['message']}")

    # 獲取統計信息
    logger.info("\n【統計信息】")
    stats = logger.get_statistics(hours=1)
    logger.info(f"日誌統計：{json.dumps(stats, indent=2, ensure_ascii=False, default=str)}")


if __name__ == "__main__":
    main()
