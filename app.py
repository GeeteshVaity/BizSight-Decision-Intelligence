# =========================
# BizSight – Decision Intelligence
# =========================
from auth.auth import create_user_table, add_user, login_user
create_user_table()

from reports.pdf_report import generate_pdf_report
import streamlit as st
import pandas as pd
import time
import requests
from streamlit_lottie import st_lottie

def reset_app():
    keys_to_reset = [
        "data_loaded",
        "df",
        "ai_result",
        "simulated_df",
        "simulation_result",
        "rev_change",
        "cost_change",
        "pdf_ready",
        "pdf_bytes"
    ]

    for key in keys_to_reset:
        if key in st.session_state:
            st.session_state[key] = None if key != "data_loaded" else False

    st.rerun()



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
        "pdf_bytes": None,
        "authenticated": False,
        "username": None

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

st.markdown("""
<style>

/* ===== UNIVERSAL (BOTH THEMES) ===== */

.metric-box {
    padding: 20px;
    border-radius: 16px;
    transition: 0.25s ease;
}

.stButton>button {
    border-radius: 10px;
    font-weight: 600;
    transition: 0.25s ease;
}

/* ===== DARK MODE ===== */
@media (prefers-color-scheme: dark) {

    .metric-box {
        background: rgba(255,255,255,0.04);
        border: 1px solid rgba(255,255,255,0.08);
    }

    .stButton>button {
        background: linear-gradient(90deg, #10b981, #34d399);
        color: #020617;
    }

    .stButton>button:hover {
        box-shadow: 0 0 18px rgba(16,185,129,0.4);
        transform: scale(1.03);
    }
}

/* ===== LIGHT MODE ===== */
@media (prefers-color-scheme: light) {

    .metric-box {
        background: rgba(255,255,255,0.9);
        border: 1px solid #e5e7eb;
    }

    .stButton>button {
        background: linear-gradient(90deg, #2563eb, #3b82f6);
        color: white;
    }

    .stButton>button:hover {
        box-shadow: 0 0 16px rgba(37,99,235,0.35);
        transform: scale(1.03);
    }
}

</style>
""", unsafe_allow_html=True)



# ----------- Auth----------
if not st.session_state.authenticated:

    # ---- Centered Layout ----
    left, center, right = st.columns([1.5, 2, 1.5])

    with center:
        st.markdown("""
        <div style="
            padding: 40px;
            border-radius: 22px;
            backdrop-filter: blur(12px);
            background: rgba(255,255,255,0.06);
            border: 1px solid rgba(0,0,0,0.1);
        ">
        """, unsafe_allow_html=True)
        st.markdown("</div>", unsafe_allow_html=True)


            # ---- Auth Animation ----
        st_lottie(
            load_lottie("https://assets9.lottiefiles.com/packages/lf20_jcikwtux.json"),
            height=140,
            key="auth_animation"
        )



        st.markdown(
            "<h2 style='text-align:center;'> BizSight Access</h2>",
            unsafe_allow_html=True
        )
        st.caption("Secure decision intelligence for modern businesses")

        tab_login, tab_signup = st.tabs(["Login", "Sign Up"])

        # ================= LOGIN =================
        with tab_login:
            st.markdown("### Welcome back")

            username = st.text_input(
                "Username",
                placeholder="e.g. analyst_01",
                key="login_user"
            )

            password = st.text_input(
                "Password",
                type="password",
                placeholder="••••••••",
                key="login_pass"
            )

            remember = st.checkbox("Remember me")

            if st.button("Login", use_container_width=True):
                with st.spinner("Authenticating…"):
                    time.sleep(0.6)
                    user = login_user(username, password)

                if user:
                    st.session_state.authenticated = True
                    st.session_state.username = username
                    st.success("Login successful")
                    st.rerun()
                else:
                    st.error("Invalid username or password")

        # ================= SIGN UP =================
        with tab_signup:
            st.markdown("### Create a new account")

            new_user = st.text_input(
                "Choose a username",
                placeholder="unique username"
            )

            new_pass = st.text_input(
                "Choose a password",
                type="password",
                placeholder="min 6 characters"
            )

            st.caption("🔒 Passwords are securely encrypted")

            if st.button("Create Account", use_container_width=True):
                if len(new_pass) < 6:
                    st.warning("Password should be at least 6 characters")
                else:
                    try:
                        with st.spinner("Creating account…"):
                            time.sleep(0.6)
                            add_user(new_user, new_pass)

                        st.success("Account created! Please login.")
                    except:
                        st.error("Username already exists")

        st.markdown("</div>", unsafe_allow_html=True)
    st.stop()

# ------------------ Sidebar ------------------
with st.sidebar:

    st_lottie(
        load_lottie("https://assets9.lottiefiles.com/packages/lf20_qp1q7mct.json"),
        height=160
    )

    st.title("BizSight")

    # 🔐 USER INFO
    if st.session_state.get("authenticated", False):
        st.markdown(
            f"""
            <div style="
                background: rgba(16,185,129,0.12);
                padding: 12px;
                border-radius: 12px;
                border: 1px solid rgba(16,185,129,0.4);
                margin-bottom: 10px;
            ">
                👤 <b>{st.session_state.username}</b><br>
                <span style="font-size: 12px; opacity: 0.8;">
                Decision Analyst
                </span>
            </div>
            """,
            unsafe_allow_html=True
        )

        app_mode = st.radio(
            "Navigate",
            ["Dashboard", "Simulation", "AI Intelligence", "Reports"],
            label_visibility="collapsed"
        )

        st.divider()

        # 🚪 LOGOUT
        if st.button("Logout"):
            st.session_state.authenticated = False
            st.session_state.username = None
            st.session_state.data_loaded = False
            st.rerun()

    else:
        st.info("🔒 Please login to access BizSight")

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

        col1, col2 = st.columns([5, 1])
        with col2:
            if st.button("🔄 Reset Dataset", use_container_width=True):
                reset_app()


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
