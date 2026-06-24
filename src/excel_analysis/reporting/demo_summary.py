from __future__ import annotations

from pathlib import Path

import pandas as pd

from excel_analysis.schemas import AnalysisResult


def build_demo_summary(
    result: AnalysisResult,
    output_path: str | Path = "reports/demo_summary.html",
    screenshots_dir: str | Path = "assets/screenshots",
    extra_artifacts: list[Path] | None = None,
) -> Path:
    output = Path(output_path)
    output.parent.mkdir(parents=True, exist_ok=True)
    screenshots = sorted(Path(screenshots_dir).glob("*.png"))
    sales = result.analytics["sales"]["kpis"]
    profiles = result.profiles
    quality = sum(profile.quality_score for profile in profiles.values()) / max(len(profiles), 1)
    profile_rows = "".join(
        f"<tr><td>{name}</td><td>{profile.rows:,}</td><td>{profile.columns}</td><td>{profile.quality_score:.1f}</td></tr>"
        for name, profile in profiles.items()
    )
    screenshot_cards = "".join(
        f"<figure><img src='../{shot.as_posix()}' alt='{shot.stem}'><figcaption>{shot.stem}</figcaption></figure>"
        for shot in screenshots
    )
    artifacts = list(result.artifacts)
    for path in extra_artifacts or []:
        artifacts.append(type("Artifact", (), {"path": path, "kind": path.suffix.lstrip("."), "description": path.name})())
    artifact_rows = "".join(f"<li><code>{artifact.path}</code> - {artifact.description}</li>" for artifact in artifacts)
    output.write_text(
        f"""<!doctype html>
<html lang="en">
<head>
  <meta charset="utf-8">
  <title>Excel Python Analytics Demo Summary</title>
  <style>
    body {{ font-family: Arial, sans-serif; margin: 32px; background: #f7f9fb; color: #1f2933; }}
    h1, h2 {{ color: #0a4c6a; }}
    .grid {{ display: grid; grid-template-columns: repeat(4, 1fr); gap: 12px; }}
    .card, figure {{ background: #fff; border: 1px solid #d8dee6; border-radius: 8px; padding: 16px; }}
    .value {{ font-size: 26px; font-weight: 800; color: #0a4c6a; }}
    table {{ border-collapse: collapse; width: 100%; background: #fff; }}
    th, td {{ border: 1px solid #d8dee6; padding: 8px 10px; text-align: left; }}
    img {{ max-width: 100%; border: 1px solid #d8dee6; border-radius: 6px; }}
  </style>
</head>
<body>
  <h1>Excel Python Analytics Demo Summary</h1>
  <p>Static snapshot for reviewers who want to inspect the outcome without launching Streamlit.</p>
  <div class="grid">
    <div class="card"><div>Total revenue</div><div class="value">${sales['total_revenue']:,.0f}</div></div>
    <div class="card"><div>Orders</div><div class="value">{sales['order_count']:,}</div></div>
    <div class="card"><div>AOV</div><div class="value">${sales['average_order_value']:,.2f}</div></div>
    <div class="card"><div>Quality score</div><div class="value">{quality:.1f}</div></div>
  </div>
  <h2>Dataset Profile</h2>
  <table><thead><tr><th>Dataset</th><th>Rows</th><th>Columns</th><th>Quality score</th></tr></thead><tbody>{profile_rows}</tbody></table>
  <h2>Generated Artifacts</h2>
  <ul>{artifact_rows}</ul>
  <h2>Dashboard Screenshots</h2>
  <div class="grid">{screenshot_cards}</div>
</body>
</html>
""",
        encoding="utf-8",
    )
    return output
