def generate_report(metrics: dict, risks: list, ai_insights: str):
    report = []

    report.append("BIZSIGHT BUSINESS REPORT")
    report.append("-" * 30)

    report.append("\nKEY METRICS:")
    for key, value in metrics.items():
        report.append(f"{key}: {value}")

    report.append("\nDETECTED RISKS:")
    if risks:
        for risk in risks:
            report.append(f"- {risk}")
    else:
        report.append("No major risks detected")

    report.append("\nAI INSIGHTS:")
    report.append(ai_insights)

    return "\n".join(report)
