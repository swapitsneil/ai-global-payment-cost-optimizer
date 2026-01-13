"""
Scenario Simulator with FX Volatility Awareness
"""

import pandas as pd
from calculator import (
    calculate_fixed_fee,
    calculate_percentage_fee,
    calculate_fx_markup,
    calculate_total_fee,
    calculate_net_received,
    calculate_total_cost,
)


def load_fx_history():
    """
    Loads historical FX data
    """
    return pd.read_csv("data/historical_fx.csv", parse_dates=["date"])


def run_scenario_simulation(payment_df, amounts):
    """
    Runs what-if analysis across multiple transfer amounts
    """

    fx_history = load_fx_history()
    scenario_results = []

    for amount in amounts:
        for _, row in payment_df.iterrows():
            fixed_fee = calculate_fixed_fee(amount, row["fixed_fee"])
            percentage_fee = calculate_percentage_fee(amount, row["percentage_fee"])
            total_fee = calculate_total_fee(fixed_fee, percentage_fee)

            fx_loss = calculate_fx_markup(amount, row["fx_markup_percent"])
            net_received = calculate_net_received(amount, total_fee, fx_loss)
            total_cost = calculate_total_cost(total_fee, fx_loss)

            # FX volatility lookup
            fx_pair = fx_history[
                (fx_history["base_currency"] == row["currency_sent"])
                & (fx_history["target_currency"] == row["currency_received"])
            ]

            volatility = (
                fx_pair["volatility_index"].mean()
                if not fx_pair.empty else None
            )

            scenario_results.append({
                "amount": amount,
                "platform": row["platform"],
                "total_cost": round(total_cost, 2),
                "net_received": round(net_received, 2),
                "settlement_time_days": row["settlement_time_days"],
                "avg_fx_volatility": volatility,
            })

    return pd.DataFrame(scenario_results)
