"""
資料載入工具模組
提供便捷的 Olist 資料集載入函數

Author: Week 3-6 pandas 進階實戰系統
Date: 2024-12-11
"""

import pandas as pd
import numpy as np
from pathlib import Path
from typing import Tuple, Optional, Dict, List
import warnings

warnings.filterwarnings('ignore')


# ==================== 配置 ====================

# 資料路徑配置
DATA_DIR = Path('/mnt/data/datasets/ecommerce/kaggle/olist')

# Dtype 優化配置
DTYPES_CONFIG = {
    'orders': {
        'order_id': 'string',
        'customer_id': 'string',
        'order_status': 'category'
    },
    'order_items': {
        'order_id': 'string',
        'order_item_id': 'int8',
        'product_id': 'string',
        'seller_id': 'string',
        'price': 'float32',
        'freight_value': 'float32'
    },
    'products': {
        'product_id': 'string',
        'product_category_name': 'category',
        'product_name_length': 'int16',
        'product_description_length': 'int16',
        'product_photos_qty': 'int8',
        'product_weight_g': 'int32',
        'product_length_cm': 'int16',
        'product_height_cm': 'int16',
        'product_width_cm': 'int16'
    },
    'customers': {
        'customer_id': 'string',
        'customer_unique_id': 'string',
        'customer_zip_code_prefix': 'int32',
        'customer_city': 'category',
        'customer_state': 'category'
    },
    'sellers': {
        'seller_id': 'string',
        'seller_zip_code_prefix': 'int32',
        'seller_city': 'category',
        'seller_state': 'category'
    },
    'payments': {
        'order_id': 'string',
        'payment_sequential': 'int8',
        'payment_type': 'category',
        'payment_installments': 'int8',
        'payment_value': 'float32'
    },
    'reviews': {
        'review_id': 'string',
        'order_id': 'string',
        'review_score': 'int8'
    }
}


# ==================== 基礎載入函數 ====================

def load_olist_data(
    data_dir: Optional[Path] = None,
    verbose: bool = True
) -> Tuple[pd.DataFrame, ...]:
    """
    載入 Olist 資料集的所有表（標準載入）

    Parameters
    ----------
    data_dir : Path, optional
        資料目錄路徑，預設為 /mnt/data/datasets/ecommerce/kaggle/olist
    verbose : bool, default True
        是否顯示載入進度

    Returns
    -------
    tuple of DataFrames
        (orders, order_items, products, customers, sellers, payments, reviews)

    Examples
    --------
    >>> orders, order_items, products, customers, sellers, payments, reviews = load_olist_data()
    ✅ 資料載入完成！
    訂單數：99,441
    訂單明細數：112,650
    商品數：32,951
    客戶數：99,441
    """
    if data_dir is None:
        data_dir = DATA_DIR

    if verbose:
        print("📂 開始載入 Olist 資料集...")

    # 載入各表
    orders = pd.read_csv(data_dir / 'olist_orders_dataset.csv')
    order_items = pd.read_csv(data_dir / 'olist_order_items_dataset.csv')
    products = pd.read_csv(data_dir / 'olist_products_dataset.csv')
    customers = pd.read_csv(data_dir / 'olist_customers_dataset.csv')
    sellers = pd.read_csv(data_dir / 'olist_sellers_dataset.csv')
    payments = pd.read_csv(data_dir / 'olist_order_payments_dataset.csv')
    reviews = pd.read_csv(data_dir / 'olist_order_reviews_dataset.csv')

    # 轉換日期欄位
    date_cols = [
        'order_purchase_timestamp',
        'order_approved_at',
        'order_delivered_carrier_date',
        'order_delivered_customer_date',
        'order_estimated_delivery_date'
    ]
    for col in date_cols:
        if col in orders.columns:
            orders[col] = pd.to_datetime(orders[col], errors='coerce')

    # 轉換評論日期
    if 'review_creation_date' in reviews.columns:
        reviews['review_creation_date'] = pd.to_datetime(
            reviews['review_creation_date'], errors='coerce'
        )
    if 'review_answer_timestamp' in reviews.columns:
        reviews['review_answer_timestamp'] = pd.to_datetime(
            reviews['review_answer_timestamp'], errors='coerce'
        )

    # 轉換訂單明細日期
    if 'shipping_limit_date' in order_items.columns:
        order_items['shipping_limit_date'] = pd.to_datetime(
            order_items['shipping_limit_date'], errors='coerce'
        )

    if verbose:
        print("\n✅ 資料載入完成！")
        print(f"📊 訂單數：{len(orders):,}")
        print(f"📊 訂單明細數：{len(order_items):,}")
        print(f"📊 商品數：{len(products):,}")
        print(f"📊 客戶數：{len(customers):,}")
        print(f"📊 賣家數：{len(sellers):,}")
        print(f"📊 付款筆數：{len(payments):,}")
        print(f"📊 評論數：{len(reviews):,}")

    return orders, order_items, products, customers, sellers, payments, reviews


