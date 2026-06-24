from __future__ import annotations

import argparse
import shutil
import subprocess
import sys
import time
from pathlib import Path

from playwright.sync_api import Page, sync_playwright


ROOT = Path(__file__).resolve().parents[1]
ARTIFACT_DIR = ROOT / "artifacts" / "playwright"
ASSET_DEMO_DIR = ROOT / "assets" / "demo"


def wait_for_server(url: str, timeout: int = 45) -> None:
    deadline = time.time() + timeout
    with sync_playwright() as p:
        browser = p.chromium.launch(headless=True)
        page = browser.new_page()
        while time.time() < deadline:
            try:
                page.goto(url, wait_until="domcontentloaded", timeout=5000)
                browser.close()
                return
            except Exception:
                time.sleep(1)
        browser.close()
    raise RuntimeError(f"Streamlit server did not become ready: {url}")


def _safe_click(page: Page, button_name: str) -> None:
    page.get_by_role("button", name=button_name).click(timeout=60000)
    page.wait_for_timeout(1200)


def _shot(page: Page, name: str, update_assets: bool) -> None:
    ARTIFACT_DIR.joinpath("screenshots").mkdir(parents=True, exist_ok=True)
    path = ARTIFACT_DIR / "screenshots" / name
    page.screenshot(path=str(path), full_page=True)
    if update_assets:
        target = ROOT / "assets" / "screenshots" / name
        target.parent.mkdir(parents=True, exist_ok=True)
        shutil.copy2(path, target)


def _assert_no_raw_html(page: Page) -> None:
    text = page.locator("body").inner_text(timeout=10000)
    if "<div class=" in text or "<span class=" in text:
        raise AssertionError("Raw HTML leaked into Streamlit UI text.")


def _run_story(base_url: str, update_assets: bool, record: bool) -> Path | None:
    ARTIFACT_DIR.mkdir(parents=True, exist_ok=True)
    ASSET_DEMO_DIR.mkdir(parents=True, exist_ok=True)
    video_dir = ARTIFACT_DIR / "videos"
    trace_dir = ARTIFACT_DIR / "traces"
    trace_dir.mkdir(parents=True, exist_ok=True)
    context_kwargs = {
        "viewport": {"width": 1440, "height": 1000},
        "device_scale_factor": 1,
    }
    if record:
        video_dir.mkdir(parents=True, exist_ok=True)
        context_kwargs["record_video_dir"] = str(video_dir)
        context_kwargs["record_video_size"] = {"width": 1440, "height": 1000}

    with sync_playwright() as p:
        browser = p.chromium.launch(headless=True)
        context = browser.new_context(**context_kwargs)
        if record:
            context.tracing.start(screenshots=True, snapshots=True, sources=True)
        page = context.new_page()

        page.goto(base_url, wait_until="domcontentloaded", timeout=60000)
        page.get_by_text("Sample quick start", exact=False).first.wait_for(timeout=60000)
        _safe_click(page, "Start guided demo")
        page.get_by_text("Guided demo mode", exact=False).first.wait_for(timeout=60000)
        _shot(page, "demo_01_home_guided.png", update_assets)

        page.goto(f"{base_url}/Upload_Profile", wait_until="domcontentloaded", timeout=60000)
        page.get_by_text("Quality overview", exact=False).first.wait_for(timeout=60000)
        page.get_by_text("Sheet preview", exact=False).first.wait_for(timeout=60000)
        _shot(page, "demo_02_upload_profile.png", update_assets)

        page.goto(f"{base_url}/Cleaning_Workbench", wait_until="domcontentloaded", timeout=60000)
        page.get_by_text("Cleaning Workbench", exact=False).first.wait_for(timeout=60000)
        _safe_click(page, "Run cleaning pipeline")
        page.get_by_text("Cleaned workbook exported", exact=False).first.wait_for(timeout=60000)
        page.get_by_role("button", name="Download cleaned workbook").wait_for(timeout=60000)
        _shot(page, "demo_03_cleaning.png", update_assets)

        page.goto(f"{base_url}/Business_Analytics", wait_until="domcontentloaded", timeout=60000)
        page.get_by_text("Business Analytics", exact=False).first.wait_for(timeout=60000)
        _safe_click(page, "Run analytics")
        page.get_by_text("RFM segment summary", exact=False).first.wait_for(timeout=60000)
        page.get_by_text("Minimum support", exact=False).first.wait_for(timeout=60000)
        page.get_by_text("Region", exact=True).first.wait_for(timeout=60000)
        _shot(page, "demo_04_business_analytics.png", update_assets)

        page.goto(f"{base_url}/Report_Export", wait_until="domcontentloaded", timeout=60000)
        page.get_by_text("Visualization & Report Export", exact=False).first.wait_for(timeout=60000)
        _safe_click(page, "Generate Excel analysis report")
        page.get_by_role("button", name="Download Excel report").wait_for(timeout=60000)
        _shot(page, "demo_05_report_export.png", update_assets)

        page.goto(f"{base_url}/Openpyxl_Showcase", wait_until="domcontentloaded", timeout=60000)
        page.get_by_text("Openpyxl Feature Showcase", exact=False).first.wait_for(timeout=60000)
        _safe_click(page, "Generate showcase workbook")
        page.get_by_role("button", name="Download openpyxl showcase").wait_for(timeout=60000)
        _shot(page, "demo_06_openpyxl_showcase.png", update_assets)

        _assert_no_raw_html(page)
        video = page.video if record and page.video else None
        if record:
            context.tracing.stop(path=str(trace_dir / "dashboard_demo_trace.zip"))
        context.close()
        browser.close()
        return Path(video.path()) if video else None


