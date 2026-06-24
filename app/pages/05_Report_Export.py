from __future__ import annotations

import sys
from pathlib import Path

import streamlit as st

ROOT = Path(__file__).resolve().parents[2]
if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))

from app.ui.components import dataset_status_bar, file_download, guided_demo_panel, insight_grid, next_action, page_header, process_nav, section_label, sidebar_brand
from app.ui.state import ensure_default_dataset, run_analysis
from app.ui.theme import load_theme


st.set_page_config(page_title="Report Export", layout="wide")
load_theme()
sidebar_brand("Report Export")
ensure_default_dataset()

page_header(
    "Step 5",
    "Visualization & Report Export",
    "Export portfolio-ready Excel reports with summary sheets, analytics tables, data quality details, and formatted workbook styling.",
)
process_nav("report")
dataset_status_bar()
guided_demo_panel("report")

if st.button("Generate Excel analysis report", type="primary"):
    run_analysis()
    st.success("Report generated.")

artifact = st.session_state.get("report_artifact")
result = st.session_state.get("analysis_result")
if artifact is None or result is None:
    next_action("Next action: generate report", "Create a formatted Excel workbook with summary, analytics, quality checks, and raw sample sheets.", "Click Generate Excel analysis report")
    st.stop()

profiles = result.profiles
analytics = result.analytics
quality = sum(profile.quality_score for profile in profiles.values()) / max(len(profiles), 1)
insight_grid(
    [
        ("Report file", artifact.path.name, artifact.kind),
        ("Workbook sheets", f"{len(profiles)}+", "Summary, sales, customer, quality, raw sample"),
        ("Quality score", f"{quality:.1f}", "Average profiled score"),
        ("Analytics blocks", f"{len(analytics)}", "Structured result objects"),
    ]
)

section_label("Download")
file_download(artifact.path, "Download Excel report", "application/vnd.openxmlformats-officedocument.spreadsheetml.sheet")
st.caption(str(artifact.path))

section_label("Included analysis modules")
st.dataframe(
    [{"module": name, "result_type": type(value).__name__} for name, value in analytics.items()],
    width="stretch",
    hide_index=True,
)
