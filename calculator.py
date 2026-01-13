"""
AI Global Payment & Cost Optimizer - Calculation Engine

Deterministic, rule-based calculations for:
- Fixed fees
- Percentage fees
- FX markup
- Total cost
- Net received
- Scoring (for preference-based ranking)
"""

# -----------------------------
# BASIC FEE CALCULATIONS
# -----------------------------

def calculate_fixed_fee(amount, fixed_fee):
    """
    Fixed fee component
    """
    return fixed_fee


def calculate_percentage_fee(amount, percentage):
    """
    Percentage-based fee
    Example: 1.5 → 1.5%
    """
    return amount * (percentage / 100)


def calculate_fx_markup(amount, markup_percent):
    """
    FX markup loss
    """
    return amount * (markup_percent / 100)


def calculate_total_fee(fixed_fee, percentage_fee):
    """
    Total fee = fixed + percentage
    """
    return fixed_fee + percentage_fee


def calculate_net_received(amount, total_fee, fx_loss):
    """
    Net received after all deductions
    """
    return amount - total_fee - fx_loss


# -----------------------------
# NEW: TOTAL COST HELPER
# -----------------------------

def calculate_total_cost(total_fee, fx_loss):
    """
    Total cost paid by user (fees + FX loss)
    """
    return total_fee + fx_loss


# -----------------------------
# NEW: SCORING ENGINE (FOR PREFERENCES)
# -----------------------------

def calculate_score(
    net_received,
    total_cost,
    settlement_time_days,
    weights=None
):
    """
    Computes a normalized score for ranking platforms.

    weights example:
    {
        "cost": 0.5,
        "speed": 0.3,
        "net": 0.2
    }
    """

    if weights is None:
        weights = {
            "cost": 0.4,
            "speed": 0.3,
            "net": 0.3
        }

    # Normalize values (simple heuristic)
    cost_score = 1 / (1 + total_cost)
    speed_score = 1 / (1 + settlement_time_days)
    net_score = net_received

    final_score = (
        weights["cost"] * cost_score +
        weights["speed"] * speed_score +
        weights["net"] * net_score
    )

    return final_score
