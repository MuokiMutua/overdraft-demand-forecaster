import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
from datetime import datetime, timedelta

st.set_page_config(page_title="Treasury Liquidity Command Center", layout="wide")

st.markdown("""
<style>
    @import url('https://fonts.googleapis.com/css2?family=Inter:wght@400;500;600;700&display=swap');
    html, body, [class*="css"] { font-family:'Inter', sans-serif; background:#0f172a; color: #e2e8f0; }
    .stApp { background:#0f172a; }
    
    .metric-card { background:#1e293b; border:1px solid #334155; border-radius:6px; padding:1.25rem; margin-bottom:1rem; box-shadow: 0 4px 6px -1px rgba(0, 0, 0, 0.1); }
    .metric-title { color:#94a3b8; font-size:0.8rem; font-weight:600; text-transform:uppercase; letter-spacing:0.05em; }
    .metric-value { color:#f8fafc; font-size:2.2rem; font-weight:700; margin-top:0.4rem; letter-spacing:-0.02em; }
    .metric-sub { color:#10b981; font-size:0.8rem; font-weight:500; margin-top:0.2rem; }
    
    .alert-card { background: rgba(239, 68, 68, 0.05); border-left: 4px solid #ef4444; padding: 1rem 1.5rem; border-radius: 4px; margin-top: 1rem; }
    .alert-title { color: #ef4444; font-weight: 600; font-size: 0.9rem; text-transform: uppercase; letter-spacing: 0.05em; margin-bottom: 0.5rem; }
</style>
""", unsafe_allow_html=True)

@st.cache_data
def load_data():
    try:
        df = pd.read_csv("liquidity_forecast_results.csv")
        df['Date'] = pd.to_datetime(df['Date'])
        return df
    except FileNotFoundError:
        return None

df = load_data()

st.markdown("<h1 style='color:#f8fafc; font-size:1.8rem; margin-bottom:0;'>TREASURY LIQUIDITY COMMAND CENTER</h1>", unsafe_allow_html=True)
st.markdown("<p style='color:#94a3b8; font-size:0.9rem; text-transform:uppercase; letter-spacing:0.05em;'>AI-Driven Instant Overdraft Reserve Allocation</p>", unsafe_allow_html=True)
st.markdown("<hr style='border-color:#334155; margin-top:0.5rem; margin-bottom:1.5rem;'>", unsafe_allow_html=True)

if df is None:
    st.error("SYSTEM ERROR: Data file not found. Please run forecasting_engine.py first.")
    st.stop()

# Calculate specific metrics for the CFO
historical_data = df[df['Type'] == 'Historical']
forecast_data = df[df['Type'] == 'Forecast']

current_date = historical_data['Date'].max()
next_7_days = forecast_data.head(7)

# Key Treasury Calculations
total_7_day_requirement = next_7_days['Predicted_Demand_Millions_KES'].sum()
peak_30_day_demand = forecast_data['Predicted_Demand_Millions_KES'].max()
peak_30_day_date = forecast_data[forecast_data['Predicted_Demand_Millions_KES'] == peak_30_day_demand]['Date'].iloc[0]
avg_historical_demand = historical_data['Predicted_Demand_Millions_KES'].mean()

c1, c2, c3, c4 = st.columns(4)
with c1:
    st.markdown(f"<div class='metric-card'><div class='metric-title'>Current Baseline (Daily)</div><div class='metric-value'>KES {avg_historical_demand:.1f}M</div></div>", unsafe_allow_html=True)
with c2:
    st.markdown(f"<div class='metric-card'><div class='metric-title'>Required Next 7 Days</div><div class='metric-value' style='color:#38bdf8;'>KES {total_7_day_requirement:.1f}M</div><div class='metric-sub'>Cumulative Settlement Target</div></div>", unsafe_allow_html=True)
with c3:
    st.markdown(f"<div class='metric-card'><div class='metric-title'>Forecasted 30-Day Peak</div><div class='metric-value' style='color:#ef4444;'>KES {peak_30_day_demand:.1f}M</div><div class='metric-sub'>Expected on {peak_30_day_date.strftime('%b %d')}</div></div>", unsafe_allow_html=True)
with c4:
    # A standard treasury buffer is usually 15% above peak forecast
    buffer_recommendation = peak_30_day_demand * 1.15
    st.markdown(f"<div class='metric-card'><div class='metric-title'>Recommended Reserve Cap</div><div class='metric-value' style='color:#10b981;'>KES {buffer_recommendation:.1f}M</div><div class='metric-sub'>Peak + 15% Safety Buffer</div></div>", unsafe_allow_html=True)

st.markdown("<br>", unsafe_allow_html=True)

st.markdown("<h3 style='color:#f8fafc; font-size:1.0rem; text-transform:uppercase; letter-spacing:0.05em;'>30-Day Liquidity Forecast Trajectory</h3>", unsafe_allow_html=True)

# We use Plotly Graph Objects to map historical and forecasted data smoothly
fig_trajectory = go.Figure()

