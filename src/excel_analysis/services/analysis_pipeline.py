from __future__ import annotations

from pathlib import Path

import pandas as pd

from excel_analysis.analytics import (
    abc_analysis,
    cohort_retention,
    customer_analysis,
    inventory_analysis,
    market_basket_analysis,
    rfm_segmentation,
    sales_analysis,
    time_series_analysis,
)
from excel_analysis.cleaning import CleaningPipeline
from excel_analysis.io import CSVReader, ExcelReader
from excel_analysis.profiling import DataProfiler
from excel_analysis.reporting import OpenpyxlReportBuilder
from excel_analysis.schemas import AnalysisResult


class AnalysisPipeline:
    """End-to-end Excel/CSV business analytics workflow."""

    def __init__(self):
        self.excel_reader = ExcelReader()
        self.csv_reader = CSVReader()
        self.profiler = DataProfiler()
        self.cleaner = CleaningPipeline()
        self.report_builder = OpenpyxlReportBuilder()

    def load(self, input_path: str | Path) -> dict[str, pd.DataFrame]:
        path = Path(input_path)
        if path.suffix.lower() in {".xlsx", ".xlsm"}:
            return self.excel_reader.read(path)
        if path.suffix.lower() == ".csv":
            return {path.stem: self.csv_reader.read(path)}  # type: ignore[dict-item]
        raise ValueError(f"Unsupported input file type: {path.suffix}")

    def run(
        self,
        input_path: str | Path,
        output_dir: str | Path = "reports",
        report_path: str | Path | None = None,
    ) -> AnalysisResult:
        datasets = self.load(input_path)
        cleaned = self.cleaner.clean_retail_frames(datasets)
        profiles = {name: self.profiler.profile(name, df) for name, df in cleaned.items()}
        analytics = self._run_analytics(cleaned)
        result = AnalysisResult(datasets=datasets, profiles=profiles, analytics=analytics, cleaned_datasets=cleaned)
        output_path = Path(report_path) if report_path else Path(output_dir) / "portfolio_excel_analysis_report.xlsx"
        result.artifacts.append(self.report_builder.build(result, output_path))
        return result

    def profile_only(self, input_path: str | Path) -> dict[str, object]:
        datasets = self.load(input_path)
        return {name: self.profiler.profile(name, df).as_dict() for name, df in datasets.items()}

    def clean_export(self, input_path: str | Path, output_path: str | Path = "data/processed/cleaned.xlsx") -> Path:
        datasets = self.load(input_path)
        cleaned = self.cleaner.clean_retail_frames(datasets)
        output = Path(output_path)
        output.parent.mkdir(parents=True, exist_ok=True)
        with pd.ExcelWriter(output, engine="openpyxl") as writer:
            for sheet_name, df in cleaned.items():
                df.to_excel(writer, sheet_name=str(sheet_name)[:31], index=False)
        return output

    def run_analytics_for_datasets(self, datasets: dict[str, pd.DataFrame]) -> dict[str, object]:
        return self._run_analytics(datasets)

    def _run_analytics(self, datasets: dict[str, pd.DataFrame]) -> dict[str, object]:
        required = {"orders", "order_items", "customers", "products", "inventory"}
        missing = required.difference(datasets)
        if missing:
            raise ValueError(f"Retail analytics requires sheets: {sorted(required)}. Missing: {sorted(missing)}")
        return {
            "sales": sales_analysis(datasets),
            "customers": customer_analysis(datasets),
            "rfm": rfm_segmentation(datasets),
            "cohort": cohort_retention(datasets),
            "inventory": inventory_analysis(datasets),
            "abc": abc_analysis(datasets),
            "market_basket": market_basket_analysis(datasets),
            "time_series": time_series_analysis(datasets),
        }
