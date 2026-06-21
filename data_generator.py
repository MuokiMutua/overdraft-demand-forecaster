import pandas as pd
import numpy as np
from datetime import datetime, timedelta

def generate_overdraft_data(start_date="2024-01-01", days=730):
    print("Initializing Overdraft Demand Synthesizer...")
    
    # 1. Generate Date Range
    dates = [datetime.strptime(start_date, "%Y-%m-%d") + timedelta(days=i) for i in range(days)]
    df = pd.DataFrame({'Date': dates})
    
    # Extract time features for our logic
    df['DayOfWeek'] = df['Date'].dt.dayofweek
    df['DayOfMonth'] = df['Date'].dt.day
    df['Month'] = df['Date'].dt.month
    
    # 2. Base Demand & Growth Trend
    # Let's say the base daily demand started at 50 Million KES and grows slowly
    base_demand = 50.0 
    growth_trend = np.linspace(0, 40.0, days) # Grows by 40M over 2 years
    
    # 3. Apply Human Behavioral Seasonality
    
    # A. The "Payday" Effect
    # Demand drops significantly from the 25th to the 2nd of the month (people have salaries)
    payday_multiplier = np.where((df['DayOfMonth'] >= 25) | (df['DayOfMonth'] <= 2), 0.6, 1.0)
    
    # B. The "Mid-Month Broke" Effect
    # Demand spikes from the 12th to the 22nd as salaries run out
    mid_month_multiplier = np.where((df['DayOfMonth'] >= 12) & (df['DayOfMonth'] <= 22), 1.3, 1.0)
    
    # C. The Weekend Effect
    # People borrow more for leisure/emergencies on Friday(4), Saturday(5), and Sunday(6)
    weekend_multiplier = np.where(df['DayOfWeek'] >= 4, 1.15, 0.95)
    
    # D. The "Njaanuary" (January) Effect
    # January has uniquely high borrowing because of school fees and holiday hangover
    january_multiplier = np.where(df['Month'] == 1, 1.25, 1.0)
    
    # 4. Calculate the Final Mathematical Demand
    # Combine the base, trend, and all behavioral multipliers
    calculated_demand = (base_demand + growth_trend) * payday_multiplier * mid_month_multiplier * weekend_multiplier * january_multiplier
    
    # 5. Add Random Noise (Real world data is never perfectly smooth)
    # Add +/- 10% random noise to simulate daily unpredictability
    noise = np.random.normal(1.0, 0.1, days)
    df['Total_Demand_Millions_KES'] = (calculated_demand * noise).round(2)
    
    # 6. Clean up the dataframe for saving
    output_df = df[['Date', 'Total_Demand_Millions_KES']]
    
    # Save to CSV
    output_file = "historical_overdraft_demand.csv"
    output_df.to_csv(output_file, index=False)
    
    print("\n--- SYNTHESIS COMPLETE ---")
    print(f"Generated {days} days of historical demand data.")
    print(f"Data saved to {output_file}")
    print("\nSample Output:")
    print(output_df.head(10))

if __name__ == "__main__":
    generate_overdraft_data()