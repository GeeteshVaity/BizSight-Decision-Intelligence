import os
from dotenv import load_dotenv
from google import genai

# --------------------------------------------------
# ENV SETUP
# --------------------------------------------------

load_dotenv()
API_KEY = os.getenv("GEMINI_API_KEY")
AI_AVAILABLE = bool(API_KEY)

client = None
if AI_AVAILABLE:
    client = genai.Client(api_key=API_KEY)

# --------------------------------------------------
# MODEL CONFIG (LOCKED)
# --------------------------------------------------

MODEL_NAME = "models/gemini-flash-lite-latest"

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
        if not AI_AVAILABLE or client is None:
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

        response = client.models.generate_content(
            model=MODEL_NAME,
            contents=prompt
        )

        parsed = _parse_ai_response(response.text)

        return {
            "success": True,
            "insights": parsed["insights"],
            "key_points": parsed["key_points"],
            "recommendations": parsed["recommendations"],
            "error": None
        }

    except Exception as e:
        msg = str(e)

        if "RESOURCE_EXHAUSTED" in msg or "Quota" in msg:
            return {
                "success": False,
                "insights": "",
                "key_points": [],
                "recommendations": [],
                "error": "AI quota exceeded"
            }

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

        if not AI_AVAILABLE or client is None:
            return {
                "success": True,
                "summary": "Business summary unavailable (AI not configured).",
                "error": None
            }

        prompt = f"""
Summarize the business performance in 2 sentences.

Revenue: {metrics['total_revenue']}
Cost: {metrics['total_cost']}
Profit: {metrics['total_profit']}
Margin: {metrics['profit_margin']}%
"""

        response = client.models.generate_content(
            model=MODEL_NAME,
            contents=prompt
        )

        return {
            "success": True,
            "summary": response.text.strip(),
            "error": None
        }

    except Exception as e:
        return {
            "success": False,
            "summary": "",
            "error": str(e)
        }

# --------------------------------------------------
# HELPERS
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