def _convert_media(video_path: Path | None) -> None:
    if not video_path or not video_path.exists():
        return
    ffmpeg = shutil.which("ffmpeg")
    if not ffmpeg:
        print(f"ffmpeg not found; raw webm kept at {video_path}")
        return
    mp4 = ASSET_DEMO_DIR / "demo_walkthrough.mp4"
    gif = ASSET_DEMO_DIR / "demo_steps.gif"
    subprocess.run([ffmpeg, "-y", "-i", str(video_path), "-vf", "fps=12,scale=1280:-2", "-movflags", "+faststart", str(mp4)], check=True)
    subprocess.run([ffmpeg, "-y", "-i", str(mp4), "-t", "18", "-vf", "fps=8,scale=900:-1", str(gif)], check=True)


def _write_html_report() -> None:
    report = ARTIFACT_DIR / "demo_report.html"
    screenshots = sorted((ARTIFACT_DIR / "screenshots").glob("demo_*.png"))
    cards = "\n".join(f"<figure><img src='screenshots/{path.name}'><figcaption>{path.stem}</figcaption></figure>" for path in screenshots)
    report.write_text(
        f"""<!doctype html>
<html lang="en">
<head><meta charset="utf-8"><title>Excel Analytics Demo E2E Report</title>
<style>body{{font-family:Arial,sans-serif;margin:32px;background:#f7f9fb;color:#1f2933}}img{{max-width:100%;border:1px solid #d8dee6;border-radius:8px}}figure{{background:#fff;padding:16px;border-radius:8px}}</style></head>
<body><h1>Excel Analytics Demo E2E Report</h1><p>Generated by scripts/run_e2e_demo.py.</p>{cards}</body></html>
""",
        encoding="utf-8",
    )


def run_e2e_demo(port: int, record: bool = True, update_assets: bool = True) -> None:
    base_url = f"http://127.0.0.1:{port}"
    proc = subprocess.Popen(
        [
            sys.executable,
            "-m",
            "streamlit",
            "run",
            "app/streamlit_app.py",
            "--server.port",
            str(port),
            "--server.address",
            "127.0.0.1",
            "--server.headless",
            "true",
        ],
        cwd=ROOT,
        stdout=subprocess.PIPE,
        stderr=subprocess.STDOUT,
        text=True,
    )
    try:
        wait_for_server(base_url)
        video = _run_story(base_url, update_assets=update_assets, record=record)
        if record:
            _convert_media(video)
        _write_html_report()
    finally:
        proc.terminate()
        try:
            proc.wait(timeout=10)
        except subprocess.TimeoutExpired:
            proc.kill()


def main() -> int:
    parser = argparse.ArgumentParser(description="Run the full portfolio demo flow with Playwright.")
    parser.add_argument("--port", type=int, default=8511)
    parser.add_argument("--record", action="store_true")
    parser.add_argument("--no-update-assets", action="store_true")
    args = parser.parse_args()
    run_e2e_demo(port=args.port, record=args.record, update_assets=not args.no_update_assets)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
