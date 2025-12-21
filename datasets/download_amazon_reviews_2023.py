#!/usr/bin/env python3
"""
Amazon Reviews 2023 完整下載腳本
從官方 UCSD 網站下載所有 33 個類別的評論和元資料
"""

import os
import requests
from pathlib import Path
from tqdm import tqdm
import time

# 配置
BASE_URL = "https://mcauleylab.ucsd.edu/public_datasets/data/amazon_2023/raw"
OUTPUT_DIR = Path("/mnt/data/datasets/ecommerce/amazon-reviews-2023")
REVIEW_DIR = OUTPUT_DIR / "reviews"
META_DIR = OUTPUT_DIR / "metadata"

# 33 個類別
CATEGORIES = [
    "All_Beauty",
    "Amazon_Fashion",
    "Appliances",
    "Arts_Crafts_and_Sewing",
    "Automotive",
    "Baby_Products",
    "Beauty_and_Personal_Care",
    "Books",
    "CDs_and_Vinyl",
    "Cell_Phones_and_Accessories",
    "Clothing_Shoes_and_Jewelry",
    "Digital_Music",
    "Electronics",
    "Gift_Cards",
    "Grocery_and_Gourmet_Food",
    "Handmade_Products",
    "Health_and_Household",
    "Health_and_Personal_Care",
    "Home_and_Kitchen",
    "Industrial_and_Scientific",
    "Kindle_Store",
    "Magazine_Subscriptions",
    "Movies_and_TV",
    "Musical_Instruments",
    "Office_Products",
    "Patio_Lawn_and_Garden",
    "Pet_Supplies",
    "Software",
    "Sports_and_Outdoors",
    "Subscription_Boxes",
    "Tools_and_Home_Improvement",
    "Toys_and_Games",
    "Video_Games",
]

def download_file(url: str, output_path: Path, desc: str = "Downloading"):
    """下載單個檔案，顯示進度條"""
    try:
        response = requests.get(url, stream=True, timeout=30)
        response.raise_for_status()

        total_size = int(response.headers.get('content-length', 0))

        output_path.parent.mkdir(parents=True, exist_ok=True)

        with open(output_path, 'wb') as f, tqdm(
            desc=desc,
            total=total_size,
            unit='B',
            unit_scale=True,
            unit_divisor=1024,
        ) as pbar:
            for chunk in response.iter_content(chunk_size=8192):
                if chunk:
                    f.write(chunk)
                    pbar.update(len(chunk))

        return True
    except requests.exceptions.RequestException as e:
        print(f"  ❌ 下載失敗: {e}")
        return False
    except Exception as e:
        print(f"  ❌ 錯誤: {e}")
        return False

def main():
    print("=" * 80)
    print("🚀 Amazon Reviews 2023 完整下載工具")
    print("=" * 80)
    print(f"📁 輸出目錄: {OUTPUT_DIR}")
    print(f"📦 類別數量: {len(CATEGORIES)}")
    print(f"📊 預計下載: 評論 + 元資料 = {len(CATEGORIES) * 2} 個檔案")
    print("=" * 80)

    # 創建目錄
    REVIEW_DIR.mkdir(parents=True, exist_ok=True)
    META_DIR.mkdir(parents=True, exist_ok=True)

    # 下載統計
    stats = {
        "reviews_success": 0,
        "reviews_failed": 0,
        "meta_success": 0,
        "meta_failed": 0,
    }

    # 下載每個類別
    for i, category in enumerate(CATEGORIES, 1):
        print(f"\n[{i}/{len(CATEGORIES)}] 📂 {category}")
        print("-" * 80)

        # 1. 下載評論資料
        review_filename = f"{category}.jsonl.gz"
        review_url = f"{BASE_URL}/review_categories/{review_filename}"
        review_path = REVIEW_DIR / review_filename

        if review_path.exists():
            print(f"  ✅ 評論已存在: {review_path.name}")
            stats["reviews_success"] += 1
        else:
            print(f"  📥 下載評論: {review_filename}")
            if download_file(review_url, review_path, f"  {category} Reviews"):
                size_mb = review_path.stat().st_size / (1024 * 1024)
                print(f"  ✅ 評論下載成功: {size_mb:.2f} MB")
                stats["reviews_success"] += 1
            else:
                stats["reviews_failed"] += 1

        # 短暫延遲，避免請求過快
        time.sleep(1)

        # 2. 下載元資料
        meta_filename = f"meta_{category}.jsonl.gz"
        meta_url = f"{BASE_URL}/meta_categories/{meta_filename}"
        meta_path = META_DIR / meta_filename

        if meta_path.exists():
            print(f"  ✅ 元資料已存在: {meta_path.name}")
            stats["meta_success"] += 1
        else:
            print(f"  📥 下載元資料: {meta_filename}")
            if download_file(meta_url, meta_path, f"  {category} Metadata"):
                size_mb = meta_path.stat().st_size / (1024 * 1024)
                print(f"  ✅ 元資料下載成功: {size_mb:.2f} MB")
                stats["meta_success"] += 1
            else:
                stats["meta_failed"] += 1

        # 短暫延遲
        time.sleep(1)

    # 最終統計
    print("\n" + "=" * 80)
    print("📊 下載完成統計")
    print("=" * 80)
    print(f"✅ 評論成功: {stats['reviews_success']}/{len(CATEGORIES)}")
    print(f"❌ 評論失敗: {stats['reviews_failed']}/{len(CATEGORIES)}")
    print(f"✅ 元資料成功: {stats['meta_success']}/{len(CATEGORIES)}")
    print(f"❌ 元資料失敗: {stats['meta_failed']}/{len(CATEGORIES)}")
    print("=" * 80)

    # 計算總大小
    total_size = 0
    for file_path in OUTPUT_DIR.rglob("*.jsonl.gz"):
        total_size += file_path.stat().st_size

    total_size_gb = total_size / (1024 ** 3)
    print(f"💾 總下載大小: {total_size_gb:.2f} GB")
    print(f"📁 檔案位置: {OUTPUT_DIR}")

    # 創建 README
    readme_path = OUTPUT_DIR / "README.txt"
    with open(readme_path, "w", encoding="utf-8") as f:
        f.write("Amazon Reviews 2023 Dataset\n")
        f.write("=" * 80 + "\n\n")
        f.write(f"下載日期: {time.strftime('%Y-%m-%d %H:%M:%S')}\n")
        f.write(f"類別數量: {len(CATEGORIES)}\n")
        f.write(f"總大小: {total_size_gb:.2f} GB\n\n")
        f.write("資料格式: JSONL.gz (壓縮的 JSON Lines)\n")
        f.write("時間範圍: 1996年5月 - 2023年9月\n\n")
        f.write("目錄結構:\n")
        f.write("  reviews/    - 評論資料 (33 個類別)\n")
        f.write("  metadata/   - 商品元資料 (33 個類別)\n\n")
        f.write("讀取範例:\n")
        f.write("```python\n")
        f.write("import gzip\n")
        f.write("import json\n\n")
        f.write("with gzip.open('reviews/Electronics.jsonl.gz', 'rt', encoding='utf-8') as f:\n")
        f.write("    for line in f:\n")
        f.write("        review = json.loads(line.strip())\n")
        f.write("        print(review)\n")
        f.write("        break\n")
        f.write("```\n")

    print(f"📝 README 已創建: {readme_path}")
    print("\n🎉 所有下載完成！")

if __name__ == "__main__":
    main()
