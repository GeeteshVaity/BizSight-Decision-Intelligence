"""
BizSight - Insight Generator Module
File: intelligence/insight_generator.py
Author: Dhruv

This module generates AI-powered business insights using Google Gemini.
Analyzes data and provides natural language recommendations.
No prints, only returns.

Required DataFrame columns: date, product_name, quantity, selling_price, revenue, cost, profit
"""

import os
import json
from dotenv import load_dotenv
from google import genai

# Import other modules for data analysis
# These imports will be done inside functions to avoid circular dependencies
# and module path issues


# Load environment variables
load_dotenv()

# Configure Gemini API
GEMINI_API_KEY = os.getenv('GEMINI_API_KEY')

if GEMINI_API_KEY:
    # Initialize the client with API key
    client = genai.Client(api_key=GEMINI_API_KEY)
else:
    client = None
    print("Warning: GEMINI_API_KEY not found in .env file")


def generate_business_insights(df, focus_area='overall'):
    """
    Generate AI-powered business insights from data.
    
    Args:
        df (DataFrame): Business data
        focus_area (str): Area to focus on - 'overall', 'revenue', 'costs', 'products', 'risks'
        
    Returns:
        dict: {
            'success': bool,
            'insights': str (AI-generated insights),
            'key_points': list of str,
            'recommendations': list of str,
            'error': str (if any)
        }
    """
    if df is None or df.empty:
        return {
            'success': False,
            'insights': '',
            'key_points': [],
            'recommendations': [],
            'error': 'No data provided'
        }
    
    if not GEMINI_API_KEY:
        return {
            'success': False,
            'insights': '',
            'key_points': [],
            'recommendations': [],
            'error': 'API key not configured. Add GEMINI_API_KEY to .env file'
        }
    
    try:
        # Import here to avoid module path issues
        import sys
        import os
        # Add parent directory to path
        current_dir = os.path.dirname(os.path.abspath(__file__))
        parent_dir = os.path.dirname(current_dir)
        if parent_dir not in sys.path:
            sys.path.insert(0, parent_dir)
        
        from analysis.analyzer import get_all_metrics
        from analysis.trends import get_all_trends
        from intelligence.risk_detector import get_all_risks
        
        # Gather all analysis data
        metrics = get_all_metrics(df)
        trends = get_all_trends(df)
        risks = get_all_risks(df)
        
        # Prepare data summary for AI
        data_summary = _prepare_data_summary(metrics, trends, risks, focus_area)
        
        # Generate AI insights
        prompt = f"""
You are a business analyst AI. Analyze the following business data and provide actionable insights.

BUSINESS DATA:
{data_summary}

Focus Area: {focus_area}

Provide a comprehensive analysis including:
1. Key observations about business performance
2. Important trends and patterns
3. Risk areas that need attention
4. Specific actionable recommendations

Format your response as:
INSIGHTS: [Your detailed analysis here]

KEY POINTS:
- [Point 1]
- [Point 2]
- [Point 3]

RECOMMENDATIONS:
- [Recommendation 1]
- [Recommendation 2]
- [Recommendation 3]

Be specific, use numbers from the data, and focus on actionable advice.
"""
        
        response = client.models.generate_content(
            model='gemini-2.0-flash-exp',
            contents=prompt
        )
        insights_text = response.text
        
        # Parse the response
        parsed = _parse_ai_response(insights_text)
        
        return {
            'success': True,
            'insights': parsed['insights'],
            'key_points': parsed['key_points'],
            'recommendations': parsed['recommendations'],
            'error': None
        }
        
    except Exception as e:
        return {
            'success': False,
            'insights': '',
            'key_points': [],
            'recommendations': [],
            'error': str(e)
        }


def generate_product_insights(df, product_name):
    """
    Generate insights focused on a specific product.
    
    Args:
        df (DataFrame): Business data
        product_name (str): Name of product to analyze
        
    Returns:
        dict: AI-generated insights for the specific product
    """
    if df is None or df.empty:
        return {
            'success': False,
            'insights': '',
            'error': 'No data provided'
        }
    
    if 'product_name' not in df.columns:
        return {
            'success': False,
            'insights': '',
            'error': 'Product name column not found'
        }
    
    # Filter data for specific product
    product_df = df[df['product_name'] == product_name]
    
    if product_df.empty:
        return {
            'success': False,
            'insights': '',
            'error': f'No data found for product: {product_name}'
        }
    
    # Generate insights for this product
    return generate_business_insights(product_df, focus_area='products')


def generate_quick_summary(df):
    """
    Generate a quick one-paragraph business summary.
    
    Args:
        df (DataFrame): Business data
        
    Returns:
        dict: {
            'success': bool,
            'summary': str (brief summary),
            'error': str (if any)
        }
    """
    if df is None or df.empty:
        return {
            'success': False,
            'summary': '',
            'error': 'No data provided'
        }
    
    if not GEMINI_API_KEY:
        return {
            'success': False,
            'summary': '',
            'error': 'API key not configured'
        }
    
    try:
        # Import here to avoid module path issues
        import sys
        import os
        current_dir = os.path.dirname(os.path.abspath(__file__))
        parent_dir = os.path.dirname(current_dir)
        if parent_dir not in sys.path:
            sys.path.insert(0, parent_dir)
        
        from analysis.analyzer import get_all_metrics
        
        metrics = get_all_metrics(df)
        
        prompt = f"""
Summarize this business performance in 2-3 sentences:

Total Revenue: ${metrics['total_revenue']:,.2f}
Total Cost: ${metrics['total_cost']:,.2f}
Total Profit: ${metrics['total_profit']:,.2f}
Profit Margin: {metrics['profit_margin']:.2f}%

Number of Products: {len(metrics['product_summary'])}

Be concise and highlight the most important point.
"""
        
        response = client.models.generate_content(
            model='gemini-2.0-flash-exp',
            contents=prompt
        )
        
        return {
            'success': True,
            'summary': response.text.strip(),
            'error': None
        }
        
    except Exception as e:
        return {
            'success': False,
            'summary': '',
            'error': str(e)
        }


