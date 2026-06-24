from __future__ import annotations

import sys
from pathlib import Path

import pandas as pd
import streamlit as st

ROOT = Path(__file__).resolve().parents[2]
if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))

from app.ui import charts
from app.ui.components import dataset_status_bar, guided_demo_panel, insight_grid, next_action, page_header, process_nav, section_label, sidebar_brand
from app.ui.state import ensure_default_dataset, filtered_retail_datasets, get_pipeline, has_retail_schema, run_analysis
from app.ui.theme import load_theme


st.set_page_config(page_title="Business Analytics", layout="wide")
load_theme()
sidebar_brand("Business Analytics")
ensure_default_dataset()

page_header(
    "Step 4",
    "Business Analytics",
    "Executive KPIs and drill-down visuals for retail sales, customers, products, cohorts, inventory, and market basket rules.",
)
process_nav("analyze")
dataset_status_bar()
guided_demo_panel("analyze")

if not has_retail_schema():
    next_action(
        "Retail schema required",
        "Business Analytics needs orders, order_items, customers, products, and inventory sheets. Load the Retail analytics sample on the Upload page.",
        "Open Upload & Profile and select Retail analytics",
    )
    st.stop()

if st.button("Run analytics", type="primary"):
    run_analysis()
    st.success("Analytics completed.")

result = st.session_state.get("analysis_result")
if result is None:
    next_action(
        "Next action: run analytics",
        "Calculate KPIs, RFM segments, cohort retention, ABC inventory, and market basket rules from the loaded retail workbook.",
        "Click Run analytics",
    )
    st.stop()

section_label("Interactive filters")
datasets = result.cleaned_datasets
orders = datasets["orders"].copy()
orders["order_date"] = pd.to_datetime(orders["order_date"], errors="coerce")
products = datasets["products"].copy()
rfm_all = result.analytics["rfm"].copy()

min_date = orders["order_date"].min().date()
max_date = orders["order_date"].max().date()
regions = sorted(str(value) for value in orders["region"].dropna().unique())
categories = sorted(str(value).strip() for value in products["category"].dropna().unique())
segments = sorted(str(value) for value in rfm_all["segment"].dropna().unique())

filter_cols = st.columns([1.25, 1, 1, 1])
with filter_cols[0]:
    selected_dates = st.date_input("Date range", value=(min_date, max_date), min_value=min_date, max_value=max_date)
with filter_cols[1]:
    selected_regions = st.multiselect("Region", regions, default=regions)
with filter_cols[2]:
    selected_categories = st.multiselect("Category", categories, default=categories)
with filter_cols[3]:
    selected_segments = st.multiselect("RFM segment", segments, default=segments)

date_range = None
if isinstance(selected_dates, tuple) and len(selected_dates) == 2:
    date_range = (pd.Timestamp(selected_dates[0]), pd.Timestamp(selected_dates[1]) + pd.Timedelta(days=1) - pd.Timedelta(seconds=1))

filtered = filtered_retail_datasets(
    datasets,
    date_range=date_range,
    regions=selected_regions,
    categories=selected_categories,
    customer_segments=selected_segments,
    rfm=rfm_all,
)
if filtered["orders"].empty or filtered["order_items"].empty:
    next_action("No matching records", "Relax the date, region, category, or RFM filters to restore analytics results.", "Adjust filters")
    st.stop()

analytics = get_pipeline().run_analytics_for_datasets(filtered)
sales = analytics["sales"]
kpis = sales["kpis"]
insight_grid(
    [
        ("Revenue", f"${kpis['total_revenue']:,.0f}", "Delivered order revenue"),
        ("Orders", f"{kpis['order_count']:,}", "Unique delivered orders"),
        ("AOV", f"${kpis['average_order_value']:,.2f}", "Average order value"),
        ("Items sold", f"{kpis['items_sold']:,}", "Positive item quantity"),
    ]
)

section_label("Sales performance")
trend_col, region_col = st.columns([1.3, 0.9])
with trend_col:
    st.plotly_chart(charts.revenue_trend(analytics["time_series"]), width="stretch")
with region_col:
    st.plotly_chart(charts.ranked_bar(sales["revenue_by_region"], "region", "line_total", "Revenue by region"), width="stretch")

section_label("Customer and product intelligence")
left, right = st.columns(2)
with left:
    st.plotly_chart(charts.rfm_segments(analytics["rfm"]), width="stretch")
with right:
    st.plotly_chart(charts.abc_mix(analytics["abc"]), width="stretch")

rfm = analytics["rfm"]
segment_summary = (
    rfm.groupby("segment", observed=False)
    .agg(
        customers=("customer_id", "nunique"),
        avg_recency=("recency", "mean"),
        avg_frequency=("frequency", "mean"),
        revenue=("monetary", "sum"),
    )
    .reset_index()
)
segment_summary["revenue_share"] = segment_summary["revenue"] / max(segment_summary["revenue"].sum(), 1)
section_label("RFM segment summary")
st.dataframe(segment_summary, width="stretch", hide_index=True)

section_label("Retention and market basket")
left, right = st.columns([1.15, 0.85])
with left:
    cohort = analytics["cohort"]
    st.plotly_chart(charts.cohort_heatmap(cohort), width="stretch")
    st.plotly_chart(charts.cohort_size_bar(cohort), width="stretch")
with right:
    rules = analytics["market_basket"]
    if rules.empty:
        next_action("No market basket rules", "The current filter selection has too few product combinations to calculate association rules.", "Relax filters")
    else:
        min_support = st.slider("Minimum support", 0.0, 0.5, 0.01, 0.01)
        min_confidence = st.slider("Minimum confidence", 0.0, 1.0, 0.05, 0.05)
        min_lift = st.slider("Minimum lift", 0.0, 10.0, 1.0, 0.1)
        filtered_rules = rules[
            (rules["support"] >= min_support)
            & (rules["confidence"] >= min_confidence)
            & (rules["lift"] >= min_lift)
        ]
        if filtered_rules.empty:
            st.info("No association rules match the current thresholds.")
        else:
            st.dataframe(filtered_rules.head(12), width="stretch", hide_index=True)
        st.caption("Top product associations ranked by lift.")

section_label("Top products")
st.dataframe(sales["top_products"], width="stretch", hide_index=True)
