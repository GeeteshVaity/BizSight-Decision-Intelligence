import pandas as pd

INTERNAL_COLUMNS = [
    "date",
    "product_name",
    "quantity",
    "selling_price",
    "revenue",
    "cost",
    "profit",
]

def validate_dataframe(df: pd.DataFrame) -> pd.DataFrame:
    missing = [c for c in INTERNAL_COLUMNS if c not in df.columns]
    if missing:
        raise ValueError(f"Missing internal columns: {missing}")

    df = df.dropna(subset=["date", "product_name", "quantity", "revenue", "cost"])

    df = df[
        (df["quantity"] >= 0)
        & (df["revenue"] >= 0)
        & (df["cost"] >= 0)
    ]

    df["selling_price"] = df["selling_price"].fillna(0)
    df["profit"] = df["profit"].fillna(df["revenue"] - df["cost"])

    return df
