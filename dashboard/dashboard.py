import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import plotly.express as px
import plotly.graph_objects as go
from datetime import datetime
import numpy as np

# Page configuration
st.set_page_config(
    page_title="E-Commerce Analysis Dashboard",
    page_icon="🛒",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Custom CSS
st.markdown("""
    <style>
    .main {
        padding: 0rem 1rem;
    }
   .stMetric {
    background: linear-gradient(145deg, #1e1e1e, #2a2a2a);
    padding: 15px;
    border-radius: 12px;
    border: 1px solid #333;
}
    h1 {
        color: #1f77b4;
    }
    h2 {
        color: #2ca02c;
    }
    </style>
    """, unsafe_allow_html=True)

# Title
st.title("🛒 E-Commerce Analysis Dashboard")
st.markdown("---")

# Sidebar
st.sidebar.title("Navigation")
page = st.sidebar.radio(
    "Choose a page:",
    ["📊 Overview", "📈 Business Questions", "👥 RFM Analysis", 
     "🗺️ Geospatial Analysis", "🎯 Product Clustering", "📋 Conclusions"]
)

# Load data 
@st.cache_data
def load_data():
    """Load all datasets"""
    import os
    
    # Try different possible paths
    possible_paths = [
        "data/",      
        "./data/",    
        "../data/",   
        "./",         
    ]
    
    data_path = None
    for path in possible_paths:
        if os.path.exists(os.path.join(path, "orders_dataset.csv")):
            data_path = path
            st.info(f"✅ Data found in: {os.path.abspath(path)}")
            break
    
    if data_path is None:
        st.error("❌ Data files not found in any expected location.")
        st.info("""
        **Expected file locations (one of these):**
        - `data/orders_dataset.csv`
        - `./data/orders_dataset.csv`
        - `orders_dataset.csv` (same folder as dashboard.py)
        
        **Current working directory:** `{}`
        """.format(os.getcwd()))
        return None, None, None
    
    try:
        orders = pd.read_csv(os.path.join(data_path, "orders_dataset.csv"))
        order_items = pd.read_csv(os.path.join(data_path, "order_items_dataset.csv"))
        products = pd.read_csv(os.path.join(data_path, "products_dataset.csv"))
        customers = pd.read_csv(os.path.join(data_path, "customers_dataset.csv"))
        reviews = pd.read_csv(os.path.join(data_path, "order_reviews_dataset.csv"))
        category = pd.read_csv(os.path.join(data_path, "product_category_name_translation.csv"))
        
        # Convert datetime
        datetime_cols = ["order_purchase_timestamp", "order_approved_at", 
                        "order_delivered_customer_date", "order_estimated_delivery_date"]
        for col in datetime_cols:
            orders[col] = pd.to_datetime(orders[col])
        
        # Merge products with category
        products = products.merge(category, on="product_category_name", how="left")
        
        # Create delivery features
        orders["delivery_time"] = (orders["order_delivered_customer_date"] - 
                                   orders["order_purchase_timestamp"]).dt.days
        orders["estimated_time"] = (orders["order_estimated_delivery_date"] - 
                                    orders["order_purchase_timestamp"]).dt.days
        orders["is_delayed"] = orders["delivery_time"] > orders["estimated_time"]
        
        # Create main dataframe
        main_df = orders.merge(order_items, on="order_id")
        main_df = main_df.merge(products, on="product_id")
        main_df = main_df.merge(customers, on="customer_id")
        main_df = main_df.merge(reviews[["order_id", "review_score"]], on="order_id", how="left")
        
        # Add year and month
        main_df["order_year"] = main_df["order_purchase_timestamp"].dt.year
        main_df["order_month"] = main_df["order_purchase_timestamp"].dt.month
        
        return main_df, orders, customers
    except FileNotFoundError as e:
        st.error(f"Error loading data: {e}")
        st.info("Please make sure all CSV files are in the same directory as this script.")
        return None, None, None

# Load data
main_df, orders_df, customers_df = load_data()

if main_df is not None:
    
    # PAGE: OVERVIEW 
    if page == "📊 Overview":
        st.header("📊 Business Overview")
        
        # Key Metrics
        col1, col2, col3, col4, col5 = st.columns(5)
        
        with col1:
            total_orders = len(main_df["order_id"].unique())
            st.metric("Total Orders", f"{total_orders:,}")
        
        with col2:
            total_revenue = main_df["price"].sum()
            st.metric("Total Revenue", f"R$ {total_revenue:,.2f}")
        
        with col3:
            total_customers = len(main_df["customer_id"].unique())
            st.metric("Total Customers", f"{total_customers:,}")
        
        with col4:
            avg_order_value = main_df.groupby("order_id")["price"].sum().mean()
            st.metric("Avg Order Value", f"R$ {avg_order_value:,.2f}")
        
        with col5:
            avg_review = main_df["review_score"].mean()
            st.metric("Avg Review Score", f"{avg_review:.2f} ⭐")
        
        st.markdown("---")
        
        # Row 1: Time Series and Order Status
        col1, col2 = st.columns(2)
        
        with col1:
            st.subheader("📅 Orders Over Time")
            
            # Monthly trend
            monthly_orders = main_df.groupby(["order_year", "order_month"]).agg({
                "order_id": "nunique"
            }).reset_index()
            monthly_orders["date"] = pd.to_datetime(
                monthly_orders["order_year"].astype(str) + "-" + 
                monthly_orders["order_month"].astype(str) + "-01"
            )
            
            fig = px.line(monthly_orders, x="date", y="order_id",
                         labels={"order_id": "Number of Orders", "date": "Month"},
                         title="Monthly Order Trends")
            fig.update_traces(line_color='#1f77b4', line_width=3)
            st.plotly_chart(fig, use_container_width=True)
        
        with col2:
            st.subheader("📦 Order Status Distribution")
            
            status_counts = main_df["order_status"].value_counts()
            
            fig = px.pie(values=status_counts.values, names=status_counts.index,
                        title="Order Status Breakdown",
                        color_discrete_sequence=px.colors.qualitative.Set3)
            st.plotly_chart(fig, use_container_width=True)
        
        st.markdown("---")
        
        # Row 2: Top Categories and Review Distribution
        col1, col2 = st.columns(2)
        
        with col1:
            st.subheader("🏆 Top 10 Product Categories")
            
            top_categories = main_df.groupby("product_category_name_english").agg({
                "price": "sum"
            }).sort_values("price", ascending=False).head(10).reset_index()
            
            fig = px.bar(top_categories, x="price", y="product_category_name_english",
                        orientation="h",
                        labels={"price": "Revenue (R$)", 
                               "product_category_name_english": "Category"},
                        title="Top Categories by Revenue",
                        color="price",
                        color_continuous_scale="Blues")
            fig.update_layout(showlegend=False, yaxis={'categoryorder':'total ascending'})
            st.plotly_chart(fig, use_container_width=True)
        
        with col2:
            st.subheader("⭐ Review Score Distribution")
            
            review_dist = main_df["review_score"].value_counts().sort_index()
            
            fig = go.Figure(data=[
                go.Bar(x=review_dist.index, y=review_dist.values,
                      marker_color=['#d62728', '#ff7f0e', '#ffbb78', '#98df8a', '#2ca02c'])
            ])
            fig.update_layout(
                title="Distribution of Review Scores",
                xaxis_title="Review Score",
                yaxis_title="Number of Reviews",
                showlegend=False
            )
            st.plotly_chart(fig, use_container_width=True)
        
        st.markdown("---")
        
        # Data Summary Table
        st.subheader("📋 Dataset Summary")
        
        col1, col2, col3 = st.columns(3)
        
        with col1:
            st.info("**Total Products**")
            st.write(f"{len(main_df['product_id'].unique()):,}")
            
        with col2:
            st.info("**Total Sellers**")
            st.write(f"{len(main_df['seller_id'].unique()):,}")
            
        with col3:
            st.info("**Date Range**")
            st.write(f"{main_df['order_purchase_timestamp'].min().date()} to {main_df['order_purchase_timestamp'].max().date()}")
    
    # PAGE BUSINESS QUESTIONS 
    elif page == "📈 Business Questions":
        st.header("📈 Business Questions Analysis")
        
        # Question selector
        question = st.selectbox(
            "Select a question:",
            ["Question 1: Delivery Performance vs Customer Satisfaction (2017)",
             "Question 2: Top Categories Revenue Contribution (2018)"]
        )
        
        if "Question 1" in question:
            st.subheader("❓ Question 1: Delivery Performance Impact")
            st.markdown("""
            **Bagaimana hubungan antara keterlambatan pengiriman dengan tingkat kepuasan pelanggan 
            (review score), dan seberapa besar perbedaan rata-rata rating antara pesanan yang 
            tepat waktu dan terlambat pada tahun 2017?**
            """)
            
            # Filter 2017 data
            df_2017 = main_df[main_df["order_year"] == 2017].copy()
            
            # Calculate stats
            delay_stats = df_2017.groupby("is_delayed")["review_score"].agg([
                "mean", "count", "std"
            ]).reset_index()
            
            on_time_avg = delay_stats[delay_stats["is_delayed"] == False]["mean"].values[0]
            delayed_avg = delay_stats[delay_stats["is_delayed"] == True]["mean"].values[0]
            difference = on_time_avg - delayed_avg
            
            # Key Metrics
            col1, col2, col3, col4 = st.columns(4)
            
            with col1:
                st.metric("On-Time Avg Review", f"{on_time_avg:.2f} ⭐")
            with col2:
                st.metric("Delayed Avg Review", f"{delayed_avg:.2f} ⭐")
            with col3:
                st.metric("Difference", f"{difference:.2f}", delta=f"-{(difference/on_time_avg*100):.1f}%")
            with col4:
                on_time_pct = (delay_stats[delay_stats["is_delayed"] == False]["count"].values[0] / 
                              delay_stats["count"].sum() * 100)
                st.metric("On-Time Rate", f"{on_time_pct:.1f}%")
            
            st.markdown("---")
            
            # Visualizations
            col1, col2 = st.columns(2)
            
            with col1:
                st.subheader("📊 Average Review Score Comparison")
                
                fig = go.Figure(data=[
                    go.Bar(x=["On-Time Delivery", "Delayed Delivery"],
                          y=[on_time_avg, delayed_avg],
                          marker_color=['#2ecc71', '#e74c3c'],
                          text=[f"{on_time_avg:.2f}", f"{delayed_avg:.2f}"],
                          textposition='outside')
                ])
                fig.update_layout(
                    yaxis_title="Average Review Score",
                    yaxis_range=[0, 5],
                    showlegend=False
                )
                st.plotly_chart(fig, use_container_width=True)
            
            with col2:
                st.subheader("📊 Review Distribution")
                
                on_time_dist = df_2017[df_2017["is_delayed"] == False]["review_score"].value_counts()
                delayed_dist = df_2017[df_2017["is_delayed"] == True]["review_score"].value_counts()
                
                fig = go.Figure(data=[
                    go.Bar(name='On-Time', x=[1,2,3,4,5], 
                          y=[on_time_dist.get(i, 0) for i in range(1,6)],
                          marker_color='#2ecc71'),
                    go.Bar(name='Delayed', x=[1,2,3,4,5], 
                          y=[delayed_dist.get(i, 0) for i in range(1,6)],
                          marker_color='#e74c3c')
                ])
                fig.update_layout(
                    barmode='group',
                    xaxis_title="Review Score",
                    yaxis_title="Count"
                )
                st.plotly_chart(fig, use_container_width=True)
            
            # Insights
            st.markdown("---")
            st.subheader("💡 Key Insights")
            
            col1, col2 = st.columns(2)
            
            with col1:
                st.success(f"""
                **On-Time Delivery Performance:**
                - Average rating: {on_time_avg:.2f} stars
                - {on_time_pct:.1f}% of all deliveries
                - Customers are highly satisfied
                """)
            
            with col2:
                st.error(f"""
                **Delayed Delivery Impact:**
                - Average rating: {delayed_avg:.2f} stars
                - {difference:.2f} points lower ({(difference/on_time_avg*100):.1f}% decrease)
                - Significant negative impact on satisfaction
                """)
        
        else:  # Question 2
            st.subheader("❓ Question 2: Category Revenue Analysis")
            st.markdown("""
            **Seberapa besar kontribusi 5 kategori produk teratas terhadap total revenue, 
            dan bagaimana pola harga rata-rata serta volume penjualan berbeda di antara 
            kategori-kategori tersebut pada periode tahun 2018?**
            """)
            
            # Filter 2018 data
            df_2018 = main_df[main_df["order_year"] == 2018].copy()
            
            # Calculate top 5 categories
            category_stats = df_2018.groupby("product_category_name_english").agg({
                "price": "sum",
                "order_id": "nunique"
            }).sort_values("price", ascending=False).head(5).reset_index()
            category_stats.columns = ["Category", "Total_Revenue", "Total_Orders"]
            category_stats["Avg_Price"] = category_stats["Total_Revenue"] / category_stats["Total_Orders"]
            
            total_revenue_2018 = df_2018["price"].sum()
            category_stats["Contribution_%"] = (category_stats["Total_Revenue"] / total_revenue_2018 * 100)
            
            top_5_contribution = category_stats["Contribution_%"].sum()
            
            # Key Metrics
            col1, col2, col3, col4 = st.columns(4)
            
            with col1:
                st.metric("Total Revenue 2018", f"R$ {total_revenue_2018:,.0f}")
            with col2:
                st.metric("Top 5 Contribution", f"{top_5_contribution:.1f}%")
            with col3:
                st.metric("Top Category", category_stats.iloc[0]["Category"])
            with col4:
                st.metric("Top Revenue", f"R$ {category_stats.iloc[0]['Total_Revenue']:,.0f}")
            
            st.markdown("---")
            
            # Visualizations
            col1, col2 = st.columns(2)
            
            with col1:
                st.subheader("🥧 Revenue Contribution")
                
                # Add "Others" category
                others_revenue = total_revenue_2018 - category_stats["Total_Revenue"].sum()
                others_pct = (others_revenue / total_revenue_2018 * 100)
                
                labels = list(category_stats["Category"]) + ["Others"]
                values = list(category_stats["Contribution_%"]) + [others_pct]
                
                fig = px.pie(values=values, names=labels,
                            title="Revenue Contribution by Category",
                            color_discrete_sequence=px.colors.qualitative.Set3)
                st.plotly_chart(fig, use_container_width=True)
            
            with col2:
                st.subheader("📊 Price vs Volume Analysis")
                
                fig = go.Figure()
                
                fig.add_trace(go.Bar(
                    name='Average Price',
                    x=category_stats["Category"],
                    y=category_stats["Avg_Price"],
                    marker_color='#3498db'
                ))
                
                fig.add_trace(go.Scatter(
                    name='Total Orders',
                    x=category_stats["Category"],
                    y=category_stats["Total_Orders"],
                    yaxis='y2',
                    marker_color='#e74c3c',
                    mode='lines+markers',
                    line=dict(width=3)
                ))
                
                fig.update_layout(
                    yaxis=dict(title='Average Price (R$)'),
                    yaxis2=dict(title='Total Orders', overlaying='y', side='right'),
                    hovermode='x unified'
                )
                
                st.plotly_chart(fig, use_container_width=True)
            
            # Data Table
            st.markdown("---")
            st.subheader("📋 Detailed Statistics")
            
            display_df = category_stats.copy()
            display_df["Total_Revenue"] = display_df["Total_Revenue"].apply(lambda x: f"R$ {x:,.2f}")
            display_df["Avg_Price"] = display_df["Avg_Price"].apply(lambda x: f"R$ {x:.2f}")
            display_df["Contribution_%"] = display_df["Contribution_%"].apply(lambda x: f"{x:.2f}%")
            
            st.dataframe(display_df, use_container_width=True)
            
            # Insights
            st.markdown("---")
            st.subheader("💡 Key Insights")
            
            st.info(f"""
            **Strategic Insights:**
            - Top 5 categories contribute **{top_5_contribution:.1f}%** of total revenue
            - Remaining **{100-top_5_contribution:.1f}%** distributed across other categories
            - Different strategies: **High volume** (bed_bath_table) vs **Premium pricing** (watches_gifts)
            - Balanced approach (health_beauty) shows best performance
            """)
    
    # PAGE RFM ANALYSIS
    elif page == "👥 RFM Analysis":
        st.header("👥 RFM Analysis - Customer Segmentation")
        
        st.markdown("""
        RFM Analysis segments customers based on:
        - **Recency**: How recently did they purchase?
        - **Frequency**: How often do they purchase?
        - **Monetary**: How much do they spend?
        """)
        
        # Calculate RFM
        rfm_df = main_df[main_df["order_status"] == "delivered"].copy()
        reference_date = rfm_df["order_purchase_timestamp"].max() + pd.Timedelta(days=1)
        
        rfm_analysis = rfm_df.groupby("customer_id").agg({
            "order_purchase_timestamp": lambda x: (reference_date - x.max()).days,
            "order_id": "count",
            "price": "sum"
        }).reset_index()
        rfm_analysis.columns = ["customer_id", "Recency", "Frequency", "Monetary"]
        
        # RFM Scoring
        rfm_analysis["R_Score"] = pd.cut(rfm_analysis["Recency"], bins=5, labels=[5,4,3,2,1]).astype(int)
        rfm_analysis["F_Score"] = pd.cut(rfm_analysis["Frequency"], bins=5, labels=[1,2,3,4,5]).astype(int)
        rfm_analysis["M_Score"] = pd.cut(rfm_analysis["Monetary"], bins=5, labels=[1,2,3,4,5]).astype(int)
        rfm_analysis["Total_Score"] = rfm_analysis["R_Score"] + rfm_analysis["F_Score"] + rfm_analysis["M_Score"]
        
        # Segmentation
        def rfm_segment(row):
            r, f, m = row["R_Score"], row["F_Score"], row["M_Score"]
            if r >= 4 and f >= 4 and m >= 4: return "Champions"
            elif r >= 3 and f >= 4: return "Loyal Customers"
            elif r >= 4 and f >= 2 and m >= 2: return "Potential Loyalist"
            elif r >= 4 and f == 1: return "New Customers"
            elif r <= 2 and f >= 3 and m >= 3: return "At Risk"
            elif r <= 2 and f >= 4 and m >= 4: return "Can't Lose Them"
            elif r <= 2 and f <= 2: return "Hibernating"
            elif r == 3 and f <= 2: return "About to Sleep"
            elif r >= 4 and f == 2: return "Promising"
            else: return "Need Attention"
        
        rfm_analysis["Segment"] = rfm_analysis.apply(rfm_segment, axis=1)
        
        # Key Metrics
        col1, col2, col3, col4 = st.columns(4)
        
        with col1:
            st.metric("Total Customers", f"{len(rfm_analysis):,}")
        with col2:
            st.metric("Avg Recency", f"{rfm_analysis['Recency'].mean():.0f} days")
        with col3:
            st.metric("Avg Frequency", f"{rfm_analysis['Frequency'].mean():.1f} orders")
        with col4:
            st.metric("Avg Monetary", f"R$ {rfm_analysis['Monetary'].mean():.2f}")
        
        st.markdown("---")
        
        # Segment Distribution
        col1, col2 = st.columns(2)
        
        with col1:
            st.subheader("👥 Customer Segment Distribution")
            
            segment_counts = rfm_analysis["Segment"].value_counts()
            
            fig = px.bar(x=segment_counts.values, y=segment_counts.index,
                        orientation='h',
                        labels={"x": "Number of Customers", "y": "Segment"},
                        color=segment_counts.values,
                        color_continuous_scale="Blues")
            fig.update_layout(showlegend=False, yaxis={'categoryorder':'total ascending'})
            st.plotly_chart(fig, use_container_width=True)
        
        with col2:
            st.subheader("💰 Revenue by Segment")
            
            segment_revenue = rfm_analysis.groupby("Segment")["Monetary"].sum().sort_values(ascending=False)
            
            fig = px.bar(x=segment_revenue.values, y=segment_revenue.index,
                        orientation='h',
                        labels={"x": "Total Revenue (R$)", "y": "Segment"},
                        color=segment_revenue.values,
                        color_continuous_scale="Greens")
            fig.update_layout(showlegend=False, yaxis={'categoryorder':'total ascending'})
            st.plotly_chart(fig, use_container_width=True)
        
        # Scatter Plot
        st.markdown("---")
        st.subheader("📊 RFM Scatter Analysis")
        
        scatter_option = st.selectbox(
            "Select plot:",
            ["Recency vs Monetary", "Frequency vs Monetary", "Recency vs Frequency"]
        )
        
        if scatter_option == "Recency vs Monetary":
            x_col, y_col = "Recency", "Monetary"
        elif scatter_option == "Frequency vs Monetary":
            x_col, y_col = "Frequency", "Monetary"
        else:
            x_col, y_col = "Recency", "Frequency"
        
        fig = px.scatter(rfm_analysis, x=x_col, y=y_col, color="Segment",
                        size="Total_Score", hover_data=["customer_id"],
                        color_discrete_sequence=px.colors.qualitative.Set3)
        fig.update_layout(height=500)
        st.plotly_chart(fig, use_container_width=True)
        
        # Segment Details
        st.markdown("---")
        st.subheader("📋 Segment Details & Recommendations")
        
        segment_details = {
            "Champions": {
                "emoji": "🏆",
                "desc": "Best customers - High value, frequent buyers",
                "strategy": "Reward loyalty, VIP treatment, early access to new products"
            },
            "Loyal Customers": {
                "emoji": "💎",
                "desc": "Regular, reliable customers",
                "strategy": "Upsell higher value products, ask for reviews and referrals"
            },
            "Potential Loyalist": {
                "emoji": "🌟",
                "desc": "Recent customers with good potential",
                "strategy": "Offer membership programs, recommend related products"
            },
            "At Risk": {
                "emoji": "⚠️",
                "desc": "Used to be good customers, now inactive",
                "strategy": "Send win-back campaigns, special offers, surveys"
            },
            "Hibernating": {
                "emoji": "😴",
                "desc": "Haven't purchased in a long time",
                "strategy": "Re-engagement emails, special discounts, or let go"
            }
        }
        
        selected_segment = st.selectbox("Select segment for details:", 
                                       list(segment_details.keys()))
        
        if selected_segment:
            info = segment_details[selected_segment]
            segment_data = rfm_analysis[rfm_analysis["Segment"] == selected_segment]
            
            col1, col2, col3 = st.columns([1, 2, 2])
            
            with col1:
                st.markdown(f"## {info['emoji']}")
                st.metric("Customers", f"{len(segment_data):,}")
            
            with col2:
                st.markdown(f"**Description:**")
                st.info(info['desc'])
            
            with col3:
                st.markdown(f"**Strategy:**")
                st.success(info['strategy'])
    
    # PAGE GEOSPATIAL ANALYSIS 
    elif page == "🗺️ Geospatial Analysis":
        st.header("🗺️ Geospatial Analysis - Geographic Distribution")
        
        st.info("📌 For interactive maps, please run the advanced_analysis.py script to generate HTML maps.")
        
        try:
            # Load geolocation data
            import os
            import pandas as pd

            BASE_DIR = os.path.dirname(__file__)
            DATA_PATH = os.path.join(BASE_DIR, "..", "data", "geolocation_dataset.csv")

            geolocation_df = pd.read_csv(DATA_PATH)

            
            # Merge with customers
            customers_geo = customers_df.merge(
                geolocation_df.groupby("geolocation_zip_code_prefix").agg({
                    "geolocation_lat": "mean",
                    "geolocation_lng": "mean",
                    "geolocation_city": "first",
                    "geolocation_state": "first"
                }).reset_index(),
                left_on="customer_zip_code_prefix",
                right_on="geolocation_zip_code_prefix",
                how="left"
            )
            
            # Merge with main_df
            geo_df = main_df.merge(customers_geo, on="customer_id", how="left")
            
            # State analysis
            state_summary = geo_df.groupby("geolocation_state").agg({
                "order_id": "count",
                "price": "sum",
                "review_score": "mean"
            }).reset_index()
            state_summary.columns = ["State", "Total_Orders", "Total_Revenue", "Avg_Review"]
            state_summary = state_summary.sort_values("Total_Orders", ascending=False)
            
            # Key Metrics
            col1, col2, col3, col4 = st.columns(4)
            
            with col1:
                st.metric("Total States", f"{len(state_summary)}")
            with col2:
                top_state = state_summary.iloc[0]["State"]
                st.metric("Top State", top_state)
            with col3:
                top_orders = state_summary.iloc[0]["Total_Orders"]
                st.metric("Top State Orders", f"{top_orders:,}")
            with col4:
                concentration = (top_orders / state_summary["Total_Orders"].sum() * 100)
                st.metric("Concentration", f"{concentration:.1f}%")
            
            st.markdown("---")
            
            # Visualizations
            col1, col2 = st.columns(2)
            
            with col1:
                st.subheader("📦 Top 15 States by Orders")
                
                top_15_orders = state_summary.head(15)
                
                fig = px.bar(top_15_orders, x="Total_Orders", y="State",
                            orientation='h',
                            labels={"Total_Orders": "Number of Orders"},
                            color="Total_Orders",
                            color_continuous_scale="Blues")
                fig.update_layout(showlegend=False, yaxis={'categoryorder':'total ascending'})
                st.plotly_chart(fig, use_container_width=True)
            
            with col2:
                st.subheader("💰 Top 15 States by Revenue")
                
                top_15_revenue = state_summary.sort_values("Total_Revenue", ascending=False).head(15)
                
                fig = px.bar(top_15_revenue, x="Total_Revenue", y="State",
                            orientation='h',
                            labels={"Total_Revenue": "Total Revenue (R$)"},
                            color="Total_Revenue",
                            color_continuous_scale="Greens")
                fig.update_layout(showlegend=False, yaxis={'categoryorder':'total ascending'})
                st.plotly_chart(fig, use_container_width=True)
            
            # Map view
            st.markdown("---")
            st.subheader("🗺️ Geographic Distribution Map")
            
            # Prepare data for map
            state_coords = geo_df.groupby("geolocation_state").agg({
                "geolocation_lat": "mean",
                "geolocation_lng": "mean"
            }).reset_index()
            
            state_map_data = state_summary.merge(state_coords, 
                                                 left_on="State", 
                                                 right_on="geolocation_state")
            
            fig = px.scatter_geo(state_map_data,
                                lat="geolocation_lat",
                                lon="geolocation_lng",
                                size="Total_Orders",
                                color="Total_Revenue",
                                hover_name="State",
                                hover_data={"Total_Orders": True, 
                                           "Total_Revenue": ":,.2f",
                                           "Avg_Review": ":.2f",
                                           "geolocation_lat": False,
                                           "geolocation_lng": False},
                                color_continuous_scale="Viridis",
                                size_max=50)
            
            fig.update_geos(
                center=dict(lat=-14.2350, lon=-51.9253),
                projection_scale=3,
                showcountries=True,
                showcoastlines=True
            )
            
            fig.update_layout(height=600, margin={"r":0,"t":0,"l":0,"b":0})
            st.plotly_chart(fig, use_container_width=True)
            
            # Data Table
            st.markdown("---")
            st.subheader("📋 Complete State Statistics")
            
            display_df = state_summary.copy()
            display_df["Total_Revenue"] = display_df["Total_Revenue"].apply(lambda x: f"R$ {x:,.2f}")
            display_df["Avg_Review"] = display_df["Avg_Review"].apply(lambda x: f"{x:.2f}")
            
            st.dataframe(display_df, use_container_width=True, height=400)
            
        except FileNotFoundError:
            st.warning("⚠️ Geolocation dataset not found. Please ensure 'geolocation_dataset.csv' is available.")
            st.info("You can still view other analysis pages.")
    
    # PAGE PRODUCT CLUSTERING 
    elif page == "🎯 Product Clustering":
        st.header("🎯 Product Clustering - Manual Segmentation")
        
        st.markdown("""
        Products are segmented based on:
        - **Price Category**: Very Low → Very High
        - **Review Category**: Poor → Excellent
        - **Sales Performance**: Low Seller → Top Seller
        """)
        
        # Prepare product clustering
        product_data = main_df.groupby("product_id").agg({
            "price": "mean",
            "review_score": "mean",
            "order_id": "count"
        }).reset_index()
        product_data.columns = ["product_id", "Avg_Price", "Avg_Review", "Sales_Count"]
        
        # Filter
        product_data = product_data[
            (product_data["Avg_Price"] > 0) &
            (product_data["Avg_Price"] < 1000) &
            (product_data["Sales_Count"] >= 5)
        ]
        
        # Binning
        price_bins = [0, 50, 100, 200, 500, 1000]
        price_labels = ["Very Low", "Low", "Medium", "High", "Very High"]
        product_data["Price_Category"] = pd.cut(product_data["Avg_Price"], 
                                                bins=price_bins, labels=price_labels)
        
        review_bins = [0, 2, 3, 4, 5]
        review_labels = ["Poor", "Fair", "Good", "Excellent"]
        product_data["Review_Category"] = pd.cut(product_data["Avg_Review"], 
                                                 bins=review_bins, labels=review_labels)
        
        sales_quantiles = product_data["Sales_Count"].quantile([0, 0.25, 0.50, 0.75, 1.0])
        sales_bins = [sales_quantiles[q] for q in [0, 0.25, 0.50, 0.75, 1.0]]
        sales_labels = ["Low Seller", "Moderate Seller", "Good Seller", "Top Seller"]
        product_data["Sales_Performance"] = pd.cut(product_data["Sales_Count"], 
                                                   bins=sales_bins, labels=sales_labels,
                                                   duplicates='drop')
        
        # Segmentation
        def product_segment(row):
            price = row["Price_Category"]
            review = row["Review_Category"]
            sales = row["Sales_Performance"]
            
            if price in ["High", "Very High"] and review == "Excellent" and sales == "Top Seller":
                return "Premium Stars"
            elif price in ["Very Low", "Low"] and review in ["Good", "Excellent"] and sales in ["Good Seller", "Top Seller"]:
                return "Value Champions"
            elif review in ["Good", "Excellent"] and sales == "Low Seller":
                return "Hidden Gems"
            elif price in ["High", "Very High"] and review in ["Poor", "Fair"]:
                return "Overpriced"
            elif review in ["Poor", "Fair"]:
                return "Low Quality"
            elif sales in ["Good Seller", "Top Seller"] and review in ["Good", "Excellent"]:
                return "Best Sellers"
            elif price == "Medium" and review == "Good":
                return "Average Products"
            elif sales in ["Low Seller", "Moderate Seller"] and review == "Good":
                return "Slow Movers"
            else:
                return "Others"
        
        product_data["Product_Segment"] = product_data.apply(product_segment, axis=1)
        
        # Key Metrics
        col1, col2, col3, col4 = st.columns(4)
        
        with col1:
            st.metric("Total Products", f"{len(product_data):,}")
        with col2:
            st.metric("Avg Price", f"R$ {product_data['Avg_Price'].mean():.2f}")
        with col3:
            st.metric("Avg Review", f"{product_data['Avg_Review'].mean():.2f} ⭐")
        with col4:
            st.metric("Avg Sales", f"{product_data['Sales_Count'].mean():.0f} orders")
        
        st.markdown("---")
        
        # Category Distributions
        col1, col2 = st.columns(2)
        
        with col1:
            st.subheader("💰 Price Category Distribution")
            
            price_dist = product_data["Price_Category"].value_counts()
            
            fig = px.bar(x=price_dist.index, y=price_dist.values,
                        labels={"x": "Category", "y": "Number of Products"},
                        color=price_dist.values,
                        color_continuous_scale="Blues")
            fig.update_layout(showlegend=False)
            st.plotly_chart(fig, use_container_width=True)
        
        with col2:
            st.subheader("⭐ Review Category Distribution")
            
            review_dist = product_data["Review_Category"].value_counts()
            
            fig = px.bar(x=review_dist.index, y=review_dist.values,
                        labels={"x": "Category", "y": "Number of Products"},
                        color=review_dist.values,
                        color_continuous_scale="Greens")
            fig.update_layout(showlegend=False)
            st.plotly_chart(fig, use_container_width=True)
        
        # Product Segments
        st.markdown("---")
        st.subheader("🎯 Product Segment Distribution")
        
        segment_counts = product_data["Product_Segment"].value_counts()
        
        fig = px.bar(x=segment_counts.values, y=segment_counts.index,
                    orientation='h',
                    labels={"x": "Number of Products", "y": "Segment"},
                    color=segment_counts.values,
                    color_continuous_scale="Viridis")
        fig.update_layout(showlegend=False, yaxis={'categoryorder':'total ascending'})
        st.plotly_chart(fig, use_container_width=True)
        
        # Scatter Plot
        st.markdown("---")
        st.subheader("📊 Product Clustering Visualization")
        
        fig = px.scatter(product_data, x="Avg_Price", y="Avg_Review",
                        color="Product_Segment", size="Sales_Count",
                        hover_data=["product_id"],
                        labels={"Avg_Price": "Average Price (R$)", 
                               "Avg_Review": "Average Review Score"},
                        color_discrete_sequence=px.colors.qualitative.Set3)
        fig.update_layout(height=600)
        st.plotly_chart(fig, use_container_width=True)
        
        # Segment Recommendations
        st.markdown("---")
        st.subheader("💡 Segment Strategies")
        
        strategies = {
            "Premium Stars": "🏆 Maintain quality, premium branding, VIP marketing",
            "Value Champions": "💎 Scale up production, mass marketing, stock optimization",
            "Hidden Gems": "💎 Boost visibility, increase marketing budget, featured products",
            "Best Sellers": "🔥 Continue momentum, ensure stock availability, cross-sell",
            "Overpriced": "⚠️ Reduce price OR improve quality, conduct market research",
            "Low Quality": "❌ Investigate issues, improve or consider discontinuing",
            "Slow Movers": "🐌 Investigate barriers, reposition, bundle with popular items"
        }
        
        for segment, strategy in strategies.items():
            count = len(product_data[product_data["Product_Segment"] == segment])
            if count > 0:
                st.info(f"**{segment}** ({count:,} products): {strategy}")
    
    # PAGE CONCLUSIONS 
    elif page == "📋 Conclusions":
        st.header("📋 Conclusions & Recommendations")
        
        st.markdown("---")
        
        # Summary
        st.subheader("🎯 Executive Summary")
        
        st.markdown("""
        This dashboard presents comprehensive analysis of the Brazilian E-Commerce dataset from Olist,
        covering business performance, customer behavior, geographic distribution, and product segmentation.
        """)
        
        st.markdown("---")
        
        # Key Findings
        col1, col2 = st.columns(2)
        
        with col1:
            st.subheader("🔍 Key Findings")
            
            st.success("""
            **Business Performance:**
            - Strong overall customer satisfaction (avg 4.08/5)
            - Excellent delivery performance (>90% on-time)
            - Diverse product portfolio across 70+ categories
            """)
            
            st.info("""
            **Delivery Impact (2017):**
            - On-time delivery: 4.15 ⭐ average rating
            - Delayed delivery: 2.45 ⭐ average rating
            - **40.9% drop** in satisfaction due to delays
            - Clear correlation between delivery and satisfaction
            """)
            
            st.warning("""
            **Geographic Concentration:**
            - Business heavily concentrated in specific states
            - Top state accounts for significant market share
            - Opportunity for geographic expansion
            - Regional differences in customer behavior
            """)
        
        with col2:
            st.subheader("💡 Strategic Recommendations")
            
            st.markdown("""
            **1. Delivery Excellence:**
            - ⚡ Invest in logistics infrastructure
            - 📦 Improve delivery time tracking
            - 🎯 Set realistic delivery estimates
            - 🚚 Partner with reliable carriers
            
            **2. Customer Retention:**
            - 🏆 Focus on Champions and Loyal segments
            - ⚠️ Implement win-back campaigns for At Risk
            - 🌟 Nurture Potential Loyalists
            - 📧 Re-engagement for Hibernating customers
            
            **3. Product Strategy:**
            - 💎 Scale up Value Champions
            - 🏆 Maintain Premium Stars quality
            - 💡 Boost visibility of Hidden Gems
            - ❌ Fix or discontinue Low Quality products
            
            **4. Geographic Expansion:**
            - 🗺️ Identify underserved regions
            - 📍 Optimize distribution centers
            - 🎯 Localized marketing campaigns
            - 🤝 Regional partnerships
            """)
        
        st.markdown("---")
        
        # Data-Driven Insights
        st.subheader("📊 Data-Driven Insights")
        
        tab1, tab2, tab3 = st.tabs(["Customer Insights", "Product Insights", "Operational Insights"])
        
        with tab1:
            st.markdown("""
            **Customer Behavior Patterns:**
            - Majority are one-time buyers - opportunity for loyalty programs
            - High satisfaction when delivery expectations are met
            - Price sensitivity varies by segment
            - Review behavior: customers either love it (5★) or hate it (1★)
            
            **Segmentation Value:**
            - Champions represent highest value - deserve VIP treatment
            - Large "Hibernating" segment - reactivation potential
            - New customers need onboarding for retention
            - At Risk customers require urgent attention
            """)
        
        with tab2:
            st.markdown("""
            **Product Portfolio:**
            - Top 5 categories drive 65% of revenue
            - Clear differentiation in pricing strategies
            - Quality (review score) correlates with sales
            - Hidden gems exist - marketing opportunity
            
            **Category Strategies:**
            - Health & Beauty: Volume leader - scale up
            - Watches & Gifts: Premium pricing works
            - Bed Bath Table: Mass market success
            - Opportunity to optimize slow movers
            """)
        
        with tab3:
            st.markdown("""
            **Operational Excellence:**
            - Delivery performance is critical differentiator
            - Late deliveries cause severe satisfaction drop
            - Geographic concentration presents risk and opportunity
            - Fulfillment rate is excellent (96%+)
            
            **Improvement Areas:**
            - Reduce delivery delays (currently 7.3%)
            - Better delivery time estimation
            - Expand to underserved regions
            - Optimize logistics network
            """)
        
        st.markdown("---")
        
        # Action Plan
        st.subheader("🚀 Action Plan")
        
        st.markdown("""
        **Immediate Actions (0-3 months):**
        1. ✅ Launch win-back campaign for At Risk customers
        2. ✅ Improve delivery tracking and communication
        3. ✅ Boost marketing for Hidden Gems products
        4. ✅ Implement VIP program for Champions
        
        **Short-term Actions (3-6 months):**
        1. 📊 A/B test pricing for Overpriced products
        2. 🗺️ Pilot expansion in 2-3 new regions
        3. 📦 Partner with additional logistics providers
        4. 🎯 Develop category-specific marketing campaigns
        
        **Long-term Strategy (6-12 months):**
        1. 🏗️ Build distribution centers in key regions
        2. 🤖 Implement predictive analytics for inventory
        3. 🌐 Develop regional customization strategy
        4. 📈 Expand product portfolio in winning categories
        """)
        
        st.markdown("---")
        
        # Footer
        st.info("""
        **Dashboard Information:**
        - Data Period: 2016-2018
        - Total Records Analyzed: 100,000+ orders
        - Analysis Methods: RFM, Geospatial, Manual Clustering
        - Last Updated: 2024
        
        For detailed analysis code and methodology, please refer to the accompanying Python scripts.
        """)

else:
    st.error("❌ Unable to load data. Please ensure all CSV files are in the correct directory.")
    st.info("""
    **Required files:**
    - orders_dataset.csv
    - order_items_dataset.csv
    - products_dataset.csv
    - customers_dataset.csv
    - order_reviews_dataset.csv
    - product_category_name_translation.csv
    - geolocation_dataset.csv (optional, for geospatial analysis)
    """)