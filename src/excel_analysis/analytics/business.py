from __future__ import annotations

from itertools import combinations

import pandas as pd


def _orders_items(datasets: dict[str, pd.DataFrame]) -> pd.DataFrame:
    orders = datasets["orders"].copy()
    items = datasets["order_items"].copy()
    df = items.merge(orders, on="order_id", how="left")
    df["order_date"] = pd.to_datetime(df["order_date"], errors="coerce")
    df["line_total"] = pd.to_numeric(df["line_total"], errors="coerce")
    df["quantity"] = pd.to_numeric(df["quantity"], errors="coerce")
    return df


def sales_analysis(datasets: dict[str, pd.DataFrame]) -> dict[str, object]:
    df = _orders_items(datasets)
    delivered = df[df["order_status"] != "cancelled"].copy()
    monthly = delivered.set_index("order_date").resample("ME")["line_total"].sum().reset_index()
    monthly["growth_rate"] = monthly["line_total"].pct_change().fillna(0)
    by_region = delivered.groupby("region", dropna=False)["line_total"].sum().sort_values(ascending=False).reset_index()
    by_product = delivered.groupby("product_id")["line_total"].sum().sort_values(ascending=False).head(10).reset_index()
    return {
        "kpis": {
            "total_revenue": round(float(delivered["line_total"].sum()), 2),
            "order_count": int(delivered["order_id"].nunique()),
            "average_order_value": round(float(delivered.groupby("order_id")["line_total"].sum().mean()), 2),
            "items_sold": int(delivered["quantity"].clip(lower=0).sum()),
        },
        "monthly_revenue": monthly,
        "revenue_by_region": by_region,
        "top_products": by_product,
    }


def customer_analysis(datasets: dict[str, pd.DataFrame]) -> dict[str, object]:
    df = _orders_items(datasets)
    customer_orders = df.groupby("customer_id").agg(
        total_revenue=("line_total", "sum"),
        orders=("order_id", "nunique"),
        first_order=("order_date", "min"),
        last_order=("order_date", "max"),
    ).reset_index()
    customer_orders["purchase_frequency"] = customer_orders["orders"]
    customer_orders["customer_lifetime_days"] = (customer_orders["last_order"] - customer_orders["first_order"]).dt.days.clip(lower=1)
    returning = int((customer_orders["orders"] > 1).sum())
    return {
        "customer_metrics": customer_orders.sort_values("total_revenue", ascending=False),
        "summary": {
            "customers": int(customer_orders["customer_id"].nunique()),
            "returning_customers": returning,
            "returning_customer_rate": round(returning / max(len(customer_orders), 1), 4),
            "average_lifetime_revenue": round(float(customer_orders["total_revenue"].mean()), 2),
        },
    }


def rfm_segmentation(datasets: dict[str, pd.DataFrame]) -> pd.DataFrame:
    df = _orders_items(datasets)
    snapshot = df["order_date"].max() + pd.Timedelta(days=1)
    rfm = df.groupby("customer_id").agg(
        recency=("order_date", lambda value: (snapshot - value.max()).days),
        frequency=("order_id", "nunique"),
        monetary=("line_total", "sum"),
    )
    for col in ["recency", "frequency", "monetary"]:
        ascending = col == "recency"
        rfm[f"{col}_score"] = pd.qcut(
            rfm[col].rank(method="first", ascending=ascending),
            q=5,
            labels=[5, 4, 3, 2, 1] if ascending else [1, 2, 3, 4, 5],
        ).astype(int)
    rfm["rfm_score"] = rfm[["recency_score", "frequency_score", "monetary_score"]].sum(axis=1)
    rfm["segment"] = pd.cut(
        rfm["rfm_score"],
        bins=[0, 6, 9, 12, 15],
        labels=["At Risk", "Needs Attention", "Loyal", "Champions"],
        include_lowest=True,
    )
    return rfm.reset_index()


def cohort_retention(datasets: dict[str, pd.DataFrame]) -> pd.DataFrame:
    df = _orders_items(datasets)
    customer_first = df.groupby("customer_id")["order_date"].min().dt.to_period("M").rename("cohort")
    cohort_df = df[["customer_id", "order_date"]].drop_duplicates().merge(customer_first, on="customer_id")
    cohort_df["order_period"] = cohort_df["order_date"].dt.to_period("M")
    cohort_df["period_number"] = (cohort_df["order_period"] - cohort_df["cohort"]).apply(lambda value: value.n)
    matrix = cohort_df.groupby(["cohort", "period_number"])["customer_id"].nunique().unstack(fill_value=0)
    return matrix.divide(matrix.iloc[:, 0].replace(0, 1), axis=0).round(4)


def inventory_analysis(datasets: dict[str, pd.DataFrame]) -> pd.DataFrame:
    inventory = datasets["inventory"].copy()
    inventory["daily_demand"] = inventory["quantity_sold_365d"] / 365
    inventory["stockout_risk"] = inventory["current_stock"] <= inventory["reorder_point"]
    inventory["recommended_order_qty"] = (inventory["reorder_point"] + inventory["safety_stock"] - inventory["current_stock"]).clip(lower=0).round(0)
    return inventory.sort_values(["stockout_risk", "recommended_order_qty"], ascending=[False, False])


def abc_analysis(datasets: dict[str, pd.DataFrame]) -> pd.DataFrame:
    df = _orders_items(datasets)
    product_revenue = df.groupby("product_id")["line_total"].sum().sort_values(ascending=False).reset_index()
    product_revenue["revenue_pct"] = product_revenue["line_total"] / product_revenue["line_total"].sum()
    product_revenue["cum_pct"] = product_revenue["revenue_pct"].cumsum()
    product_revenue["abc_class"] = pd.cut(
        product_revenue["cum_pct"],
        bins=[0, 0.8, 0.95, 1.0],
        labels=["A", "B", "C"],
        include_lowest=True,
    )
    return product_revenue


def market_basket_analysis(datasets: dict[str, pd.DataFrame]) -> pd.DataFrame:
    items = datasets["order_items"].copy()
    transactions = items.groupby("order_id")["product_id"].apply(lambda value: sorted(set(value)))
    pair_counts: dict[tuple[str, str], int] = {}
    product_counts = items.groupby("product_id")["order_id"].nunique().to_dict()
    order_count = max(items["order_id"].nunique(), 1)
    for products in transactions:
        for pair in combinations(products, 2):
            pair_counts[pair] = pair_counts.get(pair, 0) + 1
    rows = []
    for (left, right), count in pair_counts.items():
        support = count / order_count
        confidence = count / max(product_counts.get(left, 1), 1)
        lift = confidence / max(product_counts.get(right, 1) / order_count, 0.0001)
        rows.append({"antecedent": left, "consequent": right, "support": support, "confidence": confidence, "lift": lift})
    return pd.DataFrame(rows).sort_values("lift", ascending=False).head(25) if rows else pd.DataFrame()


def time_series_analysis(datasets: dict[str, pd.DataFrame]) -> pd.DataFrame:
    df = _orders_items(datasets)
    daily = df.set_index("order_date").resample("D")["line_total"].sum().rename("daily_revenue").to_frame()
    daily["rolling_7d"] = daily["daily_revenue"].rolling(7, min_periods=1).mean()
    daily["baseline_forecast"] = daily["rolling_7d"].shift(1).fillna(daily["daily_revenue"].mean())
    return daily.reset_index()

