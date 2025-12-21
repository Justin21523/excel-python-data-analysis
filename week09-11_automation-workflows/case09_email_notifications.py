"""
案例9：郵件通知系統

功能概述：
- 配置化的郵件模板
- 批量發送郵件
- 附件支援
- 郵件隊列和重試
- 發送日誌和追蹤
- HTML 和純文本格式

執行方式：
    python case09_email_notifications.py

作者：Data Engineering Team
版本：1.0.0
"""

import logging
import smtplib
import json
import sqlite3
from pathlib import Path
from datetime import datetime, timedelta
from typing import Dict, List, Optional, Tuple
from dataclasses import dataclass, field, asdict
from enum import Enum
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from email.mime.base import MIMEBase
from email import encoders
import jinja2


# ============================================================================
# 日誌配置
# ============================================================================

def setup_logging(log_dir: str = "./logs") -> logging.Logger:
    """設定日誌系統"""
    Path(log_dir).mkdir(exist_ok=True)

    logger = logging.getLogger("EmailNotification")
    logger.setLevel(logging.DEBUG)

    formatter = logging.Formatter(
        '%(asctime)s - %(name)s - %(levelname)s - [%(funcName)s:%(lineno)d] - %(message)s',
        datefmt='%Y-%m-%d %H:%M:%S'
    )

    file_handler = logging.FileHandler(
        f"{log_dir}/email_{datetime.now().strftime('%Y%m%d')}.log"
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

class EmailStatus(Enum):
    """郵件狀態"""
    PENDING = "pending"  # 待發送
    SENT = "sent"  # 已發送
    FAILED = "failed"  # 失敗
    BOUNCED = "bounced"  # 退信
    QUEUED = "queued"  # 隊列中


class EmailTemplate(Enum):
    """郵件模板類型"""
    ETL_SUCCESS = "etl_success"  # ETL 成功通知
    ETL_FAILURE = "etl_failure"  # ETL 失敗通知
    DATA_QUALITY_ALERT = "data_quality_alert"  # 資料品質告警
    PERFORMANCE_ALERT = "performance_alert"  # 性能告警
    DAILY_REPORT = "daily_report"  # 日報
    CUSTOM = "custom"  # 自定義


@dataclass
class EmailConfig:
    """郵件配置"""
    smtp_server: str
    smtp_port: int
    username: str
    password: str
    sender_email: str
    sender_name: str = "Data Pipeline System"
    use_tls: bool = True


@dataclass
class EmailMessage:
    """郵件消息"""
    email_id: str
    timestamp: datetime
    to_addresses: List[str]
    cc_addresses: List[str] = field(default_factory=list)
    bcc_addresses: List[str] = field(default_factory=list)
    subject: str = ""
    body: str = ""
    html_body: str = ""
    attachments: List[str] = field(default_factory=list)  # 檔案路徑
    template_name: EmailTemplate = EmailTemplate.CUSTOM
    template_variables: Dict[str, any] = field(default_factory=dict)
    status: EmailStatus = EmailStatus.PENDING
    retry_count: int = 0
    max_retries: int = 3
    sent_at: Optional[datetime] = None
    error_message: Optional[str] = None


# ============================================================================
# 郵件通知系統
# ============================================================================

class EmailNotificationSystem:
    """
    郵件通知系統

    功能：
    1. 配置化的郵件模板
    2. 批量發送和隊列
    3. 附件支援
    4. 重試機制
    5. 發送追蹤
    """

    # 郵件模板
    TEMPLATES = {
        EmailTemplate.ETL_SUCCESS: {
            'subject': 'ETL Pipeline - 執行成功',
            'html': '''
                <h2>ETL Pipeline 執行成功</h2>
                <p>親愛的用戶：</p>
                <p>您的數據管道已成功執行。</p>
                <table style="border: 1px solid #ddd;">
                    <tr><td>執行時間</td><td>{{ execution_time }}</td></tr>
                    <tr><td>已處理記錄數</td><td>{{ records_processed }}</td></tr>
                    <tr><td>執行狀態</td><td>成功</td></tr>
                </table>
                <p>感謝您的使用！</p>
            '''
        },
        EmailTemplate.ETL_FAILURE: {
            'subject': 'ETL Pipeline - 執行失敗（需要立即關注）',
            'html': '''
                <h2 style="color: red;">ETL Pipeline 執行失敗</h2>
                <p>親愛的用戶：</p>
                <p>您的數據管道執行失敗，需要立即採取行動。</p>
                <table style="border: 1px solid #ddd;">
                    <tr><td>執行時間</td><td>{{ execution_time }}</td></tr>
                    <tr><td>失敗原因</td><td>{{ error_message }}</td></tr>
                    <tr><td>建議</td><td>{{ recommendation }}</td></tr>
                </table>
                <p>請立即檢查日誌並採取糾正措施。</p>
            '''
        },
        EmailTemplate.DATA_QUALITY_ALERT: {
            'subject': '數據品質告警',
            'html': '''
                <h2 style="color: orange;">數據品質告警</h2>
                <p>檢測到以下數據品質問題：</p>
                <ul>
                    <li>品質評分：{{ quality_score }}%</li>
                    <li>問題數量：{{ issue_count }}</li>
                    <li>主要問題：{{ main_issue }}</li>
                </ul>
                <p>請根據建議採取糾正措施。</p>
            '''
        },
        EmailTemplate.DAILY_REPORT: {
            'subject': '每日數據管道報告 - {{ report_date }}',
            'html': '''
                <h2>每日數據管道報告</h2>
                <p>日期：{{ report_date }}</p>
                <h3>摘要</h3>
                <table style="border: 1px solid #ddd; width: 100%;">
                    <tr><td>ETL 執行次數</td><td>{{ etl_runs }}</td></tr>
                    <tr><td>成功次數</td><td style="color: green;">{{ successful_runs }}</td></tr>
                    <tr><td>失敗次數</td><td style="color: red;">{{ failed_runs }}</td></tr>
                    <tr><td>處理記錄總數</td><td>{{ total_records }}</td></tr>
                    <tr><td>平均品質評分</td><td>{{ avg_quality_score }}%</td></tr>
                </table>
                <p>詳情請參見附件。</p>
            '''
        }
    }

    def __init__(self, config: EmailConfig):
        """
        初始化郵件通知系統

        參數：
            config: 郵件配置
        """
        self.config = config
        self.template_env = jinja2.Environment(trim_blocks=True, lstrip_blocks=True)
        self.message_queue: List[EmailMessage] = []

        self._init_database()

        logger.info("郵件通知系統初始化完成")

    def _init_database(self) -> None:
        """初始化郵件發送日誌資料庫"""
        try:
            # 使用內存資料庫或實際資料庫
            conn = sqlite3.connect("./email_logs.db")
            cursor = conn.cursor()

            cursor.execute("""
                CREATE TABLE IF NOT EXISTS email_logs (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    email_id TEXT UNIQUE,
                    timestamp TIMESTAMP,
                    to_addresses TEXT,
                    cc_addresses TEXT,
                    subject TEXT,
                    status TEXT,
                    sent_at TIMESTAMP,
                    retry_count INTEGER,
                    error_message TEXT,
                    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
                )
            """)

            conn.commit()
            conn.close()
            logger.info("郵件日誌資料庫初始化完成")

        except Exception as e:
            logger.error(f"資料庫初始化失敗：{e}")

    def create_message(
        self,
        to_addresses: List[str],
        subject: str = "",
        body: str = "",
        template_name: EmailTemplate = EmailTemplate.CUSTOM,
        template_variables: Optional[Dict] = None,
        cc_addresses: Optional[List[str]] = None,
        attachments: Optional[List[str]] = None
    ) -> EmailMessage:
        """
        創建郵件消息

        參數：
            to_addresses: 收件人地址列表
            subject: 主題
            body: 郵件正文
            template_name: 模板名稱
            template_variables: 模板變量
            cc_addresses: 抄送地址
            attachments: 附件檔案路徑

        返回值：
            郵件消息對象
        """
        email_id = f"EMAIL_{datetime.now().strftime('%Y%m%d%H%M%S_%f')}"

        # 如果使用模板，先渲染
        html_body = body
        if template_name != EmailTemplate.CUSTOM and template_name in self.TEMPLATES:
            template_config = self.TEMPLATES[template_name]
            subject = subject or template_config['subject']

            # 渲染模板
            template = self.template_env.from_string(template_config['html'])
            html_body = template.render(template_variables or {})

            logger.info(f"使用模板：{template_name.value}")

        message = EmailMessage(
            email_id=email_id,
            timestamp=datetime.now(),
            to_addresses=to_addresses,
            cc_addresses=cc_addresses or [],
            subject=subject,
            body=body,
            html_body=html_body,
            attachments=attachments or [],
            template_name=template_name,
            template_variables=template_variables or {}
        )

        logger.info(f"已創建郵件消息：{email_id}")
        return message

    def send_message(self, message: EmailMessage) -> Tuple[bool, Optional[str]]:
        """
        發送單個郵件消息

        參數：
            message: 郵件消息

        返回值：
            (是否成功, 錯誤消息或 None)
        """
        try:
            logger.info(f"準備發送郵件：{message.email_id}")

            # 創建郵件
            msg = MIMEMultipart('alternative')
            msg['From'] = f"{self.config.sender_name} <{self.config.sender_email}>"
            msg['To'] = ', '.join(message.to_addresses)
            if message.cc_addresses:
                msg['Cc'] = ', '.join(message.cc_addresses)
            msg['Subject'] = message.subject

            # 添加正文
            if message.html_body:
                msg.attach(MIMEText(message.html_body, 'html', 'utf-8'))
            elif message.body:
                msg.attach(MIMEText(message.body, 'plain', 'utf-8'))

            # 添加附件
            for attachment_path in message.attachments:
                try:
                    self._attach_file(msg, attachment_path)
                except Exception as e:
                    logger.warning(f"附件添加失敗：{attachment_path} - {e}")

            # 連接 SMTP 服務器
            with smtplib.SMTP(self.config.smtp_server, self.config.smtp_port) as server:
                if self.config.use_tls:
                    server.starttls()

                server.login(self.config.username, self.config.password)

                # 發送郵件
                all_recipients = message.to_addresses + message.cc_addresses + message.bcc_addresses
                server.send_message(msg, from_addr=self.config.sender_email, to_addrs=all_recipients)

            message.status = EmailStatus.SENT
            message.sent_at = datetime.now()

            logger.info(f"郵件已成功發送：{message.email_id} 到 {message.to_addresses}")

            # 記錄到資料庫
            self._log_email(message)

            return True, None

        except smtplib.SMTPAuthenticationError as e:
            error_msg = f"SMTP 認證失敗：{str(e)}"
            logger.error(error_msg)
            message.status = EmailStatus.FAILED
            message.error_message = error_msg
            return False, error_msg

        except smtplib.SMTPException as e:
            error_msg = f"SMTP 錯誤：{str(e)}"
            logger.error(error_msg)
            message.status = EmailStatus.FAILED
            message.error_message = error_msg

            # 重試邏輯
            if message.retry_count < message.max_retries:
                message.retry_count += 1
                message.status = EmailStatus.QUEUED
                self.message_queue.append(message)
                logger.info(f"郵件已加入隊列進行重試（{message.retry_count}/{message.max_retries}）")

            return False, error_msg

        except Exception as e:
            error_msg = f"發送郵件時出錯：{str(e)}"
            logger.error(error_msg)
            message.status = EmailStatus.FAILED
            message.error_message = error_msg
            return False, error_msg

    def _attach_file(self, message: MIMEMultipart, file_path: str) -> None:
        """
        為郵件添加附件

        參數：
            message: MIME 消息
            file_path: 檔案路徑
        """
        file_path = Path(file_path)

        if not file_path.exists():
            raise FileNotFoundError(f"附件檔案不存在：{file_path}")

        # 讀取檔案
        with open(file_path, 'rb') as attachment:
            part = MIMEBase('application', 'octet-stream')
            part.set_payload(attachment.read())

        # 編碼檔案
        encoders.encode_base64(part)

        # 添加到消息
        part.add_header(
            'Content-Disposition',
            f'attachment; filename= {file_path.name}'
        )

        message.attach(part)

    def batch_send(
        self,
        recipients_list: List[Dict],
        subject: str,
        template_name: EmailTemplate = EmailTemplate.CUSTOM,
        template_variables: Optional[Dict] = None
    ) -> Dict:
        """
        批量發送郵件

        參數：
            recipients_list: 收件人列表 [{'to': [...], 'variables': {...}}, ...]
            subject: 郵件主題
            template_name: 模板名稱
            template_variables: 模板變量

        返回值：
            發送結果統計
        """
        logger.info(f"開始批量發送 {len(recipients_list)} 封郵件...")

        stats = {
            'total': len(recipients_list),
            'sent': 0,
            'failed': 0,
            'queued': 0
        }

        for recipient in recipients_list:
            to_addresses = recipient.get('to', [])
            variables = recipient.get('variables', template_variables or {})

            message = self.create_message(
                to_addresses=to_addresses,
                subject=subject,
                template_name=template_name,
                template_variables=variables
            )

            success, error = self.send_message(message)

            if success:
                stats['sent'] += 1
            elif message.status == EmailStatus.QUEUED:
                stats['queued'] += 1
            else:
                stats['failed'] += 1

        logger.info(f"批量發送完成：發送 {stats['sent']} 封，隊列 {stats['queued']} 封，失敗 {stats['failed']} 封")

        return stats

    def retry_queued_messages(self) -> Dict:
        """
        重試隊列中的郵件

        返回值：
            重試結果統計
        """
        logger.info(f"開始重試隊列中的 {len(self.message_queue)} 封郵件...")

        stats = {
            'retried': 0,
            'sent': 0,
            'failed': 0
        }

        messages_to_remove = []

        for message in self.message_queue:
            stats['retried'] += 1

            success, error = self.send_message(message)

            if success:
                stats['sent'] += 1
                messages_to_remove.append(message)
            elif message.retry_count >= message.max_retries:
                logger.error(f"郵件 {message.email_id} 重試次數已達到上限")
                messages_to_remove.append(message)
                stats['failed'] += 1

        # 移除已處理的消息
        for message in messages_to_remove:
            self.message_queue.remove(message)

        logger.info(f"重試完成：成功 {stats['sent']} 封，失敗 {stats['failed']} 封")

        return stats

    def _log_email(self, message: EmailMessage) -> None:
        """將郵件發送記錄保存到資料庫"""
        try:
            conn = sqlite3.connect("./email_logs.db")
            cursor = conn.cursor()

            cursor.execute("""
                INSERT INTO email_logs
                (email_id, timestamp, to_addresses, cc_addresses, subject, status, sent_at, retry_count, error_message)
                VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?)
            """, (
                message.email_id,
                message.timestamp.isoformat(),
                json.dumps(message.to_addresses),
                json.dumps(message.cc_addresses),
                message.subject,
                message.status.value,
                message.sent_at.isoformat() if message.sent_at else None,
                message.retry_count,
                message.error_message
            ))

            conn.commit()
            conn.close()

        except Exception as e:
            logger.error(f"記錄郵件發送日誌失敗：{e}")


# ============================================================================
# 示例和測試
# ============================================================================

def main():
    """主函數 - 演示郵件通知"""

    logger.info("\n" + "=" * 80)
    logger.info("郵件通知系統 - 演示")
    logger.info("=" * 80 + "\n")

    # 配置郵件系統
    # 注意：實際使用時，應使用真實的 SMTP 配置和認證
    email_config = EmailConfig(
        smtp_server="smtp.example.com",  # 示例 SMTP 伺服器
        smtp_port=587,
        username="your_username",
        password="your_password",
        sender_email="system@example.com",
        sender_name="Data Pipeline System"
    )

    email_system = EmailNotificationSystem(email_config)

    # 示例1：發送 ETL 成功通知
    logger.info("示例1：ETL 成功通知")
    message1 = email_system.create_message(
        to_addresses=['admin@example.com', 'team@example.com'],
        template_name=EmailTemplate.ETL_SUCCESS,
        template_variables={
            'execution_time': '2025-12-11 14:30:00',
            'records_processed': 15000
        }
    )

    logger.info(f"郵件主題：{message1.subject}")
    logger.info(f"收件人：{message1.to_addresses}")

    # 示例2：發送 ETL 失敗通知
    logger.info("\n示例2：ETL 失敗通知")
    message2 = email_system.create_message(
        to_addresses=['admin@example.com'],
        template_name=EmailTemplate.ETL_FAILURE,
        template_variables={
            'execution_time': '2025-12-11 15:00:00',
            'error_message': '資料庫連接失敗',
            'recommendation': '檢查資料庫伺服器狀態和網路連接'
        }
    )

    logger.info(f"郵件主題：{message2.subject}")

    # 示例3：發送每日報告
    logger.info("\n示例3：每日報告")
    message3 = email_system.create_message(
        to_addresses=['manager@example.com'],
        template_name=EmailTemplate.DAILY_REPORT,
        template_variables={
            'report_date': '2025-12-11',
            'etl_runs': 24,
            'successful_runs': 23,
            'failed_runs': 1,
            'total_records': 500000,
            'avg_quality_score': 94.5
        }
    )

    logger.info(f"郵件主題：{message3.subject}")

    # 示例4：批量發送
    logger.info("\n示例4：批量發送")
    recipients = [
        {
            'to': ['user1@example.com'],
            'variables': {'user_name': 'User 1', 'records': 1000}
        },
        {
            'to': ['user2@example.com'],
            'variables': {'user_name': 'User 2', 'records': 2000}
        },
        {
            'to': ['user3@example.com'],
            'variables': {'user_name': 'User 3', 'records': 1500}
        }
    ]

    # 注意：實際發送需要有效的 SMTP 配置
    # stats = email_system.batch_send(
    #     recipients_list=recipients,
    #     subject="您的每日數據報告",
    #     template_name=EmailTemplate.DAILY_REPORT
    # )
    # logger.info(f"批量發送結果：{stats}")

    logger.info("\n郵件通知系統演示完成")
    logger.info("注意：實際郵件發送需要有效的 SMTP 配置")


if __name__ == "__main__":
    main()
