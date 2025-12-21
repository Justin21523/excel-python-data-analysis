"""
案例10：Slack 整合系統

功能概述：
- 即時消息推送到 Slack
- 富文本消息和交互式組件
- 頻道和用戶通知
- 消息模板
- 錯誤和告警通知

執行方式：
    python case10_slack_integration.py

前提：
    需要安裝 slack_sdk：pip install slack-sdk

作者：Data Engineering Team
版本：1.0.0
"""

import logging
import json
import sqlite3
from pathlib import Path
from datetime import datetime
from typing import Dict, List, Optional, Any
from dataclasses import dataclass, field
from enum import Enum
import re


# ============================================================================
# 日誌配置
# ============================================================================

def setup_logging(log_dir: str = "./logs") -> logging.Logger:
    """設定日誌系統"""
    Path(log_dir).mkdir(exist_ok=True)

    logger = logging.getLogger("SlackIntegration")
    logger.setLevel(logging.DEBUG)

    formatter = logging.Formatter(
        '%(asctime)s - %(name)s - %(levelname)s - [%(funcName)s:%(lineno)d] - %(message)s',
        datefmt='%Y-%m-%d %H:%M:%S'
    )

    file_handler = logging.FileHandler(
        f"{log_dir}/slack_{datetime.now().strftime('%Y%m%d')}.log"
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

class MessageType(Enum):
    """消息類型"""
    INFO = "info"
    SUCCESS = "success"
    WARNING = "warning"
    ERROR = "error"
    CRITICAL = "critical"


class MessageColor(Enum):
    """消息顏色"""
    BLUE = "#0099FF"  # 信息
    GREEN = "#00B050"  # 成功
    YELLOW = "#FFC000"  # 警告
    RED = "#FF0000"  # 錯誤
    PURPLE = "#9933FF"  # 關鍵


@dataclass
class SlackMessage:
    """Slack 消息"""
    message_id: str
    timestamp: datetime
    channel: str
    text: str
    message_type: MessageType = MessageType.INFO
    attachments: List[Dict] = field(default_factory=list)
    blocks: List[Dict] = field(default_factory=list)
    thread_ts: Optional[str] = None
    mentions: List[str] = field(default_factory=list)  # @user
    is_sent: bool = False
    send_timestamp: Optional[datetime] = None


# ============================================================================
# Slack 集成系統
# ============================================================================

class SlackIntegration:
    """
    Slack 整合系統

    功能：
    1. 推送消息到 Slack
    2. 支援富文本和交互式組件
    3. 頻道和用戶通知
    4. 消息模板
    """

    def __init__(self, webhook_url: str = ""):
        """
        初始化 Slack 整合

        參數：
            webhook_url: Slack Webhook URL（用於 Webhook 模式）
                        或者可以使用 Slack Bot Token（用於 API 模式）
        """
        self.webhook_url = webhook_url
        self.messages_sent = 0
        self.messages_failed = 0

        # 嘗試導入 Slack SDK
        try:
            from slack_sdk import WebClient
            self.slack_client = WebClient(token=webhook_url.replace("xoxb-", ""))
            self.use_api = True
        except ImportError:
            logger.warning("未安裝 slack_sdk，將使用 Webhook 模式")
            self.use_api = False
        except Exception:
            self.use_api = False

        self._init_database()

        logger.info("Slack 整合系統初始化完成")

    def _init_database(self) -> None:
        """初始化 Slack 消息日誌資料庫"""
        try:
            conn = sqlite3.connect("./slack_logs.db")
            cursor = conn.cursor()

            cursor.execute("""
                CREATE TABLE IF NOT EXISTS slack_messages (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    message_id TEXT UNIQUE,
                    timestamp TIMESTAMP,
                    channel TEXT,
                    message_type TEXT,
                    text TEXT,
                    is_sent BOOLEAN,
                    send_timestamp TIMESTAMP,
                    response TEXT,
                    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
                )
            """)

            conn.commit()
            conn.close()
            logger.info("Slack 日誌資料庫初始化完成")

        except Exception as e:
            logger.error(f"資料庫初始化失敗：{e}")

    def send_simple_message(
        self,
        channel: str,
        text: str,
        message_type: MessageType = MessageType.INFO
    ) -> bool:
        """
        發送簡單消息

        參數：
            channel: Slack 頻道（如 #general 或 user ID）
            text: 消息文本
            message_type: 消息類型

        返回值：
            是否發送成功
        """
        message = SlackMessage(
            message_id=f"msg_{datetime.now().strftime('%Y%m%d%H%M%S_%f')}",
            timestamp=datetime.now(),
            channel=channel,
            text=text,
            message_type=message_type
        )

        return self.send_message(message)

    def send_message(self, message: SlackMessage) -> bool:
        """
        發送消息

        參數：
            message: Slack 消息

        返回值：
            是否發送成功
        """
        try:
            # 格式化消息
            payload = self._format_message(message)

            # 發送消息
            if self.use_api:
                response = self._send_via_api(message.channel, payload)
            else:
                response = self._send_via_webhook(payload)

            if response:
                message.is_sent = True
                message.send_timestamp = datetime.now()
                self.messages_sent += 1

                self._log_message(message, response)

                logger.info(f"消息已發送到 {message.channel}：{message.text[:50]}...")
                return True
            else:
                self.messages_failed += 1
                logger.error(f"消息發送失敗：{message.text[:50]}...")
                return False

        except Exception as e:
            self.messages_failed += 1
            logger.error(f"發送消息時出錯：{e}")
            return False

    def _format_message(self, message: SlackMessage) -> Dict:
        """
        格式化消息為 Slack 格式

        參數：
            message: 消息

        返回值：
            Slack 格式的消息字典
        """
        # 顏色對應
        color_map = {
            MessageType.INFO: MessageColor.BLUE,
            MessageType.SUCCESS: MessageColor.GREEN,
            MessageType.WARNING: MessageColor.YELLOW,
            MessageType.ERROR: MessageColor.RED,
            MessageType.CRITICAL: MessageColor.PURPLE,
        }

        # 圖標對應
        emoji_map = {
            MessageType.INFO: ':information_source:',
            MessageType.SUCCESS: ':white_check_mark:',
            MessageType.WARNING: ':warning:',
            MessageType.ERROR: ':x:',
            MessageType.CRITICAL: ':rotating_light:',
        }

        color = color_map.get(message.message_type, MessageColor.BLUE).value
        emoji = emoji_map.get(message.message_type, ':information_source:')

        # 構建附件
        attachments = [{
            'color': color,
            'text': message.text,
            'ts': int(message.timestamp.timestamp())
        }]

        # 添加額外的附件
        if message.attachments:
            attachments.extend(message.attachments)

        # 提及信息
        mention_text = ""
        if message.mentions:
            mention_text = " " + " ".join([f"<@{m}>" for m in message.mentions])

        payload = {
            'channel': message.channel,
            'text': f"{emoji} {message.text}{mention_text}",
            'attachments': attachments
        }

        # 添加 blocks（如果有）
        if message.blocks:
            payload['blocks'] = message.blocks

        # 線程回復
        if message.thread_ts:
            payload['thread_ts'] = message.thread_ts

        return payload

    def _send_via_webhook(self, payload: Dict) -> bool:
        """通過 Webhook 發送消息"""
        try:
            import requests
            response = requests.post(
                self.webhook_url,
                json=payload,
                timeout=10
            )
            return response.status_code == 200
        except Exception as e:
            logger.error(f"Webhook 發送失敗：{e}")
            return False

    def _send_via_api(self, channel: str, payload: Dict) -> str:
        """通過 Slack API 發送消息"""
        try:
            response = self.slack_client.chat_postMessage(
                channel=channel,
                text=payload.get('text', ''),
                attachments=payload.get('attachments', []),
                blocks=payload.get('blocks', []),
                thread_ts=payload.get('thread_ts')
            )
            return response.get('ts', '')
        except Exception as e:
            logger.error(f"API 發送失敗：{e}")
            return ""

    def _log_message(self, message: SlackMessage, response: Any) -> None:
        """記錄消息發送"""
        try:
            conn = sqlite3.connect("./slack_logs.db")
            cursor = conn.cursor()

            cursor.execute("""
                INSERT INTO slack_messages
                (message_id, timestamp, channel, message_type, text, is_sent, send_timestamp, response)
                VALUES (?, ?, ?, ?, ?, ?, ?, ?)
            """, (
                message.message_id,
                message.timestamp.isoformat(),
                message.channel,
                message.message_type.value,
                message.text,
                message.is_sent,
                message.send_timestamp.isoformat() if message.send_timestamp else None,
                str(response)
            ))

            conn.commit()
            conn.close()

        except Exception as e:
            logger.error(f"記錄消息失敗：{e}")

    def send_etl_notification(
        self,
        channel: str,
        status: str,
        pipeline_name: str,
        records_processed: int,
        duration_seconds: float,
        error_message: Optional[str] = None
    ) -> bool:
        """
        發送 ETL 通知

        參數：
            channel: Slack 頻道
            status: 狀態（'success', 'failure'）
            pipeline_name: 管道名稱
            records_processed: 處理的記錄數
            duration_seconds: 執行時長（秒）
            error_message: 錯誤信息（可選）

        返回值：
            是否發送成功
        """
        if status == 'success':
            message_type = MessageType.SUCCESS
            text = f"✅ ETL Pipeline '{pipeline_name}' 執行成功"
        else:
            message_type = MessageType.ERROR
            text = f"❌ ETL Pipeline '{pipeline_name}' 執行失敗"

        # 構建消息
        message = SlackMessage(
            message_id=f"etl_{datetime.now().strftime('%Y%m%d%H%M%S')}",
            timestamp=datetime.now(),
            channel=channel,
            text=text,
            message_type=message_type
        )

        # 添加詳情附件
        attachment = {
            'title': pipeline_name,
            'fields': [
                {
                    'title': '狀態',
                    'value': '✅ 成功' if status == 'success' else '❌ 失敗',
                    'short': True
                },
                {
                    'title': '已處理記錄',
                    'value': f"{records_processed:,}",
                    'short': True
                },
                {
                    'title': '執行時長',
                    'value': f"{duration_seconds:.2f} 秒",
                    'short': True
                }
            ]
        }

        if error_message:
            attachment['fields'].append({
                'title': '錯誤信息',
                'value': error_message,
                'short': False
            })

        message.attachments = [attachment]

        return self.send_message(message)

    def send_data_quality_alert(
        self,
        channel: str,
        quality_score: float,
        issues_found: int,
        main_issues: List[str]
    ) -> bool:
        """
        發送資料品質告警

        參數：
            channel: Slack 頻道
            quality_score: 品質評分
            issues_found: 發現的問題數
            main_issues: 主要問題列表

        返回值：
            是否發送成功
        """
        message_type = MessageType.WARNING if quality_score >= 75 else MessageType.ERROR

        message = SlackMessage(
            message_id=f"quality_{datetime.now().strftime('%Y%m%d%H%M%S')}",
            timestamp=datetime.now(),
            channel=channel,
            text=f"⚠️  資料品質告警 - 評分 {quality_score:.1f}%",
            message_type=message_type
        )

        # 添加詳情
        attachment = {
            'title': '資料品質報告',
            'fields': [
                {
                    'title': '品質評分',
                    'value': f"{quality_score:.1f}%",
                    'short': True
                },
                {
                    'title': '發現問題數',
                    'value': f"{issues_found}",
                    'short': True
                },
                {
                    'title': '主要問題',
                    'value': '\n'.join([f"• {issue}" for issue in main_issues[:5]]),
                    'short': False
                }
            ]
        }

        message.attachments = [attachment]

        return self.send_message(message)

    def get_statistics(self) -> Dict:
        """
        獲取 Slack 發送統計

        返回值：
            統計信息字典
        """
        return {
            'messages_sent': self.messages_sent,
            'messages_failed': self.messages_failed,
            'success_rate': f"{(self.messages_sent / max(self.messages_sent + self.messages_failed, 1) * 100):.2f}%"
        }


# ============================================================================
# 示例和測試
# ============================================================================

def main():
    """主函數 - 演示 Slack 整合"""

    logger.info("\n" + "=" * 80)
    logger.info("Slack 整合系統 - 演示")
    logger.info("=" * 80 + "\n")

    # 初始化 Slack 整合
    # 注意：需要提供有效的 Webhook URL 或 Bot Token
    slack = SlackIntegration(webhook_url="https://hooks.slack.com/services/YOUR/WEBHOOK/URL")

    # 示例1：發送簡單消息
    logger.info("示例1：發送簡單信息")
    slack.send_simple_message(
        channel="#data-pipeline",
        text="數據管道開始執行",
        message_type=MessageType.INFO
    )

    # 示例2：發送成功消息
    logger.info("\n示例2：發送成功通知")
    slack.send_simple_message(
        channel="#data-pipeline",
        text="每日 ETL 執行完成，已處理 50,000 條記錄",
        message_type=MessageType.SUCCESS
    )

    # 示例3：發送錯誤消息
    logger.info("\n示例3：發送錯誤告警")
    slack.send_simple_message(
        channel="#data-alerts",
        text="資料庫連接失敗，ETL 管道停止",
        message_type=MessageType.ERROR
    )

    # 示例4：發送 ETL 通知
    logger.info("\n示例4：發送 ETL 通知")
    slack.send_etl_notification(
        channel="#data-pipeline",
        status="success",
        pipeline_name="Daily Orders ETL",
        records_processed=50000,
        duration_seconds=120.5
    )

    # 示例5：發送資料品質告警
    logger.info("\n示例5：發送資料品質告警")
    slack.send_data_quality_alert(
        channel="#data-quality",
        quality_score=87.5,
        issues_found=3,
        main_issues=[
            "發現 125 個空值在 'customer_id' 欄位",
            "發現 42 個重複訂單",
            "發現 18 個超出範圍的金額"
        ]
    )

    # 顯示統計
    logger.info("\n" + "=" * 60)
    logger.info("Slack 發送統計：")
    logger.info("=" * 60)
    stats = slack.get_statistics()
    logger.info(json.dumps(stats, indent=2, ensure_ascii=False))

    logger.info("\nSlack 整合演示完成")
    logger.info("注意：實際使用需要提供有效的 Webhook URL 或 Bot Token")


if __name__ == "__main__":
    main()
