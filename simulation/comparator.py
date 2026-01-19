def compare_profit(original_df, simulated_df):
    original_profit = original_df["profit"].sum()
    simulated_profit = simulated_df["profit"].sum()

    return {
        "original_profit": original_profit,
        "simulated_profit": simulated_profit,
        "difference": simulated_profit - original_profit
    }
