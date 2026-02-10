import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import folium
from streamlit_folium import st_folium
import os


# PAGE CONFIG
st.set_page_config(page_title="E-Commerce Dashboard", layout="wide")
st.title("📊 E-Commerce Analytics Dashboard")
st.caption("Data Source: Brazilian E-Commerce Public Dataset (Olist)")


# LOAD DATA
BASE_DIR = os.path.dirname(__file__)

main_df = pd.read_csv(os.path.join(BASE_DIR, "main_df.csv"))
rfm_df = pd.read_csv(os.path.join(BASE_DIR, "rfm.csv"))
geo_df = pd.read_csv(os.path.join(BASE_DIR, "customers_geo.csv"))


# DATA PREPARATION
main_df["total_price"] = main_df["price"] + main_df["freight_value"]

order_df = main_df.groupby(
    ["order_id", "order_purchase_timestamp", "customer_id"],
    as_index=False
)["total_price"].sum()

order_df["order_purchase_timestamp"] = pd.to_datetime(
    order_df["order_purchase_timestamp"]
)

# Clean geo
geo_df = geo_df.dropna(subset=["lat", "lng"])
geo_df = geo_df[
    (geo_df["lat"].between(-90, 90)) &
    (geo_df["lng"].between(-180, 180))
]


#  SIDEBAR FILTER
st.sidebar.header("🔎 Filter Data")

min_date = order_df["order_purchase_timestamp"].min()
max_date = order_df["order_purchase_timestamp"].max()

start_date, end_date = st.sidebar.date_input(
    "Select Date Range",
    [min_date, max_date]
)

filtered_orders = order_df[
    (order_df["order_purchase_timestamp"] >= pd.to_datetime(start_date)) &
    (order_df["order_purchase_timestamp"] <= pd.to_datetime(end_date))
]


# KPI SECTION
st.subheader("Key Metrics")

col1, col2, col3 = st.columns(3)

col1.metric(
    "Total Revenue",
    f"${filtered_orders['total_price'].sum():,.0f}"
)
col2.metric(
    "Total Orders",
    filtered_orders["order_id"].nunique()
)
col3.metric(
    "Total Customers",
    filtered_orders["customer_id"].nunique()
)

#Pertanyaan 1.
#Monthly Revenue Trend
st.subheader("📈 Monthly Revenue Trend")

monthly_sales = filtered_orders.groupby(
    filtered_orders["order_purchase_timestamp"].dt.to_period("M")
)["total_price"].sum()

fig, ax = plt.subplots(figsize=(10,4))
monthly_sales.plot(ax=ax)
ax.set_xlabel("Month")
ax.set_ylabel("Revenue")

st.pyplot(fig)

st.info(
"""
Insight:
Grafik ini membantu mengidentifikasi tren penjualan dari waktu ke waktu.
Gunakan filter tanggal untuk melihat performa bisnis pada periode tertentu.
"""
)


# RFM ANALYSIS
st.subheader("👥 Customer Segmentation (RFM)")

top_customers = rfm_df.sort_values("monetary", ascending=False).head(10)

st.write("Top 10 Customers by Monetary Value")
st.dataframe(top_customers)

fig, ax = plt.subplots(figsize=(6,4))
ax.scatter(
    rfm_df["recency"],
    rfm_df["monetary"],
    alpha=0.5
)

ax.set_xlabel("Recency (days)")
ax.set_ylabel("Monetary")

st.pyplot(fig)

st.info(
"""
Insight:
Customer dengan monetary tinggi dan recency rendah adalah pelanggan terbaik
yang berpotensi menjadi target loyalty program.
"""
)


# Pertanyaan 2
# GEOSPATIAL
st.subheader("🗺️ Customer Distribution")

map_center = [
    geo_df["lat"].mean(),
    geo_df["lng"].mean()
]

m = folium.Map(location=map_center, zoom_start=4)

sample_size = min(700, len(geo_df))

for _, row in geo_df.sample(sample_size, random_state=42).iterrows():
    folium.CircleMarker(
        location=[row["lat"], row["lng"]],
        radius=2,
        fill=True,
        fill_opacity=0.6
    ).add_to(m)

st_folium(m, width=900)

st.info(
"""
Insight:
Peta ini menunjukkan persebaran pelanggan.
Area dengan kepadatan tinggi menjadi fokus strategi marketing dan logistik.
"""
)
