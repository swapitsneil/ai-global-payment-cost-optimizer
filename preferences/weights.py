"""
Preference Weighting Engine

Allows users to prioritize:
- Cheapest
- Fastest
- Balanced

Returns weights used for scoring platforms.
"""

def get_preference_weights(preference):
    """
    Returns scoring weights based on user preference
    """

    if preference == "Cheapest":
        return {
            "cost": 0.6,
            "speed": 0.1,
            "net": 0.3
        }

    if preference == "Fastest":
        return {
            "cost": 0.2,
            "speed": 0.6,
            "net": 0.2
        }

    # Balanced (default)
    return {
        "cost": 0.4,
        "speed": 0.3,
        "net": 0.3
    }
