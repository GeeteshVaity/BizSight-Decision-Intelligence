import pandas as pd


def compare_profit(original_df: pd.DataFrame, simulated_df: pd.DataFrame):
    """
    Compare total profit between an original dataset and a simulated dataset.

    Parameters
    ----------
    original_df : pandas.DataFrame
        A tabular data structure representing the original data.
        It must contain a numeric "profit" column whose values can be summed.
    simulated_df : pandas.DataFrame
        A tabular data structure representing the simulated data.
        It must contain a numeric "profit" column whose values can be summed.

    Returns
    -------
    dict
        A dictionary with the following keys:

        - "original_profit": float
            The total profit computed from the original dataset.
        - "simulated_profit": float
            The total profit computed from the simulated dataset.
        - "difference": float
            The difference between simulated and original profit
            (simulated_profit - original_profit).
    """
    original_profit = original_df["profit"].sum()
    simulated_profit = simulated_df["profit"].sum()

    return {
        "original_profit": original_profit,
        "simulated_profit": simulated_profit,
        "difference": simulated_profit - original_profit
    }
