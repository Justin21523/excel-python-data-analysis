from __future__ import annotations

import sys
from pathlib import Path

import pandas as pd
import streamlit as st

ROOT = Path(__file__).resolve().parents[2]
if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))

from app.ui.components import guided_demo_panel, insight_grid, page_header, process_nav, section_label, sidebar_brand
from app.ui.theme import load_theme
from excel_analysis.reporting import OpenpyxlFeatureShowcase


st.set_page_config(page_title="Openpyxl Showcase", layout="wide")
load_theme()
sidebar_brand("Openpyxl Showcase")

page_header(
    "Automation showcase",
    "Openpyxl Feature Showcase",
    "Generate a workbook that demonstrates formulas, named styles, comments, hyperlinks, validation, protection, formatting, and charts.",
)
process_nav("report")
guided_demo_panel("showcase")

features = [
    ("Formula demo", "SUM, AVERAGE, MAX, MIN, IF"),
    ("Named styles", "Reusable title/header/currency styles"),
    ("Comments and links", "Cell comments and internal/external hyperlinks"),
    ("Data validation", "List, whole number, decimal, and date validation"),
    ("Protection", "Protected worksheet with unlocked input cells"),
    ("Conditional formatting", "Color scales, data bars, and threshold rules"),
    ("Charts", "Bar, line, and pie charts"),
]
insight_grid(
    [
        ("Workbook sections", f"{len(features)}", "Dedicated demo areas"),
        ("Engine", "openpyxl", "Pure Python workbook automation"),
        ("Output", ".xlsx", "Formatted portfolio artifact"),
        ("Use case", "Showcase", "Excel automation capability map"),
    ]
)

section_label("Feature coverage")
st.dataframe(pd.DataFrame(features, columns=["feature", "coverage"]), width="stretch", hide_index=True)

output = Path("reports/openpyxl_feature_showcase.xlsx")
if st.button("Generate showcase workbook", type="primary"):
    artifact = OpenpyxlFeatureShowcase().build(output)
    st.session_state.showcase_artifact = artifact.path
    st.session_state.demo_step = "showcase"
    st.success(f"Showcase workbook exported: {artifact.path}")

artifact_path = st.session_state.get("showcase_artifact", output if output.exists() else None)
if artifact_path:
    artifact_path = Path(artifact_path)
    st.download_button(
        "Download openpyxl showcase",
        data=artifact_path.read_bytes(),
        file_name=artifact_path.name,
        mime="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet",
    )
