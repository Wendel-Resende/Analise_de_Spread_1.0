"""Market data loading with explicit local-file provenance."""

from __future__ import annotations

import os
from datetime import date, datetime
from pathlib import Path

import pandas as pd


def get_stock_data(
    ticker: str,
    start_date: date | datetime,
    end_date: date | datetime,
) -> pd.Series:
    """Load daily high prices from a local CSV data directory.

    The CSV must contain a date column (``Date`` or ``date``) and a high-price
    column (``High`` or ``high``). The directory is configured with
    ``STOCK_DATA_DIR`` and defaults to ``data/market``.
    """
    symbol = ticker.upper().strip().removesuffix(".SA")
    if not symbol or any(ch in symbol for ch in "/\\\\"):
        raise ValueError("Ticker must be a non-empty symbol without path separators")

    data_dir = Path(os.environ.get("STOCK_DATA_DIR", "data/market"))
    path = data_dir / f"{symbol}.csv"
    if not path.is_file():
        raise FileNotFoundError(
            f"No local market file for {symbol}: {path}. "
            "Set STOCK_DATA_DIR or provide the CSV before running the analysis."
        )

    frame = pd.read_csv(path)
    date_column = next((c for c in ("Date", "date") if c in frame.columns), None)
    high_column = next((c for c in ("High", "high") if c in frame.columns), None)
    if date_column is None or high_column is None:
        raise ValueError(f"{path} must contain Date/date and High/high columns")

    dates = pd.to_datetime(frame[date_column], errors="coerce")
    high_values = pd.Series(frame[high_column].tolist(), dtype="float64")
    result = pd.Series(high_values.tolist(), index=dates, name="High").dropna()
    result = result[~result.index.isna()].sort_index()

    start = pd.Timestamp(start_date)
    end = pd.Timestamp(end_date)
    result = result[(result.index >= start) & (result.index <= end)]
    if result.empty:
        raise ValueError(f"No valid {symbol} data between {start.date()} and {end.date()}")
    return result
