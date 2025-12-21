"""
電商資料集終極整合下載工具 - 完整版

整合功能：
1. 支援 14 個資料集（Kaggle + HuggingFace + UCI + 手動）
2. 完全遵循 AI_WAREHOUSE 3.0 結構規範
3. 靈活的參數控制
4. 完整的錯誤處理與日誌記錄

資料集儲存位置：
- 預設：/mnt/data/datasets/ecommerce/
- 可透過 --dataset-root 自訂

快取位置：
- 預設：/mnt/c/ai_cache/
- 可透過 --cache-root 自訂

使用範例：
    # 列出所有資料集
    python download_datasets_complete.py --list

    # 下載單一資料集
    python download_datasets_complete.py --dataset online-retail

    # 下載所有資料集
    python download_datasets_complete.py --all

    # 按類別下載（large/medium/ml）
    python download_datasets_complete.py --category large

    # 按優先級下載（1=最高優先）
    python download_datasets_complete.py --priority 1

    # 自訂路徑
    python download_datasets_complete.py --dataset online-retail \\
        --dataset-root /custom/path \\
        --cache-root /custom/cache

    # 批次下載多個資料集
    python download_datasets_complete.py \\
        --datasets online-retail olist instacart

    # 乾跑模式（不實際下載，只顯示會做什麼）
    python download_datasets_complete.py --all --dry-run
"""

import argparse
import os
import sys
from pathlib import Path
import subprocess
import json
import time
from datetime import datetime
from typing import List, Dict, Optional, Tuple
import logging


# ==============================================================================
# AI_WAREHOUSE 3.0 路徑設定
# ==============================================================================

class Config:
    """設定類別，管理所有路徑和環境變數"""

    def __init__(self, dataset_root=None, cache_root=None):
        # 資料集根目錄
        self.dataset_root = Path(
            dataset_root or
            os.getenv('DATASET_ROOT', '/mnt/data/datasets/ecommerce')
        )

        # 快取根目錄
        self.cache_root = Path(
            cache_root or
            os.getenv('XDG_CACHE_HOME', '/mnt/c/ai_cache')
        )

        # HuggingFace 快取
        self.hf_home = self.cache_root / 'huggingface'

        # Kaggle 設定
        self.kaggle_config = Path(
            os.getenv('KAGGLE_CONFIG_DIR', os.path.expanduser('~/.kaggle'))
        )

        # 建立所有必要目錄
        self.create_directories()

    def create_directories(self):
        """建立所有必要的目錄"""
        dirs = [
            self.dataset_root,
            self.dataset_root / 'kaggle',
            self.dataset_root / 'uci',
            self.dataset_root / 'huggingface',
            self.dataset_root / 'manual',
            self.cache_root,
            self.hf_home,
        ]

        for d in dirs:
            d.mkdir(parents=True, exist_ok=True)

    def setup_environment(self):
        """設定環境變數"""
        os.environ['DATASET_ROOT'] = str(self.dataset_root)
        os.environ['HF_HOME'] = str(self.hf_home)
        os.environ['TRANSFORMERS_CACHE'] = str(self.hf_home)
        os.environ['TORCH_HOME'] = str(self.cache_root / 'torch')
        os.environ['XDG_CACHE_HOME'] = str(self.cache_root)

        # 如果 Kaggle 配置存在，設定路徑
        if self.kaggle_config.exists():
            os.environ['KAGGLE_CONFIG_DIR'] = str(self.kaggle_config)


# ==============================================================================
# 資料集定義（共 14 個）
# ==============================================================================

