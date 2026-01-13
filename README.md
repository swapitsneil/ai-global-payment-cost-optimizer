# 🌍 AI Global Payment & Cost Optimizer

Hackathon-Ready Solution for Smart International Payments

---

## 🚀 Project Overview

AI Global Payment & Cost Optimizer helps individuals and businesses find the most cost-effective way to send money internationally by comparing fees, FX markups, settlement times, and user preferences across multiple payment platforms.

Who it's for:
- Expats
- Digital nomads
- Freelancers
- Small businesses
- Anyone making international payments

Why it matters:
International payments are full of hidden costs. Users lose money due to opaque fee structures, FX markups, and confusing trade-offs. This project brings transparency, intelligence, and explainability to global payments.

---

## ▶️ Live Demo

https://swapitsneil-ai-global-payment-cost-optimizer-app-pzexoa.streamlit.app/

---

## 📸 Screenshot



---

## 💡 Problem Statement

International payments suffer from:

- High and hidden fees (fixed + percentage-based)
- Opaque FX markups (2–5 percent losses hidden in exchange rates)
- Lack of clarity on total costs and net received amounts
- No intelligent comparison across multiple platforms
- Complex trade-offs between cost, speed, and reliability

---

## ✨ Solution

AI Global Payment & Cost Optimizer is an AI-driven comparison and recommendation engine that:

- Calculates exact costs for each payment platform
- Compares fees, FX losses, and settlement times
- Allows users to prioritize Cheapest, Fastest, or Balanced options
- Provides AI-powered recommendations with clear explanations
- Shows estimated savings visually
- Works with editable CSV data (no database required)

Key benefits:
- Save money by choosing the best platform
- Understand trade-offs clearly
- Get personalized recommendations
- No-code data management via CSV files

---

## 🤖 Use of AI

AI is used for reasoning, not calculations.

- Deterministic calculations handle all financial math
- AI analyzes trade-offs and ranking results
- Generates natural-language explanations
- Explains why one option is better than others

The AI does NOT perform financial calculations. It only reasons on pre-computed, transparent data.

---

## 🏗️ Architecture Overview

High-level flow:

User Input  
→ Streamlit UI  
→ Rule-based Calculator  
→ Preference-based Scoring  
→ AI Reasoning Engine  
→ Final Recommendation + Explanation

ASCII Architecture Diagram:
```
┌────────────────────────────────────────────┐
│ User Input (Amount, Countries, Preference) │
└───────────────┬────────────────────────────┘
                ↓
┌────────────────────────────────────────────┐
│ Rule-based Calculator                      │
│ Fixed fees, % fees, FX markup, net amount  │
└───────────────┬────────────────────────────┘
                ↓
┌────────────────────────────────────────────┐
│ Preference-weighted Scoring Engine          │
│ Cheapest / Fastest / Balanced              │
└───────────────┬────────────────────────────┘
                ↓
┌────────────────────────────────────────────┐
│ AI Reasoning Engine (OpenRouter)            │
│ Explains trade-offs and recommendations    │
└───────────────┬────────────────────────────┘
                ↓
┌────────────────────────────────────────────┐
│ Final Recommendation + Savings Insight     │
└────────────────────────────────────────────┘
```
---

## 🛠️ Tech Stack

- Streamlit for UI
- Python for logic
- OpenRouter (mistralai/devstral-2512:free)
- CSV-based data (no database)
- Environment variables for security

---

## 🚀 How to Run

1. Install dependencies:
```
pip install -r requirements.txt
```
2. Create environment file:
```
OPENROUTER_API_KEY=your_api_key_here
```
3. Run the app:
```
streamlit run app.py
```
---

## 📁 Project Structure
```
AI Global Payment & Cost Optimizer/
├── app.py
├── calculator.py
├── ai_engine.py
├── preferences/
│   └── weights.py
├── simulator/
│   └── scenario.py
├── visuals/
│   ├── charts.py
│   ├── highlights.py
│   └── fx_charts.py
├── data/
│   ├── payment_methods.csv
│   └── historical_fx.csv
├── requirements.txt
└── README.md
```
---

## 🎯 Hackathon Project Description

AI Global Payment & Cost Optimizer solves the problem of opaque and expensive international payments. Users face confusing fee structures, hidden FX markups, and unclear settlement times when sending money across borders.

This project combines deterministic financial calculations with AI-powered reasoning. Users input their payment details and preferences, and the system calculates exact costs for each platform. A preference-based scoring engine ranks options, and AI explains trade-offs in clear, natural language.

The AI does not perform math. It provides reasoning, trust, and explainability on top of transparent calculations.

---

## ❓ Judge Q&A

Why AI instead of rules only?  
AI provides nuanced explanations and human-readable reasoning that rules alone cannot.

Is the data real?  
The dataset uses realistic mock data based on real-world fee structures and can be replaced easily.

How does this scale?  
The architecture is modular. Data sources, UI, and AI reasoning can be expanded independently.

---

Built for hackathons. Designed like a real fintech product.

Author: Swapnil Nicolson Dadel
