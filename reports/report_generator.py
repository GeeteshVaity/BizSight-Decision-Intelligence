SEPARATOR_LENGTH = 30


def generate_report(metrics: dict, risks: list, ai_insights: str):
    """
    Generate a formatted business report string from metrics, risks, and AI insights.

    Args:
        metrics (dict): A mapping of metric names to their values. Keys are strings
            (for example, "Revenue", "Customer Growth"), and values are typically
            numbers or preformatted strings that can be rendered directly in the
            report.
        risks (list): A list of risk descriptions to include under the "DETECTED
            RISKS" section. Each item should be a human-readable string. If the list
            is empty or falsy, a default "No major risks detected" line is added.
        ai_insights (str): A block of AI-generated narrative or commentary to be
            included under the "AI INSIGHTS" section.

    Returns:
        str: A single multi-line string containing the complete report, with
        sections for key metrics, detected risks, and AI insights separated by
        newlines.
    """
    report = []

    report.append("BIZSIGHT BUSINESS REPORT")
    report.append("-" * SEPARATOR_LENGTH)

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
