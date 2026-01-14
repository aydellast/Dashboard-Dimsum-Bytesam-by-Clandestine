import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go

# ===============================
# 1. KONFIGURASI HALAMAN
# ===============================
st.set_page_config(
    page_title="Dashboard Dimsum Bytesam",
    page_icon="🥟",
    layout="wide"
)

# ===============================
# 2. CUSTOM CSS (PREMIUM UI STYLE)
# ===============================
st.markdown("""
<style>
    /* 1. Import Font Keren */
    @import url('https://fonts.googleapis.com/css2?family=Poppins:wght@300;400;600;800&display=swap');

    html, body, [class*="css"]  {
        font-family: 'Poppins', sans-serif;
    }

    /* 2. Background Aplikasi */
    .stApp {
        background-color: #FDFDFD; /* Putih bersih */
    }

    /* 3. Styling Sidebar (Menu Kiri) */
    section[data-testid="stSidebar"] {
        background: linear-gradient(180deg, #FFF8E1 0%, #FFECB3 100%);
        border-right: 1px solid #FFD54F;
        box-shadow: 2px 0 10px rgba(0,0,0,0.05);
    }
    
    [data-testid="stSidebar"] h1 {
        color: #D84315 !important;
        font-size: 24px;
        text-shadow: 1px 1px 2px rgba(0,0,0,0.1);
    }
    
    [data-testid="stSidebar"] p, [data-testid="stSidebar"] span, [data-testid="stSidebar"] label {
        color: #5D4037 !important;
        font-weight: 500;
    }

    /* 4. Styling Header Utama */
    .block-container h1 {
        background: linear-gradient(90deg, #FF6F00 0%, #FF8F00 100%);
        padding: 20px;
        border-radius: 15px;
        color: white !important;
        box-shadow: 0 4px 15px rgba(255, 111, 0, 0.3);
        text-align: center;
        margin-bottom: 20px;
        font-size: 2.5rem;
    }

    h2, h3 {
        color: #BF360C !important;
        border-left: 5px solid #FF6F00;
        padding-left: 10px;
        margin-top: 30px;
    }

    /* 5. KARTU METRIC (KPI) */
    div[data-testid="stMetric"] {
        background-color: #FFFFFF !important;
        border: none !important;
        padding: 20px !important;
        border-radius: 15px;
        box-shadow: 0 4px 6px rgba(0, 0, 0, 0.05), 0 1px 3px rgba(0, 0, 0, 0.08);
        border-left: 8px solid #FF6F00 !important;
        transition: all 0.3s ease;
        position: relative;
        overflow: hidden;
    }

    div[data-testid="stMetric"]:hover {
        transform: translateY(-5px) scale(1.02);
        box-shadow: 0 10px 20px rgba(255, 111, 0, 0.2);
        border-left: 8px solid #D84315 !important;
    }

    div[data-testid="stMetricLabel"] {
        color: #757575 !important;
        font-size: 14px !important;
        font-weight: 600;
        text-transform: uppercase;
        letter-spacing: 1px;
    }

    div[data-testid="stMetricValue"] {
        color: #E65100 !important;
        font-size: 32px !important;
        font-weight: 800;
        text-shadow: 1px 1px 0px rgba(0,0,0,0.1);
    }

    /* 6. Tombol */
    .stButton > button {
        background: linear-gradient(45deg, #FF6F00, #FF8F00);
        color: white;
        border-radius: 10px;
        border: none;
        box-shadow: 0 4px 6px rgba(255, 111, 0, 0.3);
        height: 50px;
        font-weight: bold;
        transition: 0.3s;
    }
    .stButton > button:hover {
        transform: translateY(-2px);
        box-shadow: 0 6px 12px rgba(255, 111, 0, 0.4);
    }
    
    /* 7. Pesan Alert (Success/Warning/Info) */
div[data-testid="stAlert"] {
        padding: 1rem !important;
    }
    
    div[data-testid="stAlert"] p, 
    div[data-testid="stAlert"] span, 
    div[data-testid="stAlert"] li,
    div[data-testid="stAlert"] h4 {
        color: #37474F !important; /* <--- Ini warnanya (Bukan hitam pekat, tapi abu tua deep) */
    }
    
    /* Ikon (Tanda seru/Info) mengikuti warna teks */
    div[data-testid="stAlert"] svg {
        fill: #37474F !important;
        
</style>
""", unsafe_allow_html=True)

# ===============================
# 3. LOAD DATA
# ===============================
@st.cache_data
def load_data():
    try:
        # GANTI URL DI BAWAH INI dengan link RAW yang kamu copy tadi
        url_csv = "https://raw.githubusercontent.com/aydellast/Dashboard-Dimsum-Bytesam-by-Clandestine/refs/heads/main/dashboard_UAS_KWU/dataset_penjualan.csv"
        
        df = pd.read_csv(url_csv) # Baca langsung dari internet
        df["Tanggal"] = pd.to_datetime(df["Tanggal"])
        return df
    except Exception as e:
        st.error(f"❌ Terjadi kesalahan saat membaca data: {e}")
        return None

