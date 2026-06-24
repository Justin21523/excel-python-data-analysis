from __future__ import annotations

import unicodedata

import pandas as pd


class CleaningPipeline:
    """Reusable cleaning operations with before/after summaries."""

    def clean_retail_frames(self, datasets: dict[str, pd.DataFrame]) -> dict[str, pd.DataFrame]:
        cleaned = {name: df.copy() for name, df in datasets.items()}
        for name, df in cleaned.items():
            cleaned[name] = self.normalize_text(df)
            cleaned[name] = self.convert_dates(cleaned[name])
            cleaned[name] = self.convert_numeric(cleaned[name])
            cleaned[name] = self.remove_exact_duplicates(cleaned[name])
        return cleaned

    def remove_exact_duplicates(self, df: pd.DataFrame) -> pd.DataFrame:
        return df.drop_duplicates().reset_index(drop=True)

    def fill_missing(self, df: pd.DataFrame, column: str, strategy: str = "mode", value: object | None = None) -> pd.DataFrame:
        result = df.copy()
        if column not in result:
            return result
        if strategy == "mean":
            result[column] = result[column].fillna(result[column].mean())
        elif strategy == "median":
            result[column] = result[column].fillna(result[column].median())
        elif strategy == "mode":
            modes = result[column].mode(dropna=True)
            result[column] = result[column].fillna(modes.iloc[0] if not modes.empty else value)
        elif strategy == "fixed":
            result[column] = result[column].fillna(value)
        elif strategy in {"ffill", "bfill"}:
            result[column] = result[column].fillna(method=strategy)
        return result

    def normalize_text(self, df: pd.DataFrame) -> pd.DataFrame:
        result = df.copy()
        for col in result.select_dtypes(include=["object", "string", "category"]).columns:
            result[col] = result[col].astype("string").map(
                lambda value: unicodedata.normalize("NFKC", value).strip() if pd.notna(value) else value
            )
        return result

    def convert_dates(self, df: pd.DataFrame) -> pd.DataFrame:
        result = df.copy()
        for col in result.columns:
            if "date" in str(col).lower() or "time" in str(col).lower():
                result[col] = pd.to_datetime(result[col], errors="coerce")
        return result

    def convert_numeric(self, df: pd.DataFrame) -> pd.DataFrame:
        result = df.copy()
        for col in result.columns:
            name = str(col).lower()
            if any(token in name for token in ("price", "amount", "total", "cost", "quantity", "stock", "discount")):
                if result[col].dtype == "object" or str(result[col].dtype).startswith("string"):
                    text = result[col].astype("string")
                    has_percent = text.str.contains("%", na=False)
                    cleaned = text.str.replace(r"[$,%]", "", regex=True).str.replace(",", "", regex=False)
                    numeric = pd.to_numeric(cleaned, errors="coerce").astype("Float64")
                    if "pct" in name or "percent" in name or has_percent.any():
                        numeric = numeric.where(~has_percent, numeric / 100)
                    result[col] = numeric
        return result

    def clip_outliers_iqr(self, df: pd.DataFrame, column: str) -> pd.DataFrame:
        result = df.copy()
        q1, q3 = result[column].quantile([0.25, 0.75])
        iqr = q3 - q1
        if iqr > 0:
            result[column] = result[column].clip(q1 - 1.5 * iqr, q3 + 1.5 * iqr)
        return result
