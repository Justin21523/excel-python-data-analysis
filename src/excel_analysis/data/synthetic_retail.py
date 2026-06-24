from __future__ import annotations

from pathlib import Path

import numpy as np
import pandas as pd


def generate_retail_data(seed: int = 42) -> dict[str, pd.DataFrame]:
    rng = np.random.default_rng(seed)
    customers = pd.DataFrame(
        {
            "customer_id": [f"C{idx:04d}" for idx in range(1, 121)],
            "customer_name": [f"Customer {idx}" for idx in range(1, 121)],
            "email": [f"customer{idx}@example.com" for idx in range(1, 121)],
            "region": rng.choice(["North", "South", "East", "West"], 120),
            "signup_date": pd.date_range("2023-01-01", periods=120, freq="3D"),
        }
    )

    categories = ["Electronics", "Home", "Beauty", "Sports", "Books", "Grocery"]
    products = pd.DataFrame(
        {
            "product_id": [f"P{idx:04d}" for idx in range(1, 61)],
            "product_name": [f"Product {idx}" for idx in range(1, 61)],
            "category": rng.choice(categories, 60),
            "unit_cost": rng.uniform(5, 120, 60).round(2),
            "unit_price": rng.uniform(15, 260, 60).round(2),
            "current_stock": rng.integers(15, 500, 60),
            "lead_time_days": rng.integers(3, 21, 60),
        }
    )

    order_ids = [f"O{idx:05d}" for idx in range(1, 421)]
    order_dates = pd.to_datetime(
        rng.choice(pd.date_range("2024-01-01", "2024-12-15", freq="D"), len(order_ids))
    ).sort_values()
    orders = pd.DataFrame(
        {
            "order_id": order_ids,
            "customer_id": rng.choice(customers["customer_id"], len(order_ids)),
            "order_date": order_dates,
            "region": rng.choice(["North", "South", "East", "West"], len(order_ids)),
            "order_status": rng.choice(
                ["delivered", "shipped", "cancelled"],
                len(order_ids),
                p=[0.88, 0.08, 0.04],
            ),
        }
    )

    items = []
    for order_id in order_ids:
        for item_no in range(1, int(rng.integers(2, 6))):
            product = products.sample(1, random_state=int(rng.integers(1, 100000))).iloc[0]
            quantity = int(rng.integers(1, 5))
            discount = float(rng.choice([0, 0.05, 0.1, 0.15], p=[0.55, 0.2, 0.15, 0.1]))
            items.append(
                {
                    "order_id": order_id,
                    "item_no": item_no,
                    "product_id": product["product_id"],
                    "quantity": quantity,
                    "unit_price": float(product["unit_price"]),
                    "discount": discount,
                    "line_total": round(quantity * float(product["unit_price"]) * (1 - discount), 2),
                }
            )
    order_items = pd.DataFrame(items)

    inventory = products[["product_id", "product_name", "category", "current_stock", "lead_time_days"]].copy()
    sales_qty = order_items.groupby("product_id")["quantity"].sum().rename("quantity_sold_365d")
    inventory = inventory.merge(sales_qty, on="product_id", how="left").fillna({"quantity_sold_365d": 0})
    inventory["safety_stock"] = rng.integers(10, 80, len(inventory))
    inventory["reorder_point"] = (inventory["quantity_sold_365d"] / 365 * inventory["lead_time_days"] + inventory["safety_stock"]).round(0)

    # 加入少量品質問題，用於展示 profiling/quality checker。
    orders.loc[5, "customer_id"] = None
    order_items.loc[10, "quantity"] = -2
    products.loc[3, "category"] = " electronics "

    return {
        "orders": orders,
        "order_items": order_items,
        "customers": customers,
        "products": products,
        "inventory": inventory,
    }


def create_retail_workbook(output_path: str | Path, seed: int = 42) -> Path:
    output = Path(output_path)
    output.parent.mkdir(parents=True, exist_ok=True)
    data = generate_retail_data(seed=seed)
    with pd.ExcelWriter(output, engine="openpyxl") as writer:
        for sheet_name, df in data.items():
            df.to_excel(writer, sheet_name=sheet_name, index=False)
    return output