DATASETS = {
    # ==================== 超大型資料集（百萬筆以上）====================

    'amazon-reviews': {
        'name': 'Amazon Reviews 2023',
        'platform': 'huggingface',
        'category': 'large',
        'size': '數十 GB（完整）/ 數百 MB（子集）',
        'records': '142.8M 筆評論',
        'use_cases': ['推薦系統', 'NLP', '情感分析'],
        'priority': 2,
        'estimated_time': '10-30 分鐘（子集）',
        'download_func': 'download_amazon_reviews'
    },

    'instacart': {
        'name': 'Instacart Market Basket Analysis',
        'platform': 'kaggle',
        'category': 'large',
        'size': '200 MB',
        'records': '3M+ 筆訂單',
        'use_cases': ['購物籃分析', '關聯規則'],
        'priority': 1,
        'estimated_time': '5-10 分鐘',
        'kaggle_id': 'instacart-market-basket-analysis',
        'competition': True
    },

    'ecommerce-behavior': {
        'name': 'eCommerce Behavior Data',
        'platform': 'kaggle',
        'category': 'large',
        'size': '數 GB',
        'records': '285M 筆事件',
        'use_cases': ['客戶行為分析', '漏斗分析'],
        'priority': 2,
        'estimated_time': '30-60 分鐘',
        'kaggle_id': 'mkechinov/ecommerce-behavior-data-from-multi-category-store',
        'warning': '檔案非常大，確保足夠空間'
    },

    'h-and-m': {
        'name': 'H&M Fashion Recommendations',
        'platform': 'kaggle',
        'category': 'large',
        'size': '數 GB（含圖片）',
        'records': '1.37M 客戶',
        'use_cases': ['推薦系統', '圖像識別'],
        'priority': 2,
        'estimated_time': '30-60 分鐘',
        'kaggle_id': 'h-and-m-personalized-fashion-recommendations',
        'competition': True,
        'warning': '包含大量圖片檔案'
    },

    'store-sales': {
        'name': 'Store Sales - Time Series',
        'platform': 'kaggle',
        'category': 'large',
        'size': '-',
        'records': '3M 筆記錄',
        'use_cases': ['時間序列預測', '需求預測'],
        'priority': 1,
        'estimated_time': '5-10 分鐘',
        'kaggle_id': 'store-sales-time-series-forecasting',
        'competition': True
    },

    # ==================== 中型資料集（10萬-100萬筆）====================

    'online-retail': {
        'name': 'Online Retail (UCI)',
        'platform': 'uci',
        'category': 'medium',
        'size': '45 MB',
        'records': '541,909 筆交易',
        'use_cases': ['商業分析', 'RFM 分析'],
        'priority': 1,
        'estimated_time': '1-2 分鐘',
        'uci_id': 352,
        'download_func': 'download_uci_dataset'
    },

    'online-retail-ii': {
        'name': 'Online Retail II (UCI)',
        'platform': 'uci',
        'category': 'medium',
        'size': '-',
        'records': '-',
        'use_cases': ['商業分析', 'RFM 分析'],
        'priority': 2,
        'estimated_time': '1-2 分鐘',
        'uci_id': 502,
        'download_func': 'download_uci_dataset'
    },

    'olist': {
        'name': 'Brazilian E-Commerce (Olist)',
        'platform': 'kaggle',
        'category': 'medium',
        'size': '50 MB',
        'records': '100K 筆訂單',
        'use_cases': ['RFM 分析', '端到端專案'],
        'priority': 1,
        'estimated_time': '3-5 分鐘',
        'kaggle_id': 'olistbr/brazilian-ecommerce'
    },

    'pakistan-retail': {
        'name': 'Pakistan Retail Dataset',
        'platform': 'manual',
        'category': 'medium',
        'size': '-',
        'records': '500K+ 筆交易',
        'use_cases': ['商業分析', '新興市場'],
        'priority': 3,
        'manual_url': 'https://github.com/mm-mazhar/Data-Analysis-and-Visualization-on-Ecommerce-Dataset',
        'note': '需要手動從 GitHub 下載'
    },

    'asos': {
        'name': 'ASOS E-commerce Dataset',
        'platform': 'huggingface',
        'category': 'medium',
        'size': '-',
        'records': '30,845 個商品',
        'use_cases': ['時尚分析', '價格策略'],
        'priority': 3,
        'estimated_time': '2-5 分鐘',
        'download_func': 'download_asos'
    },

    # ==================== 機器學習專用 ====================

    'retail-rocket': {
        'name': 'Retail Rocket Recommender',
        'platform': 'kaggle',
        'category': 'ml',
        'size': '-',
        'records': '-',
        'use_cases': ['協同過濾', '推薦系統'],
        'priority': 2,
        'estimated_time': '5-10 分鐘',
        'kaggle_id': 'retailrocket/ecommerce-dataset'
    },

    'ecommerce-chatbot': {
        'name': 'E-commerce Chatbot Dataset',
        'platform': 'huggingface',
        'category': 'ml',
        'size': '8.47M tokens',
        'records': '-',
        'use_cases': ['聊天機器人', 'NLP'],
        'priority': 3,
        'estimated_time': '2-5 分鐘',
        'download_func': 'download_chatbot'
    },

    'ecommerce-faq': {
        'name': 'E-commerce FAQ Dataset',
        'platform': 'huggingface',
        'category': 'ml',
        'size': '-',
        'records': '79 問答對',
        'use_cases': ['FAQ 系統', '聊天機器人'],
        'priority': 3,
        'estimated_time': '1 分鐘',
        'download_func': 'download_faq'
    },

    'sales-conversations': {
        'name': 'Sales Conversations Dataset',
        'platform': 'huggingface',
        'category': 'ml',
        'size': '-',
        'records': '-',
        'use_cases': ['銷售機器人', '對話系統'],
        'priority': 3,
        'estimated_time': '2-5 分鐘',
        'download_func': 'download_sales_conversations'
    }
}


