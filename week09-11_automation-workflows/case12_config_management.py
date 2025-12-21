"""
案例12：配置管理系統

功能概述：
- 支援多種配置格式（YAML, JSON, TOML）
- 環境變數和密鑰管理
- 配置驗證和預設值
- 配置版本控制
- 動態配置重載

執行方式：
    python case12_config_management.py

作者：Data Engineering Team
版本：1.0.0
"""

import logging
import json
import yaml
import os
from pathlib import Path
from typing import Dict, Any, Optional, List
from dataclasses import dataclass
from enum import Enum
import hashlib
from datetime import datetime


# ============================================================================
# 日誌配置
# ============================================================================

def setup_logging(log_dir: str = "./logs") -> logging.Logger:
    """設定日誌系統"""
    Path(log_dir).mkdir(exist_ok=True)

    logger = logging.getLogger("ConfigManagement")
    logger.setLevel(logging.DEBUG)

    formatter = logging.Formatter(
        '%(asctime)s - %(name)s - %(levelname)s - [%(funcName)s:%(lineno)d] - %(message)s',
        datefmt='%Y-%m-%d %H:%M:%S'
    )

    file_handler = logging.FileHandler(
        f"{log_dir}/config_{datetime.now().strftime('%Y%m%d')}.log"
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

class ConfigFormat(Enum):
    """配置格式"""
    YAML = "yaml"
    JSON = "json"
    TOML = "toml"


@dataclass
class ConfigSchema:
    """配置方案"""
    key: str
    data_type: type
    required: bool = True
    default: Optional[Any] = None
    description: str = ""
    env_var: Optional[str] = None  # 對應的環境變數


# ============================================================================
# 配置管理系統
# ============================================================================

class ConfigManager:
    """
    配置管理系統

    功能：
    1. 載入和管理配置
    2. 支援多種格式
    3. 環境變數替換
    4. 配置驗證
    5. 動態重載
    """

    def __init__(self, config_dir: str = "./config"):
        """
        初始化配置管理器

        參數：
            config_dir: 配置目錄
        """
        self.config_dir = Path(config_dir)
        self.config_dir.mkdir(parents=True, exist_ok=True)

        self.config: Dict[str, Any] = {}
        self.schemas: Dict[str, ConfigSchema] = {}
        self.config_file: Optional[Path] = None
        self.config_hash: Optional[str] = None

        logger.info("配置管理系統初始化完成")

    def register_schema(self, *schemas: ConfigSchema) -> None:
        """
        註冊配置方案

        參數：
            *schemas: 配置方案
        """
        for schema in schemas:
            self.schemas[schema.key] = schema
            logger.debug(f"已註冊配置方案：{schema.key}")

        logger.info(f"已註冊 {len(schemas)} 個配置方案")

    def load_config(self, config_file: str) -> bool:
        """
        載入配置檔案

        參數：
            config_file: 配置檔案路徑

        返回值：
            是否成功載入
        """
        config_path = Path(config_file)

        if not config_path.exists():
            logger.error(f"配置檔案不存在：{config_file}")
            return False

        try:
            # 根據副檔名確定格式
            suffix = config_path.suffix.lower()

            if suffix == '.yaml' or suffix == '.yml':
                with open(config_path, 'r', encoding='utf-8') as f:
                    self.config = yaml.safe_load(f) or {}

            elif suffix == '.json':
                with open(config_path, 'r', encoding='utf-8') as f:
                    self.config = json.load(f)

            elif suffix == '.toml':
                try:
                    import tomli as toml
                    with open(config_path, 'rb') as f:
                        self.config = toml.load(f)
                except ImportError:
                    logger.warning("未安裝 tomli，無法讀取 TOML 檔案")
                    return False

            else:
                logger.error(f"不支援的配置格式：{suffix}")
                return False

            self.config_file = config_path

            # 計算配置哈希
            with open(config_path, 'rb') as f:
                self.config_hash = hashlib.md5(f.read()).hexdigest()

            # 替換環境變數
            self._replace_env_vars()

            # 驗證配置
            if not self._validate_config():
                logger.error("配置驗證失敗")
                return False

            logger.info(f"配置檔案載入成功：{config_file}")
            return True

        except Exception as e:
            logger.error(f"載入配置檔案失敗：{e}")
            return False

    def _replace_env_vars(self) -> None:
        """替換配置中的環境變數"""
        def replace_value(value: Any) -> Any:
            if isinstance(value, str):
                # 檢查是否為環境變數引用 ${ENV_VAR}
                if value.startswith('${') and value.endswith('}'):
                    env_var = value[2:-1]
                    return os.getenv(env_var, value)
                return value
            elif isinstance(value, dict):
                return {k: replace_value(v) for k, v in value.items()}
            elif isinstance(value, list):
                return [replace_value(v) for v in value]
            return value

        self.config = replace_value(self.config)
        logger.info("環境變數替換完成")

    def _validate_config(self) -> bool:
        """驗證配置"""
        for schema in self.schemas.values():
            if schema.required and schema.key not in self.config:
                # 嘗試從環境變數讀取
                if schema.env_var:
                    env_value = os.getenv(schema.env_var)
                    if env_value:
                        self.config[schema.key] = env_value
                        continue

                if schema.default is not None:
                    self.config[schema.key] = schema.default
                    logger.warning(f"配置 {schema.key} 缺失，使用預設值：{schema.default}")
                else:
                    logger.error(f"必填配置缺失：{schema.key}")
                    return False

            # 驗證類型
            if schema.key in self.config:
                value = self.config[schema.key]
                if not isinstance(value, schema.data_type):
                    logger.warning(
                        f"配置 {schema.key} 類型不匹配，期望 {schema.data_type.__name__}，"
                        f"得到 {type(value).__name__}"
                    )

        logger.info("配置驗證完成")
        return True

    def get(self, key: str, default: Optional[Any] = None) -> Any:
        """
        獲取配置值

        參數：
            key: 配置鍵
            default: 預設值

        返回值：
            配置值
        """
        value = self.config.get(key)

        if value is None:
            # 嘗試從環境變數讀取
            if key in self.schemas:
                schema = self.schemas[key]
                if schema.env_var:
                    value = os.getenv(schema.env_var)

        return value if value is not None else default

    def get_section(self, section: str) -> Dict[str, Any]:
        """
        獲取配置段

        參數：
            section: 段名稱

        返回值：
            段的配置字典
        """
        return self.config.get(section, {})

    def set(self, key: str, value: Any) -> None:
        """
        設定配置值

        參數：
            key: 配置鍵
            value: 配置值
        """
        self.config[key] = value
        logger.debug(f"配置已更新：{key} = {value}")

    def has_changed(self) -> bool:
        """
        檢查配置檔案是否已更改

        返回值：
            是否已更改
        """
        if not self.config_file or not self.config_file.exists():
            return False

        try:
            with open(self.config_file, 'rb') as f:
                current_hash = hashlib.md5(f.read()).hexdigest()
            return current_hash != self.config_hash
        except Exception as e:
            logger.error(f"檢查配置變更失敗：{e}")
            return False

    def reload_if_changed(self) -> bool:
        """
        如果配置已更改則重新載入

        返回值：
            是否重新載入
        """
        if self.has_changed():
            logger.info("檢測到配置檔案已更改，重新載入...")
            return self.load_config(str(self.config_file))
        return False

    def save_config(self, output_file: str) -> bool:
        """
        保存配置到檔案

        參數：
            output_file: 輸出檔案路徑

        返回值：
            是否成功保存
        """
        try:
            output_path = Path(output_file)
            suffix = output_path.suffix.lower()

            with open(output_path, 'w', encoding='utf-8') as f:
                if suffix == '.yaml' or suffix == '.yml':
                    yaml.dump(self.config, f, default_flow_style=False, allow_unicode=True)
                elif suffix == '.json':
                    json.dump(self.config, f, indent=2, ensure_ascii=False)
                else:
                    logger.error(f"不支援的輸出格式：{suffix}")
                    return False

            logger.info(f"配置已保存到：{output_file}")
            return True

        except Exception as e:
            logger.error(f"保存配置失敗：{e}")
            return False

    def export_config(self, redact_secrets: bool = True) -> Dict[str, Any]:
        """
        匯出配置（可選隱藏敏感信息）

        參數：
            redact_secrets: 是否隱藏敏感信息

        返回值：
            配置字典
        """
        config_copy = self.config.copy()

        if redact_secrets:
            # 隱藏敏感欄位
            sensitive_keys = ['password', 'token', 'secret', 'api_key', 'access_key']
            for key in config_copy:
                if any(s in key.lower() for s in sensitive_keys):
                    config_copy[key] = "***REDACTED***"

        return config_copy

    def get_config_summary(self) -> Dict[str, Any]:
        """
        獲取配置摘要

        返回值：
            摘要字典
        """
        return {
            'config_file': str(self.config_file) if self.config_file else None,
            'config_hash': self.config_hash,
            'loaded_at': datetime.now().isoformat(),
            'config_sections': list(self.config.keys()),
            'total_keys': len(self._flatten_dict(self.config))
        }

    @staticmethod
    def _flatten_dict(d: Dict, parent_key: str = '') -> Dict:
        """展平嵌套字典"""
        items = []
        for k, v in d.items():
            new_key = f"{parent_key}.{k}" if parent_key else k
            if isinstance(v, dict):
                items.extend(ConfigManager._flatten_dict(v, new_key).items())
            else:
                items.append((new_key, v))
        return dict(items)


# ============================================================================
# 示例配置檔案和使用
# ============================================================================

EXAMPLE_CONFIG_YAML = """
# 數據管道配置示例

database:
  host: ${DB_HOST:localhost}
  port: ${DB_PORT:5432}
  username: ${DB_USER}
  password: ${DB_PASSWORD}
  database: etl_db
  timeout_seconds: 30

etl:
  input_dir: ./data/raw
  output_dir: ./data/processed
  archive_dir: ./data/archive
  batch_size: 1000
  max_workers: 4
  retry_count: 3

logging:
  level: INFO
  log_dir: ./logs
  max_file_size_mb: 100
  backup_count: 10

notifications:
  email:
    enabled: true
    smtp_server: smtp.example.com
    smtp_port: 587
    sender_email: ${SMTP_EMAIL}
    sender_password: ${SMTP_PASSWORD}

  slack:
    enabled: true
    webhook_url: ${SLACK_WEBHOOK_URL}

scheduling:
  daily_etl:
    schedule: "09:00"
    enabled: true
    priority: high

  hourly_quality_check:
    schedule: "hourly"
    enabled: true
    priority: normal
"""


def main():
    """主函數 - 演示配置管理"""

    logger.info("\n" + "=" * 80)
    logger.info("配置管理系統 - 演示")
    logger.info("=" * 80 + "\n")

    # 創建配置管理器
    config_mgr = ConfigManager(config_dir="./config")

    # 註冊配置方案
    config_mgr.register_schema(
        ConfigSchema(
            key="database.host",
            data_type=str,
            required=True,
            default="localhost",
            env_var="DB_HOST"
        ),
        ConfigSchema(
            key="database.port",
            data_type=int,
            required=True,
            default=5432,
            env_var="DB_PORT"
        ),
        ConfigSchema(
            key="etl.batch_size",
            data_type=int,
            required=False,
            default=1000
        ),
        ConfigSchema(
            key="logging.level",
            data_type=str,
            required=False,
            default="INFO"
        )
    )

    # 創建示例配置檔案
    config_file = "./config/example_config.yaml"
    try:
        with open(config_file, 'w', encoding='utf-8') as f:
            f.write(EXAMPLE_CONFIG_YAML)
        logger.info(f"已創建示例配置檔案：{config_file}")
    except Exception as e:
        logger.error(f"創建示例配置失敗：{e}")

    # 載入配置
    if config_mgr.load_config(config_file):
        logger.info("\n【配置項】")
        logger.info(f"Database Host: {config_mgr.get('database.host', 'N/A')}")
        logger.info(f"Database Port: {config_mgr.get('database.port', 'N/A')}")
        logger.info(f"ETL Batch Size: {config_mgr.get('etl.batch_size', 'N/A')}")

        logger.info("\n【配置段】")
        db_config = config_mgr.get_section('database')
        logger.info(f"Database Config: {db_config}")

        logger.info("\n【配置摘要】")
        summary = config_mgr.get_config_summary()
        logger.info(f"  - 配置檔案：{summary['config_file']}")
        logger.info(f"  - 段數：{len(summary['config_sections'])}")

        logger.info("\n【隱藏敏感信息的配置】")
        safe_config = config_mgr.export_config(redact_secrets=True)
        logger.info(json.dumps(safe_config, indent=2, ensure_ascii=False, default=str))


if __name__ == "__main__":
    main()