# Add Historical Line (Last 60 days to keep the chart clean)
recent_historical = historical_data.tail(60)
fig_trajectory.add_trace(go.Scatter(
    x=recent_historical['Date'], 
    y=recent_historical['Predicted_Demand_Millions_KES'],
    mode='lines',
    name='Historical Actuals',
    line=dict(color='#94a3b8', width=2)
))

# Add Forecast Line
fig_trajectory.add_trace(go.Scatter(
    x=forecast_data['Date'], 
    y=forecast_data['Predicted_Demand_Millions_KES'],
    mode='lines',
    name='XGBoost Forecast',
    line=dict(color='#38bdf8', width=3, dash='solid')
))

# Connect the two lines visually
connection_x = [recent_historical['Date'].iloc[-1], forecast_data['Date'].iloc[0]]
connection_y = [recent_historical['Predicted_Demand_Millions_KES'].iloc[-1], forecast_data['Predicted_Demand_Millions_KES'].iloc[0]]
fig_trajectory.add_trace(go.Scatter(
    x=connection_x, y=connection_y,
    mode='lines', showlegend=False,
    line=dict(color='#38bdf8', width=3)
))

fig_trajectory.update_layout(
    paper_bgcolor="rgba(0,0,0,0)", plot_bgcolor="rgba(0,0,0,0)",
    hovermode="x unified",
    xaxis=dict(showgrid=True, gridcolor='#334155', tickfont=dict(color='#94a3b8')),
    yaxis=dict(title="Demand (Millions KES)", showgrid=True, gridcolor='#334155', tickfont=dict(color='#f8fafc')),
    legend=dict(orientation="h", yanchor="bottom", y=1.02, xanchor="right", x=1, font=dict(color='#f8fafc')),
    margin=dict(l=0, r=0, t=30, b=0),
    height=400
)
st.plotly_chart(fig_trajectory, use_container_width=True)

col_left, col_right = st.columns([1, 1], gap="large")

with col_left:
    st.markdown("<h3 style='color:#f8fafc; font-size:1.0rem; text-transform:uppercase; letter-spacing:0.05em; margin-top:1rem;'>Behavioral Analytics: Demand by Day of Week</h3>", unsafe_allow_html=True)
    
    # Calculate average demand per day of the week to show the AI learned the "Weekend Effect"
    df['DayOfWeek'] = df['Date'].dt.day_name()
    day_order = ['Monday', 'Tuesday', 'Wednesday', 'Thursday', 'Friday', 'Saturday', 'Sunday']
    day_avg = historical_data.copy()
    day_avg['DayOfWeek'] = day_avg['Date'].dt.day_name()
    day_avg = day_avg.groupby('DayOfWeek')['Predicted_Demand_Millions_KES'].mean().reindex(day_order).reset_index()
    
    fig_bar = px.bar(
        day_avg, 
        x='DayOfWeek', 
        y='Predicted_Demand_Millions_KES',
        color_discrete_sequence=['#10b981']
    )
    fig_bar.update_layout(
        paper_bgcolor="rgba(0,0,0,0)", plot_bgcolor="rgba(0,0,0,0)",
        xaxis=dict(title="", showgrid=False, tickfont=dict(color='#94a3b8')),
        yaxis=dict(title="Avg Demand (M KES)", showgrid=True, gridcolor='#334155', tickfont=dict(color='#f8fafc')),
        margin=dict(l=0, r=0, t=20, b=0),
        height=300
    )
    st.plotly_chart(fig_bar, use_container_width=True)

with col_right:
    st.markdown("<h3 style='color:#f8fafc; font-size:1.0rem; text-transform:uppercase; letter-spacing:0.05em; margin-top:1rem;'>Treasury Action Items</h3>", unsafe_allow_html=True)
    
    st.markdown(f"""
    <div class='alert-card'>
        <div class='alert-title'>Approaching Peak Velocity</div>
        <p style='font-size: 0.9rem; margin-bottom: 0; color: #cbd5e1; line-height: 1.6;'>
        <strong>System Notice:</strong> The AI model has detected an upcoming peak on <strong>{peak_30_day_date.strftime('%B %d')}</strong> requiring <strong>KES {peak_30_day_demand:.1f}M</strong>.<br>
        <strong>Action:</strong> Ensure central bank settlement accounts are pre-funded 24 hours prior to avoid transaction degradation.
        </p>
    </div>
    
    <div class='alert-card' style='border-left-color: #38bdf8; background: rgba(56, 189, 248, 0.05);'>
        <div class='alert-title' style='color: #38bdf8;'>Weekend Surge Protocol</div>
        <p style='font-size: 0.9rem; margin-bottom: 0; color: #cbd5e1; line-height: 1.6;'>
        <strong>System Notice:</strong> Historical data indicates a consistent volume spike occurring late Friday into Saturday.<br>
        <strong>Action:</strong> Automated sweeps to yield-bearing accounts should be paused Friday at 16:00 to maintain adequate liquidity buffers.
        </p>
    </div>
    """, unsafe_allow_html=True)