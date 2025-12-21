"""
示例資料生成器

用於為各個 ETL 系統生成測試資料
"""

import pandas as pd
import numpy as np
from pathlib import Path
from datetime import datetime, timedelta
import random


def generate_orders_data(num_records: int = 1000) -> pd.DataFrame:
    """生成訂單資料"""
    np.random.seed(42)

    customer_ids = [f"C{str(i).zfill(4)}" for i in range(1, 101)]
    product_ids = [f"P{str(i).zfill(4)}" for i in range(1, 51)]
    statuses = ['pending', 'completed', 'cancelled', 'processing']

    data = {
        'order_id': [f"ORD{str(i).zfill(6)}" for i in range(1, num_records + 1)],
        'customer_id': np.random.choice(customer_ids, num_records),
        'order_date': [
            (datetime.now() - timedelta(days=random.randint(0, 90))).strftime('%Y-%m-%d')
            for _ in range(num_records)
        ],
        'product_id': np.random.choice(product_ids, num_records),
        'quantity': np.random.randint(1, 100, num_records),
        'unit_price': np.random.uniform(10, 1000, num_records).round(2),
        'status': np.random.choice(statuses, num_records),
    }

    df = pd.DataFrame(data)
    df['amount'] = (df['quantity'] * df['unit_price']).round(2)

    return df


def generate_customers_data(num_records: int = 100) -> pd.DataFrame:
    """生成客戶資料"""
    np.random.seed(42)

    first_names = ['Alice', 'Bob', 'Charlie', 'David', 'Eva', 'Frank', 'Grace', 'Henry']
    last_names = ['Smith', 'Johnson', 'Williams', 'Brown', 'Jones', 'Garcia', 'Miller', 'Davis']
    cities = ['New York', 'Los Angeles', 'Chicago', 'Houston', 'Phoenix', 'Philadelphia', 'San Antonio', 'San Diego']

    data = {
        'customer_id': [f"C{str(i).zfill(4)}" for i in range(1, num_records + 1)],
        'first_name': np.random.choice(first_names, num_records),
        'last_name': np.random.choice(last_names, num_records),
        'email': [f"user{i}@example.com" for i in range(1, num_records + 1)],
        'phone': [f"555-{random.randint(100, 999):03d}-{random.randint(1000, 9999):04d}" for _ in range(num_records)],
        'city': np.random.choice(cities, num_records),
        'registration_date': [
            (datetime.now() - timedelta(days=random.randint(1, 730))).strftime('%Y-%m-%d')
            for _ in range(num_records)
        ],
        'status': np.random.choice(['active', 'inactive', 'suspended'], num_records),
    }

    return pd.DataFrame(data)


def generate_products_data(num_records: int = 50) -> pd.DataFrame:
    """生成產品資料"""
    np.random.seed(42)

    categories = ['Electronics', 'Clothing', 'Books', 'Home', 'Sports', 'Toys']

    data = {
        'product_id': [f"P{str(i).zfill(4)}" for i in range(1, num_records + 1)],
        'product_name': [f"Product {i}" for i in range(1, num_records + 1)],
        'category': np.random.choice(categories, num_records),
        'price': np.random.uniform(10, 1000, num_records).round(2),
        'stock': np.random.randint(0, 1000, num_records),
        'supplier': [f"Supplier {random.randint(1, 20)}" for _ in range(num_records)],
        'last_updated': [datetime.now().strftime('%Y-%m-%d') for _ in range(num_records)],
    }

    return pd.DataFrame(data)


def generate_all_data():
    """生成所有示例資料"""

    # 建立資料目錄
    data_dir = Path("./data")
    raw_dir = data_dir / "raw"
    raw_dir.mkdir(parents=True, exist_ok=True)

    print("生成示例資料...")

    # 生成訂單資料
    print("  - 生成訂單資料...")
    orders_df = generate_orders_data(1000)
    orders_df.to_csv(raw_dir / "orders.csv", index=False, encoding='utf-8')
    orders_df.to_excel(raw_dir / "orders.xlsx", index=False)

    # 生成客戶資料
    print("  - 生成客戶資料...")
    customers_df = generate_customers_data(100)
    customers_df.to_csv(raw_dir / "customers.csv", index=False, encoding='utf-8')
    customers_df.to_excel(raw_dir / "customers.xlsx", index=False)

    # 生成產品資料
    print("  - 生成產品資料...")
    products_df = generate_products_data(50)
    products_df.to_csv(raw_dir / "products.csv", index=False, encoding='utf-8')
    products_df.to_excel(raw_dir / "products.xlsx", index=False)

    # 生成銷售資料
    print("  - 生成銷售資料...")
    sales_df = generate_orders_data(800)
    sales_df.to_csv(raw_dir / "sales.csv", index=False, encoding='utf-8')

    # 生成庫存資料
    print("  - 生成庫存資料...")
    inventory_df = generate_products_data(50)
    inventory_df['quantity'] = inventory_df['stock']
    inventory_df = inventory_df[['product_id', 'product_name', 'quantity']]
    inventory_df.to_excel(raw_dir / "inventory.xlsx", index=False)

    print(f"✓ 資料生成完成，已保存到 {raw_dir}")
    print(f"  - orders.csv (1000 行)")
    print(f"  - customers.csv (100 行)")
    print(f"  - products.csv (50 行)")
    print(f"  - sales.csv (800 行)")
    print(f"  - inventory.xlsx (50 行)")


if __name__ == "__main__":
    generate_all_data()
