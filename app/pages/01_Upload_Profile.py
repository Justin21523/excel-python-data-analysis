from __future__ import annotations

import sys
from pathlib import Path

import pandas as pd
import streamlit as st

ROOT = Path(__file__).resolve().parents[2]
if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))

from app.ui.components import dataset_profile_table, dataset_status_bar, guided_demo_panel, issue_table, page_header, process_nav, section_label, sidebar_brand, status_badge
from app.ui.state import SAMPLE_OPTIONS, ensure_default_dataset, ensure_sample_workbooks, load_dataset, save_upload
from app.ui.theme import load_theme


st.set_page_config(page_title="Upload & Profile", layout="wide")
load_theme()
sidebar_brand("Upload & Profile")
ensure_sample_workbooks()
ensure_default_dataset()

page_header(
    "Step 1 and 2",
    "Upload & Data Profile",
    "Load Excel or CSV data, inspect every sheet, and surface quality issues before analysis.",
)
process_nav("profile")
dataset_status_bar()
guided_demo_panel("profile")

source_col, upload_col = st.columns([0.9, 1.1])
with source_col:
    section_label("Sample workbook")
    selected = st.selectbox("Select a sample business case", list(SAMPLE_OPTIONS), label_visibility="collapsed")
    if st.button("Load selected sample", type="primary"):
        load_dataset(SAMPLE_OPTIONS[selected])
        st.success(f"Loaded {SAMPLE_OPTIONS[selected]}")

with upload_col:
    section_label("Upload file")
    uploaded = st.file_uploader("Upload Excel or CSV", type=["xlsx", "csv"])
    if uploaded is not None and st.button("Load uploaded file"):
        path = save_upload(uploaded)
        load_dataset(path)
        st.success(f"Loaded {uploaded.name}")

profiles = st.session_state.get("profiles")
datasets = st.session_state.get("datasets")
if not profiles or not datasets:
    st.info("Load a workbook or CSV to begin.")
    st.stop()

section_label("Quality overview")
profile_df = dataset_profile_table(profiles)
st.dataframe(profile_df, width="stretch", hide_index=True)

issue_df = issue_table(profiles)
if issue_df.empty:
    status_badge("No major quality issues detected", "info")
else:
    severity = "danger" if (issue_df["severity"] == "high").any() else "warning"
    status_badge(f"{len(issue_df)} quality issues detected", severity)
    st.dataframe(issue_df, width="stretch", hide_index=True)

section_label("Sheet preview")
sheet = st.selectbox("Select sheet", list(datasets))
preview = datasets[sheet].head(50)
st.dataframe(preview, width="stretch")

with st.expander("Column type profile", expanded=False):
    profile = profiles[sheet]
    dtype_df = pd.DataFrame({"column": list(profile["dtypes"]), "dtype": list(profile["dtypes"].values())})
    st.dataframe(dtype_df, width="stretch", hide_index=True)
