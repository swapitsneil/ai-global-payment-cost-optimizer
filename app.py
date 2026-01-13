"""
AI Global Payment & Cost Optimizer - Streamlit UI
"""

import streamlit as st
import pandas as pd

from calculator import (
    calculate_fixed_fee,
    calculate_percentage_fee,
    calculate_fx_markup,
    calculate_total_fee,
    calculate_net_received,
    calculate_total_cost,
    calculate_score,
)

from visuals.charts import show_cost_comparison
from visuals.highlights import show_savings_highlight
from visuals.fx_charts import show_fx_volatility_chart

from simulator.scenario import run_scenario_simulation
from preferences.weights import get_preference_weights
from ai_engine import get_ai_recommendation


# -----------------------
# Data Loading
# -----------------------

def load_payment_data():
    df = pd.read_csv("data/payment_methods.csv")

    for col in ["sender_country", "receiver_country", "platform"]:
        df[col] = df[col].astype(str).str.strip()

    df["supported"] = df["supported"].astype(str).str.strip().str.lower()
    return df


# -----------------------
# Filtering Logic
# -----------------------

def filter_payment_options(df, sender_country, receiver_country):
    return df[
        (df["sender_country"] == sender_country.strip())
        & (df["receiver_country"] == receiver_country.strip())
        & (df["supported"] == "true")
    ].copy()


# -----------------------
# Cost Calculations
# -----------------------

def calculate_payment_costs(df, amount):
    results = []

    for _, row in df.iterrows():
        fixed_fee = calculate_fixed_fee(amount, row["fixed_fee"])
        percentage_fee = calculate_percentage_fee(amount, row["percentage_fee"])
        total_fee = calculate_total_fee(fixed_fee, percentage_fee)

        fx_loss = calculate_fx_markup(amount, row["fx_markup_percent"])
        net_received = calculate_net_received(amount, total_fee, fx_loss)
        total_cost = calculate_total_cost(total_fee, fx_loss)

        results.append({
            "platform": row["platform"],
            "total_fee": round(total_fee, 2),
            "fx_loss": round(fx_loss, 2),
            "total_cost": round(total_cost, 2),
            "net_received": round(net_received, 2),
            "settlement_time_days": row["settlement_time_days"],
            "currency_sent": row["currency_sent"],
            "currency_received": row["currency_received"],
        })

    return pd.DataFrame(results)


# -----------------------
# Main App
# -----------------------

def main():
    st.title("🌍 AI Global Payment & Cost Optimizer")
    st.markdown("**Find the smartest way to send money internationally**")

    st.header("📋 Payment Details")

    sender_country = st.text_input("🌎 Sender Country", "USA")
    receiver_country = st.text_input("🌍 Receiver Country", "UK")
    amount = st.number_input("💰 Amount (USD)", min_value=0.01, value=1000.0)

    preference = st.selectbox(
        "🎯 What matters most to you?",
        ["Balanced", "Cheapest", "Fastest"]
    )

    if st.button("Compare Payment Options"):
        payment_data = load_payment_data()
        filtered = filter_payment_options(
            payment_data, sender_country, receiver_country
        )

        if filtered.empty:
            st.warning("No supported platforms for this corridor")
            return

        results_df = calculate_payment_costs(filtered, amount)

        # -----------------------
        # Preference-based Scoring
        # -----------------------

        weights = get_preference_weights(preference)

        results_df["score"] = results_df.apply(
            lambda row: calculate_score(
                net_received=row["net_received"],
                total_cost=row["total_cost"],
                settlement_time_days=row["settlement_time_days"],
                weights=weights
            ),
            axis=1
        )

        results_df = results_df.sort_values("score", ascending=False)

        # -----------------------
        # Display Results
        # -----------------------

        st.header("📊 Payment Comparison")
        st.dataframe(results_df, use_container_width=True)

        show_cost_comparison(results_df)
        show_savings_highlight(results_df)

        # -----------------------
        # FX Volatility Insight
        # -----------------------

        show_fx_volatility_chart(
            results_df.iloc[0]["currency_sent"],
            results_df.iloc[0]["currency_received"],
        )

        # -----------------------
        # AI Recommendation
        # -----------------------

        best_platform, explanation = get_ai_recommendation(results_df)

        best_row = results_df.iloc[0]

        st.header("🤖 AI Recommendation")
        st.success(f"🏆 Recommended Platform: {best_platform}")
        st.info(
            f"Net received: ${best_row['net_received']:.2f} | "
            f"Total cost: ${best_row['total_cost']:.2f} | "
            f"Settlement: {best_row['settlement_time_days']} days"
        )

        st.subheader("🧠 Why this option?")
        st.markdown(
            f"""
            <div style="
                background-color:#1f2933;
                padding:16px;
                border-radius:8px;
                color:#e5e7eb;
                line-height:1.6;
            ">
            {explanation}
            </div>
            """,
            unsafe_allow_html=True
        )

        # -----------------------
        # Scenario Simulator
        # -----------------------

        st.header("🔮 What-If Scenario Simulation")

        amounts = st.multiselect(
            "Simulate for different transfer amounts",
            [500, 1000, 2500, 5000],
            default=[500, 1000, 5000]
        )

        scenario_df = run_scenario_simulation(filtered, amounts)
        st.dataframe(scenario_df, use_container_width=True)


if __name__ == "__main__":
    main()
