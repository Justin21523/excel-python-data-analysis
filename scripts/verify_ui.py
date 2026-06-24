from __future__ import annotations

import argparse
import subprocess
import sys
import time
from pathlib import Path

from playwright.sync_api import sync_playwright


ROOT = Path(__file__).resolve().parents[1]
SCREENSHOT_DIR = ROOT / "assets" / "screenshots"


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


def capture_screenshots(base_url: str, update_screenshots: bool) -> None:
    SCREENSHOT_DIR.mkdir(parents=True, exist_ok=True)
    with sync_playwright() as p:
        browser = p.chromium.launch(headless=True)

        def shot(url: str, file_name: str, wait_text: str, button: str | None = None, post_wait: str | None = None, width: int = 1440, height: int = 1000) -> None:
            page = browser.new_page(viewport={"width": width, "height": height}, device_scale_factor=1)
            page.goto(url, wait_until="domcontentloaded", timeout=60000)
            page.get_by_text(wait_text, exact=False).first.wait_for(timeout=60000)
            if button:
                page.get_by_role("button", name=button).click(timeout=60000)
                if post_wait:
                    page.get_by_text(post_wait, exact=False).first.wait_for(timeout=60000)
            page.wait_for_timeout(2500)
            text = page.locator("body").inner_text(timeout=10000)
            if "<div class=" in text or "<span class=" in text:
                raise AssertionError(f"Raw HTML leaked into UI text on {url}")
            if width <= 430:
                overflow = page.evaluate("document.documentElement.scrollWidth > document.documentElement.clientWidth + 2")
                if overflow:
                    raise AssertionError(f"Mobile horizontal overflow detected on {url}")
            if update_screenshots:
                page.screenshot(path=str(SCREENSHOT_DIR / file_name), full_page=True)
            page.close()

        shot(base_url, "home_dashboard.png", "Sample quick start")
        shot(f"{base_url}/Upload_Profile", "upload_profile.png", "Quality overview")
        shot(f"{base_url}/Business_Analytics", "business_analytics.png", "Business Analytics", button="Run analytics", post_wait="RFM segment summary")
        shot(f"{base_url}/Report_Export", "report_export.png", "Visualization & Report Export", button="Generate Excel analysis report", post_wait="Download")
        shot(base_url, "home_mobile.png", "Sample quick start", width=390, height=844)
        browser.close()


def assert_screenshots_exist() -> None:
    required = [
        "home_dashboard.png",
        "home_mobile.png",
        "upload_profile.png",
        "business_analytics.png",
        "report_export.png",
    ]
    missing = [name for name in required if not (SCREENSHOT_DIR / name).exists() or (SCREENSHOT_DIR / name).stat().st_size == 0]
    if missing:
        raise AssertionError(f"Missing or empty screenshots: {missing}")


def main() -> int:
    parser = argparse.ArgumentParser(description="Verify Streamlit UI with Playwright.")
    parser.add_argument("--port", type=int, default=8510)
    parser.add_argument("--update-screenshots", action="store_true")
    args = parser.parse_args()

    base_url = f"http://localhost:{args.port}"
    proc = subprocess.Popen(
        [
            sys.executable,
            "-m",
            "streamlit",
            "run",
            "app/streamlit_app.py",
            "--server.port",
            str(args.port),
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
        capture_screenshots(base_url, args.update_screenshots)
        assert_screenshots_exist()
        return 0
    finally:
        proc.terminate()
        try:
            proc.wait(timeout=10)
        except subprocess.TimeoutExpired:
            proc.kill()


if __name__ == "__main__":
    raise SystemExit(main())
