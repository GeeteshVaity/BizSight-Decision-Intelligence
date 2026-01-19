import pandas as pd


def simulate_changes(df: pd.DataFrame, revenue_change_pct=0, cost_change_pct=0):
    simulated_df = df.copy()

    simulated_df["revenue"] = simulated_df["revenue"] * (1 + revenue_change_pct / 100)
    simulated_df["cost"] = simulated_df["cost"] * (1 + cost_change_pct / 100)
    simulated_df["profit"] = simulated_df["revenue"] - simulated_df["cost"]

    return simulated_df
