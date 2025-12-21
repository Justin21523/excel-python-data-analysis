"""
案例11：任務調度系統

功能概述：
- 基於時間的任務調度（Cron 表達式）
- 任務優先級和依賴關係
- 任務狀態追蹤
- 調度日誌和報告
- 失敗重試和恢復

執行方式：
    python case11_scheduling.py

前提：
    pip install APScheduler

作者：Data Engineering Team
版本：1.0.0
"""

import logging
import json
import sqlite3
from pathlib import Path
from datetime import datetime, timedelta
from typing import Dict, List, Optional, Callable, Any
from dataclasses import dataclass, field, asdict
from enum import Enum
import schedule
import time
import threading


# ============================================================================
# 日誌配置
# ============================================================================

def setup_logging(log_dir: str = "./logs") -> logging.Logger:
    """設定日誌系統"""
    Path(log_dir).mkdir(exist_ok=True)

    logger = logging.getLogger("TaskScheduling")
    logger.setLevel(logging.DEBUG)

    formatter = logging.Formatter(
        '%(asctime)s - %(name)s - %(levelname)s - [%(funcName)s:%(lineno)d] - %(message)s',
        datefmt='%Y-%m-%d %H:%M:%S'
    )

    file_handler = logging.FileHandler(
        f"{log_dir}/scheduling_{datetime.now().strftime('%Y%m%d')}.log"
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

class TaskStatus(Enum):
    """任務狀態"""
    PENDING = "pending"  # 待執行
    RUNNING = "running"  # 執行中
    SUCCESS = "success"  # 成功
    FAILED = "failed"  # 失敗
    RETRY = "retry"  # 重試
    CANCELLED = "cancelled"  # 取消


class TaskPriority(Enum):
    """任務優先級"""
    LOW = 1
    NORMAL = 2
    HIGH = 3
    CRITICAL = 4


@dataclass
class ScheduledTask:
    """計劃的任務"""
    task_id: str
    task_name: str
    task_func: Callable
    schedule_pattern: str  # Cron 表達式或 "daily", "hourly" 等
    priority: TaskPriority = TaskPriority.NORMAL
    enabled: bool = True
    max_retries: int = 3
    timeout_seconds: Optional[int] = None
    dependencies: List[str] = field(default_factory=list)  # 依賴的任務 ID
    next_run: Optional[datetime] = None
    last_run: Optional[datetime] = None
    status: TaskStatus = TaskStatus.PENDING
    failure_count: int = 0


@dataclass
class TaskExecution:
    """任務執行記錄"""
    execution_id: str
    task_id: str
    task_name: str
    start_time: datetime
    end_time: Optional[datetime] = None
    duration_seconds: float = 0.0
    status: TaskStatus = TaskStatus.PENDING
    result: Optional[Any] = None
    error_message: Optional[str] = None
    retry_count: int = 0


# ============================================================================
# 任務調度引擎
# ============================================================================

class TaskScheduler:
    """
    任務調度引擎

    功能：
    1. 基於時間的任務調度
    2. 任務優先級和依賴管理
    3. 失敗重試
    4. 任務狀態追蹤
    5. 調度報告
    """

    def __init__(self):
        """初始化任務調度引擎"""
        self.tasks: Dict[str, ScheduledTask] = {}
        self.scheduler = schedule.Scheduler()
        self.running = False
        self.executions: List[TaskExecution] = []

        self._init_database()

        logger.info("任務調度引擎初始化完成")

    def _init_database(self) -> None:
        """初始化調度資料庫"""
        try:
            conn = sqlite3.connect("./task_scheduling.db")
            cursor = conn.cursor()

            # 任務表
            cursor.execute("""
                CREATE TABLE IF NOT EXISTS tasks (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    task_id TEXT UNIQUE,
                    task_name TEXT,
                    schedule_pattern TEXT,
                    priority TEXT,
                    enabled BOOLEAN,
                    max_retries INTEGER,
                    next_run TIMESTAMP,
                    last_run TIMESTAMP,
                    status TEXT,
                    failure_count INTEGER,
                    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
                )
            """)

            # 執行歷史表
            cursor.execute("""
                CREATE TABLE IF NOT EXISTS task_executions (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    execution_id TEXT UNIQUE,
                    task_id TEXT,
                    task_name TEXT,
                    start_time TIMESTAMP,
                    end_time TIMESTAMP,
                    duration_seconds REAL,
                    status TEXT,
                    result TEXT,
                    error_message TEXT,
                    retry_count INTEGER,
                    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
                )
            """)

            conn.commit()
            conn.close()
            logger.info("調度資料庫初始化完成")

        except Exception as e:
            logger.error(f"資料庫初始化失敗：{e}")

    def add_task(
        self,
        task_id: str,
        task_name: str,
        task_func: Callable,
        schedule_pattern: str,
        priority: TaskPriority = TaskPriority.NORMAL,
        max_retries: int = 3,
        timeout_seconds: Optional[int] = None,
        dependencies: Optional[List[str]] = None
    ) -> None:
        """
        添加計劃任務

        參數：
            task_id: 任務 ID
            task_name: 任務名稱
            task_func: 任務函數
            schedule_pattern: 調度模式（"daily", "hourly", "every_5m" 等）
            priority: 優先級
            max_retries: 最大重試次數
            timeout_seconds: 超時時間（秒）
            dependencies: 依賴的任務 ID 列表
        """
        task = ScheduledTask(
            task_id=task_id,
            task_name=task_name,
            task_func=task_func,
            schedule_pattern=schedule_pattern,
            priority=priority,
            max_retries=max_retries,
            timeout_seconds=timeout_seconds,
            dependencies=dependencies or []
        )

        self.tasks[task_id] = task

        # 設置調度
        self._setup_task_schedule(task)

        logger.info(f"已添加任務：{task_name} ({task_id})")

    def _setup_task_schedule(self, task: ScheduledTask) -> None:
        """
        設置任務調度

        參數：
            task: 任務對象
        """
        try:
            # 解析調度模式
            if task.schedule_pattern == "daily":
                self.scheduler.every().day.do(self._execute_task, task_id=task.task_id)
            elif task.schedule_pattern == "hourly":
                self.scheduler.every().hour.do(self._execute_task, task_id=task.task_id)
            elif task.schedule_pattern.startswith("every_"):
                # 如 "every_5m", "every_30m"
                parts = task.schedule_pattern.split("_")
                if len(parts) == 2:
                    interval = int(parts[1].rstrip("mh"))
                    unit = parts[1][-1]
                    if unit == 'm':
                        self.scheduler.every(interval).minutes.do(self._execute_task, task_id=task.task_id)
                    elif unit == 'h':
                        self.scheduler.every(interval).hours.do(self._execute_task, task_id=task.task_id)
            elif ":" in task.schedule_pattern:
                # 如 "09:30" - 每天固定時間
                time_parts = task.schedule_pattern.split(":")
                hour, minute = int(time_parts[0]), int(time_parts[1])
                self.scheduler.every().day.at(task.schedule_pattern).do(
                    self._execute_task, task_id=task.task_id
                )

            logger.info(f"任務 {task.task_name} 調度設置完成：{task.schedule_pattern}")

        except Exception as e:
            logger.error(f"設置任務調度失敗：{e}")

    def _execute_task(self, task_id: str) -> None:
        """
        執行任務

        參數：
            task_id: 任務 ID
        """
        if task_id not in self.tasks:
            logger.error(f"任務不存在：{task_id}")
            return

        task = self.tasks[task_id]

        # 檢查依賴任務
        if task.dependencies and not self._check_dependencies(task):
            logger.warning(f"任務 {task.task_name} 的依賴任務未完成，跳過執行")
            return

        execution = TaskExecution(
            execution_id=f"exec_{datetime.now().strftime('%Y%m%d%H%M%S_%f')}",
            task_id=task_id,
            task_name=task.task_name,
            start_time=datetime.now(),
            status=TaskStatus.RUNNING
        )

        logger.info(f"開始執行任務：{task.task_name}")

        try:
            # 執行任務函數
            result = task.task_func()

            execution.end_time = datetime.now()
            execution.duration_seconds = (execution.end_time - execution.start_time).total_seconds()
            execution.status = TaskStatus.SUCCESS
            execution.result = str(result)

            task.last_run = datetime.now()
            task.status = TaskStatus.SUCCESS
            task.failure_count = 0

            logger.info(f"任務執行成功：{task.task_name}（耗時 {execution.duration_seconds:.2f} 秒）")

        except Exception as e:
            execution.end_time = datetime.now()
            execution.duration_seconds = (execution.end_time - execution.start_time).total_seconds()
            execution.error_message = str(e)

            # 重試邏輯
            if task.failure_count < task.max_retries:
                task.failure_count += 1
                execution.status = TaskStatus.RETRY
                execution.retry_count = task.failure_count

                logger.warning(
                    f"任務執行失敗：{task.task_name}，進行重試（{task.failure_count}/{task.max_retries}）"
                )

                # 重新調度重試
                self.scheduler.every(1).minutes.do(self._execute_task, task_id=task_id)

            else:
                execution.status = TaskStatus.FAILED
                task.status = TaskStatus.FAILED

                logger.error(f"任務執行失敗：{task.task_name}，重試次數已達上限")

        # 記錄執行
        self.executions.append(execution)
        self._log_execution(execution)

    def _check_dependencies(self, task: ScheduledTask) -> bool:
        """
        檢查任務依賴是否滿足

        參數：
            task: 任務

        返回值：
            依賴是否全部滿足
        """
        for dep_id in task.dependencies:
            if dep_id not in self.tasks:
                logger.warning(f"依賴的任務不存在：{dep_id}")
                return False

            dep_task = self.tasks[dep_id]
            if dep_task.status != TaskStatus.SUCCESS:
                return False

        return True

    def _log_execution(self, execution: TaskExecution) -> None:
        """記錄任務執行"""
        try:
            conn = sqlite3.connect("./task_scheduling.db")
            cursor = conn.cursor()

            cursor.execute("""
                INSERT INTO task_executions
                (execution_id, task_id, task_name, start_time, end_time, duration_seconds, status, result, error_message, retry_count)
                VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
            """, (
                execution.execution_id,
                execution.task_id,
                execution.task_name,
                execution.start_time.isoformat(),
                execution.end_time.isoformat() if execution.end_time else None,
                execution.duration_seconds,
                execution.status.value,
                execution.result,
                execution.error_message,
                execution.retry_count
            ))

            conn.commit()
            conn.close()

        except Exception as e:
            logger.error(f"記錄任務執行失敗：{e}")

    def start(self) -> None:
        """
        啟動任務調度器（後台線程）
        """
        if self.running:
            logger.warning("調度器已在運行")
            return

        self.running = True

        def scheduler_loop():
            logger.info("任務調度器已啟動")
            while self.running:
                try:
                    self.scheduler.run_pending()
                    time.sleep(1)  # 每秒檢查一次
                except Exception as e:
                    logger.error(f"調度器出錯：{e}")

        thread = threading.Thread(target=scheduler_loop, daemon=True)
        thread.start()

    def stop(self) -> None:
        """停止任務調度器"""
        self.running = False
        logger.info("任務調度器已停止")

    def get_task_status(self, task_id: str) -> Optional[Dict]:
        """
        獲取任務狀態

        參數：
            task_id: 任務 ID

        返回值：
            任務狀態字典或 None
        """
        if task_id not in self.tasks:
            return None

        task = self.tasks[task_id]
        return {
            'task_id': task.task_id,
            'task_name': task.task_name,
            'status': task.status.value,
            'last_run': task.last_run.isoformat() if task.last_run else None,
            'failure_count': task.failure_count,
            'enabled': task.enabled,
            'priority': task.priority.value
        }

    def get_all_tasks_status(self) -> List[Dict]:
        """
        獲取所有任務狀態

        返回值：
            任務狀態列表
        """
        return [self.get_task_status(task_id) for task_id in self.tasks.keys()]

    def get_execution_history(self, task_id: Optional[str] = None, limit: int = 50) -> List[Dict]:
        """
        獲取執行歷史

        參數：
            task_id: 任務 ID（可選）
            limit: 限制記錄數

        返回值：
            執行記錄列表
        """
        try:
            conn = sqlite3.connect("./task_scheduling.db")
            cursor = conn.cursor()

            if task_id:
                cursor.execute("""
                    SELECT * FROM task_executions
                    WHERE task_id = ?
                    ORDER BY start_time DESC
                    LIMIT ?
                """, (task_id, limit))
            else:
                cursor.execute("""
                    SELECT * FROM task_executions
                    ORDER BY start_time DESC
                    LIMIT ?
                """, (limit,))

            columns = [desc[0] for desc in cursor.description]
            results = [dict(zip(columns, row)) for row in cursor.fetchall()]

            conn.close()
            return results

        except Exception as e:
            logger.error(f"查詢執行歷史失敗：{e}")
            return []

    def get_scheduler_report(self) -> Dict:
        """
        獲取調度器報告

        返回值：
            報告字典
        """
        total_tasks = len(self.tasks)
        enabled_tasks = sum(1 for t in self.tasks.values() if t.enabled)
        successful_tasks = sum(1 for t in self.tasks.values() if t.status == TaskStatus.SUCCESS)
        failed_tasks = sum(1 for t in self.tasks.values() if t.status == TaskStatus.FAILED)

        return {
            'timestamp': datetime.now().isoformat(),
            'total_tasks': total_tasks,
            'enabled_tasks': enabled_tasks,
            'successful_tasks': successful_tasks,
            'failed_tasks': failed_tasks,
            'total_executions': len(self.executions),
            'scheduler_running': self.running,
            'tasks_status': self.get_all_tasks_status()
        }


# ============================================================================
# 示例和測試
# ============================================================================

def main():
    """主函數 - 演示任務調度"""

    logger.info("\n" + "=" * 80)
    logger.info("任務調度系統 - 演示")
    logger.info("=" * 80 + "\n")

    # 定義示例任務
    def daily_etl():
        """每日 ETL 任務"""
        logger.info("執行每日 ETL...")
        time.sleep(1)  # 模擬耗時操作
        return "ETL 成功執行"

    def hourly_data_quality_check():
        """每小時資料品質檢查"""
        logger.info("執行資料品質檢查...")
        time.sleep(1)
        return "品質檢查完成"

    def send_daily_report():
        """發送每日報告"""
        logger.info("發送每日報告...")
        time.sleep(1)
        return "報告已發送"

    # 創建調度器
    scheduler = TaskScheduler()

    # 添加任務
    scheduler.add_task(
        task_id="daily_etl",
        task_name="每日 ETL",
        task_func=daily_etl,
        schedule_pattern="daily",
        priority=TaskPriority.HIGH
    )

    scheduler.add_task(
        task_id="hourly_quality_check",
        task_name="每小時品質檢查",
        task_func=hourly_data_quality_check,
        schedule_pattern="hourly",
        priority=TaskPriority.NORMAL
    )

    scheduler.add_task(
        task_id="send_report",
        task_name="發送每日報告",
        task_func=send_daily_report,
        schedule_pattern="daily",
        priority=TaskPriority.NORMAL,
        dependencies=["daily_etl"]  # 依賴 daily_etl
    )

    # 啟動調度器
    scheduler.start()

    # 演示：手動執行任務
    logger.info("\n【手動執行任務演示】")
    scheduler._execute_task("daily_etl")
    scheduler._execute_task("hourly_quality_check")

    # 獲取調度器報告
    logger.info("\n" + "=" * 60)
    logger.info("調度器報告：")
    logger.info("=" * 60)
    report = scheduler.get_scheduler_report()
    logger.info(json.dumps(report, indent=2, ensure_ascii=False))

    # 獲取執行歷史
    logger.info("\n【執行歷史】")
    history = scheduler.get_execution_history(limit=5)
    for record in history:
        logger.info(f"  - {record['task_name']}: {record['status']} ({record['duration_seconds']:.2f}s)")

    # 停止調度器
    time.sleep(2)
    scheduler.stop()


if __name__ == "__main__":
    main()
