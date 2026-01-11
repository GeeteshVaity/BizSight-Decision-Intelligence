import sys
import os
import streamlit as st

from analysis.analyzer import (
    total_revenue,
    total_cost,
    total_profit,
    profit_margin
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
            use_container_width=True,
            disabled=uploaded_file is None
        )

    with col2:
        reset_btn = st.button(
            "♻ Reset",
            use_container_width=True
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
                df = validate_dataframe(df)

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
            st.dataframe(df.head(), use_container_width=True)

            st.caption(
                "Showing first 5 rows of the uploaded dataset."
            )

        except Exception as e:
            st.error(f"❌ {e}")

    # --------------------------------------------------
    # Footer
    # --------------------------------------------------
    st.divider()
    st.caption(
        "BizSight © 2026 | Business Decision Intelligence System"
    )


if __name__ == "__main__":
    main()
