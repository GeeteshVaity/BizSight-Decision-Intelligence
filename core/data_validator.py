import pandas as pd

REQUIRED_COLUMNS = [
    "date",
    "product_name",
    "quantity",
    "revenue",
    "cost",
    "profit",
]

def validate_dataframe(df: pd.DataFrame) -> pd.DataFrame:
    missing = [col for col in REQUIRED_COLUMNS if col not in df.columns]
    if missing:
        raise ValueError(f"Missing internal columns: {missing}")

    # Ensure correct dtypes and no NaNs
    df["quantity"] = pd.to_numeric(df["quantity"], errors="coerce").fillna(0)
    df["revenue"] = pd.to_numeric(df["revenue"], errors="coerce").fillna(0)
    df["cost"] = pd.to_numeric(df["cost"], errors="coerce").fillna(0)
    df["profit"] = pd.to_numeric(df["profit"], errors="coerce").fillna(0)

    if "date" in df.columns:
        df["date"] = pd.to_datetime(df["date"], errors="coerce")

    return df
