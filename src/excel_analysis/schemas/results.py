from __future__ import annotations

from dataclasses import dataclass, field
from pathlib import Path
from typing import Any

import pandas as pd


@dataclass(slots=True)
class QualityIssue:
    dataset_name: str
    column: str | None
    issue_type: str
    severity: str
    count: int
    suggestion: str

    def as_dict(self) -> dict[str, Any]:
        return {
            "dataset_name": self.dataset_name,
            "column": self.column,
            "issue_type": self.issue_type,
            "severity": self.severity,
            "count": self.count,
            "suggestion": self.suggestion,
        }


@dataclass(slots=True)
class DatasetProfile:
    dataset_name: str
    rows: int
    columns: int
    column_names: list[str]
    dtypes: dict[str, str]
    missing_values: dict[str, int]
    missing_percentage: dict[str, float]
    duplicated_rows: int
    unique_values: dict[str, int]
    numeric_summary: dict[str, dict[str, float]]
    categorical_summary: dict[str, dict[str, Any]]
    date_range: dict[str, dict[str, str | None]]
    suspected_columns: dict[str, list[str]]
    quality_score: float
    issues: list[QualityIssue] = field(default_factory=list)

    def as_dict(self) -> dict[str, Any]:
        return {
            "dataset_name": self.dataset_name,
            "rows": self.rows,
            "columns": self.columns,
            "column_names": self.column_names,
            "dtypes": self.dtypes,
            "missing_values": self.missing_values,
            "missing_percentage": self.missing_percentage,
            "duplicated_rows": self.duplicated_rows,
            "unique_values": self.unique_values,
            "numeric_summary": self.numeric_summary,
            "categorical_summary": self.categorical_summary,
            "date_range": self.date_range,
            "suspected_columns": self.suspected_columns,
            "quality_score": self.quality_score,
            "issues": [issue.as_dict() for issue in self.issues],
        }


@dataclass(slots=True)
class ReportArtifact:
    path: Path
    kind: str
    description: str


@dataclass(slots=True)
class AnalysisResult:
    datasets: dict[str, pd.DataFrame]
    profiles: dict[str, DatasetProfile]
    analytics: dict[str, Any]
    cleaned_datasets: dict[str, pd.DataFrame]
    artifacts: list[ReportArtifact] = field(default_factory=list)

