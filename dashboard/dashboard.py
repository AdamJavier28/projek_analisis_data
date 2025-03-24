import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import streamlit as st
from babel.numbers import format_currency
sns.set(style='dark')

def create_hourly_rentals_df(df):
    hourly_rentals_df = hour_df.groupby("hr").agg({
        "cnt": "sum"
    }).reset_index()
    hourly_rentals_df.rename(columns={
        "hr": "hour",
        "cnt": "total_rentals"
    }, inplace=True)

    return hourly_rentals_df

def create_monthly_trend_df(df):
    df["dteday"] = pd.to_datetime(df["dteday"])
    monthly_trend_df = day_df.resample(rule='ME', on='dteday').agg({
        "cnt": "sum"
    })
    df["dteday"] = pd.to_datetime(df["dteday"])
    monthly_trend_df.index = monthly_trend_df.index.strftime('%Y-%m')
    monthly_trend_df = monthly_trend_df.reset_index()
    monthly_trend_df.rename(columns={
        "dteday": "year_month",
        "cnt": "total_rentals"
    }, inplace=True)
    return monthly_trend_df

def create_bins_df(df):
    bins = [0, 2500, 5000, day_df["cnt"].max()]
    labels = ["Rendah", "Sedang", "Tinggi"]
    day_df["rental_category"] = pd.cut(day_df["cnt"], bins=bins, labels=labels, include_lowest=True)
    rental_counts = day_df["rental_category"].value_counts()
    return rental_counts

day_df = pd.read_csv("day_df.csv")
hour_df = pd.read_csv("hour_df.csv")

selected_option = st.sidebar.radio(
    "Pilih Tren yang Ingin Ditampilkan:",
    ("Tren Penyewaan per Bulan", "Tren Penyewaan Jam", "Distribusi Penyewaan Sepeda Berdasarkan Jumlah Per Hari")
)


if selected_option == "Tren Penyewaan per Bulan":

    monthly_trend_df = create_monthly_trend_df(day_df)
    st.subheader('Tren Penyewaan Sepeda per Bulan')

    max_month = monthly_trend_df.loc[monthly_trend_df["total_rentals"].idxmax()]
    st.metric("Tren teritinggi pada Bulan", value=str(max_month["year_month"]))

    fig, ax = plt.subplots(figsize=(10, 5))
    ax.plot(monthly_trend_df["year_month"], monthly_trend_df["total_rentals"], marker="o", linestyle="-", color="#72BCD4")
    ax.set_xlabel("Bulan", fontsize=12)
    ax.set_ylabel("Jumlah Penyewaan Sepeda", fontsize=12)
    ax.tick_params(axis='x', rotation=45) 
    st.pyplot(fig)

if selected_option == "Tren Penyewaan Jam":
    hourly_trend_df = create_hourly_rentals_df(hour_df)
    st.subheader("Tren Penyewaan Sepeda Berdasarkan Jam")
    max_hour = hourly_trend_df.loc[hourly_trend_df["total_rentals"].idxmax()]
    st.metric("Waktu dengan Penyewaan Tertinggi", value=str(max_hour["hour"]))

    fig, ax = plt.subplots(figsize=(10, 5))
    ax.plot(hourly_trend_df["hour"], hourly_trend_df["total_rentals"], 
            marker="o", linestyle="-", color="#72BCD4")
    ax.set_xticks(range(0, 24)) 

    st.pyplot(fig)

if selected_option == "Distribusi Penyewaan Sepeda Berdasarkan Jumlah Per Hari":
    rental_counts = create_bins_df(hour_df)
    st.subheader("Distribusi Penyewaan Sepeda Berdasarkan Kuantitas")
    fig, ax = plt.subplots(figsize=(8, 8))
    ax.pie(rental_counts, labels=rental_counts.index, autopct="%1.1f%%", 
       colors=["#ff9999", "#66b3ff", "#99ff99"], startangle=140)
    st.pyplot(fig)

