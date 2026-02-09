# E-Commerce Dashboard Analysis

## 📌 Deskripsi Proyek

Proyek ini bertujuan untuk menganalisis performa bisnis e-commerce menggunakan dataset Olist.
Analisis dilakukan melalui proses data cleaning, exploratory data analysis (EDA),
serta visualisasi data dalam bentuk dashboard interaktif menggunakan Streamlit.

## 📂 Struktur Folder

DASBOARD E-COMMERCE
├── dashboard
│ ├── dashboard.py
│ ├── main_df.csv
│ ├── rfm.csv
│ └── customers_geo.csv
├── data
│ ├── customers_dataset.csv
│ ├── orders_dataset.csv
│ ├── order_items_dataset.csv
│ └── ...
├── Proyek_Analisis_Data.ipynb
├── requirements.txt
└── README.md

## 🛠 Library yang Digunakan

- pandas
- matplotlib
- streamlit
- folium
- streamlit-folium

## ▶️ Cara Menjalankan Dashboard

1. Buka terminal (Command Prompt / PowerShell / Terminal VS Code)
2. Masuk ke folder proyek
3. Install dependencies:
   pip install -r requirements.txt
4. Jalankan dashboard:
   python -m streamlit run dashboard/dashboard.py
5. Dashboard akan terbuka otomatis di browser.

## 📊 Insight yang Ditampilkan

- Total Revenue
- Total Orders
- Total Customers
- Tren Penjualan Bulanan
- Segmentasi Pelanggan (RFM)
- Distribusi Pelanggan berdasarkan Lokasi

Ari Dwi Prasetyo - E-Commerce Dataset