def load_olist_with_optimization(
    data_dir: Optional[Path] = None,
    verbose: bool = True
) -> Tuple[pd.DataFrame, ...]:
    """
    載入 Olist 資料集（記憶體優化版）

    使用優化的 dtype 配置，可減少 60%+ 記憶體使用

    Parameters
    ----------
    data_dir : Path, optional
        資料目錄路徑
    verbose : bool, default True
        是否顯示載入進度與記憶體統計

    Returns
    -------
    tuple of DataFrames
        (orders, order_items, products, customers, sellers, payments, reviews)

    Examples
    --------
    >>> orders, order_items, products, customers, sellers, payments, reviews = load_olist_with_optimization()
    ✅ 資料載入完成！（記憶體優化）
    📊 訂單數：99,441（記憶體：5.2 MB）
    📊 訂單明細數：112,650（記憶體：3.8 MB）
    """
    if data_dir is None:
        data_dir = DATA_DIR

    if verbose:
        print("📂 開始載入 Olist 資料集（記憶體優化）...")

    # 載入並優化各表
    orders = pd.read_csv(
        data_dir / 'olist_orders_dataset.csv',
        dtype=DTYPES_CONFIG['orders']
    )

    order_items = pd.read_csv(
        data_dir / 'olist_order_items_dataset.csv',
        dtype=DTYPES_CONFIG['order_items']
    )

    products = pd.read_csv(
        data_dir / 'olist_products_dataset.csv',
        dtype=DTYPES_CONFIG['products']
    )

    customers = pd.read_csv(
        data_dir / 'olist_customers_dataset.csv',
        dtype=DTYPES_CONFIG['customers']
    )

    sellers = pd.read_csv(
        data_dir / 'olist_sellers_dataset.csv',
        dtype=DTYPES_CONFIG['sellers']
    )

    payments = pd.read_csv(
        data_dir / 'olist_order_payments_dataset.csv',
        dtype=DTYPES_CONFIG['payments']
    )

    reviews = pd.read_csv(
        data_dir / 'olist_order_reviews_dataset.csv',
        dtype=DTYPES_CONFIG['reviews']
    )

    # 轉換日期欄位
    date_cols = [
        'order_purchase_timestamp',
        'order_approved_at',
        'order_delivered_carrier_date',
        'order_delivered_customer_date',
        'order_estimated_delivery_date'
    ]
    for col in date_cols:
        if col in orders.columns:
            orders[col] = pd.to_datetime(orders[col], errors='coerce')

    # 轉換評論日期
    if 'review_creation_date' in reviews.columns:
        reviews['review_creation_date'] = pd.to_datetime(
            reviews['review_creation_date'], errors='coerce'
        )
    if 'review_answer_timestamp' in reviews.columns:
        reviews['review_answer_timestamp'] = pd.to_datetime(
            reviews['review_answer_timestamp'], errors='coerce'
        )

    # 轉換訂單明細日期
    if 'shipping_limit_date' in order_items.columns:
        order_items['shipping_limit_date'] = pd.to_datetime(
            order_items['shipping_limit_date'], errors='coerce'
        )

    if verbose:
        print("\n✅ 資料載入完成！（記憶體優化）")
        print(f"📊 訂單數：{len(orders):,}（記憶體：{orders.memory_usage(deep=True).sum() / 1024**2:.1f} MB）")
        print(f"📊 訂單明細數：{len(order_items):,}（記憶體：{order_items.memory_usage(deep=True).sum() / 1024**2:.1f} MB）")
        print(f"📊 商品數：{len(products):,}（記憶體：{products.memory_usage(deep=True).sum() / 1024**2:.1f} MB）")
        print(f"📊 客戶數：{len(customers):,}（記憶體：{customers.memory_usage(deep=True).sum() / 1024**2:.1f} MB）")

    return orders, order_items, products, customers, sellers, payments, reviews


