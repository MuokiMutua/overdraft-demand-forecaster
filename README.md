## Liquidity Management AI: Time Series Demand Forecasting
<img width="978" height="735" alt="image" src="https://github.com/user-attachments/assets/d68a7e48-4b15-40bf-bb9e-00abf5d4486f" />
<img width="969" height="440" alt="image" src="https://github.com/user-attachments/assets/ba5c8b8e-edd7-49b5-b82b-8ecbdbc4cf3e" />

An end-to-end Machine Learning pipeline designed to solve a critical liquidity management challenge in fintech: predicting daily cash requirements for instant overdraft facilities.

This project synthesizes historical borrowing behavior, trains an Extreme Gradient Boosting (XGBoost) model to recognize temporal and behavioral patterns, and provides a continuous 30-day forecast to optimize treasury reserves.

## The Business Problem

When a financial institution or telco offers instant micro-loans (e.g., Safaricom's Fuliza), they must maintain adequate cash in settlement accounts to fund those transactions instantly.

* **Under-funding** leads to failed transactions, damaged brand reputation, and lost revenue.

* **Over-funding** traps capital that could otherwise be invested in high-yield instruments.

Traditional, static liquidity management relies on historical averages, failing to account for compounding behavioral trends like weekend spikes, mid-month exhaustion, or holiday anomalies.

## Objective

To build a highly accurate predictive engine that allows a Chief Financial Officer (CFO) to:

* Move from reactive cash management to proactive liquidity forecasting.

* Accurately predict exact cash requirements 30 days into the future.

* Minimize idle cash reserves while mathematically guaranteeing transaction fulfillment.

## System Architecture

This project is modularized into three core components:

1. **data_generator.py (Historical Data Synthesizer)**

* Generates two years of realistic, daily continuous demand data.

* **Encodes human behavioral logic:** Payday dips (people have salaries), mid-month spikes (salaries run out), weekend surges (leisure borrowing), and the "January Effect."

2. **forecasting_engine.py (The Machine Learning Model)**

* **Feature Engineering:** Deconstructs standard Date objects into numerical features (DayOfWeek, DayOfMonth, Is_Payday, etc.) that algorithms can process.

* **Model Training:** Utilizes XGBoost (Extreme Gradient Boosting Regressor) to map historical features to continuous demand outputs.

* **Evaluation:** Calculates Mean Absolute Error (MAE) to validate model precision before generating the future 30-day requirement matrix.

3. **liquidity_dashboard.py (The Treasury Command Center)**

* A Python-based Streamlit application.

* Visualizes the historical trend against the 30-day AI forecast using Plotly.

* Calculates immediate actionable metrics (e.g., "Cash Required Next 7 Days") for treasury allocation.

## Tech Stack

* Language: Python 3.x

* Machine Learning: xgboost, scikit-learn

* Data Processing: pandas, numpy, datetime

* Visualization & UI: streamlit, plotly

## Dashboard Highlights

* The Forecast Trajectory: A seamless line chart connecting actual historical demand with the AI-predicted trajectory, clearly highlighting the confidence interval for the upcoming 30 days.

* Treasury Action Items: Dynamic key performance indicators detailing exact multi-million allocation requirements for the next 48 hours and the coming week.

* Behavioral Insights: Visual breakdowns of the "Day of Week" utilization, validating the model's understanding of human borrowing patterns.
