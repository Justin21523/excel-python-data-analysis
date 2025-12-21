"""
案例7：資料驗證規則引擎

功能概述：
- 基於配置的驗證規則
- 支援多種驗證類型（必填、類型、範圍、正則、自定義）
- 批次驗證和詳細報告
- 可擴展規則系統
- 錯誤聚合和詳細反饋

執行方式：
    python case07_validation_engine.py

配置檔案：
    validation_rules.yaml 或 validation_rules.json

作者：Data Engineering Team
版本：1.0.0
"""

import pandas as pd
import numpy as np
import logging
import yaml
import json
import re
from pathlib import Path
from datetime import datetime, date
from typing import Dict, List, Tuple, Optional, Any, Callable, Union
from dataclasses import dataclass, field, asdict
from enum import Enum
from abc import ABC, abstractmethod


# ============================================================================
# 日誌配置
# ============================================================================

def setup_logging(log_dir: str = "./logs") -> logging.Logger:
    """設定日誌系統"""
    Path(log_dir).mkdir(exist_ok=True)

    logger = logging.getLogger("ValidationEngine")
    logger.setLevel(logging.DEBUG)

    formatter = logging.Formatter(
        '%(asctime)s - %(name)s - %(levelname)s - [%(funcName)s:%(lineno)d] - %(message)s',
        datefmt='%Y-%m-%d %H:%M:%S'
    )

    file_handler = logging.FileHandler(
        f"{log_dir}/validation_{datetime.now().strftime('%Y%m%d')}.log"
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

class ValidationType(Enum):
    """驗證類型"""
    REQUIRED = "required"  # 必填
    TYPE = "type"  # 類型檢查
    RANGE = "range"  # 範圍檢查
    PATTERN = "pattern"  # 正則表達式
    LENGTH = "length"  # 長度檢查
    CUSTOM = "custom"  # 自定義
    UNIQUE = "unique"  # 唯一性
    REFERENCE = "reference"  # 外鍵參考


class ValidationSeverity(Enum):
    """驗證嚴重程度"""
    ERROR = "error"  # 錯誤：必須修復
    WARNING = "warning"  # 警告：建議修復


@dataclass
class ValidationError:
    """驗證錯誤"""
    row_index: int
    column: str
    validation_type: ValidationType
    value: Any
    message: str
    severity: ValidationSeverity
    suggestion: Optional[str] = None


@dataclass
class ValidationResult:
    """驗證結果"""
    timestamp: datetime
    total_rows: int
    valid_rows: int
    invalid_rows: int
    errors: List[ValidationError] = field(default_factory=list)
    error_summary: Dict[str, int] = field(default_factory=dict)
    pass_rate: float = 0.0


# ============================================================================
# 驗證規則基類
# ============================================================================

class ValidationRule(ABC):
    """驗證規則抽象基類"""

    def __init__(
        self,
        column: str,
        validation_type: ValidationType,
        severity: ValidationSeverity = ValidationSeverity.ERROR
    ):
        """
        初始化驗證規則

        參數：
            column: 欄位名
            validation_type: 驗證類型
            severity: 嚴重程度
        """
        self.column = column
        self.validation_type = validation_type
        self.severity = severity

    @abstractmethod
    def validate(self, value: Any, row_index: int) -> Optional[ValidationError]:
        """
        驗證值

        參數：
            value: 待驗證的值
            row_index: 行索引

        返回值：
            驗證錯誤或 None（如果通過）
        """
        pass


class RequiredRule(ValidationRule):
    """必填驗證規則"""

    def __init__(self, column: str):
        super().__init__(column, ValidationType.REQUIRED)

    def validate(self, value: Any, row_index: int) -> Optional[ValidationError]:
        """檢查值是否為空"""
        if pd.isna(value) or (isinstance(value, str) and value.strip() == ''):
            return ValidationError(
                row_index=row_index,
                column=self.column,
                validation_type=self.validation_type,
                value=value,
                message=f"欄位 '{self.column}' 是必填的",
                severity=self.severity,
                suggestion="提供此欄位的值"
            )
        return None


class TypeRule(ValidationRule):
    """資料類型驗證規則"""

    def __init__(self, column: str, expected_type: str):
        """
        初始化類型驗證規則

        參數：
            column: 欄位名
            expected_type: 期望的類型（'int', 'float', 'str', 'bool', 'date'）
        """
        super().__init__(column, ValidationType.TYPE)
        self.expected_type = expected_type.lower()

    def validate(self, value: Any, row_index: int) -> Optional[ValidationError]:
        """檢查資料類型"""
        if pd.isna(value):
            return None

        try:
            if self.expected_type == 'int':
                int(value)
            elif self.expected_type == 'float':
                float(value)
            elif self.expected_type == 'str':
                str(value)
            elif self.expected_type == 'bool':
                if not isinstance(value, bool) and str(value).lower() not in ['true', 'false', '1', '0']:
                    raise ValueError()
            elif self.expected_type == 'date':
                if isinstance(value, str):
                    pd.to_datetime(value)
            else:
                return None

            return None

        except (ValueError, TypeError):
            return ValidationError(
                row_index=row_index,
                column=self.column,
                validation_type=self.validation_type,
                value=value,
                message=f"欄位 '{self.column}' 應為 {self.expected_type} 類型，但得到 {type(value).__name__}",
                severity=self.severity,
                suggestion=f"轉換值為 {self.expected_type} 類型"
            )


class RangeRule(ValidationRule):
    """範圍驗證規則"""

    def __init__(
        self,
        column: str,
        min_value: Optional[Union[int, float]] = None,
        max_value: Optional[Union[int, float]] = None
    ):
        """
        初始化範圍驗證規則

        參數：
            column: 欄位名
            min_value: 最小值（包含）
            max_value: 最大值（包含）
        """
        super().__init__(column, ValidationType.RANGE)
        self.min_value = min_value
        self.max_value = max_value

    def validate(self, value: Any, row_index: int) -> Optional[ValidationError]:
        """檢查值是否在範圍內"""
        if pd.isna(value):
            return None

        try:
            numeric_value = float(value)

            if self.min_value is not None and numeric_value < self.min_value:
                return ValidationError(
                    row_index=row_index,
                    column=self.column,
                    validation_type=self.validation_type,
                    value=value,
                    message=f"欄位 '{self.column}' 的值 {numeric_value} 小於最小值 {self.min_value}",
                    severity=self.severity,
                    suggestion=f"將值設置為至少 {self.min_value}"
                )

            if self.max_value is not None and numeric_value > self.max_value:
                return ValidationError(
                    row_index=row_index,
                    column=self.column,
                    validation_type=self.validation_type,
                    value=value,
                    message=f"欄位 '{self.column}' 的值 {numeric_value} 大於最大值 {self.max_value}",
                    severity=self.severity,
                    suggestion=f"將值設置為最多 {self.max_value}"
                )

            return None

        except (ValueError, TypeError):
            return ValidationError(
                row_index=row_index,
                column=self.column,
                validation_type=self.validation_type,
                value=value,
                message=f"欄位 '{self.column}' 的值無法轉換為數字",
                severity=self.severity,
                suggestion="提供有效的數值"
            )


class PatternRule(ValidationRule):
    """正則表達式驗證規則"""

    def __init__(self, column: str, pattern: str):
        """
        初始化正則表達式驗證規則

        參數：
            column: 欄位名
            pattern: 正則表達式模式
        """
        super().__init__(column, ValidationType.PATTERN)
        self.pattern = pattern
        self.regex = re.compile(pattern)

    def validate(self, value: Any, row_index: int) -> Optional[ValidationError]:
        """檢查值是否匹配模式"""
        if pd.isna(value):
            return None

        str_value = str(value).strip()

        if not self.regex.match(str_value):
            return ValidationError(
                row_index=row_index,
                column=self.column,
                validation_type=self.validation_type,
                value=value,
                message=f"欄位 '{self.column}' 的值 '{str_value}' 不匹配模式 '{self.pattern}'",
                severity=self.severity,
                suggestion=f"值應匹配模式：{self.pattern}"
            )

        return None


class LengthRule(ValidationRule):
    """長度驗證規則"""

    def __init__(
        self,
        column: str,
        min_length: Optional[int] = None,
        max_length: Optional[int] = None
    ):
        """
        初始化長度驗證規則

        參數：
            column: 欄位名
            min_length: 最小長度
            max_length: 最大長度
        """
        super().__init__(column, ValidationType.LENGTH)
        self.min_length = min_length
        self.max_length = max_length

    def validate(self, value: Any, row_index: int) -> Optional[ValidationError]:
        """檢查值的長度"""
        if pd.isna(value):
            return None

        str_value = str(value)
        length = len(str_value)

        if self.min_length is not None and length < self.min_length:
            return ValidationError(
                row_index=row_index,
                column=self.column,
                validation_type=self.validation_type,
                value=value,
                message=f"欄位 '{self.column}' 的長度 {length} 小於最小值 {self.min_length}",
                severity=self.severity,
                suggestion=f"長度應至少為 {self.min_length} 個字符"
            )

        if self.max_length is not None and length > self.max_length:
            return ValidationError(
                row_index=row_index,
                column=self.column,
                validation_type=self.validation_type,
                value=value,
                message=f"欄位 '{self.column}' 的長度 {length} 大於最大值 {self.max_length}",
                severity=self.severity,
                suggestion=f"長度應最多為 {self.max_length} 個字符"
            )

        return None


class CustomRule(ValidationRule):
    """自定義驗證規則"""

    def __init__(self, column: str, validation_func: Callable):
        """
        初始化自定義驗證規則

        參數：
            column: 欄位名
            validation_func: 驗證函數，返回 True（通過）或 False（失敗）
        """
        super().__init__(column, ValidationType.CUSTOM)
        self.validation_func = validation_func

    def validate(self, value: Any, row_index: int) -> Optional[ValidationError]:
        """使用自定義函數驗證"""
        try:
            if not self.validation_func(value):
                return ValidationError(
                    row_index=row_index,
                    column=self.column,
                    validation_type=self.validation_type,
                    value=value,
                    message=f"欄位 '{self.column}' 的值 '{value}' 未通過自定義驗證",
                    severity=self.severity,
                    suggestion="檢查值是否符合業務規則"
                )
            return None
        except Exception as e:
            return ValidationError(
                row_index=row_index,
                column=self.column,
                validation_type=self.validation_type,
                value=value,
                message=f"執行自定義驗證時出錯：{str(e)}",
                severity=ValidationSeverity.ERROR,
                suggestion="檢查驗證函數是否正確"
            )


# ============================================================================
# 驗證引擎
# ============================================================================

class ValidationEngine:
    """
    資料驗證規則引擎

    核心功能：
    1. 載入驗證規則配置
    2. 對 DataFrame 執行批次驗證
    3. 收集和彙總驗證錯誤
    4. 生成詳細的驗證報告
    """

    def __init__(self):
        """初始化驗證引擎"""
        self.rules: Dict[str, List[ValidationRule]] = {}
        logger.info("驗證引擎初始化完成")

    def add_rule(self, rule: ValidationRule) -> None:
        """
        添加驗證規則

        參數：
            rule: 驗證規則
        """
        if rule.column not in self.rules:
            self.rules[rule.column] = []

        self.rules[rule.column].append(rule)
        logger.debug(f"已添加驗證規則：{rule.column} - {rule.validation_type.value}")

    def load_rules_from_yaml(self, config_file: str) -> None:
        """
        從 YAML 配置檔案載入驗證規則

        參數：
            config_file: YAML 配置檔案路徑
        """
        try:
            with open(config_file, 'r', encoding='utf-8') as f:
                config = yaml.safe_load(f)

            for column_name, column_rules in config.get('validations', {}).items():
                for rule_config in column_rules:
                    rule_type = rule_config['type']

                    severity = ValidationSeverity[
                        rule_config.get('severity', 'ERROR').upper()
                    ]

                    if rule_type == 'required':
                        rule = RequiredRule(column_name)

                    elif rule_type == 'type':
                        rule = TypeRule(column_name, rule_config['data_type'])

                    elif rule_type == 'range':
                        rule = RangeRule(
                            column_name,
                            rule_config.get('min'),
                            rule_config.get('max')
                        )

                    elif rule_type == 'pattern':
                        rule = PatternRule(column_name, rule_config['pattern'])

                    elif rule_type == 'length':
                        rule = LengthRule(
                            column_name,
                            rule_config.get('min_length'),
                            rule_config.get('max_length')
                        )

                    else:
                        logger.warning(f"未知的驗證類型：{rule_type}")
                        continue

                    rule.severity = severity
                    self.add_rule(rule)

            logger.info(f"已從 {config_file} 載入驗證規則")

        except Exception as e:
            logger.error(f"載入驗證規則失敗：{e}")
            raise

    def validate(self, df: pd.DataFrame) -> ValidationResult:
        """
        驗證 DataFrame

        參數：
            df: 待驗證的 DataFrame

        返回值：
            驗證結果
        """
        logger.info("=" * 60)
        logger.info("開始執行驗證")
        logger.info("=" * 60)

        result = ValidationResult(
            timestamp=datetime.now(),
            total_rows=len(df),
            valid_rows=0,
            invalid_rows=0
        )

        if df.empty:
            logger.warning("DataFrame 為空")
            result.pass_rate = 0.0
            return result

        # 逐行驗證
        invalid_row_indices = set()

        for column, rules in self.rules.items():
            if column not in df.columns:
                logger.warning(f"欄位 {column} 不存在於 DataFrame 中")
                continue

            for row_idx, value in enumerate(df[column]):
                for rule in rules:
                    error = rule.validate(value, row_idx)

                    if error:
                        result.errors.append(error)
                        invalid_row_indices.add(row_idx)

                        # 統計錯誤類型
                        error_key = f"{column}_{rule.validation_type.value}"
                        result.error_summary[error_key] = result.error_summary.get(error_key, 0) + 1

        # 計算統計信息
        result.invalid_rows = len(invalid_row_indices)
        result.valid_rows = len(df) - result.invalid_rows
        result.pass_rate = (result.valid_rows / len(df)) * 100 if len(df) > 0 else 0

        logger.info(f"驗證完成：")
        logger.info(f"  - 總行數：{result.total_rows}")
        logger.info(f"  - 有效行：{result.valid_rows}")
        logger.info(f"  - 無效行：{result.invalid_rows}")
        logger.info(f"  - 通過率：{result.pass_rate:.2f}%")

        return result

    def generate_report(self, result: ValidationResult) -> Dict:
        """
        生成驗證報告

        參數：
            result: 驗證結果

        返回值：
            報告字典
        """
        # 按欄位分組錯誤
        errors_by_column = {}
        errors_by_severity = {'error': [], 'warning': []}

        for error in result.errors:
            if error.column not in errors_by_column:
                errors_by_column[error.column] = []
            errors_by_column[error.column].append(error)
            errors_by_severity[error.severity.value].append(error)

        report = {
            'timestamp': result.timestamp.isoformat(),
            'summary': {
                'total_rows': result.total_rows,
                'valid_rows': result.valid_rows,
                'invalid_rows': result.invalid_rows,
                'pass_rate': f"{result.pass_rate:.2f}%"
            },
            'error_summary': result.error_summary,
            'errors_by_severity': {
                'errors': len(errors_by_severity['error']),
                'warnings': len(errors_by_severity['warning'])
            },
            'errors_by_column': {
                column: len(errors) for column, errors in errors_by_column.items()
            },
            'sample_errors': [
                {
                    'row': error.row_index,
                    'column': error.column,
                    'type': error.validation_type.value,
                    'value': str(error.value),
                    'message': error.message,
                    'suggestion': error.suggestion
                }
                for error in result.errors[:10]  # 只取前 10 條
            ]
        }

        return report


# ============================================================================
# 示例和測試
# ============================================================================

def main():
    """主函數 - 執行驗證引擎示例"""

    logger.info("\n" + "=" * 80)
    logger.info("資料驗證規則引擎 - 演示")
    logger.info("=" * 80 + "\n")

    # 創建示例資料
    data = {
        'user_id': ['U001', 'U002', None, 'U004', 'INVALID_ID', 'U006'],
        'email': ['user1@example.com', 'user2@example.com', 'invalid_email', 'user4@example.com', 'user5@example.com', 'user6@example.com'],
        'age': [25, 35, 40, 150, 28, 32],  # 150 超出合理範圍
        'salary': [50000, 75000, 60000, 80000, -5000, 55000],  # -5000 為負數
        'status': ['active', 'inactive', 'active', 'active', 'pending', 'active']
    }

    df = pd.DataFrame(data)
    logger.info("輸入資料：")
    logger.info(df)

    # 創建驗證引擎
    engine = ValidationEngine()

    # 添加驗證規則
    engine.add_rule(RequiredRule('user_id'))
    engine.add_rule(TypeRule('user_id', 'str'))
    engine.add_rule(LengthRule('user_id', min_length=4, max_length=10))

    engine.add_rule(RequiredRule('email'))
    engine.add_rule(PatternRule('email', r'^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$'))

    engine.add_rule(RequiredRule('age'))
    engine.add_rule(TypeRule('age', 'int'))
    engine.add_rule(RangeRule('age', min_value=0, max_value=120))

    engine.add_rule(RequiredRule('salary'))
    engine.add_rule(TypeRule('salary', 'float'))
    engine.add_rule(RangeRule('salary', min_value=0, max_value=1000000))

    # 執行驗證
    result = engine.validate(df)

    # 生成報告
    report = engine.generate_report(result)

    logger.info("\n" + "=" * 60)
    logger.info("驗證報告：")
    logger.info("=" * 60)
    logger.info(json.dumps(report, indent=2, ensure_ascii=False, default=str))


if __name__ == "__main__":
    main()