# ==================== 整合載入函數 ====================

def load_olist_integrated(
    data_dir: Optional[Path] = None,
    include_delivered_only: bool = True,
    include_translation: bool = True,
    optimize_memory: bool = False,
    verbose: bool = True
) -> pd.DataFrame:
    """
    載入並整合 Olist 資料集成單一寬表

    Parameters
    ----------
    data_dir : Path, optional
        資料目錄路徑
    include_delivered_only : bool, default True
        是否只保留已送達的訂單
    include_translation : bool, default True
        是否包含類別英文翻譯
    optimize_memory : bool, default False
        是否使用記憶體優化載入
    verbose : bool, default True
        是否顯示進度

    Returns
    -------
    DataFrame
        整合後的完整資料表

    Examples
    --------
    >>> df = load_olist_integrated()
    ✅ 資料整合完成！
    📊 最終筆數：112,650
    📊 最終欄位數：45
    """
    if data_dir is None:
        data_dir = DATA_DIR

    # 載入資料
    if optimize_memory:
        orders, order_items, products, customers, sellers, payments, reviews = \
            load_olist_with_optimization(data_dir, verbose=False)
    else:
        orders, order_items, products, customers, sellers, payments, reviews = \
            load_olist_data(data_dir, verbose=False)

    if verbose:
        print("🔗 開始整合資料表...")

    # 只保留已送達的訂單
    if include_delivered_only:
        orders = orders[orders['order_status'] == 'delivered'].copy()
        if verbose:
            print(f"✅ 已篩選已送達訂單：{len(orders):,} 筆")

    # Step 1: 訂單 + 客戶
    df = orders.merge(customers, on='customer_id', how='left')
    if verbose:
        print(f"✅ 訂單 + 客戶：{len(df):,} 筆")

    # Step 2: + 訂單明細
    df = df.merge(order_items, on='order_id', how='left')
    if verbose:
        print(f"✅ + 訂單明細：{len(df):,} 筆")

    # Step 3: + 商品
    df = df.merge(products, on='product_id', how='left')
    if verbose:
        print(f"✅ + 商品：{len(df):,} 筆")

    # Step 4: + 類別翻譯
    if include_translation:
        category_translation = pd.read_csv(
            data_dir / 'product_category_name_translation.csv'
        )
        df = df.merge(
            category_translation,
            on='product_category_name',
            how='left'
        )
        if verbose:
            print(f"✅ + 類別翻譯：{len(df):,} 筆")

    # Step 5: + 付款資訊（先聚合）
    payment_summary = payments.groupby('order_id').agg({
        'payment_value': 'sum',
        'payment_type': lambda x: ', '.join(x.unique()),
        'payment_installments': 'mean'
    }).reset_index()
    payment_summary.columns = [
        'order_id',
        'total_payment',
        'payment_methods',
        'avg_installments'
    ]

    df = df.merge(payment_summary, on='order_id', how='left')
    if verbose:
        print(f"✅ + 付款資訊：{len(df):,} 筆")

    # Step 6: + 評論
    review_summary = reviews[['order_id', 'review_score']]
    df = df.merge(review_summary, on='order_id', how='left')
    if verbose:
        print(f"✅ + 評論：{len(df):,} 筆")

    if verbose:
        print(f"\n✅ 資料整合完成！")
        print(f"📊 最終筆數：{len(df):,}")
        print(f"📊 最終欄位數：{len(df.columns)}")
        print(f"💾 記憶體使用：{df.memory_usage(deep=True).sum() / 1024**2:.1f} MB")

    return df


# ==================== 資料驗證函數 ====================

