from core.data_loader import load_data
from core.data_validator import validate_dataframe

# TEMP: analytics will be provided by Dhruv
try:
    from analysis.analyzer import (
        total_revenue,
        total_cost,
        total_profit,
        profit_margin,
        product_wise_summary
    )
except ImportError:
    total_revenue = total_cost = total_profit = profit_margin = product_wise_summary = None


def run_pipeline(csv_path):
    df = load_data(csv_path)
    df = validate_dataframe(df)

    print("Data loaded & validated ✅")

    if total_revenue:
        print("Total Revenue:", total_revenue(df))
        print("Total Cost:", total_cost(df))
        print("Total Profit:", total_profit(df))
        print("Profit Margin:", profit_margin(df))
        print(product_wise_summary(df))
    else:
        print("Analytics module not available yet.")


if __name__ == "__main__":
    run_pipeline("data/sample_data.csv")
