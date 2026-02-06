# =========================
# BizSight – Decision Intelligence
# =========================
from reports.pdf_report import generate_pdf_report
import streamlit as st
import pandas as pd
import time
import requests
from streamlit_lottie import st_lottie


def save_charts_to_images(df):
    charts = {
        "revenue.png": revenue_trend_chart(df),
        "profit.png": profit_by_product_chart(df),
        "pie.png": revenue_contribution_pie(df)
    }

    images = {}
    for name, fig in charts.items():
        images[name] = fig.to_image(format="png")

    return images


# ------------------ Page Config ------------------
st.set_page_config(
    page_title="BizSight – Decision Intelligence",
    page_icon="📊",
    layout="wide",
    initial_sidebar_state="expanded"
)

# ------------------ Session State ------------------
def init_state():
    defaults = {
        "data_loaded": False,
        "df": None,
        "ai_result": None,
        "simulated_df": None,
        "simulation_result": None,
        "rev_change": 0,
        "cost_change": 0,
        "pdf_ready": False,
        "pdf_bytes": None
    }
    for k, v in defaults.items():
        if k not in st.session_state:
            st.session_state[k] = v

init_state()

# ------------------ Backend Imports ------------------
from core.data_loader import load_data
from core.data_mapper import map_to_internal_schema
from core.data_validator import validate_dataframe

from analysis.analyzer import (
    total_revenue, total_cost, total_profit, profit_margin
)

from simulation.simulator import simulate_changes
from simulation.comparator import compare_profit

from intelligence.insight_generator import generate_business_insights

from reports.report_generator import generate_report

from visualization.charts import (
    revenue_trend_chart,
    profit_by_product_chart,
    revenue_contribution_pie
)

# ------------------ Lottie Loader ------------------
def load_lottie(url):
    r = requests.get(url)
    return r.json() if r.status_code == 200 else None

# ------------------ Global Styling ------------------
st.markdown("""
<style>
.stApp {
    background: radial-gradient(circle at top, #020617, #020617);
    color: #e5e7eb;
}
[data-testid="stSidebar"] {
    background: linear-gradient(180deg, #020617, #020617);
    border-right: 1px solid #1f2937;
}
.stButton>button {
    background: linear-gradient(90deg, #10b981, #34d399);
    color: black;
    border-radius: 10px;
    font-weight: 700;
    transition: 0.3s;
}
.stButton>button:hover {
    transform: scale(1.03);
    box-shadow: 0 0 25px rgba(16,185,129,0.5);
}
.metric-box {
    background: rgba(255,255,255,0.04);
    padding: 20px;
    border-radius: 15px;
    border: 1px solid rgba(255,255,255,0.08);
}
</style>
""", unsafe_allow_html=True)

# ------------------ Sidebar ------------------
with st.sidebar:
    st_lottie(load_lottie("https://assets9.lottiefiles.com/packages/lf20_qp1q7mct.json"), height=160)
    st.title("BizSight")
    app_mode = st.radio(
        "Navigate",
        ["Dashboard", "Simulation", "AI Intelligence", "Reports"],
        label_visibility="collapsed"
    )
    st.divider()
    st.caption("System Status: 🟢 Operational")

# ------------------ Header ------------------
c1, c2 = st.columns([4, 1])
with c1:
    st.title("BizSight – Decision Intelligence")
    st.caption("Retail & FMCG Analytics · AI-Powered · Real-Time")
with c2:
    st.markdown("🟢 **LIVE DATA**")

# =========================
# DATA UPLOAD
# =========================
if not st.session_state.data_loaded:
    st.markdown("## 📤 Initialize Dataset")
    uploaded_file = st.file_uploader("Upload CSV", type=["csv"])

    if uploaded_file and st.button("🚀 Start Analysis"):
        with st.status("Booting Intelligence Engine...", expanded=True):
            time.sleep(0.6)
            raw = load_data(uploaded_file)
            mapped = map_to_internal_schema(raw)
            df = validate_dataframe(mapped)
            df["profit"] = df["revenue"] - df["cost"]
            st.session_state.df = df
            st.session_state.data_loaded = True
            st.success("System Ready 🚀")
        st.rerun()