def create_messy_sales_workbook(output_path: str | Path, seed: int = 42) -> Path:
    output = Path(output_path)
    output.parent.mkdir(parents=True, exist_ok=True)
    rng = np.random.default_rng(seed)
    rows = 180
    sales = pd.DataFrame(
        {
            "order_id": [f"MS{idx:05d}" for idx in range(rows)],
            "order_date": pd.date_range("2024-01-01", periods=rows, freq="2D").astype(str),
            "customer": [f" Customer {idx % 45} " for idx in range(rows)],
            "region": rng.choice(["north", "North ", " SOUTH", "East", "west"], rows),
            "category": rng.choice(["Electronics", "electronics ", "Home", "home ", "Beauty"], rows),
            "quantity": rng.integers(1, 8, rows),
            "unit_price": [f"${value:,.2f}" for value in rng.uniform(12, 320, rows)],
            "discount_pct": rng.choice(["0%", "5%", "10%", "bad"], rows, p=[0.5, 0.25, 0.2, 0.05]),
        }
    )
    # 故意加入常見 Excel 問題，供 cleaning/profiling 展示。
    sales.loc[4, "order_date"] = "not-a-date"
    sales.loc[8, "quantity"] = -3
    sales.loc[12, "customer"] = None
    sales = pd.concat([sales, sales.iloc[[3, 7]]], ignore_index=True)
    notes = pd.DataFrame(
        {
            "issue": ["negative quantity", "bad date", "duplicate rows", "currency strings"],
            "expected_fix": ["flag for review", "parse as NaT", "drop exact duplicate", "convert to numeric"],
        }
    )
    _write_workbook(output, {"messy_sales": sales, "cleaning_notes": notes})
    return output


def create_finance_workbook(output_path: str | Path, seed: int = 42) -> Path:
    output = Path(output_path)
    output.parent.mkdir(parents=True, exist_ok=True)
    rng = np.random.default_rng(seed)
    months = pd.period_range("2024-01", periods=12, freq="M").astype(str)
    revenue = pd.DataFrame(
        {
            "month": months,
            "product_revenue": rng.uniform(80000, 150000, 12).round(2),
            "service_revenue": rng.uniform(12000, 30000, 12).round(2),
            "other_revenue": rng.uniform(1500, 7000, 12).round(2),
        }
    )
    expenses = pd.DataFrame(
        {
            "month": months,
            "cogs": rng.uniform(35000, 72000, 12).round(2),
            "payroll": rng.uniform(18000, 26000, 12).round(2),
            "marketing": rng.uniform(5000, 18000, 12).round(2),
            "operations": rng.uniform(8000, 16000, 12).round(2),
        }
    )
    budget = pd.DataFrame(
        {
            "month": months,
            "budget_revenue": np.linspace(95000, 155000, 12).round(2),
            "budget_expense": np.linspace(68000, 98000, 12).round(2),
        }
    )
    cash_flow = pd.DataFrame(
        {
            "month": months,
            "opening_cash": np.linspace(50000, 92000, 12).round(2),
            "cash_in": revenue[["product_revenue", "service_revenue", "other_revenue"]].sum(axis=1),
            "cash_out": expenses[["cogs", "payroll", "marketing", "operations"]].sum(axis=1),
        }
    )
    formulas = pd.DataFrame(
        {
            "metric": ["total_revenue", "total_expense", "net_profit", "profit_margin"],
            "excel_formula_pattern": ["=SUM(revenue row)", "=SUM(expense row)", "=revenue-expense", "=profit/revenue"],
        }
    )
    _write_workbook(output, {"revenue": revenue, "expenses": expenses, "budget_vs_actual": budget, "cash_flow": cash_flow, "formula_notes": formulas})
    return output


