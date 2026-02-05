import streamlit as st
from groq import Groq

# --------------------------------------------------
# GROQ SETUP (STREAMLIT CLOUD SAFE)
# --------------------------------------------------

client = Groq(api_key=st.secrets["GROQ_API_KEY"])
AI_AVAILABLE = True

MODEL_NAME = "llama-3.1-8b-instant"

# --------------------------------------------------
# BUSINESS INSIGHTS
# --------------------------------------------------

def generate_business_insights(df, focus_area="overall", model_key=None):
    if df is None or df.empty:
        return {
            "success": False,
            "insights": "",
            "key_points": [],
            "recommendations": [],
            "error": "No data provided"
        }

    try:
        from analysis.analyzer import get_all_metrics
        from analysis.trends import get_all_trends
        from intelligence.risk_detector import get_all_risks

        metrics = get_all_metrics(df)
        trends = get_all_trends(df)
        risks = get_all_risks(df)

        summary = _prepare_data_summary(metrics, trends, risks)

        # --------- NO AI FALLBACK ----------
        if not AI_AVAILABLE:
            return {
                "success": True,
                "insights": "AI insights unavailable. Showing rule-based analysis only.",
                "key_points": list(risks["summary"].values())[:3],
                "recommendations": [
                    "Review pricing strategy",
                    "Optimize inventory levels",
                    "Focus on high-performing products"
                ],
                "error": None
            }

        prompt = f"""
You are a business analyst AI.

Analyze the data below and respond in EXACTLY this format.
Do NOT add extra text.

DATA:
{summary}

FORMAT:

INSIGHTS:
<one paragraph>

KEY POINTS:
- Point 1
- Point 2
- Point 3

RECOMMENDATIONS:
- Recommendation 1
- Recommendation 2
- Recommendation 3
"""

        response = client.chat.completions.create(
            model=MODEL_NAME,
            messages=[
                {"role": "system", "content": "You are a professional business intelligence assistant."},
                {"role": "user", "content": prompt}
            ],
            temperature=0.4,
        )

        text = response.choices[0].message.content
        parsed = _parse_ai_response(text)

        return {
            "success": True,
            "insights": parsed["insights"],
            "key_points": parsed["key_points"],
            "recommendations": parsed["recommendations"],
            "error": None
        }

    except Exception as e:
        msg = str(e)

        return {
            "success": False,
            "insights": "",
            "key_points": [],
            "recommendations": [],
            "error": msg
        }


# --------------------------------------------------
# QUICK SUMMARY
# --------------------------------------------------

def generate_quick_summary(df, model_key=None):
    if df is None or df.empty:
        return {"success": False, "summary": "", "error": "No data"}

    try:
        from analysis.analyzer import get_all_metrics
        metrics = get_all_metrics(df)

        prompt = f"""
Summarize the business performance in 2 sentences.

Revenue: {metrics['total_revenue']}
Cost: {metrics['total_cost']}
Profit: {metrics['total_profit']}
Margin: {metrics['profit_margin']}%
"""

        response = client.chat.completions.create(
            model=MODEL_NAME,
            messages=[{"role": "user", "content": prompt}],
            temperature=0.3,
        )

        return {
            "success": True,
            "summary": response.choices[0].message.content.strip(),
            "error": None
        }

    except Exception as e:
        return {
            "success": False,
            "summary": "",
            "error": str(e)
        }

# --------------------------------------------------
# HELPERS (UNCHANGED)
# --------------------------------------------------

def _prepare_data_summary(metrics, trends, risks):
    return f"""
Revenue: {metrics['total_revenue']}
Cost: {metrics['total_cost']}
Profit: {metrics['total_profit']}
Margin: {metrics['profit_margin']}%

Revenue Trend: {trends['revenue_trend']['trend']}
Profit Trend: {trends['profit_trend']['trend']}

Risk Level: {risks['summary']['overall_risk_level']}
"""

def _parse_ai_response(text):
    insights = ""
    key_points = []
    recommendations = []
    section = None

    for line in text.splitlines():
        l = line.strip()

        if l.upper().startswith("INSIGHTS"):
            section = "insights"
            continue
        if l.upper().startswith("KEY"):
            section = "key"
            continue
        if l.upper().startswith("RECOMMEND"):
            section = "rec"
            continue

        if section == "insights" and l:
            insights += " " + l

        elif section == "key" and l.startswith(("-", "•")):
            key_points.append(l.lstrip("-• ").strip())

        elif section == "rec" and l.startswith(("-", "•")):
            recommendations.append(l.lstrip("-• ").strip())

    return {
        "insights": insights.strip() or text.strip(),
        "key_points": key_points or ["No key points generated"],
        "recommendations": recommendations or ["No recommendations generated"]
    }
