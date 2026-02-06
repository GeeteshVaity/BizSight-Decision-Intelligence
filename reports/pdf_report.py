# reports/pdf_report.py

from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer, Image
from reportlab.lib.styles import getSampleStyleSheet
from io import BytesIO

def generate_pdf_report(metrics, risks, ai_insights, chart_files):
    buffer = BytesIO()
    doc = SimpleDocTemplate(buffer)
    styles = getSampleStyleSheet()
    elements = []

    elements.append(Paragraph("BizSight Business Report", styles["Title"]))
    elements.append(Spacer(1, 12))

    for k, v in metrics.items():
        elements.append(Paragraph(f"<b>{k}:</b> {v}", styles["Normal"]))

    elements.append(Spacer(1, 12))

    elements.append(Paragraph("<b>Risks</b>", styles["Heading2"]))
    for r in risks:
        elements.append(Paragraph(f"- {r}", styles["Normal"]))

    elements.append(Spacer(1, 12))

    elements.append(Paragraph("<b>AI Insights</b>", styles["Heading2"]))
    elements.append(Paragraph(ai_insights, styles["Normal"]))

    elements.append(Spacer(1, 20))

    # 🔥 Charts from BYTES (not files)
    for name, img_bytes in chart_files.items():
        img_stream = BytesIO(img_bytes)
        elements.append(Image(img_stream, width=400, height=250))
        elements.append(Spacer(1, 12))

    doc.build(elements)
    buffer.seek(0)

    return buffer.getvalue()
