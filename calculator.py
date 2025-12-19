"""
AI Global Payment & Cost Optimizer - Calculation Engine

This module contains deterministic, rule-based calculation functions for:
- Fixed fees
- Percentage-based fees
- Foreign exchange markups
- Total cost calculations
"""

def calculate_fixed_fee(amount, fixed_fee):
    """
    Calculate fixed fee component.

    Args:
        amount: Payment amount
        fixed_fee: Fixed fee amount

    Returns:
        Fixed fee amount
    """
    return fixed_fee

def calculate_percentage_fee(amount, percentage):
    """
    Calculate percentage-based fee component.

    Args:
        amount: Payment amount
        percentage: Percentage fee (e.g., 1.5 for 1.5%)

    Returns:
        Percentage fee amount
    """
    return amount * (percentage / 100)

def calculate_fx_markup(amount, markup_percent):
    """
    Calculate foreign exchange markup loss.

    Args:
        amount: Amount to be converted
        markup_percent: FX markup percentage

    Returns:
        FX loss amount
    """
    return amount * (markup_percent / 100)

def calculate_total_fee(fixed_fee, percentage_fee):
    """
    Calculate total fee combining fixed and percentage fees.

    Args:
        fixed_fee: Fixed fee amount
        percentage_fee: Percentage fee amount

    Returns:
        Total fee amount
    """
    return fixed_fee + percentage_fee

def calculate_net_received(amount, total_fee, fx_loss):
    """
    Calculate net amount received after all fees and FX losses.

    Args:
        amount: Original payment amount
        total_fee: Total fee amount
        fx_loss: FX loss amount

    Returns:
        Net amount received
    """
    return amount - total_fee - fx_loss