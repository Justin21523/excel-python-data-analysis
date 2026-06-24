from __future__ import annotations

from pathlib import Path

from scripts.run_e2e_demo import run_e2e_demo


ROOT = Path(__file__).resolve().parents[2]


def test_dashboard_demo_flow_generates_artifacts():
    run_e2e_demo(port=8512, record=False, update_assets=False)

    report = ROOT / "artifacts" / "playwright" / "demo_report.html"
    screenshots = sorted((ROOT / "artifacts" / "playwright" / "screenshots").glob("demo_*.png"))

    assert report.exists()
    assert report.stat().st_size > 0
    assert len(screenshots) >= 6
    assert all(path.stat().st_size > 0 for path in screenshots)
