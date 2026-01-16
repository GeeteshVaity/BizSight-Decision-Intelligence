import pandas as pd

def map_to_internal_schema(df: pd.DataFrame) -> pd.DataFrame:
    df = df.copy()

    # Date
    for col in ["date", "order_date", "invoice_date"]:
        if col in df.columns:
            df["date"] = pd.to_datetime(df[col], errors="coerce")
            break
    else:
        df["date"] = pd.NaT

    # Product
    for col in ["product", "product_name", "item", "item_name"]:
        if col in df.columns:
            df["product_name"] = df[col].astype(str)
            break
    else:
        df["product_name"] = "Unknown"

    # Quantity
    for col in ["quantity", "qty", "units"]:
        if col in df.columns:
            df["quantity"] = pd.to_numeric(df[col], errors="coerce").fillna(0)
            break
    else:
        df["quantity"] = 0

    # Selling price
    for col in ["selling_price", "unit_price", "price"]:
        if col in df.columns:
            df["selling_price"] = pd.to_numeric(df[col], errors="coerce")
            break
    else:
        df["selling_price"] = 0

    # Revenue
    if "revenue" in df.columns:
        df["revenue"] = pd.to_numeric(df["revenue"], errors="coerce")
    elif "total_price" in df.columns:
        df["revenue"] = pd.to_numeric(df["total_price"], errors="coerce")
    elif "sales" in df.columns:
        df["revenue"] = pd.to_numeric(df["sales"], errors="coerce")
    else:
        df["revenue"] = df["quantity"] * df["selling_price"]

    # Cost
    if "cost" in df.columns:
        df["cost"] = pd.to_numeric(df["cost"], errors="coerce")
    elif "unit_cost" in df.columns:
        df["cost"] = pd.to_numeric(df["unit_cost"], errors="coerce") * df["quantity"]
    else:
        df["cost"] = 0

    # Profit
    if "profit" in df.columns:
        df["profit"] = pd.to_numeric(df["profit"], errors="coerce")
    else:
        df["profit"] = df["revenue"] - df["cost"]

    return df[
        [
            "date",
            "product_name",
            "quantity",
            "selling_price",
            "revenue",
            "cost",
            "profit",
        ]
    ]
