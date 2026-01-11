import pandas as pd

from visualization.charts import (
    revenue_trend_chart,
    profit_by_product_chart,
    revenue_contribution_pie
)
from simulation.simulator import simulate_changes
from simulation.comparator import compare_profit
from reports.report_generator import generate_report

# ---- Sample Data ----
df = pd.DataFrame({
    "Date": ["2024-01-01", "2024-02-01", "2024-03-01"],
    "Product": ["A", "B", "A"],
    "Revenue": [1000, 1500, 1200],
    "Cost": [700, 900, 800]
})

df["Profit"] = df["Revenue"] - df["Cost"]

# ---- Simulation ----
simulated_df = simulate_changes(df, revenue_change_pct=10, cost_change_pct=-5)

comparison = compare_profit(df, simulated_df)

print("\nSIMULATION OUTPUT:")
print(comparison)

# ---- Report ----
metrics = {
    "Total Revenue": simulated_df["Revenue"].sum(),
    "Total Cost": simulated_df["Cost"].sum(),
    "Total Profit": simulated_df["Profit"].sum()
}

risks = ["High cost ratio detected"]
ai_insights = "Revenue improved, but cost control remains important."

final_report = generate_report(metrics, risks, ai_insights)

print("\nFINAL REPORT OUTPUT:")
print(final_report)

# ---- Charts ----
revenue_trend_chart(df).show()
profit_by_product_chart(df).show()
revenue_contribution_pie(df).show()
