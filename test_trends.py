from core.data_loader import load_data
from core.data_validator import validate_dataframe
from analysis.trends import (
    revenue_trend,
    profit_trend,
    growth_rate,
    detect_consecutive_losses,
    product_trend_ranking,
    get_all_trends
)

# Load test data
df = load_data("data/sample_data.csv")
df = validate_dataframe(df)

print("===== REVENUE TREND =====")
print(revenue_trend(df))

print("\n===== PROFIT TREND =====")
print(profit_trend(df))

print("\n===== OVERALL GROWTH RATE =====")
print(growth_rate(df, "overall"))

print("\n===== AVERAGE GROWTH RATE =====")
print(growth_rate(df, "average"))

print("\n===== CONSECUTIVE LOSSES =====")
print(detect_consecutive_losses(df))

print("\n===== PRODUCT TREND RANKING =====")
for item in product_trend_ranking(df):
    print(item)

print("\n===== ALL TRENDS (SUMMARY) =====")
print(get_all_trends(df))
