import pandas as pd
import numpy as np
from xgboost import XGBRegressor
from sklearn.metrics import mean_absolute_error
from datetime import timedelta
import warnings

# Suppress warnings for a clean terminal output
warnings.filterwarnings('ignore')

def create_time_features(df):
    """
    Machine Learning algorithms cannot understand a raw Date.
    We must extract numerical features so the AI can find behavioral patterns.
    """
    df = df.copy()
    df['DayOfWeek'] = df['Date'].dt.dayofweek
    df['DayOfMonth'] = df['Date'].dt.day
    df['Month'] = df['Date'].dt.month
    df['DayOfYear'] = df['Date'].dt.dayofyear
    
    # Custom Business Features (Teaching the AI about Kenyan banking behavior)
    df['Is_Weekend'] = np.where(df['DayOfWeek'] >= 4, 1, 0) # Fri, Sat, Sun
    df['Is_Payday'] = np.where((df['DayOfMonth'] >= 25) | (df['DayOfMonth'] <= 2), 1, 0)
    df['Is_MidMonth'] = np.where((df['DayOfMonth'] >= 12) & (df['DayOfMonth'] <= 22), 1, 0)
    df['Is_January'] = np.where(df['Month'] == 1, 1, 0)
    
    return df

def run_forecaster():
    print(" Initializing XGBoost Liquidity Forecasting Engine...")
    
    # 1. Load the Historical Data
    try:
        df = pd.read_csv("historical_overdraft_demand.csv")
        df['Date'] = pd.to_datetime(df['Date'])
        df = df.sort_values('Date')
    except FileNotFoundError:
        print(" Error: Could not find historical_overdraft_demand.csv.")
        return

    print(" Engineering time-series features...")
    df_features = create_time_features(df)
    
    # Define our input features (X) and what we want to predict (y)
    features = ['DayOfWeek', 'DayOfMonth', 'Month', 'DayOfYear', 'Is_Weekend', 'Is_Payday', 'Is_MidMonth', 'Is_January']
    target = 'Total_Demand_Millions_KES'
    
    X = df_features[features]
    y = df_features[target]
    
    # Train the XGBoost Model on all historical data
    print(" Training XGBoost Regressor on 2 years of historical behavior...")
    model = XGBRegressor(n_estimators=1000, learning_rate=0.05, max_depth=4, random_state=42)
    model.fit(X, y)
    
    # Calculate training error to ensure it learned correctly
    historical_predictions = model.predict(X)
    mae = mean_absolute_error(y, historical_predictions)
    print(f" Training Complete. Mean Absolute Error: ±{mae:.2f} Million KES")
    
    # 2. Predict the Future (Next 30 Days)
    print("\n Generating 30-Day Liquidity Forecast...")
    last_date = df['Date'].max()
    future_dates = [last_date + timedelta(days=i) for i in range(1, 31)]
    
    future_df = pd.DataFrame({'Date': future_dates})
    future_features = create_time_features(future_df)
    
    # Use the trained AI to predict the demand for these future dates
    future_predictions = model.predict(future_features[features])
    future_df['Predicted_Demand_Millions_KES'] = np.round(future_predictions, 2)
    future_df['Type'] = 'Forecast'
    
    # 3. Combine Historical and Future data for the dashboard
    df['Predicted_Demand_Millions_KES'] = df['Total_Demand_Millions_KES']
    df['Type'] = 'Historical'
    
    # Concatenate and save
    final_df = pd.concat([df[['Date', 'Predicted_Demand_Millions_KES', 'Type']], future_df[['Date', 'Predicted_Demand_Millions_KES', 'Type']]])
    
    output_file = "liquidity_forecast_results.csv"
    final_df.to_csv(output_file, index=False)
    
    print(f"\n[✓] Forecast generated successfully!")
    print(f"Data saved to {output_file}")
    print("\nFuture 5-Day Liquidity Requirements (Sample):")
    print(future_df[['Date', 'Predicted_Demand_Millions_KES']].head(5))

if __name__ == "__main__":
    run_forecaster()