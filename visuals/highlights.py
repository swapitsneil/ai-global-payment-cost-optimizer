import streamlit as st


def show_savings_highlight(results_df):
    """
    Highlights cheapest platform and savings compared to next best
    """

    if results_df.shape[0] < 2:
        return

    df = results_df.copy()
    df["total_cost"] = df["total_fee"] + df["fx_loss"]

    df_sorted = df.sort_values("total_cost")

    best = df_sorted.iloc[0]
    second_best = df_sorted.iloc[1]

    savings = second_best["total_cost"] - best["total_cost"]
    savings_pct = (savings / second_best["total_cost"]) * 100

    st.success(
        f"💰 **Cheapest Option: {best['platform']}**\n\n"
        f"You save **${savings:.2f} ({savings_pct:.1f}%)** "
        f"compared to the next best alternative."
    )
