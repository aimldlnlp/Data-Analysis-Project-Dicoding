import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
import seaborn as sns
import streamlit as st

sns.set(style="whitegrid")

df_day = pd.read_csv("Dataset/day.csv")
df_day["dteday"] = pd.to_datetime(df_day["dteday"])
df_day["year"] = df_day["dteday"].dt.year

st.header("Bike Rental Demand Dashboard :bike:")
st.caption("By Zinadine Zidan")

min_date = df_day["dteday"].min().date()
max_date = df_day["dteday"].max().date()

start_date, end_date = st.sidebar.date_input(
    label="Time Range",
    min_value=min_date,
    max_value=max_date,
    value=[min_date, max_date],
)

start_date = pd.to_datetime(start_date)
end_date = pd.to_datetime(end_date)

filtered_data = df_day[
    (df_day["dteday"] >= start_date) & (df_day["dteday"] <= end_date)
]

todays_cnt = int(filtered_data["cnt"].iloc[-1])
yesterdays_cnt = int(filtered_data["cnt"].iloc[-2])

st.sidebar.metric(label="Daily user growth", value=todays_cnt, delta=yesterdays_cnt)


daily_users_data = (
    filtered_data.groupby("dteday")
    .agg({"casual": "sum", "registered": "sum", "cnt": "sum"})
    .reset_index()
)

# st.subheader("Total Users")

col1, col2, col3 = st.columns(3)


def format_number(number):
    return f"{number:,}"


with col1:
    total_casual = daily_users_data.casual.sum()
    st.metric("Total Casual Users", value=format_number(total_casual))

with col2:
    total_registered = daily_users_data.registered.sum()
    st.metric("Total Registered Users", value=format_number(total_registered))

with col3:
    total_cnt = daily_users_data.cnt.sum()
    st.metric("Total Users", value=format_number(total_cnt))

# PLOT 1
st.subheader("Daily Users")
fig_fh3, ax_fh3 = plt.subplots(figsize=(16, 8))
sns.lineplot(
    x="dteday",
    y="casual",
    data=daily_users_data,
    ax=ax_fh3,
    label="Casual",
    marker="o",
    color="#a07aff",
)
sns.lineplot(
    x="dteday",
    y="registered",
    data=daily_users_data,
    ax=ax_fh3,
    label="Registered",
    marker="o",
    color="#7affa0",
)
ax_fh3.set_ylabel("Total Users")
ax_fh3.set_xlabel("Order Date")
ax_fh3.set_title("Casual and Registered Users Counts per Day")
ax_fh3.tick_params(axis="x")
ax_fh3.legend(["Casual", "Registered"])

st.pyplot(fig_fh3)


# PLOT 2

st.subheader("Total Users vs Temperature")

fig_temp, ax_temp = plt.subplots(figsize=(12, 6))
ax_temp.scatter(filtered_data["casual"], filtered_data["temp"] * 41, label="Casual")
ax_temp.scatter(
    filtered_data["registered"], filtered_data["temp"] * 41, label="Registered"
)
ax_temp.set_xlabel("Total Users")
ax_temp.set_ylabel("Degree")
ax_temp.legend()
ax_temp.set_title("Relationship Between Bike User and Temperature")

st.pyplot(fig_temp)

season_data = (
    filtered_data.groupby("season")
    .agg({"registered": "sum", "casual": "sum"})
    .reset_index()
)

plot_data = filtered_data.groupby(["temp", "atemp"]).agg({"cnt": "sum"}).reset_index()


# PLOT 3
st.subheader("Users vs Hour")

cnt_hour = [
    39130,
    24164,
    16352,
    8174,
    4428,
    14261,
    55132,
    154171,
    261001,
    159438,
    126257,
    151320,
    184414,
    184919,
    175652,
    183149,
    227748,
    336860,
    309772,
    226789,
    164550,
    125445,
    95612,
    63941,
]

cnt_hour = [
    39130,
    24164,
    16352,
    8174,
    4428,
    14261,
    55132,
    154171,
    261001,
    159438,
    126257,
    151320,
    184414,
    184919,
    175652,
    183149,
    227748,
    336860,
    309772,
    226789,
    164550,
    125445,
    95612,
    63941,
]

fig_fh2, ax_fh2 = plt.subplots(figsize=(12, 6))
hours = np.arange(24)
sns.lineplot(x=hours, y=cnt_hour, ax=ax_fh2, marker="o", color="#90CAF9")
ax_fh2.set_ylabel("Count")
ax_fh2.set_xlabel("Hour")
ax_fh2.set_title("Hourly Users")
ax_fh2.set_xticks(hours)
ax_fh2.tick_params(axis="x")

for hour in [5, 10, 15, 20]:
    plt.axvline(x=hour, linestyle="--", color="red")

st.pyplot(fig_fh2)


with st.expander("Insights"):
    st.write(
        """
            - The total daily bike rentals are significantly influenced by temperature and hour of the day.
            - Rentals increase as temperature rises from 0°C to around 20°C and plateau up to 35°C.
            - Peak rentals occur at 5 PM and 8 AM, aligning with commuting hours.
            """
    )
