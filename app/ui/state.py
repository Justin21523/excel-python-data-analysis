from __future__ import annotations

import tempfile
from pathlib import Path
from typing import Any

import pandas as pd
import streamlit as st

from excel_analysis.data import create_all_sample_workbooks, create_retail_workbook
from excel_analysis.services import AnalysisPipeline


SAMPLE_OPTIONS = {
    "Retail analytics": Path("data/sample/retail_demo.xlsx"),
    "Messy sales": Path("data/sample/messy_sales.xlsx"),
    "Finance workbook": Path("data/sample/finance_workbook.xlsx"),
    "Inventory planning": Path("data/sample/inventory_planning.xlsx"),
    "Customer segmentation": Path("data/sample/customer_segmentation.xlsx"),
}

DEMO_STEPS = [
    ("load", "Load sample", "Load the Retail analytics workbook."),
    ("profile", "Profile data", "Review sheet profiles and quality issues."),
    ("clean", "Clean data", "Run the cleaning pipeline and compare before/after data."),
    ("analyze", "Analyze data", "Run analytics and use filters to inspect KPIs."),
    ("report", "Export report", "Generate the formatted Excel analysis report."),
    ("showcase", "Openpyxl showcase", "Generate the openpyxl feature showcase workbook."),
]


@st.cache_resource
def get_pipeline() -> AnalysisPipeline:
    return AnalysisPipeline()


def ensure_sample_workbooks() -> None:
    missing = [path for path in SAMPLE_OPTIONS.values() if not path.exists()]
    if missing:
        create_all_sample_workbooks("data/sample")


def ensure_default_dataset() -> Path:
    default_path = SAMPLE_OPTIONS["Retail analytics"]
    if not default_path.exists():
        create_retail_workbook(default_path)
    if "input_path" not in st.session_state:
        st.session_state.input_path = default_path
        load_dataset(default_path)
    return default_path


def start_guided_demo() -> None:
    ensure_sample_workbooks()
    load_dataset(SAMPLE_OPTIONS["Retail analytics"])
    st.session_state.demo_mode = True
    st.session_state.demo_step = "load"
    st.session_state.last_run_status = "Guided demo started"


def set_demo_step(step: str) -> None:
    st.session_state.demo_mode = True
    st.session_state.demo_step = step


def current_demo_step() -> tuple[int, str, str, str]:
    active = st.session_state.get("demo_step", "load")
    for idx, (key, title, body) in enumerate(DEMO_STEPS, 1):
        if key == active:
            return idx, key, title, body
    key, title, body = DEMO_STEPS[0]
    return 1, key, title, body


def save_upload(uploaded_file: Any) -> Path:
    suffix = Path(uploaded_file.name).suffix
    tmp = tempfile.NamedTemporaryFile(delete=False, suffix=suffix)
    tmp.write(uploaded_file.getbuffer())
    tmp.close()
    return Path(tmp.name)


def load_dataset(path: str | Path) -> None:
    pipeline = get_pipeline()
    input_path = Path(path)
    datasets = pipeline.load(input_path)
    profiles = pipeline.profile_only(input_path)
    st.session_state.input_path = input_path
    st.session_state.datasets = datasets
    st.session_state.profiles = profiles
    st.session_state.cleaned_datasets = None
    st.session_state.analysis_result = None
    st.session_state.report_artifact = None
    st.session_state.last_run_status = "Profiled"


def run_cleaning(output_path: str | Path = "data/processed/dashboard_cleaned.xlsx") -> Path:
    pipeline = get_pipeline()
    input_path = Path(st.session_state.input_path)
    cleaned = pipeline.cleaner.clean_retail_frames(st.session_state.datasets)
    artifact = pipeline.clean_export(input_path, output_path)
    st.session_state.cleaned_datasets = cleaned
    st.session_state.cleaned_artifact = artifact
    st.session_state.last_run_status = "Cleaned"
    set_demo_step("analyze")
    return artifact


def run_analysis(report_path: str | Path | None = None) -> None:
    pipeline = get_pipeline()
    input_path = Path(st.session_state.input_path)
    result = pipeline.run(input_path, "reports", report_path=report_path)
    st.session_state.analysis_result = result
    st.session_state.cleaned_datasets = result.cleaned_datasets
    st.session_state.report_artifact = result.artifacts[0] if result.artifacts else None
    st.session_state.last_run_status = "Analyzed and report-ready"
    set_demo_step("report")


def current_dataset_summary() -> dict[str, object]:
    input_path = Path(st.session_state.get("input_path", ""))
    datasets = st.session_state.get("datasets") or {}
    profiles = st.session_state.get("profiles") or {}
    rows = sum(len(df) for df in datasets.values()) if datasets else 0
    quality = 0.0
    if profiles:
        quality = sum(float(profile["quality_score"]) for profile in profiles.values()) / max(len(profiles), 1)
    return {
        "workbook": input_path.name if input_path.name else "No workbook loaded",
        "path": str(input_path) if input_path.name else "",
        "sheets": len(datasets),
        "rows": rows,
        "quality": quality,
        "status": st.session_state.get("last_run_status", "Ready"),
    }


def has_retail_schema(datasets: dict[str, pd.DataFrame] | None = None) -> bool:
    data = datasets if datasets is not None else st.session_state.get("datasets", {})
    return {"orders", "order_items", "customers", "products", "inventory"}.issubset(set(data))


def filtered_retail_datasets(
    datasets: dict[str, pd.DataFrame],
    date_range: tuple[pd.Timestamp, pd.Timestamp] | None = None,
    regions: list[str] | None = None,
    categories: list[str] | None = None,
    customer_segments: list[str] | None = None,
    rfm: pd.DataFrame | None = None,
) -> dict[str, pd.DataFrame]:
    filtered = {name: df.copy() for name, df in datasets.items()}
    orders = filtered["orders"].copy()
    products = filtered["products"].copy()
    items = filtered["order_items"].copy()
    customers = filtered["customers"].copy()

    orders["order_date"] = pd.to_datetime(orders["order_date"], errors="coerce")
    if date_range:
        start, end = date_range
        orders = orders[(orders["order_date"] >= start) & (orders["order_date"] <= end)]
    if regions:
        orders = orders[orders["region"].isin(regions)]
        customers = customers[customers["region"].isin(regions)] if "region" in customers else customers
    if categories:
        products = products[products["category"].astype(str).str.strip().isin(categories)]
        items = items[items["product_id"].isin(products["product_id"])]
    if customer_segments and rfm is not None and not rfm.empty:
        segment_customers = rfm[rfm["segment"].astype(str).isin(customer_segments)]["customer_id"]
        orders = orders[orders["customer_id"].isin(segment_customers)]
        customers = customers[customers["customer_id"].isin(segment_customers)]

    orders = orders[orders["customer_id"].isin(customers["customer_id"])]
    items = items[items["order_id"].isin(orders["order_id"])]
    products = products[products["product_id"].isin(items["product_id"].unique())]
    inventory = filtered["inventory"]
    if "product_id" in inventory:
        inventory = inventory[inventory["product_id"].isin(products["product_id"])]

    filtered.update({"orders": orders, "order_items": items, "customers": customers, "products": products, "inventory": inventory})
    return filtered
