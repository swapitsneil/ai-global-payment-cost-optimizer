"""
AI Global Payment & Cost Optimizer - Streamlit UI

This file contains the main user interface for the payment optimizer application.
It handles user input, displays payment comparisons, and shows AI-powered recommendations.
"""

import streamlit as st
import pandas as pd
from calculator import (
    calculate_fixed_fee,
    calculate_percentage_fee,
    calculate_fx_markup,
    calculate_total_fee,
    calculate_net_received,
)


# Data Loading

def load_payment_data():
    """Load and normalize payment methods data from CSV."""
    df = pd.read_csv("data/payment_methods.csv")

    # Normalize text columns safely
    for col in ["sender_country", "receiver_country", "platform"]:
        df[col] = df[col].astype(str).str.strip()

    # Normalize supported column (prevents .str errors)
    df["supported"] = df["supported"].astype(str).str.strip().str.lower()

    return df



# Filtering Logic

def filter_payment_options(df, sender_country, receiver_country):
    """Filter payment options based on sender, receiver, and supported status."""
    sender_country = sender_country.strip()
    receiver_country = receiver_country.strip()

    filtered = df[
        (df["sender_country"] == sender_country)
        & (df["receiver_country"] == receiver_country)
        & (df["supported"] == "true")
    ].copy()

    return filtered


# Cost Calculations
def calculate_payment_costs(df, amount):
    """Calculate fees, FX loss, and net received for each platform."""
    results = []

    for _, row in df.iterrows():
        fixed_fee = calculate_fixed_fee(amount, row["fixed_fee"])
        percentage_fee = calculate_percentage_fee(amount, row["percentage_fee"])
        total_fee = calculate_total_fee(fixed_fee, percentage_fee)

        fx_loss = calculate_fx_markup(amount, row["fx_markup_percent"])
        net_received = calculate_net_received(amount, total_fee, fx_loss)

        results.append({
            "platform": row["platform"],
            "total_fee": round(total_fee, 2),
            "fx_loss": round(fx_loss, 2),
            "net_received": round(net_received, 2),
            "settlement_time_days": row["settlement_time_days"],
        })

    return pd.DataFrame(results)



# Main App

def main():
    st.title("🌍 AI Global Payment & Cost Optimizer")
    st.markdown("**Find the smartest way to send money internationally**")

    # User Inputs
    st.header("📋 Payment Details")

    sender_country = st.text_input("🌎 Sender Country", "USA")
    receiver_country = st.text_input("🌍 Receiver Country", "UK")
    amount = st.number_input(
        "💰 Amount (USD)",
        min_value=0.01,
        value=1000.0,
        step=0.01
    )

    if st.button("Compare Payment Options"):
        try:
            payment_data = load_payment_data()
            filtered_options = filter_payment_options(
                payment_data, sender_country, receiver_country
            )

            if filtered_options.empty:
                st.warning(
                    f"No supported payment platforms found for {sender_country} → {receiver_country}."
                )
                return

            # Calculate results
            results_df = calculate_payment_costs(filtered_options, amount)

            # Display comparison table
            st.header("📊 Payment Comparison")
            st.dataframe(results_df, use_container_width=True)

            # -------------------------
            # AI Recommendation
            # -------------------------
            from ai_engine import get_ai_recommendation

            try:
                best_platform, explanation = get_ai_recommendation(results_df)

                # Normalize explanation spacing (fixes glued words)
                explanation = " ".join(explanation.split())

                best_option = results_df[
                    results_df["platform"] == best_platform
                ].iloc[0]

                other_options = results_df[
                    results_df["platform"] != best_platform
                ]

                # Safe savings calculation
                if not other_options.empty:
                    avg_other_net = other_options["net_received"].mean()
                    savings = best_option["net_received"] - avg_other_net
                    savings_text = f"💰 Estimated savings: ${savings:.2f}"
                else:
                    savings_text = "💰 This is the only available option"

                st.header("🤖 AI Recommendation")
                st.success(f"🏆 Best Platform: {best_platform}")
                st.info(savings_text)

                # Clean, wrapped explanation box
                st.subheader("🧠 Recommendation")
                st.markdown(
                    f"""
                    <div style="
                        background-color: #1f2933;
                        padding: 16px;
                        border-radius: 8px;
                        line-height: 1.6;
                        font-size: 15px;
                        color: #e5e7eb;
                        white-space: normal;
                        word-wrap: break-word;
                    ">
                    {explanation}
                    </div>
                    """,
                    unsafe_allow_html=True
                )

            except Exception:
                # Fallback if AI fails
                best_row = results_df.loc[results_df["net_received"].idxmax()]
                st.header("🤖 AI Recommendation")
                st.warning("AI recommendation unavailable. Showing best option based on calculations.")
                st.success(f"🏆 Best Platform: {best_row['platform']}")
                st.info(f"Net received: ${best_row['net_received']:.2f}")

        except Exception as e:
            st.error(f"An error occurred: {str(e)}")


if __name__ == "__main__":
    main()
