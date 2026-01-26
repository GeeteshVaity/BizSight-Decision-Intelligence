import traceback
import streamlit as st

# ------------------ Imports ------------------
from core.data_loader import load_data
from core.data_mapper import map_to_internal_schema
from core.data_validator import validate_dataframe

from analysis.analyzer import (
    total_revenue, total_cost, total_profit, profit_margin
)

from intelligence.risk_detector import (
    detect_continuous_losses,
    detect_declining_revenue,
    detect_high_cost_ratio,
    detect_low_profit_margin
)

from intelligence.insight_generator import (
    generate_business_insights,
    generate_quick_summary
)

from simulation.simulator import simulate_changes
from simulation.comparator import compare_profit

from reports.report_generator import generate_report

from visualization.charts import (
    revenue_trend_chart,
    profit_by_product_chart,
    revenue_contribution_pie
)

# ------------------ Page Config ------------------
st.set_page_config(
    page_title="BizSight – Decision Intelligence",
    page_icon="📊",
    layout="centered"
)

# ------------------ Session State ------------------
def init_state():
    defaults = {
        "data_loaded": False,
        "df": None,
        "ai_result": None,
        "summary": None,
        "simulated_df": None,
        "simulation_result": None,
        "business_report": None,
        "rev_change": 0,
        "cost_change": 0
    }
    for k, v in defaults.items():
        if k not in st.session_state:
            st.session_state[k] = v

init_state()

# ------------------ Header ------------------
st.markdown(
    """
    <h1 style="text-align:center;">BizSight</h1>
    <p style="text-align:center; color:gray;">
    Business Decision Intelligence for Retail & FMCG
    </p>
    """,
    unsafe_allow_html=True
)

st.divider()

# ------------------ Upload ------------------
uploaded_file = st.file_uploader(
    "Upload CSV file",
    type=["csv"]
)

col1, col2 = st.columns(2)
analyze = col1.button("🔍 Analyze", disabled=uploaded_file is None)
reset = col2.button("♻ Reset")

if reset:
    st.session_state.clear()
    st.rerun()

# ------------------ Analyze (LOAD DATA) ------------------
if analyze and uploaded_file:
    try:
        with st.spinner("Processing data..."):
            raw_df = load_data(uploaded_file)
            mapped_df = map_to_internal_schema(raw_df)
            df = validate_dataframe(mapped_df)

            df["profit"] = df["revenue"] - df["cost"]

            st.session_state.df = df
            st.session_state.data_loaded = True
            st.session_state.ai_result = None
            st.session_state.summary = None
            st.session_state.simulated_df = None
            st.session_state.simulation_result = None
            st.session_state.business_report = None

        st.success("Data loaded successfully")

    except Exception:
        st.error("Failed to process data")
        st.text(traceback.format_exc())

# ================== MAIN APP ==================
if st.session_state.data_loaded:
    df = st.session_state.df

    # ------------------ Metrics ------------------
    st.divider()
    st.markdown("### 📈 Business Performance")

    c1, c2, c3, c4 = st.columns(4)
    c1.metric("Revenue", f"₹ {total_revenue(df):,.0f}")
    c2.metric("Cost", f"₹ {total_cost(df):,.0f}")
    c3.metric("Profit", f"₹ {total_profit(df):,.0f}")
    c4.metric("Margin", f"{profit_margin(df):.2f}%")

    # ------------------ Risk Analysis ------------------
    st.divider()
    st.markdown("### ⚠️ Risk Analysis")

    risks = [
        detect_continuous_losses(df),
        detect_declining_revenue(df),
        detect_high_cost_ratio(df),
        detect_low_profit_margin(df)
    ]

    for r in risks:
        if r["risk_detected"]:
            st.warning(r["message"])
        else:
            st.success(r["message"])

    # ------------------ What-If Simulator ------------------
    st.divider()
    st.markdown("### 🧪 What-If Simulator")

    st.session_state.rev_change = st.slider(
        "Revenue Change (%)", -50, 50, st.session_state.rev_change
    )
    st.session_state.cost_change = st.slider(
        "Cost Change (%)", -50, 50, st.session_state.cost_change
    )

    if st.button("▶ Run Simulation"):
        st.session_state.simulated_df = simulate_changes(
            df,
            st.session_state.rev_change,
            st.session_state.cost_change
        )
        st.session_state.simulation_result = compare_profit(
            df,
            st.session_state.simulated_df
        )

    if st.session_state.simulation_result:
        r = st.session_state.simulation_result
        st.metric("Profit Impact", f"₹ {r['difference']:,.0f}")

    # ------------------ AI Insights ------------------
    st.divider()
    st.markdown("### 🤖 AI Insights (Gemini Flash Lite)")

    if st.session_state.ai_result is None:
        with st.spinner("Generating AI insights..."):
            st.session_state.ai_result = generate_business_insights(df)
            st.session_state.summary = generate_quick_summary(df)

    ai = st.session_state.ai_result

    if ai["success"]:
        st.info(st.session_state.summary["summary"])
        st.write(ai["insights"])

        st.markdown("**Key Points**")
        for p in ai["key_points"]:
            st.markdown(f"- {p}")

        st.markdown("**Recommendations**")
        for r in ai["recommendations"]:
            st.markdown(f"- {r}")
    else:
        st.warning("AI unavailable (quota / billing limitation)")

    # ------------------ Report ------------------
    st.divider()
    st.markdown("### 📝 Business Report")

    if st.button("📄 Generate Report"):
        st.session_state.business_report = generate_report(
            metrics={
                "Revenue": total_revenue(df),
                "Cost": total_cost(df),
                "Profit": total_profit(df),
                "Margin": profit_margin(df)
            },
            risks=[r["message"] for r in risks if r["risk_detected"]],
            ai_insights=ai["insights"] if ai["success"] else "AI unavailable"
        )

    if st.session_state.business_report:
        st.text(st.session_state.business_report)

    # ------------------ Charts ------------------
    st.divider()
    st.markdown("### 📊 Visual Insights")

    st.pyplot(revenue_trend_chart(df))
    st.pyplot(profit_by_product_chart(df))
    st.pyplot(revenue_contribution_pie(df))

# ------------------ Footer ------------------
st.divider()
st.caption("BizSight © 2026 | Decision Intelligence System")
