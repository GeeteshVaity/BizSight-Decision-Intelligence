import pandas as pd
from visualization.charts import (
    revenue_trend_chart,
    profit_by_product_chart,
    revenue_contribution_pie
)

# Dummy data
df = pd.DataFrame({
    "Date": ["2024-01-01", "2024-02-01", "2024-03-01"],
    "Product": ["A", "B", "A"],
    "Revenue": [1000, 1500, 1200],
    "Cost": [700, 900, 800]
})

df["Profit"] = df["Revenue"] - df["Cost"]

# Show charts
revenue_trend_chart(df).show()
profit_by_product_chart(df).show()
revenue_contribution_pie(df).show()
