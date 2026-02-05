from reportlab.lib.pagesizes import A4
from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer, Image
from reportlab.lib.styles import getSampleStyleSheet
import tempfile
import os

def generate_pdf_report(
    metrics: dict,
    risks: list,
    ai_insights: str,
    chart_files: list
):
    temp_pdf = tempfile.NamedTemporaryFile(delete=False, suffix=".pdf")
    doc = SimpleDocTemplate(temp_pdf.name, pagesize=A4)
    styles = getSampleStyleSheet()
    elements = []

    elements.append(Paragraph("<b>BizSight – Business Intelligence Report</b>", styles["Title"]))
    elements.append(Spacer(1, 12))

    elements.append(Paragraph("<b>Key Metrics</b>", styles["Heading2"]))
    for k, v in metrics.items():
        elements.append(Paragraph(f"{k}: {v}", styles["Normal"]))

    elements.append(Spacer(1, 12))
    elements.append(Paragraph("<b>Risk Analysis</b>", styles["Heading2"]))
    if risks:
        for r in risks:
            elements.append(Paragraph(f"- {r}", styles["Normal"]))
    else:
        elements.append(Paragraph("No major risks detected.", styles["Normal"]))

    elements.append(Spacer(1, 12))
    elements.append(Paragraph("<b>AI Insights</b>", styles["Heading2"]))
    elements.append(Paragraph(ai_insights, styles["Normal"]))

    elements.append(Spacer(1, 12))
    elements.append(Paragraph("<b>Visual Insights</b>", styles["Heading2"]))

    for chart in chart_files:
        if os.path.exists(chart):
            elements.append(Spacer(1, 12))
            elements.append(Image(chart, width=400, height=250))

    doc.build(elements)
    return temp_pdf.name
