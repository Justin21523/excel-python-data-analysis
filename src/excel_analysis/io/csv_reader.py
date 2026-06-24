from __future__ import annotations

import csv
from pathlib import Path
from typing import Iterator

import pandas as pd


class CSVReader:
    """CSV reader with practical delimiter and encoding fallbacks."""

    encodings = ("utf-8", "utf-8-sig", "cp950", "big5", "latin-1")

    def read(self, path: str | Path, chunksize: int | None = None) -> pd.DataFrame | Iterator[pd.DataFrame]:
        path = Path(path)
        encoding = self.detect_encoding(path)
        delimiter = self.detect_delimiter(path, encoding)
        return pd.read_csv(path, encoding=encoding, sep=delimiter, chunksize=chunksize)

    def detect_encoding(self, path: Path) -> str:
        sample = path.read_bytes()[:4096]
        for encoding in self.encodings:
            try:
                sample.decode(encoding)
                return encoding
            except UnicodeDecodeError:
                continue
        return "latin-1"

    def detect_delimiter(self, path: Path, encoding: str) -> str:
        sample = path.read_text(encoding=encoding, errors="ignore")[:4096]
        try:
            return csv.Sniffer().sniff(sample, delimiters=",;\t|").delimiter
        except csv.Error:
            return ","

