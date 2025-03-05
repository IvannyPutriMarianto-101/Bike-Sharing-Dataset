import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
sns.set(style='dark')

# Load Data
bike_df = pd.read_csv("dashboard/new_data.csv")

# Helper Functions
def create_weather_situation_df(df):
    return df.groupby(by="weathersit").cnt.mean().reset_index().rename(columns={"weathersit": "Weather Condition"})

def create_weekday_df(df):
    return df.groupby(by="weekday").cnt.mean().sort_values(ascending=False).reset_index()

def create_season_day_df(df):
    return df.groupby(by="season").agg({"casual": "mean", "registered": "mean"})

def create_holiday_df(df):
    holiday_df = df.groupby("holiday").cnt.mean().reset_index()
    holiday_df["holiday"] = holiday_df["holiday"].replace({0: "Not Holiday", 1: "Holiday"})
    return holiday_df

# Adjust Year Values
bike_df["yr"] = bike_df["yr"].replace({0: 2011, 1: 2012})

# Sidebar Filter
st.sidebar.header("🔍 Filter Data")
unique_years = sorted(bike_df["yr"].unique())
selected_year = st.sidebar.selectbox("Pilih Tahun:", ["Semua"] + [str(year) for year in unique_years])
selected_season = st.sidebar.multiselect("Pilih Musim:", ["Semua"] + ["Spring", "Summer", "Fall", "Winter"])

filtered_df = bike_df.copy()
if selected_year != "Semua":
    filtered_df = filtered_df[filtered_df["yr"] == int(selected_year)]

season_map = {1: "Spring", 2: "Summer", 3: "Fall", 4: "Winter"}
filtered_df["season"] = filtered_df["season"].map(season_map)
if "Semua" not in selected_season and selected_season:
    filtered_df = filtered_df[filtered_df["season"].isin(selected_season)]

# Prepare Data
weather_situation_df = create_weather_situation_df(filtered_df)
weekday_df = create_weekday_df(filtered_df)
season_day_df = create_season_day_df(filtered_df)
holiday_df = create_holiday_df(filtered_df)

st.header("🚴‍♂️ Bike Rental Dashboard")

# Visualisasi: Penyewaan per Musim
st.subheader("Jumlah Penyewaan Sepeda per Musim")
fig, ax = plt.subplots(figsize=(10, 5))
sns.barplot(x=filtered_df["season"], y=filtered_df["cnt"], palette="coolwarm", ax=ax)
ax.set_xlabel("Musim")
ax.set_ylabel("Jumlah Penyewaan")
st.pyplot(fig)

# Visualisasi: Penyewaan per Bulan
st.subheader("Total Penyewaan Sepeda per Bulan")
monthly_trend = filtered_df.groupby("mnth")["cnt"].sum().reset_index()
month_labels = {
    1: "Jan", 2: "Feb", 3: "Mar", 4: "Apr", 5: "May", 6: "Jun",
    7: "Jul", 8: "Aug", 9: "Sep", 10: "Oct", 11: "Nov", 12: "Dec"
}
monthly_trend["mnth"] = monthly_trend["mnth"].map(month_labels)
max_month = monthly_trend.loc[monthly_trend["cnt"].idxmax(), "mnth"]
colors = ["lightgreen" if month == max_month else "lightgray" for month in monthly_trend["mnth"]]
fig, ax = plt.subplots(figsize=(10, 5))
sns.barplot(x=monthly_trend["mnth"], y=monthly_trend["cnt"], palette=colors, ax=ax)
ax.set_xlabel("Bulan")
ax.set_ylabel("Jumlah Penyewaan")
st.pyplot(fig)

# Visualisasi: Perbandingan Penyewaan per Tahun
st.subheader("Perbandingan Penyewaan Sepeda Bulanan antara 2011 dan 2012")
fig, ax = plt.subplots(figsize=(12, 5))
bike_df.groupby(["yr", "mnth"]).cnt.sum().unstack().T.plot(kind="bar", ax=ax, color=["pink", "red"])
ax.set_xlabel("Bulan")
ax.set_ylabel("Jumlah Penyewaan")
ax.legend(title="Tahun")
st.pyplot(fig)

# Visualisasi: Hari Kerja vs Akhir Pekan
st.subheader("Rata-rata Penyewaan Sepeda pada Hari Kerja vs Akhir Pekan")
fig, ax = plt.subplots(figsize=(10, 5))
sns.barplot(x=filtered_df["workingday"].map({0: "Akhir Pekan", 1: "Hari Kerja"}), y=filtered_df["cnt"], palette="magma", ax=ax)
ax.set_xlabel("Jenis Hari")
ax.set_ylabel("Jumlah Penyewaan")
st.pyplot(fig)

st.markdown("---")
st.markdown("© 2025 **Ivanny Putri Marianto** | All rights reserved.")