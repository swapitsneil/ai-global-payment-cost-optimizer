import streamlit as st


def show_cost_comparison(results_df):
    """
    Displays bar chart comparing total cost (fees + FX loss)
    """

    if results_df.empty:
        return

    df = results_df.copy()
    df["total_cost"] = df["total_fee"] + df["fx_loss"]

    st.subheader("📊 Total Cost Comparison")

    chart_data = df.set_index("platform")["total_cost"]

    st.bar_chart(chart_data)

    st.caption("Lower bar = cheaper overall transfer")
