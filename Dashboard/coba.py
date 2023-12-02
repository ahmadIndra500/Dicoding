import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import streamlit as st
from babel.numbers import format_currency

sns.set(style='dark')

# Helper function to prepare various dataframes
def monthly_orders_df(df):
    monthly_orders_df = df.resample(rule='M').agg({
        "order_id": "nunique",
        "payment_value": "sum"
    })
    monthly_orders_df.index = monthly_orders_df.index.strftime('%B-%Y')
    monthly_orders_df = monthly_orders_df.reset_index()
    monthly_orders_df.rename(columns={
        "order_id": "order_count",
        "payment_value": "revenue"
    }, inplace=True)
    return monthly_orders_df

# Load cleaned data
order_all_df = pd.read_csv(r"C:\Users\hp\Documents\Dicoding\Submmision\Data\order_all_df.csv")
order_item_all_df = pd.read_csv(r"C:\Users\hp\Documents\Dicoding\Submmision\Data\order_item_all_df.csv")

# Set order_purchase_timestamp as DatetimeIndex
order_all_df['order_purchase_timestamp'] = pd.to_datetime(order_all_df['order_purchase_timestamp'])
order_all_df.set_index('order_purchase_timestamp', inplace=True)

# Prepare various dataframes
daily_orders_df = monthly_orders_df(order_all_df)

# Product performance
st.subheader("Best & Worst Performing Product")

daily_orders_df["order_purchase_timestamp"] = pd.to_datetime(daily_orders_df["order_purchase_timestamp"])
daily_orders_df["bulan"] = daily_orders_df["order_purchase_timestamp"].dt.strftime("%B-%Y")
daily_orders_2017_2018 = daily_orders_df[
    (daily_orders_df["order_purchase_timestamp"].dt.year >= 2017) &
    (daily_orders_df["order_purchase_timestamp"].dt.year <= 2018)
]

# Create a figure and axis
fig, ax = plt.subplots(figsize=(10, 5))
ax.plot(daily_orders_2017_2018["bulan"], daily_orders_2017_2018["order_count"], marker='o', linewidth=2, color="#72BCD4")
ax.set_title("Penjualan Perbulan (2017-2018)", loc="center", fontsize=20)
ax.set_xticklabels(daily_orders_2017_2018["bulan"], rotation=45, fontsize=10)
ax.tick_params(axis='y', labelsize=10)
ax.set_xlabel("Bulan", fontsize=12)
ax.set_ylabel("Jumlah Penjualan", fontsize=12)

# Pass the figure to st.pyplot()
st.pyplot(fig)