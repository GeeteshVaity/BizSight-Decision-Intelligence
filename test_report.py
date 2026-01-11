from reports.report_generator import generate_report

# Sample data for testing
metrics = {
    "Total Revenue": 10000,
    "Total Cost": 7000,
    "Total Profit": 3000
}

risks = [
    "High cost ratio detected",
    "Profit margin is low"
]

ai_insights = "The business shows moderate profitability but needs cost optimization."

# Call your function
final_report = generate_report(metrics, risks, ai_insights)

# Print the result
print(final_report)
