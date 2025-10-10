import streamlit as st
import pandas as pd
import numpy as np
from sklearn.linear_model import LinearRegression
import matplotlib.pyplot as plt
from datetime import datetime


st.set_page_config(page_title="AI Expense Forecasting Tool", layout="wide")
st.title(" Budget-Wise AI Expense Forecasting Tool")
st.write("An AI-powered tool that helps you forecast your future expenses and plan your budget effectively.")

st.sidebar.header(" Data Input")

data_path = "dataset.csv"  #  Connect directly to your dataset file
try:
    df = pd.read_csv(data_path)
    st.sidebar.success(f"Loaded data from {data_path}")
except FileNotFoundError:
    st.sidebar.error(" dataset.csv not found in app directory. Using sample data instead.")
    data = {
        "Month": ["Jan", "Feb", "Mar", "Apr", "May", "Jun"],
        "Food": [1200, 1500, 1600, 1400, 1700, 1550],
        "Rent": [5000, 5000, 5000, 5000, 5000, 5000],
        "Travel": [800, 700, 900, 1000, 950, 1100],
        "Entertainment": [400, 500, 600, 450, 700, 650]
    }
    df = pd.DataFrame(data)

st.subheader(" Current Expense Data")
st.dataframe(df)


def forecast_expense(data, category, months_ahead=3):
    model = LinearRegression()
    X = np.arange(len(data)).reshape(-1, 1)
    y = data[category].values
    model.fit(X, y)
    future_X = np.arange(len(data), len(data) + months_ahead).reshape(-1, 1)
    future_preds = model.predict(future_X)
    return future_preds


st.subheader("AI Forecast Results")

months_to_predict = st.slider("Select months to forecast:", 1, 12, 3)

# Select numeric columns only
numeric_cols = df.select_dtypes(include=np.number).columns

forecast_results = {}
for category in numeric_cols:
    preds = forecast_expense(df, category, months_to_predict)
    forecast_results[category] = preds

# Display predictions
future_months = [f"Month {i+1}" for i in range(months_to_predict)]
forecast_df = pd.DataFrame(forecast_results, index=future_months)
st.dataframe(forecast_df.style.format("{:.2f}"))


st.subheader(" Expense Trend & Forecast Visualization")

for category in numeric_cols:
    plt.figure()
    past_x = np.arange(len(df))
    future_x = np.arange(len(df), len(df) + months_to_predict)
    plt.plot(past_x, df[category], label="Past Data", marker='o')
    plt.plot(future_x, forecast_results[category], label="Forecast", linestyle='--', marker='x')
    plt.title(f"{category} Expense Forecast")
    plt.xlabel("Months")
    plt.ylabel("Amount (₹)")
    plt.legend()
    st.pyplot(plt)


st.subheader(" AI-Based Budget Suggestions")

total_future = forecast_df.sum(axis=1).mean()
total_past = df[numeric_cols].sum(axis=1).mean()

if total_future > total_past:
    st.warning(f" Your expenses are projected to increase by ₹{total_future - total_past:.2f}. Consider adjusting your budget.")
else:
    st.success(f"Great! Your projected expenses are stable or reducing by ₹{total_past - total_future:.2f}.")

st.write("AI Suggestion Summary:")
if total_future > total_past:
    st.markdown("""
    - Try to *reduce variable expenses* like Entertainment or Travel.  
    - Consider setting *fixed savings goals* every month.  
    - Review recurring subscriptions or non-essential spends.
    """)
else:
    st.markdown("""
    - Keep up the good savings habit!  
    - You can allocate more funds toward *investments* or *education*.  
    """)


if st.button(" Download Forecast Report"):
    forecast_df.to_csv("forecast_report.csv")
    st.success("Forecast saved as forecast_report.csv in your working directory.")