def create_inventory_planning_workbook(output_path: str | Path, seed: int = 42) -> Path:
    output = Path(output_path)
    output.parent.mkdir(parents=True, exist_ok=True)
    rng = np.random.default_rng(seed)
    sku_count = 80
    planning = pd.DataFrame(
        {
            "sku": [f"SKU{idx:04d}" for idx in range(sku_count)],
            "category": rng.choice(["A", "B", "C", "D"], sku_count),
            "current_stock": rng.integers(10, 900, sku_count),
            "avg_daily_demand": rng.uniform(1, 45, sku_count).round(2),
            "demand_std": rng.uniform(0.5, 12, sku_count).round(2),
            "lead_time_days": rng.integers(3, 30, sku_count),
            "service_level": rng.choice([0.9, 0.95, 0.98], sku_count),
            "unit_cost": rng.uniform(4, 180, sku_count).round(2),
        }
    )
    planning["safety_stock"] = (1.65 * planning["demand_std"] * np.sqrt(planning["lead_time_days"])).round(0)
    planning["reorder_point"] = (planning["avg_daily_demand"] * planning["lead_time_days"] + planning["safety_stock"]).round(0)
    planning["stockout_risk"] = planning["current_stock"] < planning["reorder_point"]
    suppliers = pd.DataFrame(
        {
            "supplier": [f"Supplier {idx}" for idx in range(1, 11)],
            "average_lead_time": rng.integers(5, 25, 10),
            "on_time_rate": rng.uniform(0.82, 0.99, 10).round(3),
        }
    )
    _write_workbook(output, {"inventory_plan": planning, "suppliers": suppliers})
    return output


def create_customer_segmentation_workbook(output_path: str | Path, seed: int = 42) -> Path:
    output = Path(output_path)
    output.parent.mkdir(parents=True, exist_ok=True)
    rng = np.random.default_rng(seed)
    customer_count = 160
    customers = pd.DataFrame(
        {
            "customer_id": [f"CS{idx:04d}" for idx in range(customer_count)],
            "signup_date": pd.date_range("2022-01-01", periods=customer_count, freq="5D"),
            "region": rng.choice(["North", "South", "East", "West"], customer_count),
            "email_opt_in": rng.choice([True, False], customer_count, p=[0.7, 0.3]),
            "support_tickets": rng.poisson(1.2, customer_count),
        }
    )
    orders = pd.DataFrame(
        {
            "order_id": [f"CSO{idx:05d}" for idx in range(600)],
            "customer_id": rng.choice(customers["customer_id"], 600),
            "order_date": pd.to_datetime(rng.choice(pd.date_range("2023-01-01", "2024-12-20", freq="D"), 600)),
            "order_amount": rng.gamma(3.0, 48.0, 600).round(2),
            "channel": rng.choice(["web", "store", "marketplace"], 600),
        }
    )
    engagement = pd.DataFrame(
        {
            "customer_id": customers["customer_id"],
            "email_opens_90d": rng.poisson(6, customer_count),
            "site_visits_90d": rng.poisson(12, customer_count),
            "loyalty_points": rng.integers(0, 8000, customer_count),
        }
    )
    _write_workbook(output, {"customers": customers, "orders": orders, "engagement": engagement})
    return output


def create_all_sample_workbooks(output_dir: str | Path = "data/sample", seed: int = 42) -> list[Path]:
    output = Path(output_dir)
    output.mkdir(parents=True, exist_ok=True)
    return [
        create_retail_workbook(output / "retail_demo.xlsx", seed=seed),
        create_messy_sales_workbook(output / "messy_sales.xlsx", seed=seed),
        create_finance_workbook(output / "finance_workbook.xlsx", seed=seed),
        create_inventory_planning_workbook(output / "inventory_planning.xlsx", seed=seed),
        create_customer_segmentation_workbook(output / "customer_segmentation.xlsx", seed=seed),
    ]


def _write_workbook(output: Path, sheets: dict[str, pd.DataFrame]) -> None:
    with pd.ExcelWriter(output, engine="openpyxl") as writer:
        for sheet_name, df in sheets.items():
            df.to_excel(writer, sheet_name=sheet_name[:31], index=False)
