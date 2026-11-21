import pandas as pd
from data_tools import summarize_dataframe

def test_financial_metrics_calculation(tmp_path):
    csv_file = tmp_path / "metrics.csv"
    pd.DataFrame({"revenue": [10, 20, 30], "profit": [1, 2, 3]}).to_csv(csv_file, index=False)
    result = summarize_dataframe(str(csv_file))
    assert result.loc["mean", "revenue"] == 20
    assert result.loc["min", "profit"] == 1
    assert result.loc["max", "profit"] == 3