df = load_data()

if df is None:
    st.error("❌ File 'dataset_penjualan.csv' tidak ditemukan.")
    st.stop()

# ===============================
# 4. SIDEBAR
# ===============================
st.sidebar.markdown("# 🥟 Dimsum Bytesam")
st.sidebar.caption("Dashboard Monitoring Penjualan")

# Filter
st.sidebar.header("📅 Filter Periode")
min_date = df["Tanggal"].min().date()
max_date = df["Tanggal"].max().date()
start_date = st.sidebar.date_input("Mulai", min_date, min_value=min_date, max_value=max_date)
end_date = st.sidebar.date_input("Sampai", max_date, min_value=min_date, max_value=max_date)

start_date = pd.to_datetime(start_date)
end_date = pd.to_datetime(end_date)

if start_date > end_date:
    st.sidebar.error("Tanggal error!")
    st.stop()

df_filtered = df[(df["Tanggal"] >= start_date) & (df["Tanggal"] <= end_date)]

# Navigasi
st.sidebar.markdown("---")
if "menu" not in st.session_state:
    st.session_state.menu = "Analisis Utama"

def nav_button(label):
    if st.sidebar.button(label):
        st.session_state.menu = label

st.sidebar.markdown("### 🧭 Menu Navigasi")
nav_button("Analisis Utama")
nav_button("Insight Bisnis")
nav_button("Data Mentah")
menu = st.session_state.menu

# ===============================
# 5. HEADER (JUDUL TETAP ADA DI SEMUA HALAMAN)
# ===============================
st.title("🔥 Dashboard Business Performance")
st.markdown(f"**Periode Evaluasi:** {start_date.strftime('%d %b %Y')} - {end_date.strftime('%d %b %Y')}")
st.markdown("---")

# --- KALKULASI DATA (Tetap dihitung global, tapi ditampilkan nanti) ---
total_revenue = df_filtered["Total Revenue"].sum()
total_hpp = df_filtered["Total HPP"].sum()
total_profit = df_filtered["Total Profit"].sum()
total_qty = df_filtered["Qty"].sum()
profit_margin = (total_profit / total_revenue * 100) if total_revenue > 0 else 0

# Data Processing untuk Grafik
daily_trend = df_filtered.groupby("Tanggal")[["Total Revenue", "Total HPP", "Total Profit", "Qty"]].sum().reset_index()
product_analysis = df_filtered.groupby("Varian")[["Qty", "Total Profit"]].sum().reset_index()
payment_analysis = df_filtered.groupby("Metode Bayar")[["Qty"]].sum().reset_index()

color_palette = ['#FF6F00', '#D84315', '#FFAB00', '#FFD54F', '#BF360C']

# ===============================
# 6. KONTEN UTAMA (LOGIKA MENU)
# ===============================

if menu == "Analisis Utama":
    # === KPI HANYA MUNCUL DISINI ===
    # Baris 1: 3 Kolom
    col1, col2, col3 = st.columns(3)
    with col1:
        st.metric("💰 Total Revenue", f"Rp {total_revenue:,.0f}")
    with col2:
        st.metric("📦 Produk Terjual", f"{total_qty} pcs")
    with col3:
        st.metric("💸 Total Biaya (HPP)", f"Rp {total_hpp:,.0f}")

    # Baris 2: 2 Kolom
    st.markdown("<br>", unsafe_allow_html=True)
    col4, col5 = st.columns(2)
    with col4:
        st.metric("📈 Total Profit", f"Rp {total_profit:,.0f}")
    with col5:
        st.metric("📊 Profit Margin", f"{profit_margin:.1f}%")
    
    st.markdown("---")
    # ===============================

    st.subheader("📊 Grafik Tren Keuangan")
    st.caption("Tren Harian Revenue, HPP, dan Profit dari Waktu ke Waktu")

    fig_trend = go.Figure()
    fig_trend.add_trace(go.Scatter(x=daily_trend["Tanggal"], y=daily_trend["Total Revenue"], mode='lines+markers', name='Revenue', line=dict(color='#FF6F00', width=3)))
    fig_trend.add_trace(go.Scatter(x=daily_trend["Tanggal"], y=daily_trend["Total HPP"], mode='lines+markers', name='Total HPP (Modal)', line=dict(color='#FFCA28', width=2, dash='dash')))
    fig_trend.add_trace(go.Scatter(x=daily_trend["Tanggal"], y=daily_trend["Total Profit"], mode='lines+markers', name='Profit', line=dict(color='#D84315', width=3, dash='dot')))

    fig_trend.update_layout(
        title="Tren Pemasukan vs Modal vs Keuntungan",
        plot_bgcolor='rgba(0,0,0,0)', paper_bgcolor='rgba(0,0,0,0)', 
        hovermode="x unified", yaxis=dict(title="Rupiah"), legend=dict(orientation="h", y=1.1)
    )
    st.plotly_chart(fig_trend, use_container_width=True)

    c1, c2 = st.columns(2)
    with c1:
        fig_pie = px.pie(payment_analysis, names="Metode Bayar", values="Qty", title="Distribusi Metode Pembayaran", color_discrete_sequence=color_palette, hole=0.4)
        fig_pie.update_layout(plot_bgcolor='rgba(0,0,0,0)', paper_bgcolor='rgba(0,0,0,0)')
        st.plotly_chart(fig_pie, use_container_width=True)
    
    with c2:
        fig_bar = px.bar(product_analysis.sort_values("Qty"), x="Qty", y="Varian", orientation='h', title="Produk Terlaris", color="Qty", color_continuous_scale='OrRd')
        fig_bar.update_layout(plot_bgcolor='rgba(0,0,0,0)', paper_bgcolor='rgba(0,0,0,0)')
        st.plotly_chart(fig_bar, use_container_width=True)