# ==============================================================================
# 顏色輸出工具
# ==============================================================================

class Colors:
    """ANSI 顏色代碼"""
    HEADER = '\033[95m'
    BLUE = '\033[94m'
    CYAN = '\033[96m'
    GREEN = '\033[92m'
    YELLOW = '\033[93m'
    RED = '\033[91m'
    END = '\033[0m'
    BOLD = '\033[1m'

def color_text(text: str, color: str) -> str:
    """返回帶顏色的文字"""
    return f"{color}{text}{Colors.END}"

def print_header(text: str):
    """列印標題"""
    print("\n" + "=" * 80)
    print(color_text(text, Colors.BOLD + Colors.BLUE))
    print("=" * 80)

def print_success(text: str):
    print(color_text(f"✅ {text}", Colors.GREEN))

def print_error(text: str):
    print(color_text(f"❌ {text}", Colors.RED))

def print_warning(text: str):
    print(color_text(f"⚠️  {text}", Colors.YELLOW))

def print_info(text: str):
    print(color_text(f"ℹ️  {text}", Colors.CYAN))


# ==============================================================================
# 下載器類別
# ==============================================================================

class DatasetDownloader:
    """資料集下載器"""

    def __init__(self, config: Config, dry_run: bool = False, verbose: bool = True):
        self.config = config
        self.dry_run = dry_run
        self.verbose = verbose
        self.results = {}

        # 設定日誌
        self.setup_logging()

    def setup_logging(self):
        """設定日誌系統"""
        log_dir = self.config.dataset_root / 'logs'
        log_dir.mkdir(exist_ok=True)

        log_file = log_dir / f'download_{datetime.now().strftime("%Y%m%d_%H%M%S")}.log'

        logging.basicConfig(
            level=logging.INFO if self.verbose else logging.WARNING,
            format='%(asctime)s - %(levelname)s - %(message)s',
            handlers=[
                logging.FileHandler(log_file),
                logging.StreamHandler()
            ]
        )

        self.logger = logging.getLogger(__name__)

    def download(self, dataset_keys: List[str]) -> Dict[str, str]:
        """下載多個資料集"""
        print_header(f"開始下載 {len(dataset_keys)} 個資料集")

        if self.dry_run:
            print_warning("乾跑模式：不會實際下載")

        for i, key in enumerate(dataset_keys, 1):
            print(f"\n{'='*80}")
            print(f"[{i}/{len(dataset_keys)}] {key}")
            print('='*80)

            try:
                result = self.download_single(key)
                self.results[key] = result

                if result == 'success':
                    print_success(f"{key} 下載成功")
                elif result == 'manual':
                    print_warning(f"{key} 需要手動下載")
                else:
                    print_error(f"{key} 下載失敗")

            except Exception as e:
                self.logger.error(f"Error downloading {key}: {e}", exc_info=True)
                self.results[key] = f'error: {str(e)}'
                print_error(f"{key} 發生錯誤：{e}")

            # 避免請求過於頻繁
            if not self.dry_run and i < len(dataset_keys):
                time.sleep(2)

        return self.results

    def download_single(self, dataset_key: str) -> str:
        """下載單一資料集"""
        if dataset_key not in DATASETS:
            raise ValueError(f"Unknown dataset: {dataset_key}")

        info = DATASETS[dataset_key]
        platform = info['platform']

        # 顯示資訊
        self.print_dataset_info(dataset_key, info)

        if self.dry_run:
            return 'dry-run'

        # 根據平台選擇下載方法
        if platform == 'kaggle':
            return self.download_kaggle(dataset_key, info)
        elif platform == 'uci':
            return self.download_uci(dataset_key, info)
        elif platform == 'huggingface':
            return self.download_huggingface(dataset_key, info)
        elif platform == 'manual':
            return self.download_manual(dataset_key, info)
        else:
            raise ValueError(f"Unsupported platform: {platform}")

    def print_dataset_info(self, key: str, info: Dict):
        """列印資料集資訊"""
        print_info(f"名稱：{info['name']}")
        print_info(f"平台：{info['platform'].upper()}")
        print_info(f"類別：{info['category']}")
        print_info(f"大小：{info['size']}")
        print_info(f"記錄數：{info['records']}")
        print_info(f"用途：{', '.join(info['use_cases'])}")

        if 'estimated_time' in info:
            print_info(f"預估時間：{info['estimated_time']}")

        if 'warning' in info:
            print_warning(info['warning'])

    def download_kaggle(self, key: str, info: Dict) -> str:
        """下載 Kaggle 資料集"""
        output_dir = self.config.dataset_root / 'kaggle' / key
        output_dir.mkdir(parents=True, exist_ok=True)

        kaggle_id = info['kaggle_id']
        is_competition = info.get('competition', False)

        if is_competition:
            command = f"kaggle competitions download -c {kaggle_id} -p {output_dir} --force"
        else:
            command = f"kaggle datasets download -d {kaggle_id} -p {output_dir} --force"

        try:
            self.logger.info(f"Running: {command}")
            subprocess.run(command, shell=True, check=True, capture_output=False)

            # 解壓縮
            self.logger.info("Extracting files...")
            subprocess.run(
                f"cd {output_dir} && unzip -o '*.zip' && rm -f *.zip",
                shell=True,
                check=False
            )

            print_success(f"已儲存至：{output_dir}")
            return 'success'

        except subprocess.CalledProcessError as e:
            self.logger.error(f"Kaggle download failed: {e}")
            return 'failed'

    def download_uci(self, key: str, info: Dict) -> str:
        """下載 UCI 資料集"""
        try:
            from ucimlrepo import fetch_ucirepo
            import pandas as pd

            output_dir = self.config.dataset_root / 'uci' / key
            output_dir.mkdir(parents=True, exist_ok=True)

            uci_id = info['uci_id']
            self.logger.info(f"Fetching UCI dataset {uci_id}...")

            dataset = fetch_ucirepo(id=uci_id)
            df = dataset.data.features

            # 儲存為多種格式
            csv_path = output_dir / f"{key}.csv"
            parquet_path = output_dir / f"{key}.parquet"

            df.to_csv(csv_path, index=False)
            df.to_parquet(parquet_path)

            # 儲存元資料
            readme_path = output_dir / "README.txt"
            with open(readme_path, "w") as f:
                f.write(f"{info['name']}\n")
                f.write(f"Source: UCI Machine Learning Repository\n")
                f.write(f"Records: {len(df):,}\n")
                f.write(f"Columns: {len(df.columns)}\n")

            print_success(f"已儲存至：{output_dir}")
            print_info(f"記錄數：{len(df):,}")

            return 'success'

        except Exception as e:
            self.logger.error(f"UCI download failed: {e}")
            return 'failed'

    def download_huggingface(self, key: str, info: Dict) -> str:
        """下載 HuggingFace 資料集"""
        try:
            from datasets import load_dataset
            import pandas as pd

            output_dir = self.config.dataset_root / 'huggingface' / key
            output_dir.mkdir(parents=True, exist_ok=True)

            # 根據不同資料集使用不同的下載函數
            if 'download_func' in info:
                func_name = info['download_func']
                return getattr(self, func_name)(key, info, output_dir)

            return 'failed'

        except Exception as e:
            self.logger.error(f"HuggingFace download failed: {e}")
            return 'failed'

    def download_amazon_reviews(self, key: str, info: Dict, output_dir: Path) -> str:
        """下載 Amazon Reviews"""
        from datasets import load_dataset
        import pandas as pd

        # 下載子集
        dataset = load_dataset(
            "McAuley-Lab/Amazon-Reviews-2023",
            "raw_review_All_Beauty",
            split="full[:50000]"
        )

        df = dataset.to_pandas()
        df.to_csv(output_dir / "amazon_reviews_beauty_50k.csv", index=False)
        df.to_parquet(output_dir / "amazon_reviews_beauty_50k.parquet")

        print_success(f"已儲存 {len(df):,} 筆評論")
        return 'success'

    def download_asos(self, key: str, info: Dict, output_dir: Path) -> str:
        """下載 ASOS"""
        from datasets import load_dataset
        import pandas as pd

        dataset = load_dataset("TrainingDataPro/asos-e-commerce-dataset")
        df = dataset['train'].to_pandas()

        df.to_csv(output_dir / "asos_products.csv", index=False)
        df.to_parquet(output_dir / "asos_products.parquet")

        print_success(f"已儲存 {len(df):,} 個產品")
        return 'success'

    def download_chatbot(self, key: str, info: Dict, output_dir: Path) -> str:
        """下載聊天機器人資料集"""
        from datasets import load_dataset
        import pandas as pd

        dataset = load_dataset("bitext/Bitext-retail-ecommerce-llm-chatbot-training-dataset")
        df = dataset['train'].to_pandas()

        df.to_csv(output_dir / "chatbot_training.csv", index=False)
        df.to_parquet(output_dir / "chatbot_training.parquet")

        print_success(f"已儲存 {len(df):,} 個訓練樣本")
        return 'success'

    def download_faq(self, key: str, info: Dict, output_dir: Path) -> str:
        """下載 FAQ 資料集"""
        from datasets import load_dataset
        import pandas as pd

        dataset = load_dataset("Andyrasika/Ecommerce_FAQ")
        df = dataset['train'].to_pandas()

        df.to_csv(output_dir / "faq.csv", index=False)
        df.to_json(output_dir / "faq.json", orient='records', indent=2)

        print_success(f"已儲存 {len(df):,} 個 FAQ")
        return 'success'

    def download_sales_conversations(self, key: str, info: Dict, output_dir: Path) -> str:
        """下載銷售對話資料集"""
        from datasets import load_dataset
        import pandas as pd

        dataset = load_dataset("goendalf666/sales-conversations")
        df = dataset['train'].to_pandas()

        df.to_csv(output_dir / "sales_conversations.csv", index=False)
        df.to_parquet(output_dir / "sales_conversations.parquet")

        print_success(f"已儲存 {len(df):,} 個對話")
        return 'success'

    def download_manual(self, key: str, info: Dict) -> str:
        """手動下載指示"""
        print_warning(info['note'])
        print_info(f"URL: {info['manual_url']}")
        print_info(f"請下載並放到：{self.config.dataset_root}/manual/{key}/")
        return 'manual'

    def save_log(self):
        """儲存下載記錄"""
        log_file = self.config.dataset_root / 'download_log.json'

        log_data = {
            'timestamp': datetime.now().isoformat(),
            'total': len(self.results),
            'successful': sum(1 for v in self.results.values() if v == 'success'),
            'failed': sum(1 for v in self.results.values() if v == 'failed'),
            'manual': sum(1 for v in self.results.values() if v == 'manual'),
            'results': self.results,
            'config': {
                'dataset_root': str(self.config.dataset_root),
                'cache_root': str(self.config.cache_root)
            }
        }

        with open(log_file, 'w') as f:
            json.dump(log_data, f, indent=2, ensure_ascii=False)

        print_info(f"下載記錄已儲存：{log_file}")


