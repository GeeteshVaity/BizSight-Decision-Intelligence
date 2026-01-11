import pandas as pd


def simulate_changes(df: pd.DataFrame, revenue_change_pct=0, cost_change_pct=0):
    simulated_df = df.copy()

    simulated_df["Revenue"] = simulated_df["Revenue"] * (1 + revenue_change_pct / 100)
    simulated_df["Cost"] = simulated_df["Cost"] * (1 + cost_change_pct / 100)
    simulated_df["Profit"] = simulated_df["Revenue"] - simulated_df["Cost"]

    return simulated_df
