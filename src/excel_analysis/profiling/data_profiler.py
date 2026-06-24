from __future__ import annotations

import pandas as pd

from excel_analysis.profiling.quality_checker import QualityChecker
from excel_analysis.schemas import DatasetProfile


class DataProfiler:
    """Build structured profiles for Excel sheets and CSV datasets."""

    def __init__(self, quality_checker: QualityChecker | None = None):
        self.quality_checker = quality_checker or QualityChecker()

    def profile(self, dataset_name: str, df: pd.DataFrame) -> DatasetProfile:
        issues = self.quality_checker.check(dataset_name, df)
        numeric_summary = self._numeric_summary(df)
        categorical_summary = self._categorical_summary(df)
        date_range = self._date_range(df)
        suspected = self._suspected_columns(df)
        return DatasetProfile(
            dataset_name=dataset_name,
            rows=int(len(df)),
            columns=int(len(df.columns)),
            column_names=[str(col) for col in df.columns],
            dtypes={str(col): str(dtype) for col, dtype in df.dtypes.items()},
            missing_values={str(col): int(df[col].isna().sum()) for col in df.columns},
            missing_percentage={str(col): round(float(df[col].isna().mean() * 100), 2) for col in df.columns},
            duplicated_rows=int(df.duplicated().sum()),
            unique_values={str(col): int(df[col].nunique(dropna=True)) for col in df.columns},
            numeric_summary=numeric_summary,
            categorical_summary=categorical_summary,
            date_range=date_range,
            suspected_columns=suspected,
            quality_score=self.quality_checker.quality_score(df, issues),
            issues=issues,
        )

    def _numeric_summary(self, df: pd.DataFrame) -> dict[str, dict[str, float]]:
        result: dict[str, dict[str, float]] = {}
        for col in df.select_dtypes(include="number").columns:
            desc = df[col].describe()
            result[str(col)] = {key: round(float(value), 4) for key, value in desc.items() if pd.notna(value)}
        return result

    def _categorical_summary(self, df: pd.DataFrame) -> dict[str, dict[str, object]]:
        result: dict[str, dict[str, object]] = {}
        for col in df.select_dtypes(include=["object", "category", "string"]).columns:
            counts = df[col].astype("string").value_counts(dropna=True).head(10)
            result[str(col)] = {"top_values": counts.to_dict(), "unique_count": int(df[col].nunique(dropna=True))}
        return result

    def _date_range(self, df: pd.DataFrame) -> dict[str, dict[str, str | None]]:
        result: dict[str, dict[str, str | None]] = {}
        for col in df.columns:
            if pd.api.types.is_datetime64_any_dtype(df[col]) or "date" in str(col).lower() or "time" in str(col).lower():
                parsed = pd.to_datetime(df[col], errors="coerce")
                if parsed.notna().any():
                    result[str(col)] = {"min": str(parsed.min()), "max": str(parsed.max())}
        return result

    def _suspected_columns(self, df: pd.DataFrame) -> dict[str, list[str]]:
        names = {col: str(col).lower() for col in df.columns}
        return {
            "id": [col for col, name in names.items() if name == "id" or name.endswith("_id")],
            "amount": [col for col, name in names.items() if any(token in name for token in ("amount", "price", "total", "revenue", "cost"))],
            "date": [col for col, name in names.items() if "date" in name or "time" in name],
            "category": [col for col, name in names.items() if "category" in name or "region" in name or "status" in name],
        }

