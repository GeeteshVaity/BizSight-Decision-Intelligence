import pandas as pd

REQUIRED_COLUMNS = ["date", "product", "revenue", "cost"]

def validate_dataframe(df: pd.DataFrame) -> pd.DataFrame:
    # 1. Check required columns
    missing = [col for col in REQUIRED_COLUMNS
                if col not in df.columns]
    if missing:
        raise ValueError(f"Missing columns: {missing}")

    # 2. Drop rows with nulls
    df = df.dropna(subset=REQUIRED_COLUMNS)

    # 3. Remove invalid rows
    df = df.dropna()
    df = df[(df["revenue"] >= 0) & (df["cost"] >= 0)] #Keep only rows where revenue ≥ 0 AND cost ≥ 0.

    return df