from __future__ import annotations

from html import escape
from pathlib import Path
from typing import Iterable

import pandas as pd
import streamlit as st

from app.ui.state import DEMO_STEPS, current_dataset_summary, current_demo_step, has_retail_schema


PROCESS_STEPS = [
    ("upload", "Upload"),
    ("profile", "Profile"),
    ("clean", "Clean"),
    ("analyze", "Analyze"),
    ("report", "Report"),
]


def page_header(eyebrow: str, title: str, subtitle: str) -> None:
    st.markdown(
        f"""
        <div class="platform-header">
          <div class="platform-eyebrow">{escape(eyebrow)}</div>
          <h1>{escape(title)}</h1>
          <p class="platform-subtitle">{escape(subtitle)}</p>
        </div>
        """,
        unsafe_allow_html=True,
    )


def sidebar_brand(active_page: str) -> None:
    with st.sidebar:
        st.markdown(
            "<div class='sidebar-brand'>"
            "<div class='sidebar-title'>Excel Analytics Platform</div>"
            "<div class='sidebar-subtitle'>Python + pandas + openpyxl</div>"
            "</div>",
            unsafe_allow_html=True,
        )
        st.caption(f"Current page: {active_page}")


def process_nav(active: str) -> None:
    completed = {
        "upload": "input_path" in st.session_state,
        "profile": bool(st.session_state.get("profiles")),
        "clean": st.session_state.get("cleaned_datasets") is not None,
        "analyze": st.session_state.get("analysis_result") is not None,
        "report": st.session_state.get("report_artifact") is not None,
    }
    blocks = []
    for key, label in PROCESS_STEPS:
        state = "active" if key == active else "done" if completed[key] else ""
        status = "Active" if key == active else "Done" if completed[key] else "Pending"
        blocks.append(
            f"<div class='process-step {state}'>"
            f"<span class='process-status'>{status}</span>"
            f"<div class='process-title'>{escape(label)}</div>"
            "</div>"
        )
    st.markdown(f"<div class='process-rail'>{''.join(blocks)}</div>", unsafe_allow_html=True)


def dataset_status_bar() -> None:
    summary = current_dataset_summary()
    schema = "Retail analytics ready" if has_retail_schema() else "Profiling only"
    items = [
        ("Workbook", str(summary["workbook"]), str(summary["path"])),
        ("Sheets", f"{summary['sheets']}", "Loaded datasets"),
        ("Rows", f"{summary['rows']:,}", "Total visible records"),
        ("Quality", f"{summary['quality']:.1f}", "Average profile score"),
        ("Run status", str(summary["status"]), schema),
    ]
    html = "".join(
        f"<div class='status-item'><div class='status-label'>{escape(label)}</div>"
        f"<div class='status-value'>{escape(value)}</div><div class='status-note'>{escape(note)}</div></div>"
        for label, value, note in items
    )
    st.markdown(f"<div class='dataset-status-bar'>{html}</div>", unsafe_allow_html=True)


def guided_demo_panel(page_step: str) -> None:
    if not st.session_state.get("demo_mode"):
        return
    idx, active_key, title, body = current_demo_step()
    blocks = []
    for step_idx, (key, label, _) in enumerate(DEMO_STEPS, 1):
        state = "active" if key == active_key else "done" if step_idx < idx else ""
        blocks.append(f"<div class='guided-step {state}'>{step_idx}. {escape(label)}</div>")
    page_hint = "You are on the right page." if page_step == active_key else f"Current guided step: {escape(title)}"
    st.markdown(
        "<div class='guided-demo'>"
        "<div class='guided-title'>Guided demo mode</div>"
        f"<div class='guided-body'>Step {idx} of {len(DEMO_STEPS)}: <strong>{escape(title)}</strong>. {escape(body)}</div>"
        f"<div class='guided-hint'>{page_hint}</div>"
        f"<div class='guided-steps'>{''.join(blocks)}</div>"
        "</div>",
        unsafe_allow_html=True,
    )


def next_action(title: str, body: str, action_label: str | None = None) -> None:
    action = f"<div class='next-action-command'>{escape(action_label)}</div>" if action_label else ""
    st.markdown(
        f"<div class='next-action'><div class='next-action-title'>{escape(title)}</div>"
        f"<div class='next-action-body'>{escape(body)}</div>{action}</div>",
        unsafe_allow_html=True,
    )


def section_label(text: str) -> None:
    st.markdown(f"<div class='section-label'>{escape(text)}</div>", unsafe_allow_html=True)


def insight_card(label: str, value: str, note: str = "") -> None:
    st.markdown(
        f"<div class='insight-card'>"
        f"<div class='insight-label'>{escape(label)}</div>"
        f"<div class='insight-value'>{escape(value)}</div>"
        f"<div class='insight-note'>{escape(note)}</div>"
        "</div>",
        unsafe_allow_html=True,
    )


def insight_grid(items: Iterable[tuple[str, str, str]], columns: int = 4) -> None:
    cols = st.columns(columns)
    for idx, item in enumerate(items):
        with cols[idx % columns]:
            insight_card(*item)


def status_badge(text: str, level: str = "info") -> None:
    cls = {"info": "status-badge", "warning": "warning-badge", "danger": "danger-badge"}.get(level, "status-badge")
    st.markdown(f"<span class='{cls}'>{escape(text)}</span>", unsafe_allow_html=True)


def callout(text: str) -> None:
    st.markdown(f"<div class='callout'>{escape(text)}</div>", unsafe_allow_html=True)


def dataset_profile_table(profiles: dict[str, dict]) -> pd.DataFrame:
    return pd.DataFrame(
        [
            {
                "dataset": name,
                "rows": data["rows"],
                "columns": data["columns"],
                "quality_score": data["quality_score"],
                "issues": len(data["issues"]),
                "duplicated_rows": data["duplicated_rows"],
            }
            for name, data in profiles.items()
        ]
    )


def issue_table(profiles: dict[str, dict]) -> pd.DataFrame:
    rows = []
    for profile in profiles.values():
        rows.extend(profile.get("issues", []))
    return pd.DataFrame(rows)


def file_download(path: Path, label: str, mime: str) -> None:
    st.download_button(label, data=path.read_bytes(), file_name=path.name, mime=mime)
