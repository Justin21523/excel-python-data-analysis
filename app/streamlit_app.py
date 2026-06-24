from __future__ import annotations

import sys
from pathlib import Path

import streamlit as st

ROOT = Path(__file__).resolve().parents[1]
if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))

from app.ui.components import callout, dataset_status_bar, guided_demo_panel, insight_grid, page_header, process_nav, section_label, sidebar_brand
from app.ui.state import SAMPLE_OPTIONS, ensure_default_dataset, ensure_sample_workbooks, load_dataset, run_analysis, start_guided_demo
from app.ui.theme import load_theme


st.set_page_config(page_title="Excel Python Analytics Platform", layout="wide")
load_theme()
sidebar_brand("Home")
ensure_sample_workbooks()
ensure_default_dataset()

page_header(
    "Portfolio analytics system",
    "Excel Python Data Analysis Platform",
    "A light-mode analytics platform for profiling Excel/CSV data, cleaning messy business workbooks, running pandas analysis, and exporting openpyxl reports.",
)
process_nav("upload")
dataset_status_bar()
guided_demo_panel("load")

section_label("Executive summary")
profiles = st.session_state.get("profiles", {})
datasets = st.session_state.get("datasets", {})
total_rows = sum(profile["rows"] for profile in profiles.values()) if profiles else 0
avg_quality = sum(profile["quality_score"] for profile in profiles.values()) / max(len(profiles), 1) if profiles else 0
insight_grid(
    [
        ("Loaded sheets", f"{len(datasets)}", "Multi-sheet Excel workflow"),
        ("Profiled rows", f"{total_rows:,}", "Across currently selected workbook"),
        ("Average quality", f"{avg_quality:.1f}", "0-100 data quality score"),
        ("Analysis modules", "8", "Sales, RFM, cohort, ABC, basket, inventory"),
    ]
)

left, right = st.columns([1.15, 0.85])
with left:
    section_label("Workflow")
    callout("Use the pages in the sidebar to move from upload and profiling to cleaning, analysis, report export, and openpyxl feature demonstration.")
    st.markdown(
        """
        The platform is designed around a repeatable business analytics workflow:

        1. Upload or select a sample workbook.
        2. Inspect schema, missing values, duplicates, and quality issues.
        3. Apply reusable cleaning rules and export cleaned data.
        4. Run retail analytics including sales, customer, RFM, cohort, inventory, ABC, market basket, and time series analysis.
        5. Export a formatted Excel report and an openpyxl feature showcase workbook.
        """
    )
with right:
    section_label("Guided demo")
    if st.button("Start guided demo", type="primary"):
        start_guided_demo()
        st.rerun()
    section_label("Sample quick start")
    sample = st.selectbox("Choose sample workbook", list(SAMPLE_OPTIONS), label_visibility="collapsed")
    if st.button("Load sample workbook"):
        load_dataset(SAMPLE_OPTIONS[sample])
        st.success(f"Loaded {SAMPLE_OPTIONS[sample]}")
    if st.button("Run sample analysis and report"):
        load_dataset(SAMPLE_OPTIONS["Retail analytics"])
        run_analysis()
        st.success("Sample analysis completed. Open Business Analytics or Report Export for details.")
    st.caption("Default sample: data/sample/retail_demo.xlsx")
