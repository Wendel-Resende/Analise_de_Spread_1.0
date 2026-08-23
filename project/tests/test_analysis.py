import os
import tempfile
import unittest
from datetime import date
from pathlib import Path

import pandas as pd

from src.utils.spread_analysis import analyze_pair
from src.utils.stock_data import get_stock_data


class SpreadAnalysisTests(unittest.TestCase):
    def test_analyze_pair_counts_opportunities_and_returns(self):
        index = pd.date_range("2026-01-01", periods=3, freq="D")
        stock_a = pd.Series([10.0, 14.0, 12.0], index=index)
        stock_b = pd.Series([9.0, 10.0, 11.0], index=index)

        result = analyze_pair(stock_a, stock_b, spread_min=2.0)

        self.assertEqual(result["Total_Opportunities"], 1)
        self.assertAlmostEqual(result["Total_Return"], -7.0)
        self.assertAlmostEqual(result["Spread_Max"], 4.0)

    def test_analyze_pair_handles_no_opportunities(self):
        index = pd.date_range("2026-01-01", periods=2, freq="D")
        result = analyze_pair(
            pd.Series([10.0, 11.0], index=index),
            pd.Series([9.5, 10.5], index=index),
            spread_min=2.0,
        )

        self.assertEqual(result["Total_Opportunities"], 0)
        self.assertEqual(result["Total_Return"], 0)


class StockDataTests(unittest.TestCase):
    def test_loads_and_filters_local_csv(self):
        with tempfile.TemporaryDirectory() as directory:
            path = Path(directory) / "PETR3.csv"
            pd.DataFrame(
                {
                    "Date": ["2026-01-01", "2026-01-02", "2026-01-03"],
                    "High": [10, 11, 12],
                }
            ).to_csv(path, index=False)
            old_value = os.environ.get("STOCK_DATA_DIR")
            os.environ["STOCK_DATA_DIR"] = directory
            try:
                result = get_stock_data("PETR3.SA", date(2026, 1, 2), date(2026, 1, 3))
            finally:
                if old_value is None:
                    os.environ.pop("STOCK_DATA_DIR", None)
                else:
                    os.environ["STOCK_DATA_DIR"] = old_value

        self.assertEqual(result.tolist(), [11.0, 12.0])

    def test_rejects_missing_local_file(self):
        with tempfile.TemporaryDirectory() as directory:
            old_value = os.environ.get("STOCK_DATA_DIR")
            os.environ["STOCK_DATA_DIR"] = directory
            try:
                with self.assertRaises(FileNotFoundError):
                    get_stock_data("MISSING", date(2026, 1, 1), date(2026, 1, 2))
            finally:
                if old_value is None:
                    os.environ.pop("STOCK_DATA_DIR", None)
                else:
                    os.environ["STOCK_DATA_DIR"] = old_value


if __name__ == "__main__":
    unittest.main()
