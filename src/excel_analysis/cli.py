from __future__ import annotations

import argparse
import json
from pathlib import Path

from excel_analysis.data import (
    create_all_sample_workbooks,
    create_customer_segmentation_workbook,
    create_finance_workbook,
    create_inventory_planning_workbook,
    create_messy_sales_workbook,
    create_retail_workbook,
)
from excel_analysis.reporting import OpenpyxlFeatureShowcase
from excel_analysis.reporting import build_demo_summary
from excel_analysis.services import AnalysisPipeline


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description="Excel Python Data Analysis portfolio CLI")
    sub = parser.add_subparsers(dest="command", required=True)

    sample = sub.add_parser("generate-sample", help="Generate deterministic synthetic sample workbooks")
    sample.add_argument("--case", choices=["retail", "messy-sales", "finance", "inventory", "customer", "all"], default="retail")
    sample.add_argument("--output", default=None)
    sample.add_argument("--output-dir", default="data/sample")
    sample.add_argument("--seed", type=int, default=42)

    profile = sub.add_parser("profile", help="Profile an Excel or CSV file")
    profile.add_argument("--input", required=True)

    analyze = sub.add_parser("analyze", help="Run full analysis and export an Excel report")
    analyze.add_argument("--input", required=True)
    analyze.add_argument("--output-dir", default="reports")

    clean = sub.add_parser("clean", help="Clean an Excel or CSV file and export cleaned sheets")
    clean.add_argument("--input", required=True)
    clean.add_argument("--output", default="data/processed/cleaned.xlsx")

    export = sub.add_parser("export-report", help="Run full analytics and export report to an explicit path")
    export.add_argument("--input", required=True)
    export.add_argument("--output", default="reports/portfolio_excel_analysis_report.xlsx")

    showcase = sub.add_parser("showcase-openpyxl", help="Generate standalone openpyxl feature showcase workbook")
    showcase.add_argument("--output", default="reports/openpyxl_feature_showcase.xlsx")

    demo = sub.add_parser("demo", help="Generate all portfolio demo artifacts")
    demo.add_argument("--sample-dir", default="data/sample")
    demo.add_argument("--reports-dir", default="reports")

    args = parser.parse_args(argv)

    if args.command == "generate-sample":
        paths = _generate_sample(args.case, args.output, args.output_dir, args.seed)
        for path in paths:
            print(f"Generated sample workbook: {path}")
        return 0

    pipeline = AnalysisPipeline()
    if args.command == "profile":
        print(json.dumps(pipeline.profile_only(args.input), indent=2, default=str))
        return 0

    if args.command == "analyze":
        result = pipeline.run(args.input, args.output_dir)
        for artifact in result.artifacts:
            print(f"Created {artifact.kind} report: {artifact.path}")
        return 0

    if args.command == "clean":
        path = pipeline.clean_export(args.input, args.output)
        print(f"Created cleaned workbook: {path}")
        return 0

    if args.command == "export-report":
        result = pipeline.run(args.input, report_path=args.output)
        for artifact in result.artifacts:
            print(f"Created {artifact.kind} report: {artifact.path}")
        return 0

    if args.command == "showcase-openpyxl":
        artifact = OpenpyxlFeatureShowcase().build(args.output)
        print(f"Created {artifact.kind} showcase: {artifact.path}")
        return 0

    if args.command == "demo":
        sample_paths = create_all_sample_workbooks(args.sample_dir)
        reports_dir = Path(args.reports_dir)
        reports_dir.mkdir(parents=True, exist_ok=True)
        retail = Path(args.sample_dir) / "retail_demo.xlsx"
        messy = Path(args.sample_dir) / "messy_sales.xlsx"
        profile = pipeline.profile_only(retail)
        cleaned = pipeline.clean_export(messy, "data/processed/demo_cleaned_messy_sales.xlsx")
        result = pipeline.run(retail, report_path=reports_dir / "portfolio_excel_analysis_report.xlsx")
        showcase_artifact = OpenpyxlFeatureShowcase().build(reports_dir / "openpyxl_feature_showcase.xlsx")
        summary = build_demo_summary(result, reports_dir / "demo_summary.html", extra_artifacts=[cleaned, showcase_artifact.path])
        print("Demo artifacts generated:")
        for path in sample_paths:
            print(f"- sample: {path}")
        print(f"- profiled datasets: {', '.join(profile)}")
        for artifact in result.artifacts:
            print(f"- report: {artifact.path}")
        print(f"- cleaned workbook: {cleaned}")
        print(f"- openpyxl showcase: {showcase_artifact.path}")
        print(f"- demo summary: {summary}")
        return 0

    return 1


def _generate_sample(case: str, output: str | None, output_dir: str, seed: int):
    defaults = {
        "retail": "retail_demo.xlsx",
        "messy-sales": "messy_sales.xlsx",
        "finance": "finance_workbook.xlsx",
        "inventory": "inventory_planning.xlsx",
        "customer": "customer_segmentation.xlsx",
    }
    if case == "all":
        return create_all_sample_workbooks(output_dir, seed=seed)
    target = output or f"{output_dir}/{defaults[case]}"
    creators = {
        "retail": create_retail_workbook,
        "messy-sales": create_messy_sales_workbook,
        "finance": create_finance_workbook,
        "inventory": create_inventory_planning_workbook,
        "customer": create_customer_segmentation_workbook,
    }
    return [creators[case](target, seed=seed)]


if __name__ == "__main__":
    raise SystemExit(main())
