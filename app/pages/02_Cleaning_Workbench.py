from __future__ import annotations

import sys
from pathlib import Path

import pandas as pd
import streamlit as st

ROOT = Path(__file__).resolve().parents[2]
if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))

from app.ui.components import dataset_status_bar, guided_demo_panel, insight_grid, next_action, page_header, process_nav, section_label, sidebar_brand
from app.ui.state import ensure_default_dataset, run_cleaning
from app.ui.theme import load_theme


st.set_page_config(page_title="Cleaning Workbench", layout="wide")
load_theme()
sidebar_brand("Cleaning Workbench")
ensure_default_dataset()

page_header(
    "Step 3",
    "Cleaning Workbench",
    "Apply reusable cleaning logic for whitespace, dates, numeric fields, duplicates, and export-ready datasets.",
)
process_nav("clean")
dataset_status_bar()
guided_demo_panel("clean")

datasets = st.session_state.datasets
before_rows = sum(len(df) for df in datasets.values())
before_missing = sum(int(df.isna().sum().sum()) for df in datasets.values())
before_dupes = sum(int(df.duplicated().sum()) for df in datasets.values())

if st.button("Run cleaning pipeline", type="primary"):
    artifact = run_cleaning()
    st.success(f"Cleaned workbook exported: {artifact}")

cleaned = st.session_state.get("cleaned_datasets")
if cleaned is None:
    next_action("Next action: run cleaning", "Apply the cleaning pipeline to compare raw and cleaned datasets, then download a cleaned workbook.", "Click Run cleaning pipeline")
    cleaned = datasets

after_rows = sum(len(df) for df in cleaned.values())
after_missing = sum(int(df.isna().sum().sum()) for df in cleaned.values())
after_dupes = sum(int(df.duplicated().sum()) for df in cleaned.values())
insight_grid(
    [
        ("Rows", f"{after_rows:,}", f"Before: {before_rows:,}"),
        ("Missing cells", f"{after_missing:,}", f"Before: {before_missing:,}"),
        ("Duplicate rows", f"{after_dupes:,}", f"Before: {before_dupes:,}"),
        ("Sheets cleaned", f"{len(cleaned)}", "Text, dates, numbers, duplicates"),
    ]
)

section_label("Before / after preview")
sheet = st.selectbox("Select sheet", list(datasets))
left, right = st.columns(2)
with left:
    st.caption("Before")
    st.dataframe(datasets[sheet].head(30), width="stretch")
with right:
    st.caption("After")
    st.dataframe(cleaned[sheet].head(30), width="stretch")

artifact = st.session_state.get("cleaned_artifact")
if artifact:
    st.download_button(
        "Download cleaned workbook",
        data=artifact.read_bytes(),
        file_name=artifact.name,
        mime="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet",
    )

with st.expander("Cleaning operations applied", expanded=False):
    st.dataframe(
        pd.DataFrame(
            [
                {"operation": "Normalize text", "scope": "string/category columns"},
                {"operation": "Convert dates", "scope": "columns containing date/time"},
                {"operation": "Convert numeric", "scope": "price, amount, total, cost, quantity, stock, discount"},
                {"operation": "Remove duplicates", "scope": "exact duplicate rows"},
            ]
        ),
        width="stretch",
        hide_index=True,
    )
