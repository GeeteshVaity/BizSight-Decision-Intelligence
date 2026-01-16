from core.data_loader import load_data
from core.data_validator import validate_dataframe

from core.data_mapper import map_to_internal_schema


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
    df_raw = load_data(csv_path)
    df_mapped = map_to_internal_schema(df_raw)
    df = validate_dataframe(df_mapped)

    print("Data loaded, mapped & validated ")


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
    