# ==============================================================================
# 檢查工具
# ==============================================================================

def check_environment(config: Config) -> bool:
    """檢查環境"""
    print_header("環境檢查")

    all_good = True

    # 檢查磁碟
    if not Path('/mnt/data').exists():
        print_error("/mnt/data 不存在！")
        all_good = False
    else:
        print_success("/mnt/data 存在")

    # 檢查路徑
    print_info(f"DATASET_ROOT: {config.dataset_root}")
    print_info(f"CACHE_ROOT: {config.cache_root}")

    # 檢查 Kaggle API
    kaggle_json = config.kaggle_config / 'kaggle.json'
    if not kaggle_json.exists():
        print_warning("Kaggle API 未設定！部份資料集無法下載")
        print_info("請前往 https://www.kaggle.com/account 設定")
    else:
        print_success("Kaggle API 已設定")

    return all_good


def check_dependencies() -> bool:
    """檢查 Python 套件"""
    print_header("檢查 Python 套件")

    required = {
        'kaggle': 'kaggle',
        'ucimlrepo': 'ucimlrepo',
        'datasets': 'datasets',
        'pandas': 'pandas'
    }

    missing = []
    for module, pip_name in required.items():
        try:
            __import__(module)
            print_success(f"{module} ✓")
        except ImportError:
            print_error(f"{module} ✗")
            missing.append(pip_name)

    if missing:
        print_warning(f"\n請執行：pip install {' '.join(missing)}")
        return False

    return True


