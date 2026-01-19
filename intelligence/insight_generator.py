import os
from dotenv import load_dotenv
from google import genai

load_dotenv()

API_KEY = os.getenv("GEMINI_API_KEY")

if not API_KEY:
    raise RuntimeError("GEMINI_API_KEY not found")

client = genai.Client(api_key=API_KEY)

MODEL_NAME = "models/gemini-flash-lite-latest"


def generate_business_insights(df, focus_area="overall"):
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

        prompt = f"""
        You are a business analyst AI.

        Analyze the data below and respond in EXACTLY this format.
        Do NOT add extra text or explanations.

        DATA:
        {summary}

        FORMAT (FOLLOW STRICTLY):

        INSIGHTS:
        <one clear paragraph>

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
                "error": "AI quota exceeded. Please try again later."
            }

        return {
            "success": False,
            "insights": "",
            "key_points": [],
            "recommendations": [],
            "error": msg
        }


def generate_product_insights(df, product_name):
    if df is None or df.empty:
        return {"success": False, "insights": "", "error": "No data"}

    if "product_name" not in df.columns:
        return {
            "success": False,
            "insights": "",
            "error": "product_name column missing"
        }

    product_df = df[df["product_name"] == product_name]

    if product_df.empty:
        return {
            "success": False,
            "insights": "",
            "error": f"No data for product: {product_name}"
        }

    return generate_business_insights(product_df, focus_area="products")


def generate_quick_summary(df):
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

        elif section == "key" and l:
            if l.startswith(("-", "•")) or l[0].isdigit():
                key_points.append(l.lstrip("-•0123456789. ").strip())

        elif section == "rec" and l:
            if l.startswith(("-", "•")) or l[0].isdigit():
                recommendations.append(l.lstrip("-•0123456789. ").strip())

    return {
        "insights": insights.strip() or text.strip(),
        "key_points": key_points if key_points else ["No key points generated"],
        "recommendations": recommendations if recommendations else ["No recommendations generated"]
    }
