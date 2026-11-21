from pathlib import Path
import pandas as pd
try:
    from crewai.tools import tool
except ImportError:  # Allows local unit tests before CrewAI dependencies are installed.
    def tool(name=None):
        def decorator(func):
            return func
        return decorator

@tool("Calculate Financial Metrics")
def calculate_financial_metrics(csv_path: str) -> str:
    """Load a CSV file and return count, mean, standard deviation, minimum and maximum."""
    path = Path(csv_path)
    if not path.exists():
        return f"CSV file not found: {csv_path}"
    try:
        df = pd.read_csv(path)
        numeric = df.select_dtypes(include="number")
        if numeric.empty:
            return "The CSV contains no numeric columns."
        summary = numeric.describe().round(2).to_markdown()
        return f"Rows: {len(df)}\n\n{summary}"
    except Exception as exc:
        return f"Could not analyze CSV: {exc}"

def summarize_dataframe(csv_path: str) -> pd.DataFrame:
    """Non-agent helper used by automated tests."""
    df = pd.read_csv(csv_path)
    numeric = df.select_dtypes(include="number")
    if numeric.empty:
        raise ValueError("No numeric columns found")
    return numeric.describe()
