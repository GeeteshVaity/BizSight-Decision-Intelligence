import pandas as pd


def simulate_changes(df: pd.DataFrame, revenue_change_pct=0, cost_change_pct=0):
    """
    Simulate percentage changes in revenue and cost and recompute profit.

    Parameters
    ----------
    df : pandas.DataFrame
        Input data containing at least "revenue" and "cost" columns.
    revenue_change_pct : float, optional
        Percentage change to apply to the "revenue" column. For example,
        10 increases revenue by 10%, and -5 decreases it by 5%.
    cost_change_pct : float, optional
        Percentage change to apply to the "cost" column. For example,
        10 increases cost by 10%, and -5 decreases it by 5%.

    Returns
    -------
    pandas.DataFrame
        A copy of the input DataFrame with updated "revenue" and "cost"
        values and a recomputed "profit" column ("revenue" - "cost").
    """
    simulated_df = df.copy()

    simulated_df["revenue"] = simulated_df["revenue"] * (1 + revenue_change_pct / 100)
    simulated_df["cost"] = simulated_df["cost"] * (1 + cost_change_pct / 100)
    simulated_df["profit"] = simulated_df["revenue"] - simulated_df["cost"]

    return simulated_df