def _prepare_data_summary(metrics, trends, risks, focus_area):
    """
    Prepare a formatted summary of all data for AI.
    
    Args:
        metrics (dict): Business metrics
        trends (dict): Trend analysis
        risks (dict): Risk detection results
        focus_area (str): Area of focus
        
    Returns:
        str: Formatted data summary
    """
    summary = f"""
=== BUSINESS METRICS ===
Total Revenue: ${metrics['total_revenue']:,.2f}
Total Cost: ${metrics['total_cost']:,.2f}
Total Profit: ${metrics['total_profit']:,.2f}
Profit Margin: {metrics['profit_margin']:.2f}%

=== TRENDS ===
Revenue Trend: {trends['revenue_trend']['trend']} ({trends['revenue_trend']['change_percent']:.2f}%)
Profit Trend: {trends['profit_trend']['trend']} ({trends['profit_trend']['change_percent']:.2f}%)
Overall Growth Rate: {trends['overall_growth_rate']:.2f}%

=== PRODUCTS ===
"""
    
    for product, data in metrics['product_summary'].items():
        summary += f"{product}: Revenue=${data['revenue']:,.2f}, Profit=${data['profit']:,.2f}, Margin={data['margin']:.1f}%\n"
    
    summary += f"""
=== RISKS DETECTED ===
Total Risks: {risks['summary']['total_risks_detected']}
Overall Risk Level: {risks['summary']['overall_risk_level']}

"""
    
    if risks['continuous_losses']['risk_detected']:
        summary += f"⚠ Continuous Losses: {risks['continuous_losses']['message']}\n"
    
    if risks['declining_revenue']['risk_detected']:
        summary += f"⚠ Declining Revenue: {risks['declining_revenue']['message']}\n"
    
    if risks['low_profit_margin']['risk_detected']:
        summary += f"⚠ Low Profit Margin: {risks['low_profit_margin']['message']}\n"
    
    if risks['underperforming_products']['risk_detected']:
        summary += f"⚠ Underperforming Products: {risks['underperforming_products']['count']} products\n"
    
    return summary


def _parse_ai_response(response_text):
    """
    Parse AI response into structured format.
    
    Args:
        response_text (str): Raw AI response
        
    Returns:
        dict: Parsed insights, key points, and recommendations
    """
    insights = ""
    key_points = []
    recommendations = []
    
    # Split by sections
    sections = response_text.split('\n')
    current_section = None
    
    for line in sections:
        line = line.strip()
        
        if 'INSIGHTS:' in line.upper():
            current_section = 'insights'
            insights = line.replace('INSIGHTS:', '').strip()
        elif 'KEY POINTS:' in line.upper():
            current_section = 'key_points'
        elif 'RECOMMENDATIONS:' in line.upper():
            current_section = 'recommendations'
        elif line.startswith('-') or line.startswith('•'):
            point = line.lstrip('-•').strip()
            if current_section == 'key_points' and point:
                key_points.append(point)
            elif current_section == 'recommendations' and point:
                recommendations.append(point)
        elif current_section == 'insights' and line:
            insights += ' ' + line
    
    # If parsing failed, use entire response as insights
    if not insights:
        insights = response_text
    
    return {
        'insights': insights.strip(),
        'key_points': key_points if key_points else ['Analysis provided above'],
        'recommendations': recommendations if recommendations else ['Review the insights for guidance']
    }


def validate_ai_safety(insights_text):
    """
    Validate that AI-generated insights are safe and appropriate.
    Simple rule-based validation.
    
    Args:
        insights_text (str): AI-generated text
        
    Returns:
        dict: {
            'is_safe': bool,
            'issues': list of str (any issues found)
        }
    """
    issues = []
    
    # Check for empty response
    if not insights_text or len(insights_text.strip()) < 10:
        issues.append("Response too short or empty")
    
    # Check for inappropriate content (basic check)
    inappropriate_keywords = ['hack', 'illegal', 'fraud', 'scam']
    for keyword in inappropriate_keywords:
        if keyword in insights_text.lower():
            issues.append(f"Potentially inappropriate content detected: {keyword}")
    
    # Check if response is actually about business
    business_keywords = ['revenue', 'profit', 'cost', 'business', 'product', 'sales']
    has_business_content = any(keyword in insights_text.lower() for keyword in business_keywords)
    
    if not has_business_content:
        issues.append("Response doesn't appear to be business-related")
    
    is_safe = len(issues) == 0
    
    return {
        'is_safe': is_safe,
        'issues': issues
    }