from __future__ import annotations

import re

import pandas as pd

from excel_analysis.schemas import QualityIssue


class QualityChecker:
    """Detect common Excel business-data quality issues."""

    def check(self, dataset_name: str, df: pd.DataFrame) -> list[QualityIssue]:
        issues: list[QualityIssue] = []
        rows = max(len(df), 1)

        duplicated = int(df.duplicated().sum())
        if duplicated:
            issues.append(QualityIssue(dataset_name, None, "duplicated_rows", "medium", duplicated, "Remove exact duplicate rows."))

        for col in df.columns:
            series = df[col]
            missing = int(series.isna().sum())
            if missing:
                severity = "high" if missing / rows > 0.2 else "medium"
                issues.append(QualityIssue(dataset_name, col, "missing_values", severity, missing, "Fill, remove, or validate against source data."))

            if self._looks_like_id(col):
                dup_ids = int(series.dropna().duplicated().sum())
                if dup_ids:
                    issues.append(QualityIssue(dataset_name, col, "duplicated_ids", "high", dup_ids, "Check primary key uniqueness."))

            if self._looks_like_quantity(col) and pd.api.types.is_numeric_dtype(series):
                count = int((series < 0).sum())
                if count:
                    issues.append(QualityIssue(dataset_name, col, "negative_quantities", "high", count, "Quantities should usually be non-negative."))

            if self._looks_like_amount(col) and pd.api.types.is_numeric_dtype(series):
                count = int((series < 0).sum())
                if count:
                    issues.append(QualityIssue(dataset_name, col, "negative_amounts", "high", count, "Validate refunds separately from sales amounts."))

            if series.dtype == "object":
                whitespace = int(series.dropna().astype(str).str.contains(r"^\s+|\s+$").sum())
                if whitespace:
                    issues.append(QualityIssue(dataset_name, col, "suspicious_whitespace", "low", whitespace, "Strip leading and trailing whitespace."))

                if "email" in col.lower():
                    invalid = int(~series.dropna().astype(str).str.match(r"^[^@\s]+@[^@\s]+\.[^@\s]+$").sum())
                    if invalid:
                        issues.append(QualityIssue(dataset_name, col, "invalid_email", "medium", invalid, "Validate email format."))

            if pd.api.types.is_numeric_dtype(series):
                outliers = self._iqr_outlier_count(series)
                if outliers:
                    issues.append(QualityIssue(dataset_name, col, "numeric_outliers", "low", outliers, "Review outliers with IQR rule."))

        return issues

    def quality_score(self, df: pd.DataFrame, issues: list[QualityIssue]) -> float:
        if df.empty:
            return 0.0
        penalty = {"high": 10.0, "medium": 5.0, "low": 2.0}
        raw = 100.0 - sum(penalty.get(issue.severity, 1.0) for issue in issues)
        return round(max(0.0, raw), 1)

    def _iqr_outlier_count(self, series: pd.Series) -> int:
        clean = series.dropna()
        if len(clean) < 8:
            return 0
        q1, q3 = clean.quantile([0.25, 0.75])
        iqr = q3 - q1
        if iqr == 0:
            return 0
        return int(((clean < q1 - 1.5 * iqr) | (clean > q3 + 1.5 * iqr)).sum())

    def _looks_like_id(self, column: str) -> bool:
        return bool(re.search(r"(^id$|_id$|id$)", column.lower()))

    def _looks_like_amount(self, column: str) -> bool:
        return any(token in column.lower() for token in ("amount", "price", "revenue", "sales", "total", "cost"))

    def _looks_like_quantity(self, column: str) -> bool:
        return any(token in column.lower() for token in ("qty", "quantity", "units"))