# ==============================================================================
# 列表工具
# ==============================================================================

def list_datasets(filter_category: Optional[str] = None, filter_priority: Optional[int] = None):
    """列出所有資料集"""
    print_header("📚 可用資料集清單")

    # 過濾
    datasets = DATASETS
    if filter_category:
        datasets = {k: v for k, v in datasets.items() if v['category'] == filter_category}
    if filter_priority:
        datasets = {k: v for k, v in datasets.items() if v['priority'] == filter_priority}

    # 按類別分組
    categories = {}
    for key, info in datasets.items():
        cat = info['category']
        if cat not in categories:
            categories[cat] = []
        categories[cat].append((key, info))

    cat_names = {
        'large': '超大型資料集（百萬筆以上）',
        'medium': '中型資料集（10萬-100萬筆）',
        'ml': '機器學習專用資料集'
    }

    for cat_key in ['large', 'medium', 'ml']:
        if cat_key not in categories:
            continue

        print(f"\n{cat_names[cat_key]}:")
        print("-" * 80)

        for key, info in sorted(categories[cat_key], key=lambda x: x[1]['priority']):
            stars = "⭐" * (4 - info['priority'])
            print(f"\n{stars} {key}")
            print(f"    {info['name']}")
            print(f"    平台: {info['platform'].upper()} | 大小: {info['size']} | 記錄: {info['records']}")
            print(f"    用途: {', '.join(info['use_cases'])}")
            if 'estimated_time' in info:
                print(f"    預估時間: {info['estimated_time']}")

    print("\n" + "=" * 80)
    print(f"總共：{len(datasets)} 個資料集")


