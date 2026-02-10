# 📊 E-Commerce Dashboard Analysis

## 📌 Deskripsi Proyek

Proyek ini bertujuan untuk menganalisis performa bisnis e-commerce menggunakan **Brazilian E-Commerce Public Dataset (Olist)**.  
Analisis dilakukan melalui tahapan:

- Data Cleaning
- Exploratory Data Analysis (EDA)
- Customer Segmentation (RFM)
- Interactive Data Visualization menggunakan **Streamlit**

Dashboard dibuat agar pengguna dapat mengeksplorasi data secara mandiri melalui filter interaktif.

---

## 🎯 Tujuan Analisis

- Mengidentifikasi tren revenue dari waktu ke waktu
- Mengetahui jumlah pelanggan dan pertumbuhan order
- Melakukan segmentasi pelanggan menggunakan metode **RFM**
- Menganalisis persebaran geografis pelanggan

---

## 📂 Struktur Folder

DASHBOARD E-COMMERCE
├── dashboard
│ ├── dashboard.py
│ ├── main_df.csv
│ ├── rfm.csv
│ └── customers_geo.csv
├── data
│ ├── customers_dataset.csv
│ ├── orders_dataset.csv
│ ├── order_items_dataset.csv
│ └── lainnya..
├── Proyek_Analisis_Data.ipynb
├── requirements.txt
└── README.md

---

## 🛠 Library yang Digunakan

- pandas
- matplotlib
- streamlit
- folium
- streamlit-folium

---

## ⚙️ Cara Menjalankan Dashboard

Masuk ke folder project:

cd dashboard-ecommerce

---

### 2️⃣ Buat Virtual Environment

python -m venv venv

---

### 3️⃣ Aktifkan Virtual Environment

**Windows:**

venv\Scripts\activate

**Mac/Linux:**

source venv/bin/activate

---

### 4️⃣ Install Dependencies

pip install -r requirements.txt

---

### 5️⃣ Jalankan Dashboard

streamlit run dashboard/dashboard.py

Dashboard akan otomatis terbuka di browser.

---

## 📊 Insight yang Ditampilkan

Dashboard menyediakan fitur interaktif sehingga pengguna dapat mengeksplorasi data lebih dalam.

Beberapa insight utama:

✅ Total Revenue  
✅ Total Orders  
✅ Total Customers  
✅ Monthly Revenue Trend  
✅ Customer Segmentation (RFM)  
✅ Customer Geographic Distribution

---

## Dataset

Dataset: **Brazilian E-Commerce Public Dataset by Olist**
