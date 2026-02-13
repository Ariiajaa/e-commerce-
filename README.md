# 🛒 E-Commerce Olist Analysis Dashboard

[![Python](https://img.shields.io/badge/Python-3.9+-blue.svg)](https://www.python.org/downloads/)
[![Streamlit](https://img.shields.io/badge/Streamlit-1.28+-red.svg)](https://streamlit.io)
[![License](https://img.shields.io/badge/License-MIT-green.svg)](LICENSE)

Analisis komprehensif terhadap dataset E-Commerce publik dari Olist Brazil, mencakup RFM Analysis, Geospatial Analysis, Product Clustering, dan Interactive Dashboard.

---

## 📋 Daftar Isi

- [Tentang Proyek](#-tentang-proyek)
- [Struktur Proyek](#-struktur-proyek)
- [Instalasi](#-instalasi)
- [Cara Menjalankan](#-cara-menjalankan)
- [Pertanyaan Bisnis](#-pertanyaan-bisnis)
- [Analisis Lanjutan](#-analisis-lanjutan)
- [Dashboard](#-dashboard)
- [Hasil Analisis](#-hasil-analisis)
- [Teknologi](#-teknologi)

---

## 📖 Tentang Proyek

Proyek ini merupakan analisis mendalam terhadap **Brazilian E-Commerce Public Dataset by Olist** yang berisi informasi tentang 100,000+ pesanan dari September 2016 hingga Agustus 2018.

**Dataset**: [Kaggle - Brazilian E-Commerce](https://www.kaggle.com/datasets/olistbr/brazilian-ecommerce)

**Periode Data**: September 2016 - Agustus 2018  
**Total Orders**: 99,441  
**Total Customers**: 99,441  
**States Coverage**: 27 states di Brazil

---

## 📁 Struktur Proyek

```
Dasboard e-commerce/
├── dashboard/
│   ├── dashboard.py           # Streamlit dashboard utama
│   ├── main_df.csv            # Dataset yang sudah dibersihkan
│   └── rfm.csv                # Hasil RFM analysis
│
├── data/                      # ⭐ Folder dataset (CSV files)
│   ├── customers_dataset.csv
│   ├── geolocation_dataset.csv
│   ├── order_items_dataset.csv
│   ├── order_payments_dataset.csv
│   ├── order_reviews_dataset.csv
│   ├── orders_dataset.csv
│   ├── product_category_name_translation.csv
│   ├── products_dataset.csv
│   └── sellers_dataset.csv
│
├── venv/                      # Virtual environment
│
├── README.md                  # Dokumentasi utama (file ini)
├── requirements.txt           # Python dependencies
├── ecommerce_analysis_fixed.py      # Script analisis utama
├── advanced_analysis.py             # Script analisis lanjutan
└── ADVANCED_INSIGHTS.md             # Insights mendalam
```

---

## 🚀 Instalasi

### 1. Clone atau Download Project

```bash
# Download project
cd "Dasboard e-commerce"
```

### 2. Buat Virtual Environment

```bash
# Windows
python -m venv venv
venv\Scripts\activate

# Mac/Linux
python3 -m venv venv
source venv/bin/activate
```

### 3. Install Dependencies

```bash
pip install -r requirements.txt
```

**Dependencies yang dibutuhkan:**

- streamlit
- pandas
- numpy
- matplotlib
- seaborn
- plotly
- folium

### 4. Download Dataset

1. Download dari [Kaggle](https://www.kaggle.com/datasets/olistbr/brazilian-ecommerce)
2. Extract semua CSV files
3. Letakkan di folder `data/`

### 5. Verifikasi

```bash
# Check data files
dir data\*.csv  # Windows
ls data/*.csv   # Mac/Linux
```

Pastikan ada minimal 6 files:

- ✅ orders_dataset.csv
- ✅ order_items_dataset.csv
- ✅ products_dataset.csv
- ✅ customers_dataset.csv
- ✅ order_reviews_dataset.csv
- ✅ product_category_name_translation.csv

---

## 🎯 Cara Menjalankan

### Menjalankan Dashboard

```bash
# Masuk ke folder dashboard
cd dashboard

# Run Streamlit
streamlit run dashboard.py
```

Dashboard akan terbuka di: `http://localhost:8502`

### Troubleshooting

**❌ Error: "FileNotFoundError: orders_dataset.csv"**

✅ **Solusi**: Pastikan file CSV ada di folder `data/`

```
Struktur yang BENAR:
Dasboard e-commerce/
├── dashboard/
│   └── dashboard.py
└── data/              ← CSV files harus di sini!
    ├── orders_dataset.csv
    └── ...
```

**❌ Error: "ModuleNotFoundError: streamlit"**

✅ **Solusi**:

```bash
pip install streamlit pandas plotly
```

**❌ Error: "Port 8502 already in use"**

✅ **Solusi**:

```bash
streamlit run dashboard.py --server.port 8503
```

---

## 🔍 Pertanyaan Bisnis

### Question 1: Dampak Keterlambatan Pengiriman (2017)

**Pertanyaan:**

> Bagaimana hubungan antara keterlambatan pengiriman dengan tingkat kepuasan pelanggan, dan seberapa besar perbedaan rata-rata rating antara pesanan tepat waktu dan terlambat pada tahun 2017?

**Hasil:**

- On-time (92.5%): Rating **4.15** ⭐
- Delayed (7.5%): Rating **2.45** ⭐
- Perbedaan: **1.70 poin (40.9% penurunan)**

**Kesimpulan:**  
Keterlambatan pengiriman meskipun hanya 7.5%, mengakibatkan penurunan kepuasan yang sangat signifikan (40.9%).

---

### Question 2: Kontribusi Kategori Produk (2018)

**Pertanyaan:**

> Seberapa besar kontribusi 5 kategori teratas terhadap total revenue, dan bagaimana pola harga serta volume berbeda antar kategori pada tahun 2018?

**Hasil:**

- Top 5 kategori: **65.4%** dari total revenue
- **health_beauty** (15.2%): R$ 129 avg, 8,836 orders
- **watches_gifts** (14.5%): R$ 201 avg (premium)
- **bed_bath_table** (12.8%): R$ 93 avg, 9,417 orders (volume)

**Kesimpulan:**  
Konsentrasi revenue tinggi pada top 5 dengan strategi berbeda: premium pricing, volume-based, dan balanced approach.

---

## 🎨 Analisis Lanjutan

### 1. RFM Analysis

**10 Customer Segments:**

- 🏆 Champions
- 💎 Loyal Customers
- 🌟 Potential Loyalist
- 👶 New Customers (66.9%)
- ⚠️ At Risk
- 🚨 Can't Lose Them
- 😴 Hibernating
- 💤 About to Sleep
- 💡 Promising
- 🔍 Need Attention

**Critical Finding:**  
Hanya **7 loyal customers (0.01%)** dari 94,000+ total!

**Opportunity:** +R$ 4.6M melalui retention

---

### 2. Geospatial Analysis

**Key Findings:**

- SP dominasi: **47.5%** orders
- Top 3 states: **75.2%** orders
- Northeast underserved: 28% populasi → 6% orders

**Opportunity:** +R$ 3.5M melalui ekspansi geografis

**Output:**

- `map_brazil_orders.html` (interactive map)
- `map_brazil_heatmap.html` (heatmap)

---

### 3. Product Clustering

**9 Segments:**

1. 💎 Hidden Gems (31.3%) - R$ 27M locked!
2. 🏆 Value Champions (27.7%) - Winning formula
3. 🔥 Best Sellers (14.0%)
4. 👑 Premium Stars (1.4%) - Only 66 products
5. ⚠️ Low Quality (8.4%)
6. 🐌 Slow Movers (4.9%)
7. Others (10.6%)

**Opportunity:** +R$ 42.5M melalui portfolio optimization

---

## 📊 Dashboard

### 6 Halaman Interaktif:

1. **📊 Overview**
   - Business metrics
   - Monthly trends
   - Top categories

2. **📈 Business Questions**
   - Question 1: Delivery impact
   - Question 2: Category revenue

3. **👥 RFM Analysis**
   - Customer segments
   - Revenue contribution
   - Scatter plots

4. **🗺️ Geospatial Analysis**
   - Top states
   - Geographic map
   - Regional insights

5. **🎯 Product Clustering**
   - Product segments
   - Distribution charts
   - Recommendations

6. **📋 Conclusions**
   - Executive summary
   - Key findings
   - Action plan

---

## 📈 Hasil Analisis

### Business Metrics

- 📦 Total Orders: **99,441**
- 💰 Total Revenue: **R$ 13.2M**
- ⭐ Avg Review: **4.08/5**
- 📊 Avg Order Value: **R$ 137**

### Critical Findings

1. **Retention Crisis**: 0.01% loyal customers
2. **Geographic Risk**: 47.5% dependent on SP
3. **Portfolio Underutilization**: 31.3% Hidden Gems

### Total Opportunity

| Initiative           | Impact                |
| -------------------- | --------------------- |
| RFM Optimization     | +R$ 4.6M              |
| Geographic Expansion | +R$ 3.5M              |
| Product Portfolio    | +R$ 42.5M             |
| **TOTAL**            | **+R$ 50.6M (+384%)** |

### Strategic Actions

**Phase 1 (0-3 months)**: Quick wins → +R$ 3.3M  
**Phase 2 (3-6 months)**: Build engine → +R$ 3.7M  
**Phase 3 (6-12 months)**: Scale → +R$ 42.5M

---

## 🛠️ Teknologi

- **Python 3.9+**
- **Streamlit** - Interactive dashboard
- **Pandas** - Data manipulation
- **Plotly** - Interactive visualizations
- **Folium** - Geographic maps
- **Matplotlib & Seaborn** - Statistical plots

---

## 📚 Dokumentasi Lengkap

**File Dokumentasi:**

1. `README.md` - Overview (file ini)
2. `STREAMLIT_GUIDE.md` - Panduan dashboard
3. `QUICK_START.md` - Quick start guide
4. `ADVANCED_INSIGHTS.md` - Insights mendalam
5. `CONCLUSION_PARAGRAPHS.md` - Kesimpulan paragraf

**Scripts:**

1. `ecommerce_analysis_fixed.py` - Main analysis
2. `advanced_analysis.py` - RFM, Geo, Clustering
3. `dashboard.py` - Streamlit dashboard

---

## 🎯 Quick Start

```bash
# 1. Install dependencies
pip install -r requirements.txt

# 2. Ensure data/ folder has CSV files
ls data/*.csv

# 3. Run dashboard
cd dashboard
streamlit run dashboard.py

# 4. Open browser
# http://localhost:8502
```

---

## 📞 Support

Jika ada masalah:

1. Pastikan struktur folder benar
2. Check semua CSV files ada di `data/`
3. Verifikasi dependencies terinstall
4. Lihat troubleshooting di atas

---

## 🙏 Credits

- **Dataset**: Olist via Kaggle
- **Framework**: Streamlit

---

**Made with ❤️ and ☕**

**Last Updated**: February 2026

---

**Happy Analyzing! 📊✨**

Untuk panduan lengkap, lihat:

- [Streamlit Guide](STREAMLIT_GUIDE.md)
- [Advanced Insights](ADVANCED_INSIGHTS.md)
- [Quick Start](QUICK_START.md)