# ==============================================================================
# 主程式
# ==============================================================================

def main():
    parser = argparse.ArgumentParser(
        description='電商資料集終極整合下載工具',
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
範例：
  %(prog)s --list                          # 列出所有資料集
  %(prog)s --dataset online-retail         # 下載單一資料集
  %(prog)s --datasets online-retail olist  # 下載多個資料集
  %(prog)s --all                           # 下載所有資料集
  %(prog)s --category large                # 按類別下載
  %(prog)s --priority 1                    # 按優先級下載
  %(prog)s --all --dry-run                 # 乾跑模式
  %(prog)s --all --dataset-root /custom/path  # 自訂路徑
        """
    )

    # 資料集選擇
    parser.add_argument('--dataset', type=str, help='下載單一資料集')
    parser.add_argument('--datasets', nargs='+', help='下載多個資料集')
    parser.add_argument('--all', action='store_true', help='下載所有資料集')
    parser.add_argument('--category', choices=['large', 'medium', 'ml'], help='按類別下載')
    parser.add_argument('--priority', type=int, choices=[1, 2, 3], help='按優先級下載')

    # 路徑設定
    parser.add_argument('--dataset-root', type=str, help='資料集根目錄')
    parser.add_argument('--cache-root', type=str, help='快取根目錄')

    # 其他選項
    parser.add_argument('--list', action='store_true', help='列出所有資料集')
    parser.add_argument('--dry-run', action='store_true', help='乾跑模式（不實際下載）')
    parser.add_argument('--skip-checks', action='store_true', help='跳過環境檢查')
    parser.add_argument('--verbose', action='store_true', help='詳細輸出')

    args = parser.parse_args()

    # 列出資料集
    if args.list:
        list_datasets(filter_category=args.category, filter_priority=args.priority)
        return

    # 建立設定
    config = Config(dataset_root=args.dataset_root, cache_root=args.cache_root)
    config.setup_environment()

    print_header("🚀 電商資料集終極整合下載工具")
    print_info(f"資料集目錄：{config.dataset_root}")
    print_info(f"快取目錄：{config.cache_root}")

    # 環境檢查
    if not args.skip_checks:
        if not check_environment(config):
            print_error("\n環境檢查失敗！")
            sys.exit(1)

        if not check_dependencies():
            sys.exit(1)

    # 確定要下載的資料集
    datasets_to_download = []

    if args.all:
        datasets_to_download = list(DATASETS.keys())
        print_warning(f"\n將下載全部 {len(datasets_to_download)} 個資料集")

    elif args.category:
        datasets_to_download = [k for k, v in DATASETS.items() if v['category'] == args.category]
        print_info(f"\n將下載 {args.category} 類別的 {len(datasets_to_download)} 個資料集")

    elif args.priority:
        datasets_to_download = [k for k, v in DATASETS.items() if v['priority'] == args.priority]
        print_info(f"\n將下載優先級 {args.priority} 的 {len(datasets_to_download)} 個資料集")

    elif args.datasets:
        datasets_to_download = args.datasets
        # 驗證資料集存在
        invalid = [d for d in datasets_to_download if d not in DATASETS]
        if invalid:
            print_error(f"找不到資料集：{', '.join(invalid)}")
            sys.exit(1)

    elif args.dataset:
        if args.dataset not in DATASETS:
            print_error(f"找不到資料集：{args.dataset}")
            print_info("使用 --list 查看可用資料集")
            sys.exit(1)
        datasets_to_download = [args.dataset]

    else:
        list_datasets()
        return

    # 顯示清單並確認
    print("\n" + "=" * 80)
    print(color_text("即將下載以下資料集：", Colors.BOLD))
    for key in datasets_to_download:
        info = DATASETS[key]
        print(f"  • {info['name']} ({info['size']}) - {info['platform'].upper()}")
    print("=" * 80)

    if not args.dry_run:
        confirm = input("\n確認下載？(y/N): ")
        if confirm.lower() != 'y':
            print_warning("已取消")
            return

    # 下載
    downloader = DatasetDownloader(config, dry_run=args.dry_run, verbose=args.verbose)
    results = downloader.download(datasets_to_download)

    # 儲存記錄
    downloader.save_log()

    # 顯示摘要
    print_header("📊 下載摘要")
    success = sum(1 for v in results.values() if v == 'success')
    failed = sum(1 for v in results.values() if v == 'failed')
    manual = sum(1 for v in results.values() if v == 'manual')

    print_success(f"成功：{success} 個")
    if manual > 0:
        print_warning(f"需手動：{manual} 個")
    if failed > 0:
        print_error(f"失敗：{failed} 個")

    print_info(f"\n資料集位置：{config.dataset_root}")

    if not args.dry_run:
        print_header("🎉 下載完成！")
        print("\n建議的下一步：")
        print(f"  1. 查看資料集：cd {config.dataset_root} && find . -type f -name '*.csv' | head -10")
        print("  2. 開始分析：conda activate data_env && jupyter lab")
        print("  3. 查看指南：cat docs/quick_start_datasets.md")


if __name__ == "__main__":
    main()
