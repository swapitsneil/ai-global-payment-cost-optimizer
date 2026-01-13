import streamlit as st
import pandas as pd


def show_fx_volatility_chart(sender_currency, receiver_currency):
    """
    Displays FX rate trend and volatility
    """

    fx_df = pd.read_csv("data/historical_fx.csv", parse_dates=["date"])

    fx_pair = fx_df[
        (fx_df["base_currency"] == sender_currency)
        & (fx_df["target_currency"] == receiver_currency)
    ]

    if fx_pair.empty:
        st.info("No FX history available for this corridor")
        return

    st.subheader("📈 FX Rate Trend & Volatility")

    st.line_chart(
        fx_pair.set_index("date")[["avg_rate"]]
    )

    avg_vol = fx_pair["volatility_index"].mean()

    if avg_vol > 0.25:
        st.warning("⚠️ High FX volatility detected — costs may fluctuate")
    elif avg_vol > 0.15:
        st.info("ℹ️ Moderate FX volatility")
    else:
        st.success("✅ FX rates relatively stable")
