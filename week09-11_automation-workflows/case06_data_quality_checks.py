"""
案例6：資料品質自動檢查系統

功能概述：
- 自動化的資料品質檢查
- 多維度檢查（完整性、準確性、一致性、時效性）
- 質量評分
- 異常報告和告警
- 品質歷史追蹤

執行方式：
    python case06_data_quality_checks.py

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
from typing import Dict, List, Tuple, Optional, Any, Callable
from dataclasses import dataclass, field, asdict
from enum import Enum
from abc import ABC, abstractmethod


# ============================================================================
# 日誌配置
# ============================================================================

def setup_logging(log_dir: str = "./logs") -> logging.Logger:
    """設定日誌系統"""
    Path(log_dir).mkdir(exist_ok=True)

    logger = logging.getLogger("DataQuality")
    logger.setLevel(logging.DEBUG)

    formatter = logging.Formatter(
        '%(asctime)s - %(name)s - %(levelname)s - [%(funcName)s:%(lineno)d] - %(message)s',
        datefmt='%Y-%m-%d %H:%M:%S'
    )

    file_handler = logging.FileHandler(
        f"{log_dir}/data_quality_{datetime.now().strftime('%Y%m%d')}.log"
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

class QualityDimension(Enum):
    """品質維度"""
    COMPLETENESS = "completeness"  # 完整性（缺少值）
    ACCURACY = "accuracy"  # 準確性（格式、範圍）
    CONSISTENCY = "consistency"  # 一致性（跨欄位、跨表）
    TIMELINESS = "timeliness"  # 時效性（過時資料）
    UNIQUENESS = "uniqueness"  # 唯一性（重複）


class QualityLevel(Enum):
    """品質級別"""
    EXCELLENT = "excellent"  # 優秀：95-100%
    GOOD = "good"  # 良好：85-95%
    ACCEPTABLE = "acceptable"  # 可接受：75-85%
    POOR = "poor"  # 差：< 75%


@dataclass
class QualityIssue:
    """品質問題"""
    issue_id: str
    dimension: QualityDimension
    severity: str  # 'high', 'medium', 'low'
    column: Optional[str]
    row_count: int
    sample_values: List[Any]
    description: str
    recommendation: str


@dataclass
class QualityCheckResult:
    """品質檢查結果"""
    check_id: str
    timestamp: datetime
    data_source: str
    total_records: int
    quality_score: float  # 0-100
    quality_level: QualityLevel
    dimensions: Dict[str, float]  # 各維度得分
    issues: List[QualityIssue] = field(default_factory=list)
    alerts: List[str] = field(default_factory=list)


# ============================================================================
# 品質檢查基類和具體實現
# ============================================================================

class QualityCheck(ABC):
    """品質檢查抽象基類"""

    def __init__(self, name: str, dimension: QualityDimension, weight: float = 1.0):
        """
        初始化品質檢查

        參數：
            name: 檢查名稱
            dimension: 品質維度
            weight: 權重（用於計算總分）
        """
        self.name = name
        self.dimension = dimension
        self.weight = weight

    @abstractmethod
    def check(self, df: pd.DataFrame, **kwargs) -> Tuple[float, List[QualityIssue]]:
        """
        執行品質檢查

        返回值：
            (維度得分 0-100, 問題列表)
        """
        pass


class CompletenessCheck(QualityCheck):
    """完整性檢查"""

    def __init__(self, required_columns: Optional[List[str]] = None):
        """
        初始化完整性檢查

        參數：
            required_columns: 必填欄位列表
        """
        super().__init__(
            name="完整性檢查",
            dimension=QualityDimension.COMPLETENESS,
            weight=0.25
        )
        self.required_columns = required_columns or []

    def check(self, df: pd.DataFrame, **kwargs) -> Tuple[float, List[QualityIssue]]:
        """檢查資料完整性"""
        issues = []

        if df.empty:
            return 0.0, [
                QualityIssue(
                    issue_id="completeness_001",
                    dimension=self.dimension,
                    severity="high",
                    column=None,
                    row_count=0,
                    sample_values=[],
                    description="資料框為空",
                    recommendation="檢查資料源是否有數據"
                )
            ]

        # 檢查必填欄位
        missing_columns = [col for col in self.required_columns if col not in df.columns]
        if missing_columns:
            return 0.0, [
                QualityIssue(
                    issue_id="completeness_002",
                    dimension=self.dimension,
                    severity="high",
                    column=None,
                    row_count=len(missing_columns),
                    sample_values=missing_columns,
                    description=f"缺少必填欄位：{missing_columns}",
                    recommendation="檢查資料源是否包含所有必需的欄位"
                )
            ]

        # 檢查空值
        total_cells = len(df) * len(df.columns)
        null_count = df.isnull().sum().sum()

        for col in df.columns:
            null_in_col = df[col].isnull().sum()
            if null_in_col > 0:
                issues.append(
                    QualityIssue(
                        issue_id=f"completeness_{col}",
                        dimension=self.dimension,
                        severity="medium" if null_in_col / len(df) < 0.1 else "high",
                        column=col,
                        row_count=null_in_col,
                        sample_values=df[df[col].isnull()].index.tolist()[:5],
                        description=f"欄位 {col} 有 {null_in_col} 個空值（{null_in_col/len(df)*100:.1f}%）",
                        recommendation="填充空值或移除不完整的記錄"
                    )
                )

        # 計算完整性得分
        completeness_score = ((total_cells - null_count) / total_cells) * 100

        logger.info(f"完整性檢查：{completeness_score:.2f}%")

        return completeness_score, issues


class AccuracyCheck(QualityCheck):
    """準確性檢查"""

    def __init__(self, validation_rules: Optional[Dict[str, Callable]] = None):
        """
        初始化準確性檢查

        參數：
            validation_rules: 驗證規則字典 {欄位名: 驗證函數}
        """
        super().__init__(
            name="準確性檢查",
            dimension=QualityDimension.ACCURACY,
            weight=0.25
        )
        self.validation_rules = validation_rules or {}

    def check(self, df: pd.DataFrame, **kwargs) -> Tuple[float, List[QualityIssue]]:
        """檢查資料準確性"""
        issues = []
        invalid_count = 0

        for col, rule_func in self.validation_rules.items():
            if col not in df.columns:
                continue

            try:
                # 應用驗證規則
                invalid_mask = ~df[col].apply(rule_func)
                invalid_in_col = invalid_mask.sum()

                if invalid_in_col > 0:
                    invalid_count += invalid_in_col
                    issues.append(
                        QualityIssue(
                            issue_id=f"accuracy_{col}",
                            dimension=self.dimension,
                            severity="high" if invalid_in_col / len(df) > 0.05 else "medium",
                            column=col,
                            row_count=invalid_in_col,
                            sample_values=df.loc[invalid_mask, col].unique().tolist()[:5],
                            description=f"欄位 {col} 有 {invalid_in_col} 個無效值",
                            recommendation="檢查資料格式和數值範圍"
                        )
                    )

            except Exception as e:
                logger.warning(f"驗證欄位 {col} 時出錯：{e}")

        # 計算準確性得分
        total_cells = len(df) * len(self.validation_rules)
        accuracy_score = ((total_cells - invalid_count) / max(total_cells, 1)) * 100

        logger.info(f"準確性檢查：{accuracy_score:.2f}%")

        return accuracy_score, issues


class ConsistencyCheck(QualityCheck):
    """一致性檢查"""

    def __init__(self, consistency_rules: Optional[Dict[str, Callable]] = None):
        """
        初始化一致性檢查

        參數：
            consistency_rules: 一致性規則字典 {規則名: 檢查函數}
        """
        super().__init__(
            name="一致性檢查",
            dimension=QualityDimension.CONSISTENCY,
            weight=0.20
        )
        self.consistency_rules = consistency_rules or {}

    def check(self, df: pd.DataFrame, **kwargs) -> Tuple[float, List[QualityIssue]]:
        """檢查資料一致性"""
        issues = []
        violations = 0

        for rule_name, rule_func in self.consistency_rules.items():
            try:
                result = rule_func(df)

                if isinstance(result, tuple):
                    is_consistent, violation_count, sample_rows = result
                else:
                    is_consistent = result
                    violation_count = 0 if is_consistent else len(df)
                    sample_rows = []

                if not is_consistent:
                    violations += violation_count
                    issues.append(
                        QualityIssue(
                            issue_id=f"consistency_{rule_name}",
                            dimension=self.dimension,
                            severity="medium",
                            column=None,
                            row_count=violation_count,
                            sample_values=sample_rows[:5],
                            description=f"一致性規則 '{rule_name}' 違反，{violation_count} 條記錄不符合規則",
                            recommendation="檢查跨欄位和跨表的數據關係"
                        )
                    )

            except Exception as e:
                logger.warning(f"執行一致性檢查 {rule_name} 時出錯：{e}")

        # 計算一致性得分
        consistency_score = (1 - (violations / max(len(df), 1))) * 100

        logger.info(f"一致性檢查：{consistency_score:.2f}%")

        return consistency_score, issues


class TimelinessCheck(QualityCheck):
    """時效性檢查"""

    def __init__(self, timestamp_column: str, max_age_days: int = 30):
        """
        初始化時效性檢查

        參數：
            timestamp_column: 時間戳欄位名
            max_age_days: 最大年齡（天數）
        """
        super().__init__(
            name="時效性檢查",
            dimension=QualityDimension.TIMELINESS,
            weight=0.15
        )
        self.timestamp_column = timestamp_column
        self.max_age_days = max_age_days

    def check(self, df: pd.DataFrame, **kwargs) -> Tuple[float, List[QualityIssue]]:
        """檢查資料時效性"""
        issues = []

        if self.timestamp_column not in df.columns:
            logger.warning(f"時間戳欄位 {self.timestamp_column} 不存在")
            return 100.0, []

        try:
            # 轉換為 datetime
            df_temp = df.copy()
            df_temp[self.timestamp_column] = pd.to_datetime(df_temp[self.timestamp_column])

            now = datetime.now()
            max_age = now - timedelta(days=self.max_age_days)

            # 找出過時的記錄
            outdated_mask = df_temp[self.timestamp_column] < max_age
            outdated_count = outdated_mask.sum()

            if outdated_count > 0:
                issues.append(
                    QualityIssue(
                        issue_id="timeliness_001",
                        dimension=self.dimension,
                        severity="medium",
                        column=self.timestamp_column,
                        row_count=outdated_count,
                        sample_values=df_temp.loc[outdated_mask, self.timestamp_column].unique().tolist()[:5],
                        description=f"發現 {outdated_count} 條超過 {self.max_age_days} 天的過時記錄",
                        recommendation="更新或移除過時的資料"
                    )
                )

            # 計算時效性得分
            timeliness_score = (1 - (outdated_count / max(len(df), 1))) * 100

        except Exception as e:
            logger.warning(f"時效性檢查失敗：{e}")
            timeliness_score = 100.0

        logger.info(f"時效性檢查：{timeliness_score:.2f}%")

        return timeliness_score, issues


class UniquenessCheck(QualityCheck):
    """唯一性檢查"""

    def __init__(self, key_columns: Optional[List[str]] = None):
        """
        初始化唯一性檢查

        參數：
            key_columns: 鍵欄位列表
        """
        super().__init__(
            name="唯一性檢查",
            dimension=QualityDimension.UNIQUENESS,
            weight=0.15
        )
        self.key_columns = key_columns or []

    def check(self, df: pd.DataFrame, **kwargs) -> Tuple[float, List[QualityIssue]]:
        """檢查唯一性"""
        issues = []

        if not self.key_columns:
            return 100.0, []

        # 過濾存在的欄位
        valid_keys = [col for col in self.key_columns if col in df.columns]

        if not valid_keys:
            return 100.0, []

        # 檢查重複
        duplicates = df[valid_keys].duplicated()
        duplicate_count = duplicates.sum()

        if duplicate_count > 0:
            issues.append(
                QualityIssue(
                    issue_id="uniqueness_001",
                    dimension=self.dimension,
                    severity="high",
                    column=",".join(valid_keys),
                    row_count=duplicate_count,
                    sample_values=df[duplicates].head().values.tolist(),
                    description=f"發現 {duplicate_count} 條重複記錄（基於鍵 {valid_keys}）",
                    recommendation="移除或合併重複記錄"
                )
            )

        # 計算唯一性得分
        uniqueness_score = (1 - (duplicate_count / max(len(df), 1))) * 100

        logger.info(f"唯一性檢查：{uniqueness_score:.2f}%")

        return uniqueness_score, issues


# ============================================================================
# 品質檢查引擎
# ============================================================================

class DataQualityEngine:
    """
    資料品質檢查引擎

    核心功能：
    1. 執行多維度品質檢查
    2. 計算品質評分
    3. 生成品質報告
    4. 追蹤品質歷史
    5. 發出品質告警
    """

    def __init__(self, database_path: str = "./data_quality.db"):
        """
        初始化品質檢查引擎

        參數：
            database_path: 資料庫路徑
        """
        self.database_path = database_path
        self.checks: List[QualityCheck] = []
        self.results: List[QualityCheckResult] = []

        self._init_database()

        logger.info("資料品質檢查引擎初始化完成")

    def _init_database(self) -> None:
        """初始化品質追蹤資料庫"""
        try:
            conn = sqlite3.connect(self.database_path)
            cursor = conn.cursor()

            # 品質檢查結果表
            cursor.execute("""
                CREATE TABLE IF NOT EXISTS quality_results (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    check_id TEXT UNIQUE,
                    timestamp TIMESTAMP,
                    data_source TEXT,
                    total_records INTEGER,
                    quality_score REAL,
                    quality_level TEXT,
                    dimensions TEXT,
                    issues_count INTEGER,
                    alerts TEXT,
                    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
                )
            """)

            # 品質問題表
            cursor.execute("""
                CREATE TABLE IF NOT EXISTS quality_issues (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    check_id TEXT,
                    issue_id TEXT,
                    dimension TEXT,
                    severity TEXT,
                    column_name TEXT,
                    row_count INTEGER,
                    description TEXT,
                    recommendation TEXT,
                    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
                )
            """)

            conn.commit()
            conn.close()
            logger.info("品質追蹤資料庫初始化完成")

        except Exception as e:
            logger.error(f"資料庫初始化失敗：{e}")
            raise

    def add_check(self, check: QualityCheck) -> None:
        """添加品質檢查"""
        self.checks.append(check)
        logger.info(f"已添加檢查：{check.name}")

    def run_checks(
        self,
        df: pd.DataFrame,
        data_source: str = "unknown"
    ) -> QualityCheckResult:
        """
        執行所有品質檢查

        參數：
            df: 待檢查的 DataFrame
            data_source: 資料源名稱

        返回值：
            檢查結果
        """
        logger.info("=" * 60)
        logger.info("開始執行品質檢查")
        logger.info("=" * 60)

        check_id = f"QC_{datetime.now().strftime('%Y%m%d%H%M%S')}"

        dimension_scores = {}
        all_issues = []
        alerts = []

        # 執行每個檢查
        for check in self.checks:
            score, issues = check.check(df)
            dimension_scores[check.dimension.value] = score

            if issues:
                all_issues.extend(issues)

            # 生成告警
            if score < 80:
                alert = f"警告：{check.name}得分低於 80%（當前：{score:.2f}%）"
                alerts.append(alert)
                logger.warning(alert)

        # 計算總體得分
        total_score = self._calculate_total_score(dimension_scores)

        # 確定品質級別
        if total_score >= 95:
            quality_level = QualityLevel.EXCELLENT
        elif total_score >= 85:
            quality_level = QualityLevel.GOOD
        elif total_score >= 75:
            quality_level = QualityLevel.ACCEPTABLE
        else:
            quality_level = QualityLevel.POOR

        result = QualityCheckResult(
            check_id=check_id,
            timestamp=datetime.now(),
            data_source=data_source,
            total_records=len(df),
            quality_score=total_score,
            quality_level=quality_level,
            dimensions=dimension_scores,
            issues=all_issues,
            alerts=alerts
        )

        self.results.append(result)

        # 保存到資料庫
        self._save_result(result)

        logger.info(f"品質檢查完成，總分：{total_score:.2f}%（{quality_level.value}）")

        return result

    def _calculate_total_score(self, dimension_scores: Dict[str, float]) -> float:
        """
        計算總體品質得分

        參數：
            dimension_scores: 各維度得分

        返回值：
            加權平均得分
        """
        if not dimension_scores:
            return 0.0

        # 簡化的加權平均（可根據需要調整權重）
        weights = {
            QualityDimension.COMPLETENESS.value: 0.25,
            QualityDimension.ACCURACY.value: 0.25,
            QualityDimension.CONSISTENCY.value: 0.20,
            QualityDimension.TIMELINESS.value: 0.15,
            QualityDimension.UNIQUENESS.value: 0.15,
        }

        total = 0
        weight_sum = 0

        for dimension, score in dimension_scores.items():
            weight = weights.get(dimension, 0.1)
            total += score * weight
            weight_sum += weight

        return total / max(weight_sum, 1)

    def _save_result(self, result: QualityCheckResult) -> None:
        """保存檢查結果到資料庫"""
        try:
            conn = sqlite3.connect(self.database_path)
            cursor = conn.cursor()

            cursor.execute("""
                INSERT INTO quality_results
                (check_id, timestamp, data_source, total_records, quality_score, quality_level, dimensions, issues_count, alerts)
                VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?)
            """, (
                result.check_id,
                result.timestamp.isoformat(),
                result.data_source,
                result.total_records,
                result.quality_score,
                result.quality_level.value,
                json.dumps(result.dimensions),
                len(result.issues),
                json.dumps(result.alerts)
            ))

            # 保存問題詳情
            for issue in result.issues:
                cursor.execute("""
                    INSERT INTO quality_issues
                    (check_id, issue_id, dimension, severity, column_name, row_count, description, recommendation)
                    VALUES (?, ?, ?, ?, ?, ?, ?, ?)
                """, (
                    result.check_id,
                    issue.issue_id,
                    issue.dimension.value,
                    issue.severity,
                    issue.column,
                    issue.row_count,
                    issue.description,
                    issue.recommendation
                ))

            conn.commit()
            conn.close()

            logger.info("檢查結果已保存到資料庫")

        except Exception as e:
            logger.error(f"保存檢查結果失敗：{e}")

    def generate_report(self, result: QualityCheckResult) -> Dict:
        """
        生成品質報告

        參數：
            result: 檢查結果

        返回值：
            報告字典
        """
        report = {
            'report_id': result.check_id,
            'timestamp': result.timestamp.isoformat(),
            'data_source': result.data_source,
            'summary': {
                'total_records': result.total_records,
                'quality_score': f"{result.quality_score:.2f}%",
                'quality_level': result.quality_level.value,
                'issues_found': len(result.issues)
            },
            'dimensions': {
                dimension: f"{score:.2f}%"
                for dimension, score in result.dimensions.items()
            },
            'issues': [
                {
                    'id': issue.issue_id,
                    'dimension': issue.dimension.value,
                    'severity': issue.severity,
                    'column': issue.column,
                    'affected_rows': issue.row_count,
                    'description': issue.description,
                    'recommendation': issue.recommendation
                }
                for issue in result.issues
            ],
            'alerts': result.alerts
        }

        return report


# ============================================================================
# 示例和測試
# ============================================================================

def main():
    """主函數 - 執行資料品質檢查示例"""

    logger.info("\n" + "=" * 80)
    logger.info("資料品質自動檢查系統 - 演示")
    logger.info("=" * 80 + "\n")

    # 創建示例資料
    data = {
        'order_id': ['A001', 'A002', 'A003', 'A003', None, 'A005'],
        'customer_id': ['C001', 'C002', 'C003', 'C003', 'C005', 'C006'],
        'amount': [100.5, 200.75, 300.0, 300.0, 400.0, -50],  # 最後一條金額為負
        'order_date': ['2025-12-01', '2025-12-05', '2025-11-20', '2025-12-05', '2025-12-10', '2023-01-01'],  # 最後一條過舊
        'status': ['completed', 'pending', 'completed', 'pending', 'pending', 'completed']
    }

    df = pd.DataFrame(data)
    logger.info("輸入資料：")
    logger.info(df)

    # 創建品質檢查引擎
    engine = DataQualityEngine()

    # 添加檢查
    engine.add_check(CompletenessCheck(required_columns=['order_id', 'customer_id', 'amount']))

    engine.add_check(AccuracyCheck(validation_rules={
        'amount': lambda x: x > 0,
        'order_id': lambda x: isinstance(x, str) and len(x) > 0
    }))

    engine.add_check(ConsistencyCheck(consistency_rules={
        '客戶和訂單關係': lambda df: (True, 0, []) if len(df) > 0 else (False, len(df), [])
    }))

    engine.add_check(TimelinessCheck(timestamp_column='order_date', max_age_days=60))

    engine.add_check(UniquenessCheck(key_columns=['order_id']))

    # 執行檢查
    result = engine.run_checks(df, data_source="test_orders")

    # 生成報告
    report = engine.generate_report(result)

    logger.info("\n" + "=" * 60)
    logger.info("品質檢查報告：")
    logger.info("=" * 60)
    logger.info(json.dumps(report, indent=2, ensure_ascii=False))


if __name__ == "__main__":
    main()
