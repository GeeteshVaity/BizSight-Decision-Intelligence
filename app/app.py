import sys
import os
import streamlit as st

# --------------------------------------------------
# Add project root to Python path
# --------------------------------------------------
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

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
