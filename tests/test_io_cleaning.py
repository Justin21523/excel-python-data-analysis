import pandas as pd

from excel_analysis.cleaning import CleaningPipeline
from excel_analysis.io import CSVReader


def test_csv_reader_detects_delimiter_and_chunks(tmp_path):
    csv_path = tmp_path / "sales.csv"
    csv_path.write_text("order_id;amount\nA001;10\nA002;20\n", encoding="utf-8")

    reader = CSVReader()
    df = reader.read(csv_path)
    chunks = list(reader.read(csv_path, chunksize=1))

    assert list(df.columns) == ["order_id", "amount"]
    assert len(chunks) == 2


def test_cleaning_pipeline_core_operations():
    df = pd.DataFrame(
        {
            "category": [" Electronics ", "Ｅｌｅｃｔｒｏｎｉｃｓ", None],
            "order_date": ["2024-01-01", "bad-date", "2024-01-03"],
            "unit_price": ["$1,200.50", "$50.00", None],
            "discount_pct": ["10%", "5%", None],
            "quantity": [1, 2, 1000],
        }
    )
    cleaner = CleaningPipeline()
    cleaned = cleaner.convert_numeric(cleaner.convert_dates(cleaner.normalize_text(df)))
    filled = cleaner.fill_missing(cleaned, "category", strategy="fixed", value="Unknown")
    clipped = cleaner.clip_outliers_iqr(filled, "quantity")

    assert filled.loc[0, "category"] == "Electronics"
    assert pd.isna(filled.loc[1, "order_date"])
    assert filled.loc[0, "unit_price"] == 1200.50
    assert filled.loc[0, "discount_pct"] == 0.10
    assert filled.loc[2, "category"] == "Unknown"
    clip_source = pd.DataFrame({"quantity": [1, 2, 2, 3, 4, 1000]})
    assert cleaner.clip_outliers_iqr(clip_source, "quantity")["quantity"].max() < 1000
