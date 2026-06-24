from __future__ import annotations

from pathlib import Path

import plotly.io as pio
import streamlit as st


STYLE_PATH = Path(__file__).resolve().parents[1] / "styles" / "dashboard.css"

COLORWAY = ["#1696D2", "#FDBF11", "#EC008B", "#55B748", "#DB2B27", "#5C5859"]


def load_theme() -> None:
    css = STYLE_PATH.read_text(encoding="utf-8")
    st.markdown(f"<style>{css}</style>", unsafe_allow_html=True)
    pio.templates["excel_light"] = {
        "layout": {
            "font": {"family": "Lato, Arial, sans-serif", "color": "#1F2933", "size": 14},
            "paper_bgcolor": "#FFFFFF",
            "plot_bgcolor": "#FFFFFF",
            "colorway": COLORWAY,
            "margin": {"l": 48, "r": 24, "t": 52, "b": 48},
            "xaxis": {"gridcolor": "#E7EBF0", "zerolinecolor": "#D8DEE6", "title": {"font": {"size": 13}}},
            "yaxis": {"gridcolor": "#E7EBF0", "zerolinecolor": "#D8DEE6", "title": {"font": {"size": 13}}},
            "legend": {"orientation": "h", "y": -0.22},
        }
    }
    pio.templates.default = "excel_light"