def validate_olist_data(
    orders: pd.DataFrame,
    order_items: pd.DataFrame,
    products: pd.DataFrame,
    customers: pd.DataFrame,
    verbose: bool = True
) -> Dict[str, any]:
    """
    驗證 Olist 資料的完整性與品質

    Parameters
    ----------
    orders, order_items, products, customers : DataFrame
        各個資料表
    verbose : bool, default True
        是否顯示詳細驗證結果

    Returns
    -------
    dict
        驗證結果字典

    Examples
    --------
    >>> result = validate_olist_data(orders, order_items, products, customers)
    ✅ 資料驗證完成
    """
    if verbose:
        print("🔍 開始驗證資料...")

    validation_results = {}

    # 1. 檢查主鍵唯一性
    validation_results['orders_unique'] = orders['order_id'].is_unique
    validation_results['products_unique'] = products['product_id'].is_unique

    # 2. 檢查外鍵關係
    order_items_in_orders = order_items['order_id'].isin(orders['order_id'])
    validation_results['order_items_fk_valid'] = order_items_in_orders.all()
    validation_results['order_items_orphan_count'] = (~order_items_in_orders).sum()

    # 3. 檢查缺失值
    validation_results['orders_missing'] = orders.isnull().sum().to_dict()
    validation_results['products_missing'] = products.isnull().sum().to_dict()

    # 4. 檢查異常值
    validation_results['negative_prices'] = (order_items['price'] < 0).sum()
    validation_results['zero_prices'] = (order_items['price'] == 0).sum()

    if verbose:
        print("\n📊 驗證結果：")
        print(f"✅ orders 主鍵唯一：{validation_results['orders_unique']}")
        print(f"✅ products 主鍵唯一：{validation_results['products_unique']}")
        print(f"✅ order_items 外鍵有效：{validation_results['order_items_fk_valid']}")
        if validation_results['order_items_orphan_count'] > 0:
            print(f"⚠️  order_items 孤兒記錄：{validation_results['order_items_orphan_count']} 筆")
        print(f"⚠️  負價格數量：{validation_results['negative_prices']} 筆")
        print(f"⚠️  零價格數量：{validation_results['zero_prices']} 筆")

    return validation_results


# ==================== 快速統計函數 ====================

def get_olist_summary(
    orders: pd.DataFrame,
    order_items: pd.DataFrame,
    customers: pd.DataFrame,
    products: pd.DataFrame
) -> pd.DataFrame:
    """
    獲取 Olist 資料集的快速統計摘要

    Parameters
    ----------
    orders, order_items, customers, products : DataFrame
        各個資料表

    Returns
    -------
    DataFrame
        統計摘要表

    Examples
    --------
    >>> summary = get_olist_summary(orders, order_items, customers, products)
    >>> print(summary)
    """
    summary_data = {
        '指標': [
            '訂單總數',
            '已送達訂單數',
            '訂單明細數',
            '商品數',
            '客戶數',
            '獨立客戶數',
            '平均訂單金額',
            '總營收',
            '時間範圍'
        ],
        '數值': [
            f"{len(orders):,}",
            f"{(orders['order_status'] == 'delivered').sum():,}",
            f"{len(order_items):,}",
            f"{len(products):,}",
            f"{len(customers):,}",
            f"{customers['customer_unique_id'].nunique():,}",
            f"R$ {order_items['price'].mean():.2f}",
            f"R$ {order_items['price'].sum():,.2f}",
            f"{orders['order_purchase_timestamp'].min().date()} 至 {orders['order_purchase_timestamp'].max().date()}"
        ]
    }

    return pd.DataFrame(summary_data)


# ==================== 範例使用 ====================

if __name__ == '__main__':
    # 範例 1：標準載入
    print("=" * 60)
    print("範例 1：標準載入")
    print("=" * 60)
    orders, order_items, products, customers, sellers, payments, reviews = load_olist_data()

    print("\n" + "=" * 60)
    print("範例 2：記憶體優化載入")
    print("=" * 60)
    orders_opt, order_items_opt, products_opt, customers_opt, sellers_opt, payments_opt, reviews_opt = \
        load_olist_with_optimization()

    # 記憶體對比
    print("\n💾 記憶體對比：")
    print(f"標準載入 - orders: {orders.memory_usage(deep=True).sum() / 1024**2:.1f} MB")
    print(f"優化載入 - orders: {orders_opt.memory_usage(deep=True).sum() / 1024**2:.1f} MB")
    memory_saved = (1 - orders_opt.memory_usage(deep=True).sum() / orders.memory_usage(deep=True).sum()) * 100
    print(f"節省記憶體：{memory_saved:.1f}%")

    print("\n" + "=" * 60)
    print("範例 3：整合載入")
    print("=" * 60)
    df_integrated = load_olist_integrated(optimize_memory=True)

    print("\n" + "=" * 60)
    print("範例 4：資料驗證")
    print("=" * 60)
    validation = validate_olist_data(orders, order_items, products, customers)

    print("\n" + "=" * 60)
    print("範例 5：快速統計")
    print("=" * 60)
    summary = get_olist_summary(orders, order_items, customers, products)
    print(summary.to_string(index=False))

    print("\n✅ 所有範例執行完成！")
