"""
案例1：每日訂單 ETL Pipeline

功能概述：
- 從指定資料夾讀取新訂單檔案（支援 xlsx, csv）
- 資料驗證（必填欄位、格式檢查、重複檢查）
- 清洗轉換（日期格式、數值標準化、文本規範化）
- 寫入到數據倉庫（CSV 或 SQLite）
- 自動產生每日報告（統計、異常警告）
- 完整日誌記錄與錯誤恢復

執行方式：
    python case01_daily_orders_etl.py

日誌輸出：
    etl_daily.log

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
import sys
import traceback
from typing import Dict, List, Tuple, Optional
import re
from dataclasses import dataclass, asdict
import hashlib


# ============================================================================
# 日誌配置
# ============================================================================

def setup_logging(log_dir: str = "./logs") -> logging.Logger:
    """
    設定日誌系統

    參數：
        log_dir: 日誌目錄

    返回值：
        配置好的 logger 實例
    """
    Path(log_dir).mkdir(exist_ok=True)

    logger = logging.getLogger("DailyOrdersETL")
    logger.setLevel(logging.DEBUG)

    # 日誌格式
    formatter = logging.Formatter(
        '%(asctime)s - %(name)s - %(levelname)s - [%(funcName)s:%(lineno)d] - %(message)s',
        datefmt='%Y-%m-%d %H:%M:%S'
    )

    # 文件處理器（所有日誌）
    file_handler = logging.FileHandler(
        f"{log_dir}/etl_daily_{datetime.now().strftime('%Y%m%d')}.log"
    )
    file_handler.setLevel(logging.DEBUG)
    file_handler.setFormatter(formatter)
    logger.addHandler(file_handler)

    # 錯誤文件處理器（僅錯誤）
    error_handler = logging.FileHandler(
        f"{log_dir}/etl_errors_{datetime.now().strftime('%Y%m%d')}.log"
    )
    error_handler.setLevel(logging.ERROR)
    error_handler.setFormatter(formatter)
    logger.addHandler(error_handler)

    # 控制台處理器
    console_handler = logging.StreamHandler()
    console_handler.setLevel(logging.INFO)
    console_handler.setFormatter(formatter)
    logger.addHandler(console_handler)

    return logger


logger = setup_logging()


# ============================================================================
# 數據類和統計信息
# ============================================================================

@dataclass
class ValidationResult:
    """驗證結果數據類"""
    is_valid: bool
    total_records: int
    valid_records: int
    invalid_records: int
    errors: Dict[str, List[str]]
    warnings: List[str]


@dataclass
class ETLStats:
    """ETL 統計信息"""
    start_time: datetime
    end_time: Optional[datetime]
    files_processed: int
    total_rows_read: int
    valid_rows: int
    invalid_rows: int
    rows_inserted: int
    errors: List[str]
    warnings: List[str]


# ============================================================================
# ETL 主類
# ============================================================================

class DailyOrdersETL:
    """
    每日訂單 ETL Pipeline 主類

    工作流程：
    1. 初始化（設定目錄、資料庫連接）
    2. 讀取檔案（xlsx, csv）
    3. 資料驗證（完整性、格式、重複）
    4. 清洗轉換（標準化、轉換、充實）
    5. 寫入資料庫
    6. 產生報告
    7. 清理與備份
    """

    # 必填欄位列表
    REQUIRED_FIELDS = [
        'order_id', 'customer_id', 'order_date',
        'product_id', 'quantity', 'unit_price', 'amount'
    ]

    # 數據類型定義
    DTYPE_MAPPING = {
        'order_id': str,
        'customer_id': str,
        'order_date': str,
        'product_id': str,
        'quantity': int,
        'unit_price': float,
        'amount': float,
        'status': str
    }

    def __init__(
        self,
        input_dir: str,
        output_dir: str,
        database_path: str = "./etl_database.db",
        archive_dir: str = "./archive"
    ):
        """
        初始化 ETL Pipeline

        參數：
            input_dir: 輸入檔案目錄
            output_dir: 輸出檔案目錄
            database_path: SQLite 資料庫路徑
            archive_dir: 存檔目錄
        """
        self.input_dir = Path(input_dir)
        self.output_dir = Path(output_dir)
        self.archive_dir = Path(archive_dir)
        self.database_path = database_path

        # 建立目錄
        for dir_path in [self.input_dir, self.output_dir, self.archive_dir]:
            dir_path.mkdir(parents=True, exist_ok=True)

        # 初始化統計信息
        self.stats = ETLStats(
            start_time=datetime.now(),
            end_time=None,
            files_processed=0,
            total_rows_read=0,
            valid_rows=0,
            invalid_rows=0,
            rows_inserted=0,
            errors=[],
            warnings=[]
        )

        # 初始化資料庫
        self._init_database()

        logger.info("=" * 80)
        logger.info(f"ETL Pipeline 初始化完成")
        logger.info(f"輸入目錄: {self.input_dir}")
        logger.info(f"輸出目錄: {self.output_dir}")
        logger.info(f"資料庫: {self.database_path}")
        logger.info("=" * 80)

    def _init_database(self) -> None:
        """
        初始化 SQLite 資料庫
        建立訂單表和驗證記錄表
        """
        try:
            conn = sqlite3.connect(self.database_path)
            cursor = conn.cursor()

            # 訂單表
            cursor.execute("""
                CREATE TABLE IF NOT EXISTS orders (
                    order_id TEXT PRIMARY KEY,
                    customer_id TEXT NOT NULL,
                    order_date TEXT NOT NULL,
                    product_id TEXT NOT NULL,
                    quantity INTEGER NOT NULL,
                    unit_price REAL NOT NULL,
                    amount REAL NOT NULL,
                    status TEXT DEFAULT 'pending',
                    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
                )
            """)

            # 驗證記錄表
            cursor.execute("""
                CREATE TABLE IF NOT EXISTS validation_logs (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    batch_id TEXT NOT NULL,
                    file_name TEXT NOT NULL,
                    total_records INTEGER,
                    valid_records INTEGER,
                    invalid_records INTEGER,
                    validation_date TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                    errors TEXT,
                    warnings TEXT
                )
            """)

            # ETL 執行日誌表
            cursor.execute("""
                CREATE TABLE IF NOT EXISTS etl_logs (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    batch_id TEXT UNIQUE NOT NULL,
                    start_time TIMESTAMP,
                    end_time TIMESTAMP,
                    status TEXT,
                    files_processed INTEGER,
                    rows_processed INTEGER,
                    rows_inserted INTEGER,
                    errors TEXT,
                    warnings TEXT
                )
            """)

            conn.commit()
            conn.close()
            logger.info("資料庫表初始化成功")

        except Exception as e:
            logger.error(f"資料庫初始化失敗: {e}")
            self.stats.errors.append(f"資料庫初始化失敗: {str(e)}")
            raise

    def read_files(self) -> Tuple[pd.DataFrame, List[str]]:
        """
        讀取輸入目錄的所有訂單檔案

        支援格式：
            - .xlsx (Excel)
            - .csv (逗號分隔)

        返回值：
            (合併後的 DataFrame, 已處理的檔案列表)
        """
        logger.info(f"開始讀取檔案，路徑：{self.input_dir}")

        dataframes = []
        processed_files = []

        # 查找所有 Excel 和 CSV 檔案
        files = list(self.input_dir.glob("*.xlsx")) + list(self.input_dir.glob("*.csv"))

        if not files:
            logger.warning(f"在 {self.input_dir} 中未找到任何訂單檔案")
            return pd.DataFrame(), []

        for file_path in files:
            try:
                logger.info(f"讀取檔案：{file_path.name}")

                if file_path.suffix.lower() == '.xlsx':
                    # 讀取 Excel 檔案
                    df = pd.read_excel(file_path)
                else:
                    # 讀取 CSV 檔案
                    df = pd.read_csv(file_path, encoding='utf-8')

                # 記錄讀取統計
                self.stats.total_rows_read += len(df)
                self.stats.files_processed += 1

                logger.info(f"  - 讀取行數：{len(df)}")
                logger.info(f"  - 欄位：{list(df.columns)}")

                dataframes.append(df)
                processed_files.append(file_path.name)

            except UnicodeDecodeError:
                # 嘗試使用 latin-1 編碼
                try:
                    logger.warning(f"UTF-8 讀取失敗，嘗試 latin-1 編碼")
                    df = pd.read_csv(file_path, encoding='latin-1')
                    self.stats.total_rows_read += len(df)
                    self.stats.files_processed += 1
                    dataframes.append(df)
                    processed_files.append(file_path.name)
                except Exception as e:
                    error_msg = f"檔案 {file_path.name} 讀取失敗：{e}"
                    logger.error(error_msg)
                    self.stats.errors.append(error_msg)

            except Exception as e:
                error_msg = f"處理檔案 {file_path.name} 時出錯：{e}"
                logger.error(error_msg)
                self.stats.errors.append(error_msg)

        if not dataframes:
            logger.warning("沒有成功讀取任何檔案")
            return pd.DataFrame(), processed_files

        # 合併所有 DataFrame
        combined_df = pd.concat(dataframes, ignore_index=True)
        logger.info(f"檔案合併完成，總行數：{len(combined_df)}")

        return combined_df, processed_files

    def validate_data(self, df: pd.DataFrame) -> ValidationResult:
        """
        執行多層次的資料驗證

        驗證項目：
        1. 空值檢查（必填欄位）
        2. 資料類型檢查
        3. 範圍檢查
        4. 格式檢查（日期、ID 格式）
        5. 重複檢查
        6. 邏輯檢查（數量、金額）

        參數：
            df: 待驗證的 DataFrame

        返回值：
            ValidationResult 驗證結果對象
        """
        logger.info("=" * 60)
        logger.info("開始資料驗證")
        logger.info("=" * 60)

        validation_result = ValidationResult(
            is_valid=True,
            total_records=len(df),
            valid_records=0,
            invalid_records=0,
            errors={},
            warnings=[]
        )

        # 檢查 DataFrame 是否為空
        if df.empty:
            validation_result.is_valid = False
            validation_result.errors['empty_dataframe'] = ["數據框為空"]
            logger.warning("輸入數據框為空")
            return validation_result

        # 1. 檢查必填欄位
        logger.info("驗證1：檢查必填欄位...")
        missing_fields = [f for f in self.REQUIRED_FIELDS if f not in df.columns]
        if missing_fields:
            validation_result.is_valid = False
            validation_result.errors['missing_fields'] = missing_fields
            logger.error(f"缺少必填欄位：{missing_fields}")
            return validation_result

        # 2. 檢查空值
        logger.info("驗證2：檢查空值...")
        null_check_errors = {}
        for field in self.REQUIRED_FIELDS:
            null_count = df[field].isna().sum()
            if null_count > 0:
                null_check_errors[field] = f"空值數量：{null_count}"
                logger.warning(f"欄位 {field} 有 {null_count} 個空值")

        if null_check_errors:
            validation_result.errors['null_values'] = null_check_errors
            validation_result.is_valid = False

        # 3. 重複檢查
        logger.info("驗證3：檢查重複記錄...")
        duplicate_mask = df.duplicated(subset=['order_id'], keep=False)
        duplicate_count = duplicate_mask.sum()

        if duplicate_count > 0:
            msg = f"發現 {duplicate_count} 個重複的訂單 ID"
            validation_result.warnings.append(msg)
            logger.warning(msg)
            validation_result.errors['duplicates'] = [msg]

        # 4. 日期格式驗證
        logger.info("驗證4：檢查日期格式...")
        invalid_dates = []
        for idx, date_str in enumerate(df['order_date']):
            if not self._is_valid_date(str(date_str)):
                invalid_dates.append(f"行 {idx}：{date_str}")

        if invalid_dates[:5]:  # 只記錄前5條
            msg = f"發現 {len(invalid_dates)} 個無效日期"
            validation_result.errors['invalid_dates'] = [msg]
            logger.warning(msg)

        # 5. 數值範圍檢查
        logger.info("驗證5：檢查數值範圍...")

        # 檢查數量
        invalid_quantities = ((df['quantity'] < 0) | (df['quantity'] > 10000)).sum()
        if invalid_quantities > 0:
            msg = f"發現 {invalid_quantities} 個超出範圍的數量值"
            validation_result.warnings.append(msg)
            logger.warning(msg)

        # 檢查金額
        invalid_amounts = ((df['amount'] < 0) | (df['amount'] > 1000000)).sum()
        if invalid_amounts > 0:
            msg = f"發現 {invalid_amounts} 個超出範圍的金額值"
            validation_result.warnings.append(msg)
            logger.warning(msg)

        # 6. 邏輯檢查（金額應約等於 quantity * unit_price）
        logger.info("驗證6：檢查邏輯一致性...")
        df_temp = df.copy()
        df_temp['calculated_amount'] = df_temp['quantity'] * df_temp['unit_price']
        tolerance = 0.01  # 允許誤差 0.01
        amount_mismatches = (abs(df_temp['amount'] - df_temp['calculated_amount']) > tolerance).sum()

        if amount_mismatches > 0:
            msg = f"發現 {amount_mismatches} 條記錄的金額計算不匹配"
            validation_result.warnings.append(msg)
            logger.warning(msg)

        # 7. ID 格式檢查（簡單檢查）
        logger.info("驗證7：檢查 ID 格式...")
        invalid_order_ids = df[df['order_id'].astype(str).str.match(r'^[A-Z0-9]{5,}$') == False]
        if len(invalid_order_ids) > 0:
            msg = f"發現 {len(invalid_order_ids)} 個不規範的訂單 ID"
            validation_result.warnings.append(msg)
            logger.warning(msg)

        # 標記有效行
        # 創建有效行的標記（沒有空值且日期有效）
        valid_mask = (
            df[self.REQUIRED_FIELDS].notna().all(axis=1) &
            df['order_date'].astype(str).apply(self._is_valid_date)
        )

        validation_result.valid_records = valid_mask.sum()
        validation_result.invalid_records = len(df) - validation_result.valid_records

        logger.info(f"驗證總結：")
        logger.info(f"  - 總記錄數：{validation_result.total_records}")
        logger.info(f"  - 有效記錄：{validation_result.valid_records}")
        logger.info(f"  - 無效記錄：{validation_result.invalid_records}")
        logger.info(f"  - 警告數量：{len(validation_result.warnings)}")

        # 如果有效記錄少於 50%，則標記為驗證失敗
        if validation_result.valid_records / validation_result.total_records < 0.5:
            validation_result.is_valid = False
            logger.error("有效記錄少於 50%，驗證失敗")

        return validation_result

    def _is_valid_date(self, date_str: str) -> bool:
        """
        檢查日期字符串是否有效
        支援格式：YYYY-MM-DD, YYYY/MM/DD, DD-MM-YYYY
        """
        if pd.isna(date_str):
            return False

        date_str = str(date_str).strip()

        # 支援的日期格式
        formats = [
            '%Y-%m-%d',
            '%Y/%m/%d',
            '%d-%m-%Y',
            '%d/%m/%Y',
            '%Y%m%d'
        ]

        for fmt in formats:
            try:
                datetime.strptime(date_str, fmt)
                return True
            except ValueError:
                continue

        return False

    def clean_transform(self, df: pd.DataFrame) -> pd.DataFrame:
        """
        清洗和轉換資料

        操作：
        1. 移除重複行
        2. 填充空值
        3. 標準化日期格式
        4. 數值類型轉換
        5. 文本規範化
        6. 添加衍生欄位

        參數：
            df: 待清洗的 DataFrame

        返回值：
            清洗後的 DataFrame
        """
        logger.info("=" * 60)
        logger.info("開始資料清洗與轉換")
        logger.info("=" * 60)

        df_clean = df.copy()

        # 1. 移除完全重複的行
        logger.info("步驟1：移除重複行...")
        before_dup = len(df_clean)
        df_clean = df_clean.drop_duplicates(subset=['order_id'], keep='first')
        dup_removed = before_dup - len(df_clean)
        logger.info(f"  - 移除 {dup_removed} 個重複行")

        # 2. 標準化日期格式
        logger.info("步驟2：標準化日期格式...")
        df_clean['order_date'] = df_clean['order_date'].apply(
            self._standardize_date
        )
        logger.info(f"  - 日期標準化完成")

        # 3. 數值類型轉換和清理
        logger.info("步驟3：轉換數值類型...")
        df_clean['quantity'] = pd.to_numeric(
            df_clean['quantity'], errors='coerce'
        ).fillna(0).astype(int)

        df_clean['unit_price'] = pd.to_numeric(
            df_clean['unit_price'], errors='coerce'
        ).fillna(0.0)

        df_clean['amount'] = pd.to_numeric(
            df_clean['amount'], errors='coerce'
        ).fillna(0.0)
        logger.info(f"  - 數值轉換完成")

        # 4. 文本規範化
        logger.info("步驟4：規範化文本...")
        for col in ['order_id', 'customer_id', 'product_id']:
            if col in df_clean.columns:
                df_clean[col] = df_clean[col].astype(str).str.upper().str.strip()

        if 'status' in df_clean.columns:
            df_clean['status'] = df_clean['status'].astype(str).str.lower().str.strip()
        else:
            df_clean['status'] = 'pending'

        logger.info(f"  - 文本規範化完成")

        # 5. 添加衍生欄位
        logger.info("步驟5：添加衍生欄位...")

        # 驗證金額計算
        df_clean['calculated_amount'] = (
            df_clean['quantity'] * df_clean['unit_price']
        ).round(2)

        # 金額差異
        df_clean['amount_diff'] = (
            df_clean['amount'] - df_clean['calculated_amount']
        ).round(2)

        # 處理金額不匹配（修正明顯的計算錯誤）
        amount_tolerance = 0.01
        amount_mismatch = abs(df_clean['amount_diff']) > amount_tolerance
        logger.info(f"  - 發現 {amount_mismatch.sum()} 條金額不匹配記錄，已修正")
        df_clean.loc[amount_mismatch, 'amount'] = df_clean.loc[
            amount_mismatch, 'calculated_amount'
        ]

        # 添加處理時間戳
        df_clean['processed_at'] = datetime.now().isoformat()

        # 添加批次 ID（用於追蹤）
        batch_id = datetime.now().strftime('%Y%m%d%H%M%S')
        df_clean['batch_id'] = batch_id

        logger.info(f"  - 衍生欄位添加完成")
        logger.info(f"  - 最終資料行數：{len(df_clean)}")

        return df_clean

    def _standardize_date(self, date_val) -> str:
        """
        將日期值標準化為 YYYY-MM-DD 格式

        參數：
            date_val: 日期值（字符串或 datetime）

        返回值：
            標準化後的日期字符串
        """
        if pd.isna(date_val):
            return None

        # 如果已經是 Timestamp
        if isinstance(date_val, pd.Timestamp):
            return date_val.strftime('%Y-%m-%d')

        date_str = str(date_val).strip()

        # 嘗試各種格式
        formats = [
            '%Y-%m-%d',
            '%Y/%m/%d',
            '%d-%m-%Y',
            '%d/%m/%Y',
            '%Y%m%d'
        ]

        for fmt in formats:
            try:
                dt = datetime.strptime(date_str, fmt)
                return dt.strftime('%Y-%m-%d')
            except ValueError:
                continue

        # 如果無法解析，返回原始值（供後續處理）
        logger.warning(f"無法解析日期：{date_val}")
        return None

    def save_to_database(self, df: pd.DataFrame) -> int:
        """
        將清洗後的資料保存到 SQLite 資料庫

        參數：
            df: 待保存的 DataFrame

        返回值：
            成功插入的行數
        """
        logger.info("=" * 60)
        logger.info("開始寫入資料庫")
        logger.info("=" * 60)

        if df.empty:
            logger.warning("DataFrame 為空，跳過資料庫寫入")
            return 0

        try:
            conn = sqlite3.connect(self.database_path)

            # 準備插入的數據
            insert_cols = [
                'order_id', 'customer_id', 'order_date', 'product_id',
                'quantity', 'unit_price', 'amount', 'status'
            ]

            df_insert = df[insert_cols].copy()

            # 使用 to_sql 方法（推薦）
            df_insert.to_sql(
                'orders',
                conn,
                if_exists='append',
                index=False,
                method='multi'
            )

            conn.commit()
            conn.close()

            rows_inserted = len(df_insert)
            self.stats.rows_inserted += rows_inserted

            logger.info(f"成功寫入 {rows_inserted} 條記錄到資料庫")
            return rows_inserted

        except Exception as e:
            error_msg = f"資料庫寫入失敗：{e}"
            logger.error(error_msg)
            self.stats.errors.append(error_msg)
            raise

    def save_to_csv(self, df: pd.DataFrame) -> Path:
        """
        將資料保存為 CSV 檔案

        參數：
            df: 待保存的 DataFrame

        返回值：
            保存的檔案路徑
        """
        logger.info("保存資料到 CSV...")

        timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
        output_file = self.output_dir / f"orders_processed_{timestamp}.csv"

        try:
            df.to_csv(output_file, index=False, encoding='utf-8')
            logger.info(f"CSV 檔案已保存：{output_file}")
            return output_file
        except Exception as e:
            error_msg = f"CSV 保存失敗：{e}"
            logger.error(error_msg)
            self.stats.errors.append(error_msg)
            raise

    def generate_daily_report(self, df: pd.DataFrame, validation_result: ValidationResult) -> Dict:
        """
        產生每日 ETL 報告

        包含：
        1. 資料摘要統計
        2. 驗證結果摘要
        3. 異常警告列表
        4. 性能指標
        5. 推薦行動

        參數：
            df: 處理後的 DataFrame
            validation_result: 驗證結果

        返回值：
            報告字典
        """
        logger.info("=" * 60)
        logger.info("生成每日報告")
        logger.info("=" * 60)

        # 基本統計
        report = {
            'report_date': datetime.now().isoformat(),
            'batch_id': df['batch_id'].iloc[0] if len(df) > 0 else 'N/A',

            # 數據量統計
            'data_summary': {
                'files_processed': self.stats.files_processed,
                'total_records_read': self.stats.total_rows_read,
                'valid_records': validation_result.valid_records,
                'invalid_records': validation_result.invalid_records,
                'records_inserted': self.stats.rows_inserted,
                'success_rate': f"{(validation_result.valid_records / max(validation_result.total_records, 1) * 100):.2f}%"
            },

            # 驗證結果
            'validation_summary': {
                'total_validations': validation_result.total_records,
                'passed': validation_result.valid_records,
                'failed': validation_result.invalid_records,
                'errors': validation_result.errors,
                'warnings': validation_result.warnings
            },

            # 業務指標
            'business_metrics': {},

            # 性能指標
            'performance_metrics': {
                'processing_time_seconds': (
                    datetime.now() - self.stats.start_time
                ).total_seconds() if self.stats.end_time is None else (
                    self.stats.end_time - self.stats.start_time
                ).total_seconds()
            },

            # 異常警告
            'alerts': []
        }

        # 計算業務指標
        if len(df) > 0:
            report['business_metrics'] = {
                'total_orders': len(df),
                'total_revenue': f"${df['amount'].sum():.2f}",
                'average_order_value': f"${df['amount'].mean():.2f}",
                'total_items_sold': int(df['quantity'].sum()),
                'unique_customers': df['customer_id'].nunique(),
                'unique_products': df['product_id'].nunique(),
                'date_range': f"{df['order_date'].min()} 至 {df['order_date'].max()}"
            }

        # 生成警告
        if validation_result.invalid_records > 0:
            report['alerts'].append({
                'type': 'warning',
                'severity': 'high',
                'message': f"發現 {validation_result.invalid_records} 條無效記錄"
            })

        if len(validation_result.warnings) > 0:
            for warning in validation_result.warnings:
                report['alerts'].append({
                    'type': 'warning',
                    'severity': 'medium',
                    'message': warning
                })

        if len(self.stats.errors) > 0:
            for error in self.stats.errors:
                report['alerts'].append({
                    'type': 'error',
                    'severity': 'high',
                    'message': error
                })

        return report

    def save_report(self, report: Dict) -> Path:
        """
        將報告保存為 JSON 和 HTML 格式

        參數：
            report: 報告字典

        返回值：
            保存的報告路徑
        """
        logger.info("保存報告...")

        timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')

        # 保存 JSON 報告
        json_file = self.output_dir / f"report_{timestamp}.json"
        try:
            with open(json_file, 'w', encoding='utf-8') as f:
                json.dump(report, f, ensure_ascii=False, indent=2)
            logger.info(f"JSON 報告已保存：{json_file}")
        except Exception as e:
            logger.error(f"JSON 報告保存失敗：{e}")

        # 保存文本報告
        text_file = self.output_dir / f"report_{timestamp}.txt"
        try:
            with open(text_file, 'w', encoding='utf-8') as f:
                self._write_text_report(f, report)
            logger.info(f"文本報告已保存：{text_file}")
        except Exception as e:
            logger.error(f"文本報告保存失敗：{e}")

        return json_file

    def _write_text_report(self, file_obj, report: Dict) -> None:
        """
        寫入文本格式的報告

        參數：
            file_obj: 文件對象
            report: 報告字典
        """
        f = file_obj

        f.write("=" * 80 + "\n")
        f.write(f"每日 ETL 報告 - {report['report_date']}\n")
        f.write("=" * 80 + "\n\n")

        # 數據摘要
        f.write("【數據摘要】\n")
        f.write("-" * 40 + "\n")
        for key, value in report['data_summary'].items():
            f.write(f"{key:.<30} {value}\n")

        f.write("\n【業務指標】\n")
        f.write("-" * 40 + "\n")
        for key, value in report['business_metrics'].items():
            f.write(f"{key:.<30} {value}\n")

        f.write("\n【驗證摘要】\n")
        f.write("-" * 40 + "\n")
        val_sum = report['validation_summary']
        f.write(f"{'通過驗證':.<30} {val_sum['passed']}\n")
        f.write(f"{'未通過驗證':.<30} {val_sum['failed']}\n")

        if val_sum['errors']:
            f.write(f"\n【驗證錯誤】\n")
            f.write("-" * 40 + "\n")
            for error_type, details in val_sum['errors'].items():
                f.write(f"{error_type}: {details}\n")

        if report['alerts']:
            f.write(f"\n【警告和異常】\n")
            f.write("-" * 40 + "\n")
            for alert in report['alerts']:
                f.write(f"[{alert['severity'].upper()}] {alert['message']}\n")

        f.write("\n" + "=" * 80 + "\n")
        f.write("報告生成時間：" + report['report_date'] + "\n")
        f.write("=" * 80 + "\n")

    def archive_processed_files(self) -> None:
        """
        存檔已處理的源檔案
        """
        logger.info("存檔已處理的檔案...")

        try:
            import shutil
            timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
            archive_subdir = self.archive_dir / timestamp
            archive_subdir.mkdir(parents=True, exist_ok=True)

            for file_path in list(self.input_dir.glob("*.xlsx")) + list(self.input_dir.glob("*.csv")):
                shutil.move(str(file_path), str(archive_subdir / file_path.name))
                logger.info(f"已存檔：{file_path.name}")

            logger.info(f"檔案已存檔至：{archive_subdir}")

        except Exception as e:
            logger.error(f"文件存檔失敗：{e}")
            self.stats.errors.append(f"文件存檔失敗：{str(e)}")

    def run(self) -> bool:
        """
        執行完整的 ETL 流程

        工作流程：
        1. 讀取檔案
        2. 驗證資料
        3. 清洗轉換
        4. 寫入資料庫
        5. 生成報告
        6. 存檔檔案

        返回值：
            True 表示成功，False 表示失敗
        """
        try:
            logger.info("\n" + "=" * 80)
            logger.info("開始執行每日 ETL Pipeline")
            logger.info("=" * 80 + "\n")

            # 1. 讀取檔案
            logger.info("【步驟1：讀取檔案】")
            df_raw, processed_files = self.read_files()

            if df_raw.empty:
                logger.warning("沒有資料需要處理")
                self.stats.end_time = datetime.now()
                return False

            # 2. 驗證資料
            logger.info("\n【步驟2：驗證資料】")
            validation_result = self.validate_data(df_raw)
            self.stats.valid_rows = validation_result.valid_records
            self.stats.invalid_rows = validation_result.invalid_records

            # 3. 清洗轉換
            logger.info("\n【步驟3：清洗轉換】")
            df_clean = self.clean_transform(df_raw)

            # 4. 寫入資料庫
            logger.info("\n【步驟4：寫入資料庫】")
            self.save_to_database(df_clean)

            # 5. 保存 CSV
            logger.info("\n【步驟5：保存 CSV】")
            self.save_to_csv(df_clean)

            # 6. 生成報告
            logger.info("\n【步驟6：生成報告】")
            report = self.generate_daily_report(df_clean, validation_result)
            self.save_report(report)

            # 7. 存檔檔案
            logger.info("\n【步驟7：存檔檔案】")
            self.archive_processed_files()

            # 完成
            self.stats.end_time = datetime.now()

            logger.info("\n" + "=" * 80)
            logger.info("ETL Pipeline 執行成功")
            logger.info(f"總耗時：{(self.stats.end_time - self.stats.start_time).total_seconds():.2f} 秒")
            logger.info("=" * 80 + "\n")

            return True

        except Exception as e:
            logger.error(f"\nETL Pipeline 執行失敗：{e}")
            logger.error(traceback.format_exc())
            self.stats.errors.append(f"Pipeline 執行失敗：{str(e)}")
            self.stats.end_time = datetime.now()
            return False


# ============================================================================
# 主函數
# ============================================================================

def main():
    """
    主函數 - 執行 ETL Pipeline
    """
    # 定義目錄
    input_dir = "/home/justin/web-projects/excel-python-data-analysis/week09-11_automation-workflows/data/raw"
    output_dir = "/home/justin/web-projects/excel-python-data-analysis/week09-11_automation-workflows/data/processed"
    db_path = "/home/justin/web-projects/excel-python-data-analysis/week09-11_automation-workflows/etl_database.db"

    # 建立 ETL 實例
    etl = DailyOrdersETL(
        input_dir=input_dir,
        output_dir=output_dir,
        database_path=db_path
    )

    # 執行 ETL
    success = etl.run()

    # 返回適當的退出碼
    sys.exit(0 if success else 1)


if __name__ == "__main__":
    main()