# --- BAGIAN INSIGHT (LANGSUNG KONTEN, TANPA KPI GLOBAL) ---
elif menu == "Insight Bisnis":
    # Karena KPI Global di atas hilang, konten ini akan otomatis naik ke atas (Auto Scroll Effect)
    st.subheader("🧠 Insight & Evaluasi Bisnis (Executive Summary)")
    
    modal_awal = 200000
    net_profit_accumulation = total_profit
    roi = (net_profit_accumulation / modal_awal) * 100
    sisa_lebih = net_profit_accumulation - modal_awal

    st.markdown("#### 1. Performa Keuangan vs Modal Awal")
    col_m1, col_m2, col_m3 = st.columns(3)
    col_m1.metric("💵 Modal Awal (RAB)", f"Rp {modal_awal:,.0f}")
    col_m2.metric("💰 Total Profit Saat Ini", f"Rp {total_profit:,.0f}")
    col_m3.metric("📈 ROI (Balik Modal)", f"{roi:.1f}%", delta="Positif")

    st.markdown("---")

    st.markdown("#### 2. Analisis Titik Balik Modal (Break Even Point)")
    st.success(f"""
    **✅ STATUS: SUDAH BALIK MODAL (PROFITABLE)**
    
    Berdasarkan evaluasi kinerja dari periode sebelumnya (UTS) hingga saat ini, usaha **Dimsum Bytesam** menunjukkan performa yang sangat sehat secara finansial.
    
    * **Efisiensi Modal:** Dengan modal awal yang efisien sebesar **Rp {modal_awal:,.0f}**, usaha mampu menghasilkan perputaran kas yang cepat.
    * **Pencapaian BEP:** Titik Impas (Break Even Point) telah berhasil dicapai secara historis pada **penjualan unit ke-45**. 
    * **Kondisi Saat Ini:** Sejak melewati penjualan ke-45 tersebut, seluruh pendapatan yang masuk telah menjadi **keuntungan bersih (pure profit)** bagi usaha. Saat ini, total keuntungan telah melampaui modal awal dengan surplus sebesar **Rp {sisa_lebih:,.0f}**.
    """)

    st.markdown("#### 3. Evaluasi Produk & Rekomendasi Strategi")
    best_product = product_analysis.sort_values("Qty", ascending=False).iloc[0]
    worst_product = product_analysis.sort_values("Qty", ascending=True).iloc[0]

    c_strat1, c_strat2 = st.columns(2)
    with c_strat1:
        st.info(f"""
        **🏆 Produk Unggulan (Star): {best_product['Varian']}**
        
        Varian ini menjadi penyumbang volume penjualan terbesar ({best_product['Qty']} pcs).
        
        **Rekomendasi Strategi:**
        * Jadikan produk ini sebagai "hook" dalam materi promosi (poster/story IG).
        * Pastikan stok bahan baku varian ini selalu melebih varian lain (safety stock 20%).
        """)
    with c_strat2:
        st.warning(f"""
        **⚠️ Produk Perlu Evaluasi: {worst_product['Varian']}**
        
        Varian ini memiliki performa penjualan terendah ({worst_product['Qty']} pcs) dibandingkan yang lain.
        
        **Rekomendasi Strategi:**
        * **Bundling:** Jual varian ini dalam paket hemat bersama {best_product['Varian']} untuk mendorong trial.
        * **Review:** Lakukan tes rasa ulang atau tanyakan feedback pelanggan kenapa varian ini kurang diminati.
        """)

    st.markdown("#### 4. Kesimpulan Akhir Periode")
    st.write(f"""
    Secara keseluruhan, **Dimsum Bytesam** layak dinyatakan sebagai usaha yang **menguntungkan (Feasible)**. 
    Dengan Margin Keuntungan sebesar **{profit_margin:.1f}%**, usaha memiliki ketahanan yang cukup baik terhadap fluktuasi harga bahan baku. 
    Fokus periode berikutnya adalah meningkatkan **Average Order Value (AOV)** agar pelanggan membeli lebih dari 1 porsi per transaksi.
    """)

# --- MENU DATA MENTAH (Full Tabel) ---
elif menu == "Data Mentah":
    st.subheader("📂 Data Penjualan Mentah")
    # Langsung tabel, bersih tanpa angka-angka di atas

    st.dataframe(df_filtered.style.background_gradient(cmap="OrRd"), use_container_width=True)



