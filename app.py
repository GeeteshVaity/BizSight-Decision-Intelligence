import sys
import os
import traceback
import streamlit as st

from core.data_mapper import map_to_internal_schema

from intellligence.risk_detector import (
    detect_continuous_losses,
    detect_declining_revenue,
    detect_high_cost_ratio,
    detect_low_profit_margin,
    detect_underperforming_products
)

from intellligence.insight_generator import (
    generate_business_insights,
    generate_product_insights,
    generate_quick_summary
)



from analysis.analyzer import (
    total_revenue,
    total_cost,
    total_profit,
    profit_margin
)

from visualization.charts import (
    revenue_trend_chart,
    profit_by_product_chart,
    revenue_contribution_pie
)

from analysis.trends import (
    revenue_trend,
    profit_trend,
    growth_rate,
    detect_consecutive_losses
)




# Add project root to Python path
PROJECT_ROOT = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))
if PROJECT_ROOT not in sys.path:
    sys.path.insert(0, PROJECT_ROOT)

from core.data_loader import load_data
from core.data_validator import validate_dataframe


def main():
    # --------------------------------------------------
    # Session state (for uploader reset)
    # --------------------------------------------------
    if "uploader_key" not in st.session_state:
        st.session_state.uploader_key = 0

    # --------------------------------------------------
    # App Configuration
    # --------------------------------------------------
    st.set_page_config(
        page_title="BizSight – Decision Intelligence",
        page_icon="📊",
        layout="centered"
    )

    # --------------------------------------------------
    # Header Section
    # --------------------------------------------------
    st.markdown(
        """
        <h1 style="text-align:center;">BizSight</h1>
        <p style="text-align:center; color:gray;">
        Business Decision Intelligence for Retail & FMCG Companies
        </p>
        """,
        unsafe_allow_html=True
    )

    st.divider()

    # --------------------------------------------------
    # Instructions
    # --------------------------------------------------
    st.markdown(
        """
        ### 📁 Upload Business Data
        Upload a CSV file containing monthly product-wise business data.
        
        **Required columns:**
        - `date`
        - `product`
        - `revenue`
        - `cost`
        """
    )

    # --------------------------------------------------
    # File Upload
    # --------------------------------------------------
    uploaded_file = st.file_uploader(
        "Select CSV file",
        type=["csv"],
        key=f"csv_uploader_{st.session_state.uploader_key}"
    )

    # --------------------------------------------------
    # Action Buttons
    # --------------------------------------------------
    col1, col2 = st.columns(2)

    with col1:
        analyze_btn = st.button(
            "🔍 Analyze",
            width='stretch',
            disabled=uploaded_file is None
        )

    with col2:
        reset_btn = st.button(
            "♻ Reset",
           width='stretch'
        )

    # --------------------------------------------------
    # Reset Logic
    # --------------------------------------------------
    if reset_btn:
        st.session_state.uploader_key += 1
        st.rerun()

    # --------------------------------------------------
    # Core Logic
    # --------------------------------------------------
    if uploaded_file is not None and analyze_btn:
        try:
            with st.spinner("Validating and processing data..."):
                
                df = load_data(uploaded_file)
                raw_df = load_data(uploaded_file)
                if raw_df is None or raw_df.empty:
                    st.error("No valid data to analyze")
                    st.stop()

                mapped_df = map_to_internal_schema(raw_df)
                df = validate_dataframe(mapped_df)

                df["profit"] = df["revenue"] - df["cost"]

            st.success("Data loaded and validated successfully")

            # --------------------------------------------------
            # Business Metrics
            # --------------------------------------------------
            st.markdown("### 📈 Business Performance Summary")
            
            col1, col2, col3, col4 = st.columns(4)
            
            with col1:
                st.metric(
                    label="Total Revenue",
                    value=f"₹ {total_revenue(df):,.0f}"
                )
            
            with col2:
                st.metric(
                    label="Total Cost",
                    value=f"₹ {total_cost(df):,.0f}"
                )
            
            with col3:
                profit = total_profit(df)
                st.metric(
                    label="Total Profit",
                    value=f"₹ {profit:,.0f}",
                    delta="Profit" if profit >= 0 else "Loss"
                )
            
            with col4:
                st.metric(
                    label="Profit Margin",
                    value=f"{profit_margin(df):.2f} %"
                )
            

            st.markdown("### 🔎 Data Preview")
            st.dataframe(df.head(), width='stretch')

            st.caption(
                "Showing first 5 rows of the uploaded dataset."
            )

        except Exception as e:
            st.error("❌ Something went wrong")
            st.error(str(e))
            st.text(traceback.format_exc())

        # --------------------------------------------------
        # Trend Insights
        # --------------------------------------------------
        st.divider()
        st.markdown("### 📉 Trend Insights")
        
        rev_trend = revenue_trend(df)
        prof_trend = profit_trend(df)
        overall_growth = growth_rate(df, "overall")
        loss_info = detect_consecutive_losses(df)
        
        col1, col2, col3 = st.columns(3)
        
        with col1:
            st.metric(
                label="Revenue Trend",
                value=rev_trend["trend"].capitalize(),
                delta=f"{rev_trend['change_percent']:.2f}%"
            )
        
        with col2:
            st.metric(
                label="Profit Trend",
                value=prof_trend["trend"].capitalize(),
                delta=f"{prof_trend['change_percent']:.2f}%"
            )
        
        with col3:
            st.metric(
                label="Overall Growth Rate",
                value=f"{overall_growth:.2f}%"
            )
        
        # --------------------------------------------------
        # Risk Analysis
        # --------------------------------------------------
        st.divider()
        st.markdown("### ⚠️ Risk Analysis")

        risk1 = detect_continuous_losses(df)
        risk2 = detect_declining_revenue(df)
        risk3 = detect_high_cost_ratio(df)
        risk4 = detect_low_profit_margin(df)
        risk5 = detect_underperforming_products(df)

        # Helper to display risk messages
        def show_risk(risk):
            if risk["risk_detected"]:
                if risk.get("severity") == "high":
                    st.error("🚨 " + risk["message"])
                elif risk.get("severity") == "medium":
                    st.warning("⚠️ " + risk["message"])
                else:
                    st.info("ℹ️ " + risk["message"])
            else:
                st.success("✅ " + risk["message"])

        show_risk(risk1)
        show_risk(risk2)
        show_risk(risk3)
        show_risk(risk4)

        # --------------------------------------------------
        # Underperforming Products (Table)
        # --------------------------------------------------
        if risk5["risk_detected"]:
            st.markdown("#### 🔻 Underperforming Products")

            under_df = pd.DataFrame(risk5["underperforming_products"])
            under_df["profit_margin"] = under_df["profit_margin"].round(2)

            st.dataframe(
                under_df,
                use_container_width=True
            )
        else:
            st.success("✅ No underperforming products detected.")

        

    # --------------------------------------------------
    # Visualization 
    # --------------------------------------------------
    if uploaded_file is not None and analyze_btn:
        st.divider()
        st.markdown("### 📊 Visual Insights")

        # Create two columns
        col1, col2 = st.columns(2)

        with col1:
            try:
                plt_obj = revenue_trend_chart(df)
                st.pyplot(plt_obj)
                plt_obj.clf()
            except Exception as e:
                st.warning(f"Unable to render revenue trend chart: {e}")

        with col2:
            try:
                plt_obj = profit_by_product_chart(df)
                st.pyplot(plt_obj)
                plt_obj.clf()
            except Exception as e:
                st.warning(f"Unable to render profit by product chart: {e}")

        # Pie chart below (full width)
        try:
            plt_obj = revenue_contribution_pie(df)
            st.pyplot(plt_obj)
            plt_obj.clf()
        except Exception as e:
            st.warning(f"Unable to render revenue contribution pie: {e}")



    # --------------------------------------------------
    # Footer
    # --------------------------------------------------
    st.divider()
    st.caption(
        "BizSight © 2026 | Business Decision Intelligence System"
    )


if __name__ == "__main__":
    main()
