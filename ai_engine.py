import os
import requests
from dotenv import load_dotenv

load_dotenv()

OPENROUTER_API_KEY = os.getenv("OPENROUTER_API_KEY")

API_URL = "https://openrouter.ai/api/v1/chat/completions"
MODEL = "tngtech/deepseek-r1t2-chimera:free"


def get_ai_recommendation(results_df):
    """
    Uses AI to compare payment options and recommend the best one.
    Returns:
    - best_platform (str)
    - explanation (str)
    """

    # ---------- SAFETY FALLBACK ----------
    if results_df.empty:
        raise ValueError("No results to analyze")

    # Convert results to readable text
    options_text = ""
    for _, row in results_df.iterrows():
        options_text += (
            f"Platform: {row['platform']}\n"
            f"Net received: {row['net_received']}\n"
            f"Total fee: {row['total_fee']}\n"
            f"FX loss: {row['fx_loss']}\n"
            f"Settlement time: {row['settlement_time_days']} days\n\n"
        )

    prompt = f"""
You are a fintech decision assistant.

Compare international payment options and recommend the best one.

Decision rules:
- Highest net received is most important
- Lower total fee and FX loss are important
- Faster settlement time is a bonus

Payment options:
{options_text}

Respond STRICTLY in this format:

Best Platform: <platform name>
Explanation:
- Why this platform is recommended
- Trade-offs involved
- One alternative option
"""

    # ---------- IF API KEY MISSING → DETERMINISTIC FALLBACK ----------
    if not OPENROUTER_API_KEY:
        best_row = results_df.loc[results_df["net_received"].idxmax()]
        explanation = (
            f"{best_row['platform']} offers the highest net received amount "
            f"with competitive fees and FX costs. "
            f"It is the safest choice based on pure cost efficiency."
        )
        return best_row["platform"], explanation

    headers = {
        "Authorization": f"Bearer {OPENROUTER_API_KEY}",
        "Content-Type": "application/json",
    }

    payload = {
        "model": MODEL,
        "messages": [
            {"role": "system", "content": "You are a helpful fintech AI assistant."},
            {"role": "user", "content": prompt},
        ],
        "temperature": 0.3,
    }

    try:
        response = requests.post(
            API_URL,
            json=payload,
            headers=headers,
            timeout=25
        )
        response.raise_for_status()
        data = response.json()
        content = data["choices"][0]["message"]["content"]
    except Exception:
        # ---------- API FAILURE FALLBACK ----------
        best_row = results_df.loc[results_df["net_received"].idxmax()]
        explanation = (
            f"{best_row['platform']} provides the highest net received amount "
            f"after fees and FX loss. "
            f"This recommendation is based on deterministic cost analysis."
        )
        return best_row["platform"], explanation

    # ---------- PARSE RESPONSE ----------
    best_platform = None
    explanation_lines = []

    for line in content.splitlines():
        if line.lower().startswith("best platform"):
            best_platform = line.split(":", 1)[1].strip()
        elif line.strip().startswith("-"):
            explanation_lines.append(line.strip("- ").strip())

    explanation = " ".join(explanation_lines)

    if not best_platform or not explanation:
        # ---------- PARSING FALLBACK ----------
        best_row = results_df.loc[results_df["net_received"].idxmax()]
        explanation = (
            f"{best_row['platform']} maximizes the amount received "
            f"and keeps overall costs low compared to other options."
        )
        return best_row["platform"], explanation

    return best_platform, explanation
