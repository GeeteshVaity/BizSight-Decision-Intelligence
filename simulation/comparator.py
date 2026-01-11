def compare_profit(original_df, simulated_df):
    original_profit = original_df["Profit"].sum()
    simulated_profit = simulated_df["Profit"].sum()

    return {
        "original_profit": original_profit,
        "simulated_profit": simulated_profit,
        "difference": simulated_profit - original_profit
    }
