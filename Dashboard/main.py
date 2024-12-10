import streamlit as st
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
from statsmodels.tsa.holtwinters import ExponentialSmoothing

# Load the dataet
data = pd.read_csv('./Dataset/hour.csv)

# Dashboard Title
st.title("Bike Rental Demand Dashboard")

# Display Insights
st.header("Insights from Predicted Demand Analysis")
st.write("""
- The total daily bike rentals are significantly influenced by temperature and hour of the day.
- Rentals increase as temperature rises from 0°C to around 20°C and plateau up to 35°C.
- Peak rentals occur at 5 PM and 8 AM, aligning with commuting hours.
- Rentals on working days average around 4,500, while holiday rentals hover around 4,300.
""")

# Data Overview
st.header("Data Overview")
st.write(data.head())

# Visualization of Rentals by Temperature
st.header("Bike Rentals vs Temperature")
plt.figure(figsize=(10, 5))
sns.lineplot(data=data, x='temperature', y='rentals')
plt.title("Bike Rentals vs Temperature")
plt.xlabel("Temperature (°C)")
plt.ylabel("Number of Rentals")
st.pyplot(plt)

# Exponential Smoothing Forecast
st.header("Predicted Demand Using Exponential Smoothing")

# Fit Exponential Smoothing model
model = ExponentialSmoothing(data['rentals'], seasonal='add', seasonal_periods=12)
fit = model.fit()
data['forecast'] = fit.fittedvalues

# Plotting the forecast
plt.figure(figsize=(10, 5))
plt.plot(data['rentals'], label='Actual Rentals', color='blue')
plt.plot(data['forecast'], label='Forecasted Rentals', color='orange')
plt.title("Actual vs Forecasted Rentals")
plt.xlabel("Time")
plt.ylabel("Number of Rentals")
plt.legend()
st.pyplot(plt)

# Display the forecasted values
st.subheader("Forecasted Rentals")
st.write(fit.forecast(steps=30))  # Forecast for the next 30 time periods
