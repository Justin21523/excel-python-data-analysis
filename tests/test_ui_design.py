from __future__ import annotations

from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
CSS_PATH = ROOT / "app" / "styles" / "dashboard.css"


def _relative_luminance(hex_color: str) -> float:
    value = hex_color.lstrip("#")
    rgb = [int(value[idx : idx + 2], 16) / 255 for idx in (0, 2, 4)]
    linear = [channel / 12.92 if channel <= 0.04045 else ((channel + 0.055) / 1.055) ** 2.4 for channel in rgb]
    return 0.2126 * linear[0] + 0.7152 * linear[1] + 0.0722 * linear[2]


def _contrast_ratio(foreground: str, background: str) -> float:
    fg = _relative_luminance(foreground)
    bg = _relative_luminance(background)
    lighter, darker = max(fg, bg), min(fg, bg)
    return (lighter + 0.05) / (darker + 0.05)


def test_dashboard_css_contains_light_theme_tokens():
    css = CSS_PATH.read_text(encoding="utf-8").lower()

    for token in ["#f7f9fb", "#ffffff", "#1696d2", "#12719e", "#fdbf11", "#ec008b"]:
        assert token in css
    assert "lato, arial, sans-serif" in css
    assert "font-variant-numeric: tabular-nums" in css
    assert ".process-rail" in css
    assert ".insight-card" in css
    assert ".dataset-status-bar" in css
    assert ".sidebar-brand" in css


def test_primary_ui_contrast_meets_wcag_aa():
    assert _contrast_ratio("#1F2933", "#FFFFFF") >= 4.5
    assert _contrast_ratio("#5B6670", "#FFFFFF") >= 4.5
    assert _contrast_ratio("#FFFFFF", "#12719E") >= 4.5
    assert _contrast_ratio("#0A4C6A", "#F7F9FB") >= 4.5


def test_streamlit_multipage_structure_exists():
    pages = sorted((ROOT / "app" / "pages").glob("*.py"))
    page_names = [path.name for path in pages]

    assert "01_Upload_Profile.py" in page_names
    assert "02_Cleaning_Workbench.py" in page_names
    assert "03_Business_Analytics.py" in page_names
    assert "04_Openpyxl_Showcase.py" in page_names
    assert "05_Report_Export.py" in page_names
    assert (ROOT / "app" / "ui" / "components.py").exists()
    assert (ROOT / "app" / "ui" / "theme.py").exists()


def test_ui_verification_assets_and_readme_references_exist():
    screenshots = [
        "before_single_page.png",
        "home_dashboard.png",
        "home_mobile.png",
        "upload_profile.png",
        "business_analytics.png",
        "report_export.png",
        "demo_01_home_guided.png",
        "demo_02_upload_profile.png",
        "demo_03_cleaning.png",
        "demo_04_business_analytics.png",
        "demo_05_report_export.png",
        "demo_06_openpyxl_showcase.png",
    ]
    readme = (ROOT / "README.md").read_text(encoding="utf-8")

    assert (ROOT / "scripts" / "verify_ui.py").exists()
    for screenshot in screenshots:
        path = ROOT / "assets" / "screenshots" / screenshot
        assert path.exists()
        assert path.stat().st_size > 0
        assert f"assets/screenshots/{screenshot}" in readme


def test_sidebar_brand_and_dataset_status_are_wired():
    components = (ROOT / "app" / "ui" / "components.py").read_text(encoding="utf-8")
    home = (ROOT / "app" / "streamlit_app.py").read_text(encoding="utf-8")

    assert "Excel Analytics Platform" in components
    assert "dataset_status_bar" in components
    assert "sidebar_brand" in home


def test_demo_storyline_docs_and_media_exist():
    required_docs = [
        "DEMO.md",
        "docs/demo_script.md",
        "docs/case_study_excel_automation.md",
        "docs/case_study_business_analytics.md",
        "docs/case_study_data_quality_pipeline.md",
        "docs/case_study_dashboard_testing.md",
    ]
    for doc in required_docs:
        path = ROOT / doc
        assert path.exists()
        assert path.stat().st_size > 0

    for media in ["assets/demo/demo_walkthrough.mp4", "assets/demo/demo_steps.gif", "reports/demo_summary.html"]:
        path = ROOT / media
        assert path.exists()
        assert path.stat().st_size > 0


def test_readme_links_demo_and_case_studies():
    readme = (ROOT / "README.md").read_text(encoding="utf-8")
    for expected in [
        "DEMO.md",
        "docs/demo_script.md",
        "assets/demo/demo_walkthrough.mp4",
        "assets/demo/demo_steps.gif",
        "docs/case_study_excel_automation.md",
        "docs/case_study_dashboard_testing.md",
        "excel-analysis demo",
    ]:
        assert expected in readme
