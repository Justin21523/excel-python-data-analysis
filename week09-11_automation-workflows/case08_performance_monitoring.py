"""
案例8：性能監控系統

功能概述：
- 實時性能監控（CPU、內存、磁盤）
- 操作耗時追蹤
- 資料庫查詢性能分析
- 性能告警和報告
- 性能趨勢分析

執行方式：
    python case08_performance_monitoring.py

作者：Data Engineering Team
版本：1.0.0
"""

import logging
import time
import psutil
import json
import sqlite3
from pathlib import Path
from datetime import datetime, timedelta
from typing import Dict, List, Optional, Callable
from dataclasses import dataclass, field, asdict
from enum import Enum
from functools import wraps
import threading


# ============================================================================
# 日誌配置
# ============================================================================

def setup_logging(log_dir: str = "./logs") -> logging.Logger:
    """設定日誌系統"""
    Path(log_dir).mkdir(exist_ok=True)

    logger = logging.getLogger("PerformanceMonitoring")
    logger.setLevel(logging.DEBUG)

    formatter = logging.Formatter(
        '%(asctime)s - %(name)s - %(levelname)s - [%(funcName)s:%(lineno)d] - %(message)s',
        datefmt='%Y-%m-%d %H:%M:%S'
    )

    file_handler = logging.FileHandler(
        f"{log_dir}/performance_{datetime.now().strftime('%Y%m%d')}.log"
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

class PerformanceMetricType(Enum):
    """性能指標類型"""
    OPERATION = "operation"  # 操作耗時
    CPU = "cpu"  # CPU 使用率
    MEMORY = "memory"  # 內存使用
    DISK = "disk"  # 磁盤使用
    DATABASE = "database"  # 資料庫查詢


@dataclass
class PerformanceMetric:
    """性能指標"""
    metric_id: str
    timestamp: datetime
    metric_type: PerformanceMetricType
    operation_name: str
    value: float  # 值
    unit: str  # 單位（ms, %, MB 等）
    threshold: Optional[float] = None  # 警告閾值
    is_alert: bool = False  # 是否超出閾值


@dataclass
class OperationMetrics:
    """操作性能指標"""
    operation_name: str
    start_time: datetime
    end_time: Optional[datetime] = None
    duration_ms: float = 0.0
    cpu_usage: float = 0.0  # %
    memory_used_mb: float = 0.0  # MB
    rows_processed: int = 0
    records_per_second: float = 0.0


# ============================================================================
# 性能監控引擎
# ============================================================================

class PerformanceMonitor:
    """
    性能監控引擎

    功能：
    1. 實時監控系統資源
    2. 追蹤操作耗時
    3. 性能告警
    4. 性能分析和報告
    """

    def __init__(
        self,
        database_path: str = "./performance_metrics.db",
        cpu_threshold: float = 80.0,
        memory_threshold: float = 85.0,
        operation_threshold_ms: float = 5000.0
    ):
        """
        初始化性能監控

        參數：
            database_path: 資料庫路徑
            cpu_threshold: CPU 使用率警告閾值（%）
            memory_threshold: 內存使用率警告閾值（%）
            operation_threshold_ms: 操作耗時警告閾值（毫秒）
        """
        self.database_path = database_path
        self.cpu_threshold = cpu_threshold
        self.memory_threshold = memory_threshold
        self.operation_threshold_ms = operation_threshold_ms

        self.metrics: List[PerformanceMetric] = []
        self.alerts: List[Dict] = []

        self._init_database()

        # 啟動後台監控線程
        self.monitoring = False
        self._start_background_monitoring()

        logger.info("性能監控引擎初始化完成")

    def _init_database(self) -> None:
        """初始化性能指標資料庫"""
        try:
            conn = sqlite3.connect(self.database_path)
            cursor = conn.cursor()

            # 性能指標表
            cursor.execute("""
                CREATE TABLE IF NOT EXISTS performance_metrics (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    metric_id TEXT UNIQUE,
                    timestamp TIMESTAMP,
                    metric_type TEXT,
                    operation_name TEXT,
                    value REAL,
                    unit TEXT,
                    threshold REAL,
                    is_alert BOOLEAN,
                    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
                )
            """)

            # 性能告警表
            cursor.execute("""
                CREATE TABLE IF NOT EXISTS performance_alerts (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    alert_id TEXT UNIQUE,
                    timestamp TIMESTAMP,
                    alert_type TEXT,
                    operation_name TEXT,
                    message TEXT,
                    metric_value REAL,
                    threshold REAL,
                    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
                )
            """)

            conn.commit()
            conn.close()
            logger.info("性能指標資料庫初始化完成")

        except Exception as e:
            logger.error(f"資料庫初始化失敗：{e}")
            raise

    def _start_background_monitoring(self) -> None:
        """啟動後台系統資源監控"""
        self.monitoring = True

        def monitor():
            while self.monitoring:
                try:
                    self._collect_system_metrics()
                    time.sleep(5)  # 每 5 秒收集一次
                except Exception as e:
                    logger.error(f"後台監控出錯：{e}")

        thread = threading.Thread(target=monitor, daemon=True)
        thread.start()

    def _collect_system_metrics(self) -> None:
        """收集系統資源指標"""
        try:
            # CPU 使用率
            cpu_percent = psutil.cpu_percent(interval=0.5)
            if cpu_percent > self.cpu_threshold:
                self._record_alert(
                    alert_type="CPU",
                    operation_name="system_monitor",
                    message=f"CPU 使用率過高：{cpu_percent:.1f}%",
                    metric_value=cpu_percent,
                    threshold=self.cpu_threshold
                )

            # 內存使用
            memory = psutil.virtual_memory()
            if memory.percent > self.memory_threshold:
                self._record_alert(
                    alert_type="MEMORY",
                    operation_name="system_monitor",
                    message=f"內存使用率過高：{memory.percent:.1f}%",
                    metric_value=memory.percent,
                    threshold=self.memory_threshold
                )

            # 記錄指標
            cpu_metric = PerformanceMetric(
                metric_id=f"cpu_{datetime.now().timestamp()}",
                timestamp=datetime.now(),
                metric_type=PerformanceMetricType.CPU,
                operation_name="system",
                value=cpu_percent,
                unit="%",
                threshold=self.cpu_threshold,
                is_alert=cpu_percent > self.cpu_threshold
            )

            memory_metric = PerformanceMetric(
                metric_id=f"memory_{datetime.now().timestamp()}",
                timestamp=datetime.now(),
                metric_type=PerformanceMetricType.MEMORY,
                operation_name="system",
                value=memory.percent,
                unit="%",
                threshold=self.memory_threshold,
                is_alert=memory.percent > self.memory_threshold
            )

            self._save_metrics([cpu_metric, memory_metric])

        except Exception as e:
            logger.warning(f"收集系統指標失敗：{e}")

    def track_operation(
        self,
        operation_name: str,
        threshold_ms: Optional[float] = None
    ):
        """
        操作性能追蹤裝飾器

        使用示例：
            @monitor.track_operation("資料讀取", threshold_ms=1000)
            def read_data():
                pass
        """
        threshold = threshold_ms or self.operation_threshold_ms

        def decorator(func):
            @wraps(func)
            def wrapper(*args, **kwargs):
                # 記錄開始時間和資源
                start_time = datetime.now()
                start_mem = psutil.Process().memory_info().rss / 1024 / 1024  # MB

                try:
                    result = func(*args, **kwargs)
                    return result
                finally:
                    # 記錄結束時間和資源
                    end_time = datetime.now()
                    end_mem = psutil.Process().memory_info().rss / 1024 / 1024  # MB

                    duration_ms = (end_time - start_time).total_seconds() * 1000
                    mem_used_mb = end_mem - start_mem

                    # 記錄性能
                    self.record_operation_metric(
                        operation_name=operation_name or func.__name__,
                        duration_ms=duration_ms,
                        memory_used_mb=mem_used_mb,
                        threshold_ms=threshold
                    )

            return wrapper
        return decorator

    def record_operation_metric(
        self,
        operation_name: str,
        duration_ms: float,
        memory_used_mb: float = 0.0,
        rows_processed: int = 0,
        threshold_ms: Optional[float] = None
    ) -> None:
        """
        記錄操作性能指標

        參數：
            operation_name: 操作名稱
            duration_ms: 耗時（毫秒）
            memory_used_mb: 內存使用（MB）
            rows_processed: 處理的記錄數
            threshold_ms: 警告閾值（毫秒）
        """
        threshold = threshold_ms or self.operation_threshold_ms
        is_alert = duration_ms > threshold

        metric = PerformanceMetric(
            metric_id=f"op_{operation_name}_{datetime.now().timestamp()}",
            timestamp=datetime.now(),
            metric_type=PerformanceMetricType.OPERATION,
            operation_name=operation_name,
            value=duration_ms,
            unit="ms",
            threshold=threshold,
            is_alert=is_alert
        )

        self._save_metric(metric)

        # 生成告警
        if is_alert:
            rps = (rows_processed / (duration_ms / 1000)) if duration_ms > 0 else 0
            self._record_alert(
                alert_type="PERFORMANCE",
                operation_name=operation_name,
                message=f"操作 '{operation_name}' 耗時過長：{duration_ms:.2f}ms（閾值：{threshold:.0f}ms）",
                metric_value=duration_ms,
                threshold=threshold
            )
            logger.warning(
                f"性能警告：{operation_name} - {duration_ms:.2f}ms，內存：{memory_used_mb:.2f}MB，速率：{rps:.0f} rps"
            )
        else:
            logger.info(
                f"操作完成：{operation_name} - {duration_ms:.2f}ms，內存：{memory_used_mb:.2f}MB"
            )

    def _save_metric(self, metric: PerformanceMetric) -> None:
        """保存單個指標"""
        self._save_metrics([metric])

    def _save_metrics(self, metrics: List[PerformanceMetric]) -> None:
        """保存指標到資料庫"""
        try:
            conn = sqlite3.connect(self.database_path)
            cursor = conn.cursor()

            for metric in metrics:
                cursor.execute("""
                    INSERT INTO performance_metrics
                    (metric_id, timestamp, metric_type, operation_name, value, unit, threshold, is_alert)
                    VALUES (?, ?, ?, ?, ?, ?, ?, ?)
                """, (
                    metric.metric_id,
                    metric.timestamp.isoformat(),
                    metric.metric_type.value,
                    metric.operation_name,
                    metric.value,
                    metric.unit,
                    metric.threshold,
                    metric.is_alert
                ))

            conn.commit()
            conn.close()

        except Exception as e:
            logger.error(f"保存指標失敗：{e}")

    def _record_alert(
        self,
        alert_type: str,
        operation_name: str,
        message: str,
        metric_value: float,
        threshold: float
    ) -> None:
        """記錄性能告警"""
        try:
            alert_id = f"ALERT_{datetime.now().strftime('%Y%m%d%H%M%S_%f')}"

            alert = {
                'alert_id': alert_id,
                'timestamp': datetime.now().isoformat(),
                'alert_type': alert_type,
                'operation_name': operation_name,
                'message': message,
                'metric_value': metric_value,
                'threshold': threshold
            }

            self.alerts.append(alert)

            # 保存到資料庫
            conn = sqlite3.connect(self.database_path)
            cursor = conn.cursor()

            cursor.execute("""
                INSERT INTO performance_alerts
                (alert_id, timestamp, alert_type, operation_name, message, metric_value, threshold)
                VALUES (?, ?, ?, ?, ?, ?, ?)
            """, (
                alert_id,
                alert['timestamp'],
                alert_type,
                operation_name,
                message,
                metric_value,
                threshold
            ))

            conn.commit()
            conn.close()

            logger.warning(f"性能告警：{message}")

        except Exception as e:
            logger.error(f"記錄告警失敗：{e}")

    def get_performance_summary(self, hours: int = 1) -> Dict:
        """
        獲取性能摘要

        參數：
            hours: 過去幾小時的摘要

        返回值：
            性能摘要字典
        """
        try:
            conn = sqlite3.connect(self.database_path)
            cursor = conn.cursor()

            since = (datetime.now() - timedelta(hours=hours)).isoformat()

            # 操作耗時統計
            cursor.execute("""
                SELECT operation_name, AVG(value) as avg_duration, MAX(value) as max_duration, COUNT(*) as count
                FROM performance_metrics
                WHERE metric_type = 'operation' AND timestamp > ?
                GROUP BY operation_name
            """, (since,))

            operation_stats = {}
            for row in cursor.fetchall():
                operation_stats[row[0]] = {
                    'avg_ms': row[1],
                    'max_ms': row[2],
                    'count': row[3]
                }

            # CPU 和內存統計
            cursor.execute("""
                SELECT metric_type, AVG(value) as avg_value, MAX(value) as max_value
                FROM performance_metrics
                WHERE metric_type IN ('cpu', 'memory') AND timestamp > ?
                GROUP BY metric_type
            """, (since,))

            resource_stats = {}
            for row in cursor.fetchall():
                resource_stats[row[0]] = {
                    'avg': row[1],
                    'max': row[2]
                }

            # 告警統計
            cursor.execute("""
                SELECT alert_type, COUNT(*) as count
                FROM performance_alerts
                WHERE timestamp > ?
                GROUP BY alert_type
            """, (since,))

            alert_stats = {row[0]: row[1] for row in cursor.fetchall()}

            conn.close()

            summary = {
                'time_range_hours': hours,
                'operation_statistics': operation_stats,
                'resource_statistics': resource_stats,
                'alert_statistics': alert_stats,
                'timestamp': datetime.now().isoformat()
            }

            return summary

        except Exception as e:
            logger.error(f"獲取性能摘要失敗：{e}")
            return {}

    def stop_monitoring(self) -> None:
        """停止後台監控"""
        self.monitoring = False
        logger.info("後台監控已停止")


# ============================================================================
# 示例和測試
# ============================================================================

def main():
    """主函數 - 演示性能監控"""

    logger.info("\n" + "=" * 80)
    logger.info("性能監控系統 - 演示")
    logger.info("=" * 80 + "\n")

    monitor = PerformanceMonitor()

    # 定義被監控的操作
    @monitor.track_operation("快速操作", threshold_ms=500)
    def fast_operation():
        """快速操作"""
        time.sleep(0.1)
        return "完成"

    @monitor.track_operation("慢速操作", threshold_ms=500)
    def slow_operation():
        """慢速操作（超出閾值）"""
        time.sleep(2)
        return "完成"

    # 執行操作
    logger.info("執行快速操作...")
    result1 = fast_operation()

    logger.info("\n執行慢速操作...")
    result2 = slow_operation()

    # 手動記錄大資料操作
    logger.info("\n模擬大資料操作...")
    import pandas as pd
    df = pd.DataFrame({'a': range(100000)})

    start = time.time()
    result = df['a'].sum()
    duration = (time.time() - start) * 1000

    monitor.record_operation_metric(
        operation_name="大資料求和",
        duration_ms=duration,
        rows_processed=len(df)
    )

    # 等待後台監控收集數據
    time.sleep(2)

    # 獲取性能摘要
    logger.info("\n" + "=" * 60)
    logger.info("性能摘要：")
    logger.info("=" * 60)
    summary = monitor.get_performance_summary(hours=1)
    logger.info(json.dumps(summary, indent=2, ensure_ascii=False, default=str))

    # 停止監控
    monitor.stop_monitoring()


if __name__ == "__main__":
    main()
