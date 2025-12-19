import os
import requests
from dotenv import load_dotenv

load_dotenv()

OPENROUTER_API_KEY = os.getenv("OPENROUTER_API_KEY")

if not OPENROUTER_API_KEY:
    raise ValueError("OpenRouter API key is required")

API_URL = "https://openrouter.ai/api/v1/chat/completions"
MODEL = "mistralai/devstral-2512:free"


def get_ai_recommendation(results_df):
    """
    Uses AI to compare payment options and recommend the best one.
    """

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
You are a financial assistant.

Compare the following international payment options and recommend the best one.

Criteria:
- Maximize net received amount
- Consider lower fees and FX loss
- Faster settlement time is a bonus

Payment options:
{options_text}

Return your response in this format:
Best Platform: <platform name>
Explanation: <clear explanation>
"""

    headers = {
        "Authorization": f"Bearer {OPENROUTER_API_KEY}",
        "Content-Type": "application/json",
    }

    payload = {
        "model": MODEL,
        "messages": [
            {"role": "system", "content": "You are a helpful financial AI assistant."},
            {"role": "user", "content": prompt},
        ],
        "temperature": 0.3,
    }

    response = requests.post(API_URL, json=payload, headers=headers, timeout=30)
    response.raise_for_status()

    data = response.json()
    content = data["choices"][0]["message"]["content"]

    # Parse AI response
    best_platform = None
    explanation = ""

    for line in content.splitlines():
        if line.lower().startswith("best platform"):
            best_platform = line.split(":", 1)[1].strip()
        elif line.lower().startswith("explanation"):
            explanation = line.split(":", 1)[1].strip()

    if not best_platform or not explanation:
        raise ValueError("AI response format invalid")

    return best_platform, explanation