# =========================
# MAIN APP
# =========================
if st.session_state.data_loaded:
    df = st.session_state.df

    # ------------------ DASHBOARD ------------------
    if app_mode == "Dashboard":
        st.markdown("## 📊 Business Snapshot")

        m1, m2, m3, m4 = st.columns(4)
        m1.metric("Revenue", f"₹ {total_revenue(df):,.0f}", "+12%")
        m2.metric("Cost", f"₹ {total_cost(df):,.0f}", "-4%")
        m3.metric("Profit", f"₹ {total_profit(df):,.0f}", "+18%")
        m4.metric("Margin", f"{profit_margin(df):.2f}%", "+1.2%")

        st.divider()

        t1, t2 = st.tabs(["Revenue Flow", "Product Intelligence"])
        with t1:
            st.plotly_chart(revenue_trend_chart(df), use_container_width=True)
        with t2:
            a, b = st.columns(2)
            a.plotly_chart(revenue_contribution_pie(df), use_container_width=True)
            b.plotly_chart(profit_by_product_chart(df), use_container_width=True)

    # ------------------ SIMULATION ------------------
    elif app_mode == "Simulation":
        st.markdown("## 🔮 What-If Simulator")

        c1, c2 = st.columns([1, 2])
        with c1:
            st.session_state.rev_change = st.select_slider(
                "Revenue Change (%)", options=range(-50, 55, 5), value=0
            )
            st.session_state.cost_change = st.select_slider(
                "Cost Change (%)", options=range(-50, 55, 5), value=0
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

        with c2:
            if st.session_state.simulation_result:
                r = st.session_state.simulation_result
                st.metric(
                    "Projected Profit Impact",
                    f"₹ {r['difference']:,.0f}",
                    delta=f"{st.session_state.rev_change}%"
                )
                st.area_chart(
                    st.session_state.simulated_df.groupby("date")["revenue"].sum()
                )

    # ------------------ AI INTELLIGENCE ------------------
    elif app_mode == "AI Intelligence":
        st.markdown("## 🧠 AI Decision Support")

        if st.button("✨ Generate AI Insights"):
            with st.spinner("AI is thinking..."):
                st.session_state.ai_result = generate_business_insights(df)
                st.balloons()

        if st.session_state.ai_result:
            ai = st.session_state.ai_result
            st.chat_message("assistant").write(
                ai.get("insights", "No insights available")
            )

            with st.expander("📌 Strategic Recommendations"):
                for r in ai.get("recommendations", []):
                    st.markdown(f"✅ {r}")

    # ------------------ REPORTS ------------------
    elif app_mode == "Reports":
        st.markdown("## 📑 Business Reports")

        # -------- TEXT REPORT --------
        if st.button("📄 Generate Executive Summary"):
            report = generate_report(
                metrics={
                    "Revenue": total_revenue(df),
                    "Cost": total_cost(df),
                    "Profit": total_profit(df),
                    "Margin": profit_margin(df)
                },
                risks=[],
                ai_insights=(
                    st.session_state.ai_result.get("insights")
                    if st.session_state.ai_result else
                    "AI insights not generated."
                )
            )
            st.text(report)

        st.divider()

        # -------- PDF REPORT --------
        if st.button("⬇ Generate Full PDF Report"):
            progress = st.progress(0)
            status = st.empty()

            with st.spinner("Building executive-grade PDF..."):
                status.info("Rendering charts…")
                progress.progress(30)

                chart_images = save_charts_to_images(df)

                status.info("Compiling document…")
                progress.progress(65)

                st.session_state.pdf_bytes = generate_pdf_report(
                    metrics={
                        "Revenue": total_revenue(df),
                        "Cost": total_cost(df),
                        "Profit": total_profit(df),
                        "Margin": f"{profit_margin(df):.2f}%"
                    },
                    risks=[],
                    ai_insights=(
                        st.session_state.ai_result.get("insights")
                        if st.session_state.ai_result else
                        "AI insights not generated."
                    ),
                    chart_files=chart_images
                )

                progress.progress(100)
                status.success("✅ PDF Ready!")
                st.session_state.pdf_ready = True

        if st.session_state.pdf_ready:
            st.download_button(
                label="📥 Download BizSight PDF",
                data=st.session_state.pdf_bytes,
                file_name="BizSight_Report.pdf",
                mime="application/pdf"
            )


# ------------------ FOOTER ------------------
st.divider()
st.caption("BizSight © 2026 · Built for decision-makers, not dashboards.")
