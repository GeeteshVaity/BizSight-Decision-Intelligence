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

    # Selling price (ONLY for revenue calculation)
    selling_price_col = None
    for col in ["selling_price","sell_price", "mrp", "unit_selling_price"]:
        if col in df.columns:
            selling_price_col = col
            df["selling_price"] = pd.to_numeric(df[col], errors="coerce")
            break

    # Revenue
    if "revenue" in df.columns:
        df["revenue"] = pd.to_numeric(df["revenue"], errors="coerce")
    elif selling_price_col is not None:
        df["revenue"] = df["quantity"] * df["selling_price"]
    elif "total_price" in df.columns:
        df["revenue"] = pd.to_numeric(df["total_price"], errors="coerce")
    elif "sales" in df.columns:
        df["revenue"] = pd.to_numeric(df["sales"], errors="coerce")
    else:
        df["revenue"] = 0

    # Cost (price treated as COST per unit)
    if "cost" in df.columns:
        df["cost"] = pd.to_numeric(df["cost"], errors="coerce")
    elif "price" in df.columns:
        df["cost"] = pd.to_numeric(df["price"], errors="coerce") * df["quantity"]
    else:
        df["cost"] = 0

    # Profit
    df["profit"] = df["revenue"] - df["cost"]

    return df[
        [
            "date",
            "product_name",
            "quantity",
            "revenue",
            "cost",
            "profit",
        ]
    ]
